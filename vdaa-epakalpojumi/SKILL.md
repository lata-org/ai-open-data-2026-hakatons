---
name: vdaa-epakalpojumi
description: >-
  Visaptverošas vadlīnijas, tehniskās prasības, arhitektūras standarti un audita kontrolsaraksts
  Latvijas valsts un pašvaldību e-pakalpojumu izstrādei, integrācijai un izmitināšanai vienotajā
  valsts pārvaldes pakalpojumu portālā Latvija.gov.lv un VDAA (Valsts digitālās attīstības aģentūras)
  infrastruktūrā. Izmantojiet šo prasmi, lai plānotu, projektētu, izstrādātu, pārbaudītu vai auditētu
  e-pakalpojumus, sagatavotu piegādes vai nodrošinātu atbilstību oficiālajām VDAA vadlīnijām.
---

# VDAA E-pakalpojumu izstrādes, prasību un izmitināšanas prasme

Šī prasme instruē asistentu (aģentu) rīkoties kā augstākā līmeņa valsts e-pārvaldes arhitektam, risinājumu izstrādātājam un atbilstības auditoram saskaņā ar **Valsts digitālās attīstības aģentūras (VDAA)** un portāla **Latvija.gov.lv** prasībām.

---

## 1. Pamatprincipi un "E-pakalpojumu baušļi"

Plānojot vai vērtējot jebkuru e-pakalpojumu, obligāti jāpiemēro šādi pamatprincipi:

1. **Lietderības izvērtējums (*MK noteikumi Nr. 402, 3.p.*)**:
   - Digitalizē tikai pakalpojumus ar lielu klientu skaitu un būtisku iestādes noslodzi.
   - Pārskata pašu procesu — netulko papīra veidlapu digitālā formā, bet optimizē procedūru.
2. **Princips "Tikai vienreiz" (*Once-Only Principle*, Valsts informācijas sistēmu likuma 6.p. 2.d.)**:
   - **Stingri aizliegts prasīt lietotājam datus, kas pieejami valsts reģistros** (PMLP, UR, VZD, VID, CSDD u.c.). Dati jāielasa tiešsaistē caur API un jāparāda tikai apskatei/apstiprināšanai.
   - Jāprasa tikai tie dati, bez kuriem lēmuma pieņemšana nav iespējama.
3. **90% lietotāju plūsma un *Mobile-First***:
   - Galvenajai plūsmai jābūt maksimāli vienkāršai un pielāgotai 90% lietotāju.
   - Reti izņēmumi jāpaslēpj zem *"Cits gadījums"*.
   - Saskarnei jābūt pilnībā lietojamai viedtālruņos bez horizontālās ritjoslas.
4. **Lietotājam draudzīga valoda un lauku formulējumi**:
   - Ievades grupas formulējamas kā aicinājumi uz darbību ("Ievadiet deklarētās dzīvesvietas adresi", nevis "Adrese").
   - Aizliegts iekšējais iestādes žargons un sarežģītas juridiskās frāzes ekrāna pamatplūsmā.
5. **Skaidrs noslēgums un "Kas sekos tālāk"**:
   - Pakalpojuma pēdējā solī obligāti jānorāda: izpildes/lēmuma termiņš, atbildes saņemšanas kanāls (e-adrese, KDV, e-pasts) un vai klientam vēl jāveic kādas darbības.
6. **Īsta elektronizācija**:
   - Datiem no e-pakalpojuma strukturētā veidā (JSON/REST) jānonāk iestādes informācijas sistēmā, izslēdzot manuālu pārrakstīšanu.

---

## 2. Kritiskie termiņi un tehnoloģiskie ierobežojumi

> [!IMPORTANT]
> - **Oranžais dizains beidzas 2027. gada 30. jūnijā**: Pašreizējais dizains pēc 30.06.2027. vairs netiks atbalstīts. Visiem jaunajiem vai būtiski pilnveidotajiem pakalpojumiem **obligāti jāizmanto jaunais vienotais dizains**.
> - **Gada veidņu atjaunošanas pienākums**: Iestādei ir pienākums vismaz **reizi gadā** veikt pakalpojuma migrāciju uz jaunāko veidnes versiju. Ja veidnes atpalicība pārsniedz **18 mēnešus**, VDAA **atpublicē pakalpojumu** no portāla.
> - **Jenkins Deploy aizliegums**: Izstrādātājiem **STINGRI AIZLIEGTS** patstāvīgi palaist Jenkins uzstādīšanas darbus (*Deploy Jobs*). To drīkst veikt tikai VDAA speciālisti.
> - **Git 2FA prasība**: Git kontiem obligāti jāieslēdz divfaktoru autentifikācija, citādi konts tiek nobloķēts. Konti ar 6 mēnešu neaktivitāti tiek anulēti.
> - **Uzstādīšanas SLA**: VDAA uzstāda piegādi testa vidē 10 darbdienu laikā; produkcijas vidē — 10 darbdienu laikā pēc akcepttestēšanas akta abpusējas parakstīšanas.

---

## 3. Tehniskā arhitektūra un standarti

### Zonu struktūra un komponentes:
- **Vide**: Linux bāzes Docker konteineri uz **Kubernetes** klastera.
- **Arhitektūras šablons**: **BFF (Backend For Frontend)**. BFF ir bezstāvokļa (*stateless*). Sesijas datu pagaidu uzglabāšanai izmanto **Konteksta mikroservisu** (`LvpContext.SessionProperties`).
- **Frontend opcijas**:
  1. **SPA**: ReactJS (TypeScript/JS) — [React Storybook](https://eservices-test.vraa.gov.lv/EservicePlatform.Controls.React.Full.Dev/)
  2. **MPA**: ASP.NET Core MVC (C#) — [HTML Storybook](https://eservices-test.vraa.gov.lv/EservicePlatform.Controls.Html.Full.Dev/)
- **Piekļūstamība**: **W3C WCAG 2.1 AA līmenis** (kontrasti ≥ 4.5:1, pilnvērtīga tastatūras navigācija ar skaidru fokusu, ekrāna lasītāji, vājredzīgo režīms, adaptivitāte).
- **Lietotāja saskarnes ierobežojumi**:
  - Vienā solī **ne vairāk kā 7–10 ievadlauki**.
  - Navigācijas pogas apakšā; primārā poga vizuāli izcelta.
  - **Neparādās liekas ritjoslas (*No scrollbars*)**.
  - Adrešu ievadei obligāti izmanto **VISS Adrešu meklēšanas komponenti (AMK)**.
- **Autentifikācija un talonu apmaiņa**:
  - `Lvp.Portal.IdentityServer` (OIDC code-grant ar PKCE).
  - Pārlūks -> IDS Reference Token -> Konteksta API -> IDS JWT -> Pieprasījumu API -> **PFAS STS AUTH Token** -> WSO2 API Pārvaldnieks -> Datu devēja serviss.
- **Lietotāju URN shēma (`urn:ivis:100001:name.id-viss`)**:
  - Iedzīvotājs: `PK:10098610000`
  - Iestādes darbinieks: `AU:100001-PK:10098610000`
  - Juridiskās personas pārstāvis: `PK:07017010000-UR:40003627089`
  - Pilnvarotais: `DP:01127612344-PK:07017010000`
- **Pieturpunkti (*Milestones*)**:
  - URN formāts: `URN:IVIS:<AuthID>:EP-<nosaukums>-v<Maj>-<Min>-MS-<MilestoneID>` (nosaukums ≤ 15 zīmes).
  - Obligāti: vismaz viens `start`, vismaz viens `finish` un starpposmi.
- **Servisu SLA un datu apjoms**:
  - Sinhronais izpildes laiks: **≤ 3 sekundes**.
  - Datu apjoms saskarnē: **≤ 4 MB**. Ja lielāks — obligāti izmanto **Elektronisko dokumentu krātuvi (EDK, CMIS standarts)**.
  - Sarakstiem obligāta **server-side lapošana** (*pagination*).
  - Datņu augšupielādei: obligāta pretvīrusu pārbaude ar ietvara **ClamAV** mikroservisu + papildu formātu un satura validācija.
  - Datu validācija obligāti jāveic **gan klienta, gan servera pusē**.

---

## 4. Sadarbības procedūras 4 soļu darba plūsma

Kad lietotājs vaicā par e-pakalpojuma ieviešanas gaitu, vadieties pēc šiem 4 soļiem:

1. **Pieteikšanās un reģistrācija**:
   - Iestāde aizpilda `epak_registresanas_veidlapa_v2_0.docx` un ar drošu e-parakstu nosūta uz VDAA e-adresi.
   - VDAA piešķir e-pakalpojuma ID (`EPXXX`) un kontaktpersonu.
   - Iestāde iesniedz tiesību pieprasījumu testa videi un API Pārvaldnieka veidlapu.
2. **Izstrāde un nodevumi testa vidē**:
   - Izstrāde atbilstoši arhitektūrai un jaunajam dizainam.
   - Piegāde: Docker tēls uz Nexus, kods uz Git, apraksts uz `piegades@vdaa.gov.lv` ar `EpakalpojumaAprakstsSablons.xlsx`.
   - VDAA uzstāda testa vidē 10 darbdienu laikā.
3. **Akcepttestēšana un demonstrācija**:
   - Pozitīvo un negatīvo scenāriju izpilde noteiktā laika logā.
   - VDAA noņem auditpierakstus un aizpilda atbilstības pārskatu (Bloki A–K).
   - Iestāde veic demonstrāciju VDAA 1. līmeņa atbalsta dienestam.
   - Abpusēja Akcepttestēšanas akta parakstīšana ar drošu e-parakstu.
4. **Uzstādīšana un uzturēšana produkcijā**:
   - API piekļuves atvēršana produkcijā.
   - Oficiāls pieprasījums ar pilnu nodevuma komplektu un VIRSIS kartītes apstiprinājumu.
   - VDAA uzstāda produkcijā 10 darbdienu laikā.
   - Iestāde nodrošina regulāru veidņu atjaunošanu (vismaz 1x gadā).

---

## 5. Aģenta darbības un audita instrukcijas

Kad aģentam tiek uzdots analizēt vai veidot e-pakalpojumu:

### Darbība A: Prasību un dizaina pārbaude (Pre-audit)
Pārbaudi risinājumu pret VDAA oficiālajiem 11 blokiem:
- **Bloks A (Bizness)**: Viens skaidrs mērķis, jūtams rezultāts, minimāli ievaddati.
- **Bloks B (Soļi)**: 3–6 soļi, ≤ 7–10 lauki solī, kopsavilkuma solis pirms iesniegšanas, nav tukšu soļu, aizliegti iegulti modālie logi virs citiem modālajiem logiem.
- **Bloks C (Saturs)**: Skaidra valoda, nav juridiskā žargona pamatplūsmā, informatīvi kļūdu ziņojumi ar rīcības norādi, skaidras pakalpojuma maksas.
- **Bloks D & E (UI vadīklas un izkārtojums)**: Radiopogas maziem sarakstiem, dropdown lieliem, AMK adrešu meklētājs, kalendārs datumiem, primārā poga apakšā izcelta, **nav ritjoslu (scrollbars)**.
- **Bloks F (Tehniskais)**: Dublēta servera validācija, teksti resursu failos, derīgi sertifikāti.
- **Bloks G & H (Arhitektūra un veiktspēja)**: BFF slānis, REST/OpenAPI, SLA ≤ 3 s, datu apjoms ≤ 4 MB, definēti URN pieturpunkti (≤ 15 zīmes).
- **Bloks I (Drošība)**: OWASP aizsardzība, injekciju novēršana, abu pušu validācija, ClamAV pārbaudes.
- **Bloks J & K (VIRSIS un atsauksmes)**: Kartīte VIRSIS ar video/teksta pamācību, integrēta novērtējuma komponente.

### Darbība B: Koda ģenerēšana
Ģenerējot e-pakalpojuma kodu (React SPA vai .NET Core MVC):
- Izmantojiet VDAA Storybook un dizaina SDK atbilstošās komponentes;
- Nodrošiniet semantisku HTML ar WCAG 2.1 AA marķējumu (`aria-label`, `role="alert"`, korekti `<label for="...">`);
- Pievienojiet dublētas validācijas shēmas backend BFF līmenī (piemēram, Zod / FluentValidation / DataAnnotations);
- Integrējiet AMK un pieturpunktu reģistrāciju.
