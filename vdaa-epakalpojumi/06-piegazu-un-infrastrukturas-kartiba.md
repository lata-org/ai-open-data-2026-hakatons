# 6. Piegāžu un infrastruktūras kārtība (CI/CD un drošība)

Šis dokuments nosaka prasības un procedūras, kādā veidā tiek piegādāti programmatūras laidieni uzstādīšanai Valsts digitālās attīstības aģentūras (VDAA) tehniskajā infrastruktūrā.

---

## 6.1. VDAA piegāžu infrastruktūras komponentes

Piegāžu procesa nodrošināšanai VDAA uztur centralizētu izstrādes un izvietošanas vidi:
- **Git serveris**: Pirmkoda versiju vadībai un dokumentācijai.
- **Nexus serveris**: Izpildkoda, konteineru (Docker) tēlu un bibliotēku artifaktu krātuve.
- **Jenkins serveris**: Automatizētās būvēšanas un izvietošanas (CI/CD) rīks.
- **PAM (Privileged Access Management)**: Droša administratīvā piekļuve testa vides serveriem un resursiem.
- **Kubernetes klasteris**: Konteineru izpildes vide testa un produkcijas zonās.

---

## 6.2. Piekļuves tiesību saņemšana un kontu drošības prasības

### Pieteikšanās kārtība
1. Organizācijas pilnvarots pārstāvis (līguma parakstītājs vai kontaktpersona) nosūta elektroniski parakstītu **"Veidlapu tiesību pieprasīšanai Aģentūras piegāžu infrastruktūrai"** (`cicd_piekluves_veidlapa_vraa_1.docx`) uz **VDAA e-adresi**.
2. Pēc apstiprināšanas:
   - Serveru adreses un lietotājvārds tiek nosūtīti uz veidlapā norādīto **e-pastu**;
   - Sākotnējā parole tiek nosūtīta uz lietotāja **mobilo tālruni (ar SMS)**.

### Kritiskie drošības noteikumi kontiem
- **Obligāts 2FA Git serverim**: Pēc Git piekļuves saņemšanas lietotājam **nekavējoties jāieslēdz divfaktoru autentifikācija (2FA)**. Lietotāji bez 2FA tiek bloķēti.
- **6 mēnešu neaktivitāte**: Ja lietotājs 6 mēnešu laikā nepieslēdzas VDAA resursiem, piekļuves tiesības tiek automātiski anulētas.
- **Regulāra piekļuvju revīzija**: Ik pēc 6 mēnešiem VDAA nosūta paziņojumu ar aicinājumu apstiprināt piekļuves nepieciešamību. Ja lietotājs noteiktajā termiņā nesniedz atbildi, konts tiek dzēsts.

---

## 6.3. Piegādes pieteikšanas un noformēšanas kārtība

Kad programmatūras laidiens ir sagatavots un pārbaudīts piegādātāja pusē, tiek veikta piegādes pieteikšana:

### Saziņas kanāli:
- **JIRA**: Ja organizācijai ir spēkā esošs izstrādes līgums ar VDAA.
- **E-pasts uz `piegades@vdaa.gov.lv`**: Ja iestāde piegādā savā pārziņā esošu e-pakalpojumu.
  - *Obligātā kopija*: Jāadresē e-pakalpojuma pārzinim (iestādei) un VDAA atbildīgajai kontaktpersonai.
  - *E-pasta temats*: Obligāti jānorāda sistēmas/e-pakalpojuma nosaukums un identifikators (piemēram: `[EP042] Laidiens v1.2.0 uzstādīšanai testa vidē`).

### Obligātā informācija pieteikumā:
1. Sistēmas un komponentes nosaukums, piegādes ID un versija.
2. Piegādes novietne (konkrēta Git filiāle/tags un Nexus mapes ceļš).
3. Projekta vai līguma numurs.
4. Piegādes veids (jauna versija vai kļūdu labojums).
5. Funkcionālo izmaiņu īss kopsavilkums (*Release notes*).
6. VDAA kontaktpersonas vārds un uzvārds.

---

## 6.4. Piegādes pakotnes obligātais saturs

Programmatūras laidiena piegādei jāsatur:
1. **Instalācijas pakotne / Docker tēls** (Nexus serverī atbilstošajā mapē).
2. **Pirmkods** (Git serverī atbilstošajā repozitorijā un tagā).
3. **Uzstādīšanas instrukcija** (Markdown formātā Git serverī):
   - Laidiena numurs, izdošanas datums un izmaiņu vēsture;
   - Konfigurācijas failu un vides mainīgo (*Environment variables*) izmaiņas;
   - Datubāzes migrācijas skripti (ja attiecināms).
4. **Izmaiņu un uzlabojumu apraksts** (funkcionālais apraksts un risinātie pieteikumi).
5. **Saistīto komponenšu un bibliotēku versiju saraksts**.
6. **Testēšanas dokumentācija**:
   - Testēšanas scenāriji;
   - Testēšanas izpildes protokols (apliecinājums par sekmīgiem testiem pirms nodošanas).
7. **Pirmajai piegādei**: Aizpildīts `EpakalpojumaAprakstsSablons.xlsx`.

> [!WARNING]
> **Piegādes noraidīšana:**
> VDAA ir tiesīga piegādi nekavējoties noraidīt, ja:
> - Trūkst kāda no obligātajiem metadatiem vai dokumentiem;
> - Drošības pārbaudēs (statiskā koda analīze, konteineru skenēšana) tiek atklātas kritiski augstas drošības ievainojamības (*CVE vulnerabilities*).

---

## 6.5. Izvietošanas (Deployment) un CI/CD noteikumi

> [!CAUTION]
> **Jenkins darbu palaišanas aizliegums:**
> Izstrādātājiem ir **KATEGORISKI AIZLIEGTS** patstāvīgi palaist Jenkins uzstādīšanas darbus (*Deploy Jobs*).
> Izvietošanu testa un produkcijas klasterī veic **tikai VDAA administratoru komanda** pēc oficiāla pieteikuma apstrādes!

### Izvietošanas izpildes termiņi (SLA):
- Piegādes uzstādīšana **testa vidē**: **10 darbdienu laikā** no korekta pieteikuma reģistrācijas.
- Piegādes uzstādīšana **produkcijas vidē**: **10 darbdienu laikā** pēc Akcepttestēšanas akta abpusējas parakstīšanas un gala pieprasījuma saņemšanas.

---

## 6.6. Piekļuve tehniskajiem resursiem caur PAM

Ja izstrādes vai incidentu risināšanas gaitā nepieciešama tieša piekļuve VDAA testa vides serveriem, datubāzēm vai konteineriem:
- Piekļuve tiek nodrošināta caur **PAM** (*Privileged Access Management*) risinājumu ar obligātu 2FA.
- **Tehniskā prasība klientam**: Darbstacija ar **Windows operētājsistēmu** un jaunāko pārlūkprogrammas versiju.
- Visas darbības PAM sesijas laikā tiek auditētas un video ierakstītas.
