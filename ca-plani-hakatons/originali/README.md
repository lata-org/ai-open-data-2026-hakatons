# Oriģinālo dokumentu metadati

Šajā mapē ir tikai metadati par katras pašvaldības oriģinālajiem CA plāna failiem, nevis paši faili. Oriģināli (PDF, DOCX, ODT, kopā aptuveni 790 MB) repozitorijā netiek glabāti, lai komplekts paliktu viegls.

Katrā `<slug>/` mapē:

- `AVOTS.md`: pašvaldība, plāna nosaukums, kur publicēts, apstiprināšanas lēmumi, versiju vēsture un failu tabula ar avota URL un sha256.
- `faili.json`: tas pats failu saraksts mašīnlasāmā formā (`tools/download.py` izvade).

Oriģinālu var lejupielādēt pēc URL no `faili.json` un pārbaudīt ar sha256. Ja URL vairs nedarbojas, `AVOTS.md` parasti norāda arī alternatīvu saiti vai Wayback Machine kopiju.
