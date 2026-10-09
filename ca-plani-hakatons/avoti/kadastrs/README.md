# Kadastra un adrešu datu datubāze

SQLite datubāze `dati/kadastrs.db`, uzbūvēta pēc `VAR_ATVERTIE_DATI_MODELIS.md` un
`NIVKIS_ATVERTIE_DATI_MODELIS.md` aprakstiem. Paredzēta regulārai adrešu reģistra
datu atjaunināšanai — VZD publicē VAR teksta datus **katru dienu**.

## Lietošana

```bash
# aktuālie + vēsturiskie adrešu reģistra dati (~680 MB lejupielāde, ~4,5 M rindas)
uv run --no-project --with httpx --with certifi atjaunot.py

# stāvokļa pārskats — kas ielādēts un kad
uv run --no-project --with httpx --with certifi atjaunot.py --statuss

# atsevišķi faili
uv run --no-project --with httpx --with certifi atjaunot.py --tikai aw_eka.csv,aw_iela.csv

# papildu iespējas
uv run --no-project --with httpx --with certifi atjaunot.py --bez-vestures  # tikai aktuālie (~290 MB)
uv run --no-project --with httpx --with certifi atjaunot.py --dokumenti     # dokumenti, ~220 MB
uv run --no-project --with httpx --with certifi atjaunot.py --nivkis        # kadastrs, ~620 MB
```

Vēsturiskie faili (`aw_*_his.csv` → tabula `aw_vesture`) ielādējas **pēc noklusējuma**, jo
ģeokodēšanai tie ir obligāti: cilvēku deklarētajās adresēs regulāri figurē pārdēvētas ielas
un vecie pieraksti (skatīt `../geocode/API_KONCEPTS.md`). Adreses kods ir nemainīgs visu
objekta mūžu, tāpēc vēsturiskais pieraksts ir tieša atslēga uz aktuālo objektu.

## Kā darbojas atjaunināšana

Skripts ir droši palaižams atkārtoti — arī katru dienu no plānotāja:

1. **Lejupielāde ir atomiska.** Fails vispirms nonāk `.daljejs` pagaidu vārdā un tikai pēc
   pilnīgas saņemšanas tiek pārsaukts. Pārtraukts palaidums neatstāj bojātu failu.
2. **Nemainīgie faili netiek pārlādēti.** Katram failam glabājas SHA-256 jaucējsumma tabulā
   `avota_fails`. Ja avots nav mainījies, ielāde tiek izlaista (`--piespiest` to apiet).
3. **Ielāde ir transakcijā.** Vecais tabulas saturs tiek dzēsts un jaunais ielikts vienā
   transakcijā. Ja parsēšana pusceļā neizdodas, notiek `ROLLBACK` un datubāzē paliek
   iepriekšējie dati — nekad puse veco, puse jauno.
4. **Kolonnas kartējas pēc nosaukuma, ne pēc secības.** Ja VZD maina kolonnu secību, ielāde
   turpina strādāt; ja parādās nezināma kolonna, skripts to izdrukā kā brīdinājumu.
5. **Katrs palaidums tiek žurnalēts** tabulā `atjauninajums`.

Vēsturiskie (`aw_vesture`) un dokumentu (`aw_doc`) faili ielādējas kopīgās tabulās, tāpēc tiem
tiek dzēsts tikai attiecīgā avota faila apakškopums, nevis visa tabula.

## Kas ielādēts

| Tabula | Rindas |
|---|---:|
| `aw_vesture` | 2 968 091 |
| `aw_dziv` | 964 464 |
| `aw_eka` | 610 050 |
| `aw_ppils` | 49 018 |
| `aw_iela` | 20 648 |
| `aw_ciems` | 10 958 |
| `aw_vietu_centroidi` | 6 903 |
| `aw_pagasts` | 530 |
| `aw_novads` | 146 |
| `aw_pilseta` | 84 |
| `aw_rajons` | 26 |
| `marks` (NĪVKIS) | 45 039 |
| `parcel_parts`, `parcel_part_land_purposes` (NĪVKIS) | 12 375 / 12 793 |

Pārējās NĪVKIS tabulas ir izveidotas, bet tukšas — ielādē ar `--nivkis`.

## Skats `v_adrese`

Aktuālās ēku adreses ar koordinātēm un izšķirtu hierarhiju (iela → ciems → pagasts/pilsēta →
novads). Aptver visas 550 109 aktīvās (`statuss='EKS'`) ēkas.

```sql
SELECT kods, adrese, lat, lon FROM v_adrese WHERE novads = 'Ogres nov.';   -- 21 276 ēkas
SELECT * FROM v_adrese WHERE adrese LIKE 'Zinību iela 3, Ogre%';
```

Valstspilsētām (Rīga, Liepāja u. c.) `novads` ir NULL — tās ir tieši LR pakļautībā, nevis
novadā. Tas nav trūkums, bet administratīvā iedalījuma īpatnība.

## Skats `v_adrese_vesture`

Vēsturiskais adreses pieraksts → tas pats objekts šodien. Katra `aw_vesture` rinda ir
iepriekšēja objekta pieraksta versija ar to pašu nemainīgo kodu un `dat_beig` (spēkā līdz);
skats piekabina aktuālo pierakstu no attiecīgās tabulas pēc `tips_cd`.

```sql
-- kā tagad sauc adresi, kas agrāk bija Celmlaužu iela 1 Ciemupē?
SELECT vecais_std, speka_lidz, kods, aktualais_std
FROM v_adrese_vesture WHERE vecais_std LIKE 'Celmlaužu iela 1,%';
-- Celmlaužu iela 1, Ciemupe, ... | 2026.03.30 | 102622041 | Rītausmas iela 1, Ciemupe, ...

-- visa viena objekta pieraksta vēsture
SELECT vecais_std, speka_lidz FROM v_adrese_vesture WHERE kods = '100377943'
ORDER BY speka_lidz;
```

`aktualais_std` ir NULL, ja objekts aktuālajos datos vairs neeksistē (likvidēts un izņemts).
Vienam vaicājuma tekstam vēsturē var atbilst vairākas versijas — jāņem jaunākā
(`MAX(speka_lidz)`). Ģeokodēšanas lietojums un reģiona saskaņotības noteikums aprakstīts
`../geocode/API_KONCEPTS.md`.

## Atkāpes no modeļa aprakstiem

Divas vietas, kur reālie dati nesakrīt ar dokumentāciju:

1. **`aw_vietu_centroidi.KODS` nav unikāls.** `VAR_ATVERTIE_DATI_MODELIS.md` 12.1. sadaļā tas
   deklarēts kā `PRIMARY KEY`, bet failā 6903 rindās ir tikai 6880 unikālu kodu — 18 objektiem
   ir vairāki centroīdi (piem., Zebrenes pag. un Lažas pag., kuru teritorija sastāv no
   nesavienotām daļām). Shēmā ielikta surogātatslēga `id` un indekss uz `kods`.
2. **Kolonnu secība `aw_eka.csv` atšķiras.** Modelī norādīts `... DD_E, DD_N`, faktiskajā failā
   ir `... DD_N, DD_E`. Tā kā ielāde kartē pēc nosaukuma, tas neietekmē rezultātu, bet, ielādējot
   pēc pozīcijas, platums un garums samainītos vietām.

Pārējais sakrīt: modelis brīdina par iespējamu `STATUSS`/`STATUS` neatbilstību, taču visos
faktiskajos CSV failos ir `STATUSS` ar diviem S, kā shēmā.

## NĪVKIS XML nianse

Kadastra XML lieto noklusēto nosaukumvietu
(`xmlns="http://ivis.eps.gov.lv/XMLSchemas/100007/CadastreRegistry/v1-0"`), tāpēc
ElementTree tagi ir `{ns}Tag` un `find("ObjectRelation")` neatrod neko. Ielādētājs pirms
apstrādes nosaukumvietu nostrip'o (`bez_nosaukumvietas()`). Bez tā tabulas ielādētos tukšas,
skriptam ziņojot par apstrādātiem ierakstiem.

Modeļa aprakstā nav minēts `ImprovementItemData` (labiekārtojumi), kas sastopams
`building.zip` — tam shēmā tabulas nav.

## Faili

| Fails | Saturs |
|---|---|
| `shema.sql` | pilna shēma — VAR + NĪVKIS + atjaunināšanas uzskaite + skati |
| `atjaunot.py` | lejupielāde un ielāde |
| `dati/kadastrs.db` | datubāze |
| `dati/lejupielades/` | lejupielādētie avota faili (kešs jaucējsummu salīdzināšanai) |

## Sasaiste ar pārējiem projekta datiem

`aw_eka.kods` ir tas pats VZD adreses kods, kas PPI datubāzē
(`../publisko-personu-saraksts/dati/ppi.db`, kolonna `iestades.adreses_kods`), un uz to norāda
arī NĪVKIS `VARISCode`/`ARCode`. Tas dod ceļu no izglītības iestādes uz koordinātēm:

```sql
ATTACH '../publisko-personu-saraksts/dati/ppi.db' AS ppi;
SELECT p.nosaukums, a.adrese, a.lat, a.lon
FROM ppi.iestades p JOIN v_adrese a ON a.kods = p.adreses_kods
WHERE p.statuss = 'REGISTERED';
```
