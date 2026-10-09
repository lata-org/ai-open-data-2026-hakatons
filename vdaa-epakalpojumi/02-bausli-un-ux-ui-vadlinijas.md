# 2. E-pakalpojumu izveides baušļi un UX/UI vadlīnijas

## 2.1. E-pakalpojumu izveides 15 baušļi ("Viegli lasīt")

VDAA izstrādātie "E-pakalpojumu izveides baušļi" ir metodisks materiāls, kas katrai valsts pārvaldes iestādei un izstrādātājam ir obligāti jāņem vērā pirms pakalpojuma digitalizēšanas un tās laikā.

---

### I. Kas jāņem vērā pirms pakalpojumu digitalizēšanas?

#### 1. Slodzes un lietderības izpēte
> **Princips**: Digitalizējiet tikai tos pakalpojumus, kuri sagādā vislielāko slodzi iestādei un kuriem ir ievērojams klientu skaits.
- Ja pakalpojuma pieprasījums paredzams tikai dažas reizes gadā, e-pakalpojuma izstrādei tērēt ievērojamus valsts resursus nav ekonomiski pamatoti (*MK noteikumu Nr. 402 3. punkts*).

#### 2. Procedūras pārskatīšana un optimizācija
> **Princips**: Pirms digitalizēšanas pārskatiet pašu pakalpojuma procedūru.
- Nedrīkst vienkārši "pārnest papīra veidlapu uz ekrāna".
- Ar informācijas tehnoloģiju palīdzību bieži vien labāku rezultātu var sasniegt ar pavisam citu, īsāku vai automatizētu procedūru (piemēram, proaktīvs pakalpojums, automātiska datu pārbaude).

---

### II. Ieteikumi veiksmīga e-pakalpojuma izveidei

#### 3. Prioritāte mobilajām ierīcēm (*Mobile-first*)
- Izstrādājot skices un ekrānus, galvenā uzmanība jāpievērš lietošanas ērtumam viedtālruņos.
- Lielākā daļa iedzīvotāju e-pakalpojumus mūsdienās iniciē un lieto no mobilajām ierīcēm.

#### 4. 90% lietotāju plūsmas likums
- Visērtāk un ātrāk jābūt izpildāmām darbībām, kuras veic **90% lietotāju**.
- Retie un izņēmuma gadījumi jāapskata atsevišķi, nevis jāsarežģī galvenā pakalpojuma plūsma.
- Izņēmuma gadījumus ieteicams paslēpt zem opcijas *"Cits gadījums"* vai atsevišķā atzarā.

#### 5. Mērķa noskaidrošana sākumā sarežģītiem pakalpojumiem
- Ja pakalpojumā iespējams atrisināt vairākas atšķirīgas situācijas, jau pirmajā solī jānoskaidro lietotāja mērķis (piemēram, ar radiopogām).
- Zem katras izvēles jāsniedz īss, skaidrojošs apraksts:
  - ko šī izvēle nozīmē;
  - kādi dokumenti vai dati jāsagatavo pirms darba uzsākšanas;
  - kāds būs sagaidāmais rezultāts.

#### 6. Datu pieprasīšanas vienreizības princips (*Once-Only*)
- **Lietotājam jāprasa tikai tie dati, kuru nav valsts iestāžu reģistros.**
- Ja dati pieejami citā reģistrā (PMLP, UR, VZD, VID, CSDD u.c.), tie e-pakalpojumā jāsaņem tiešsaistē ar API/servisiem un lietotājam jāparāda tikai pārbaudei.
- *Valsts informācijas sistēmu likuma 6. panta 2. daļa aizliedz vākt no datu subjektiem datus, kas jau ir integrētajā valsts informācijas sistēmā.*

#### 7. Tikai obligāti nepieciešamie dati
- Prasiet tikai tos datus, bez kuriem pakalpojums nav juridiski vai tehniski izpildāms.
- Ja tiek vaicāti neobligāti dati, vienmēr skaidri jānorāda, kāds būs lietotāja tiešais ieguvums no to aizpildīšanas. Ja ieguvuma nav — datus prasīt aizliegts.

#### 8. Lauku nosaukumi kā aicinājums uz darbību (*Call-to-Action*)
- Ievaddatu grupas jāformulē darbības formā vai kā jautājums, nevis kā statisks nosaukums:
  - *Pareizi*: "Ievadiet meklējamā dokumenta numuru", "Kurai izglītības iestādei iesniegsiet pieteikumu?".
  - *Nepareizi*: "Dokumenta dati", "Izglītības iestāde".

#### 9. Skaidri paskaidrojumi redzamā vietā
- Katrā solī jāparedz, kas lietotājam varētu būt neskaidrs.
- Svarīgākajai informācijai jābūt uzreiz redzamai uz ekrāna, nevis paslēptai rīka padomēs (*tooltips*) vai lapas kājenē.

#### 10. Skaidra navigācija un "Kas jādara tālāk"
- Jebkurā situācijā lietotājam jābūt skaidram, kas notiek pašlaik un kas sekos tālāk.
- Lietotājs nedrīkst nonākt strupceļā.

#### 11. Skaidrs pakalpojuma noslēgums
- E-pakalpojuma noslēgumā (iesniedzot pieteikumu) **nepietiek** ar paziņojumu: *"Paldies, jūsu pieteikums ir pieņemts"*.
- **Obligāti jānorāda**:
  - kāds ir lēmuma pieņemšanas vai izpildes termiņš;
  - kur un kādā veidā klients saņems atbildi (e-adrese, e-pasts, KDV darba vieta);
  - vai klientam pašam vēl kaut kas jādara.
  - Pretējā gadījumā iedzīvotāji vēršas atbalsta dienestā vai iestādē ar liekiem zvaniem un vēstulēm.

#### 12. Nerādiet lieku informāciju
- Uz ekrāna jārāda tikai tie dati, kuri lietotājam konkrētajā brīdī palīdz pieņemt lēmumu vai veikt darbību.
- Nav pieļaujams attēlot milzīgas iekšējās datubāzes tabulas, kurās lietotājs nespēj orientēties.

#### 13. Cilvēcīga un saprotama valoda
- Aizliegts lietot specifisku iekšējo iestādes žargonu vai saīsinājumus.
- Jāizvairās no sarežģītas juridiskās terminoloģijas pat tad, ja tā burtiski lietota likumos.
- E-pakalpojumi tiek veidoti iedzīvotājiem, nevis juristiem vai ierēdņiem. Likuma pantu atsauces izvietojamas paskaidrojošajā sadaļā zem izpildes loga.

#### 14. Datu tieša integrācija iestādes informācijas sistēmā
- E-pakalpojumā ievadītajiem datiem struktūrvidē (JSON/XML) automātiski jānonāk iestādes informācijas sistēmā vai lietvedībā.
- **Aizliegts veidot pseido-elektronizāciju**, kur e-pakalpojums tikai saģenerē PDF/DOC failu, kuru iestādes darbinieks pēc tam manuāli pārraksta iekšējā sistēmā.

---

### III. Kam vēl jāpievērš uzmanība?

#### 15. Pārstāvības un lietotāju lomu diferencēšana
- Jāparedz, vai pakalpojumu saņem:
  - fiziska persona par sevi;
  - vecāks par bērnu / aizbilstamais;
  - juridiskās personas likumiskais pārstāvis (Uzņēmumu reģistra dati);
  - pilnvarotā persona (pilnvarojums reģistrēts UR vai VISS Pilnvarošanas risinājumā).
- Jānodrošina korekta tiesību pārbaude un lomu pārslēgšana saskarnē.

#### 16. Starptautiskā pieejamība (eIDAS / ES pilsoņi)
- Ja pakalpojums ir pieejams citu ES dalībvalstu iedzīvotājiem (ar pārrobežu eID rīkiem saskaņā ar eIDAS regulu), tā lietotāja saskarnei un soļu aprakstiem obligāti jānodrošina pilnvērtīga **angļu valodas versija**.

---

## 2.2. Lietotāja saskarnes (UI/UX) obligātās prasības

### Soļu organizācija
1. **Pakalpojuma sadalījums secīgos soļos**:
   - Soļu skaits parasti ir 3–6 soļi.
   - Soļu nosaukumi ir darbības vārdi vai lietvārdu frāzes ("1. Datu pārbaude", "2. Pakalpojuma parametri", "3. Iesnieguma apstiprināšana").
2. **Ievadlauku limits**:
   - Vienā solī **ne vairāk kā 7–10 ievadlauki**.
   - Ja nepieciešams ievadīt vairāk datu, lauki jāsadala loģiskās grupās ar apakšvirsrakstiem vai atsevišķos soļos.
3. **Pirms-nosūtīšanas kopsavilkums (*Summary / Confirmation step*)**:
   - Pirms datu galīgās nosūtīšanas lietotājam obligāti jārāda visu ievadīto datu pārskats apstiprināšanai.
   - Ja darbība ir neatgriezeniska (piemēram, anulēšana, maksājums), nepieciešams skaidrs brīdinājums.
4. **Loģisks noslēgums**:
   - E-pakalpojumam jābūt loģiski noslēdzamam jebkurā gadījumā, arī tad, ja klients nesaņem pozitīvu rezultātu (jābūt informatīvam kļūdas vai atteikuma solim).

### Vadīklu izvēles standarts
- **Viena varianta izvēle (līdz 5–7 variantiem)**: Radiopogas (*Radio buttons*).
- **Viena varianta izvēle (vairāk nekā 7 varianti vai dinamisks saraksts)**: Nolaižamais saraksts (*Dropdown / Select*) vai meklēšanas lauks (*Autocomplete*).
- **Vairāku variantu izvēle**: Izvēles rūtiņas (*Checkboxes*).
- **Bināra loģiskā pazīme (Jā / Nē)**:
  - Ja piekrišana nosacījumiem — viena izvēles rūtiņa (*Checkbox*).
  - Ja divas līdzvērtīgas alternatīvas — divas radiopogas.
- **Datuma ievade**: Specializēts kalendāra komponents ar manuālas ievades iespēju (`DD.MM.GGGG`).
- **Adreses ievade**: **Obligāti** jāizmanto VISS Adrešu meklēšanas komponente (AMK), kas pieslēgta Valsts adrešu reģistram.

### Ekrāna izkārtojums un uzvedība
- **Navigācijas pogas**:
  - Izvietotas lapas apakšā.
  - Primārā darbības poga ("Tālāk", "Iesniegt") ir vizuāli izcelta kā noklusētā.
  - Sekundārā poga ("Atpakaļ", "Pārtraukt") ir neitrāla.
- **Aizliegtas liekas ritjoslas (*No Scrollbars*)**:
  - E-pakalpojuma pamatrāmī nedrīkst parādīties ne horizontālās, ne vertikālās ritjoslas, ko izraisa nepareizs layout vai fiksēti pikseļu augstumi (`overflow: hidden` vai dinamiska iframe/konteinera augstuma pielāgošana).
- **Paziņojumi un kļūdas**:
  - Kļūdu paziņojumiem par konkrētu lauku jāparādās tieši pie attiecīgā lauka (ar sarkanu ietvaru un paskaidrojošu tekstu).
  - Globālajiem paziņojumiem jābūt lapas augšpusē atbilstošā semantiskā krāsā (info, brīdinājums, kļūda, veiksme).
