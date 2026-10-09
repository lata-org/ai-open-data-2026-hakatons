---
name: celu-kartes-datubaze
description: >
  Darbs ar ceļu kartes SQLite datubāzi (dati/celi.db) — valsts ceļu tīkls ar
  klasifikāciju un prioritārajiem ceļiem (WKB, WGS84), melnie punkti, ātruma
  zīmes, gājēju ceļi, masas ierobežojumi, meteostacijas un reāllaika DATEX II
  notikumu vēsture (slēgumi, remonti, slidens ceļš, negadījumi, meteo
  mērījumi). Lietot, kad jāatbild par ceļu stāvokli, maršrutu drošību, ziemas
  apstākļiem vai jāgatavo ceļu/notikumu kartes slānis.
---

# Ceļu kartes datubāze — instrukcija darbam

Datubāze: `dati/celi.db` (~150 MB; shēma `db_shema.sql`, plūsma un atslēgu
pārvaldība `PLUSMA.md`, avoti `PUBLISKO_DATU_IESPEJAS.md`, oficiālā
dokumentācija un tās nesakritības `dokumentacija/DOKUMENTACIJA.md`).
Saturs: NAP katalogs (55 kopas), 4 087 ceļu posmi (WKB **WGS84**, ne LKS-92!),
118 punkti, 1 304 papildslāņu rindas, notikumu vēsture (tikai aug) ar
meteostaciju mērījumiem ik stundu.

## Būve un atjaunināšana

Komandas palaist no šīs mapes (Python TIKAI caur `uv run`):

```bash
uv run datubaze.py buvet        # DB no nulles (~2 min; lejupielādē ~150 MB)
uv run datubaze.py atjaunot     # statiskajiem hash skip; notikumus pievieno vienmēr
uv run datubaze.py statuss      # atslēgas, svaigums, aktīvie notikumi
```

- Karodziņi: `--bez-kataloga`, `--bez-statiskajiem`, `--bez-notikumiem`,
  `--piespiest`, `--db`.
- **Atslēgas**: `dati/nap_atslegas.json` (katrai kopai sava, NEKAD git/čatā);
  bez faila strādā tikai kataloga solis. Abonēšana: `ABONESANA.txt`.
- Ritmi: notikumu pull mācību dienu logos (06–09, 13–17) ik 30 min — praksē
  `atjaunot` cron reizē; statiskie reāli mainās 2×/gadā. Ziemā (nov–mar)
  slidens/slikti apstākļi kļūst aktīvi — vasarā tie ir 204 (tas ir normāli).
- Notikumu vēsture TIKAI AUG — `atjaunot` nekad nedzēš; dedup pa
  (kopa, datex_id, versija).

## Modeļa pamati

| Elements | Būtība |
|---|---|
| `celu_posms` | 3 pārklājošas tīkla reprezentācijas pa `kopa`: `valsts_celu_tikls` (2500 posmi), `celu_klasifikacija` (1582 maršruti), `prioritarie_celi` (5) — **vienmēr filtrēt pēc `kopa`**, citādi ceļš trīskāršojas |
| `cela_punkts` | `tips`: melnais_punkts (38 — bāze lvceli.lv pilnais 2020.–2022. XLSX; koordinātas ATVASINĀTAS, atribūtos km/CSNg/ticamiba/metode), atruma_zime (14, izlase), meteostacija (70, `avota_id` = DATEX stacijas id) |
| `cela_papildslanis` | `tips`: gajeju_cels (748; 7 bez wkb — avota kļūdas), masas_ierobezojums (556; `atribūti.parent_id` grupē viena tilta rindas) |
| `cela_notikums` | DATEX II vēsture; `redzets` = pēdējoreiz plūsmā; `atributi` JSON (xsi tips, ziemas apakštipi, meteo mērvērtības); `wkb` līnija posmu notikumiem |
| Skati | `v_aktivie_notikumi` (jaunākā versija + derīguma logs + redzēts pēdējā ievākumā), `v_prioritarie_celi`, `v_meteo_jaunakie`, `v_drosibas_punkti` |
| Ģeometrijas | **viss WGS84** (lon/lat grādi) WKB + bbox kolonnas — atšķirībā no teritorijas.db (LKS-92)! |

## Vaicājumu receptes (pārbaudītas uz reālās db)

**Aktīvo notikumu slānis kartei:**

```sql
SELECT tips, cela_nr, lat, lon, apraksts, sakums, beigas
FROM v_aktivie_notikumi;
-- 78 rindas: 68 remonti, 6 slēgumi, 2 joslu slēgumi, 2 negadījumi (2026-07-31)
```

**Meteostaciju jaunākie mērījumi** (ziemas panelis; mērvērtības JSON):

```sql
SELECT stacija, lat, lon,
       json_extract(atributi,'$.gaisa_t')    gaiss_c,
       json_extract(atributi,'$.virsmas_t')  virsma_c,
       json_extract(atributi,'$.berze')      berze,
       json_extract(atributi,'$.virsmas_stavoklis') stavoklis
FROM v_meteo_jaunakie ORDER BY stacija;
-- 'A1 Ainaži' 28.02°C gaiss, 36.2°C virsma, berze 0.82, 'dry' ...
-- berze < ~0.4 = slidens; ziemā šis ir galvenais drošības signāls
```

**Ceļu tīkla slānis Ogres novadam** (bbox WGS84 priekšatlase; WKB zīmē
shapely/MapLibre pusē):

```sql
SELECT cela_nr, klase, prioritars, wkb FROM celu_posms
WHERE kopa='valsts_celu_tikls'
  AND maxx >= 24.429 AND minx <= 25.556
  AND maxy >= 56.541 AND miny <= 56.997;
-- 230 posmi / 156 ceļi Ogres novada bbox (bbox no teritorijas.db + pyproj)
```

**Masas/augstuma ierobežojumi uz maršruta ceļa** (autobusu piemērotība):

```sql
SELECT vertiba, json_extract("atribūti",'$.km_no') km,
       json_extract("atribūti",'$.piezimes') piezimes
FROM cela_papildslanis
WHERE tips='masas_ierobezojums' AND cela_nr LIKE 'A6%';
-- 'augstums 4.5 m' 139.96 km 'Pārvads pār dzelzceļu' ...
-- UZMANĪBU: kolonna "atribūti" ar diakritiku — SQL jāliek pēdiņās
```

**Gājēju infrastruktūra pie ceļa** (vai bērnam ir ietve; papildina OSM):

```sql
SELECT cela_nr, vertiba,
       json_extract("atribūti",'$.platums_m')  platums,
       json_extract("atribūti",'$.apgaismots') apgaismots,
       json_extract("atribūti",'$.puse')       puse
FROM cela_papildslanis
WHERE tips='gajeju_cels' AND wkb IS NOT NULL
  AND maxx >= 24.429 AND minx <= 25.556 AND maxy >= 56.541 AND miny <= 56.997;
-- 82 posmi Ogres bbox; V996 'gājēju ietve' 1.5 m, apgaismota, kreisā puse ...
```

**Melnie punkti ar koordinātām un negadījumu statistiku** (koordinātas
atvasinātas — NAP tās nedod; `atribūti.ticamiba` rāda drošumu):

```sql
SELECT cela_nr, json_extract("atribūti",'$.km') km, lat, lon, vertiba,
       json_extract("atribūti",'$.csng')                 csng,
       json_extract("atribūti",'$.boja_gajusie')         bojagajusie,
       json_extract("atribūti",'$.ticamiba')             ticamiba
FROM cela_punkts WHERE tips='melnais_punkts'
ORDER BY json_extract("atribūti",'$.boja_gajusie') DESC,
         json_extract("atribūti",'$.csng_ar_cietusajiem') DESC;
-- 38/38 ar koordinātām un pilnu CSNg statistiku; bīstamākie: A9 km 8
-- (2 bojāgājušie), A10 km 25 (2), A1 km 5 Baltezers (1, 5 CSNg ar cietušajiem)
```

**Ziemas sezonas hronika** (cik dienas katrs ceļš bijis slidens — pildīsies
no novembra; vasarā tukšs, bet vaicājums validēts):

```sql
SELECT cela_nr, COUNT(DISTINCT date(sakums)) slidenas_dienas
FROM cela_notikums
WHERE tips='slidens' AND sakums BETWEEN '2026-11-01' AND '2027-03-31'
GROUP BY cela_nr ORDER BY slidenas_dienas DESC;
```

**ATTACH ar transporta db — meteostacijas pie skolēnu pieturām:**

```sql
ATTACH '../sabiedriskais-transports/dati/transports.db' AS tr;
SELECT p.vertiba, ROUND(MIN(
    111.19*SQRT((pk.lat-p.lat)*(pk.lat-p.lat)
      + ((pk.lon-p.lon)*0.545)*((pk.lon-p.lon)*0.545))),1) min_km
FROM cela_punkts p, tr.pieturu_klasteris pk
WHERE p.tips='meteostacija' AND p.lat IS NOT NULL
  AND pk.lat BETWEEN 56.541 AND 56.997 AND pk.lon BETWEEN 24.429 AND 25.556
GROUP BY p.punkts_id HAVING min_km <= 5 ORDER BY min_km;
-- 'A6 Ādmiņi' 0.8 km, 'A6 Saulkalne' 1.1, 'P80 Zādzene' 1.4, 'A6 Kaibala' 2.1,
-- 'P80 Ogresgals' 2.2 — novada reisiem ir 5 "savas" stacijas apledojuma kontrolei
```

## Noteikumi un kļūdu novēršana

1. **`celu_posms` vienmēr filtrēt pēc `kopa`** — trīs pārklājošas tīkla
   reprezentācijas; SUM/COUNT bez filtra ir 2–3× par lielu.
2. **Ģeometrijas ir WGS84** (lon/lat), ne LKS-92 kā teritorijas.db —
   savienojot ar robežām, tās jāpārprojicē (pyproj EPSG:3059→4326).
3. **Kolonna `atribūti`** (posmiem/papildslāņiem) ir ar diakritiku — SQL
   rakstīt `"atribūti"`; notikumu tabulā tā saucas `atributi` (bez!).
4. **Aktīvos notikumus ņemt TIKAI no `v_aktivie_notikumi`** — pati tabula ir
   vēsture, kur notikumi bez beigu laika citādi izskatās "aktīvi" mūžīgi.
5. Notikumu `cela_nr` situācijām gandrīz vienmēr NULL (avots nedod ceļa nr,
   tikai koordinātas) — piesaistei ceļam lietot lat/lon + posmu bbox;
   meteo mērījumiem `cela_nr` IR (caur stacijas nosaukumu).
6. Melno punktu koordinātas ir ATVASINĀTAS (km interpolācija ar per-ceļa
   kalibrāciju + verificēta orientieru ģeokodēšana — skripti/
   melnie_punkti_slanis.py), ne avota dotas — atribūtos `ticamiba` un
   `metode`; ātruma zīmes ir 14 punktu izlase; posmu platums/joslas avotā
   100% tukši (sk. dokumentacija/DOKUMENTACIJA.md).
7. Vasarā slidens/slikti apstākļi/īslaicīgie remonti ir 204 (tukša plūsma) —
   tas NAV bojājums; struktūra validēta pret oficiālajiem paraugiem
   `dokumentacija/paraugi/`.
8. DATEX XML parsē tikai datubaze.py — ja jāparsē pašam, elementu meklēšana
   NEDRĪKST atgriezt pašu elementu (`<friction><friction>` ligzdošana) un
   `ET.iter()` neatbalsta `{*}` aizstājējzīmi.
9. SQLite `UPPER()` neapstrādā latviešu burtus — meklēt ar `LIKE` un pareizu
   reģistru vai salīdzināt Python pusē.

## Idejas tālākai lietošanai

- **Ziemas drošības panelis**: v_meteo_jaunakie berze + virsmas_t pie novada
  stacijām (A6 Ādmiņi/Saulkalne/Kaibala, P80 Zādzene/Ogresgals) → rīta
  brīdinājums pirms reisu logiem.
- **Maršruta drošības audits** (ATTACH visas db): reisa ceļu virkne ×
  prioritars (tīra pirmo ziemā) × masas ierobežojumi × aktīvie slēgumi.
- **Kartes slāņi**: novada izgriezums no celu_posms bbox (230 posmi ≈ 2–3 MB
  GeoJSON pēc vienkāršošanas — PMTiles šim mērogam nevajag); notikumu ikonas
  no v_aktivie_notikumi (sīks, dinamisks GeoJSON).
- **Sezonas atskaite pašvaldībai**: slideno dienu hronika pa ceļiem ×
  skolēnu maršruti — objektīvs pamats uzturēšanas prasībām LVC.
