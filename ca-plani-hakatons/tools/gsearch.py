"""Tīmekļa meklēšana. Lietojums:
    uv run gsearch.py "meklējamā frāze" [--engine ddg|google|both] [--num 20] [--raw]
- ddg (noklusējums): DuckDuckGo HTML — dod ĪSTOS rezultātu URL, bez ZenRows izmaksām.
- google: Google caur ZenRows (LV proxy). Google slēpj īstos URL, tāpēc izdrukā virsrakstu,
  redzamo adreses ceļu (breadcrumb) un fragmentu — pēc tiem īsto URL jāatrod pašā vietnē vai ar ddg.
- both: abi pēc kārtas.
Atkārto pieprasījumu pie 429/5xx ar eksponenciālu gaidīšanu.
"""
import sys as _s; _s.stdout.reconfigure(encoding="utf-8"); _s.stderr.reconfigure(encoding="utf-8")
import argparse, html, os, re, sys, time, urllib.parse
import requests

API = "https://api.zenrows.com/v1/"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"


def ddg(query: str, num: int):
    delay = 3
    for _ in range(5):
        r = requests.get("https://html.duckduckgo.com/html/", params={"q": query, "kl": "lv-lv"}, headers={"User-Agent": UA}, timeout=60)
        if r.status_code == 200 and "result__a" in r.text:
            break
        if r.status_code == 200 and "No results" in r.text or "nav rezultātu" in r.text.lower():
            return []
        time.sleep(delay); delay *= 2
    else:
        return None
    out = []
    blocks = re.split(r'<div class="result results_links', r.text)[1:]
    for b in blocks[:num]:
        m = re.search(r'result__a" href="([^"]+)"[^>]*>(.*?)</a>', b, flags=re.S)
        if not m:
            continue
        href = html.unescape(m.group(1))
        q = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
        url = q.get("uddg", [href])[0]
        title = html.unescape(re.sub(r"<[^>]+>", "", m.group(2))).strip()
        s = re.search(r'result__snippet"[^>]*>(.*?)</a>', b, flags=re.S)
        snip = html.unescape(re.sub(r"<[^>]+>", "", s.group(1))).strip() if s else ""
        out.append({"title": title, "url": url, "snippet": snip})
    return out


def google_markdown(query: str, num: int) -> str:
    key = os.environ.get("ZENROWS_API_KEY")
    if not key:
        sys.exit("ZENROWS_API_KEY nav iestatīts")
    gurl = "https://www.google.com/search?" + urllib.parse.urlencode({"q": query, "hl": "lv", "gl": "lv", "num": num, "pws": 0})
    params = {"apikey": key, "url": gurl, "js_render": "true", "premium_proxy": "true", "proxy_country": "lv", "response_type": "markdown"}
    delay = 5
    for _ in range(6):
        r = requests.get(API, params=params, timeout=180)
        if r.status_code == 200:
            return r.text
        if r.status_code in (429, 500, 502, 503, 504, 422):
            time.sleep(delay); delay = min(delay * 2, 60); continue
        sys.exit(f"ZenRows kļūda {r.status_code}: {r.text[:300]}")
    sys.exit("ZenRows: pārāk daudz neveiksmīgu mēģinājumu")


def google_results(md: str):
    md = re.sub(r"!\[\]\(data:[^)]*\)", "", md)
    out = []
    # rezultāta bloks: [**Virsraksts** ... domēns ... https://dom › ceļš](goto)  \n\n domēns \n\n https://... \n\n fragments
    for m in re.finditer(r"\[\*\*(.+?)\*\*[^\]]*?(https?://\S+?(?: › [^\]\n]+)?)\s*\]\(http://www\.google\.com/goto[^)]*\)(.*?)(?=\n\[\*\*|\Z)", md, flags=re.S):
        title, crumb, rest = m.group(1).strip(), m.group(2).strip(), m.group(3)
        lines = [l.strip() for l in rest.strip().splitlines() if l.strip()]
        snip = " ".join(l for l in lines if not l.startswith("http") and "›" not in l and len(l) > 25)[:300]
        out.append({"title": title, "crumb": crumb, "snippet": snip})
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("query"); ap.add_argument("--engine", default="ddg", choices=["ddg", "google", "both"])
    ap.add_argument("--num", type=int, default=20); ap.add_argument("--raw", action="store_true")
    a = ap.parse_args()
    if a.engine in ("ddg", "both"):
        res = ddg(a.query, a.num)
        print(f"## DuckDuckGo: {a.query}")
        if res is None:
            print("(DDG neatbildēja — mēģini --engine google)")
        elif not res:
            print("(nav rezultātu)")
        for r in res or []:
            print(f"- {r['title']}\n  {r['url']}\n  {r['snippet']}")
        print()
    if a.engine in ("google", "both"):
        md = google_markdown(a.query, a.num)
        print(f"## Google (caur ZenRows): {a.query}")
        if a.raw:
            print(md)
        else:
            res = google_results(md)
            if not res:
                print("(rezultātu bloki nav atpazīti — mēģini --raw)")
            for r in res:
                print(f"- {r['title']}\n  {r['crumb']}\n  {r['snippet']}")
