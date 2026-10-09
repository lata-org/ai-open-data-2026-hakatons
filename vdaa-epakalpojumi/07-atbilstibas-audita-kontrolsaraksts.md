# 7. E-pakalpojuma atbilstības audita kontrolsaraksts (Bloki A – K)

Šis kontrolsaraksts atbilst VDAA oficiālajam dokumentam *"Pārskats par e-pakalpojuma atbilstību vadlīnijām"*. Šo kontrolsarakstu iestādei un izstrādātājam **jāizmanto kā pašnovērtējuma rīku** pirms e-pakalpojuma pieteikšanas akcepttestēšanai un pirms nodošanas produkcijas vidē.

### Atbilstības novērtējuma līmeņi:
- **Pilnībā atbilst**: Prasība ir pilnībā izpildīta bez aizrādījumiem.
- **Nepieciešami labojumi (*)**: Konstatēti nebūtiski trūkumi, ar kuriem pakalpojumu pieļaujams izvietot, bet pārzinim tie ir jānovērš noteiktā termiņā.
- **Neatbilst (****)**: Konstatēti **būtiski trūkumi vai nepilnības**, ar kurām pakalpojums **NEVAR tikt pieņemts un izvietots** Latvija.gov.lv.

---

## Bloks A: Biznesa līmenis

| ID | Prasības formulējums | Obligātums | Atsauce | Pārbaudes kritērijs |
| :--- | :--- | :---: | :--- | :--- |
| **A.1** | E-pakalpojuma izpilde ļauj sasniegt lietotājam jūtamu rezultātu (noteikto mērķi) | **Neatceļams** | EPAK.UI.Biz.1 | Lietotājs saņem reālu izziņu, lēmumu, iesnieguma reģistrāciju vai pakalpojumu, nevis tukšu apstiprinājumu. |
| **A.2** | E-pakalpojums kalpo tikai viena mērķa sasniegšanai | Obligāts | EPAK.UI.Biz.1 | Pakalpojums nav pārslogots ar nesaistītām funkcijām; katram atšķirīgam mērķim ir savs e-pakalpojums. |
| **A.3** | E-pakalpojums neatkārto citu e-pakalpojumu funkcionalitāti nozīmīgā apjomā | Obligāts | EPAK.UI.Biz.1 | Netiek dublēts jau esošs valsts e-pakalpojums. |
| **A.4** | Katra pakalpojuma izpildes reize nav atkarīga no iepriekšējās | Obligāts | EPAK.UI.Biz.2 | Jauna transakcija sākas no tīra stāvokļa (izņemot iestādes biznesa datu aktualitāti). |
| **A.5** | E-pakalpojums prasa minimāli nepieciešamo ievaddatu apjomu | Obligāts | EPAK.UI.Biz.3 | Netiek prasīti dati, kuri nav obligāti lēmuma pieņemšanai vai kurus var iegūt no reģistriem. |
| **A.6** | E-pakalpojums rāda tikai lietotājam nepieciešamu un saprotamu informāciju | Obligāts | EPAK.UI.Biz.3 | Ekrānā nav lieku tehnisku lauku vai nesaprotamu datubāzes tabulu. |

---

## Bloks B: E-pakalpojuma soļu organizācija

| ID | Prasības formulējums | Obligātums | Atsauce | Pārbaudes kritērijs |
| :--- | :--- | :---: | :--- | :--- |
| **B.1** | E-pakalpojums ir organizēts secīgos soļos | Obligāts | EPAK.UI.Org.1 | Loģiska 3–6 soļu plūsma ar vizuālu stāvokļa joslu augšā. |
| **B.2** | E-pakalpojumā nav apslēptu soļu | Obligāts | EPAK.UI.Org.4 | Izņemot specifiskus kļūdu vai atteikuma paziņojumu soļus. |
| **B.3** | Sarežģīta formāta datu laukiem tiek lietoti uznirstošie elementi vai modālie logi | Obligāts | EPAK.UI.Org.5 | Papildu klasifikatoru meklēšanai vai sarežģītām konfigurācijām. |
| **B.4** | Ievaddatu pārbaudes notiek katru reizi, pārejot pie nākamā soļa | Obligāts | EPAK.UI.Org.1 | Lietotājs netiek laists tālāk, ja solī ir nekorekti aizpildīti obligātie lauki. |
| **B.5** | E-pakalpojums ir loģiski noslēdzams visos gadījumos | Obligāts | EPAK.UI.Org.2 | Nav strupceļa scenāriju; atteikuma vai kļūdas gadījumā ir skaidrs paziņojums. |
| **B.6** | Ievadei pirmie tiek prasīti būtiskākie dati | Obligāts | EPAK.UI.Org.5 | Svarīgākie parametri ir sākumā, lai atsijātu nederīgus pieprasījumus. |
| **B.7** | Loģiski saistīti lauki ir sagrupēti blakus | Obligāts | EPAK.UI.Org.5 | Vizuāls grupējums (piemēram, Kontaktinformācija). |
| **B.8** | Katrā solī nav vairāk par 7–10 ievadlaukiem | Obligāts | EPAK.UI.Org.5 | Aizliegts pārslogot vienu ekrānu ar bezgalīgu formu. |
| **B.9** | Loģiski mazsaistīti lauki ir atdalīti ar horizontālu līniju vai izvietoti atsevišķos soļos | Obligāts | EPAK.UI.Org.5 | Vizuāls noformējums palīdz uztvert saturu. |
| **B.10** | Lietotājs tiek brīdināts pirms būtisku/neatgriezenisku darbību veikšanas | Obligāts | EPAK.UI.Org.3 | Apstiprinājuma logs pirms maksāšanas, dzēšanas vai iesniegšanas. |
| **B.11** | Pirms datu nosūtīšanas tiek parādīts to kopsavilkums | Obligāts | EPAK.UI.Org.3 | Galīgais pārskata solis (*Summary*). |
| **B.12** | E-pakalpojumā nav tukšu soļu/darbību | Obligāts | EPAK.UI.Org.4 | Katram solim ir konkrēta jēga. |
| **B.13** | Soļu nosaukumi ir lietvārdi vai darbības frāzes | Obligāts | EPAK.UI.Org.1 | Skaidri apzīmē veicamo darbību. |
| **B.14** | Atgriešanās iepriekšējos soļos ir liegta, ja iniciēta biznesa darbība | Obligāts | EPAK.UI.Org.1 | Ja noticis maksājums vai datu iesniegšana, ar "Back" nedrīkst dublēt darījumu. |
| **B.15** | Atkārtotu datu ievade izdalīta atsevišķā uznirstošajā logā | Obligāts | EPAK.UI.Org.5 | Ērta tabulāro sarakstu ievade. |
| **B.16** | Uznirstošajos logos nav citu uznirstošo logu (*No nested modals*) | Obligāts | EPAK.UI.Org.5 | Modālais logs virs cita modālā loga ir aizliegts. |

---

## Bloks C: Saturs un valoda

| ID | Prasības formulējums | Obligātums | Atsauce | Pārbaudes kritērijs |
| :--- | :--- | :---: | :--- | :--- |
| **C.1** | Formulējumi nav pretrunīgi | **Neatceļams** | EPAK.UI.Cont.1 | Loģiska konsistence visā pakalpojumā. |
| **C.2** | Formulējumi ir saskaņoti ar nozarē pieņemtajiem | **Neatceļams** | EPAK.UI.Cont.1 | Standarta termini atbilstošajā nozarē. |
| **C.3** | Viens jēdziens vienmēr tiek apzīmēts ar vienu un to pašu terminu | Obligāts | EPAK.UI.Cont.1 | Nav sinonīmu jucekļa. |
| **C.4** | Pareiza ortogrāfija, gramatika un interpunkcija | **Neatceļams** | EPAK.UI.Cont.2 | Nav pareizrakstības un stila kļūdu. |
| **C.5** | Ievērots lietišķais rakstu stils | **Neatceļams** | EPAK.UI.Cont.2 | Cieņpilna, formāla valoda ("Jūs" uzruna). |
| **C.6** | Paskaidres pieejamas katram ievades elementam vai grupai | Obligāts | EPAK.UI.Cont.3 | Norādes par datu formātu, ierobežojumiem. |
| **C.7** | Paskaidres ir informatīvas | Obligāts | EPAK.UI.Cont.3 | Sniedz reālu palīdzību, nevis atkārto lauka nosaukumu. |
| **C.8** | Kļūdu ziņojumi definē problēmu un tās novēršanas iespēju | Obligāts | EPAK.UI.Cont.4 | Norāda konkrētu risinājumu lietotājam. |
| **C.9** | Izmantota vienota ziņojumu tipu klasifikācija | Obligāts | EPAK.UI.Cont.5 | Standarta krāsas (info, warning, error, success). |
| **C.10** | Maksas pakalpojumu opcijas ir skaidri izdalītas | Obligāts | EPAK.UI.Cont.6 | Lietotājs ir informēts par pakalpojuma cenu pirms maksājuma. |
| **C.11** | Intervāliem norādīts, vai beigu punkts ir iekļauts | Vēlams | EPAK.UI.Cont.7 | Piemēram: "no 1 līdz 10 (ieskaitot)". |

---

## Bloks D: Lietotāja saskarnes vadīklu izvēle

| ID | Vadīklas veids | Obligātums | Standarts |
| :--- | :--- | :---: | :--- |
| **D.1** | Viena varianta izvēle no iepriekšdefinētiem (līdz 5–7) | Obligāts | **Radiopogu grupa** (*Radio buttons*). |
| **D.2** | Viena varianta izvēle no dinamiskiem vai daudziem variantiem | Obligāts | **Nolaižamais saraksts** (*Dropdown*) vai meklētājs. |
| **D.3** | Vairāku variantu izvēle no iepriekšdefinētiem | Obligāts | **Izvēles rūtiņu grupa** (*Checkboxes*). |
| **D.4** | Vairāku variantu izvēle no dinamiskiem variantiem | Obligāts | **Vairākatlašu saraksts** (*Multi-select box*). |
| **D.5** | Bināra loģiskā pazīme (Jā / Nē, piekrišana) | Obligāts | **Izvēles rūtiņa** (*Checkbox*). |
| **D.6** | Bināra alternatīva (divi līdzvērtīgi stāvokļi) | Obligāts | **Divu radiopogu grupa**. |
| **D.7** | Datuma ievade | Obligāts | **Kalendāra komponents** ar manuālu korekcijas iespēju. |
| **D.8** | Darbības, kas attiecas uz visu soli/logu | Obligāts | **Pogas** (*Buttons*). |
| **D.9** | Darbības, kas attiecas uz atsevišķu lauku vai palīdzību | Obligāts | **Hipersaites** (*Links*). |

---

## Bloks E: UI izkārtojums un piekļūstamība

| ID | Prasība | Obligātums | Kritērijs |
| :--- | :--- | :---: | :--- |
| **E.1** | Viens ievadlauks — viena veida datiem | Obligāts | Nedublēt vārdu un uzvārdu vienā laukā, ja datubāzē tie ir atsevišķi. |
| **E.2** | Soļu navigācijas pogas izvietotas apakšā | Obligāts | Standarta pogu josla ekrāna apakšdaļā. |
| **E.3** | Ievaddatiem nav nepamatotu ierobežojumu | Obligāts | Pieļaujami garāki uzvārdi, ārvalstu tālruņi, dubultie vārdi ar defisi. |
| **E.4** | Lokālie paziņojumi rādīti pie attiecīgā lauka | Vēlams | Kļūda tieši pie kļūdainā ievadlauka. |
| **E.5** | Paziņojumi par kļūdu rādīti paskaidres elementā | Obligāts | Sarkans marķējums un kļūdas paskaidrojošs teksts. |
| **E.6** | **Neparādās ritjoslas (ne horizontālās, ne vertikālās)** | Obligāts | Ietvars korekti mērogojas un novērš liekus *scrollbars*. |
| **E.7** | Primārā darbības poga ir vizuāli izcelta | Obligāts | Primārā poga ir dominējošā krāsā kā noklusētā. |
| **E.8** | Elementi, krāsas un stili veidoti ar ietvara SDK | Obligāts | Izmantots jaunais Latvija.gov.lv dizaina SDK un komponentes. |
| **E.9** | Teksta kontrasts atbilst standartam | Obligāts | Kontrasts atbilst WCAG 2.1 AA (≥ 4.5:1). |
| **E.10**| Pilnvērtīga vadība tikai ar tastatūru | Obligāts | Visi elementi fokusējami un aktivizējami bez peles. |
| **E.11**| Ekrāna lasītāju (Screen Readers) atbalsts | Obligāts | Semantisks HTML un korekti ARIA marķējumi. |

---

## Bloks F: Tehniskā organizācija

| ID | Prasība | Obligātums | Kritērijs |
| :--- | :--- | :---: | :--- |
| **F.1** | Izmantota ietvara aktuālā versija | **Neatceļams** | E-pakalpojums būvēts uz aktuālās VDAA veidnes bāzes. |
| **F.2** | **Datu pārbaudes tiek dublētas servera pusē** | **Neatceļams** | Aizliegts paļauties tikai uz klienta (JavaScript) validāciju! |
| **F.3** | Adrešu ievadei izmantota VISS AMK komponente | Obligāts | Izmantots Valsts adrešu meklētājs, nevis brīva teksta lauks. |
| **F.4** | Teksti glabāti kā resursi | Obligāts | Lokalizācijas resursu faili (`.resx` vai JSON). |
| **F.5** | Uznirstošajiem logiem lietoti tikai ietvara rīki | Obligāts | Izmantoti standarta SDK dialoglogi, nevis pārlūka `alert()`/`confirm()`. |
| **F.6** | Servisu sertifikāti ir izveidoti un derīgi | Obligāts | Visi SSL/TLS un VISS savienojumu sertifikāti ir derīgi. |

---

## Bloks G: Arhitektūra un servisi

| ID | Prasība | Obligātums | Kritērijs |
| :--- | :--- | :---: | :--- |
| **G.1** | Mikroservisu arhitektūra uz Linux Docker/K8s | Obligāts | Risinājums ir pilnībā konteinerizēts un darbināms VDAA Kubernetes klasterī. |
| **G.2** | Mobilā adaptivitāte, daudzvalodība, vājredzīgo režīms | Obligāts | Nodrošināts pilns atbalsts dažādām iekārtām un režīmiem. |
| **G.3** | Realizēts BFF (Backend-For-Frontend) slānis | Obligāts | UI nekad tieši neizsauc ārējos reģistrus, visa loģika iet caur BFF. |
| **G.4** | Datu apmaiņai izmantots JSON REST | Obligāts | Standartizēti REST API ar OpenAPI 3.0 dokumentāciju. |
| **G.5** | Ja tiek izmantots XML SOAP, tas reģistrēts API pārvaldniekā | Obligāts | Atbilstība VISS XML standartam. |
| **G.6** | Sarakstu lapošana servera pusē (*Pagination*) | Obligāts | Serveris atgriež ierakstus pa lapām ar kopējā skaita norādi. |
| **G.7** | Klasifikatoru saskaņošana ar VISS katalogu | Obligāts | Izmantoti VISS uzturētie klasifikatori (ATVK u.c.). |

---

## Bloks H: E-pakalpojumu izstrāde un veiktspēja

| ID | Prasība | Obligātums | Kritērijs |
| :--- | :--- | :---: | :--- |
| **H.1** | Pieejama programmatūras prasību specifikācija | Obligāts | Dokumentētas funkcionālās un nefunkcionālās prasības. |
| **H.2** | JSON struktūru shēmas un OpenAPI apraksti | Obligāts | Pilnīgi API apraksti WSO2 reģistrācijai. |
| **H.3** | **SLA izpilde**: Sinhronais laiks **≤ 3 s**, datu apjoms **≤ 4 MB** | Obligāts | Ja pārsniedz, obligāti jāizmanto EDK vai asinhronā apstrāde. |
| **H.4** | Dokumentētas visas izņēmuma situācijas | Obligāts | Definēti kļūdu kodi un notikumi. |
| **H.5** | Servisi reģistrēti VDAA API pārvaldniekā | Obligāts | API publicēti WSO2 Publisher/Store. |
| **H.6** | Pievienoti servisu un pakalpojuma testēšanas protokoli | Obligāts | Piegādei pievienots veiksmīgu testu apliecinājums. |
| **H.7** | Nodefinēti e-pakalpojumu pieturpunkti (*Milestones*) | Obligāts | Sākuma, starpposmu un beigu URN pieturpunkti (garums ≤ 15 zīmes). |
| **H.8** | Aizpildīts e-pakalpojuma apraksta šablons | Obligāts | Iesniegts `EpakalpojumaAprakstsSablons.xlsx`. |

---

## Bloks I: Drošība

| ID | Prasība | Obligātums | Kritērijs |
| :--- | :--- | :---: | :--- |
| **I.1** | Veikts drošības audits un novērstas ievainojamības | **Neatceļams** | Nav neatrisinātu augsta riska drošības kļūdu (OWASP Top 10). |
| **I.2** | Ievadlauki aizsargāti pret injekcijām | **Neatceļams** | Drošība pret SQLi, XSS, CSRF, komandu injekcijām. |
| **I.3** | Datu validācija nodrošināta abās pusēs | **Neatceļams** | Klienta validācija UX ērtībai + servera validācija datu integritātei. |

---

## Bloks J: VIRSIS kartītes atbilstība

| ID | Prasība | Obligātums | Kritērijs |
| :--- | :--- | :---: | :--- |
| **J.1 – J.3** | Skaidrs pakalpojuma nosaukums, īss apraksts un atslēgvārdi | Obligāts | Atbilstība vienotajam valsts pakalpojumu katalogam. |
| **J.4 – J.6** | Pieprasīšanas/saņemšanas kanāli un saistītās dzīves situācijas | Obligāts | Saistīts ar konkrētu dzīves situāciju Latvija.gov.lv. |
| **J.7 – J.8** | Pakalpojuma sniegšanas process teksta un video formātā | Obligāts | Iedzīvotājam pieejama video un teksta pamācība (datora un mobilajā skatā). |
| **J.9 – J.11** | Normatīvie akti un detalizēta papildu informācija | Obligāts | Precīzas juridiskās atsauces VIRSIS kartītē. |

---

## Bloks K: Lietotāju novērtējuma komponente

| ID | Prasība | Obligātums | Kritērijs |
| :--- | :--- | :---: | :--- |
| **K.1** | Integrēta saite uz vienoto novērtējuma komponenti | Obligāts | Pakalpojuma noslēgumā iedzīvotājam dota iespēja novērtēt e-pakalpojuma kvalitāti un atstāt atsauksmi. |
