# NAP kopu oficiālā dokumentācija un tās salīdzinājums ar realitāti

Savākta 2026-07-31 visām 17 abonētajām kopām. Šī mape ir **lokālais
dokumentācijas spogulis** — uz to atsaucas PLUSMA.md un nākotnes izmaiņu
diagnostika (ja avots mainās, vispirms salīdzina ar šeit saglabāto).

## Kur portāls tur dokumentāciju (viss bez API atslēgas)

| Kas | Kur | Piezīmes |
|---|---|---|
| Kopas metadati (apraksts LV/EN, kategorijas, formāts, ritms, koordinātu sistēma, DATEX publikācijas tips, regula, versija) | `GET /lv/public/metadata/data?dataset_id=<nid>` | **nid ir skaitlisks** (ne kartītes UUID — ar UUID galapunkts atgriež servera kļūdu!); nid iegūstams no failu saraksta atbildes lauka `dataset` |
| Oficiālie parauga faili | `field_field_data_sample` ceļš (piem. `/npp-test/public/2024-08/temporarySlipperyRoad.xml`) | 15/17 kopām ir; ziemas plūsmām tas ir VIENĪGAIS veids redzēt struktūru vasarā |
| Apraksta faili (datu vārdnīca) | `field_dataset_desc_file` / `_lv` | Tikai prioritārajiem ceļiem (txt ar lauku skaidrojumiem) |
| DATEX II shēmas | Palīdzības lapa /lv/49307 ("DATEX II datu shēmas") | LVC profils, modelBaseVersion=3 |
| REST/MQTT API specifikācijas | Palīdzības lapa /lv/27281 | REST spec lokāli: Downloads/DN_LV_REST_HTML |

Mapes saturs: `metadati/<slug>.json` (pilnie metadati + `_kopsavilkums.json`),
`paraugi/<slug>_paraugs.<ext>` (oficiālie paraugi + prioritāro apraksta txt).

## Deklarētais pret piegādāto (pārbaudīts pret mūsu profilēm un celi.db)

Sakrīt pilnībā (12/17): koordinātu sistēma **WGS84 deklarēta un apstiprināta
visām kopām**; DATEX publikācijas tipi (SituationPublication /
MeasuredDataPublication / MeasurementSiteTablePublication) sakrīt ar failiem;
`masas_ierobezojumi` "GeoJSON + Datu izmaiņu plūsma" un `meteo_vietas`
"plūsma ar pusgada ritmu" — mūsu novērotās "dīvainības" izrādās precīzi
dokumentēta uzvedība.

**Nesakritības (dokumentēts ≠ piegādāts):**

| Kopa | Dokumentācija sola | Realitāte |
|---|---|---|
| `celu_posmi_atributi` | Satura kategorijas: "Gradienti, Savienojumi, **Joslu skaits, Ceļa platums**" | Lauki `autocela_platums` un `brauksanas_joslu_skaits` ir 100% tukši visos 2500 posmos; gradientu lauka nav vispār. Tāpēc datubaze.py šo kopu apzināti neielādē (dublētu tīklu) |
| `melnie_punkti` | Koordinātu sistēma WGS84; paraugā (XLSX) strukturētas kolonnas: **Autoceļš, km, CSNg, bojāgājušie, ievainotie**, posma apraksts | Piegādātajā CSV nav ne koordinātu, ne ceļa/km kolonnu, ne negadījumu statistikas — tikai brīvteksta nosaukums. ATRISINĀTS: pilnais saraksts (38 punkti ar VISĀM kolonnām) publicēts lvceli.lv — `paraugi/melnie_punkti_2020_2022_pilns.xlsx` (https://lvceli.lv/wp-content/uploads/2023/09/2020-2022-jaunais_sutisanai-1.xlsx); NAP CSV izrādās tā nepilna kopija ar kļūdām (piem., "Annas" punkts īstenībā ir uz A9, ne A6) |
| `atruma_zimes` | Ritms "Pastāvīgi"; valsts tīkla ātruma ierobežojumu zīmju vietas | Failā tikai 14 punkti (izlase/pilots, ne valsts pārklājums); properties satur ~30 citu objektu klašu tukšus laukus |
| `valsts_celu_tikls` | Kategorija "Ceļu klasifikācija" | Sakrīt saturiski, bet nosaukumu līmenī tīkls un klasifikācija ir divas dažādas kopas ar 90% pārklājumu (2500 posmi pret 1582 maršrutiem) |

## Parsera validācija pret oficiālajiem paraugiem (2026-07-31)

`datubaze.py` `_situacijas`/`_meteo_merijumi`/`_ielade_meteo_vietas` palaisti
pret 9 oficiālajiem paraugiem — **visi iztur**, ieskaitot vasarā tukšās
ziemas plūsmas:

- `slidens_sic` paraugs: `WeatherRelatedRoadConditions` ar `ice`/`blackIce` un
  `NonWeatherRelatedRoadConditions` ar `looseChippings` — visi tipi nonāk
  atributi JSON (vispārīgā lauku savākšana, ne cietais saraksts);
- `slikti_apstakli_uzturetaji`: `freezingRain`/`ice`/`wet` + ierobežojuma tips;
- `negadijumi` paraugs atklāj tipus, kas dzīvajā vēl nav redzēti:
  `InfrastructureDamageObstruction`, `GeneralObstruction` ar `hazardsOnTheRoad`
  — arī tie tiek noķerti;
- `meteo_merijumi` paraugs: berze 3/3, virsmas stāvoklis 3/3;
- koordinātas 100% visos situāciju paraugos.

Secinājums: parseris ir gatavs ziemas sezonai, un paraugi kalpo kā
regresijas fikstūras — ja LVC maina struktūru, tests pret `paraugi/` to
parādīs pirms dzīvās plūsmas.
