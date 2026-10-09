---
pasvaldiba_slug: jurmala
originals: N001_pielikums_apzinosanas_kartiba.pdf
originala_formats: pdf
originala_sha256: 1f4df0aed2bbbbe4cfd99a9a02fb3d4474e5a982c8b92e79e6270623e8d25fd2
avota_url: https://dokumenti.jurmala.lv/docs/m23/x/N001_pielikums.pdf
konvertets: 2026-09-12
konvertesanas_riks: pymupdf4llm
lpp: 1
skenets: False
teksta_rakstzimes: 1441
lpp_ar_atteliem: 1
layout: True
vizualas_lapas: [{'lpp': 1, 'atteli': 30, 'lieli_atteli': 30, 'zimejumi': 22, 'liknes': 0, 'krasaini_laukumi': 10, 'teksta_rakstzimes': 1441}]
---
<!-- lpp. 1 -->

Pielikums Jūrmalas domes 2023. gada 26. janvāra nolikumam Nr. 1 (protokols Nr. 1, 4. punkts)

### Komisijas apziņošanas kārtība

> **Shēma (lpp. 1): Civilās aizsardzības komisijas apziņošanas kārtība**  
> Tips: lēmumu pieņemšanas un operatīvās apziņošanas struktūrshēma.  
> Avots oriģinālā: Jūrmalas domes 2023. gada 26. janvāra nolikums Nr. 1 (protokols Nr. 1, 4. punkts).

```mermaid
flowchart TD
  A["Komisijas priekšsēdētājs<br/>(Jūrmalas domes priekšsēdētājs)<br/><b>pieņem lēmumu par komisijas apziņošanu</b>"] --> B["Komisijas sekretāre<br/><b>veic apziņošanu, zvanot vai sūtot SMS komisijas locekļiem</b>"]

  B --> C["Jūrmalas valstspilsētas pašvaldības izpilddirektors"]
  B --> D["VUGD Rīgas reģiona pārvaldes 4. daļas komandieris"]
  B --> E["VUGD Rīgas reģiona pārvaldes 4. daļas Bulduru posteņa komandieris"]
  B --> F["Jūrmalas pašvaldības policijas priekšnieks"]
  B --> G["Zemessardzes 17. kaujas atbalsta bataljona komandieris"]
  B --> H["SIA 'Jūrmalas slimnīca' valdes priekšsēdētājs"]
  B --> I["Jūrmalas administrācijas Attīstības pārvaldes<br/>Stratēģiskās plānošanas nodaļas vadītājs"]
  B --> J["Valsts policijas Rīgas reģiona pārvaldes<br/>Jūrmalas iecirkņa priekšnieks"]
```

> **Skaidrojums un procesa gaita:**  
> 1. Domes priekšsēdētājs pieņem operatīvo lēmumu par CAK sasaukšanu.  
> 2. Komisijas sekretāre caur balss zvaniem un SMS paralēli apziņo visus 8 komisijas locekļus (pašvaldības vadību, policiju, glābējus, slimnīcu un bruņotos spēkus).

### Ziņas piemēri:

> [!NOTE]
> **Pārbaudes ziņojums (SMS / e-pasts):**  
> *“Notiek apziņošanas kārtības pārbaude. Lūdzu, nosūtiet apstiprinājumu par ziņas saņemšanu uz tālr.nr.20000000 norādot vārdu un uzvārdu”*

> [!IMPORTANT]
> **Sēdes sasaukšanas ziņojums (Trauksme / Operatīvā sēde):**  
> *“Tiek organizēta Jūrmalas pilsētas sadarbības teritorijas civilās aizsardzības komisijas sēde 20___.gada _____, Jomas ielā 1/5, Jūrmalā, sēžu zālē. Lūdzu, nosūtiet apstiprinājumu par ierašanos vai arī informāciju par neierašanos uz tālr.nr.20000000 norādot vārdu un uzvārdu.”*

---

### Atvērto datu validācija un nākotnes rīka iespējas
- **Adrese:** Sēžu zāle Jomas ielā 1/5, Jūrmalā — validējama pret [VZD VARIS atvērtajiem datiem](../../avoti/kadastrs/VAR_ATVERTIE_DATI_MODELIS.md) (ēkas kods: `100083049`, koordinātas: 56.9723, 23.7915).
- **Infrastruktūra un glābēji:** VUGD 4. daļas un Bulduru posteņa izvietojums sasaistāms ar VUGD atvērto datu kopu un [LVC ceļu tīklu](../../avoti/celu-tikls/PUBLISKO_DATU_IESPEJAS.md) operatīvai nokļūšanai.
- **Automatizācija nākotnes rīkam:** Iespēja nosūtīt automatizētus API SMS brīdinājumus un saņemt apstiprinājumus digitālā CA vadības panelī.
