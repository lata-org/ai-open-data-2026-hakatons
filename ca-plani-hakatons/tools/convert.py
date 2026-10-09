"""Oriģināla konvertēšana uz Markdown. Lietojums:
    uv run convert.py <ceļš uz oriģinālu> --slug <pasvaldibas-slug> [--out <md ceļš>]
Rezultāts: ../markdown/<slug>/<faila_nosaukums>.md ar YAML galveni un JSON kopsavilkums stdout.
PDF -> pymupdf4llm (+pymupdf-layout), pa lapām ar <!-- lpp. N --> marķieriem; virsrakstu līmeņi pēc
numerācijas (1. -> ##, 1.2. -> ###, 1.2.3. -> ####), romiešu cipari apvienoti ar nākamo virsrakstu.
Ja PDF bez teksta slāņa -> skenets=true (teksts netiek izgūts).
DOCX/ODT/HTML/RTF -> pandoc (gfm). DOC/XLS/PPT/PPTX -> LibreOffice -> DOCX/XLSX/PDF -> tālāk.
XLSX -> openpyxl tabulas.
"""
import sys as _s; _s.stdout.reconfigure(encoding="utf-8"); _s.stderr.reconfigure(encoding="utf-8")
import argparse, hashlib, json, os, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
MD_ROOT = os.path.abspath(os.path.join(HERE, "..", "markdown"))
SOFFICE = r"C:\Program Files\LibreOffice\program\soffice.exe"
PANDOC = "pandoc"

ROMAN = re.compile(r"^(?:[IVX]{1,5})\.?$")
NUM = re.compile(r"^(\d{1,2}(?:\.\d{1,2}){0,4})\.?\s*(.*)$")


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)


def soffice_convert(path: str, target: str, outdir: str) -> str:
    r = run([SOFFICE, "--headless", "--norestore", "--convert-to", target, "--outdir", outdir, path], timeout=300)
    base = os.path.splitext(os.path.basename(path))[0]
    out = os.path.join(outdir, f"{base}.{target.split(':')[0]}")
    if not os.path.exists(out):
        raise RuntimeError(f"LibreOffice neizdevās: {r.stdout} {r.stderr}")
    return out


def clean_heading_text(t: str) -> str:
    t = t.strip()
    t = t.replace("**", "")
    t = re.sub(r"\s{2,}", " ", t)
    return t.strip()


def postprocess_page(text: str) -> str:
    lines = text.split("\n")
    out = []
    pending_roman = None
    for ln in lines:
        s = ln.rstrip()
        if re.match(r"^\*\*==> picture .*omitted <==\*\*$", s.strip()):
            out.append("*[attēls izlaists]*")
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            txt = clean_heading_text(m.group(2))
            if not txt:
                continue
            if ROMAN.match(txt):
                pending_roman = txt.rstrip(".")
                continue
            level = None
            nm = NUM.match(txt)
            if nm and nm.group(2):
                depth = nm.group(1).count(".") + 1
                level = min(1 + depth, 6)
            elif pending_roman:
                level = 2
            if pending_roman:
                txt = f"{pending_roman}. {txt}"
                pending_roman = None
            if level is None:
                level = 3  # nenumurēts virsraksts vai tabulas nosaukums
            out.append("#" * level + " " + txt)
            continue
        if pending_roman and s.strip():
            out.append(f"## {pending_roman}.")
            pending_roman = None
        out.append(s)
    while out and not out[-1].strip():
        out.pop()
    if out and re.fullmatch(r"\d{1,3}", out[-1].strip()):
        out.pop()  # lapas numurs lapas beigās
    body = "\n".join(out)
    body = re.sub(r"\n{3,}", "\n\n", body)
    return body.strip()


def pdf_to_md(path: str):
    import pymupdf
    try:
        import pymupdf.layout  # noqa: F401  uzlabota izkārtojuma analīze; JĀIMPORTĒ pirms pymupdf4llm
        layout = True
    except Exception:
        layout = False
    import pymupdf4llm
    doc = pymupdf.open(path)
    n = len(doc)
    text_chars = sum(len(p.get_text()) for p in doc)
    # vizuālo elementu karte: attēli (rastra) un zīmējumi (vektoru shēmas, kartes, diagrammas)
    vis = []
    for i, p in enumerate(doc):
        imgs = p.get_images(full=True)
        big = 0
        for im in imgs:
            try:
                w, h = im[2], im[3]
                if w * h >= 40000:  # >= ~200x200 px – nav ikona/logo
                    big += 1
            except Exception:
                pass
        dr = curves = colored = 0
        try:
            for d in p.get_drawings():
                dr += 1
                curves += sum(1 for it in d.get("items", []) if it and it[0] == "c")
                f = d.get("fill")
                if f and len(f) >= 3 and (max(f) - min(f)) > 0.12:  # krāsains (ne pelēks/balts) aizpildījums
                    colored += 1
        except Exception:
            pass
        tx = len(p.get_text())
        # shēma/karte/diagramma: līknes vai krāsaini laukumi; tabulas dod tikai melnbaltas taisnas līnijas
        if big or curves >= 6 or colored >= 3 or (tx < 80 and (imgs or dr)):
            vis.append({"lpp": i + 1, "atteli": len(imgs), "lieli_atteli": big, "zimejumi": dr, "liknes": curves,
                        "krasaini_laukumi": colored, "teksta_rakstzimes": tx})
    img_pages = sum(1 for p in doc if len(p.get_images()) > 0)
    doc.close()
    scanned = n > 0 and text_chars / n < 80
    if scanned:
        body = f"> **UZMANĪBU:** PDF bez teksta slāņa (skenēts dokuments, {n} lpp.). Automātiska teksta izguve nav iespējama — teksts jāatveido vizuāli (modelim lasot lapas).\n"
        return body, {"lpp": n, "skenets": True, "teksta_rakstzimes": text_chars, "lpp_ar_atteliem": img_pages, "vizualas_lapas": vis}
    chunks = pymupdf4llm.to_markdown(path, page_chunks=True, write_images=False, show_progress=False)
    vis_by = {v["lpp"]: v for v in vis}
    parts = []
    for i, c in enumerate(chunks):
        pn = c["metadata"].get("page_number", i + 1)
        t = postprocess_page(c["text"])
        v = vis_by.get(pn)
        if v:
            t += (f"\n\n> **[VIZUĀLI ELEMENTI lpp. {pn}: {v['lieli_atteli']} lieli attēli, {v['zimejumi']} vektoru zīmējumi — "
                  f"JĀAPSKATA vizuāli un jāapraksta / jāatveido kā mermaid shēma vai tabula]**")
        parts.append(f"<!-- lpp. {pn} -->\n\n{t}\n")
    body = "\n".join(parts)
    return body, {"lpp": n, "skenets": False, "teksta_rakstzimes": text_chars, "lpp_ar_atteliem": img_pages, "layout": layout,
                  "vizualas_lapas": vis}


def pandoc_to_md(path: str, fmt: str):
    r = run([PANDOC, "-f", fmt, "-t", "gfm", "--wrap=none", "--markdown-headings=atx", path], timeout=300)
    if r.returncode != 0:
        raise RuntimeError(f"pandoc kļūda: {r.stderr}")
    body = r.stdout
    body = re.sub(r"!\[[^\]]*\]\([^)]*\)", "*[attēls izlaists]*", body)
    return body, {}


def xlsx_to_md(path: str):
    import openpyxl
    wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
    out = []
    for ws in wb.worksheets:
        rows = [[("" if v is None else str(v).replace("\n", " ").replace("|", "\\|")) for v in r] for r in ws.iter_rows(values_only=True)]
        rows = [r for r in rows if any(c.strip() for c in r)]
        if not rows:
            continue
        w = max(len(r) for r in rows)
        rows = [r + [""] * (w - len(r)) for r in rows]
        out.append(f"## Lapa: {ws.title}\n")
        out.append("| " + " | ".join(rows[0]) + " |")
        out.append("|" + "---|" * w)
        for r in rows[1:]:
            out.append("| " + " | ".join(r) + " |")
        out.append("")
    return "\n".join(out), {"lapas": len(wb.worksheets)}


def convert(path: str, tmpdir: str):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        return pdf_to_md(path), "pymupdf4llm"
    if ext in (".docx", ".odt", ".rtf", ".html", ".htm"):
        fmt = {".docx": "docx", ".odt": "odt", ".rtf": "rtf", ".html": "html", ".htm": "html"}[ext]
        return pandoc_to_md(path, fmt), f"pandoc({fmt})"
    if ext in (".doc", ".wpd"):
        p = soffice_convert(path, "docx", tmpdir)
        return pandoc_to_md(p, "docx"), "libreoffice->docx->pandoc"
    if ext == ".xlsx":
        return xlsx_to_md(path), "openpyxl"
    if ext in (".xls", ".ods"):
        p = soffice_convert(path, "xlsx", tmpdir)
        return xlsx_to_md(p), "libreoffice->xlsx->openpyxl"
    if ext in (".ppt", ".pptx"):
        p = soffice_convert(path, "pdf", tmpdir)
        return pdf_to_md(p), "libreoffice->pdf->pymupdf4llm"
    raise RuntimeError(f"neatbalstīts formāts: {ext}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("path"); ap.add_argument("--slug", required=True); ap.add_argument("--out")
    a = ap.parse_args()
    src = os.path.abspath(a.path)
    slug_dir = os.path.join(MD_ROOT, a.slug); os.makedirs(slug_dir, exist_ok=True)
    tmpdir = os.path.join(slug_dir, ".tmp"); os.makedirs(tmpdir, exist_ok=True)
    out = a.out or os.path.join(slug_dir, os.path.splitext(os.path.basename(src))[0] + ".md")
    (body, info), tool = convert(src, tmpdir)
    sha = hashlib.sha256(open(src, "rb").read()).hexdigest()
    meta = {}
    fj = os.path.join(os.path.dirname(src), "faili.json")
    if os.path.exists(fj):
        for x in json.load(open(fj, encoding="utf-8")):
            if x.get("fails") == os.path.basename(src):
                meta = x
    head = [
        "---",
        f"pasvaldiba_slug: {a.slug}",
        f"originals: {os.path.basename(src)}",
        f"originala_formats: {os.path.splitext(src)[1].lstrip('.').lower()}",
        f"originala_sha256: {sha}",
        f"avota_url: {meta.get('avota_url', '')}",
        f"konvertets: {time.strftime('%Y-%m-%d')}",
        f"konvertesanas_riks: {tool}",
    ] + [f"{k}: {v}" for k, v in info.items()] + ["---", ""]
    open(out, "w", encoding="utf-8").write("\n".join(head) + body)
    headings = re.findall(r"^#{1,6} .+", body, flags=re.M)
    tables = len(re.findall(r"^\|.*\|\s*$", body, flags=re.M))
    summary = {"ok": True, "md": out, "riks": tool, "rakstzimes": len(body), "virsraksti": len(headings),
               "tabulu_rindas": tables, **info}
    print(json.dumps(summary, ensure_ascii=False, indent=2))
