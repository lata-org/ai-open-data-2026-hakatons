# NĪVKIS Atvērto Datu Modelis

> Izsmeļošs Latvijas kadastra atvērto teksta datu apraksts no Valsts zemes dienesta (VZD).
> Datu avots: Nekustamā īpašuma valsts kadastra informācijas sistēma (NĪVKIS).
> Atjaunināts: 2026-02-23 | Licence: CC-BY-4.0 | Atjaunināšanas biežums: reizi nedēļā

---

## Satura rādītājs

1. [Pārskats](#1-pārskats)
2. [Datu kopu struktūra](#2-datu-kopu-struktūra)
3. [Entītiju relāciju modelis](#3-entītiju-relāciju-modelis)
4. [Detalizētas shēmas pa resursiem](#4-detalizētas-shēmas-pa-resursiem)
5. [Klasifikatori](#5-klasifikatori)
6. [Sasaiste ar VAR](#6-sasaiste-ar-var)
7. [Lietošanas scenāriji](#7-lietošanas-scenāriji)
8. [Tehniskie norādījumi](#8-tehniskie-norādījumi)
9. [CKAN API pieejas punkti](#9-ckan-api-pieejas-punkti)
10. [Datu lejupielādes URL saraksts](#10-datu-lejupielādes-url-saraksts)
11. [Datu normalizācijas ieteikumi](#11-datu-normalizācijas-ieteikumi)

---

## 1. Pārskats

### 1.1 Kas ir NĪVKIS atvērtie dati?

VZD publicē Latvijas atvērto datu portālā (data.gov.lv) kadastra informācijas sistēmas teksta datus XML formātā. Dati aptver **10 datu kopu** par nekustamā īpašuma objektiem.

### 1.2 Metadati

| Parametrs | Vērtība |
|-----------|---------|
| **Nosaukums** | Kadastra informācijas sistēmas atvērtie teksta dati |
| **Publicētājs** | Valsts zemes dienests (VZD) |
| **Kontakts** | dati@vzd.gov.lv |
| **Licence** | CC-BY-4.0 |
| **CKAN dataset ID** | `kadastra-informacijas-sistemas-atvertie-dati` |
| **CKAN UUID** | `be841486-4af9-4d38-aa14-6502a2ddb517` |
| **Formāts** | XML faili ZIP arhīvos |
| **Atjaunināšana** | Reizi nedēļā |
| **Maksimālais datnes izmērs** | 500 MB |
| **HVD** | Augstvērtīga datu kopa (ES HVD) |

### 1.3 Termini un saīsinājumi

| Saīsinājums | Pilns nosaukums |
|-------------|-----------------|
| **NĪVKIS** | Nekustamā īpašuma valsts kadastra informācijas sistēma |
| **VAR** | Valsts adrešu reģistrs |
| **VZD** | Valsts zemes dienests |
| **ATVK** | Administratīvo teritoriju un teritoriālā iedalījuma vienību klasifikators |
| **FSO** | Funkcionāli saistītais objekts |
| **LIZ** | Lauksaimniecībā izmantojamā zeme |
| **VMD** | Valsts meža dienests |
| **XSD** | XML shēmas definīcija |
| **ZG** | Zemesgrāmata |

### 1.4 Kadastra numuru struktūra

#### Kadastra numurs (īpašumam, 11 cipari)

Formāts: `KKGGNNNNNNN`

| Pozīcija | Cipari | Apraksts | Piemērs |
|----------|--------|----------|---------|
| 1-2 | KK | Kadastrālās teritorijas kods | 01 = Rīga |
| 3-4 | GG | Kadastrālās grupas kods | 00 |
| 5-11 | NNNNNNN | Īpašuma/zemes vienības numurs | 1240238 |

**Piemērs:** `01001240238` = Rīgas īpašums

#### Kadastra apzīmējums (objektiem)

| Objekta tips | Ciparu skaits | Formāts | Piemērs |
|--------------|---------------|---------|---------|
| Zemes vienība | 11 | KKGGNNNNNNN | `01001240238` |
| Zemes vienības daļa | 15 | KKGGNNNNNNN DDDD | `010012402380001` |
| Būve | 14 | KKGGNNNNNNN BBB | `01001240238001` |
| Telpu grupa | 17 | KKGGNNNNNNN BBBTTTT | `01000190003001129` |

### 1.5 Kadastra numuri — datu tips

Lai gan specifikācija norāda kadastra numurus kā Number tipu, XSD shēmā visi kadastra numuri (`ProCadastreNr`, `ParcelCadastreNr`, `BuildingCadastreNr`, `PremiseGroupCadastreNr`, `ObjectCadastreNr`) ir definēti kā `xs:string` ar ciparu šablonu `[0-9]+`. Datubāzē ieteicams glabāt kā **TEXT**, lai saglabātu sākuma nulles (piem. `01001240238`).

---

## 2. Datu kopu struktūra

### 2.1 Resursu pārskats

| # | ZIP fails | XSD shēma | Apraksts | Izmērs |
|---|-----------|-----------|----------|--------|
| 1 | `property.zip` | PropertyFullData | Nekustamie īpašumi un to sastāvs | 70.8 MB |
| 2 | `parcel.zip` | ParcelFullData | Zemes vienības | 47.6 MB |
| 3 | `parcelpart.zip` | ParcelPartFullData | Zemes vienību daļas | 526 KB |
| 4 | `building.zip` | BuildingFullData | Būves (ēkas, inženierbūves) | 196.2 MB |
| 5 | `premisegroup.zip` | PremiseGroupFullData | Telpu grupas (dzīvokļi, telpas) | 57.6 MB |
| 6 | `address.zip` | AddressFullData | Kadastra objektu adreses | 37.5 MB |
| 7 | `ownership.zip` | OwnershipFullData | Īpašumtiesību statusi | 11.6 MB |
| 8 | `encumbrance.zip` | EncumbranceFullData | Apgrūtinājumi | 52.0 MB |
| 9 | `mark.zip` | MarkFullData | Atzīmes | 539 KB |
| 10 | `valuation.zip` | ValuationFullData | Kadastrālās vērtības | 145.6 MB |
| 11 | `ad_xsdshemas_01012025.zip` | — | XSD shēmu fails | 22 KB |

**Kopējais izmērs: ~620 MB** (ZIP arhīvi ar XML datiem)

### 2.2 XML failu struktūra arhīvos

```
{DatuKopa}.zip/
└── {DatuKopa}/
    ├── {ATVK}_{datums}_{paketes_id}/
    │   └── {GUID}.xml
    └── ...
```

**Piemērs:**
```
property.zip/
└── Property/
    ├── 0001000_20260120_439439/
    │   └── a1b2c3d4-e5f6-7890-abcd-ef1234567890.xml
    └── 0170000_20260120_439440/
        └── ...
```

Katrs XML satur vienas ATVK teritorijas datus. Katram XML failam ir kopīga saknes struktūra:

```xml
<{Schema}FullData>
  <PreparedDate>2026-01-20</PreparedDate>
  <PacketId>439439</PacketId>
  <FilePartCount>1</FilePartCount>
  <FilePartNr>1</FilePartNr>
  <ATVK>0001000</ATVK>
  <{Schema}ItemList>
    <{Schema}ItemData>...</{Schema}ItemData>
  </{Schema}ItemList>
</{Schema}FullData>
```

---

## 3. Entītiju relāciju modelis

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              NĪVKIS                                     │
│                                                                         │
│  ┌──────────────┐        ┌──────────────┐        ┌──────────────┐      │
│  │   Property   │───────►│   Objects    │        │   Address    │      │
│  │              │        │ (ObjectList) │        │              │      │
│  │ ProCadastreNr│        │              │        │ ARCode ──────┼──┐   │
│  │   (11 cip.)  │        │ObjectCadastre│◄──────►│ObjectCadastre│  │   │
│  └──────────────┘        │   NrData     │        │     Nr       │  │   │
│         │                └──────┬───────┘        └──────────────┘  │   │
│         │                       │                                   │   │
│  ┌──────┴───────┐  ┌───────────┼─────────────────────┐            │   │
│  │  Ownership   │  │           │                     │            │   │
│  │  Valuation   │  ▼           ▼                     ▼            │   │
│  │  Mark        │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐│
│  └──────────────┘  │    Parcel    │  │   Building   │  │ PremiseGroup ││
│                    │              │◄─│              │◄─│              ││
│  ┌──────────────┐  │ (11 cipari) │  │ (14 cipari)  │  │ (17 cipari)  ││
│  │  Encumbrance │  │              │  │              │  │              ││
│  │              │  │ VARISCode────┼──┤ VARISCode────┼──┤ VARISCode────┼┤
│  │(Parcel/Bldg/ │  │              │  │              │  │              ││
│  │ PremGrp/Part)│  │ParcelPart ◄──┘  │              │  │              ││
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘│
│                                                                         │
└─────────────────────────────────────────────────────────────┬───────────┘
                                                               │
                    VARISCode / ARCode                          │
                                                               ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       VAR (Valsts adrešu reģistrs)                      │
│   AW_EKA.KODS = VARISCode / ARCode                                      │
│   AW_DZIV.KODS = PremiseGroupVARISCode / ARCode                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.1 Relāciju kopsavilkums

| Saistība | Tips | Atslēga | Apraksts |
|----------|------|---------|----------|
| Property → Parcel/Building/PremiseGroup | 1:N | `ObjectCadastreNrData` | Īpašuma sastāvā esošie objekti |
| Building → Parcel | N:1 | `ObjectRelation.ObjectCadastreNr` | Būve atrodas uz zemes vienības |
| PremiseGroup → Building | N:1 | `ObjectRelation.ObjectCadastreNr` | Telpu grupa atrodas būvē |
| ParcelPart → Parcel | N:1 | `ObjectRelation.ObjectCadastreNr` | Daļa pieder zemes vienībai |
| Address → jebkurš objekts | N:1 | `ObjectRelation.ObjectCadastreNr` | Adreses sasaiste ar objektu |
| Ownership → Property/Building | N:1 | `ObjectRelation.ObjectCadastreNr` | Īpašumtiesību sasaiste |
| Encumbrance → Parcel/Building/PremGrp/Part | N:1 | `ObjectRelation.ObjectCadastreNr` | Apgrūtinājumu sasaiste |
| Mark → Property/Parcel/Building/Part | N:1 | `ObjectRelation.ObjectCadastreNr` | Atzīmju sasaiste |
| Valuation → jebkurš objekts | N:1 | `ObjectRelation.ObjectCadastreNr` | Vērtību sasaiste |
| Address → VAR | N:1 | `ARCode` = `KODS` | Sasaiste ar VAR adrešu reģistru |
| Parcel/Building/PremiseGroup → VAR | N:1 | `VARISCode` = `KODS` | Tieša sasaiste ar VAR |

### 3.2 ObjectRelation mehānisms

Datu kopas 3-10 (viss izņemot Property un Parcel) izmanto vienotu `ObjectRelation` struktūru:

```xml
<ObjectRelation>
  <ObjectCadastreNr>01001240238</ObjectCadastreNr>
  <ObjectType>PARCEL</ObjectType>
</ObjectRelation>
```

**Piezīme:** Parcel (datu kopa 2) NEIZMANTO ObjectRelation — zemes vienība tiek identificēta ar savu `ParcelCadastreNr` un saistīta ar īpašumu caur PropertyContentData.

`ObjectType` norāda vecākobjekta tipu. Katrai datu kopai ir savi atļautie ObjectType vērtību kopumi (skatīt 4. sadaļu).

---

## 4. Detalizētas shēmas pa resursiem

### 4.1 PropertyFullData — Nekustamie īpašumi

Galvenā tabula. Katrs ieraksts = viens nekustamais īpašums ar tā sastāvu.

```xml
<PropertyItemData>
  <CadastreObjectIdData>
    <PropertyKind>Zemes un būvju īpašums</PropertyKind>
    <ProCadastreNr>01001240238</ProCadastreNr>
    <ShareFlatProperty/>
  </CadastreObjectIdData>
  <PropertyContentData>
    <ObjectList>
      <ObjectData>
        <ObjectKindData>Zemes vienība</ObjectKindData>
        <ObjectCadastreNrData>01001240238</ObjectCadastreNrData>
        <ShareParts>1</ShareParts>
        <NrOfShares>1</NrOfShares>
      </ObjectData>
    </ObjectList>
  </PropertyContentData>
  <PropertyBasicData>
    <PropertyName>Mājas nosaukums</PropertyName>
    <PropertyParcelTotalArea>556</PropertyParcelTotalArea>
    <PropertyPremiseGroupTotalArea/>
  </PropertyBasicData>
  <LandbookData>
    <LandbookFolioNr>16875</LandbookFolioNr>
    <LandbookFolioLiterNr/>
    <LandbookOfficeName>Rīgas pilsētas zemesgrāmata</LandbookOfficeName>
    <NotCorroboratedInLandbook/>
  </LandbookData>
</PropertyItemData>
```

| Elements | Tips | Obligāts | Apraksts |
|----------|------|----------|----------|
| `ProCadastreNr` | String(11) | Jā | **PK** — Īpašuma kadastra numurs |
| `PropertyKind` | String(40) | Jā | Īpašuma veids (skatīt 5.1) |
| `ShareFlatProperty` | String(40) | Nē | Sadales dzīvokļa īpašumos pazīme |
| `ObjectKindData` | String(200) | Jā | Objekta veids (skatīt 5.2) |
| `ObjectCadastreNrData` | String(17) | Jā | Objekta kadastra apzīmējums (**FK → Parcel/Building/PremiseGroup**) |
| `ShareParts` | Number(16) | Nē | Domājamās daļas skaitītājs |
| `NrOfShares` | Number(16) | Nē | Domājamās daļas saucējs |
| `PropertyName` | String(40) | Nē | Īpašuma nosaukums |
| `PropertyParcelTotalArea` | Number(20,4) | Nē | Zemes kopplatība m² |
| `PropertyPremiseGroupTotalArea` | Number(20,4) | Nē | Telpu grupu kopplatība m² |
| `LandbookFolioNr` | String(12) | Nē | Zemesgrāmatas nodalījuma numurs |
| `LandbookFolioLiterNr` | String(10) | Nē | Apakšnodalījuma numurs |
| `LandbookOfficeName` | String(100) | Nē | Zemesgrāmatas nodaļas nosaukums |
| `NotCorroboratedInLandbook` | String(62) | Nē | Pazīme — izmaiņas nav nostiprinātas ZG |

---

### 4.2 ParcelFullData — Zemes vienības

```xml
<ParcelItemData>
  <ParcelBasicData>
    <ParcelCadastreNr>01001240238</ParcelCadastreNr>
    <ParcelStatus>
      <ParcelStatusKindId>1</ParcelStatusKindId>
      <ParcelStatusKindName>Reģistrēta</ParcelStatusKindName>
    </ParcelStatus>
    <ParcelVARISCode>101234567</ParcelVARISCode>
    <ATVKCode>0001000</ATVKCode>
    <ParcelArea>556.00</ParcelArea>
    <ParcelLizValue>45</ParcelLizValue>
    <NewForestArea>100.00</NewForestArea>
  </ParcelBasicData>
  <LandPurposeList>
    <LandPurposeData>
      <LandPurposeKind>
        <LandPurposeKindId>0601</LandPurposeKindId>
        <LandPurposeKindName>Individuālo dzīvojamo māju apbūve</LandPurposeKindName>
      </LandPurposeKind>
      <LandPurposeArea>556.00</LandPurposeArea>
      <LandPurposeExplicationData>
        <AgricultTotal>200.00</AgricultTotal>
        <AgricultDetails>
          <Areable>100.00</Areable>
          <Orchards>50.00</Orchards>
          <Meadows>30.00</Meadows>
          <Pastures>20.00</Pastures>
        </AgricultDetails>
        <Forest>150.00</Forest>
        <Bushes>10.00</Bushes>
        <Swamp>0</Swamp>
        <UnderWaterTotal>20.00</UnderWaterTotal>
        <UnderWaterDetails>
          <UnderFishPonds>10.00</UnderFishPonds>
          <Flooded>10.00</Flooded>
        </UnderWaterDetails>
        <UnderBuildings>106.00</UnderBuildings>
        <UnderRoads>50.00</UnderRoads>
        <OtherLand>20.00</OtherLand>
        <Drained>100.00</Drained>
      </LandPurposeExplicationData>
    </LandPurposeData>
  </LandPurposeList>
  <SurveyList>
    <SurveyData>
      <SurveyKind>Instrumentālā</SurveyKind>
      <SurveyDate>2020-05-15</SurveyDate>
    </SurveyData>
  </SurveyList>
  <PlannedParcelList>
    <PlannedParcelData>
      <VARISCode>101234568</VARISCode>
      <PlannedParcelCadastreNr>01001240239</PlannedParcelCadastreNr>
      <PlannedParcelArea>300.00</PlannedParcelArea>
    </PlannedParcelData>
  </PlannedParcelList>
</ParcelItemData>
```

| Elements | Tips | Obligāts | Apraksts |
|----------|------|----------|----------|
| `ParcelCadastreNr` | String(11) | Jā | **PK** — Zemes vienības kadastra apzīmējums |
| `ParcelStatusKindId` | Number(2) | Jā | Statusa kods |
| `ParcelStatusKindName` | String(120) | Jā | Statusa nosaukums |
| `ParcelVARISCode` | Number(12) | Nē | **FK → VAR** (AW_EKA.KODS) |
| `ATVKCode` | String(7) | Nē | ATVK teritorijas kods |
| `ParcelArea` | Number(12,4) | Jā | Platība m² |
| `ParcelLizValue` | String | Nē | LIZ kvalitātes novērtējums ballēs |
| `NewForestArea` | Number(12,4) | Nē | Jaunaudzes platība m² |
| `LandPurposeKindId` | String(10) | Jā | Lietošanas mērķa kods |
| `LandPurposeKindName` | String(400) | Jā | Lietošanas mērķa nosaukums |
| `LandPurposeArea` | Number(12,4) | Jā | Mērķim piekrītošā platība m² |

#### Zemes eksplikācija (LandPurposeExplicationData)

| Elements | Apraksts |
|----------|----------|
| `AgricultTotal` | Lauksaimniecības zemes kopplatība m² |
| `Areable` | Aramzeme m² |
| `Orchards` | Augļu dārzs m² |
| `Meadows` | Pļava m² |
| `Pastures` | Ganības m² |
| `Forest` | Mežs m² |
| `Bushes` | Krūmājs m² |
| `Swamp` | Purvs m² |
| `UnderWaterTotal` | Ūdens objektu zeme m² |
| `UnderFishPonds` | Zeme zem zivju dīķiem m² |
| `Flooded` | Zeme zem ūdeņiem m² |
| `UnderBuildings` | Zeme zem ēkām un pagalmiem m² |
| `UnderRoads` | Zeme zem ceļiem m² |
| `OtherLand` | Pārējās zemes m² |
| `Drained` | Meliorētā LIZ m² |

#### Plānotās zemes vienības (PlannedParcelList)

| Elements | Tips | Obligāts | Apraksts |
|----------|------|----------|----------|
| `VARISCode` | Number(10) | Nē | Plānotās zemes vienības VAR kods |
| `PlannedParcelCadastreNr` | String(11) | Jā* | Plānotais kadastra apzīmējums |
| `PlannedParcelArea` | Number(12,4) | Jā* | Plānotā platība m² |

*Obligāti PlannedParcelData elementa iekšienē (PlannedParcelList pats ir neobligāts).

#### Uzmērīšanas dati (SurveyList)

| Elements | Tips | Obligāts | Apraksts |
|----------|------|----------|----------|
| `SurveyKind` | String | Jā* | Uzmērīšanas veids |
| `SurveyDate` | Date | Jā* | Uzmērīšanas datums |

*Obligāti SurveyData elementa iekšienē (SurveyList pats ir neobligāts).

---

### 4.3 ParcelPartFullData — Zemes vienību daļas

```xml
<ParcelPartItemData>
  <ParcelPartBasicData>
    <ParcelPartCadastreNr>010012402380001</ParcelPartCadastreNr>
    <ParcelPartArea>200.00</ParcelPartArea>
    <ParcelPartLizValue>42</ParcelPartLizValue>
  </ParcelPartBasicData>
  <LandPurposeList>...</LandPurposeList>
  <SurveyList>...</SurveyList>
  <ObjectRelation>
    <ObjectCadastreNr>01001240238</ObjectCadastreNr>
    <ObjectType>PARCEL</ObjectType>
  </ObjectRelation>
</ParcelPartItemData>
```

| Elements | Tips | Obligāts | Apraksts |
|----------|------|----------|----------|
| `ObjectCadastreNr` | String(11) | Jā | **FK → Parcel** |
| `ObjectType` | String(40) | Jā | Vienmēr "PARCEL" |
| `ParcelPartCadastreNr` | String(15) | Jā | **PK** — Daļas kadastra apzīmējums |
| `ParcelPartArea` | Number(12,4) | Jā | Platība m² |
| `ParcelPartLizValue` | String | Nē | LIZ kvalitātes novērtējums ballēs |

Satur arī `LandPurposeList` un `SurveyList` — identiska struktūra kā ParcelFullData.

---

### 4.4 BuildingFullData — Būves

```xml
<BuildingItemData>
  <BuildingBasicData>
    <BuildingCadastreNr>01001240238001</BuildingCadastreNr>
    <VARISCode>101234567</VARISCode>
    <BuildingName>Dzīvojamā māja</BuildingName>
    <BuildingUseKind>
      <BuildingUseKindId>1110</BuildingUseKindId>
      <BuildingUseKindName>Viena dzīvokļa māja</BuildingUseKindName>
    </BuildingUseKind>
    <BuildingArea>150.50</BuildingArea>
    <BuildingConstrArea>80.00</BuildingConstrArea>
    <BuildingGroundFloors>2</BuildingGroundFloors>
    <BuildingUndergroundFloors>1</BuildingUndergroundFloors>
    <BuildingMaterialKind>
      <MaterialKindId>2</MaterialKindId>
      <MaterialKindName>Ķieģeļi</MaterialKindName>
    </BuildingMaterialKind>
    <BuildingPregCount>4</BuildingPregCount>
    <BuildingAcceptionYears>1985</BuildingAcceptionYears>
    <BuildingExploitYear>1985</BuildingExploitYear>
    <BuildingDeprecation>V3</BuildingDeprecation>
    <BuildingDepValDate>2023-06-15</BuildingDepValDate>
    <BuildingSurveyDate>2023-06-15</BuildingSurveyDate>
    <NotForLandBook/>
    <ParcelCadastreNrList>
      <ObjectCadastreNrData>01001240238</ObjectCadastreNrData>
    </ParcelCadastreNrList>
    <Prereg/>
    <NotExist/>
    <EngineeringStructureType/>
  </BuildingBasicData>
  <BuildingTypeData>
    <BuildingKind>
      <BuildingKindId>11100101</BuildingKindId>
      <BuildingKindName>Viena dzīvokļa māja</BuildingKindName>
    </BuildingKind>
  </BuildingTypeData>
  <BuildingElementData>
    <ConstructionDataList>
      <BuildingElementMaterialKindList>
        <BuildingElementMaterialKind>
          <MaterialKindId>1</MaterialKindId>
          <MaterialKindName>Dzelzsbetona</MaterialKindName>
        </BuildingElementMaterialKind>
      </BuildingElementMaterialKindList>
      <BuildingElementName>Pamati</BuildingElementName>
      <BuildingElementExploitYear>1985</BuildingElementExploitYear>
    </ConstructionDataList>
  </BuildingElementData>
  <BuildingAmountList>
    <BuildingAmountData>
      <BuildingAmountKind>
        <AmountKindId>1</AmountKindId>
        <AmountKindName>Tilpums</AmountKindName>
      </BuildingAmountKind>
      <BuildingAmountQuantity>450.00</BuildingAmountQuantity>
      <BuildingAmountMeasure>
        <MeasureKindId>1</MeasureKindId>
        <MeasureKindName>m³</MeasureKindName>
      </BuildingAmountMeasure>
    </BuildingAmountData>
  </BuildingAmountList>
  <BuildingOrPremiseGroupExplicationData>
    <TotalArea>150.50</TotalArea>
    <TotalAreaDetails>
      <ExpedientArea>140.00</ExpedientArea>
      <ExpedientAreaDetails>
        <FlatTotalArea>100.00</FlatTotalArea>
        <FlatTotalAreaDetails>
          <FlatArea>90.00</FlatArea>
          <FlatAreaDetails>
            <LivingArea>70.00</LivingArea>
            <FlatAuxArea>20.00</FlatAuxArea>
          </FlatAreaDetails>
          <FlatOuterArea>10.00</FlatOuterArea>
        </FlatTotalAreaDetails>
        <NonlivingTotalArea>40.00</NonlivingTotalArea>
        <NonlivingAreaDetails>
          <NonlivingInteriorArea>35.00</NonlivingInteriorArea>
          <NonlivingOuterArea>5.00</NonlivingOuterArea>
        </NonlivingAreaDetails>
      </ExpedientAreaDetails>
      <SharedArea>10.50</SharedArea>
      <SharedAreaDetails>
        <SharedInteriorArea>8.00</SharedInteriorArea>
        <SharedOuterArea>2.50</SharedOuterArea>
      </SharedAreaDetails>
    </TotalAreaDetails>
  </BuildingOrPremiseGroupExplicationData>
  <BuildingHistoricalData>
    <BuildingHistoricalLiter>A</BuildingHistoricalLiter>
    <BuildingHistoricalName>Vecais nosaukums</BuildingHistoricalName>
  </BuildingHistoricalData>
  <ObjectRelation>
    <ObjectCadastreNr>01001240238</ObjectCadastreNr>
    <ObjectType>PARCEL</ObjectType>
  </ObjectRelation>
</BuildingItemData>
```

#### Pamata lauki (BuildingBasicData)

| Elements | Tips | Obligāts | Apraksts |
|----------|------|----------|----------|
| `BuildingCadastreNr` | String(14) | Jā | **PK** — Būves kadastra apzīmējums |
| `ObjectCadastreNr` (ObjectRelation) | String(11) | Jā | **FK → Parcel** |
| `VARISCode` | Number(12) | Nē | **FK → VAR** (AW_EKA.KODS) |
| `BuildingName` | String(100) | Nē | Būves nosaukums |
| `BuildingUseKindId` | Number(6) | Nē | Galvenā lietošanas veida kods |
| `BuildingUseKindName` | String(235) | Nē | Galvenā lietošanas veida nosaukums |
| `BuildingArea` | Number(20,4) | Nē | Kopējā platība m² |
| `BuildingConstrArea` | Number(12,4) | Nē | Apbūves laukums m² |
| `BuildingGroundFloors` | Number(3) | Nē | Virszemes stāvu skaits |
| `BuildingUndergroundFloors` | Number(3) | Nē | Pazemes stāvu skaits |
| `MaterialKindId` | Number(4) | Nē | Ārsienu materiāla kods |
| `MaterialKindName` | String(100) | Nē | Ārsienu materiāla nosaukums |
| `BuildingPregCount` | Number(4) | Nē | Telpu grupu skaits būvē |
| `BuildingAcceptionYears` | String(500) | Nē | Ekspluatācijā pieņemšanas gads(-i) |
| `BuildingExploitYear` | gYear | Nē | Uzbūvēšanas gads |
| `BuildingDeprecation` | String(5) | Nē | Nolietojums (%, vai V1-V5 ēkām) |
| `BuildingDepValDate` | Date | Nē | Nolietojuma noteikšanas datums |
| `BuildingSurveyDate` | Date | Nē | Apsekošanas datums |
| `NotForLandBook` | String(47) | Nē | Pazīme — dati nav izmantojami ZG |
| `Prereg` | String(20) | Nē | Pazīme par pirmsreģistrētu būvi |
| `NotExist` | String(26) | Nē | Pazīme — būve apvidū nav konstatēta |
| `EngineeringStructureType` | String(30) | Nē | Inženierbūves tips (skatīt 5.5) |

#### Būves tipa dati (BuildingTypeData)

| Elements | Tips | Obligāts | Apraksts |
|----------|------|----------|----------|
| `BuildingKindId` | String(8) | Nē | Būves tipa kods |
| `BuildingKindName` | String(1000) | Nē | Būves tipa nosaukums |

#### Konstrukciju dati (BuildingElementData / ConstructionDataList)

| Elements | Tips | Obligāts | Apraksts |
|----------|------|----------|----------|
| `BuildingElementMaterialKindList` | — | Nē | Materiālu saraksts |
| `MaterialKindId` | String(4) | Nē | Materiāla kods |
| `MaterialKindName` | String(100) | Nē | Materiāla nosaukums |
| `BuildingElementName` | String(100) | Nē | Konstrukcijas elementa nosaukums |
| `BuildingElementExploitYear` | gYear | Nē | Uzbūvēšanas gads |
| `BuildingElementConstructionKindList` | — | Nē | Konstrukcijas veidi (dati netiek reģistrēti) |
| `BuildingElementAcceptionYears` | String | Nē | Pieņemšanas gads (dati netiek reģistrēti) |
| `BuildingElementDeprecation` | String | Nē | Elementa nolietojums (dati netiek reģistrēti) |

#### Apjoma dati (BuildingAmountData)

| Elements | Tips | Obligāts | Apraksts |
|----------|------|----------|----------|
| `AmountKindId` | String(4) | Nē | Apjoma rādītāja kods |
| `AmountKindName` | String(100) | Nē | Apjoma rādītāja nosaukums |
| `BuildingAmountQuantity` | String(12) | Nē | Daudzums |
| `MeasureKindId` | String(4) | Nē | Mērvienības kods |
| `MeasureKindName` | String(80) | Nē | Mērvienības nosaukums |
| `BuildingAmountTitle` | String(100) | Nē | Apjoma nosaukums |
| `BuildingAmountBuildingKind` | — | Nē | Apjoma rādītāja būves tips |
| `BuildingKindId` (Amount) | String(8) | Nē | Būves tipa kods |
| `BuildingKindName` (Amount) | String(30) | Nē | Būves tipa nosaukums |

#### Labiekārtojumu dati (ImprovementItemData)

```xml
<ImprovementItemData>
  <ImprovementCommonData>
    <ImprovementDate>2023-01-15</ImprovementDate>
  </ImprovementCommonData>
  <ImprovementList>
    <ImprovementData>
      <ImprovementTypeName>Apkure</ImprovementTypeName>
      <ImprovementDetectionForm>Apsekošana</ImprovementDetectionForm>
      <ImprovementQuantity>1</ImprovementQuantity>
    </ImprovementData>
  </ImprovementList>
</ImprovementItemData>
```

| Elements | Tips | Obligāts | Apraksts |
|----------|------|----------|----------|
| `ImprovementDate` | String | Nē | Labiekārtojumu noteikšanas datums |
| `ImprovementTypeName` | String | Nē | Labiekārtojuma veids |
| `ImprovementDetectionForm` | String | Nē | Noteikšanas veids |
| `ImprovementQuantity` | String | Nē | Daudzums |

#### Platību eksplikācija (BuildingOrPremiseGroupExplicationData)

Hierarhiskā platību struktūra (lietota tikai Building — XSD nesatur šo struktūru PremiseGroup):

```
TotalArea
├── ExpedientArea (lietderīgā)
│   ├── FlatTotalArea (dzīvojamā)
│   │   ├── FlatArea (iekšējā)
│   │   │   ├── LivingArea (dzīvojamā platība)
│   │   │   └── FlatAuxArea (palīgplatība)
│   │   └── FlatOuterArea (ārējā — balkoni u.c.)
│   └── NonlivingTotalArea (nedzīvojamā)
│       ├── NonlivingInteriorArea (iekšējā)
│       └── NonlivingOuterArea (ārējā)
└── SharedArea (koplietošanas)
    ├── SharedInteriorArea (iekšējā)
    └── SharedOuterArea (ārējā)
```

---

### 4.5 PremiseGroupFullData — Telpu grupas

```xml
<PremiseGroupItemData>
  <PremiseGroupBasicData>
    <PremiseGroupCadastreNr>01001240238001001</PremiseGroupCadastreNr>
    <PremiseGroupName>Dzīvoklis</PremiseGroupName>
    <PremiseGroupVARISCode>119612571</PremiseGroupVARISCode>
    <PremiseGroupUseKind>
      <PremiseGroupUseKindId>1122</PremiseGroupUseKindId>
      <PremiseGroupUseKindName>Triju vai vairāku dzīvokļu mājas dzīvojamo telpu grupa</PremiseGroupUseKindName>
    </PremiseGroupUseKind>
    <PremiseGroupBuildingFloor>4</PremiseGroupBuildingFloor>
    <PremiseGroupPremiseCount>3</PremiseGroupPremiseCount>
    <PremiseGroupArea>65.40</PremiseGroupArea>
    <PremiseGroupSurveyDate>2023-12-19</PremiseGroupSurveyDate>
    <PremiseGroupAcceptionYears>1975</PremiseGroupAcceptionYears>
    <NotForLandBook/>
  </PremiseGroupBasicData>
  <ObjectRelation>
    <ObjectCadastreNr>01001240238001</ObjectCadastreNr>
    <ObjectType>BUILDING</ObjectType>
  </ObjectRelation>
</PremiseGroupItemData>
```

| Elements | Tips | Obligāts | Apraksts |
|----------|------|----------|----------|
| `ObjectCadastreNr` (ObjectRelation) | String(14) | Jā | **FK → Building** |
| `ObjectType` | String(40) | Jā | Vienmēr "BUILDING" |
| `PremiseGroupCadastreNr` | String(17) | Jā | **PK** — Telpu grupas kadastra apzīmējums |
| `PremiseGroupName` | String(100) | Jā | Nosaukums (piem. "Dzīvoklis") |
| `PremiseGroupVARISCode` | Number(12) | Nē | **FK → VAR** (AW_DZIV.KODS) |
| `PremiseGroupUseKindId` | Number(6) | Nē | Lietošanas veida kods |
| `PremiseGroupUseKindName` | String(235) | Nē | Lietošanas veida nosaukums |
| `PremiseGroupBuildingFloor` | String | Jā | Piesaistes stāvs |
| `PremiseGroupPremiseCount` | Number(4) | Jā | Telpu skaits |
| `PremiseGroupArea` | Number(20,4) | Jā | Kopējā platība m² |
| `PremiseGroupSurveyDate` | Date | Nē | Apsekošanas datums |
| `PremiseGroupAcceptionYears` | String(500) | Nē | Ekspluatācijā pieņemšanas gads(-i) |
| `NotForLandBook` | String(47) | Nē | Pazīme — dati nav izmantojami ZG |

**Piezīme:** Atšķirībā no specifikācijas apraksta, XSD shēma (`PremiseGroupFullData.xsd`) NESATUR `BuildingOrPremiseGroupExplicationData` elementu telpu grupas struktūrā — platību eksplikācija ir pieejama tikai būvju datos (BuildingFullData). SQLite shēmā `premise_groups` tabulas eksplikācijas kolonnas var būt vienmēr NULL.

---

### 4.6 AddressFullData — Adreses

```xml
<AddressItemData>
  <ObjectRelation>
    <ObjectCadastreNr>01001240238</ObjectCadastreNr>
    <ObjectType>PARCEL</ObjectType>
  </ObjectRelation>
  <AddressData>
    <ARCode>101234567</ARCode>
    <PostIndex>LV-1010</PostIndex>
    <Town>Rīga</Town>
    <County/>
    <Parish/>
    <Village/>
    <Street>Brīvības iela</Street>
    <House>21</House>
    <Apartment>5</Apartment>
  </AddressData>
</AddressItemData>
```

| Elements | Tips | Obligāts | Apraksts |
|----------|------|----------|----------|
| `ObjectCadastreNr` | String(17) | Jā | **FK** — jebkura objekta kadastra apzīmējums |
| `ObjectType` | String(40) | Jā | PARCEL/BUILDING/PREMISE GROUP |
| `ARCode` | Number(12) | Nē | **FK → VAR** (AW_EKA.KODS vai AW_DZIV.KODS) |
| `PostIndex` | String(42) | Nē | Pasta indekss (LV-XXXX) |
| `Town` | String(128) | Nē | Pilsētas nosaukums |
| `County` | String(128) | Nē | Novads (ar "nov.") |
| `Parish` | String(128) | Nē | Pagasts (ar "pag.") |
| `Village` | String(128) | Nē | Ciems/mazciems |
| `Street` | String(128) | Nē | Ielas nosaukums ar nomenklatūras vārdu |
| `House` | String(128) | Nē | Mājas numurs/nosaukums |
| `Apartment` | String(19) | Nē | Dzīvokļa numurs |

---

### 4.7 OwnershipFullData — Īpašumtiesības

```xml
<OwnershipItemData>
  <ObjectRelation>
    <ObjectCadastreNr>01001240238</ObjectCadastreNr>
    <ObjectType>PROPERTY</ObjectType>
  </ObjectRelation>
  <OwnershipStatusKindList>
    <OwnershipStatusKind>
      <OwnershipStatus>Īpašnieks</OwnershipStatus>
      <PersonStatus>fiziska persona</PersonStatus>
    </OwnershipStatusKind>
  </OwnershipStatusKindList>
</OwnershipItemData>
```

| Elements | Tips | Obligāts | Apraksts |
|----------|------|----------|----------|
| `ObjectCadastreNr` | String(14) | Jā | **FK** — Property vai Building |
| `ObjectType` | String(40) | Jā | "PROPERTY" vai "BUILDING" |
| `OwnershipStatus` | String(50) | Jā | Īpašuma tiesību statuss (skatīt 5.7) |
| `PersonStatus` | String(100) | Jā | Personas statuss (skatīt 5.8) |

**Piezīme:** Personas dati (vārdi, personas kodi) nav iekļauti atvērtajos datos.

---

### 4.8 EncumbranceFullData — Apgrūtinājumi

```xml
<EncumbranceItemData>
  <ObjectRelation>
    <ObjectCadastreNr>01001240238</ObjectCadastreNr>
    <ObjectType>PARCEL</ObjectType>
  </ObjectRelation>
  <EncumbranceList>
    <EncumbranceRowData>
      <EncumbranceKind>
        <EncumbranceKindId>1001</EncumbranceKindId>
        <EncumbranceKindName>Servitūts</EncumbranceKindName>
      </EncumbranceKind>
      <EncumbranceNr>1</EncumbranceNr>
      <EncumbranceEstablishDate>2020-01-15</EncumbranceEstablishDate>
      <EncumbranceArea>50.00</EncumbranceArea>
      <EncumbranceMeasure>m2</EncumbranceMeasure>
    </EncumbranceRowData>
  </EncumbranceList>
</EncumbranceItemData>
```

| Elements | Tips | Obligāts | Apraksts |
|----------|------|----------|----------|
| `ObjectCadastreNr` | String(17) | Jā | **FK** — Parcel/ParcelPart/Building/PremiseGroup |
| `ObjectType` | String(40) | Jā | Objekta tips |
| `EncumbranceKindId` | Number(10) | Jā | Apgrūtinājuma kods |
| `EncumbranceKindName` | String(500) | Jā | Apgrūtinājuma apraksts |
| `EncumbranceNr` | String | Jā | Kārtas numurs |
| `EncumbranceEstablishDate` | Date | Nē | Reģistrācijas datums |
| `EncumbranceArea` | Number(12,4) | Nē | Piekritīgā platība |
| `EncumbranceMeasure` | String(3) | Nē | Mērvienība |

---

### 4.9 MarkFullData — Atzīmes

```xml
<MarkItemData>
  <ObjectRelation>
    <ObjectCadastreNr>01001240238</ObjectCadastreNr>
    <ObjectType>PARCEL</ObjectType>
  </ObjectRelation>
  <MarkList>
    <MarkRecData>
      <MarkType>A</MarkType>
      <MarkDate>2023-05-10</MarkDate>
      <MarkDescription>Atzīmes apraksts</MarkDescription>
      <MarkArea>100.00</MarkArea>
    </MarkRecData>
  </MarkList>
</MarkItemData>
```

| Elements | Tips | Obligāts | Apraksts |
|----------|------|----------|----------|
| `ObjectCadastreNr` | String(14) | Jā | **FK** — Property/Parcel/ParcelPart/Building |
| `ObjectType` | String(40) | Jā | Objekta tips |
| `MarkType` | String(4) | Jā | Atzīmes tips |
| `MarkDate` | Date | Nē | Atzīmes datums |
| `MarkDescription` | String(100) | Nē | Atzīmes apraksts |
| `MarkArea` | Number(12,2) | Nē | Atzīmes platība m² |

---

### 4.10 ValuationFullData — Kadastrālās vērtības

```xml
<ValuationItemData>
  <ObjectRelation>
    <ObjectCadastreNr>01001240238</ObjectCadastreNr>
    <ObjectType>PROPERTY</ObjectType>
  </ObjectRelation>
  <ValuationDataList>
    <ValuationRowData>
      <ValueType>fiskālā</ValueType>
      <PropertyValuation>85000.00</PropertyValuation>
      <PropertyValuationDate>2024-01-01</PropertyValuationDate>
      <PropertyCadastralValue>75000.00</PropertyCadastralValue>
      <PropertyCadastralValueDate>2024-01-01</PropertyCadastralValueDate>
      <ObjectCadastralValue>50000.00</ObjectCadastralValue>
      <ObjectCadastralValueDate>2024-01-01</ObjectCadastralValueDate>
      <ValDescription>Kadastrālās vērtības apraksts</ValDescription>
    </ValuationRowData>
  </ValuationDataList>
  <ObjectForestValue>5000.00</ObjectForestValue>
  <ObjectForestValueDate>2024-01-01</ObjectForestValueDate>
</ValuationItemData>
```

| Elements | Tips | Obligāts | Apraksts |
|----------|------|----------|----------|
| `ObjectCadastreNr` | String(17) | Jā | **FK** — jebkurš objekts |
| `ObjectType` | String(40) | Jā | PROPERTY/PARCEL/PARCEL PART/BUILDING/PREMISE GROUP |
| `ValueType` | String(10) | Nē | Vērtības tips (skatīt 5.9) |
| `PropertyValuation` | Number(18,2) | Nē | Īpašuma novērtējums EUR |
| `PropertyValuationDate` | Date | Nē | Novērtējuma datums |
| `PropertyCadastralValue` | Number(18,2) | Nē | Īpašuma kadastrālā vērtība EUR |
| `PropertyCadastralValueDate` | Date | Nē | Kadastrālās vērtības datums |
| `ObjectCadastralValue` | Number(24,2) | Nē | Objekta kadastrālā vērtība EUR |
| `ObjectCadastralValueDate` | Date | Nē | Objekta vērtības datums |
| `ValDescription` | String(2000) | Nē | Vērtības apraksts |
| `ObjectForestValue` | Number(12,2) | Nē | Mežaudzes vērtība EUR |
| `ObjectForestValueDate` | Date | Nē | VMD datu datums |

---

## 5. Klasifikatori

### 5.1 PropertyKind (Īpašuma veids)

| Vērtība | Apraksts |
|---------|----------|
| `Zemes un būvju īpašums` | Zeme ar ēkām |
| `Būvju īpašums` | Tikai ēkas (bez zemes) |
| `Dzīvokļa īpašums` | Dzīvoklis daudzdzīvokļu mājā |
| `Paātrināti privatizēts dzīvoklis` | Privatizēts dzīvoklis |

### 5.2 ObjectKindData (Objekta veids Property sastāvā)

| Vērtība | Apraksts |
|---------|----------|
| `Zemes vienība` | Zemes gabals |
| `Būve` | Ēka vai inženierbūve |
| `Būve (FSO)` | Funkcionāli saistīts objekts |
| `Telpu grupa` | Dzīvoklis vai cita telpu grupa |

### 5.3 ShareFlatProperty (Sadalīšana dzīvokļa īpašumos)

| Vērtība | Apraksts |
|---------|----------|
| `pilnībā sadalīts dzīvokļa īpašumos` | Pilnībā sadalīts |
| `daļēji sadalīts dzīvokļa īpašumos` | Daļēji sadalīts |

### 5.4 BuildingDeprecation (Nolietojums ēkām)

| Vērtība | Apraksts |
|---------|----------|
| `V1` | Ļoti labs stāvoklis |
| `V2` | Labs stāvoklis |
| `V3` | Apmierinošs stāvoklis |
| `V4` | Slikts stāvoklis |
| `V5` | Ļoti slikts / avārijas stāvoklis |

**Piezīme:** Inženierbūvēm nolietojums norādīts procentos (piem. '45%'), ēkām — V1-V5 skala.

### 5.5 EngineeringStructureType

| Vērtība | Apraksts |
|---------|----------|
| `Lineāra` | Lineāra inženierbūve |
| `Punktveida` | Punktveida inženierbūve |
| `Lineāra/Punktveida` | Kombinēta |

### 5.6 ParcelStatusKindId

| Kods | Nosaukums |
|------|-----------|
| 1 | Reģistrēta |

### 5.7 OwnershipStatus

| Vērtība | Apraksts |
|---------|----------|
| `Īpašnieks` | Īpašuma tiesības |
| `Tiesiskais valdītājs` | Tiesiskais valdījums |
| `Lietotājs` | Lietošanas tiesības |
| `Apbūves tiesīgais (īpašnieks)` | Apbūves tiesības (īpašnieks) |
| `Apbūves tiesīgais (tiesiskais valdītājs)` | Apbūves tiesības (valdītājs) |

### 5.8 PersonStatus

| Vērtība | Apraksts |
|---------|----------|
| `fiziska persona` | Fiziska persona |
| `juridiska persona` | Juridiska persona |
| `valsts` | Valsts |
| `pašvaldība` | Pašvaldība |
| `cits` | Cits |

### 5.9 ValueType

| Vērtība | Apraksts |
|---------|----------|
| `fiskālā` | Fiskālā vērtība (nodokļu aprēķinam) |
| `universālā` | Universālā vērtība |
| `projektētā` | Projektētā vērtība |
| `prognozētā` | Prognozētā vērtība |

---

## 6. Sasaiste ar VAR

### 6.1 Sasaistes atslēgas

| NĪVKIS elements | VAR tabula | VAR lauks | Apraksts |
|------------------|-----------|-----------|----------|
| `ParcelVARISCode` | AW_EKA | KODS | Zemes vienības adrese |
| `VARISCode` (Building) | AW_EKA | KODS | Būves adrese |
| `PremiseGroupVARISCode` | AW_DZIV | KODS | Telpu grupas adrese |
| `ARCode` (Address) | AW_EKA / AW_DZIV | KODS | Adreses kods |

### 6.2 Sasaistes piemērs

```sql
-- Ēkas pilna adrese no VAR
SELECT b.BuildingCadastreNr, e.STD as adrese, e.DD_N as lat, e.DD_E as lon
FROM buildings b
JOIN aw_eka e ON b.varis_code = e.KODS
WHERE e.STATUSS = 'EKS';
```

---

## 7. Lietošanas scenāriji

### 7.1 Atrast visus objektus īpašumā

```sql
SELECT po.object_kind, po.object_cadastre_nr
FROM property_objects po
WHERE po.property_cadastre_nr = '01001240238';
```

### 7.2 Atrast ēkas raksturojumu pēc kadastra apzīmējuma

```sql
SELECT b.*, a.street, a.house, a.town
FROM buildings b
LEFT JOIN addresses a ON b.cadastre_nr = a.object_cadastre_nr AND a.object_type = 'BUILDING'
WHERE b.cadastre_nr = '01001240238001';
```

### 7.3 Kadastrālā vērtība visiem objektiem īpašumā

```sql
SELECT po.object_kind, po.object_cadastre_nr,
       v.value_type, v.object_cadastral_value, v.property_cadastral_value
FROM property_objects po
LEFT JOIN valuations v ON po.object_cadastre_nr = v.object_cadastre_nr
WHERE po.property_cadastre_nr = '01001240238';
```

### 7.4 Visi dzīvokļi ēkā ar platībām

```sql
SELECT pg.cadastre_nr, pg.name, pg.area, pg.floor, pg.premise_count
FROM premise_groups pg
WHERE pg.building_cadastre_nr = '01001240238001'
ORDER BY pg.floor, pg.cadastre_nr;
```

### 7.5 Apgrūtinājumi zemes vienībai

```sql
SELECT e.kind_name, e.establish_date, e.area, e.measure
FROM encumbrances e
WHERE e.object_cadastre_nr = '01001240238'
  AND e.object_type = 'PARCEL';
```

---

## 8. Tehniskie norādījumi

### 8.1 XML parsēšana

- XML failos ir namespace `http://ivis.eps.gov.lv/XMLSchemas/100007/CadastreRegistry/v1-0` (ar `elementFormDefault="qualified"`). Praksē elementi var izmantot noklusējuma namespace bez prefiksa.
- Viens ZIP satur daudzus XML failus, katrs ATVK teritorijai
- ZIP iekšienē ir viena direktorija ar datu kopas nosaukumu

### 8.2 XML simbolu aizvietošana

| Oriģinālais | XML aizvietojums |
|-------------|------------------|
| `<` | `&lt;` |
| `>` | `&gt;` |
| `&` | `&amp;` |
| `'` | `&apos;` |
| `"` | `&quot;` |

**Lauki ar aizvietošanu:** `House`, `PremiseGroupName`, `PropertyName`, `BuildingName`, `BuildingHistoricalName`, `BuildingHistoricalLiter`, `BuildingAmountTitle`

### 8.3 Tukšu elementu interpretācija

Tukši XML elementi (`<Element/>`) nozīmē NULL/nav datu. Vienmēr pārbaudīt, vai elements satur tekstu.

### 8.4 Datu ierobežojumi

**Nav publicēti (konfidenciāli):**
- Personas dati (vārdi, personas kodi, reg. numuri)
- Valsts drošībai svarīgu objektu dati
- Telpu labiekārtojuma detaļas

**Publicētie dati:**
- Kadastra numuri un apzīmējumi
- Platības un apjoma rādītāji
- Adreses un to komponenti
- Būvju un telpu grupu raksturojumi
- Zemesgrāmatas informācija
- Kadastrālās vērtības
- Apgrūtinājumi un atzīmes
- Īpašumtiesību statusi (bez personu datiem)

### 8.5 Kadastra numuri kā teksts

Lai gan specifikācija norāda kadastra numurus kā Number tipu, XSD shēmā tie definēti kā `xs:string` ar ciparu šablonu `[0-9]+`. Datubāzē ieteicams glabāt kā TEXT, lai saglabātu sākuma nulles.

---

## 9. CKAN API pieejas punkti

### 9.1 Datu kopas metadati

```
GET https://data.gov.lv/dati/api/3/action/package_show?id=kadastra-informacijas-sistemas-atvertie-dati
```

### 9.2 Organizācijas informācija

```
GET https://data.gov.lv/dati/api/3/action/organization_show?id=valsts-zemes-dienests
```

### 9.3 Resursu lejupielāde

Resursu URL iegūstami no `package_show` atbildes `resources[].url` laukā.

---

## 10. Datu lejupielādes URL saraksts

**Bāzes URL:** `https://data.gov.lv/dati/dataset/be841486-4af9-4d38-aa14-6502a2ddb517/resource/`

| # | Resurss | Izmērs | Resource ID | URL |
|---|---------|--------|-------------|-----|
| 1 | Nekustamie īpašumi | 70.8 MB | `931e6299-61ba-477b-ba8d-f0fb30db9667` | `https://data.gov.lv/dati/dataset/be841486-4af9-4d38-aa14-6502a2ddb517/resource/931e6299-61ba-477b-ba8d-f0fb30db9667/download/property.zip` |
| 2 | Īpašumtiesību statusi | 11.6 MB | `a0d801da-8eb0-4426-9087-50e8139bce39` | `https://data.gov.lv/dati/dataset/be841486-4af9-4d38-aa14-6502a2ddb517/resource/a0d801da-8eb0-4426-9087-50e8139bce39/download/ownership.zip` |
| 3 | Zemes vienības | 47.6 MB | `1618f19a-c818-4966-8183-a2e3c108597a` | `https://data.gov.lv/dati/dataset/be841486-4af9-4d38-aa14-6502a2ddb517/resource/1618f19a-c818-4966-8183-a2e3c108597a/download/parcel.zip` |
| 4 | Zemes vienību daļas | 526 KB | `58635c63-8c04-4193-a9f2-ec674c57ae93` | `https://data.gov.lv/dati/dataset/be841486-4af9-4d38-aa14-6502a2ddb517/resource/58635c63-8c04-4193-a9f2-ec674c57ae93/download/parcelpart.zip` |
| 5 | Būves | 196.2 MB | `9fe29b57-07cd-4458-b22c-b0b9f2bc8915` | `https://data.gov.lv/dati/dataset/be841486-4af9-4d38-aa14-6502a2ddb517/resource/9fe29b57-07cd-4458-b22c-b0b9f2bc8915/download/building.zip` |
| 6 | Telpu grupas | 57.6 MB | `5d8b1cfa-1e67-4b77-a6ac-b4e37eba0d7e` | `https://data.gov.lv/dati/dataset/be841486-4af9-4d38-aa14-6502a2ddb517/resource/5d8b1cfa-1e67-4b77-a6ac-b4e37eba0d7e/download/premisegroup.zip` |
| 7 | Adreses | 37.5 MB | `2aeea249-6948-4713-92c2-e01543ea0f33` | `https://data.gov.lv/dati/dataset/be841486-4af9-4d38-aa14-6502a2ddb517/resource/2aeea249-6948-4713-92c2-e01543ea0f33/download/address.zip` |
| 8 | Apgrūtinājumi | 52.0 MB | `ca8a415c-a894-427f-b14d-d1e44c582620` | `https://data.gov.lv/dati/dataset/be841486-4af9-4d38-aa14-6502a2ddb517/resource/ca8a415c-a894-427f-b14d-d1e44c582620/download/encumbrance.zip` |
| 9 | Atzīmes | 539 KB | `9417c9f2-5961-492d-8606-ca84a5b41386` | `https://data.gov.lv/dati/dataset/be841486-4af9-4d38-aa14-6502a2ddb517/resource/9417c9f2-5961-492d-8606-ca84a5b41386/download/mark.zip` |
| 10 | Kadastrālās vērtības | 145.6 MB | `35a2dbfa-e4b9-41d5-88d0-e1393115dcb1` | `https://data.gov.lv/dati/dataset/be841486-4af9-4d38-aa14-6502a2ddb517/resource/35a2dbfa-e4b9-41d5-88d0-e1393115dcb1/download/valuation.zip` |
| 11 | XSD shēmas | 22 KB | `dc113f7a-80a3-4e4c-8975-a8ac7424cdc7` | `https://data.gov.lv/dati/dataset/be841486-4af9-4d38-aa14-6502a2ddb517/resource/dc113f7a-80a3-4e4c-8975-a8ac7424cdc7/download/ad_xsdshemas_01012025.zip` |

---

## 11. Datu normalizācijas ieteikumi

### 11.1 SQLite datubāzes shēma

```sql
-- ============================================================
-- Nekustamie īpašumi
-- ============================================================
CREATE TABLE properties (
    cadastre_nr         TEXT PRIMARY KEY,  -- 11 cipari
    property_kind       TEXT NOT NULL,
    share_flat_property TEXT,
    property_name       TEXT,
    parcel_total_area   REAL,
    premise_group_total_area REAL,
    landbook_folio_nr   TEXT,
    landbook_folio_liter TEXT,
    landbook_office     TEXT,
    not_corroborated    TEXT
);

CREATE TABLE property_objects (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    property_cadastre_nr TEXT NOT NULL REFERENCES properties(cadastre_nr),
    object_kind         TEXT NOT NULL,
    object_cadastre_nr  TEXT NOT NULL,
    share_parts         INTEGER,
    nr_of_shares        INTEGER
);
CREATE INDEX idx_po_property ON property_objects(property_cadastre_nr);
CREATE INDEX idx_po_object ON property_objects(object_cadastre_nr);

-- ============================================================
-- Zemes vienības
-- ============================================================
CREATE TABLE parcels (
    cadastre_nr         TEXT PRIMARY KEY,  -- 11 cipari
    status_id           INTEGER,
    status_name         TEXT,
    varis_code          TEXT,              -- FK → VAR AW_EKA.KODS
    atvk_code           TEXT,
    area                REAL,
    liz_value           INTEGER,
    new_forest_area     REAL
);
CREATE INDEX idx_parcel_varis ON parcels(varis_code);
CREATE INDEX idx_parcel_atvk ON parcels(atvk_code);

CREATE TABLE parcel_land_purposes (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    parcel_cadastre_nr  TEXT NOT NULL REFERENCES parcels(cadastre_nr),
    purpose_id          TEXT,
    purpose_name        TEXT,
    purpose_area        REAL,
    agricult_total      REAL,
    areable             REAL,
    orchards            REAL,
    meadows             REAL,
    pastures            REAL,
    forest              REAL,
    bushes              REAL,
    swamp               REAL,
    under_water_total   REAL,
    under_fish_ponds    REAL,
    flooded             REAL,
    under_buildings     REAL,
    under_roads         REAL,
    other_land          REAL,
    drained             REAL
);
CREATE INDEX idx_plp_parcel ON parcel_land_purposes(parcel_cadastre_nr);

CREATE TABLE parcel_surveys (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    parcel_cadastre_nr  TEXT NOT NULL,
    survey_kind         TEXT,
    survey_date         TEXT
);
CREATE INDEX idx_ps_parcel ON parcel_surveys(parcel_cadastre_nr);

CREATE TABLE parcel_planned (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    parcel_cadastre_nr  TEXT NOT NULL,
    varis_code          TEXT,
    planned_cadastre_nr TEXT,
    planned_area        REAL
);
CREATE INDEX idx_ppl_parcel ON parcel_planned(parcel_cadastre_nr);
CREATE INDEX idx_ppl_planned ON parcel_planned(planned_cadastre_nr);

-- ============================================================
-- Zemes vienību daļas
-- ============================================================
CREATE TABLE parcel_parts (
    cadastre_nr         TEXT PRIMARY KEY,  -- 15 cipari
    parcel_cadastre_nr  TEXT NOT NULL,     -- FK → parcels
    area                REAL,
    liz_value           INTEGER
);
CREATE INDEX idx_pp_parcel ON parcel_parts(parcel_cadastre_nr);

CREATE TABLE parcel_part_land_purposes (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    parcel_part_cadastre_nr TEXT NOT NULL,
    purpose_id          TEXT,
    purpose_name        TEXT,
    purpose_area        REAL,
    agricult_total      REAL,
    areable             REAL,
    orchards            REAL,
    meadows             REAL,
    pastures            REAL,
    forest              REAL,
    bushes              REAL,
    swamp               REAL,
    under_water_total   REAL,
    under_fish_ponds    REAL,
    flooded             REAL,
    under_buildings     REAL,
    under_roads         REAL,
    other_land          REAL,
    drained             REAL
);
CREATE INDEX idx_pplp_part ON parcel_part_land_purposes(parcel_part_cadastre_nr);

-- ============================================================
-- Būves
-- ============================================================
CREATE TABLE buildings (
    cadastre_nr         TEXT PRIMARY KEY,  -- 14 cipari
    parcel_cadastre_nr  TEXT,              -- FK → parcels (no ObjectRelation)
    varis_code          TEXT,              -- FK → VAR AW_EKA.KODS
    name                TEXT,
    use_kind_id         TEXT,
    use_kind_name       TEXT,
    area                REAL,
    constr_area         REAL,
    ground_floors       INTEGER,
    underground_floors  INTEGER,
    material_id         TEXT,
    material_name       TEXT,
    preg_count          INTEGER,
    acception_years     TEXT,
    exploit_year        INTEGER,
    deprecation         TEXT,
    dep_val_date        TEXT,
    survey_date         TEXT,
    not_for_landbook    TEXT,
    prereg              TEXT,
    not_exist           TEXT,
    engineering_type    TEXT,
    -- Platību eksplikācija
    total_area          REAL,
    expedient_area      REAL,
    flat_total_area     REAL,
    flat_area           REAL,
    living_area         REAL,
    flat_aux_area       REAL,
    flat_outer_area     REAL,
    nonliving_total     REAL,
    nonliving_interior  REAL,
    nonliving_outer     REAL,
    shared_area         REAL,
    shared_interior     REAL,
    shared_outer        REAL,
    -- BuildingTypeData
    building_kind_id    TEXT,
    building_kind_name  TEXT,
    -- BuildingHistoricalData
    historical_liter    TEXT,
    historical_name     TEXT
);
CREATE INDEX idx_bldg_parcel ON buildings(parcel_cadastre_nr);
CREATE INDEX idx_bldg_varis ON buildings(varis_code);

CREATE TABLE building_parcels (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    building_cadastre_nr TEXT NOT NULL,
    parcel_cadastre_nr  TEXT NOT NULL
);
CREATE INDEX idx_bp_bldg ON building_parcels(building_cadastre_nr);
CREATE INDEX idx_bp_parcel ON building_parcels(parcel_cadastre_nr);

CREATE TABLE building_elements (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    building_cadastre_nr TEXT NOT NULL,
    element_name        TEXT,
    material_name       TEXT,
    exploit_year        INTEGER
);
CREATE INDEX idx_be_bldg ON building_elements(building_cadastre_nr);

CREATE TABLE building_amounts (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    building_cadastre_nr TEXT NOT NULL,
    amount_kind_name    TEXT,
    quantity            REAL,
    measure_kind_name   TEXT
);
CREATE INDEX idx_ba_bldg ON building_amounts(building_cadastre_nr);

-- ============================================================
-- Telpu grupas
-- ============================================================
CREATE TABLE premise_groups (
    cadastre_nr         TEXT PRIMARY KEY,  -- 17 cipari
    building_cadastre_nr TEXT NOT NULL,    -- FK → buildings
    name                TEXT,
    varis_code          TEXT,              -- FK → VAR AW_DZIV.KODS
    use_kind_id         TEXT,
    use_kind_name       TEXT,
    floor               INTEGER,
    premise_count       INTEGER,
    area                REAL,
    survey_date         TEXT,
    acception_years     TEXT,
    not_for_landbook    TEXT,
    -- Platību eksplikācija (tāda pati struktūra kā buildings)
    total_area          REAL,
    expedient_area      REAL,
    flat_total_area     REAL,
    flat_area           REAL,
    living_area         REAL,
    flat_aux_area       REAL,
    flat_outer_area     REAL,
    nonliving_total     REAL,
    nonliving_interior  REAL,
    nonliving_outer     REAL,
    shared_area         REAL,
    shared_interior     REAL,
    shared_outer        REAL
);
CREATE INDEX idx_pg_building ON premise_groups(building_cadastre_nr);
CREATE INDEX idx_pg_varis ON premise_groups(varis_code);

-- ============================================================
-- Adreses
-- ============================================================
CREATE TABLE addresses (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    object_cadastre_nr  TEXT NOT NULL,
    object_type         TEXT NOT NULL,
    ar_code             TEXT,              -- FK → VAR
    post_index          TEXT,
    town                TEXT,
    county              TEXT,
    parish              TEXT,
    village             TEXT,
    street              TEXT,
    house               TEXT,
    apartment           TEXT
);
CREATE INDEX idx_addr_object ON addresses(object_cadastre_nr, object_type);
CREATE INDEX idx_addr_ar ON addresses(ar_code);

-- ============================================================
-- Īpašumtiesības
-- ============================================================
CREATE TABLE ownerships (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    object_cadastre_nr  TEXT NOT NULL,
    object_type         TEXT NOT NULL,
    ownership_status    TEXT,
    person_status       TEXT
);
CREATE INDEX idx_own_object ON ownerships(object_cadastre_nr, object_type);

-- ============================================================
-- Apgrūtinājumi
-- ============================================================
CREATE TABLE encumbrances (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    object_cadastre_nr  TEXT NOT NULL,
    object_type         TEXT NOT NULL,
    kind_id             TEXT,
    kind_name           TEXT,
    encumbrance_nr      INTEGER,
    establish_date      TEXT,
    area                REAL,
    measure             TEXT
);
CREATE INDEX idx_enc_object ON encumbrances(object_cadastre_nr, object_type);

-- ============================================================
-- Atzīmes
-- ============================================================
CREATE TABLE marks (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    object_cadastre_nr  TEXT NOT NULL,
    object_type         TEXT NOT NULL,
    mark_type           TEXT,
    mark_date           TEXT,
    description         TEXT,
    area                REAL
);
CREATE INDEX idx_mark_object ON marks(object_cadastre_nr, object_type);

-- ============================================================
-- Kadastrālās vērtības
-- ============================================================
CREATE TABLE valuations (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    object_cadastre_nr  TEXT NOT NULL,
    object_type         TEXT NOT NULL,
    value_type          TEXT,
    property_valuation  REAL,
    property_val_date   TEXT,
    property_cadastral_value REAL,
    property_cad_val_date TEXT,
    object_cadastral_value REAL,
    object_cad_val_date TEXT,
    val_description     TEXT,
    forest_value        REAL,
    forest_value_date   TEXT
);
CREATE INDEX idx_val_object ON valuations(object_cadastre_nr, object_type);
```

### 11.2 ETL transformāciju kopsavilkums

```
XML parsēšanas secība:
1. Izpako ZIP arhīvu
2. Apstaigā visas .xml datnes direktorijā
3. Katram XML failam parsē ItemList elementus
4. Katram ItemData ierakstam izvelk laukus
5. Ielādē SQLite datubāzē

Īpaši gadījumi:
- Property: ObjectList ir saraksts → atsevišķa tabula property_objects
- Parcel: LandPurposeList → atsevišķa tabula parcel_land_purposes
- Building: BuildingOrPremiseGroupExplicationData → flatten uz kolonnām
- PremiseGroup: tāda pati eksplikācija kā Building
- Encumbrance: EncumbranceList → vairāki ieraksti vienam objektam
- Mark: MarkList → vairāki ieraksti vienam objektam
- Valuation: ValuationDataList → vairāki ieraksti vienam objektam
- Ownership: OwnershipStatusKindList → vairāki ieraksti vienam objektam
```

### 11.3 Datubāzes optimizācijas

#### 11.3.1 Tipu korekcijas

Seši lauki XSD shēmā definēti kā `xs:string`, `xs:normalizedString` vai `xs:gYear`, bet VZD datu kopā satur tikai veselas skaitliskas vērtības. SQLite shēmā tie mainīti uz `INTEGER`:

| Tabula | Kolonna | XSD tips | Faktiskais diapazons | SQLite tips |
|--------|---------|----------|----------------------|-------------|
| `parcels` | `liz_value` | xs:string | 0–95 | INTEGER |
| `parcel_parts` | `liz_value` | xs:string | 0–80 | INTEGER |
| `buildings` | `exploit_year` | xs:gYear | 1184–2026 | INTEGER |
| `building_elements` | `exploit_year` | xs:gYear | 1184–2026 | INTEGER |
| `premise_groups` | `floor` | xs:string | -1–9 | INTEGER |
| `encumbrances` | `encumbrance_nr` | xs:normalizedString | 0–99 | INTEGER |

**Pamatojums:** Faktiskie dati ir pārāki par XSD shēmu — datu kvalitātes analīze apliecina, ka šie lauki satur tikai veselus skaitļus. INTEGER tips nodrošina pareizu kārtošanu un aritmētiskās operācijas.

#### 11.3.2 Noņemtās kolonnas

Četras kolonnas eksistē XSD shēmā, bet VZD datu kopā to vērtības ir 100% NULL:

| Tabula | Kolonna | Iemesls |
|--------|---------|---------|
| `properties` | `atvk` | VZD nepublicē ATVK kodu īpašumu līmenī (1.5M rindu, visas NULL) |
| `building_elements` | `material_id` | VZD lieto tikai `material_name` (4.4M rindu, visas NULL) |
| `building_amounts` | `amount_kind_id` | VZD lieto tikai `amount_kind_name` (3.4M rindu, visas NULL) |
| `building_amounts` | `measure_kind_id` | VZD lieto tikai `measure_kind_name` (3.4M rindu, visas NULL) |

#### 11.3.3 Salikti indeksi

Piecas polimorfās tabulas (`addresses`, `ownerships`, `encumbrances`, `marks`, `valuations`) satur `object_cadastre_nr` un `object_type` kolonnas. Vaicājumi gandrīz vienmēr filtrē pēc abām kolonnām:

```sql
WHERE object_cadastre_nr = ? AND object_type = ?
```

Vienas kolonnas indekss aizvietots ar salikto `(object_cadastre_nr, object_type)`. Saliktais indekss joprojām atbalsta vaicājumus tikai pēc `object_cadastre_nr` (kā pirmā kolonna), tāpēc esošie vaicājumi netiek sabojāti.

Pievienoti arī jauni indeksi:
- `idx_bp_parcel ON building_parcels(parcel_cadastre_nr)` — reversais lookup
- `idx_ppl_planned ON parcel_planned(planned_cadastre_nr)` — reversais lookup

---

## Atsauces

| Resurss | URL |
|---------|-----|
| **Datu portāls** | https://data.gov.lv/dati/lv/dataset/kadastra-informacijas-sistemas-atvertie-dati |
| **VZD specifikācija** | https://www.vzd.gov.lv/lv/kadastra-teksta-datu-atversana |
| **XSD shēmas** | https://www.vzd.gov.lv/lv/media/9293/download?attachment |
| **PDF specifikācija** | https://www.vzd.gov.lv/lv/media/9290/download?attachment |
| **VAR dati** | https://data.gov.lv/dati/dataset/varis-atvertie-dati |
| **VZD kontakts** | dati@vzd.gov.lv |

---

*Dokuments sagatavots: 2026-02-23*
*Pamatots uz VZD specifikāciju v0.12 (14.10.2025) un data.gov.lv CKAN API datiem*
