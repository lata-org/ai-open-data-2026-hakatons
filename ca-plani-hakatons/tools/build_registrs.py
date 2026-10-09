"""Reģistra un README veidošana no workflow rezultātiem un failu metadatiem.
    uv run build_registrs.py <rezultati.json>
Izveido ../registrs.csv (viena rinda uz failu), ../registrs_kopsavilkums.csv (viena rinda uz pašvaldību)
un ../README.md.
"""
import sys as _s; _s.stdout.reconfigure(encoding="utf-8")
import csv, json, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
ORIG = os.path.join(ROOT, "originali")
MD = os.path.join(ROOT, "markdown")


def load_faili(slug):
    p = os.path.join(ORIG, slug, "faili.json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else []


def md_for(slug, fails):
    base = os.path.splitext(fails)[0] + ".md"
    p = os.path.join(MD, slug, base)
    return f"markdown/{slug}/{base}" if os.path.exists(p) else ""


def main(res_path):
    res = json.load(open(res_path, encoding="utf-8"))
    items = json.load(open(os.path.join(ROOT, "darba_saraksts.json"), encoding="utf-8"))
    by_slug = {r["slug"]: r for r in res if r}
    rows, summ = [], []
    for it in items:
        r = by_slug.get(it["slug"])
        d = (r or {}).get("atrasana") or {}
        k = (r or {}).get("konvertesana") or {}
        faili = load_faili(it["slug"])
        kval = {x["originals"]: x for x in (k.get("konvertetie") or [])}
        struct = f"markdown/{it['slug']}/STRUKTURA.md" if os.path.exists(os.path.join(MD, it["slug"], "STRUKTURA.md")) else ""
        summ.append({
            "pasvaldiba": it["pasvaldiba"], "tips": it["tips"], "slug": it["slug"], "majas_lapa": it["majas_lapa"],
            "statuss": d.get("statuss", "nav_apstradats"), "plana_nosaukums": d.get("plana_nosaukums", ""),
            "publicesanas_lapa": d.get("publicesanas_lapa", ""), "publicesanas_vieta": d.get("publicesanas_vieta_apraksts", ""),
            "apstiprinats": d.get("apstiprinats", ""), "versija": d.get("versija", ""),
            "kopigs_ar": ";".join(d.get("kopigs_ar") or []), "ierobezota_pieejamiba": d.get("ierobezota_pieejamiba", ""),
            "failu_skaits": len(faili), "formati": ";".join(sorted({f["formats"] for f in faili})),
            "originalu_mape": f"originali/{it['slug']}/" if faili else "", "avots_md": f"originali/{it['slug']}/AVOTS.md" if os.path.exists(os.path.join(ORIG, it["slug"], "AVOTS.md")) else "",
            "struktura_md": struct, "konvertesanas_problemas": " | ".join(k.get("problemas") or []), "piezimes": d.get("piezimes", ""),
        })
        for f in faili:
            q = kval.get(f["fails"], {})
            rows.append({
                "pasvaldiba": it["pasvaldiba"], "slug": it["slug"], "fails": f["fails"], "apraksts": f.get("apraksts", ""),
                "formats": f["formats"], "izmers_baiti": f["izmers_baiti"], "sha256": f["sha256"], "avota_url": f["avota_url"],
                "lejupieladets": f.get("lejupieladets", ""), "originals": f"originali/{it['slug']}/{f['fails']}",
                "markdown": md_for(it["slug"], f["fails"]), "konvertesanas_kvalitate": q.get("kvalitate", ""), "konvertesanas_piezimes": q.get("piezimes", ""),
            })
    with open(os.path.join(ROOT, "registrs.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()) if rows else ["pasvaldiba"]); w.writeheader(); w.writerows(rows)
    with open(os.path.join(ROOT, "registrs_kopsavilkums.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(summ[0].keys())); w.writeheader(); w.writerows(summ)

    n_atr = sum(1 for s in summ if s["statuss"] == "atrasts")
    n_dal = sum(1 for s in summ if s["statuss"] == "atrasts_daleji")
    n_nav = sum(1 for s in summ if s["statuss"] not in ("atrasts", "atrasts_daleji"))
    L = []
    L.append("# Latvijas pašvaldību civilās aizsardzības plāni\n")
    L.append(f"Stāvoklis uz {time.strftime('%Y-%m-%d')}. Pašvaldības: {len(summ)} (7 valstspilsētas + 35 novadi). "
             f"Plāns atrasts: **{n_atr}**, daļēji: **{n_dal}**, nav atrasts: **{n_nav}**.\n")
    L.append("## Mapes struktūra\n")
    L.append("| Ceļš | Saturs |\n|---|---|")
    L.append("| `pasvaldibas.csv`, `pasvaldibas.md` | 42 pašvaldību saraksts ar pārbaudītām mājas lapām |")
    L.append("| `registrs_kopsavilkums.csv` | viena rinda uz pašvaldību: statuss, publicēšanas vieta, apstiprināšana, formāti, saites uz mapēm |")
    L.append("| `registrs.csv` | viena rinda uz katru lejupielādēto failu: avota URL, formāts, sha256, oriģināla un Markdown ceļš, konvertēšanas kvalitāte |")
    L.append("| `originali/<slug>/` | **ORIĢINĀLI** — nemainīti lejupielādētie faili; `faili.json` (metadati, sha256), `AVOTS.md` (kur publicēts, meklēšanas gaita) |")
    L.append("| `markdown/<slug>/` | konvertētie Markdown faili (YAML galvene ar avotu un sha256; PDF ar `<!-- lpp. N -->` marķieriem) un `STRUKTURA.md` (detalizēts dokumenta struktūras apraksts) |")
    L.append("| `avoti/` | VZD adrešu reģistra CSV un VUGD pašvaldību CA plānu saraksta kopija |")
    L.append("| `tools/` | uv projekts: `gsearch.py` (DDG/Google), `fetch.py`, `download.py`, `convert.py`, `build_registrs.py` |")
    L.append("| `darba_saraksts.json` | workflow ievade (slug, domēns, VUGD norāde, kopīgo plānu partneri) |\n")
    L.append("## Kopsavilkums pa pašvaldībām\n")
    L.append("| Pašvaldība | Statuss | Kur publicēts | Apstiprināts | Faili (formāti) | Kopīgs ar | Oriģināli | Struktūra |")
    L.append("|---|---|---|---|---|---|---|---|")
    for s in summ:
        lapa = f"[saite]({s['publicesanas_lapa']})" if s["publicesanas_lapa"] else ""
        orig = f"[{s['failu_skaits']}]({s['originalu_mape']})" if s["originalu_mape"] else "0"
        strukt = f"[STRUKTURA]({s['struktura_md']})" if s["struktura_md"] else ""
        L.append(f"| {s['pasvaldiba']} | {s['statuss']} | {lapa} {s['publicesanas_vieta'][:80]} | {s['apstiprinats'][:60]} | {orig} ({s['formati']}) | {s['kopigs_ar']} | {s['avots_md'] and '[AVOTS](' + s['avots_md'] + ')'} | {strukt} |")
    L.append("\n## Metodika\n")
    L.append("1. Pašvaldību saraksts no VZD adrešu reģistra (`avoti/aw_novads.csv`, `avoti/aw_pilseta.csv`), mājas lapas pārbaudītas ar HTTP pieprasījumiem.")
    L.append("2. Katrai pašvaldībai atsevišķs aģents meklēja plānu: VUGD saraksts (`avoti/vugd_pasvaldibu_ca_plani_2026-09-11.md`), pašvaldības mājas lapa, DuckDuckGo, Google (caur ZenRows, LV proxy), domes lēmumi. Neatrastajiem — otrs aģents ar citu pieeju.")
    L.append("3. Oriģināli lejupielādēti nemainīti (`tools/download.py`): formāts noteikts pēc satura, sha256 ierakstīts `faili.json`.")
    L.append("4. Konvertēšana (`tools/convert.py`): PDF → pymupdf4llm + pymupdf-layout (pa lapām, virsrakstu līmeņi no numerācijas); DOCX/ODT → pandoc; DOC/XLS/PPT → LibreOffice → tālāk; XLSX → openpyxl. Pēc tam aģents salīdzināja ar oriģinālu, laboja struktūru un uzrakstīja `STRUKTURA.md`.")
    L.append("5. Skenētiem PDF (bez teksta slāņa) OCR nav veikts — tie atzīmēti `registrs.csv` ar kvalitāti `skenets`.")
    open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(json.dumps({"pasvaldibas": len(summ), "atrasts": n_atr, "daleji": n_dal, "nav": n_nav, "faili": len(rows)}, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1])
