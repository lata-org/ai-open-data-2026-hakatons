# Publisko datu iespējas ceļu kartei

Pārbaudīts praktiski 2026-07-30: transportdata.gov.lv katalogs izgūts caur tā
publisko API un **visas 55 datu kopas analizētas** (paralēla multi-aģentu
analīze); piekļuves modelis — no oficiālās "Datu ņēmēja REST API specifikācijas"
(lejupielādētā `dn_rest_lv.html`, LVC, CC0). Konteksts: portāla ceļu tīkla,
ceļu stāvokļa un maršrutu drošības slāņi.

## Īsais kopsavilkums

Ceļu ĢEOMETRIJU portāls jau iegūst no OSM un VZD (pārbaudīta prakse). Jaunais
atradums ir **transportdata.gov.lv (Nacionālais piekļuves punkts, NAP)** — LVC
uzturēts katalogs ar 55 kopām: valsts ceļu tīkls GeoJSON ar atribūtiem un
klasifikāciju, melnie punkti, un **reāllaika DATEX II plūsmas** (slidens ceļš,
slēgumi, remonti, negadījumi) — tieši ziemas drošības slānis skolēnu
maršrutiem. Katalogs un metadati ir publiski; failu lejupielādei vajag
**bezmaksas abonēšanu + API atslēgu** (lietotājam tāda iespēja ir). Svarīgā
robeža: NAP sedz tikai VALSTS ceļus — pašvaldību ceļi un ielas paliek OSM/VZD
pusē.

---

## A. Ceļu tīkla ģeometrija (projektā jau pārbaudītā prakse)

| Avots | Loma | Piezīmes no prakses |
|---|---|---|
| **OSM caur Overpass API** | Gājēju tīkls sasniedzamībai: bbox vaicājums ar ceļu tipiem, atstājot `path`, `footway`, `cycleway` — skolēni iet kājām | Spoguļu cikls + User-Agent obligāts; pilnajam apjomam labāks Geofabrik |
| **Geofabrik `latvia-latest.osm.pbf`** | Valhalla izohronas + OTP multimodālais grafs; gājēju ceļu ekstrakcija (36 861 posms Ogres apkārtnē, t. sk. 3 602 taciņas) | Atjauno katru dienu; ~139 MB; Geofabrik 502 mēdz būt viņu CDN puses problēma |
| **VZD Ielas + Autoceļi** (atvērtie dati) | ArcGIS network dataset (gājēju tīkls bez taciņām) | Garās polilīnijas jāsadala krustpunktos; 64 bitu OID GPKG slazds |
| LĢIA topo 1:10 000 | Atsauce: CSP tieši ar to rēķina attālumus pa ceļiem (TEA metodika) | Nav brīvi lejupielādējams slānis, bet apliecina metodikas savietojamību |

## B. transportdata.gov.lv — Nacionālais piekļuves punkts (NAP)

**Kas tas ir:** ITS direktīvas nacionālais piekļuves punkts, uztur VSIA
"Latvijas Valsts ceļi". React SPA katalogs (tāpēc parasta lapas ielāde neko
nerāda), bet **API ir atvērts un dokumentēts** (OpenAPI spec ar CC0 licenci).

**Piekļuves modelis (no oficiālās REST specifikācijas):**

| Darbība | Galapunkts | Atslēga? |
|---|---|---|
| VISU kopu katalogs DCAT/RDF | `GET https://www.transportdata.gov.lv/api/v1/subscriber/metadata_dcat` | **Nē** (pārbaudīts — 342 KB, 55 kopas) |
| Vienas kopas DCAT | `GET /api/v1/subscriber/metadata_dcat/{dataset_id}` | Nē |
| Kopas metadati JSON (apraksti, kategorijas, koordinātu sistēma, parauga faili) | `GET /lv/public/metadata/data?dataset_id=<nid>` — nid ir SKAITLISKS (no failu saraksta lauka `dataset`), ar kartītes UUID atgriež kļūdu | Nē |
| Kopas failu saraksts | `GET /api/v1/metadata/file/info` (galvene `x-api-key`) | **Jā** |
| Faila lejupielāde | `POST /api/v1/get/file/download-file` (`{"file_id","format"}`; plūsmām `file_id="1"`) | **Jā** |
| Izmaiņu/mērījumu push | **MQTT saskarne** | Jā |

API atslēgu iegūst, reģistrējoties un abonējot konkrētas kopas (bezmaksas;
licences pārsvarā "royalty free"). Atslēga ir KATRAI kopai sava un pati
identificē kopu — pieprasījumā dataset_id nenorāda. Statuss 2026-07-31: visas
17 ieteiktās kopas abonētas, atslēgas `dati/nap_atslegas.json` (sk. `ABONESANA.txt`). Metadatos katrs ieraksts satur formātu
(pārsvarā **DATEX II V3 XML**; statiskajiem slāņiem GeoJSON/CSV), atjaunošanas
biežumu (CONT = nepārtraukti vai BIANNUAL = 2× gadā) un komunikācijas veidu
(Push/Pull).

**Katalogā 55 kopas:** 52 LVC, 2 Eco-Movement (e-uzlāde), 1 Rīgas pašvaldības
policija. Tēmu virsotne: negaidīti ceļu notikumi (24), ceļu laikapstākļi (9),
slikti ceļa apstākļi (8), negadījumi (7), statiskais tīkls (5).

### Augstas noderības kopas portālam (analīzes rezultāts — 25)

**Statiskais tīkls un drošības kartējums** (GeoJSON, 2× gadā; ātruma zīmes — nepārtraukti):

| Kopa | Kāpēc portālam |
|---|---|
| Valsts ceļu tīkls (ģeometrija + klasifikācija A/P/V) | Pamatslānis maršrutu kartei |
| Ceļu posmi ar fiziskajiem atribūtiem (platums, joslas, garumi) | Maršrutu piemērotība autobusiem |
| **Prioritārie autoceļi** (MK 188 — ziemā tīra pirmos) | Drošāko maršrutu izvēle ziemā |
| **Melnie punkti** (bīstamie posmi/krustojumi; CSV, pārskata ~reizi 3 gados). NAP CSV ir nepilns un bez koordinātām — PILNAIS saraksts ar ceļu/km/CSNg: lvceli.lv (https://lvceli.lv/celu-tikls/celu-kartes/melnie-punkti/, XLSX pielikums; lokāli dokumentacija/paraugi/); koordinātu atvasināšana: PLUSMA.md | Riska vietas maršrutos |
| Ātruma ierobežojuma zīmju vietas | Drošības vērtējums + laika aprēķini |

**Reāllaika DATEX II plūsmas** (nepārtraukti; katram notikumu tipam līdz 3
avotiem — Satiksmes informācijas centrs / ceļu uzturētāji / meteostacijas):

| Kopa | Kāpēc portālam |
|---|---|
| **Ceļu slēgumi** + braukšanas joslu slēgumi | Kritiski: slēgts posms = tūlītējs apvedceļš |
| **Ceļu remontdarbi** + īslaicīgie darbi | Maršrutu kavējumi un riski |
| **Īslaicīgi slidens ceļš** (3 avoti) | Ziemas drošības kodols skolēnu reisiem |
| Slikti ceļa apstākļi (3 avoti) + laikapstākļi, kas ietekmē segumu | Ziemas uzturēšanas aina |
| Ceļu meteostaciju reāllaika mērījumi | Objektīvi sensoru dati (apledojums) |
| Negadījumi, nenorobežotas negadījumu vietas, nosprostojumi | Operatīvie drošības brīdinājumi |
| Ārkārtēji laikapstākļi (SIC + meteostacijas) | Lēmumi par reisu atcelšanu |

### Vidējas noderības (13) — atlasīti interesantākie

- **Gājēju ceļi valsts autoceļu tīklā** (GeoJSON) — vai pie pieturas ir ietve
  (papildina OSM, oficiālais avots);
- Masas un gabarītu ierobežojumi (tilti ar tonnāžu — lieliem autobusiem);
- Brīdinājuma zīmju vietas; satiksmes intensitāte/ātrums (minūšu un stundu
  griezums — tikai skaitītāju punktos); meteostaciju vietas (atslēga reāllaika
  datu piesaistei); bojāts aprīkojums; šķēršļi uz ceļa.

### Zemas noderības (17)

Kravas stāvvietas, vinjetes, e-uzlāde (Eco-Movement + LVC), TEN-T, mainīgās
zīmes tikai A2/E77 un E67 koridoros (neskar Ogri — novadam aktuāla A6/E22),
Rīgas policijas kameras (tikai Rīga), robežšķērsošanas rindas, nobraukuma
statistika.

## C. Ieteikums abonēšanai (kad ņemat API atslēgu)

Minimālais komplekts ceļu kartei: **Valsts ceļu tīkls + posmi ar atribūtiem +
klasifikācija + prioritārie ceļi + melnie punkti + ātruma zīmes** (statiskie,
lejupielāde 2× gadā) un **slēgumi + remontdarbi + slidens ceļš (SIC) + slikti
ceļa apstākļi (uzturētāji) + meteostaciju mērījumi** (reāllaika; sākumā pull,
vēlāk MQTT push). Tas dod pilnu "valsts ceļu drošības" slāni virs OSM/VZD
ģeometrijas.

## Robeža ar teritorijas bloku

Dalījuma princips: **celu-karte = "pa ko pārvietojas un kādā stāvoklī"** (ceļu
līnijas/punkti + notikumi uz tiem, ritms līdz reāllaikam), **teritorijas =
"kur un kas dzīvo"** (poligoni/režģa šūnas + statistika, ritms gadi).

- Šajā blokā glabāsies: ceļu tīkla ģeometrijas (OSM, VZD, NAP valsts ceļu
  posmi ar atribūtiem), klasifikācija, prioritārie ceļi, zīmes, melnie punkti,
  gājēju ceļi valsts tīklā, masas ierobežojumi, reāllaika DATEX II notikumi.
- Teritoriju pusē paliek: robežas (šeit tikai ATTACH kā telpiskais filtrs —
  nedublēt!), iedzīvotāji/demogrāfija, TEA, svārstmigrācija, režģa šūnas.
- Pieturas un maršruti — sabiedriskais-transports blokā (GTFS); Valhalla/OTP
  maršrutēšanas tīkli ir atvasinājumi no šī bloka avotiem, ne krātuve.
- Tipiskais apvienojošais vaicājums (ATTACH visas db): "slidenā ceļa notikumu
  biežums pa pagastiem ziemā" = šī bloka notikumi × teritoriju robežas.

## D. Izgūšana un atjaunināšana (kad būvēsim)

- **Kataloga uzraudzība bez atslēgas:** DCAT galapunkta satura hash (tas pats
  idempotences princips kā citos blokos) — jaunas kopas vai metadatu izmaiņas
  pamana automātiski.
- Statiskie GeoJSON/CSV: hash pārbaude 1× mēnesī, reāla lejupielāde ~2× gadā
  (avota BIANNUAL ritms) — ritmu detaļas PLUSMA.md.
- Reāllaika DATEX II: pull ar atslēgu pēc vajadzības (piem., katru rītu pirms
  reisiem) vai MQTT abonements nepārtrauktai plūsmai; DATEX II V3 XML parsēšanai
  ir gatavas shēmas (Datex 3.4).
- OSM/VZD ģeometrijas ritmi — kā transporta bloka PLUSMA.md (Geofabrik reizi
  ceturksnī, VZD līdzi kadastram).

Piezīme par piekļuvi: zenrows nebija vajadzīgs — SPA aizsegs slēpj tikai UI,
API ir atklāts; lokāli saglabātā REST specifikācija izrādījās pilnīga un
precīza (visi galapunkti pārbaudīti pret dzīvo vidi).

## Oficiālā dokumentācija (lokālais spogulis: dokumentacija/)

Visu 17 abonēto kopu oficiālie metadati un parauga faili lejupielādēti
2026-07-31 uz `dokumentacija/` (metadati/, paraugi/); salīdzinājums
"deklarētais pret piegādāto" un parsera validācija pret oficiālajiem
paraugiem (t. sk. ziemas plūsmām) — `dokumentacija/DOKUMENTACIJA.md`.
Galvenās nesakritības: posmu kopai deklarētie platums/joslas ir 100% tukši;
melno punktu piegādātajā CSV nav paraugā dokumentēto ceļš/km/CSNg kolonnu;
ātruma zīmes ir 14 punktu izlase, ne valsts pārklājums.
