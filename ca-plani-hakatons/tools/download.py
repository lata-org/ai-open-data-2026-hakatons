"""Oriģināla lejupielāde ar metadatiem. Lietojums:
    uv run download.py URL --slug <pasvaldibas-slug> [--name faila_nosaukums] [--zenrows]
Saglabā failu mapē ../originali/<slug>/, nosaka formātu pēc satura (magic bytes), aprēķina
sha256, un pievieno ierakstu ../originali/<slug>/faili.json. Izdrukā JSON ar rezultātu.
"""
import sys as _s; _s.stdout.reconfigure(encoding="utf-8"); _s.stderr.reconfigure(encoding="utf-8")
import argparse, hashlib, json, os, re, sys, time, urllib.parse, urllib3
import requests

urllib3.disable_warnings()
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "originali"))


def sniff(data: bytes, ctype: str, url: str) -> str:
    head = data[:8]
    if head.startswith(b"%PDF"):
        return "pdf"
    if head.startswith(b"PK\x03\x04"):
        # OOXML vai ODF
        blob = data[:4000]
        if b"word/" in blob: return "docx"
        if b"xl/" in blob: return "xlsx"
        if b"ppt/" in blob: return "pptx"
        if b"mimetypeapplication/vnd.oasis.opendocument.text" in blob: return "odt"
        if b"mimetypeapplication/vnd.oasis.opendocument.spreadsheet" in blob: return "ods"
        return "zip"
    if head.startswith(b"\xd0\xcf\x11\xe0"):
        ext = os.path.splitext(urllib.parse.urlparse(url).path)[1].lower()
        return {".xls": "xls", ".ppt": "ppt"}.get(ext, "doc")
    if head.startswith(b"{\\rtf"):
        return "rtf"
    low = data[:2000].lower()
    if b"<html" in low or b"<!doctype html" in low:
        return "html"
    if "pdf" in ctype: return "pdf"
    return "bin"


def filename_from(resp, url: str, fmt: str, override: str | None) -> str:
    name = override
    if not name:
        cd = resp.headers.get("content-disposition", "")
        m = re.search(r"filename\*=(?:UTF-8|utf-8)''([^;]+)", cd) or re.search(r'filename="?([^";]+)"?', cd)
        if m:
            name = urllib.parse.unquote(m.group(1))
        else:
            name = urllib.parse.unquote(os.path.basename(urllib.parse.urlparse(url).path)) or "fails"
    name = re.sub(r'[\\/:*?"<>|]+', "_", name).strip() or "fails"
    if not os.path.splitext(name)[1] or fmt == "html" and not name.lower().endswith((".html", ".htm")):
        name = f"{name}.{fmt}" if fmt != "bin" else name
    return name


def fetch(url: str, use_zenrows: bool):
    if not use_zenrows:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=120, verify=False, allow_redirects=True, stream=False)
        return r
    key = os.environ.get("ZENROWS_API_KEY")
    if not key:
        sys.exit("ZENROWS_API_KEY nav iestatīts")
    delay = 5
    for _ in range(6):
        r = requests.get("https://api.zenrows.com/v1/", params={"apikey": key, "url": url, "mode": "auto"}, timeout=180)
        if r.status_code == 200:
            return r
        if r.status_code in (429, 500, 502, 503, 504):
            time.sleep(delay); delay = min(delay * 2, 60); continue
        return r
    return r


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("url"); ap.add_argument("--slug", required=True); ap.add_argument("--name"); ap.add_argument("--zenrows", action="store_true")
    ap.add_argument("--apraksts", default="", help="īss apraksts, piem. 'pamatdokuments' vai '1. pielikums'")
    a = ap.parse_args()
    r = fetch(a.url, a.zenrows)
    if r.status_code != 200:
        print(json.dumps({"ok": False, "status": r.status_code, "url": a.url}, ensure_ascii=False)); sys.exit(1)
    data = r.content
    ctype = r.headers.get("content-type", "")
    fmt = sniff(data, ctype, a.url)
    name = filename_from(r, a.url, fmt, a.name)
    d = os.path.join(ROOT, a.slug); os.makedirs(d, exist_ok=True)
    path = os.path.join(d, name)
    base, ext = os.path.splitext(name); i = 2
    while os.path.exists(path) and hashlib.sha256(open(path, "rb").read()).hexdigest() != hashlib.sha256(data).hexdigest():
        path = os.path.join(d, f"{base}_{i}{ext}"); i += 1
    open(path, "wb").write(data)
    meta = {
        "fails": os.path.basename(path), "formats": fmt, "content_type": ctype, "izmers_baiti": len(data),
        "sha256": hashlib.sha256(data).hexdigest(), "avota_url": a.url, "gala_url": getattr(r, "url", a.url),
        "lejupieladets": time.strftime("%Y-%m-%d %H:%M:%S"), "apraksts": a.apraksts, "originals": True,
        "caur_zenrows": a.zenrows,
    }
    jp = os.path.join(d, "faili.json")
    lst = json.load(open(jp, encoding="utf-8")) if os.path.exists(jp) else []
    lst = [x for x in lst if x.get("fails") != meta["fails"]] + [meta]
    json.dump(lst, open(jp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    meta["ok"] = True; meta["cels"] = path
    print(json.dumps(meta, ensure_ascii=False, indent=2))
