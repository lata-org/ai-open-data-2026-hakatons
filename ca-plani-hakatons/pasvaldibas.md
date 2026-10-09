# Latvijas pašvaldības un to mājas lapas

Stāvoklis uz **2026-09-11**. Kopā **42 pašvaldības**: 7 valstspilsētas + 35 novadi.

Avots sarakstam: VZD Valsts adrešu reģistra atvērtie dati (data.gov.lv) — `avoti/aw_novads.csv` un
`avoti/aw_pilseta.csv` (ieraksti ar `STATUSS = EKS`). Mājas lapas pārbaudītas 2026-09-11, sekojot
pāradresācijām līdz gala adresei. Mašīnlasāma versija: `pasvaldibas.csv`.

## Valstspilsētas (7 patstāvīgas pašvaldības)

| Pašvaldība | ATVK | Mājas lapa |
|---|---|---|
| Rīga | 0001000 | https://www.riga.lv |
| Daugavpils | 0002000 | https://daugavpils.lv |
| Jelgava | 0003000 | https://www.jelgava.lv |
| Jūrmala | 0004000 | https://www.jurmala.lv |
| Liepāja | 0005000 | https://www.liepaja.lv |
| Rēzekne | 0006000 | https://rezekne.lv |
| Ventspils | 0007000 | https://www.ventspils.lv |

Vēl trīs pilsētām ir valstspilsētas statuss, bet tās **nav** atsevišķas pašvaldības — ietilpst novadā:
Jēkabpils (Jēkabpils novads), Ogre (Ogres novads), Valmiera (Valmieras novads).

## Novadi (35)

| Pašvaldība | ATVK | Mājas lapa | Piezīmes |
|---|---|---|---|
| Aizkraukles novads | 0020000 | https://www.aizkraukle.lv | |
| Alūksnes novads | 0021000 | https://aluksne.lv | |
| Augšdaugavas novads | 0022000 | https://www.augsdaugavasnovads.lv | |
| Ādažu novads | 0023000 | https://www.adazunovads.lv | adazi.lv pāradresē šeit |
| Balvu novads | 0024000 | https://www.balvi.lv | |
| Bauskas novads | 0025000 | https://www.bauskasnovads.lv | vecais bauska.lv pāradresē šeit; tā sertifikāts beidzies 2026-09-05 |
| Cēsu novads | 0026000 | https://www.cesis.lv | cesunovads.lv pāradresē šeit |
| Dienvidkurzemes novads | 0027000 | https://www.dkn.lv | |
| Dobeles novads | 0028000 | https://www.dobele.lv | |
| Gulbenes novads | 0029000 | https://www.gulbene.lv | |
| Jelgavas novads | 0030000 | https://www.jelgavasnovads.lv | |
| Jēkabpils novads | 0031000 | https://www.jekabpils.lv | ietver valstspilsētu Jēkabpils |
| Krāslavas novads | 0032000 | https://www.kraslava.lv | |
| Kuldīgas novads | 0033000 | https://kuldigasnovads.lv | vecais kuldiga.lv atgriež 404 |
| Ķekavas novads | 0034000 | https://kekava.lv | kekavasnovads.lv pāradresē šeit |
| Limbažu novads | 0035000 | https://www.limbazunovads.lv | |
| Līvānu novads | 0036000 | https://www.livani.lv | |
| Ludzas novads | 0037000 | https://www.ludzasnovads.lv | |
| Madonas novads | 0038001 | https://madona.lv | no 2025-07-01 ietver bijušo Varakļānu novadu |
| Mārupes novads | 0039000 | https://www.marupe.lv | |
| Ogres novads | 0040000 | https://www.ogresnovads.lv | ietver valstspilsētu Ogre |
| Olaines novads | 0041000 | https://olaine.lv | |
| Preiļu novads | 0042000 | https://www.preili.lv | |
| Rēzeknes novads | 0043000 | https://rezeknesnovads.lv | |
| Ropažu novads | 0044000 | https://www.ropazi.lv | |
| Salaspils novads | 0045000 | https://salaspils.lv | |
| Saldus novads | 0046000 | https://www.saldus.lv | |
| Saulkrastu novads | 0047000 | https://saulkrasti.lv | |
| Siguldas novads | 0048000 | https://sigulda.lv | |
| Smiltenes novads | 0049000 | https://www.smiltenesnovads.lv | |
| Talsu novads | 0051000 | https://www.talsunovads.lv | talsi.lv ir tikai pāradresācijas lapa |
| Tukuma novads | 0052000 | https://www.tukums.lv | |
| Valkas novads | 0053000 | https://www.valka.lv | |
| Valmieras novads | 0054000 | https://www.valmierasnovads.lv | ietver valstspilsētu Valmiera |
| Ventspils novads | 0056000 | https://www.ventspilsnovads.lv | |

## Metodika

1. No `aw_novads.csv` ņemti visi ieraksti ar `STATUSS = EKS` (35 novadi). Varakļānu novads reģistrā
   slēgts 2025-06-30 (`DAT_BEIG`), pievienots Madonas novadam.
2. No `aw_pilseta.csv` ņemtas pilsētas, kas pakļautas tieši valstij (`VKUR_TIPS = 101`) — 7 valstspilsētas.
3. Katrs domēns pārbaudīts ar HTTP pieprasījumu (sekojot pāradresācijām), nolasīts gala URL un lapas
   virsraksts. Papildus pārbaudīti alternatīvie `*novads.lv` domēni, lai atklātu domēna maiņas.
