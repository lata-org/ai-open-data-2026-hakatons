# /// script
# requires-python = ">=3.13,<3.14"
# dependencies = ["openpyxl>=3.1,<4", "shapely>=2,<3", "pyproj>=3.6,<4"]
# ///
"""Melno punktu kartes slāņi -> dati/slani/melnie_punkti_lv.geojson (visa
Latvija) un melnie_punkti_ogre.geojson (Ogres novads + 5 km buferis).

PAMATAVOTS: LVC pilnais 2020.–2022. gada saraksts
(dokumentacija/paraugi/melnie_punkti_2020_2022_pilns.xlsx, lejupielādēts no
lvceli.lv) — 38 punkti, katram pamatceļš + km + CSNg statistika. NAP CSV ir
šī saraksta nepilnīga kopija bez ceļa/km (33 unikāli apraksti ar kļūdām).

Koordinātas katram punktam:
  1. km interpolācija uz pamatceļa ass (celi.db klasifikācijas līnija).
     Līnijas VIRZIENU katram ceļam kalibrē pret verificētajām orientieru
     lokalizācijām (dati/slani/melnie_punkti_lokalizacijas.json — sonnet
     ģeokodēšana + opus verifikācija) vai, ja tādu nav, pret Rīgu (A ceļu
     km 0 ir Rīgas pusē).
  2. Ja punktam ir verificēta orientieru lokalizācija <= 2,5 km no km punkta,
     lieto TO (precīzāka par veselu km) -> ticamiba 'augsta'.
  3. Citādi km punkts; ticamību paaugstina, ja aprakstā nosauktais
     šķērsojošais ceļš ir <= 2 km (metode 'xlsx_km', ticamiba 'augsta'/'videja').
"""
import json
import pathlib
import re
import sqlite3

import openpyxl
from pyproj import Transformer
from shapely import from_wkb
from shapely.geometry import MultiLineString, Point, mapping
from shapely.ops import linemerge, transform

HERE = pathlib.Path(__file__).resolve().parent.parent
CELI = HERE / "dati" / "celi.db"
TERITORIJAS = HERE.parent / "teritorijas" / "dati" / "teritorijas.db"
XLSX = HERE / "dokumentacija" / "paraugi" / "melnie_punkti_2020_2022_pilns.xlsx"
SLANI = HERE / "dati" / "slani"

UZ_LKS = Transformer.from_crs("EPSG:4326", "EPSG:3059", always_xy=True).transform
UZ_WGS = Transformer.from_crs("EPSG:3059", "EPSG:4326", always_xy=True).transform
RIGA = Point(506500, 312000)
CELA_NR = re.compile(r"\(([APV]\d{1,4})\)")

_linijas = {}


def cela_linija(con, nr):
    if nr in _linijas:
        return _linijas[nr]
    rindas = con.execute(
        "SELECT wkb FROM celu_posms WHERE kopa='celu_klasifikacija' AND cela_nr=?",
        (nr,)).fetchall()
    g = None
    if rindas:
        dalas = []
        for (wkb,) in rindas:
            gg = from_wkb(wkb)
            dalas.extend(gg.geoms if isinstance(gg, MultiLineString) else [gg])
        g = linemerge(MultiLineString(dalas))
        if isinstance(g, MultiLineString):
            g = max(g.geoms, key=lambda x: x.length)
        g = transform(UZ_LKS, g)
    _linijas[nr] = g
    return g


def parsst_km(v):
    skaitli = [float(x) for x in re.findall(r"\d+(?:[.,]\d+)?", str(v))]
    return sum(skaitli) / len(skaitli) if skaitli else None


def atslega(t):
    t = (t or "").lower().translate(str.maketrans("āčēģīķļņšūž", "acegiklnsuz"))
    return re.sub(r"[^0-9a-z]", "", t)[:28]


def objekts(punkts_lks, ip):
    lon, lat = UZ_WGS(punkts_lks.x, punkts_lks.y)
    return {"type": "Feature",
            "geometry": mapping(Point(round(lon, 6), round(lat, 6))),
            "properties": ip}


def main():
    con = sqlite3.connect(f"file:{CELI}?mode=ro", uri=True)
    ter = sqlite3.connect(f"file:{TERITORIJAS}?mode=ro", uri=True)
    novads = from_wkb(ter.execute(
        "SELECT wkb FROM geometrija WHERE kods='LV0040000' AND versija='2026_5km'"
    ).fetchone()[0])

    # verificētās orientieru lokalizācijas pēc apraksta atslēgas
    lok = {}
    lok_fails = SLANI / "melnie_punkti_lokalizacijas.json"
    if lok_fails.exists():
        for p in json.loads(lok_fails.read_text(encoding="utf-8"))["punkti"]:
            if p.get("lat"):
                lok[atslega(p["apraksts"])] = p

    # XLSX pilnās rindas
    rindas = []
    lapa = openpyxl.load_workbook(XLSX).active
    for r in lapa.iter_rows(min_row=5, values_only=True):
        nr, cels, km_teksts, csng, ar_ciet, boja, ievain, apraksts = r[:8]
        if not cels or not apraksts:
            continue
        rindas.append({"nr": int(nr), "cels": str(cels).strip(),
                       "km": parsst_km(km_teksts),
                       "csng": int(csng), "ar_ciet": int(ar_ciet),
                       "boja": int(boja), "ievain": int(ievain),
                       "apraksts": str(apraksts).strip()})

    def wf_punkts(apraksts):
        """Verificētā lokalizācija (LKS-92 punkts) vai None. TIKAI precīza
        atslēgas sakritība — prefiksi jauc 'Apļveida krustojums ar...' punktus."""
        p = lok.get(atslega(apraksts))
        return Point(*UZ_LKS(p["lon"], p["lat"])) if p else None

    # Katram ceļam kalibrē km ass VIRZIENU un NOBĪDI pret verificētajiem
    # enkuriem: celi.db līnijām mēdz trūkt pilsētu posmu (piem., A10 bez
    # Rīgas daļas -> visa kilometrāža nobīdīta par ~14 km). Modelis:
    # attālums_pa_līniju = nobide + zime * km * 1000 (mediāna pa enkuriem).
    kalibracijas = {}   # cels -> (zime, nobide_m)

    def kalibracija(cels_nr, linija):
        if cels_nr in kalibracijas:
            return kalibracijas[cels_nr]
        enkuri = []
        for r in rindas:
            if r["cels"] == cels_nr and r["km"] is not None:
                p = wf_punkts(r["apraksts"])
                if p is not None and p.distance(linija) < 3000:
                    enkuri.append((r["km"], linija.project(p)))
        labakais = None
        for zime in (1, -1):
            if enkuri:
                nobides = sorted(pr - zime * km * 1000 for km, pr in enkuri)
                nobide = nobides[len(nobides) // 2]
                kluda = sum(abs(pr - (nobide + zime * km * 1000))
                            for km, pr in enkuri) / len(enkuri)
            else:
                sakums, beigas = Point(linija.coords[0]), Point(linija.coords[-1])
                nobide = 0 if zime == 1 else linija.length
                kluda = (0 if (zime == 1) == (sakums.distance(RIGA)
                                              <= beigas.distance(RIGA)) else 1)
            if labakais is None or kluda < labakais[0]:
                labakais = (kluda, zime, nobide)
        kalibracijas[cels_nr] = (labakais[1], labakais[2])
        return kalibracijas[cels_nr]

    objekti, atskaite = [], []
    for r in rindas:
        linija = cela_linija(con, r["cels"])
        ip = {"nr_mp": r["nr"], "cels": r["cels"], "km": r["km"],
              "csng": r["csng"], "csng_ar_cietusajiem": r["ar_ciet"],
              "boja_gajusie": r["boja"], "ievainotie": r["ievain"],
              "apraksts": r["apraksts"]}
        if linija is None or r["km"] is None:
            atskaite.append((r["apraksts"], f"{r['cels']}: nav līnijas/km"))
            continue
        zime, nobide = kalibracija(r["cels"], linija)
        km_p = linija.interpolate(
            min(max(0, nobide + zime * r["km"] * 1000), linija.length))
        wf = wf_punkts(r["apraksts"])
        if wf is not None and km_p.distance(wf) <= 2500:
            punkts = wf
            ip.update(ticamiba="augsta", metode="xlsx_km+orientieri",
                      km_nobide_km=round(km_p.distance(wf) / 1000, 2))
        else:
            punkts = km_p
            ip.update(ticamiba="videja", metode="xlsx_km")
            if wf is not None:
                ip["piezime"] = (f"orientieru lokalizācija {km_p.distance(wf)/1000:.1f} km"
                                 " no km punkta — izmantots km punkts, jāpārbauda")
            m = CELA_NR.search(r["apraksts"])
            if m and m.group(1) != r["cels"]:
                krustojuma = cela_linija(con, m.group(1))
                if krustojuma is not None and punkts.distance(krustojuma) <= 2000:
                    ip.update(ticamiba="augsta",
                              validets_pret=m.group(1),
                              validacijas_km=round(punkts.distance(krustojuma) / 1000, 2))
        objekti.append(objekts(punkts, ip))

    SLANI.mkdir(parents=True, exist_ok=True)
    (SLANI / "melnie_punkti_lv.geojson").write_text(json.dumps(
        {"type": "FeatureCollection",
         "name": "Melnie punkti (LVC pilnais 2020–2022 saraksts; koordinātas atvasinātas)",
         "features": objekti}, ensure_ascii=False, indent=1), encoding="utf-8")
    ogres = [o for o in objekti if novads.contains(
        Point(*UZ_LKS(*o["geometry"]["coordinates"])))]
    (SLANI / "melnie_punkti_ogre.geojson").write_text(json.dumps(
        {"type": "FeatureCollection",
         "name": "Melnie punkti Ogres novadā + 5 km (LVC 2020–2022)",
         "features": ogres}, ensure_ascii=False, indent=1), encoding="utf-8")

    a = sum(1 for o in objekti if o["properties"]["ticamiba"] == "augsta")
    print(f"Latvijas slānis: {len(objekti)}/38 punkti (augsta: {a},"
          f" vidēja: {len(objekti) - a}); Ogres tuvumā: {len(ogres)}")
    for o in objekti:
        p = o["properties"]
        zime = ("✓" if p["ticamiba"] == "augsta" else "~")
        piez = f"  [{p['piezime']}]" if p.get("piezime") else ""
        print(f"  {zime} {p['cels']:>4} km {p['km']:>5}: {p['apraksts'][:55]}{piez}")
    for teksts, iemesls in atskaite:
        print(f"  ! {teksts[:55]}: {iemesls}")


if __name__ == "__main__":
    main()
