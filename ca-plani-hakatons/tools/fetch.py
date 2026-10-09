"""Lapas ielāde. Lietojums:
    uv run fetch.py URL [--md] [--zenrows] [--out FILE]
Pēc noklusējuma mēģina tieši (curl-veidīgi, ignorējot sertifikātu kļūdas); ja atbilde nav 200 vai
--zenrows norādīts, iet caur ZenRows (mode=auto). --md atgriež lapu kā Markdown (tieši: vienkāršs
HTML->teksts ar saitēm; caur ZenRows: response_type=markdown).
"""
import sys as _s; _s.stdout.reconfigure(encoding="utf-8"); _s.stderr.reconfigure(encoding="utf-8")
import argparse, html, os, re, sys, time, urllib3
import requests

urllib3.disable_warnings()
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"


def direct(url: str):
    r = requests.get(url, headers={"User-Agent": UA, "Accept-Language": "lv,en;q=0.7"}, timeout=60, verify=False, allow_redirects=True)
    return r.status_code, r.url, r.text, r.headers.get("content-type", "")


def zenrows(url: str, md: bool):
    key = os.environ.get("ZENROWS_API_KEY")
    if not key:
        sys.exit("ZENROWS_API_KEY nav iestatīts")
    params = {"apikey": key, "url": url, "mode": "auto"}
    if md:
        params["response_type"] = "markdown"
    delay = 5
    for _ in range(6):
        r = requests.get("https://api.zenrows.com/v1/", params=params, timeout=180)
        if r.status_code == 200:
            return 200, r.headers.get("Zr-Final-Url", url), r.text, r.headers.get("content-type", "")
        if r.status_code in (429, 500, 502, 503, 504):
            time.sleep(delay); delay = min(delay * 2, 60); continue
        return r.status_code, url, r.text, ""
    return 599, url, "", ""


def html_to_md(h: str) -> str:
    h = re.sub(r"(?is)<(script|style|noscript|svg).*?</\1>", " ", h)
    h = re.sub(r"(?is)<a\s[^>]*href=[\"']([^\"']+)[\"'][^>]*>(.*?)</a>", lambda m: f"[{re.sub(r'<[^>]+>', '', m.group(2)).strip()}]({html.unescape(m.group(1))})", h)
    h = re.sub(r"(?i)<h([1-6])[^>]*>", lambda m: "\n" + "#" * int(m.group(1)) + " ", h)
    h = re.sub(r"(?i)</(h[1-6]|p|div|li|tr|section|article|br)[^>]*>", "\n", h)
    h = re.sub(r"(?i)<li[^>]*>", "- ", h)
    h = re.sub(r"<[^>]+>", " ", h)
    h = html.unescape(h)
    h = re.sub(r"[ \t]+", " ", h)
    h = re.sub(r"\n\s*\n+", "\n\n", h)
    return h.strip()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("url"); ap.add_argument("--md", action="store_true"); ap.add_argument("--zenrows", action="store_true"); ap.add_argument("--out")
    a = ap.parse_args()
    code, final, text, ctype = (0, a.url, "", "")
    if not a.zenrows:
        try:
            code, final, text, ctype = direct(a.url)
        except Exception as e:
            print(f"# tiešā ielāde neizdevās: {e}", file=sys.stderr)
    if a.zenrows or code != 200 or len(text) < 500:
        print(f"# tiešā ielāde: {code}; izmanto ZenRows", file=sys.stderr)
        code, final, text, ctype = zenrows(a.url, a.md)
        if a.md:
            out = text
        else:
            out = text
    else:
        out = html_to_md(text) if a.md else text
    print(f"# status={code} url={final} content-type={ctype}", file=sys.stderr)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(out)
        print(f"# saglabāts: {a.out} ({len(out)} rakstzīmes)", file=sys.stderr)
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(out)
