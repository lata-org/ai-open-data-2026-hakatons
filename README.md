# VARAM un LATA atvērto datu un mākslīgā intelekta hakatons 2026: starta komplekts

Šis repozitorijs ir starta komplekts komandām, kas piedalās Viedās administrācijas un reģionālās attīstības ministrijas (VARAM) un Latvijas Atvērto tehnoloģiju asociācijas (LATA) rīkotajā atvērto datu un mākslīgā intelekta hakatonā 2026. gada 9. un 10. oktobrī Latvijas Universitātes Akadēmiskajā centrā Torņakalnā.

Hakatona mērķis ir parādīt, ko var paveikt, apvienojot Latvijas atvērtos datus ar mūsdienu MI aģentu rīkiem, un atstāt aiz sevis publicētus prototipus, kurus var attīstīt tālāk. Komplekts ir sagatavots tā, lai komanda nesāktu no tukšas lapas: dati jau ir savākti un sakārtoti, prasības jau ir aprakstītas, un MI aģents tās var izlasīt un lietot uzreiz.

## Divi darba virzieni un divas mapes

| Virziens | Mape | Kas tajā ir |
|---|---|---|
| **Krīzes pārvaldība** | [`ca-plani-hakatons/`](ca-plani-hakatons/) | Visu 42 pašvaldību civilās aizsardzības plāni Markdown formātā, atvērto datu katalogs (adrešu reģistrs, kadastrs, ceļu tīkls, patvertnes), datubāzu shēmas, ielādes skripti, lokālie datu faili un vietnes prototips plānu salīdzināšanai. |
| **E-pakalpojumu prototipi** | [`vdaa-epakalpojumi/`](vdaa-epakalpojumi/) | Valsts digitālās attīstības aģentūras (VDAA) vadlīnijas e-pakalpojumu veidošanai Latvija.gov.lv portālā: 15 e-pakalpojumu baušļi, UX un UI principi, tehniskā arhitektūra, jaunais dizains, atbilstības audita kontrolsaraksts un gatavs MI aģenta prasmju fails. |

Abas mapes var lietot kopā. Piemēram, vētras zaudējumu pieteikums pašvaldībai ir e-pakalpojums, kas ņem adresi no adrešu reģistra, īpašumu no kadastra un patvertņu vai evakuācijas vietu datus no civilās aizsardzības plāna.

## Kā lietot ar MI aģentu

Hakatonā komandas strādā ar MI aģentu rīkiem, piemēram, Claude Code, Codex vai Gemini un Antigravity. Komanda apraksta problēmu un pakalpojumu vienkāršā valodā, aģents raksta un izpilda kodu. Komplekts ir veidots tieši šādam darbam.

1. **Klonē repozitoriju** vai lejupielādē to kā ZIP arhīvu un atver aģenta rīkā kā projektu.

   ```bash
   git clone https://github.com/lata-org/ai-open-data-2026-hakatons.git
   ```

2. **Pieslēdz prasmju failus.** Abās mapēs ir `SKILL.md` fails, ko aģents var ielādēt kā prasmi: `vdaa-epakalpojumi/SKILL.md` iemāca aģentam VDAA prasības, `ca-plani-hakatons/avoti/celu-tikls/SKILL.md` iemāca darbu ar ceļu tīkla datiem. Claude Code gadījumā mapi var nokopēt uz `.claude/skills/`, citos rīkos pietiek, ja aģentam liek izlasīt failu.

3. **Sāc ar sarunu par datiem.** Pirms būvēšanas pajautā aģentam, kas komplektā ir pieejams un ko no tā var uzbūvēt. Piemēri jautājumiem:

   - "Izlasi ca-plani-hakatons/README.md un pasaki, kādi dati ir par Ogres novadu."
   - "Kuras pašvaldības plānos nav norādītas evakuācijas vietas ar adresēm?"
   - "Uzprojektē vētras zaudējumu pieteikuma pakalpojumu pēc vdaa-epakalpojumi/SKILL.md principiem 4 soļos."

4. **Būvē lokāli, tad publicē.** Viens uzdevums aģentam aizņem 5 līdz 10 minūtes, rezultāts vienmēr jāpārbauda. Sestdien komanda nodod publicētu prototipu vai maketu, 10 minūšu prezentāciju un skaidru atbildi, kas ir lietotājs un kā viņu sasniegs.

## Vērtēšanas kritēriji

Abām trasēm, gan būvētājiem ar darbojošos prototipu, gan projektētājiem ar klikšķināmu maketu, kritēriji ir vienādi un balstīti VDAA pakalpojumu veidošanas principos.

1. **Konkrēts rezultāts.** Lietotājs saņem lēmumu, statusu vai reģistrāciju, ne tikai "paldies".
2. **Tikai vienreiz.** Neprasa to, kas jau ir reģistros vai atvērtajos datos. Katrs izmantotais datu avots ir pluss.
3. **Plūsma.** 3 līdz 6 soļi, kopsavilkums pirms iesniegšanas un skaidrs noslēgums ar norādi, kas sekos.
4. **Darbojas.** Prototips ir publicēts, lietojams telefonā un bez strupceļiem.
5. **MI un dati.** Ir skaidrs, kā MI izmantots izstrādē vai pašā produktā un kuras atvērto datu kopas izmantotas.

Pilns kontrolsaraksts e-pakalpojuma pārbaudei ir `vdaa-epakalpojumi/07-atbilstibas-audita-kontrolsaraksts.md`.

## Ideju piemēri

- Vētras zaudējumu pieteikums pašvaldībai: adrese no adrešu reģistra, īpašums no kadastra, jāpievieno tikai foto un apraksts.
- "Kur ir gaisma, ūdens un sakari": pēc adreses redzams statuss un tuvākie darbojošies punkti.
- Ziņojums par kritušu koku vai slēgtu ceļu, kur MI nosaka atbildīgo iestādi un apvieno dublikātus.
- Mājsaimniecības gatavības pase: pēc adreses personalizēts risku un 72 stundu sagatavotības saraksts.
- Pašvaldības krīzes panelis: kur elektrības nav ilgāk par diennakti, kur ir riska grupas, kā prioritizēt palīdzību.
- Visu pašvaldību civilās aizsardzības plānu salīdzinājums un vizualizācija ar atvērto datu kartēm.
- Esoša Latvija.gov.lv pakalpojuma pārbūve pēc jaunajiem principiem.

Komanda var izvēlēties kādu no šiem vai piedāvāt savu ideju.

## Datu avoti un lietošanas nosacījumi

- Civilās aizsardzības plāni ir pašvaldību publicētas publiskās versijas. Konvertēšana uz Markdown var saturēt kļūdas, noteicošais ir oriģināls, uz kuru norāda `ca-plani-hakatons/originali/<slug>/AVOTS.md`.
- Adrešu reģistrs un kadastrs: Valsts zemes dienests, data.gov.lv, licence CC BY 4.0.
- Ceļu tīkls un reāllaika plūsmas: VSIA Latvijas Valsts ceļi, transportdata.gov.lv.
- Patvertnes: VUGD un Iekšlietu ministrijas Informācijas centrs, 112.lv.
- VDAA vadlīnijas: vdaa.gov.lv sadaļa par e-pakalpojuma izmitināšanu.

Komplekta materiāli tapuši ar MI aģentu palīdzību 2026. gada vasarā un septembrī. Hakatona prototipi tiks publicēti atvērtā repozitorijā un būs pieejami pēc pasākuma.

## Kontakti

Pēteris Jurčenko, LATA valdes priekšsēdētājs, peteris.jurcenko@lata.org.lv
