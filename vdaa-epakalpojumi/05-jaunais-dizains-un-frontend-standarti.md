# 5. Jaunais Latvija.gov.lv dizains un Frontend standarti

## 5.1. Pāreja uz jauno vienoto dizainu un termiņi

Latvijas valsts portāls Latvija.gov.lv un VDAA e-pakalpojumu platforma pāriet uz modernizētu dizaina un lietojamības ietvaru.

> [!IMPORTANT]
> **Kritiskie nosacījumi un termiņi:**
> 1. **Jaunu e-pakalpojumu izstrādē vai esošo būtiskā pilnveidē obligāti jāizmanto jaunais dizains.**
> 2. **Vecais (oranžais) dizains tiek uzturēts tikai līdz 2027. gada 30. jūnijam.** Pēc šī datuma tā atbalsts tiek pilnībā pārtraukts.
> 3. Visām iestādēm plānveidīgi jāieplāno budžets un izstrādes resursi esošo e-pakalpojumu pārcelšanai uz jauno dizainu.

### Piekļuves saņemšana jaunajam dizainam
Jaunais dizains un tā repozitoriji atrodas kontrolētā piekļuvē. Lai saņemtu piekļuvi veidnēm un bibliotēkām:
- Iestāde vai izstrādātājs nosūta e-pastu uz: **`atbalsts@vdaa.gov.lv`**
- E-pasta temats: **"Piekļuves e-pakalpojumu jaunajam dizainam"**
- VDAA nosūta tehniskās veidnes, piekļuves Git un dokumentāciju.

---

## 5.2. Tehnoloģiskās platformas un Storybook resursi

VDAA nodrošina divas oficiāli atbalstītas tehnoloģiju bāzes:

### 1. Vienas lapas lietotne — SPA (*Single Page Application*)
- **Tehnoloģija**: **ReactJS** (ar TypeScript vai modernu JavaScript ES6+).
- **Pielietojums**: Sarežģīti, dinamiski e-pakalpojumi ar daudziem interaktīviem stāvokļiem, kartēm, aprēķiniem un tūlītēju lauku validāciju.
- **Storybook kontroļu katalogs**:
  `https://eservices-test.vraa.gov.lv/EservicePlatform.Controls.React.Full.Dev/?path=/story/atoms-colors--brand-colors`
- **Piemēri portāla testa vidē**:
  `https://portal-test.vraa.gov.lv/Search/?sp=reactdev`

### 2. Vairāku lapu lietotne — MPA (*Multiple Page Application*)
- **Tehnoloģija**: **Microsoft .NET Core MVC** (C#).
- **Pielietojums**: Pakāpeniski formu un anketu pakalpojumi, klasiska servera puses renderēšana.
- **HTML/CSS Storybook kontroļu bāze**:
  `https://eservices-test.vraa.gov.lv/EservicePlatform.Controls.Html.Full.Dev/?path=/story/atoms-colors--brand-colors`
- **MVC bibliotēkas Helpers dokumentācija**:
  `https://eservices-test.vraa.gov.lv/EservicePlatform.Controls.Mvc.Dev/doc/index.html`
- **Piemēri portāla testa vidē**:
  `https://portal-test.vraa.gov.lv/Search/?sp=mvcdev`

---

## 5.3. Piekļūstamības (Accessibility) standarti — WCAG 2.1 AA

Atbilstoši MK noteikumiem Nr. 445 un Eiropas standartam EN 301 549, visiem e-pakalpojumiem obligāti jānodrošina atbilstība **W3C Web Content Accessibility Guidelines (WCAG) 2.1 AA līmenim**.

### Galvenās piekļūstamības prasības:

1. **Krāsu kontrasts**:
   - Pamattekstam attiecība pret fonu vismaz **4.5:1**.
   - Lielam tekstam (virs 18pt vai 14pt bold) un grafiskajām vadīklām vismaz **3:1**.
   - Krāsa nedrīkst būt vienīgais veids, kā tiek nodota informācija (piemēram, kļūdas laukam papildus sarkanai krāsai jābūt brīdinošai ikonai un teksta paziņojumam).

2. **Navigācija tikai ar tastatūru**:
   - Visiem elementiem (saitēm, pogām, ievadlaukumiem, nolaižamajiem sarakstiem) jābūt sasniedzamiem un aktivizējamiem tikai ar tastatūru (`Tab`, `Shift+Tab`, `Enter`, `Space`, bultiņas, `Esc`).
   - Fokusa indikatoram (`focus outline`) jābūt skaidri redzamam un kontrastējošam. Aizliegts lietot `outline: none` bez alternatīva stila!

3. **Ekrāna lasītāju (*Screen Readers*) atbalsts**:
   - Semantisks HTML5 marķējums (`<main>`, `<nav>`, `<form>`, `<fieldset>`, `<legend>`, `<label>`).
   - Visiem attēliem informatīvs `alt` teksts (dekoratīviem attēliem `alt=""`).
   - Formu ievadlaukumiem obligāti piesaistīts `<label for="id">` vai `aria-label`.
   - Dinamiskām izmaiņām (piemēram, jaunas ziņas ielāde bez lapas pārlādes) jāizmanto `aria-live="polite"` vai `role="alert"`.

4. **Teksta mērogošana un vājredzīgo režīms**:
   - Palielinot teksta izmēru līdz 200%, lapas saturs nedrīkst pārklāties, pazust vai radīt horizontālu ritjoslu.
   - Pakalpojumam jānodrošina korekta darbība vājredzīgo režīmā (augsta kontrasta režīms).

5. **Atsaucīgs (adaptīvais) izkārtojums (*Responsive design*)**:
   - Saskarnei nevainojami jādarbojas uz ekrāna platumiem no 320px (viedtālruņi) līdz 4K monitoriem.
   - Pamatlapā nedrīkst rasties horizontālā ritjosla (`overflow-x`).

---

## 5.4. Satura un teksta standarti

- **Lietišķais stils**: Formāls, bet vienkāršs un cieņpilns ("Jūs" forma).
- **Vienota terminoloģija**: Viens un tas pats jēdziens visā pakalpojumā jāsauc vienādi.
- **Tekstu lokalizācija kā resursi**: Visiem ekrānos redzamajiem tekstiem jābūt nodalītiem resursu failos (`.resx` vai JSON lokalizācijas failos), lai nodrošinātu valodu maiņu (LV / EN) un vienkāršu labošanu bez koda pārkompilēšanas.
- **Kļūdu ziņojumu struktūra**:
  - Kļūdas ziņojumam skaidri jānorāda:
    1. Kas tieši ir noticis?
    2. Kāpēc tā noticis?
    3. Ko lietotājam darīt, lai kļūdu novērstu?
  - *Slikts piemērs*: "Kļūda sistēmā".
  - *Labs piemērs*: "Norādītais personas kods nav atrasts Iedzīvotāju reģistrā. Pārbaudiet ievadītos datus vai sazinieties ar PMLP."
