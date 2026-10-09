# 1. Tiesiskais regulējums un atbildības sadalījums

## 1.1. Tiesiskais regulējums

E-pakalpojumu izstrādi, uzturēšanu, integrāciju un izmitināšanu vienotajā valsts pārvaldes pakalpojumu portālā [Latvija.gov.lv](https://latvija.gov.lv) regulē Latvijas Republikas un Eiropas Savienības tiesību akti un standarti:

1. **Ministru kabineta 2017. gada 4. jūlija noteikumi Nr. 402 "Valsts pārvaldes e-pakalpojumu noteikumi"**:
   - Nosaka kārtību, kādā valsts un pašvaldību institūcijas nodrošina publisko pakalpojumu pieejamību elektroniskā formā.
   - **3. punkts**: Nosaka pienākumu izvērtēt pakalpojuma elektronizēšanas lietderību — pakalpojuma pieprasījumu skaitu, mērķauditoriju, iestādes administratīvo un finanšu resursu noslodzi pirms izstrādes uzsākšanas.
   - **10.2. punkts**: Nosaka principu "Tikai vienreiz" (*Once-Only Principle*) — aizliegts pieprasīt no pakalpojuma saņēmēja datus, kas jau ir pieejami valsts informācijas sistēmās vai reģistros.

2. **Valsts informācijas sistēmu likums**:
   - **6. panta otrā daļa**: Aizliedz vākt no datu subjektiem un ievadīt valsts informācijas sistēmu datubāzēs datus, kas ir pieejami integrētā valsts informācijas sistēmā (VISS).
   - Nosaka valsts informācijas sistēmu savietojamības un datu apmaiņas pamatprincipus.

3. **Ministru kabineta 2020. gada 14. jūlija noteikumi Nr. 445 "Kārtība, kādā iestādes ievieto informāciju internetā"**:
   - Nosaka piekļūstamības prasības valsts pārvaldes tīmekļvietnēm un e-pakalpojumiem atbilstoši Eiropas standartam **EN 301 549** un **W3C WCAG 2.1 AA līmenim**.

4. **Eiropas Parlamenta un Padomes Regula (ES) Nr. 910/2014 (eIDAS)**:
   - Prasības par elektronisko identifikāciju un uzticamības pakalpojumiem elektronisko darījumu veikšanai iekšējā tirgū.
   - Ja pakalpojums pieejams citu ES dalībvalstu pilsoņiem ar pārrobežu eID rīkiem, jānodrošina tā pieejamība un saskarne arī **angļu valodā**.

5. **Ministru kabineta 2005. gada 28. jūnija noteikumi Nr. 473 "Elektronisko dokumentu izstrādāšanas, noformēšanas, glabāšanas un aprites kārtība valsts un pašvaldību iestādēs un kārtība, kādā notiek elektronisko dokumentu aprite starp valsts un pašvaldību iestādēm vai starp šīm iestādēm un fiziskajām un juridiskajām personām"**:
   - Nosaka prasības elektronisko dokumentu noformēšanai (piemēram, `.edoc`, `.asice`, kā arī lietotājam apskatāmās informācijas formātu `.rtf` vai `.pdf`).

6. **Oficiālās elektroniskās adreses likums**:
   - E-adrese kā obligāts oficiālās saziņas un dokumentu apmaiņas kanāls starp iestādēm un sadarbībā ar VDAA (pieteikumu un veidlapu iesniegšana).

---

## 1.2. Iestāžu lomas un atbildības

### Valsts digitālās attīstības aģentūra (VDAA)
*VDAA (iepriekš VRAA) ir valsts pārvaldes e-pakalpojumu infrastruktūras un portāla Latvija.gov.lv pārzinis.*

VDAA nodrošina:
- E-pakalpojumu izstrādes un izpildes infrastruktūru (Kubernetes klasteris, konteineru vide, tīkla drošība).
- Koplietošanas komponentes un mikroservisus (LVP Identity Server, VISS API Pārvaldnieks WSO2, Adrešu meklēšanas komponente, Elektronisko dokumentu krātuve, Maksājumu modulis, Notifikācijas u.c.).
- Vienotās lietotāja saskarnes ietvarus, bibliotēkas un dizaina sistēmas (ReactJS un .NET Core MVC SDK, Storybook).
- Piegāžu un izvietošanas infrastruktūru (Git repozitoriji, Nexus artifaktu krātuve, Jenkins CI/CD konveijeri, PAM piekļuve).
- 1. līmeņa konsultatīvo atbalstu e-pakalpojumu galalietotājiem (iedzīvotājiem un uzņēmējiem) portāla darbības laikā.
- E-pakalpojumu akceptēšanu, uzstādīšanu testa un produkcijas vidēs (10 darbdienu SLA).
- Lietotāju jautājumu, sūdzību un ierosinājumu nodošanu atbildīgajai iestādei.

### Pakalpojuma pārzinis (Valsts vai pašvaldības iestāde)
*Iestāde, kuras kompetencē ir konkrētā publiskā pakalpojuma sniegšana un kura ir e-pakalpojuma īpašnieks.*

Iestāde nodrošina:
- Pakalpojuma elektronizēšanas lietderības un biznesa loģikas analīzi.
- E-pakalpojuma izstrādes pasūtīšanu un uzraudzību saskaņā ar VDAA vadlīnijām.
- Sadarbības procedūras izpildi (oficiālo pieteikumu un veidlapu iesniegšanu ar drošu e-parakstu caur e-adresi).
- Sadarbību ar citu iestāžu reģistriem (nepieciešamo API tiesību pieprasīšanu un saskaņošanu).
- 2. un 3. līmeņa atbalsta nodrošināšanu (iestādes biznesa procesu, lēmumu pieņemšanas un satura jautājumos).
- E-pakalpojuma demonstrāciju VDAA 1. līmeņa atbalsta dienesta darbiniekiem pirms laišanas produkcijā.
- Pakalpojuma apraksta uzturēšanu un aktualizāciju Valsts pārvaldes pakalpojumu portālā / katalogā **VIRSIS**.
- **Regulāru uzturēšanu produkcijā**: Pienākumu sekot līdzi aktuālajai e-pakalpojuma veidnes versijai un **vismaz reizi gadā** veikt e-pakalpojuma migrāciju uz jaunāko veidni. Ja veidnes noilgums pārsniedz 18 mēnešus, pakalpojums var tikt atpublicēts.

### Izstrādātājs (Iestādes nolīgtais piegādātājs vai iekšējā IT komanda)
*Tehniskais izpildītājs, kas programmē un piegādā e-pakalpojumu.*

Izstrādātājs nodrošina:
- Programmatūras izstrādi saskaņā ar VDAA arhitektūras, vizuālā izskata un tehniskajām vadlīnijām.
- Divfaktoru autentifikācijas (2FA) lietošanu VDAA Git un izstrādes resursos.
- Piegāžu pakotņu sagatavošanu (Docker attēli, Helm pakotnes, pirmkods Git, izpildkods Nexus, testēšanas protokoli, izmaiņu apraksti).
- Veiktspējas (SLA: atbilde < 3 s, datu apjoms < 4 MB), pieejamības (WCAG 2.1 AA) un drošības (OWASP, validācijas) prasību izpildi.
- Testēšanu testa vidē un dalību akcepttestēšanā kopā ar iestādi un VDAA.
- Aizlieguma ievērošanu — izstrādātājs **nekad pats neveic** Jenkins produkcijas/testa izvietošanas darbus (Deploy job).
