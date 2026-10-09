# Pašvaldību civilās aizsardzības plāni: hakatona starta komplekts

Latvijas 42 pašvaldību sadarbības teritoriju civilās aizsardzības (CA) plāni mašīnlasāmā Markdown formātā, saistīto atvērto datu apraksti, datubāzu shēmas, ielādes skripti un lokālie datu faili. Komplekts sagatavots VARAM atvērto datu un mākslīgā intelekta hakatonam 2026, lai komandas varētu uzreiz sākt darbu ar krīzes pārvaldības tēmu, nevis vākt un konvertēt dokumentus.

Komplektā apzināti **nav** oriģinālo PDF, DOCX un ODT failu (aptuveni 790 MB), konvertēšanas starpfailu un lapu attēlu. To vietā katrai pašvaldībai ir `originali/<slug>/AVOTS.md` ar saiti uz oficiālo publikāciju, faila izmēru un sha256 kontrolsummu, pēc kuras oriģinālu var lejupielādēt un pārbaudīt.

## Kas ir komplektā

| Mape vai fails | Saturs |
|---|---|
| `markdown/<slug>/` | 41 mape ar 306 konvertētiem dokumentiem: plāni, pielikumi, domes lēmumi. Katrā mapē `STRUKTURA.md` ar dokumenta nodaļu koku un atbilstību MK noteikumu Nr. 658 prasībām. Ventspils novadam plāns ir kopīgs ar Ventspils valstspilsētu (`markdown/ventspils/`). |
| `originali/<slug>/` | Tikai metadati: `AVOTS.md` (kur publicēts, apstiprināšanas lēmums, versija) un `faili.json` (URL, izmērs, sha256). Pašu failu nav. |
| `avoti/` | Atvērto datu katalogs un integrācijas rīki: VZD adrešu reģistrs un kadastrs (datu modeļi, SQLite shēma, ielādes skripts), LVC ceļu tīkls un DATEX II plūsmas (shēma, skripts, dokumentācija), VUGD publiskās patvertnes (781 objekts GeoJSON, CSV un JSON formātā), Ogres novada robeža un evakuācijas vietas. |
| `pasvaldibas.csv`, `pasvaldibas.md` | 42 pašvaldību reģistrs ar ATVK kodiem un pārbaudītām mājas lapām. |
| `darba_saraksts.json` | Katrai pašvaldībai VUGD norādītā plāna publikācijas saite un norāde uz kopīgu plānu. |
| `dokumentacija/` | Metodiskie dokumenti: atvērto datu izmantošana CA plānošanā un data.gov.lv CKAN API, plānu konvertēšanas uzdevums LLM aģentam, vizuālās rekonstrukcijas un datu aizstāšanas matrica, Ogres interaktīvā plāna koncepcija. |
| `prototipi/` | Divas Ogres novada CA plāna interaktīvās HTML versijas (viens fails, atverams pārlūkā). |
| `vietne/` | Astro statiskās vietnes prototips: plānu salīdzinājums pēc MK 658 prasībām, novada pārskats ar kartēm un diagrammām, pilns plāna teksts. Izvērsti Ogres un Cēsu novadi. |
| `tools/` | Python skripti plānu lejupielādei, konvertēšanai uz Markdown (pymupdf4llm, pandoc, LibreOffice) un reģistra veidošanai. |

## Ātrais sākums

**Lasīt plānu.** Atver `markdown/<slug>/STRUKTURA.md`, tad pašu plāna failu. Plāna Markdown failos ir YAML galvene un lapu marķieri `<!-- lpp. N -->`, pēc kuriem var atsaukties uz oriģināla lappusi.

**Lietot patvertņu datus.** `avoti/patvertnes/patvertnes_latvija_112.geojson` ielādējas tieši Leaflet, MapLibre vai QGIS. Lauku apraksts un atjaunošanas komanda ir `avoti/patvertnes/README.md`.

**Uzbūvēt adrešu datubāzi.** Skripts `avoti/kadastrs/atjaunot.py` lejupielādē VZD adrešu reģistra atvērtos datus un ieliek SQLite datubāzē pēc shēmas `avoti/kadastrs/shema.sql`. Vajadzīgs `uv`:

```bash
cd avoti/kadastrs
uv run --no-project --with httpx --with certifi atjaunot.py --bez-vestures
```

**Palaist vietni.**

```bash
cd vietne
pnpm install
pnpm sagatavot   # kopē plānus no ../markdown un ģeodatus no ../avoti
pnpm dev         # http://localhost:4321
```

**Konvertēt jaunu dokumentu.** Skripti mapē `tools/` darbojas ar `uv run`. Lejupielādes un meklēšanas skriptiem ar ZenRows vajadzīgs vides mainīgais `ZENROWS_API_KEY`; bez tā tie strādā tiešā režīmā vai apstājas ar paziņojumu.

## Idejas hakatonam

- Plānu salīdzināšana: kuras MK 658 obligātās sadaļas trūkst, cik veci ir plāni, kur evakuācijas vietas nav ģeokodētas.
- Patvertņu pieejamība: attālums no dzīvesvietas līdz tuvākajai patvertnei, pārklājuma caurumi, salīdzinājums ar iedzīvotāju blīvumu.
- Plānos minēto objektu ģeokodēšana ar VZD adrešu reģistru un attēlošana kartē.
- Reāllaika slāņi: LVC ceļu slēgumi un meteostacijas, LVĢMC brīdinājumi virs plāna evakuācijas maršrutiem.
- Jautājumu atbildēšana par plāniem ar LLM: "kur Ogrē pulcējas evakuācijas gadījumā", "kas apziņo iedzīvotājus Jūrmalā".

## Datu avoti un lietošanas nosacījumi

- CA plāni ir pašvaldību publicētas publiskās versijas. Vairākas pašvaldības norāda, ka publiskā versija ir saīsināta personas datu un ierobežotas pieejamības informācijas dēļ. Konvertēšana var saturēt kļūdas; strīdus gadījumā noteicošais ir oriģināls, uz kuru norāda `originali/<slug>/AVOTS.md`.
- Adrešu reģistrs un kadastrs: Valsts zemes dienests, data.gov.lv, licence CC BY 4.0.
- Ceļu tīkls un DATEX II plūsmas: VSIA Latvijas Valsts ceļi, transportdata.gov.lv.
- Patvertnes: VUGD un IeM Informācijas centrs, 112.lv.

Metodiskie dokumenti un daļa konvertāciju tapuši ar LLM aģentu palīdzību 2026. gada septembrī. Stāvoklis uz 2026-09-13.
