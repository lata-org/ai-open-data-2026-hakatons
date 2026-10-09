# Rīki plānu lejupielādei un konvertēšanai

Visi skripti darbojas ar `uv run <skripts.py>` no šīs mapes. Atkarības ir `pyproject.toml`.

| Skripts | Ko dara |
|---|---|
| `fetch.py URL [--md]` | Ielādē lapu; ja tiešā ielāde neizdodas vai norādīts `--zenrows`, iet caur ZenRows. |
| `gsearch.py "frāze"` | Tīmekļa meklēšana (DuckDuckGo vai Google caur ZenRows), lai atrastu plāna publikācijas lapu. |
| `download.py URL --slug <slug>` | Lejupielādē oriģinālu uz `../originali/<slug>/`, nosaka formātu, aprēķina sha256 un papildina `faili.json`. |
| `convert.py <fails> --slug <slug>` | Konvertē PDF, DOCX, ODT, DOC, XLSX uz Markdown mapē `../markdown/<slug>/`. PDF ar pymupdf4llm, pārējie ar pandoc vai LibreOffice. |
| `build_registrs.py` | Veido reģistra CSV un README no konvertēšanas rezultātiem. |

ZenRows režīmam vajadzīgs vides mainīgais `ZENROWS_API_KEY`. `convert.py` uz Windows sagaida LibreOffice ceļā `C:\Program Files\LibreOffice\program\soffice.exe` un pandoc komandrindā.

Detalizēta konvertēšanas metodika un kvalitātes prasības: `../dokumentacija/UZDEVUMS_KONVERTESANA.md`.
