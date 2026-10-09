# Latvijas publisko patvertņu vienotā datubāze (VUGD / 112.lv)

Šajā mapē apkopoti visi Latvijas publisko patvertņu dati, kas izgūti no Valsts ugunsdzēsības un glābšanas dienesta (VUGD) un Iekšlietu ministrijas Informācijas centra (IeM IC) oficiālā portāla [112.lv/lv/patvertnes](https://www.112.lv/lv/patvertnes).

---

## 1. Datu avots un tehniskie parametri

- **Oficiālā vietne:** [https://www.112.lv/lv/patvertnes](https://www.112.lv/lv/patvertnes)
- **Pakalpojuma sniedzējs:** Iekšlietu ministrijas Informācijas centrs (IeM IC) / VUGD
- **ArcGIS WebMap Item ID:** `61de68b5c6d34e0a88cd1c6f3cf811cd`
- **ArcGIS REST FeatureServer galapunkts:**  
  `https://services9.arcgis.com/f2QOaaoX08g1sAc2/arcgis/rest/services/PatvertnesDati_view/FeatureServer/0`
- **Kopējais patvertņu skaits Latvijā:** **781 objekts**
- **Ģeometrijas tips:** Punkts (`Point`)
- **Koordinātu sistēma:** WGS-84 (`EPSG:4326`)

---

## 2. Datu faili mapē

1. 🗺️ **[`patvertnes_latvija_112.geojson`](./patvertnes_latvija_112.geojson)** — Pilna GeoJSON ģeotelpiskā datne, gatava tūlītējai ielādei Leaflet, MapLibre, QGIS vai ArcGIS;
2. 📊 **[`patvertnes_latvija_112.csv`](./patvertnes_latvija_112.csv)** — Tabulārie dati (UTF-8 ar BOM) ar koordinātēm, adresēm un ēkas lietošanas veidu Excel un datubāzēm;
3. 📦 **[`patvertnes_latvija_112.json`](./patvertnes_latvija_112.json)** — JSON masīvs integrācijai tīmekļa lietotnēs un API.

---

## 3. Datu atribūti

| Atribūts | Apraksts | Piemērs |
| :--- | :--- | :--- |
| `objectid` | Unikāls objekta ID sistēmā | `1` |
| `pilsetasvaiapdzvietasnosaukums` | Pilsēta, pagasts, novads | `Jaunpiebalga, Jaunpiebalgas pagasts, Cēsu novads` |
| `ielasnosaukums` | Ielas vai māju nosaukums | `Gaujas iela` |
| `ekasnumurs` | Ēkas numurs | `2a` |
| `ekasgalvlietosanasveids` | Ēkas galvenais lietošanas veids | `Kultūras nams`, `Skola`, `Daudzdzīvokļu māja` |
| `lat` / `lon` | Ieejas durvju koordinātas (WGS-84) | `57.180357`, `26.055227` |
| `komentars` | Papildu norādes par ieeju | `Ieeja no pagalma puses` |
| `globalid` | Universālais unikālais identifikators | `67f21bbc-87d8-468c-8406-7d39454625bf` |

---

## 4. Patvertņu pārklājums pa pašvaldībām (Top 20)

| Reģions / Pašvaldība | Patvertņu skaits |
| :--- | :---: |
| **Rīga** | 106 |
| **Jēkabpils novads** (t.sk. pilsēta) | 47 |
| **Cēsu novads** (t.sk. pilsēta) | 45 |
| **Aizkraukles novads** | 30 |
| **Jelgavas novads un Jelgava** | 38 |
| **Ogres novads un Ogre** | 31 |
| **Tukuma novads un Tukums** | 30 |
| **Augšdaugavas novads un Daugavpils** | 52 |
| **Smiltenes novads** | 25 |
| **Madonas novads** | 25 |
| **Dobeles novads** | 21 |
| **Jūrmala** | 17 |
| **Rēzekne un Rēzeknes novads** | 31 |
| **Saldus novads** | 15 |
| **Valmieras novads** | 14 |
| **Gulbenes novads** | 14 |
| **Ķekavas novads** | 11 |
| **Bauskas novads** | 11 |
| **Kuldīgas novads** | 10 |
| **Preiļu novads** | 8 |

---

## 5. Datu atjaunināšana

Datus var jebkurā laikā atkārtoti sinhronizēt, izsaucot pieprasījumu pret oficiālo IeM IC REST servisu:

```bash
uv run --with httpx python -c "
import httpx, json
url = 'https://services9.arcgis.com/f2QOaaoX08g1sAc2/arcgis/rest/services/PatvertnesDati_view/FeatureServer/0/query'
params = {'where': '1=1', 'outFields': '*', 'f': 'geojson', 'outSR': '4326'}
r = httpx.get(url, params=params, timeout=60)
with open('avoti/patvertnes/patvertnes_latvija_112.geojson', 'w', encoding='utf-8') as f:
    json.dump(r.json(), f, ensure_ascii=False, indent=2)
print('Atjaunots veiksmīgi!')
"
```
