# VAR Atvērto Datu Modelis

> Izsmeļošs Latvijas Valsts adrešu reģistra atvērto datu apraksts no Valsts zemes dienesta (VZD).
> Datu avots: Valsts adrešu reģistra informācijas sistēma (VARIS).
> Atjaunināts: 2026-02-23 | Licence: CC-BY-4.0 | Atjaunināšanas biežums: katru dienu

---

## Satura rādītājs

1. [Pārskats](#1-pārskats)
2. [Latvijas administratīvais iedalījums](#2-latvijas-administratīvais-iedalījums)
3. [Datu kopu struktūra](#3-datu-kopu-struktūra)
4. [Entītiju relāciju modelis](#4-entītiju-relāciju-modelis)
5. [Detalizētas shēmas pa resursiem](#5-detalizētas-shēmas-pa-resursiem)
6. [Klasifikatori](#6-klasifikatori)
7. [Sasaiste ar NĪVKIS](#7-sasaiste-ar-nīvkis)
8. [Lietošanas scenāriji](#8-lietošanas-scenāriji)
9. [Tehniskie norādījumi](#9-tehniskie-norādījumi)
10. [CKAN API pieejas punkti](#10-ckan-api-pieejas-punkti)
11. [Datu lejupielādes URL saraksts](#11-datu-lejupielādes-url-saraksts)
12. [Datu normalizācijas ieteikumi](#12-datu-normalizācijas-ieteikumi)

---

## 1. Pārskats

### 1.1 Kas ir VAR atvērtie dati?

VZD publicē Latvijas atvērto datu portālā (data.gov.lv) denormalizētus Valsts adrešu reģistra datus:
- **Teksta dati** CSV formātā (atjaunināti katru dienu)
- **Telpiskie dati** SHP formātā (atjaunināti reizi nedēļā)

Dati nodrošina pilnu Latvijas adresācijas objektu uzskaiti ar unikāliem, nemainīgiem 9 ciparu kodiem.

### 1.2 Metadati

| Parametrs | Vērtība |
|-----------|---------|
| **Nosaukums** | Valsts adrešu reģistra atvērtie dati |
| **Publicētājs** | Valsts zemes dienests (VZD) |
| **Kontakts** | dati@vzd.gov.lv |
| **Licence** | CC-BY-4.0 |
| **CKAN dataset ID** | `varis-atvertie-dati` |
| **CKAN UUID** | `6b06a7e8-dedf-4705-a47b-2a7c51177473` |
| **Formāts** | CSV (UTF-8 BOM), SHP (ZIP) |
| **Teksta datu atjaunināšana** | Katru dienu |
| **Telpisko datu atjaunināšana** | Reizi nedēļā |
| **HVD** | Augstvērtīga datu kopa (ES HVD) |

### 1.3 Termini un saīsinājumi

| Saīsinājums | Pilns nosaukums |
|-------------|-----------------|
| **VAR** | Valsts adrešu reģistrs |
| **VARIS** | Valsts adrešu reģistra informācijas sistēma |
| **VZD** | Valsts zemes dienests |
| **ATVK** | Administratīvo teritoriju un teritoriālā iedalījuma vienību klasifikators |
| **NĪVKIS** | Nekustamā īpašuma valsts kadastra informācijas sistēma |
| **LKS-92** | Latvijas ģeodēziskā koordinātu sistēma |
| **WGS84** | Pasaules ģeodēziskā sistēma (GPS) |

### 1.4 Normatīvie akti

| Dokuments | Saite |
|-----------|-------|
| Administratīvo teritoriju un apdzīvoto vietu likums | https://likumi.lv/ta/id/315654 |
| Adresācijas noteikumi (MK Nr. 698) | https://likumi.lv/ta/id/324387 |
| ATVK klasifikatora noteikumi (MK Nr. 379) | https://likumi.lv/ta/id/324030 |

---

## 2. Latvijas administratīvais iedalījums

### 2.1 Teritoriju hierarhija

```
Latvijas Republika (kods: 100000000)
├── Valstspilsētas (7 gab.)
│   ├── Rīga, Daugavpils, Jelgava, Jūrmala
│   ├── Liepāja, Rēzekne, Ventspils
│   └── → Ielas → Ēkas → Telpu grupas
│
└── Novadi (43 gab.)
    ├── Pilsētas (novada pilsētas) → Ielas → Ēkas → Telpu grupas
    └── Pagasti → Ciemi/Mazciemi → Ielas → Ēkas → Telpu grupas
```

### 2.2 Apdzīvoto vietu veidi

| Veids | Apraksts |
|-------|----------|
| **Valstspilsēta** | Republikas nozīmes pilsēta ar pašvaldības statusu |
| **Novada pilsēta** | Pilsēta novada teritorijā |
| **Ciems** | Teritorija ar koncentrētu apbūvi, ar noteiktām robežām |
| **Mazciems** | Vēsturiski izveidojusies vieta bez noteiktām robežām |
| **Viensēta** | Savrupa dzīvojamā ēka lauku zemēs |

### 2.3 Adreses struktūra

#### Valstspilsētā:
```
[Iela] [Ēkas nr.][-][Dzīvoklis], [Pilsēta], [Pasta indekss]
→ Brīvības iela 21-5, Rīga, LV-1010
```

#### Novada pilsētā:
```
[Iela] [Ēkas nr.][-][Dzīvoklis], [Pilsēta], [Novads], [Pasta indekss]
→ Rīgas iela 15-3, Sigulda, Siguldas nov., LV-2150
```

#### Ciemā:
```
[Iela] [Ēkas nr.][-][Dzīvoklis], [Ciems], [Pagasts], [Novads], [Pasta indekss]
→ Skolas iela 5, Mālpils, Mālpils pag., Siguldas nov., LV-2152
```

#### Viensēta:
```
"[Nosaukums]", [Pagasts], [Novads], [Pasta indekss]
→ "Kalnciema", Mālpils pag., Siguldas nov., LV-2152
```

### 2.4 Adreses kods

- **Garums:** 9 cipari (100000000–999999999)
- **Unikalitāte:** katram adresācijas objektam unikāls
- **Nemainīgums:** kods paliek nemainīgs visu objekta pastāvēšanas laiku
- **Atkārtota lietošana:** likvidēti kodi netiek atkārtoti piešķirti

### 2.5 ATVK koda struktūra (7 cipari)

| Pozīcija | Apraksts | Piemērs |
|----------|----------|---------|
| 1-2 | Novada/valstspilsētas kods | 00 = Rīga |
| 3-4 | Pilsētas/pagasta kods | 01 = Rīgas pilsēta |
| 5-7 | Apakšteritoriāla vienība | 000 |

**Piemēri:** 0001000 = Rīga, 0170000 = Siguldas novads, 0170200 = Sigulda (pilsēta)

---

## 3. Datu kopu struktūra

### 3.1 Resursu pārskats — aktuālie dati

| # | Fails | Apraksts | Izmērs | Ieraksti (aptuveni) |
|---|-------|----------|--------|---------------------|
| 1 | `aw_pilseta.csv` | Pilsētas | 12 KB | ~77 |
| 2 | `aw_novads.csv` | Novadi | 22 KB | ~43 |
| 3 | `aw_pagasts.csv` | Pagasti | 84 KB | ~530 |
| 4 | `aw_ciems.csv` | Ciemi un mazciemi | 1.6 MB | ~11,000 |
| 5 | `aw_iela.csv` | Ielas | 3.2 MB | ~20,500 |
| 6 | `aw_eka.csv` | Ēkas un zemes vienības | 135 MB | ~608,000 |
| 7 | `aw_dziv.csv` | Telpu grupas (dzīvokļi) | 136 MB | ~866,000 |
| 8 | `aw_ppils.csv` | Rīgas priekšpilsētas | 3.6 MB | — |
| 9 | `aw_vietu_centroidi.csv` | Vietu centroīdi | 0.9 MB | — |
| 10 | `aw_rajons.csv` | Vēsturiskie rajoni | 4 KB | ~26 (visi DEL) |

### 3.2 Resursu pārskats — vēsturiskie dati

| # | Fails | Apraksts | Izmērs |
|---|-------|----------|--------|
| 11 | `aw_pilseta_his.csv` | Pilsētu vēsture | 17 KB |
| 12 | `aw_novads_his.csv` | Novadu vēsture | 8 KB |
| 13 | `aw_pagasts_his.csv` | Pagastu vēsture | 118 KB |
| 14 | `aw_ciems_his.csv` | Ciemu vēsture | 2.8 MB |
| 15 | `aw_iela_his.csv` | Ielu vēsture | 4.2 MB |
| 16 | `aw_eka_his.csv` | Ēku adrešu vēsture | 183 MB |
| 17 | `aw_dziv_his.csv` | Telpu grupu vēsture | 204 MB |

### 3.3 Resursu pārskats — dokumentu metadati

| # | Fails | Apraksts | Izmērs |
|---|-------|----------|--------|
| 18 | `aw_doc_nl.csv` | Ēku/zemes vienību dokumenti | 120 MB |
| 19 | `aw_doc_tg.csv` | Telpu grupu dokumenti | 89 MB |
| 20 | `aw_doc_vieta.csv` | Vietu dokumenti | 11 MB |

### 3.4 Telpiskie dati

| # | Fails | Apraksts | Izmērs |
|---|-------|----------|--------|
| 21 | `aw_shp.zip` | SHP telpiskie dati (robežas, centroīdi) | 50 MB |

**Kopējais izmērs: ~820 MB** (visi CSV + SHP faili)

### 3.5 Telpisko datu slāņi (aw_shp.zip)

**Koordinātu sistēma:** LKS-92 TM (EPSG:3059)

Visiem SHP slāņiem datumi ir `Text(19)` formātā (atšķirībā no CSV `Date(10)`). KODS ir `Long Integer(9)` (atšķirībā no CSV `String(9)`).

#### PILSETAS — Pilsētu robežas (Polygon)

| Lauks | Tips | Apraksts |
|-------|------|----------|
| `KODS` | Long Integer(9) | Adresācijas objekta kods |
| `TIPS_CD` | Long Integer(13) | Tipa kods (104) — specifikācijā norādīts (13), iespējama kļūda |
| `NOSAUKUMS` | Text(128) | Nosaukums |
| `VKUR_CD` | Long Integer(9) | Vecākobjekta kods |
| `VKUR_TIPS` | Long Integer(3) | Vecākobjekta tipa kods |
| `APSTIPR` | Text(1) | Apstiprināts (Y) |
| `APST_PAK` | Long Integer(3) | Apstiprināšanas pakāpe |
| `STATUSSS` | Text(3) | Statuss (EKS/DEL) — specifikācijā `STATUSSS`, iespējama OCR kļūda |
| `SORT_NOS` | Text(160) | Kārtošanas nosaukums |
| `DAT_SAK` | Text(19) | Izveidošanas datums |
| `DAT_MOD` | Text(19) | Modifikācijas datums |
| `DAT_BEIG` | Text(19) | Likvidācijas datums |
| `ATRIB` | Text(32) | ATVK kods |
| `STD` | Text(255) | Pilnais adreses pieraksts |

#### NOVADI — Novadu robežas (Polygon)

Tāda pati struktūra kā PILSETAS, bet: `TIPS_CD` Long Integer(3), `STATUS` Text(3).

#### PAGASTI — Pagastu robežas (Polygon)

Tāda pati struktūra kā NOVADI (STATUS Text(3)).

#### CIEMI — Ciemu robežas (Polygon)

Tāda pati struktūra kā NOVADI (STATUS Text(3)).

#### MAZCIEMI — Mazciemu centroīdi (Point)

Tāda pati struktūra kā NOVADI, bet: `STATUSS` Text(3) (ar diviem S).

#### EKAS — Ēku/zemes vienību adrešu punkti (Point)

| Lauks | Tips | Apraksts |
|-------|------|----------|
| `KODS` | Long Integer(9) | Adresācijas objekta kods |
| `TIPS_CD` | Long Integer(3) | Tipa kods (108) |
| `STATUS` | Text(3) | Statuss (EKS/DEL) |
| `APSTIPR` | Text(1) | Apstiprināts (Y) |
| `APST_PAK` | Long Integer(3) | Apstiprināšanas pakāpe |
| `VKUR_CD` | Long Integer(9) | Vecākobjekta kods |
| `VKUR_TIPS` | Long Integer(3) | Vecākobjekta tipa kods |
| `NOSAUKUMS` | Text(128) | Nosaukums |
| `SORT_NOS` | Text(160) | Kārtošanas nosaukums |
| `ATRIB` | Text(32) | Pasta indekss |
| `PNOD_CD` | Long Integer(9) | Pasta nodaļas kods |
| `DAT_SAK` | Text(19) | Izveidošanas datums |
| `DAT_MOD` | Text(19) | Modifikācijas datums |
| `DAT_BEIG` | Text(19) | Likvidācijas datums |
| `FOR_BUILD` | Text(1) | Y = zemes vienība; N = ēka |
| `PLAN_ADR` | Text(10) | Y = plānotā; N = piesaistīta |
| `STD` | Text(255) | Pilnais adreses pieraksts |

> **Piezīme:** Atšķirībā no CSV, SHP EKAS slānis NESATUR koordināšu laukus (KOORD_X, KOORD_Y, DD_E, DD_N) — koordinātes ir Shape ģeometrijā.

#### IELAS — Ielu līnijas (Polyline)

Tāda pati struktūra kā vispārīgais slānis (KODS, TIPS_CD, NOSAUKUMS, VKUR_CD, VKUR_TIPS, APSTIPR, APST_PAK, STATUS, SORT_NOS, DAT_SAK, DAT_MOD, DAT_BEIG, ATRIB). **Nav STD lauka.**

#### AUTOCELI — Autoceļu līnijas (Polyline)

Tāda pati struktūra kā IELAS. **Nav STD lauka.** TIPS_CD atsaucas uz autoceļu tipu kodiem (2. pielikums: 114-119).

#### ADM_ROB — Administratīvo teritoriju robežas (Polygon)

Minimāla shēma — tikai: `KODS`, `TIPS_CD`, `NOSAUKUMS`, `VKUR_CD`, `VKUR_TIPS`, `ATRIB`. Nav APSTIPR, APST_PAK, STATUS, SORT_NOS, datumu un STD lauku.

---

## 4. Entītiju relāciju modelis

```
┌───────────────────────────────────────────────────────────────┐
│                    VAR Objektu Hierarhija                     │
│                                                               │
│  Latvijas Republika (101)                                     │
│      KODS: 100000000                                          │
│           │                                                   │
│           ├──► Novads (113) ◄────────────────────────────┐   │
│           │        │                                      │   │
│           │        ├──► Pilsēta (104)                     │   │
│           │        │        │                             │   │
│           │        │        └──► Iela (107) ──────────┐   │   │
│           │        │                                  │   │   │
│           │        └──► Pagasts (105)                 │   │   │
│           │                 │                         │   │   │
│           │                 └──► Ciems (106)          │   │   │
│           │                        │                  │   │   │
│           │                        └──► Iela (107) ───┤   │   │
│           │                                           │   │   │
│           └──► Valstspilsēta (104) ──► Iela (107) ───┤   │   │
│                                                       ▼   │   │
│                                    Ēka/Zemes vien. (108)  │   │
│                                           │               │   │
│                                           ▼               │   │
│                                    Telpu grupa (109)      │   │
│                                                           │   │
│  Sasaistes loģika:                                        │   │
│  - VKUR_CD = vecākobjekta KODS                           │   │
│  - VKUR_TIPS = vecākobjekta TIPS_CD                      │   │
└───────────────────────────────────────────────────────────────┘
```

### 4.1 Relāciju kopsavilkums

| Saistība | Tips | Atslēga | Apraksts |
|----------|------|---------|----------|
| LR → Novads | 1:N | VKUR_CD = 100000000 | Novadi pieder valstij |
| LR → Valstspilsēta | 1:N | VKUR_CD = 100000000 | Valstspilsētas pieder valstij |
| Novads → Pilsēta | 1:N | VKUR_CD = novada KODS | Pilsētas novadā |
| Novads → Pagasts | 1:N | VKUR_CD = novada KODS | Pagasti novadā |
| Pagasts → Ciems | 1:N | VKUR_CD = pagasta KODS | Ciemi pagastā |
| Pilsēta → Ciems | 1:N | VKUR_CD = pilsētas KODS | Ciemi pilsētā |
| Pilsēta → Iela | 1:N | VKUR_CD = pilsētas KODS | Ielas pilsētā |
| Ciems → Iela | 1:N | VKUR_CD = ciema KODS | Ielas ciemā |
| Iela → Ēka | 1:N | VKUR_CD = ielas KODS | Ēkas uz ielas |
| Ciems/Pagasts → Ēka | 1:N | VKUR_CD = ciema/pagasta KODS | Ēkas bez ielas (viensētas) |
| Ēka → Telpu grupa | 1:N | VKUR_CD = ēkas KODS | Dzīvokļi ēkā |

### 4.2 VKUR (vecākobjekta) mehānisms

Visi VAR objekti izmanto vienotu hierarhijas mehānismu:
- `VKUR_CD` — vecākobjekta kods (9 cipari)
- `VKUR_TIPS` — vecākobjekta tipa kods

Šis mehānisms ļauj rekonstruēt pilnu adreses hierarhiju no jebkura objekta līdz valstij.

---

## 5. Detalizētas shēmas pa resursiem

### 5.1 AW_PILSETA.CSV — Pilsētas

| Lauks | Tips | Apraksts |
|-------|------|----------|
| `KODS` | String(9) | **PK** — Adresācijas objekta kods |
| `TIPS_CD` | String(3) | Objekta tipa kods (104 = pilsēta) |
| `NOSAUKUMS` | String(20) | Pilsētas nosaukums |
| `VKUR_CD` | String(9) | Vecākobjekta kods (novads vai LR) |
| `VKUR_TIPS` | String(3) | Vecākobjekta tipa kods |
| `APSTIPR` | String(1) | "Y" = apstiprināts |
| `APST_PAK` | String(3) | Apstiprināšanas pakāpes kods (skatīt 6.2) |
| `STATUSS` | String(3) | EKS/DEL/ERR (skatīt 6.3) |
| `SORT_NOS` | String(22) | Kārtošanas nosaukums |
| `DAT_SAK` | Date(10) | Izveidošanas datums (yyyy.mm.dd) |
| `DAT_MOD` | Date(10) | Modifikācijas datums |
| `DAT_BEIG` | Date(10) | Likvidācijas datums (tukšs = aktīvs) |
| `ATRIB` | String(7) | ATVK kods |
| `STD` | String(29) | Pilnais adreses pieraksts |

> **Piezīme:** Teksta datu specifikācijas tabula ir nocirsta lappuses pārtraukumā — lauki DAT_BEIG, ATRIB, STD nav parādīti. Vērtības šeit secintas no analoģiskām tabulām un reālajiem datiem.

**Piezīme par STATUSS/STATUS:** Telpisko datu specifikācija uzrāda `STATUS` (viens S) dažiem slāņiem (NOVADI, PAGASTI, CIEMI, EKAS, IELAS, AUTOCELI) un `STATUSSS` (trīs S — iespējama OCR kļūda) PILSETAS slānim, bet `STATUSS` MAZCIEMI slānim. Teksta datu specifikācija līdzīgi uzrāda `STATUS` (AW_PILSETA, AW_NOVADS, AW_RAJONS) un `STATUSS` (AW_CIEMS, AW_EKA, AW_DZIV). Reālajos CSV un SHP failos lauka nosaukums var atšķirties — ieteicams pārbaudīt faktisko galveni.

### 5.2 AW_NOVADS.CSV — Novadi

Tāda pati struktūra kā AW_PILSETA, bet `TIPS_CD = 113`.

| Lauks | Tips | Apraksts |
|-------|------|----------|
| `KODS` | String(9) | **PK** — Novada kods |
| `TIPS_CD` | String(3) | 113 = novads |
| `NOSAUKUMS` | String(20) | Novada nosaukums |
| `VKUR_CD` | String(9) | 100000000 = LR |
| `VKUR_TIPS` | String(3) | 101 = LR |
| `APSTIPR` | String(1) | "Y" |
| `APST_PAK` | String(3) | Apstiprināšanas pakāpe |
| `STATUSS` | String(3) | EKS/DEL/ERR |
| `SORT_NOS` | String(22) | Kārtošanas nosaukums |
| `DAT_SAK` | Date(10) | Izveidošanas datums |
| `DAT_MOD` | Date(10) | Modifikācijas datums |
| `DAT_BEIG` | Date(10) | Likvidācijas datums |
| `ATRIB` | String(7) | ATVK kods |
| `STD` | String(29) | Pilnais pieraksts |

### 5.3 AW_PAGASTS.CSV — Pagasti

| Lauks | Tips | Apraksts |
|-------|------|----------|
| `KODS` | String(9) | **PK** — Pagasta kods |
| `TIPS_CD` | String(3) | 105 = pagasts |
| `NOSAUKUMS` | String(19) | Pagasta nosaukums |
| `VKUR_CD` | String(9) | **FK** → Novada KODS |
| `VKUR_TIPS` | String(3) | 113 = novads |
| `APSTIPR` | String(1) | "Y" |
| `APST_PAK` | String(3) | Apstiprināšanas pakāpe |
| `STATUSS` | String(3) | EKS/DEL/ERR |
| `SORT_NOS` | String(22) | Kārtošanas nosaukums |
| `DAT_SAK` | Date(10) | Izveidošanas datums |
| `DAT_MOD` | Date(10) | Modifikācijas datums |
| `DAT_BEIG` | Date(10) | Likvidācijas datums |
| `ATRIB` | String(7) | ATVK kods |
| `STD` | String(36) | Pilnais pieraksts |

### 5.4 AW_CIEMS.CSV — Ciemi un mazciemi

| Lauks | Tips | Apraksts |
|-------|------|----------|
| `KODS` | String(9) | **PK** — Ciema kods |
| `TIPS_CD` | String(3) | 106 = ciems/mazciems |
| `NOSAUKUMS` | String(29) | Ciema nosaukums |
| `VKUR_CD` | String(9) | **FK** → Pagasta vai pilsētas KODS |
| `VKUR_TIPS` | String(3) | 105 = pagasts vai 104 = pilsēta |
| `APSTIPR` | String(1) | "Y" |
| `APST_PAK` | String(3) | Apstiprināšanas pakāpe |
| `STATUSS` | String(3) | EKS/DEL/ERR |
| `SORT_NOS` | String(29) | Kārtošanas nosaukums |
| `DAT_SAK` | Date(10) | Izveidošanas datums |
| `DAT_MOD` | Date(10) | Modifikācijas datums |
| `DAT_BEIG` | Date(10) | Likvidācijas datums |
| `ATRIB` | String(1) | "1" = mazciems (bez robežas) |
| `STD` | String(60) | Pilnais pieraksts |

### 5.5 AW_IELA.CSV — Ielas

| Lauks | Tips | Apraksts |
|-------|------|----------|
| `KODS` | String(9) | **PK** — Ielas kods |
| `TIPS_CD` | String(3) | 107 = iela |
| `NOSAUKUMS` | String(35) | Ielas nosaukums |
| `VKUR_CD` | String(9) | **FK** → Ciema vai pilsētas KODS |
| `VKUR_TIPS` | String(3) | 106 = ciems vai 104 = pilsēta |
| `APSTIPR` | String(1) | "Y" |
| `APST_PAK` | String(3) | Apstiprināšanas pakāpe |
| `STATUSS` | String(3) | EKS/DEL/ERR |
| `SORT_NOS` | String(35) | Kārtošanas nosaukums |
| `DAT_SAK` | Date(10) | Izveidošanas datums |
| `DAT_MOD` | Date(10) | Modifikācijas datums |
| `DAT_BEIG` | Date(10) | Likvidācijas datums |
| `ATRIB` | String(32) | Netiek aizpildīts |
| `STD` | String(80) | Pilnais pieraksts |

> **Piezīme:** STD izmērs String(80) ir novērtējums, kas balstīts uz reālajiem datiem, nevis oficiālo specifikāciju (kurai šī entītija ir ar saīsinātu tabulu). Vēsturiskais fails AW_IELA_HIS uzrāda String(92), kas norāda, ka pašreizējie dati var būt lielāki.

### 5.6 AW_EKA.CSV — Ēkas un apbūvei paredzētās zemes vienības

**Lielākais un svarīgākais fails (~608,000 ieraksti).**

| Lauks | Tips | Apraksts |
|-------|------|----------|
| `KODS` | String(9) | **PK** — Adresācijas objekta kods |
| `TIPS_CD` | String(3) | 108 = ēka/zemes vienība |
| `STATUSS` | String(3) | EKS/DEL/ERR |
| `APSTIPR` | String(1) | "Y" |
| `APST_PAK` | String(3) | Apstiprināšanas pakāpe |
| `VKUR_CD` | String(9) | **FK** → Ielas vai ciema/pagasta KODS |
| `VKUR_TIPS` | String(3) | 107/106/105/104 |
| `NOSAUKUMS` | String(55) | Mājas numurs/nosaukums |
| `SORT_NOS` | String(55) | Kārtošanas nosaukums |
| `ATRIB` | String(7) | Pasta indekss (LV-XXXX) |
| `PNOD_CD` | String(9) | Pasta nodaļas apkalpes teritorijas kods |
| `DAT_SAK` | Date(10) | Izveidošanas datums |
| `DAT_MOD` | Date(10) | Modifikācijas datums |
| `DAT_BEIG` | Date(10) | Likvidācijas datums |
| `FOR_BUILD` | String(1) | "Y" = apbūvei paredzēta zemes vienība; "N" = ēka |
| `PLAN_ADR` | String(10) | "Y" = plānotā adrese; "N" = piesaistīta NĪVKIS |
| `STD` | String(103) | Pilnais adreses pieraksts |
| `KOORD_X` | Double(10) | Centroīda X koordināte (LKS-92) |
| `KOORD_Y` | Double(10) | Centroīda Y koordināte (LKS-92) |
| `DD_E` | Double(9) | Garuma grādi (WGS84 longitude) |
| `DD_N` | Double(9) | Platuma grādi (WGS84 latitude) |

### 5.7 AW_DZIV.CSV — Telpu grupas (dzīvokļi)

**Otrais lielākais fails (~866,000 ieraksti).**

| Lauks | Tips | Apraksts |
|-------|------|----------|
| `KODS` | String(9) | **PK** — Adresācijas objekta kods |
| `TIPS_CD` | String(3) | 109 = telpu grupa |
| `STATUSS` | String(3) | EKS/DEL/ERR |
| `APSTIPR` | String(1) | "Y" |
| `APST_PAK` | String(3) | Apstiprināšanas pakāpe |
| `VKUR_CD` | String(9) | **FK** → Ēkas KODS (AW_EKA) |
| `VKUR_TIPS` | String(3) | 108 = ēka |
| `NOSAUKUMS` | String(8) | Telpu grupas numurs |
| `SORT_NOS` | String(17) | Kārtošanas numurs (ar nullēm) |
| `ATRIB` | String(0) | Netiek aizpildīts |
| `DAT_SAK` | Date(10) | Izveidošanas datums |
| `DAT_MOD` | Date(10) | Modifikācijas datums |
| `DAT_BEIG` | Date(10) | Likvidācijas datums |
| `STD` | String(95) | Pilnais adreses pieraksts |

> **Piezīme:** STD izmērs String(95) ir novērtējums, kas balstīts uz reālajiem datiem, nevis oficiālo specifikāciju (kurai šī entītija ir ar saīsinātu tabulu). Vēsturiskais fails AW_DZIV_HIS uzrāda String(103), kas norāda, ka pašreizējie dati var būt lielāki.

### 5.8 AW_VIETA_CENTROIDI.CSV — Vietu centroīdi

| Lauks | Tips | Apraksts |
|-------|------|----------|
| `KODS` | String(9) | Adresācijas objekta kods |
| `TIPS_CD` | String(3) | Objekta tipa kods |
| `NOSAUKUMS` | String(22) | Objekta nosaukums |
| `VKUR_CD` | String(9) | Vecākobjekta kods |
| `VKUR_TIPS` | String(3) | Vecākobjekta tipa kods |
| `STD` | String(54) | Pilnais pieraksts |
| `KOORD_X` | Double(10) | X (LKS-92) |
| `KOORD_Y` | Double(10) | Y (LKS-92) |
| `DD_E` | Double(9) | Garuma grādi (WGS84) |
| `DD_N` | Double(9) | Platuma grādi (WGS84) |

### 5.9 AW_PPILS.CSV — Rīgas priekšpilsētas

| Lauks | Tips | Apraksts |
|-------|------|----------|
| `KODS` | String(9) | Ēkas adresācijas objekta kods (FK → AW_EKA) |
| `PPILS` | String(32) | Priekšpilsētas nosaukums |
| `PPILS_CD` | String(9) | Priekšpilsētas kods |
| `DAT_SAK` | Date(10) | Sākuma datums |
| `DAT_MOD` | Date(10) | Modifikācijas datums |
| `DAT_BEIG` | Date(10) | Beigu datums |

### 5.10 AW_RAJONS.CSV — Vēsturiskie rajoni

**Visi ieraksti ar statusu DEL (likvidēti 2009. gada administratīvi teritoriālajā reformā).**

| Lauks | Tips | Apraksts |
|-------|------|----------|
| `KODS` | String(9) | **PK** — Rajona kods |
| `TIPS_CD` | String(3) | 102 = rajons |
| `NOSAUKUMS` | String(16) | Rajona nosaukums |
| `VKUR_CD` | String(9) | 100000000 = LR |
| `VKUR_TIPS` | String(3) | 101 = LR |
| `APSTIPR` | String(1) | Apstiprināts |
| `APST_PAK` | String(3) | Apstiprināšanas pakāpe |
| `STATUSS` | String(3) | DEL (visi likvidēti) |
| `SORT_NOS` | String(18) | Kārtošanas nosaukums |
| `DAT_SAK` | Date(10) | Izveidošanas datums |
| `DAT_MOD` | Date(10) | Modifikācijas datums |
| `DAT_BEIG` | Date(10) | Likvidācijas datums |
| `ATRIB` | String(6-7) | ATVK kods (specifikācija norāda String(6), bet apraksta kā 'septiņas zīmes' — pretruna specifikācijā) |

### 5.11 Dokumentu metadatu faili (AW_DOC_NL, AW_DOC_TG, AW_DOC_VIETA)

Vienota struktūra visiem trim failiem:

| Lauks | Tips | Apraksts |
|-------|------|----------|
| `ADRESES_KODS` | String(9) | Adresācijas objekta kods |
| `ADRESES_VEIDS` | String(2)/String(5) | "NL" (AW_DOC_NL), "TG" (AW_DOC_TG) = String(2); "VIETA" (AW_DOC_VIETA) = String(5) |
| `AUTORS` | String(128) | Dokumenta autors |
| `DATUMS` | Date(10) | Dokumenta datums |
| `VEIDS` | String(35) | Dokumenta veids |
| `NUMURS` | String(35) | Dokumenta numurs |
| `NOSAUKUMS` | String(512) | Dokumenta nosaukums |

### 5.12 Vēsturisko failu struktūra (kopīgie lauki)

| Lauks | Tips | Apraksts |
|-------|------|----------|
| `KODS` | String(9) | Adresācijas objekta kods |
| `TIPS_CD` | String(3) | Objekta tipa kods |
| `DAT_SAK` | Date(10) | Ieraksta sākuma datums |
| `DAT_MOD` | Date(10) | Modifikācijas datums |
| `DAT_BEIG` | Date(10) | Ieraksta beigu datums |
| `STD` | String (skatīt zemāk) | Vēsturiskais pilnais pieraksts |
| `NOSAUKUMS` | String (skatīt zemāk) | Vēsturiskais nosaukums |
| `VKUR_CD` | String(9) | Vēsturiskais vecākobjekta kods |
| `VKUR_TIPS` | String(3) | Vēsturiskais vecākobjekta tips |

**STD un NOSAUKUMS izmēri pa failiem:**

| Fails | STD izmērs | NOSAUKUMS izmērs |
|-------|------------|-----------------|
| AW_PILSETA_HIS | String(48) | String(12) |
| AW_NOVADS_HIS | String(36) | String(18) |
| AW_PAGASTS_HIS | String(58) | String(29) |
| AW_CIEMS_HIS | String(75) | String(32) |
| AW_IELA_HIS | String(92) | String(35) |
| AW_EKA_HIS | String(116) | String(64) |
| AW_DZIV_HIS | String(103) | String(11) |

**AW_EKA_HIS.CSV papildus lauks:** `KODS_HIS` — vēsturiskais saistītais kods.

---

## 6. Klasifikatori

### 6.1 Adresācijas objektu tipi (TIPS_CD, VKUR_TIPS)

| Kods | Objekta tips |
|------|--------------|
| 101 | Latvijas Republika |
| 102 | Rajons (vēsturisks, visi DEL) |
| 103 | Apriņķis (vēsturisks) |
| 104 | Pilsēta |
| 105 | Pagasts |
| 106 | Ciems/mazciems |
| 107 | Iela |
| 108 | Ēka, apbūvei paredzēta zemes vienība |
| 109 | Telpu grupa |
| 113 | Novads |

**Autoceļu tipu kodi (SHP AUTOCELI slānis):**

| Kods | Objekta tips |
|------|--------------|
| 114 | Valsts galvenais autoceļš |
| 115 | Valsts reģionālais autoceļš |
| 116 | Valsts vietējais autoceļš |
| 117 | Pašvaldības ceļš |
| 118 | Uzņēmuma ceļš |
| 119 | Mājas ceļš |

> Kodi 114–119 izmantoti tikai telpisko datu (SHP) slāņos.

### 6.2 Apstiprināšanas pakāpes (APST_PAK)

| Kods | Apraksts |
|------|----------|
| 251 | Kļūdains apstiprinājums |
| 252 | Oficiāls (uz dokumenta pamata) |
| 253 | Daļējs (bez juridiskā statusa dokumenta) |
| 254 | Saņemts no citām sistēmām (nepārbaudīts) |

### 6.3 Statusi (STATUSS)

| Kods | Apraksts |
|------|----------|
| EKS | Eksistējošs (aktīvs) |
| DEL | Likvidēts |
| ERR | Kļūdains ieraksts |

### 6.4 STD lauka struktūra

| Objekta tips | STD formāts | Piemērs |
|--------------|-------------|---------|
| Novads | `{nosaukums} nov.` | `Siguldas nov.` |
| Pilsēta | `{nosaukums}` vai `{nosaukums}, {novads}` | `Rīga` vai `Sigulda, Siguldas nov.` |
| Pagasts | `{nosaukums} pag., {novads}` | `Mālpils pag., Siguldas nov.` |
| Ciems | `{nosaukums}, {pagasts}, {novads}` | `Mālpils, Mālpils pag., Siguldas nov.` |
| Iela | `{nosaukums}, {pilsēta/ciems}, ...` | `Brīvības iela, Rīga` |
| Ēka | `{iela} {numurs}, {vieta}, {indekss}` | `Brīvības iela 21, Rīga, LV-1010` |
| Telpu grupa | `{iela} {numurs} - {dz.}, {vieta}, {indekss}` | `Brīvības iela 21 - 5, Rīga, LV-1010` |

---

## 7. Sasaiste ar NĪVKIS

### 7.1 Sasaistes atslēgas

| VAR lauks | NĪVKIS elements | Apraksts |
|-----------|-----------------|----------|
| `KODS` (AW_EKA) | `ARCode` (Address) | Ēkas adreses sasaiste |
| `KODS` (AW_DZIV) | `ARCode` (Address) | Telpu grupas adreses sasaiste |
| `KODS` (AW_EKA) | `VARISCode` (Building) | Tieša būves sasaiste |
| `KODS` (AW_EKA) | `ParcelVARISCode` (Parcel) | Tieša zemes vienības sasaiste |
| `KODS` (AW_DZIV) | `PremiseGroupVARISCode` (PremiseGroup) | Tieša telpu grupas sasaiste |

### 7.2 Piemērs: No kadastra numura uz pilnu adresi

```sql
-- 1. Atrast VARISCode no NĪVKIS Building datiem
SELECT varis_code FROM buildings WHERE cadastre_nr = '01001240238001';
-- Rezultāts: 101234567

-- 2. Atrast pilnu adresi VAR
SELECT STD, DD_N, DD_E FROM aw_eka WHERE KODS = '101234567' AND STATUSS = 'EKS';
-- Rezultāts: "Brīvības iela 21, Rīga, LV-1010", 56.987654, 24.123456
```

---

## 8. Lietošanas scenāriji

### 8.1 Atrast adresi pēc teksta

```sql
-- Meklēt "Brīvības 21, Rīga"
SELECT KODS, STD, DD_N, DD_E FROM aw_eka
WHERE STD LIKE '%Brīvības%21%Rīga%' AND STATUSS = 'EKS';
```

### 8.2 Atrast visus dzīvokļus ēkā

```sql
SELECT KODS, NOSAUKUMS, STD FROM aw_dziv
WHERE VKUR_CD = '101234567' AND STATUSS = 'EKS'
ORDER BY CAST(NOSAUKUMS AS INTEGER);
```

### 8.3 Iegūt pilnu adreses hierarhiju

```sql
SELECT
  eka.STD as adrese,
  eka.KODS as eka_kods,
  iela.NOSAUKUMS as iela,
  ciems.NOSAUKUMS as ciems,
  pagasts.NOSAUKUMS as pagasts,
  novads.NOSAUKUMS as novads
FROM aw_eka eka
LEFT JOIN aw_iela iela ON eka.VKUR_CD = iela.KODS
LEFT JOIN aw_ciems ciems ON iela.VKUR_CD = ciems.KODS OR eka.VKUR_CD = ciems.KODS
LEFT JOIN aw_pagasts pagasts ON ciems.VKUR_CD = pagasts.KODS
LEFT JOIN aw_novads novads ON pagasts.VKUR_CD = novads.KODS
WHERE eka.KODS = '101234567';
```

### 8.4 Visas ēkas noteiktā teritorijā (novadā)

```sql
SELECT e.KODS, e.STD FROM aw_eka e
WHERE e.STATUSS = 'EKS'
  AND EXISTS (
    SELECT 1 FROM aw_iela i
    JOIN aw_pilseta p ON i.VKUR_CD = p.KODS
    WHERE e.VKUR_CD = i.KODS AND p.VKUR_CD = '105375636'
  );
```

### 8.5 Atšķirt ēku no zemes vienības

```sql
-- FOR_BUILD = 'N' → ēka
-- FOR_BUILD = 'Y' → apbūvei paredzēta zemes vienība
SELECT KODS, STD, FOR_BUILD FROM aw_eka
WHERE FOR_BUILD = 'N' AND STATUSS = 'EKS' LIMIT 10;
```

---

## 9. Tehniskie norādījumi

### 9.1 CSV failu raksturojums

| Parametrs | Vērtība |
|-----------|---------|
| **Kodējums** | UTF-8 BOM |
| **Atdalītājs** | Komats (,) |
| **Teksta kvalifikators** | Pēdiņas (") |
| **Rindu beigas** | LF vai CRLF |
| **Pirmā rinda** | Lauku nosaukumi |
| **Datumu formāts** | `yyyy.mm.dd` |
| **BOM problēma** | Pirmās kolonnas nosaukumā var būt BOM prefikss `﻿` |

### 9.2 BOM noņemšana (Python)

```python
import csv
with open('aw_eka.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Lauku nosaukumi automātiski notīrīti ar utf-8-sig
        pass
```

### 9.3 SORT_NOS lauka loģika

| Oriģināls | SORT_NOS | Skaidrojums |
|-----------|----------|-------------|
| "5" | "0005" | 4 ciparu formāts (ēkas) |
| "5A" | "0005A" | Burts saglabāts |
| "12" | "00012" | 5 ciparu formāts (dzīvokļi) |
| "Brīvības iela" | "Brīvības iela" | Teksts nemainīts |

### 9.4 Koordinātu sistēmas

| Lauki | Sistēma | Apraksts |
|-------|---------|----------|
| `KOORD_X`, `KOORD_Y` | LKS-92 | Latvijas koordinātu sistēma (metri) |
| `DD_E`, `DD_N` | WGS84 | Decimālgrādi (lat/lon) |

### 9.5 Tukša DAT_BEIG interpretācija

Ja `DAT_BEIG` ir tukšs — objekts joprojām eksistē. Aizpildīts `DAT_BEIG` norāda likvidācijas datumu.

### 9.6 Datu piemēri

**AW_EKA.CSV:**
```csv
KODS,TIPS_CD,STATUSS,APSTIPR,APST_PAK,VKUR_CD,VKUR_TIPS,NOSAUKUMS,SORT_NOS,ATRIB,PNOD_CD,DAT_SAK,DAT_MOD,DAT_BEIG,FOR_BUILD,PLAN_ADR,STD,KOORD_X,KOORD_Y,DD_E,DD_N
100123456,108,EKS,Y,252,100065432,107,21,0021,LV-1010,100500001,1992.01.01,2024.03.20,,N,N,"Brīvības iela 21, Rīga, LV-1010",506789.12,312456.78,24.123456,56.987654
```

**AW_DZIV.CSV:**
```csv
KODS,TIPS_CD,STATUSS,APSTIPR,APST_PAK,VKUR_CD,VKUR_TIPS,NOSAUKUMS,SORT_NOS,ATRIB,DAT_SAK,DAT_MOD,DAT_BEIG,STD
100123457,109,EKS,Y,252,100123456,108,5,00005,,1992.01.01,2024.03.20,,"Brīvības iela 21 - 5, Rīga, LV-1010"
```

### 9.7 INSPIRE datu servisi

VZD nodrošina INSPIRE lejupielādes servisus (WFS) adrešu un administratīvo vienību datiem:

**WFS servisu URL:**

| Serviss | Tēma | URL |
|---------|------|-----|
| Adreses (AD) | Address | `https://grafws.kadastrs.lv/gateway/gateto/GEOPRODUKTS-WFS-INSPIRE-AD-cfc607ca-a5d8-4178-83e1-a176ea835d64` |
| Administratīvās vienības (AU) | AdministrativeUnit | `https://grafws.kadastrs.lv/gateway/gateto/GEOPRODUKTS-WFS-INSPIRE-AU-4cd9484d-8350-45e8-b819-ba87aaf97604` |
| Administratīvās robežas (AUB) | AdministrativeBoundary | `https://grafws.kadastrs.lv/gateway/gateto/GEOPRODUKTS-WFS-INSPIRE-AUB-579546ba-af84-4e7c-bfb0-1fd9aeae0b29` |
| Administratīvo teritoriju centri (AUR) | — | `https://grafws.kadastrs.lv/gateway/gateto/GEOPRODUKTS-WFS-INSPIRE-AUR-8b83e5a0-2480-4134-ba8e-1870e6ac524e` |

**Nacionālā līmeņa atbilstība:**

| VARIS slānis | NATIONALLEVELNAME | NATIONALLEVEL |
|--------------|-------------------|---------------|
| AR.ARCountry | Latvijas Republika | 1st Order |
| AR.ARDistrict | Novads | 2nd Order |
| AR.ARParish | Pagasts | 3rd Order |
| AR.ARCity | Pilsēta | 2nd Order (ja Republikas pilsēta) / 3rd Order (ja novada pilsēta) |

**INSPIRE datu tabulas:**
- **adComponent** — adreses komponentes (VARIS kods, pasta indekss, nosaukums)
- **adAddress** — adreses objekti (statuss, derīgums, ģeometrija)
- **adAddress_position** — adreses ģeogrāfiskā pozīcija
- **adAddress_locator** / **adAddress_locator_designator** — adreses apzīmējums
- **auAdmUnitS** — administratīvās vienības (poligoni, ATVK kods, līmenis)
- **auAdmBoundaryL** — administratīvās robežas (līnijas)

Pilna INSPIRE datu kartēšana: `docs/specs/VAR_INSPIRE_specifikacija.md`

---

## 10. CKAN API pieejas punkti

### 10.1 Datu kopas metadati

```
GET https://data.gov.lv/dati/api/3/action/package_show?id=varis-atvertie-dati
```

**Svarīgi:** Vecais dataset ID `valsts-adresu-registra-informacijas-sistemas-atvertie-dati` atgriež 403 kļūdu. Lietot `varis-atvertie-dati`.

### 10.2 Organizācijas informācija

```
GET https://data.gov.lv/dati/api/3/action/organization_show?id=valsts-zemes-dienests
```

---

## 11. Datu lejupielādes URL saraksts

**Bāzes URL:** `https://data.gov.lv/dati/dataset/6b06a7e8-dedf-4705-a47b-2a7c51177473/resource/`

### 11.1 Aktuālie dati

| # | Fails | Izmērs | Resource ID | URL |
|---|-------|--------|-------------|-----|
| 1 | `aw_pilseta.csv` | 12 KB | `ee02baa4-2bc3-4f77-a6cb-5427a3e9befe` | `https://data.gov.lv/dati/dataset/6b06a7e8-dedf-4705-a47b-2a7c51177473/resource/ee02baa4-2bc3-4f77-a6cb-5427a3e9befe/download/aw_pilseta.csv` |
| 2 | `aw_novads.csv` | 22 KB | `c62c60bb-58d4-4f26-82c0-5b630769f9d1` | `https://data.gov.lv/dati/dataset/6b06a7e8-dedf-4705-a47b-2a7c51177473/resource/c62c60bb-58d4-4f26-82c0-5b630769f9d1/download/aw_novads.csv` |
| 3 | `aw_pagasts.csv` | 84 KB | `6ba8c905-27a1-443a-b9c6-256a0777425b` | `https://data.gov.lv/dati/dataset/6b06a7e8-dedf-4705-a47b-2a7c51177473/resource/6ba8c905-27a1-443a-b9c6-256a0777425b/download/aw_pagasts.csv` |
| 4 | `aw_ciems.csv` | 1.6 MB | `0d3810f4-1ac0-4fba-8b10-0188084a361b` | `https://data.gov.lv/dati/dataset/6b06a7e8-dedf-4705-a47b-2a7c51177473/resource/0d3810f4-1ac0-4fba-8b10-0188084a361b/download/aw_ciems.csv` |
| 5 | `aw_iela.csv` | 3.2 MB | `3c4ab802-76cf-433c-9c1c-89215e28d833` | `https://data.gov.lv/dati/dataset/6b06a7e8-dedf-4705-a47b-2a7c51177473/resource/3c4ab802-76cf-433c-9c1c-89215e28d833/download/aw_iela.csv` |
| 6 | `aw_eka.csv` | 135 MB | `a510737a-18ce-400f-ad4b-04fce5228272` | `https://data.gov.lv/dati/dataset/6b06a7e8-dedf-4705-a47b-2a7c51177473/resource/a510737a-18ce-400f-ad4b-04fce5228272/download/aw_eka.csv` |
| 7 | `aw_dziv.csv` | 136 MB | `b83be373-f444-4f50-9b98-28741845325e` | `https://data.gov.lv/dati/dataset/6b06a7e8-dedf-4705-a47b-2a7c51177473/resource/b83be373-f444-4f50-9b98-28741845325e/download/aw_dziv.csv` |
| 8 | `aw_ppils.csv` | 3.6 MB | `21856ec7-8592-40d6-9e65-b23117348c98` | `https://data.gov.lv/dati/dataset/6b06a7e8-dedf-4705-a47b-2a7c51177473/resource/21856ec7-8592-40d6-9e65-b23117348c98/download/aw_ppils.csv` |
| 9 | `aw_vietu_centroidi.csv` | 0.9 MB | `68f1152c-0f4c-4fc3-abb3-df4b8bfea992` | `https://data.gov.lv/dati/dataset/6b06a7e8-dedf-4705-a47b-2a7c51177473/resource/68f1152c-0f4c-4fc3-abb3-df4b8bfea992/download/aw_vietu_centroidi.csv` |
| 10 | `aw_rajons.csv` | 4 KB | `e7f17c92-fad4-4153-bef5-670a321c4ec1` | `https://data.gov.lv/dati/dataset/6b06a7e8-dedf-4705-a47b-2a7c51177473/resource/e7f17c92-fad4-4153-bef5-670a321c4ec1/download/aw_rajons.csv` |

### 11.2 Vēsturiskie dati

| # | Fails | Izmērs | Resource ID | URL |
|---|-------|--------|-------------|-----|
| 11 | `aw_pilseta_his.csv` | 17 KB | `87e2c4e5-13d9-4142-9052-8a6e9f094479` | `https://data.gov.lv/dati/dataset/6b06a7e8-dedf-4705-a47b-2a7c51177473/resource/87e2c4e5-13d9-4142-9052-8a6e9f094479/download/aw_pilseta_his.csv` |
| 12 | `aw_novads_his.csv` | 8 KB | `c5c3d570-1596-49f2-a486-53439b449641` | `https://data.gov.lv/dati/dataset/6b06a7e8-dedf-4705-a47b-2a7c51177473/resource/c5c3d570-1596-49f2-a486-53439b449641/download/aw_novads_his.csv` |
| 13 | `aw_pagasts_his.csv` | 118 KB | `5950bf88-4441-470f-9e13-efcbd79bc1f0` | `https://data.gov.lv/dati/dataset/6b06a7e8-dedf-4705-a47b-2a7c51177473/resource/5950bf88-4441-470f-9e13-efcbd79bc1f0/download/aw_pagasts_his.csv` |
| 14 | `aw_ciems_his.csv` | 2.8 MB | `c8f34472-8ca4-40d5-9c84-05b24dc19afe` | `https://data.gov.lv/dati/dataset/6b06a7e8-dedf-4705-a47b-2a7c51177473/resource/c8f34472-8ca4-40d5-9c84-05b24dc19afe/download/aw_ciems_his.csv` |
| 15 | `aw_iela_his.csv` | 4.2 MB | `a7461a4e-4407-4506-9333-a50c4f51b328` | `https://data.gov.lv/dati/dataset/6b06a7e8-dedf-4705-a47b-2a7c51177473/resource/a7461a4e-4407-4506-9333-a50c4f51b328/download/aw_iela_his.csv` |
| 16 | `aw_eka_his.csv` | 183 MB | `d07443d7-15a8-4db6-9e53-7a68eec3c0dd` | `https://data.gov.lv/dati/dataset/6b06a7e8-dedf-4705-a47b-2a7c51177473/resource/d07443d7-15a8-4db6-9e53-7a68eec3c0dd/download/aw_eka_his.csv` |
| 17 | `aw_dziv_his.csv` | 204 MB | `26e63e84-c04d-40b5-9c37-0ca9d08789ad` | `https://data.gov.lv/dati/dataset/6b06a7e8-dedf-4705-a47b-2a7c51177473/resource/26e63e84-c04d-40b5-9c37-0ca9d08789ad/download/aw_dziv_his.csv` |

### 11.3 Dokumentu metadati

| # | Fails | Izmērs | Resource ID | URL |
|---|-------|--------|-------------|-----|
| 18 | `aw_doc_nl.csv` | 120 MB | `7d98b01c-60d3-46e6-8583-320a83301174` | `https://data.gov.lv/dati/dataset/6b06a7e8-dedf-4705-a47b-2a7c51177473/resource/7d98b01c-60d3-46e6-8583-320a83301174/download/aw_doc_nl.csv` |
| 19 | `aw_doc_tg.csv` | 89 MB | `b1552dfe-605f-4260-9602-e5e6886bb754` | `https://data.gov.lv/dati/dataset/6b06a7e8-dedf-4705-a47b-2a7c51177473/resource/b1552dfe-605f-4260-9602-e5e6886bb754/download/aw_doc_tg.csv` |
| 20 | `aw_doc_vieta.csv` | 11 MB | `2dbe69b1-6b14-4f35-98b8-2a64119af163` | `https://data.gov.lv/dati/dataset/6b06a7e8-dedf-4705-a47b-2a7c51177473/resource/2dbe69b1-6b14-4f35-98b8-2a64119af163/download/aw_doc_vieta.csv` |

### 11.4 Telpiskie dati

| # | Fails | Izmērs | Resource ID | URL |
|---|-------|--------|-------------|-----|
| 21 | `aw_shp.zip` | 50 MB | `b643b1b3-223f-4394-9beb-18524f8b0b82` | `https://data.gov.lv/dati/dataset/6b06a7e8-dedf-4705-a47b-2a7c51177473/resource/b643b1b3-223f-4394-9beb-18524f8b0b82/download/aw_shp.zip` |

---

## 12. Datu normalizācijas ieteikumi

### 12.1 SQLite datubāzes shēma

```sql
-- ============================================================
-- Novadi
-- ============================================================
CREATE TABLE aw_novads (
    kods            TEXT PRIMARY KEY,
    tips_cd         TEXT,
    nosaukums       TEXT,
    vkur_cd         TEXT,
    vkur_tips       TEXT,
    apstipr         TEXT,
    apst_pak        TEXT,
    statuss         TEXT,
    sort_nos        TEXT,
    dat_sak         TEXT,
    dat_mod         TEXT,
    dat_beig        TEXT,
    atrib           TEXT,  -- ATVK kods
    std             TEXT
);
CREATE INDEX idx_novads_statuss ON aw_novads(statuss);

-- ============================================================
-- Pilsētas
-- ============================================================
CREATE TABLE aw_pilseta (
    kods            TEXT PRIMARY KEY,
    tips_cd         TEXT,
    nosaukums       TEXT,
    vkur_cd         TEXT,
    vkur_tips       TEXT,
    apstipr         TEXT,
    apst_pak        TEXT,
    statuss         TEXT,
    sort_nos        TEXT,
    dat_sak         TEXT,
    dat_mod         TEXT,
    dat_beig        TEXT,
    atrib           TEXT,
    std             TEXT
);
CREATE INDEX idx_pilseta_vkur ON aw_pilseta(vkur_cd);
CREATE INDEX idx_pilseta_statuss ON aw_pilseta(statuss);

-- ============================================================
-- Pagasti
-- ============================================================
CREATE TABLE aw_pagasts (
    kods            TEXT PRIMARY KEY,
    tips_cd         TEXT,
    nosaukums       TEXT,
    vkur_cd         TEXT,
    vkur_tips       TEXT,
    apstipr         TEXT,
    apst_pak        TEXT,
    statuss         TEXT,
    sort_nos        TEXT,
    dat_sak         TEXT,
    dat_mod         TEXT,
    dat_beig        TEXT,
    atrib           TEXT,
    std             TEXT
);
CREATE INDEX idx_pagasts_vkur ON aw_pagasts(vkur_cd);
CREATE INDEX idx_pagasts_statuss ON aw_pagasts(statuss);

-- ============================================================
-- Ciemi un mazciemi
-- ============================================================
CREATE TABLE aw_ciems (
    kods            TEXT PRIMARY KEY,
    tips_cd         TEXT,
    nosaukums       TEXT,
    vkur_cd         TEXT,  -- FK → pagasts vai pilsēta
    vkur_tips       TEXT,
    apstipr         TEXT,
    apst_pak        TEXT,
    statuss         TEXT,
    sort_nos        TEXT,
    dat_sak         TEXT,
    dat_mod         TEXT,
    dat_beig        TEXT,
    atrib           TEXT,  -- "1" = mazciems
    std             TEXT
);
CREATE INDEX idx_ciems_vkur ON aw_ciems(vkur_cd);
CREATE INDEX idx_ciems_statuss ON aw_ciems(statuss);

-- ============================================================
-- Ielas
-- ============================================================
CREATE TABLE aw_iela (
    kods            TEXT PRIMARY KEY,
    tips_cd         TEXT,
    nosaukums       TEXT,
    vkur_cd         TEXT,  -- FK → ciems vai pilsēta
    vkur_tips       TEXT,
    apstipr         TEXT,
    apst_pak        TEXT,
    statuss         TEXT,
    sort_nos        TEXT,
    dat_sak         TEXT,
    dat_mod         TEXT,
    dat_beig        TEXT,
    atrib           TEXT,
    std             TEXT
);
CREATE INDEX idx_iela_vkur ON aw_iela(vkur_cd);
CREATE INDEX idx_iela_nosaukums ON aw_iela(nosaukums);
CREATE INDEX idx_iela_statuss ON aw_iela(statuss);

-- ============================================================
-- Ēkas un apbūvei paredzētās zemes vienības
-- ============================================================
CREATE TABLE aw_eka (
    kods            TEXT PRIMARY KEY,
    tips_cd         TEXT,
    statuss         TEXT,
    apstipr         TEXT,
    apst_pak        TEXT,
    vkur_cd         TEXT,  -- FK → iela vai ciems/pagasts
    vkur_tips       TEXT,
    nosaukums       TEXT,
    sort_nos        TEXT,
    atrib           TEXT,  -- pasta indekss LV-XXXX
    pnod_cd         TEXT,
    dat_sak         TEXT,
    dat_mod         TEXT,
    dat_beig        TEXT,
    for_build       TEXT,  -- Y/N
    plan_adr        TEXT,  -- Y/N
    std             TEXT,
    koord_x         REAL,
    koord_y         REAL,
    dd_e            REAL,  -- WGS84 longitude
    dd_n            REAL   -- WGS84 latitude
);
CREATE INDEX idx_eka_vkur ON aw_eka(vkur_cd);
CREATE INDEX idx_eka_statuss ON aw_eka(statuss);
CREATE INDEX idx_eka_std ON aw_eka(std);
CREATE INDEX idx_eka_pnod ON aw_eka(pnod_cd);
CREATE INDEX idx_eka_nosaukums ON aw_eka(nosaukums);

-- ============================================================
-- Telpu grupas (dzīvokļi)
-- ============================================================
CREATE TABLE aw_dziv (
    kods            TEXT PRIMARY KEY,
    tips_cd         TEXT,
    statuss         TEXT,
    apstipr         TEXT,
    apst_pak        TEXT,
    vkur_cd         TEXT,
    vkur_tips       TEXT,
    nosaukums       TEXT,
    sort_nos        TEXT,
    atrib           TEXT,
    dat_sak         TEXT,
    dat_mod         TEXT,
    dat_beig        TEXT,
    std             TEXT
);
CREATE INDEX idx_dziv_vkur ON aw_dziv(vkur_cd);
CREATE INDEX idx_dziv_statuss ON aw_dziv(statuss);

-- ============================================================
-- Rīgas priekšpilsētas
-- ============================================================
CREATE TABLE aw_ppils (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    kods            TEXT,  -- FK → aw_eka
    ppils           TEXT,
    ppils_cd        TEXT,
    dat_sak         TEXT,
    dat_mod         TEXT,
    dat_beig        TEXT
);
CREATE INDEX idx_ppils_kods ON aw_ppils(kods);

-- ============================================================
-- Vietu centroīdi
-- ============================================================
CREATE TABLE aw_vietu_centroidi (
    kods            TEXT PRIMARY KEY,
    tips_cd         TEXT,
    nosaukums       TEXT,
    vkur_cd         TEXT,
    vkur_tips       TEXT,
    std             TEXT,
    koord_x         REAL,
    koord_y         REAL,
    dd_e            REAL,
    dd_n            REAL
);

-- ============================================================
-- Vēsturiskie rajoni
-- ============================================================
CREATE TABLE aw_rajons (
    kods            TEXT PRIMARY KEY,
    tips_cd         TEXT,
    nosaukums       TEXT,
    vkur_cd         TEXT,
    vkur_tips       TEXT,
    apstipr         TEXT,
    apst_pak        TEXT,
    statuss         TEXT,
    sort_nos        TEXT,
    dat_sak         TEXT,
    dat_mod         TEXT,
    dat_beig        TEXT,
    atrib           TEXT
);

-- ============================================================
-- Dokumentu metadati
-- ============================================================
CREATE TABLE aw_doc (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    adreses_kods    TEXT NOT NULL,
    adreses_veids   TEXT NOT NULL,  -- NL / TG / VIETA
    autors          TEXT,
    datums          TEXT,
    veids           TEXT,
    numurs          TEXT,
    nosaukums       TEXT
);
CREATE INDEX idx_doc_kods ON aw_doc(adreses_kods);
CREATE INDEX idx_doc_veids ON aw_doc(adreses_veids);

-- ============================================================
-- Vēsturiskie dati (vienota tabula visiem objektu tipiem)
-- ============================================================
CREATE TABLE aw_vesture (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    kods            TEXT NOT NULL,
    tips_cd         TEXT,
    nosaukums       TEXT,
    vkur_cd         TEXT,
    vkur_tips       TEXT,
    dat_sak         TEXT,
    dat_mod         TEXT,
    dat_beig        TEXT,
    std             TEXT,
    kods_his        TEXT,  -- tikai aw_eka_his
    avota_fails     TEXT   -- no kura faila ielādēts
);
CREATE INDEX idx_vest_kods ON aw_vesture(kods);
CREATE INDEX idx_vest_avots ON aw_vesture(avota_fails);
CREATE INDEX idx_vest_kodshis ON aw_vesture(kods_his);
```

### 12.2 ETL transformāciju kopsavilkums

```
CSV ielādes secība (prioritārā secībā):
1. aw_novads.csv    → aw_novads
2. aw_pilseta.csv   → aw_pilseta
3. aw_pagasts.csv   → aw_pagasts
4. aw_ciems.csv     → aw_ciems
5. aw_iela.csv      → aw_iela
6. aw_eka.csv       → aw_eka        (lielākais — ~608K ieraksti)
7. aw_dziv.csv      → aw_dziv       (~866K ieraksti)
8. aw_rajons.csv    → aw_rajons
9. aw_ppils.csv     → aw_ppils
10. aw_vietu_centroidi.csv → aw_vietu_centroidi

Dokumentu metadati (apvienoti vienā tabulā):
11. aw_doc_nl.csv   → aw_doc (adreses_veids = 'NL')
12. aw_doc_tg.csv   → aw_doc (adreses_veids = 'TG')
13. aw_doc_vieta.csv → aw_doc (adreses_veids = 'VIETA')

Vēsturiskie (apvienoti vienā tabulā):
14. aw_pilseta_his.csv → aw_vesture (avota_fails = 'pilseta_his')
15. aw_novads_his.csv  → aw_vesture
16. aw_pagasts_his.csv → aw_vesture
17. aw_ciems_his.csv   → aw_vesture
18. aw_iela_his.csv    → aw_vesture
19. aw_eka_his.csv     → aw_vesture (ar kods_his lauku)
20. aw_dziv_his.csv    → aw_vesture

Parsēšanas noteikumi:
- Kodējums: utf-8-sig (automātiski noņem BOM)
- Tukšie lauki → NULL
- Datumi atstāt kā tekstu (yyyy.mm.dd)
- Koordinātes pārveidot uz REAL
```

### 12.3 Minimālais datu kopums

Adrešu meklēšanai pietiek ar:
- `aw_eka.csv` (ar STD un koordinātēm)
- `aw_dziv.csv` (ar STD)

Pilnai hierarhijai papildus:
- `aw_iela.csv`, `aw_ciems.csv`, `aw_pagasts.csv`, `aw_novads.csv`, `aw_pilseta.csv`

### 12.4 Datubāzes optimizācijas

Papildu indeksi VAR tabulām:

| Indekss | Tabula | Kolonna(-s) | Pamatojums |
|---------|--------|-------------|------------|
| `idx_eka_pnod` | `aw_eka` | `pnod_cd` | Plānošanas nodaļu teritoriju meklēšana (836 unikālas vērtības) |
| `idx_eka_nosaukums` | `aw_eka` | `nosaukums` | Ēku nosaukumu/numuru meklēšana |
| `idx_vest_kodshis` | `aw_vesture` | `kods_his` | Vēsturisko kodu meklēšana (tikai aw_eka_his datos) |

---

## Atsauces

| Resurss | URL |
|---------|-----|
| **VAR atvērtie dati** | https://data.gov.lv/dati/dataset/varis-atvertie-dati |
| **VZD specifikācija** | https://www.vzd.gov.lv/lv/VAR-atversana |
| **Adresācijas noteikumi** | https://likumi.lv/ta/id/324387 |
| **ATVK klasifikators** | https://likumi.lv/ta/id/324030 |
| **Administratīvo teritoriju likums** | https://likumi.lv/ta/id/315654 |
| **Kadastrs.lv** | https://www.kadastrs.lv |
| **Ģeolatvija.lv** | https://www.geolatvija.lv |
| **VZD kontakts** | dati@vzd.gov.lv |

---

*Dokuments sagatavots: 2026-02-23*
*Pamatots uz VZD specifikāciju v7.0 (24.07.2025) un telpisko datu specifikāciju v1.0 (22.12.2021) un data.gov.lv CKAN API datiem*
