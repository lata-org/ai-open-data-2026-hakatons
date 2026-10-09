# Darba plūsma: ceļu kartes datu izgūšana un aktualizēšana

`datubaze.py` UZBŪVĒTS un pārbaudīts ar dzīvo API 2026-07-31 (buvet/atjaunot/
statuss; multi-modeļu revīzija + testi). Avotu apraksts:
`PUBLISKO_DATU_IESPEJAS.md`; shēma: `db_shema.sql`. Robeža ar teritorijas bloku
aprakstīta abos PUBLISKO dokumentos: šeit līnijas un notikumi, tur poligoni un
statistika.

## API atslēga: kam vajag, kā iegūt, kur glabāt

**Kam vajag:** transportdata.gov.lv failu lejupielādei — VISĀM abonētajām kopām,
arī statiskajām GeoJSON/CSV (tā nosaka oficiālā REST specifikācija: failu
saraksts un `POST` lejupielāde iet ar atslēgu galvenē). BEZ atslēgas strādā
tikai kataloga/metadatu daļa (`GET /api/v1/subscriber/metadata_dcat` u.c.) —
tāpēc kataloga monitorings darbosies uzreiz, vēl pirms abonēšanas.

**Abonētās kopas (visas 17 abonētas 2026-07-31):**

| Prioritāte | Kopas |
|---|---|
| Obligāti — statiskie (6) | Valsts ceļu tīkls; ceļu posmi ar fiziskajiem atribūtiem; klasifikācija (A/P/V); prioritārie autoceļi; melnie punkti; ātruma ierobežojuma zīmju vietas |
| Obligāti — reāllaika (6) | Ceļu slēgumi; remontdarbi; īslaicīgie remontdarbi; īslaicīgi slidens ceļš (SIC); slikti ceļa apstākļi (uzturētāju ziņojumi); ceļu meteostaciju reāllaika mērījumi |
| Ieteicams (5) | Gājēju ceļi valsts tīklā; masas un gabarītu ierobežojumi; meteostaciju atrašanās vietas; braukšanas joslu slēgumi; negadījumi |

**Kur glabājas atslēgas (nekad čatā, nekad kodā, nekad git):**

APSTIPRINĀTS 2026-07-31: katrai kopai ir SAVA atslēga — atslēga pati identificē
abonēto kopu (pieprasījumos nav dataset_id, tikai galvene `x-api-key`). Visas
17 kopas abonētas, atslēgas noglabātas `dati/nap_atslegas.json`
(slug → {nosaukums, veids, card, atslega}) un pārbaudītas pret API (17/17
strādā). Galapunkti: failu saraksts `GET /api/v1/metadata/file/info`;
lejupielāde `POST /api/v1/get/file/download-file` ar ķermeni
`{"file_id","format"}` — reāllaika plūsmām `file_id="1"`, statiskajām kopām
file_id no failu saraksta.

`datubaze.py` lasīs `dati/nap_atslegas.json`; ja faila nav — lejupielādes soļi
izlaižas ar skaidru paziņojumu (tas pats tolerances princips kā ģeokodēšanas
solim iestāžu db). Atslēgas noplūdes gadījumā to pārģenerē NAP portālā
("Abonētie dati") — tāpēc arī ievaks žurnālā atslēgas nekad neierakstām.
Soli pa solim instrukcija ar visu kopu saitēm: `ABONESANA.txt`.

## Statiskais pret reāllaika — dalījums un ritmi

**Statiskie slāņi** (lejupielāde kā fails, hash-idempotenti, pilna aizstāšana):

| Kopa | Avota ritms | Mūsu ritms | Glabāšana |
|---|---|---|---|
| Ceļu tīkls, posmi+atribūti, klasifikācija, prioritārie | 2× gadā (BIANNUAL) | Pārbaude 1× mēnesī (hash; reāli mainīsies 2× gadā) | `celu_posms` (WKB līnijas) |
| Melnie punkti | ~reizi 3 gados (metadatos 2× gadā) | 1× mēnesī hash | `cela_punkts` — bagātināti: bāze lvceli.lv pilnais XLSX (38 ar ceļu/km/CSNg; NAP CSV tikai krustpārbaudei) + atvasinātās koordinātas no `dati/slani/` (sk. sadaļu zemāk) |
| Ātruma zīmju vietas | CONT metadatos, bet pēc dabas statisks slānis | 1× mēnesī | `cela_punkts` (tips) |
| Gājēju ceļi | 2× gadā | 1× mēnesī hash | `cela_papildslanis` |
| Masas ierobežojumi, meteostaciju vietas | 2× gadā; PIEGĀDE kā DATEX II plūsma (failu saraksts tukšs — lejupielādē ar `file_id="1"`, pārbaudīts 2026-07-31) | 1× mēnesī hash | `cela_papildslanis` / `cela_punkts` |
| OSM (Geofabrik pbf) | katru dienu | Reizi ceturksnī / pirms tīklu pārbūves | paliek faili + atvasinājumi (Valhalla/OTP), NE db |
| VZD Ielas/Autoceļi | VZD ritmā | līdzi kadastram | paliek ArcGIS cauruļvadā, NE db |

**Reāllaika REST plūsmas** (DATEX II V3 XML; katrs pieprasījums = momentuzņēmums,
ko pievieno notikumu vēsturei — nekad nepārraksta):

| Kopa | Avota ritms | Mūsu ritms (pull) |
|---|---|---|
| Ceļu slēgumi, joslu slēgumi | nepārtraukti | **Mācību dienās ik 30 min** reisu logos (06:00–09:00, 13:00–17:00); citādi 1× stundā |
| Remontdarbi (ilgtermiņa + īslaicīgie) | nepārtraukti | 2× dienā (mainās lēnāk) |
| Slidens ceļš, slikti apstākļi, laikapstākļi | nepārtraukti | **Ziemas sezonā (nov–mar) ik 30 min reisu logos**; vasarā 2× dienā |
| Meteostaciju mērījumi | nepārtraukti | Ziemā 1× stundā; vasarā izlaists |
| Negadījumi, nosprostojumi | nepārtraukti | 1× stundā |

Vēlākais uzlabojums: **MQTT abonements** (spec. to paredz) aizstāj pull ciklus
ar push — bet tikai tad, kad portālam būs pastāvīgi strādājošs process; pull
modelis der tāpēc, ka lēmumi tiek pieņemti reisu logos, ne nepārtraukti.

## Soļi (datubaze.py — uzbūvēts, uzvedības piezīmes)

1. **Katalogs (bez atslēgas)** — DCAT lejupielāde + hash; `nap_katalogs` tabula
   ar visu 55 kopu metadatiem un abonēšanas atzīmi; brīdinājums par jaunām
   kopām. DCAT saturā ir laika zīmogi, tāpēc hash praktiski vienmēr mainās —
   solis vienkārši pārlādē (lēts, 342 KB).
2. **Statiskie slāņi (ar atslēgu)** — failu saraksts → lejupielāde → GeoJSON/
   CSV/DATEX parsēšana → WKB + bbox tabulās; hash-idempotence pa kopām; raw
   arhīvs `dati/arhivs/` ar datumu. Apjoma atskaites punkts (2026-07-31):
   pilnais ceļu tīkls = 71,6 MB / 2 500 MultiLineString — kartes slāņiem
   obligāti vajadzīgs novada izgriezums + vienkāršošana, ne pilnais fails.
   ĪPATNĪBAS: `celu_posmi_atributi` ielādi izlaiž, kamēr platums/joslas avotā
   ir 100% tukši (dublētu tīkla ģeometriju); nulles parsēšana pēc pilnas
   tabulas NEpārraksta vecos datus un neieraksta hash (aizsardzība pret avota
   formāta maiņu); prioritāro atzīmi tīkla posmiem pārrēķina KATRĀ palaidienā
   (citādi tīkla pārlāde bez prioritāro pārlādes nodzēstu atzīmes).
3. **Reāllaika notikumi (ar atslēgu)** — DATEX II XML → `cela_notikums`
   INSERT OR IGNORE pa (kopa, datex_id, versija); vēsture tikai aug; `redzets`
   laiks atzīmē arī nemainītos ierakstus, un `v_aktivie_notikumi` rāda tikai
   pēdējā ievākumā redzētos derīguma logā (citādi notikumi bez beigu laika
   paliktu "aktīvi" mūžīgi). Meteo mērījumi glabājas ar stacijas id un
   mērvērtību JSON (berze, temperatūras, vējš...); koordinātas caur
   `cela_punkts` meteostacijām.
4. **Statuss** — atslēgas esamība, katras kopas pēdējā ielāde, aktīvie
   notikumi pa tipiem, meteostaciju jaunākie mērījumi, kataloga izmaiņas.

## Melno punktu izgūšanas ķēde (koordinātas NAV nevienā avotā!)

Neviens publiskais avots melno punktu koordinātas nedod, tāpēc tās ir
ATVASINĀTAS vairāku soļu ķēdē (katram punktam db atribūtos `ticamiba` un
`metode`):

1. **Avoti**: NAP CSV (34 apraksti, bez ceļa/km, ar kļūdām — piem., "Annas"
   punktam nepareizs ceļš) + **lvceli.lv pilnais 2020.–2022. XLSX**
   (`dokumentacija/paraugi/melnie_punkti_2020_2022_pilns.xlsx` — 38 punkti,
   katram pamatceļš, km un CSNg statistika; NAP CSV izrādās nepilna kopija).
2. **Orientieru ģeokodēšana** (multi-modeļu workflow): sonnet aģenti ģeokodē
   aprakstu orientierus (ezeri, ciemi, kanāli, DUS) caur OSM Nominatim/
   Overpass un kadastra ciemu centroīdiem, projicē uz ceļa ass; opus aģenti
   katru lokalizāciju adversāri verificē ar neatkarīgu pārrēķinu. Verdikti:
   `dati/slani/melnie_punkti_lokalizacijas.json`.
3. **km interpolācija ar kalibrāciju** (`skripti/melnie_punkti_slanis.py`):
   punktu liek uz pamatceļa ass km atzīmē; katra ceļa līnijas VIRZIENU un
   NOBĪDI kalibrē pret 2. soļa verificētajiem punktiem (celi.db klasifikācijas
   līnijām trūkst pilsētu posmu — A10 nobīde 14,6 km, A7 robs pie Bauskas!).
   Ja verificētais punkts ir <= 2,5 km no km punkta, uzvar verificētais
   (precīzāks par veselu km). Rezultāts: 38/38 ar koordinātām (30 augsta).
4. **Ielāde db** (`datubaze.py` melnie_punkti solis): bāze = pilnais XLSX,
   koordinātas no 3. soļa slāņa, NAP CSV tikai krustpārbaudei ievaks piezīmē.
   (Manuālās precizēšanas web rīks kādreiz bija atsevišķā projektā
   melno-punktu-redaktors — dzēsts 2026-07-31 kā vairs nevajadzīgs; ja
   precizēšana atkal kļūst aktuāla, vidējās ticamības punktus var labot
   tieši slāņa GeoJSON un pārlaist ielādi.)

Atjaunojot avotus (jauns LVC saraksts ~2029): lejupielādēt jauno XLSX uz
dokumentacija/paraugi/, pārlaist skripti/melnie_punkti_slanis.py, tad
datubaze.py atjaunot --piespiest.

## Datu nesajaukšanas principi

- Robežu poligonus NEdublē (teritorijas.db caur ATTACH); pieturas/maršruti —
  sabiedriskais-transports; OSM/VZD ģeometrijas paliek failu cauruļvados —
  db glabā tikai NAP slāņus un notikumus.
- `cela_notikums` vēsture tikai aug — ziemas analīzēm ("cik bieži posms bijis
  slidens") vajadzīga pilna notikumu hronika ar ielādes momentuzņēmumiem.
- Katrai rindai `avots`/`kopa` marķējums — viens notikumu tips nāk no 3 avotiem
  (SIC / uzturētāji / meteostacijas), tos nekad nesapludina bez marķējuma.
