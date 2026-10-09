# /// script
# requires-python = ">=3.13,<3.14"
# dependencies = ["httpx>=0.27,<1", "shapely>=2,<3", "openpyxl>=3.1,<4"]
# ///
"""Ceļu kartes datubāzes būve un aktualizēšana (shēma: db_shema.sql).

    uv run datubaze.py buvet [--parrakstit]     # DB no nulles (visi soļi)
    uv run datubaze.py atjaunot [--piespiest]   # statiskajiem hash skip; notikumi vienmēr
    uv run datubaze.py statuss

Karodziņi: --bez-kataloga, --bez-statiskajiem, --bez-notikumiem (soļu
izlaišana), --db (cits datubāzes ceļš), --piespiest (ignorē hash).

Soļi: katalogs (DCAT bez atslēgas; DCAT saturā ir laika zīmogi, tāpēc hash
gandrīz vienmēr mainās — solis ir lēts un vienkārši pārlādē), statiskie
(9 slāņu kopas ar atslēgām; nulles ielāde pēc pilnas tabulas NEpārraksta
vecos datus un neieraksta hash), notikumi (8 DATEX II plūsmas — vēsture
tikai aug; `redzets` laiks ļauj skatam rādīt tikai pēdējā ievākumā redzētos).
Atslēgas: dati/nap_atslegas.json (katrai kopai sava; bez faila lejupielādes
soļi izlaižas ar paziņojumu). Avotu īpatnības (pārbaudītas 2026-07-31):
melnajiem punktiem NAV koordinātu; masas ierobežojumi nāk kā GeoJSON caur
plūsmas mehānismu; meteo mērījumiem sava DATEX publikācija bez koordinātām
(piesaiste caur meteo_vietas staciju id); DATEX ligzdo vienādvārdu elementus
(<friction><friction>), tāpēc apakšmeklēšana NEDRĪKST atgriezt pašu elementu.
"""
import argparse
import csv
import datetime
import hashlib
import io
import json
import pathlib
import re
import sqlite3
import sys
import xml.etree.ElementTree as ET

import httpx

HERE = pathlib.Path(__file__).resolve().parent
DATI = HERE / "dati"
DB_CELS = DATI / "celi.db"
SHEMA = HERE / "db_shema.sql"
ATSLEGAS_FAILS = DATI / "nap_atslegas.json"
ARHIVS = DATI / "arhivs"

BAZE = "https://www.transportdata.gov.lv"
DCAT_URL = f"{BAZE}/api/v1/subscriber/metadata_dcat"
INFO_URL = f"{BAZE}/api/v1/metadata/file/info"
LEJUP_URL = f"{BAZE}/api/v1/get/file/download-file"

XSI = "{http://www.w3.org/2001/XMLSchema-instance}type"
RDF_ABOUT = "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about"
RDF_RESURSS = "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource"
XML_LANG = "{http://www.w3.org/XML/1998/namespace}lang"

STATISKIE = ["valsts_celu_tikls", "celu_posmi_atributi", "celu_klasifikacija",
             "prioritarie_celi", "melnie_punkti", "atruma_zimes", "gajeju_celi",
             "masas_ierobezojumi", "meteo_vietas"]
STATISKO_TABULA = {"valsts_celu_tikls": "celu_posms",
                   "celu_posmi_atributi": "celu_posms",
                   "celu_klasifikacija": "celu_posms",
                   "prioritarie_celi": "celu_posms",
                   "melnie_punkti": "cela_punkts",
                   "atruma_zimes": "cela_punkts",
                   "meteo_vietas": "cela_punkts",
                   "gajeju_celi": "cela_papildslanis",
                   "masas_ierobezojumi": "cela_papildslanis"}
NOTIKUMU_TIPS = {"celu_slegumi": "slegums", "joslu_slegumi": "joslas_slegums",
                 "remontdarbi": "remonts", "islaicigie_remontdarbi": "remonts",
                 "slidens_sic": "slidens",
                 "slikti_apstakli_uzturetaji": "slikti_apstakli",
                 "negadijumi": "negadijums", "meteo_merijumi": "meteo_merijums"}

CELA_NR = re.compile(r"\b([APV]\d{1,4})\b")


# ------------------------------------------------------------------ palīgi

def atslegas():
    """dati/nap_atslegas.json saturs vai None (tolerants trūkums)."""
    if not ATSLEGAS_FAILS.exists():
        return None
    return json.loads(ATSLEGAS_FAILS.read_text(encoding="utf-8"))["kopas"]


def ievaks(con, avots, hash_, skaits, piezimes=None, savakts=None):
    cur = con.execute(
        "INSERT INTO ievaks (avots, savakts, satura_hash, ierakstu_skaits, piezimes)"
        " VALUES (?,?,?,?,?)",
        (avots, savakts or datetime.datetime.now().isoformat(timespec="seconds"),
         hash_, skaits, piezimes))
    return cur.lastrowid


def pedejais_hash(con, avots):
    r = con.execute("SELECT satura_hash FROM ievaks WHERE avots=?"
                    " ORDER BY ievaks_id DESC LIMIT 1", (avots,)).fetchone()
    return r[0] if r else None


def lejupieladet(klients, atslega, fmt, file_id="1"):
    """(saturs, sha256) vai (None, None) pie 204. Kļūdas met izņēmumu.

    fmt=None -> format lauku neiekļauj (vienformāta faili, piem. CSV — API
    enum pieļauj tikai xml/geojson, tāpēc CSV prasa bez format).
    """
    kermenis = {"file_id": file_id}
    if fmt:
        kermenis["format"] = fmt
    r = klients.post(LEJUP_URL, headers={"x-api-key": atslega}, json=kermenis)
    if r.status_code == 204:
        return None, None
    r.raise_for_status()
    return r.content, hashlib.sha256(r.content).hexdigest()


def faila_id(klients, atslega):
    """Pirmā faila id kopām ar lejupielade='faili' (vai None)."""
    r = klients.get(INFO_URL, headers={"x-api-key": atslega})
    r.raise_for_status()
    faili = r.json().get("files") or []
    return str(faili[0]["file_id"]) if faili else None


def arhivet(slug, saturs, ext):
    ARHIVS.mkdir(parents=True, exist_ok=True)
    (ARHIVS / f"{datetime.date.today():%Y%m%d}_{slug}.{ext}").write_bytes(saturs)


def visi(el, tags):
    """Pēcteči (BEZ paša el!) ar doto lokālo vārdu. DATEX ligzdo vienādvārdu
    elementus (<friction><friction>0.82</>), tāpēc pats el jāizslēdz — citādi
    apakšmeklēšana atgriež vecāku ar atstarpju tekstu un vērtība pazūd."""
    return (e for e in el.iter() if e is not el
            and e.tag.rsplit("}", 1)[-1] == tags)


def pirmais(el, tags):
    return next(visi(el, tags), None)


def _teksts(el, tags):
    for e in visi(el, tags):
        if e.text and e.text.strip():
            return e.text.strip()
    return None


def nav_none(v):
    """NAP GeoJSON tukšums mēdz būt burtisks teksts 'None' — normalizē uz None."""
    if v is None:
        return None
    v = str(v).strip()
    return None if v in ("", "None") else v


def skaitlis(v):
    v = nav_none(v)
    if v is None:
        return None
    try:
        return float(str(v).replace(",", "."))
    except ValueError:
        return None


def geo_wkb(geometrija):
    """GeoJSON geometry -> (wkb, bounds) vai (None, None); Z ass tiek nomesta."""
    if not geometrija or geometrija.get("coordinates") is None:
        return None, None
    from shapely.geometry import shape
    from shapely import force_2d, to_wkb
    g = force_2d(shape(geometrija))
    if g.is_empty:
        return None, None
    return to_wkb(g), g.bounds


def kompakts_json(pari):
    """JSON tikai no aizpildītām vērtībām (vai None, ja nekā nav)."""
    tirs = {k: v for k, v in pari.items() if v not in (None, "", [], False)}
    return json.dumps(tirs, ensure_ascii=False, sort_keys=True) if tirs else None


# ------------------------------------------------------------------ 1. katalogs

def solis_katalogs(con, klients, piespiest):
    print("1) NAP katalogs (DCAT, bez atslēgas) ...", flush=True)
    r = klients.get(DCAT_URL)
    r.raise_for_status()
    h = hashlib.sha256(r.content).hexdigest()
    if h == pedejais_hash(con, "katalogs") and not piespiest:
        print("  katalogs nav mainījies — izlaists")
        return
    sakne = ET.fromstring(r.content)
    kartes = {(k.get("card") or "") for k in (atslegas() or {}).values()}
    esosie = {r[0] for r in con.execute("SELECT dataset_id FROM nap_katalogs")}
    n, jauni = 0, []
    for ds in visi(sakne, "Dataset"):
        m = re.search(r"/card/([0-9a-f-]{36})", ds.get(RDF_ABOUT) or "")
        if not m:
            continue
        did = m.group(1)
        nosaukumi = {}
        for t in ds.findall("{*}title"):
            nosaukumi[t.get(XML_LANG) or "en"] = (t.text or "").strip()
        temas = [e.get(RDF_RESURSS, "").rsplit("/", 1)[-1]
                 for e in ds.findall("{*}mobilityTheme")]
        formati = {e.get(RDF_RESURSS, "").rsplit("/", 1)[-1]
                   for e in visi(ds, "format")}
        ritms = next((e.get(RDF_RESURSS, "").rsplit("/", 1)[-1]
                      for e in ds.findall("{*}accrualPeriodicity")), None)
        izdevejs = next((v.text for v in visi(ds, "name") if v.text), None)
        modificets = next((v.text for v in ds.findall("{*}modified")), None)
        con.execute("""INSERT INTO nap_katalogs
            (dataset_id, nosaukums, nosaukums_lv, temas, formats, atjaunosana,
             izdevejs, modificets, abonets)
            VALUES (?,?,?,?,?,?,?,?,?)
            ON CONFLICT(dataset_id) DO UPDATE SET nosaukums=excluded.nosaukums,
              nosaukums_lv=excluded.nosaukums_lv, temas=excluded.temas,
              formats=excluded.formats, atjaunosana=excluded.atjaunosana,
              izdevejs=excluded.izdevejs, modificets=excluded.modificets,
              abonets=excluded.abonets""",
            (did, nosaukumi.get("en") or nosaukumi.get("lv") or did,
             nosaukumi.get("lv"), ";".join(t for t in temas if t) or None,
             ";".join(sorted(f for f in formati if f)) or None, ritms,
             izdevejs, modificets, 1 if did in kartes else 0))
        if did not in esosie:
            jauni.append(nosaukumi.get("lv") or nosaukumi.get("en") or did)
        n += 1
    if n == 0:
        # DCAT struktūra mainījusies? Neierakstam hash — nākamreiz mēģinās vēlreiz.
        con.rollback()
        print("  ! katalogā izparsētas 0 kopas — hash NAV ierakstīts, dati nav"
              " aiztikti (DCAT formāts mainījies?)", file=sys.stderr)
        return
    ievaks(con, "katalogs", h, n)
    con.commit()
    print(f"  kopas katalogā: {n}"
          + (f"; JAUNAS: {', '.join(jauni[:5])}" if jauni and esosie else ""))


# ------------------------------------------------------------------ 2. statiskie

def _ielade_celu_posmus(con, slug, dati):
    n, bez_geo = 0, 0
    for f in dati["features"]:
        p = f.get("properties") or {}
        wkb, robezas = geo_wkb(f.get("geometry"))
        if wkb is None:
            bez_geo += 1
            continue
        platums = skaitlis(p.get("autocela_platums"))
        joslas = skaitlis(p.get("brauksanas_joslu_skaits"))
        con.execute("""INSERT INTO celu_posms (kopa, cela_nr, klase, nosaukums,
              prioritars, platums_m, joslas, garums_m, atribūti, wkb, srid,
              minx, miny, maxx, maxy) VALUES (?,?,?,?,?,?,?,NULL,?,?,4326,?,?,?,?)""",
            (slug, nav_none(p.get("ac_index")) or nav_none(p.get("routeid")),
             nav_none(p.get("ac_type")), nav_none(p.get("ac_name")),
             1 if slug == "prioritarie_celi" else 0,
             platums, int(joslas) if joslas else None,
             kompakts_json({"routeid": nav_none(p.get("routeid")),
                            "ac_part": nav_none(p.get("ac_part")),
                            "e_index": nav_none(p.get("e_index")),
                            "fromdate": nav_none(p.get("fromdate")),
                            "todate": nav_none(p.get("todate")),
                            # vienība nav apstiprināta — tāpēc ne garums_m kolonnā
                            "shape_leng": skaitlis(p.get("Shape_Leng"))}),
             wkb, *robezas))
        n += 1
    return n, (f"{bez_geo} posmi bez ģeometrijas izlaisti" if bez_geo else None)


MP_PILNAIS_XLSX = HERE / "dokumentacija" / "paraugi" / "melnie_punkti_2020_2022_pilns.xlsx"
MP_SLANIS = DATI / "slani" / "melnie_punkti_lv.geojson"


def _mp_atslega(t):
    """Aprakstu salīdzināšanas atslēga (NAP CSV un lvceli.lv XLSX teksti
    atšķiras ar drukas kļūdām/atstarpēm — translit + tikai burti/cipari)."""
    t = (t or "").lower().translate(str.maketrans("āčēģīķļņšūž", "acegiklnsuz"))
    return re.sub(r"[^0-9a-z]", "", t)[:28]


def _ielade_melnos_punktus(con, slug, saturs):
    """Trīs avotu apvienojums (visi lokāli, izsekojami atribūtos):
    1. NAP CSV (šis lejupielādētais saturs) — kanoniskais NAP saraksts, bet
       bez koordinātām/ceļa/km un ar kļūdām (nepilna lvceli.lv kopija);
    2. lvceli.lv PILNAIS 2020.–2022. XLSX (dokumentacija/paraugi/) — pamatceļš,
       km un CSNg statistika visiem 38 punktiem; ja fails ir, tas kļūst par bāzi;
    3. atvasinātās koordinātas no dati/slani/melnie_punkti_lv.geojson
       (skripti/melnie_punkti_slanis.py: km interpolācija ar per-ceļa
       kalibrāciju + multi-modeļu orientieru lokalizācija ar verifikāciju).
    """
    # 1) NAP CSV apraksti (arī tad, ja XLSX ir — krustpārbaudei ievaks piezīmē)
    teksts = saturs.decode("utf-8-sig", errors="replace")
    rindas = list(csv.reader(io.StringIO(teksts)))
    galvene = rindas[0]
    csv_apraksti, anomalijas = [], 0
    for r in rindas[1:]:
        if not any(v.strip() for v in r):
            continue
        if len(r) > len(galvene):     # zināma bojāta rinda (pēdiņa name laukā)
            papildu = len(r) - len(galvene)
            r = r[:3] + [",".join(r[3:4 + papildu])] + r[4 + papildu:]
            anomalijas += 1
        vards = (dict(zip(galvene, r)).get("name") or "").strip()
        if vards:
            csv_apraksti.append(vards)

    # 3) atvasinātās koordinātas pēc apraksta atslēgas
    koordinatas = {}
    if MP_SLANIS.exists():
        for f in json.loads(MP_SLANIS.read_text(encoding="utf-8"))["features"]:
            ip = f["properties"]
            koordinatas[_mp_atslega(ip["apraksts"])] = (
                f["geometry"]["coordinates"], ip.get("ticamiba"), ip.get("metode"))

    piezimes = [f"{anomalijas} CSV rindas ar bojātu citēšanu salabotas"] \
        if anomalijas else []
    n = 0
    if MP_PILNAIS_XLSX.exists():
        # 2) pilnais XLSX kā bāze
        import openpyxl
        csv_atslegas = {_mp_atslega(t) for t in csv_apraksti}
        xlsx_atslegas = set()
        lapa = openpyxl.load_workbook(MP_PILNAIS_XLSX).active
        for r in lapa.iter_rows(min_row=5, values_only=True):
            nr, cels, km, csng, ar_ciet, boja, ievain, apraksts = r[:8]
            if not cels or not apraksts:
                continue
            apraksts = str(apraksts).strip()
            k = _mp_atslega(apraksts)
            xlsx_atslegas.add(k)
            koord, ticamiba, metode = koordinatas.get(k, (None, None, None))
            con.execute("""INSERT INTO cela_punkts (kopa, tips, avota_id,
                  cela_nr, vertiba, lat, lon, atribūti)
                  VALUES (?,?,?,?,?,?,?,?)""",
                (slug, "melnais_punkts", str(int(nr)), str(cels).strip(),
                 apraksts,
                 koord[1] if koord else None, koord[0] if koord else None,
                 kompakts_json({
                     "km": str(km).strip(), "csng": int(csng),
                     "csng_ar_cietusajiem": int(ar_ciet),
                     "boja_gajusie": int(boja), "ievainotie": int(ievain),
                     "ticamiba": ticamiba, "metode": metode,
                     "avoti": "lvceli.lv 2020-2022 XLSX + NAP CSV;"
                              " koordinātas atvasinātas (ne avota)"})))
            n += 1
        tikai_csv = [t for t in csv_apraksti
                     if _mp_atslega(t) not in xlsx_atslegas]
        piezimes.append(f"bāze: lvceli.lv pilnais XLSX ({n});"
                        f" koordinātas {sum(1 for k in xlsx_atslegas if k in koordinatas)}"
                        f"; NAP CSV krustpārbaude: {len(csv_apraksti)} rindas"
                        + (f", BEZ pāra XLSX: {len(tikai_csv)}" if tikai_csv else ""))
    else:
        # rezerves ceļš: tikai NAP CSV (bez koordinātām)
        for vards in csv_apraksti:
            m = CELA_NR.search(vards)
            koord, ticamiba, metode = koordinatas.get(_mp_atslega(vards),
                                                      (None, None, None))
            con.execute("""INSERT INTO cela_punkts (kopa, tips, cela_nr,
                  vertiba, lat, lon, atribūti) VALUES (?,?,?,?,?,?,?)""",
                (slug, "melnais_punkts", m.group(1) if m else None, vards,
                 koord[1] if koord else None, koord[0] if koord else None,
                 kompakts_json({"ticamiba": ticamiba, "metode": metode})))
            n += 1
        piezimes.append("tikai NAP CSV (pilnais XLSX nav lejupielādēts)")
    return n, "; ".join(piezimes) or None


def _ielade_atruma_zimes(con, slug, dati):
    from shapely.geometry import shape
    n = 0
    for f in dati["features"]:
        p = f.get("properties") or {}
        g = f.get("geometry")
        lat = lon = None
        if g and g.get("coordinates") is not None:
            c = shape(g).centroid       # der arī ne-Point ģeometrijai
            lat, lon = c.y, c.x
        con.execute("""INSERT INTO cela_punkts (kopa, tips, avota_id, vertiba,
              apraksts, lat, lon, atribūti) VALUES (?,?,?,?,?,?,?,?)""",
            (slug, "atruma_zime", nav_none(p.get("id")),
             nav_none(p.get("piezime_cela_zime")) or nav_none(p.get("cela_zimes_nr")),
             " / ".join(x for x in (nav_none(p.get("veids")),
                                    nav_none(p.get("uz_ko_attiecas"))) if x) or None,
             lat, lon,
             kompakts_json({"zimes_nr": nav_none(p.get("cela_zimes_nr")),
                            "novertejums": nav_none(p.get("novertejums")),
                            "ipasnieks": nav_none(p.get("zimes_ipasnieks"))})))
        n += 1
    return n, None


def _ielade_gajeju_celus(con, slug, dati):
    n, bez_geo = 0, 0
    for f in dati["features"]:
        p = f.get("properties") or {}
        wkb, robezas = geo_wkb(f.get("geometry"))
        if wkb is None:
            bez_geo += 1
            robezas = (None, None, None, None)
        kreisa = p.get("Novietojums - kreisā puse") == "+"
        laba = p.get("Novietojums - labā puse") == "+"
        con.execute("""INSERT INTO cela_papildslanis (kopa, tips, avota_id,
              cela_nr, vertiba, atribūti, wkb, srid, minx, miny, maxx, maxy)
              VALUES (?,?,?,?,?,?,?,4326,?,?,?,?)""",
            (slug, "gajeju_cels", nav_none(p.get("OBJECTID")),
             nav_none(p.get("Autoceļa indekss")),
             nav_none(p.get("Infrastruktūras veids")),
             kompakts_json({"nosaukums": nav_none(p.get("Autoceļa nosaukums")),
                            "km_no": skaitlis(p.get("Adrese - no, km")),
                            "km_lidz": skaitlis(p.get("Adrese - līdz, km")),
                            "garums_km": skaitlis(p.get("Posma garums, km")),
                            "platums_m": skaitlis(p.get("Platums, m")),
                            "apgaismots": p.get("Apgaismojums") == "+",
                            "puse": ("abas" if kreisa and laba else
                                     "kreisa" if kreisa else
                                     "laba" if laba else None),
                            "piezimes": nav_none(p.get("Piezīmes"))}),
             wkb, *robezas))
        n += 1
    return n, (f"{bez_geo} posmi bez ģeometrijas (avota kļūdas) — wkb NULL"
               if bez_geo else None)


def _ielade_masas(con, slug, dati):
    vertibas = {"heightRestrictions": ("augstums", "heightRestrictionInMeters", "m"),
                "widthRestrictions": ("platums", "widthRestrictionsInMeters", "m"),
                "massRestrictions": ("masa", "massRestrictionsInTons", "t"),
                "virtualMassRestriction": ("masa_virtuala", "virtualMassRestrictionInTons", "t"),
                "virtualMassRestrictionWithException":
                    ("masa_virtuala_iznemumi", "virtualMassRestrictionInTons", "t")}
    n = 0
    for f in dati["features"]:
        p = f.get("properties") or {}
        wkb, robezas = geo_wkb(f.get("geometry"))
        robezas = robezas or (None, None, None, None)
        klase = p.get("restrictionClass") or ""
        veids, lauks, vien = vertibas.get(klase, ("cits", "", ""))
        v = skaitlis(p.get(lauks))
        con.execute("""INSERT INTO cela_papildslanis (kopa, tips, avota_id,
              cela_nr, vertiba, atribūti, wkb, srid, minx, miny, maxx, maxy)
              VALUES (?,?,?,?,?,?,?,4326,?,?,?,?)""",
            (slug, "masas_ierobezojums", nav_none(p.get("id")),
             nav_none(p.get("street")),
             f"{veids} {v:g} {vien}" if v is not None else veids,
             kompakts_json({"klase": klase,
                            "parent_id": nav_none(p.get("parentId")),
                            "rezims": nav_none(p.get("restrictionType")),
                            "no": nav_none(p.get("startDate")),
                            "lidz": nav_none(p.get("endDate")),
                            "km_no": skaitlis(p.get("start")),
                            "km_lidz": skaitlis(p.get("end")),
                            "iznemumi": nav_none(p.get("additionalExceptionRules")),
                            "piezimes": nav_none(p.get("notes"))}),
             wkb, *robezas))
        n += 1
    return n, None


def _ielade_meteo_vietas(con, slug, saturs):
    sakne = ET.fromstring(saturs)
    n = 0
    for vieta in visi(sakne, "measurementSite"):
        # pirmais <value> pieder equipmentType ('Road Weather Stations') —
        # stacijas vārds jāņem TIEŠI no measurementSiteName apakškoka!
        vards_el = pirmais(vieta, "measurementSiteName")
        vards = _teksts(vards_el, "value") if vards_el is not None else None
        lat = next((float(e.text) for e in visi(vieta, "latitude")), None)
        lon = next((float(e.text) for e in visi(vieta, "longitude")), None)
        veidi = sorted({e.text for e in
                        visi(vieta, "specificMeasurementValueType") if e.text})
        m = CELA_NR.match(vards or "")
        con.execute("""INSERT INTO cela_punkts (kopa, tips, avota_id, cela_nr,
              vertiba, lat, lon, atribūti) VALUES (?,?,?,?,?,?,?,?)""",
            (slug, "meteostacija", vieta.get("id"), m.group(1) if m else None,
             vards, lat, lon, kompakts_json({"merijumi": veidi})))
        n += 1
    return n, None


IELADETAJI = {"valsts_celu_tikls": _ielade_celu_posmus,
              "celu_posmi_atributi": _ielade_celu_posmus,
              "celu_klasifikacija": _ielade_celu_posmus,
              "prioritarie_celi": _ielade_celu_posmus,
              "melnie_punkti": _ielade_melnos_punktus,
              "atruma_zimes": _ielade_atruma_zimes,
              "gajeju_celi": _ielade_gajeju_celus,
              "masas_ierobezojumi": _ielade_masas,
              "meteo_vietas": _ielade_meteo_vietas}


def solis_statiskie(con, klients, kopas, piespiest):
    print("2) Statiskie slāņi ...", flush=True)
    for slug in STATISKIE:
        kopa = kopas.get(slug)
        if not kopa:
            print(f"  ! {slug}: nav atslēgas — izlaists")
            continue
        marker = f"kopa:{slug}"
        try:
            if kopa.get("lejupielade") == "faili":
                fid = faila_id(klients, kopa["atslega"])
                if fid is None:
                    print(f"  ! {slug}: failu saraksts tukšs — izlaists")
                    continue
                fmt = None if slug == "melnie_punkti" else "geojson"
                saturs, h = lejupieladet(klients, kopa["atslega"], fmt, fid)
                fmt = fmt or "csv"
            else:   # plūsmas mehānisms, bet saturs statisks (masas, meteo vietas)
                fmt = "xml" if slug == "meteo_vietas" else "geojson"
                saturs, h = lejupieladet(klients, kopa["atslega"], fmt)
        except httpx.HTTPError as e:
            print(f"  ! {slug}: lejupielādes kļūda ({e}) — izlaists", file=sys.stderr)
            continue
        if saturs is None:
            ievaks(con, marker, None, None, "204 — avotā nav datu")
            con.commit()
            print(f"  {slug}: 204 — avotā šobrīd nav datu (skaļi reģistrēts)")
            continue
        if h == pedejais_hash(con, marker) and not piespiest:
            print(f"  {slug}: nav mainījies — izlaists")
            continue

        tabula = STATISKO_TABULA[slug]
        pirms = con.execute(f"SELECT COUNT(*) FROM {tabula} WHERE kopa=?",
                            (slug,)).fetchone()[0]
        try:
            if slug == "celu_posmi_atributi":
                dati = json.loads(saturs)
                # 2026-07: platums/joslas 100% tukši — dublēt tīkla ģeometriju nav jēgas
                if not any(nav_none((f.get("properties") or {}).get("autocela_platums"))
                           or nav_none((f.get("properties") or {})
                                       .get("brauksanas_joslu_skaits"))
                           for f in dati["features"]):
                    piez = "platums/joslas visiem tukši — ielāde izlaista (dublē tīklu)"
                    ievaks(con, marker, h, 0, piez)
                    con.commit()
                    print(f"  {slug}: {piez}")
                    continue
            con.execute(f"DELETE FROM {tabula} WHERE kopa=?", (slug,))
            if slug in ("melnie_punkti", "meteo_vietas"):
                n, piez = IELADETAJI[slug](con, slug, saturs)
            else:
                n, piez = IELADETAJI[slug](con, slug, json.loads(saturs))
            if n == 0 and pirms > 0:
                con.rollback()
                print(f"  ! {slug}: izparsētas 0 rindas (iepriekš {pirms}) —"
                      " vecie dati ATSTĀTI, hash nav ierakstīts", file=sys.stderr)
                continue
        except Exception as e:
            con.rollback()
            print(f"  ! {slug}: apstrādes kļūda ({type(e).__name__}: {e}) —"
                  " vecie dati atstāti, turpinu", file=sys.stderr)
            continue
        arhivet(slug, saturs, fmt)
        cur = con.execute("UPDATE nap_katalogs SET pedejais_hash=?"
                          " WHERE dataset_id=?", (h, kopa.get("card")))
        if cur.rowcount == 0:
            print(f"    piezīme: {slug} card nav katalogā — pedejais_hash izlaists")
        ievaks(con, marker, h, n, piez)
        con.commit()
        if piez:
            print(f"    piezīme: {piez}")
        print(f"  {slug}: {n} ieraksti ({len(saturs) / 1e6:.1f} MB)")

    # prioritāro atzīme VIENMĒR no jauna (arī ja visi slāņi hash-izlaisti) —
    # citādi tīkla pārlāde bez prioritāro pārlādes klusi nodzēstu atzīmes.
    con.execute("""UPDATE celu_posms SET prioritars =
        CASE WHEN kopa='prioritarie_celi' THEN 1
             WHEN cela_nr IN (SELECT DISTINCT cela_nr FROM celu_posms
                              WHERE kopa='prioritarie_celi' AND cela_nr IS NOT NULL)
             THEN 1 ELSE 0 END""")
    con.commit()


# ------------------------------------------------------------------ 3. notikumi

# Lauki, kas jau glabājas savās kolonnās vai ir troksnis — ārpus atributi JSON.
_TROKSNIS = {"situationRecordCreationTime", "situationRecordVersionTime",
             "probabilityOfOccurrence", "safetyRelatedMessage", "sourceCountry",
             "sourceIdentification", "sourceNationalIdentifier", "value",
             "validityStatus", "overrunning", "overallStartTime",
             "overallEndTime", "delayTimeValue", "confidentiality",
             "informationStatus", "publicationTime"}
_IZLAIST_ZARUS = {"locationReference", "source", "generalPublicComment",
                  "validity", "headerInformation", "impact"}


def _lauki(el):
    """Visi lapu elementi ar tekstu (bez trokšņa un izlaižamajiem zariem) —
    lai nezināmi DATEX lauki (piem. ziemas weatherRelatedRoadConditionType)
    nekad nepazūd klusi."""
    rez = {}

    def staiga(e):
        for b in e:
            vards = b.tag.rsplit("}", 1)[-1]
            if vards in _IZLAIST_ZARUS:
                continue
            if len(b) == 0:
                t = (b.text or "").strip()
                if t and vards not in _TROKSNIS:
                    rez.setdefault(vards, t)
            else:
                staiga(b)

    staiga(el)
    return rez


def _linijas(sit):
    """Līnijas pa virziena apakškokiem (LocationGroupByList grupas un
    secondDirection NEdrīkst saplūdināt vienā LineString!)."""
    linijas = []
    for virziens in ("firstDirection", "secondDirection"):
        for zars in visi(sit, virziens):
            pari = _koordinatas(zars)
            if len(pari) >= 2:
                linijas.append(pari)
    return linijas


def _koordinatas(el):
    pari = []
    for punkts in visi(el, "openlrCoordinates"):
        lat = next((float(e.text) for e in visi(punkts, "latitude")), None)
        lon = next((float(e.text) for e in visi(punkts, "longitude")), None)
        if lat is not None and lon is not None:
            pari.append((lon, lat))
    return pari


def _situacijas(con, slug, tips, sakne, iev_id, tagad):
    n, redzeti = 0, []
    for sit in visi(sakne, "situationRecord"):
        rid = sit.get("id")
        versija = (_teksts(sit, "situationRecordVersionTime")
                   or sit.get("version") or "-")
        linijas = _linijas(sit)
        pari = [p for l in linijas for p in l] or _koordinatas(sit)
        wkb = None
        if linijas:
            from shapely import to_wkb
            from shapely.geometry import LineString, MultiLineString
            wkb = to_wkb(LineString(linijas[0]) if len(linijas) == 1
                         else MultiLineString(linijas))
        komentars = pirmais(sit, "generalPublicComment")
        apraksts = _teksts(komentars, "value") if komentars is not None else None
        m = CELA_NR.search(apraksts or "")
        atributi = kompakts_json({
            "xsi_tips": (sit.get(XSI) or "").split(":")[-1] or None, **_lauki(sit)})
        con.execute("""INSERT OR IGNORE INTO cela_notikums
              (kopa, tips, datex_id, versija, sakums, beigas, cela_nr, lat, lon,
               wkb, apraksts, atributi, redzets, ieladets, ievaks_id)
              VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (slug, tips, rid, versija,
             _teksts(sit, "overallStartTime"), _teksts(sit, "overallEndTime"),
             m.group(1) if m else None,
             pari[0][1] if pari else None, pari[0][0] if pari else None, wkb,
             apraksts, atributi, tagad, tagad, iev_id))
        redzeti.append(rid)
        n += 1
    return n, redzeti


_METEO_LAUKI = [("gaisa_t", "airTemperature", "temperature"),
                ("rasas_t", "dewPointTemperature", "temperature"),
                ("virsmas_t", "roadSurfaceTemperature", "temperature"),
                ("berze", "friction", "friction"),
                ("sniegs_m", "depthOfSnow", "distance"),
                ("udens_m", "waterFilmThickness", "distance"),
                ("ledus_m", "iceLayerThickness", "distance"),
                ("mitrums_pct", "relativeHumidity", "percentage"),
                ("redzamiba_m", "minimumVisibilityDistance", "integerMetreDistance"),
                ("vejs_ms", "windSpeed", "windSpeed"),
                ("vejs_max_ms", "maximumWindSpeed", "windSpeed")]


def _meteo_merijumi(con, slug, sakne, iev_id, tagad):
    stacijas_cels = dict(con.execute(
        "SELECT avota_id, cela_nr FROM cela_punkts WHERE tips='meteostacija'"))
    n, redzeti = 0, []
    for bloks in visi(sakne, "siteMeasurements"):
        ref = pirmais(bloks, "measurementSiteReference")
        sid = ref.get("id") if ref is not None else None
        noklusejums = pirmais(bloks, "measurementTimeDefault")
        laiks = (_teksts(noklusejums, "timeValue") if noklusejums is not None
                 else None) or _teksts(bloks, "timeValue")
        if not (sid and laiks):
            continue
        vertibas = {}
        for vards, virselements, apakselements in _METEO_LAUKI:
            el = pirmais(bloks, virselements)
            if el is not None:
                v = _teksts(el, apakselements)
                if v is not None:
                    vertibas[vards] = skaitlis(v)
        vertibas["virsmas_stavoklis"] = _teksts(bloks, "weatherRelatedRoadConditionType")
        vertibas["bez_nokrisniem"] = _teksts(bloks, "noPrecipitation")
        con.execute("""INSERT OR IGNORE INTO cela_notikums
              (kopa, tips, datex_id, versija, sakums, cela_nr, atributi,
               redzets, ieladets, ievaks_id)
              VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (slug, "meteo_merijums", sid, laiks, laiks,
             stacijas_cels.get(sid), kompakts_json(vertibas), tagad, tagad, iev_id))
        redzeti.append(sid)
        n += 1
    return n, redzeti


def solis_notikumi(con, klients, kopas):
    print("3) Reāllaika notikumi (DATEX II) ...", flush=True)
    for slug, tips in NOTIKUMU_TIPS.items():
        kopa = kopas.get(slug)
        if not kopa:
            print(f"  ! {slug}: nav atslēgas — izlaists")
            continue
        tagad = datetime.datetime.now().isoformat(timespec="seconds")
        try:
            saturs, h = lejupieladet(klients, kopa["atslega"], "xml")
        except httpx.HTTPError as e:
            print(f"  ! {slug}: kļūda ({e}) — izlaists", file=sys.stderr)
            continue
        if saturs is None:
            ievaks(con, f"kopa:{slug}", None, 0, "204 — plūsma tukša",
                   savakts=tagad)
            con.commit()
            print(f"  {slug}: 204 — šobrīd nav notikumu")
            continue
        try:
            sakne = ET.fromstring(saturs)
            pirms = con.total_changes
            iev_id = ievaks(con, f"kopa:{slug}", h, None, savakts=tagad)
            if slug == "meteo_merijumi":
                n, redzeti = _meteo_merijumi(con, slug, sakne, iev_id, tagad)
            else:
                n, redzeti = _situacijas(con, slug, tips, sakne, iev_id, tagad)
            jauni = con.total_changes - pirms - 1   # bez paša ievaks ieraksta
            # arī nemainītajiem (INSERT OR IGNORE izlaistajiem) atzīmē redzēšanu
            for rid in set(redzeti):
                con.execute("UPDATE cela_notikums SET redzets=? WHERE kopa=?"
                            " AND datex_id=?", (tagad, slug, rid))
            con.execute("UPDATE ievaks SET ierakstu_skaits=? WHERE ievaks_id=?",
                        (jauni, iev_id))
            con.commit()
        except Exception as e:
            con.rollback()
            print(f"  ! {slug}: apstrādes kļūda ({type(e).__name__}: {e}) —"
                  " izlaists, turpinu", file=sys.stderr)
            continue
        print(f"  {slug}: {n} ieraksti plūsmā, {jauni} jauni vēsturē")


# ------------------------------------------------------------------ statuss

def statuss(con):
    k = atslegas()
    print(f"Atslēgas: {'ir (' + str(len(k)) + ' kopas)' if k else 'NAV — tikai katalogs'}")
    print("\n=== Avotu svaigums (pēdējā ielāde) ===")
    for r in con.execute("""SELECT avots, MAX(savakts), ierakstu_skaits, piezimes
                            FROM ievaks GROUP BY avots ORDER BY avots"""):
        piez = f"  [{r[3]}]" if r[3] else ""
        print(f"  {r[0]:<32} {r[1]}  ({r[2]} ieraksti){piez}")
    print("\n=== Piepildījums ===")
    for tab in ("nap_katalogs", "celu_posms", "cela_punkts",
                "cela_papildslanis", "cela_notikums"):
        print(f"  {tab:<20} {con.execute(f'SELECT COUNT(*) FROM {tab}').fetchone()[0]:>8}")
    print("\n=== Aktīvie notikumi (v_aktivie_notikumi) ===")
    rindas = list(con.execute(
        "SELECT tips, COUNT(*) FROM v_aktivie_notikumi GROUP BY tips"))
    for r in rindas:
        print(f"  {r[0]:<16} {r[1]}")
    if not rindas:
        print("  (nav)")
    r = con.execute("SELECT COUNT(*), MAX(merits) FROM v_meteo_jaunakie").fetchone()
    print(f"\nMeteostaciju jaunākie mērījumi: {r[0]} stacijas (līdz {r[1]})")
    jaunas = con.execute("SELECT COUNT(*) FROM nap_katalogs WHERE abonets=0").fetchone()[0]
    print(f"Katalogā neabonētas kopas: {jaunas} (jaunu kopu uzraudzībai)")


# ------------------------------------------------------------------ main

def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("komanda", choices=["buvet", "atjaunot", "statuss"])
    ap.add_argument("--db", default=str(DB_CELS))
    ap.add_argument("--parrakstit", action="store_true")
    ap.add_argument("--piespiest", action="store_true")
    ap.add_argument("--bez-kataloga", action="store_true")
    ap.add_argument("--bez-statiskajiem", action="store_true")
    ap.add_argument("--bez-notikumiem", action="store_true")
    args = ap.parse_args()

    db = pathlib.Path(args.db)
    if args.komanda == "buvet":
        if db.exists() and not args.parrakstit:
            print(f"{db} jau eksistē — lieto `atjaunot` vai --parrakstit",
                  file=sys.stderr)
            return 1
        if db.exists():
            db.unlink()
        db.parent.mkdir(parents=True, exist_ok=True)
        con = sqlite3.connect(db)
        con.executescript(SHEMA.read_text(encoding="utf-8"))
        print(f"Shēma izveidota: {db}")
    else:
        if not db.exists():
            print(f"{db} nav — vispirms `buvet`", file=sys.stderr)
            return 1
        con = sqlite3.connect(db)
    con.execute("PRAGMA foreign_keys=ON")

    if args.komanda == "statuss":
        statuss(con)
        return 0

    kopas = atslegas()
    with httpx.Client(timeout=600, follow_redirects=True) as klients:
        if not args.bez_kataloga:
            try:
                solis_katalogs(con, klients, args.piespiest)
            except Exception as e:
                print(f"! katalogs: kļūda ({type(e).__name__}: {e}) — turpinu ar"
                      " pārējiem soļiem", file=sys.stderr)
        if kopas is None:
            print(f"! {ATSLEGAS_FAILS.name} nav — statiskie un notikumi izlaisti"
                  " (sk. ABONESANA.txt)")
        else:
            if not args.bez_statiskajiem:
                solis_statiskie(con, klients, kopas, args.piespiest)
            if not args.bez_notikumiem:
                solis_notikumi(con, klients, kopas)
    print()
    statuss(con)
    return 0


if __name__ == "__main__":
    sys.exit(main())
