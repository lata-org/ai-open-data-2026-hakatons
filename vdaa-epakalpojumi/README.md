# VDAA E-pakalpojumu izstrādes, prasību un izmitināšanas zināšanu bāze

Šī zināšanu bāze ir izveidota, balstoties uz **Valsts digitālās attīstības aģentūras (VDAA)** oficiālajām vadlīnijām, standartiem un sadarbības procedūrām e-pakalpojumu izstrādei un izmitināšanai vienotajā valsts pārvaldes pakalpojumu portālā **[Latvija.gov.lv](https://latvija.gov.lv)** (avots: [vdaa.gov.lv/lv/e-pakalpojuma-izmitinasana](https://www.vdaa.gov.lv/lv/e-pakalpojuma-izmitinasana)).

Šīs zināšanu bāzes materiāli ir strukturēti tā, lai no tiem varētu automātiski darbināt vai ģenerēt Antigravity AI aģenta prasmju failu (**`SKILL.md`**), kā arī izmantot iestāžu vadītājiem, arhitektiem, izstrādātājiem un kvalitātes testētājiem.

---

## 📁 Zināšanu bāzes satura rādītājs

| Fails | Tēma un apraksts |
| :--- | :--- |
| **[01-tiesiskais-ietvars-un-atbildiba.md](./01-tiesiskais-ietvars-un-atbildiba.md)** | Tiesiskais regulējums (MK 402, Valsts informācijas sistēmu likums, MK 445, eIDAS) un VDAA / Iestādes / Izstrādātāja atbildības matrica. |
| **[02-bausli-un-ux-ui-vadlinijas.md](./02-bausli-un-ux-ui-vadlinijas.md)** | Oficiālie 15 e-pakalpojumu izveides baušļi ("Viegli lasīt"), cilvēkorientēta dizaina principi, *Mobile-first*, 90% plūsmas likums un datu minimizēšana. |
| **[03-dzivescikls-un-sadarbibas-procedura.md](./03-dzivescikls-un-sadarbibas-procedura.md)** | E-pakalpojumu ieviešanas 4 soļu procedūra: 1. Pieteikšanās un reģistrēšana -> 2. Izstrāde un nodevumi -> 3. Akcepttestēšana un demonstrācija -> 4. Uzstādīšana un uzturēšana produkcijā (gada noilguma limits). |
| **[04-tehniska-arhitektura-un-koplietosana.md](./04-tehniska-arhitektura-un-koplietosana.md)** | 4 platformas zonas (`epak-public`, Sistēmas zona, Iekšējā zona, VISS), Linux Docker/Kubernetes, BFF šablons, OIDC / PFAS talonu apmaiņa, URN shēmas (RFC 4619), EDK, Maksājumi, AMK, ClamAV un SLA (≤3s, ≤4MB). |
| **[05-jaunais-dizains-un-frontend-standarti.md](./05-jaunais-dizains-un-frontend-standarti.md)** | **Kritiskais pārejas termiņš: oranžais dizains beidzas 2027. gada 30. jūnijā.** Jaunais vienotais dizains, SPA (ReactJS) un MPA (.NET Core MVC) Storybook bāzes, WCAG 2.1 AA piekļūstamība. |
| **[06-piegazu-un-infrastrukturas-kartiba.md](./06-piegazu-un-infrastrukturas-kartiba.md)** | CI/CD kārtība: Git, Nexus, Jenkins, **stingrs aizliegums pašiem palaist Deploy jobs**, 2FA obligātums Git kontiem, PAM piekļuve ar 2FA no Windows darbstacijas, piegāžu noraidīšanas kritēriji. |
| **[07-atbilstibas-audita-kontrolsaraksts.md](./07-atbilstibas-audita-kontrolsaraksts.md)** | Oficiālais VDAA atbilstības audita kontrolsaraksts: Bloks A līdz Bloks K (Bizness, Soļi, Saturs, UI izvēle, UI organizācija, Tehniskā puse, Arhitektūra, Veiktspēja, Drošība, VIRSIS, Atsauksmes). |
| **[SKILL.md](./SKILL.md)** | **Gatavs AI aģenta prasmju fails**, ko var iekļaut Antigravity vai citās aģentu platformās profesionālam atbalstam e-pakalpojumu plānošanā, auditā un izstrādē. |

---

## 📌 Svarīgākie kritiskie noteikumi (Quick Highlights)

> [!IMPORTANT]
> 1. **Dizaina modernizācija un termiņš**: Pašreizējais (oranžais) dizains tiks atbalstīts tikai līdz **2027. gada 30. jūnijam**. Visiem jaunajiem vai būtiski pilnveidotajiem e-pakalpojumiem **obligāti jāizmanto jaunais vienotais dizains** (piekļuve piesakāma: `atbalsts@vdaa.gov.lv`).
> 2. **Uzturēšanas pienākums produkcijā**: Iestādei ir pienākums vismaz **reizi gadā** veikt e-pakalpojuma migrāciju uz aktuālāko veidnes versiju. Ja veidnes versijas atpalicība no aktuālās pārsniedz **18 mēnešus**, VDAA ir tiesīga e-pakalpojumu **atpublicēt no portāla**.
> 3. **Piegāžu SLA termiņi**: VDAA veic piegādes uzstādīšanu testa vidē **10 darbdienu laikā** un produkcijas vidē **10 darbdienu laikā** pēc Akcepttestēšanas akta abpusējas parakstīšanas.
> 4. **Jenkins Deploy aizliegums**: Izstrādātājiem ir **kategoriski aizliegts** patstāvīgi palaist Jenkins uzstādīšanas darbus (*Deploy Jobs*).
> 5. **Git kontu 2FA prasība**: Saņemot Git piekļuvi, **obligāti jāieslēdz divfaktoru autentifikācija (2FA)**. Lietotāji bez 2FA tiek bloķēti. Konti ar 6 mēnešu neaktivitāti tiek dzēsti.
> 6. **Veiktspējas standarti (SLA)**: Sinhronā REST API atbildes laiks nedrīkst pārsniegt **3 sekundes**. Pārsūtāmās pakotnes apjoms nedrīkst pārsniegt **4 MB** (lielākiem datiem obligāti jāizmanto EDK). Sarakstiem obligāta servera puses lapošana.
> 7. **Datu minimizēšanas princips**: Stingri aizliegts vaicāt lietotājam datus, kas jau ir pieejami valsts reģistros (PMLP, UR, VZD, VID u.c.) — tie jāielasa automātiski tiešsaistē caur API.

---

## 📂 Pielikumā pieejamie oficiālie PDF dokumenti (`references/`)

Mapē `references/` ir saglabāti oriģinālie VDAA dokumenti:
- `references/bausli.pdf` — *E-pakalpojumu izveides baušļi jeb viegli lasīt* (VDAA, 2026).
- `references/parskats_paraugs.pdf` — *Pārskats par e-pakalpojuma atbilstību Latvija.gov.lv vadlīnijām* (Kontrolsaraksts Bloki A–K).
- `references/arhitektura.pdf` — *E-pakalpojumu platforma. Arhitektūras vadlīnijas* (VDAA-VDL_ARH-Lvp.EservicePlatform v1.09, 2025).
- `references/celvedis.pdf` — *E-pakalpojumu izveidošanas ceļvedis Latvija.gov.lv portālam. Programmētāja rokasgrāmata* (v1.41).
