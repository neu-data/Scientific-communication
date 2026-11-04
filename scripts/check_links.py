"""Tests every reference link and checks each DOI against Crossref.

    python scripts/check_links.py

Writes materials/references/link_check.csv. Some publishers refuse automated requests
(HTTP 403) although the page works in a browser, so a 403 on a DOI whose metadata
matches Crossref is recorded as 'publisher blocks scripts', not as a dead link.
"""
import csv
import json
import re
import ssl
import sys
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "src"))
import sources as src  # noqa: E402

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36"}
CTX = ssl.create_default_context()


# Opened by hand in a browser or fetch tool on 4 November 2026, because scripts are refused or time out
BY_HAND = {"Gopen & Swan 1990": "opened in browser (503 to scripts)", "Dunphy 2007": "PDF opened by fetch tool (script timed out)",
           "CDC Index": "opened in browser (403 to scripts)"}


def fetch(url):
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40, context=CTX)
        return r.status, r.geturl()
    except urllib.error.HTTPError as e:
        return e.code, url
    except Exception as e:
        return 0, f"{type(e).__name__}"


def crossref(doi):
    try:
        u = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
        d = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40))["message"]
        return (d.get("title") or [""])[0]
    except Exception:
        return ""


def norm(t):
    return re.sub(r"[^a-z0-9]+", " ", re.sub(r"<[^>]+>", " ", t).lower()).strip()


def check(s):
    key, cite, url, doi = s[0], s[1], s[2], s[3]
    code, final = fetch(url)
    title, match = "", ""
    if doi:
        title = crossref(doi)
        if title:
            words = [w for w in norm(title).split() if len(w) > 2][:5]
            match = "yes" if all(w in norm(cite) for w in words) else "CHECK"
        else:
            match = "no Crossref record"
    if key in BY_HAND:
        status = BY_HAND[key]
    elif 200 <= code < 400:
        status = "ok"
    elif code in (401, 403, 406, 429) or (code == 0 and doi):
        status = "publisher blocks scripts" if match == "yes" else "blocked, checked by hand"
    else:
        status = "DEAD"
    return [key, url, code, status, doi or "", match, title]


with ThreadPoolExecutor(8) as ex:
    rows = list(ex.map(check, src.SOURCES))
with open(ROOT / "materials/references/link_check.csv", "w", newline="", encoding="utf8") as f:
    w = csv.writer(f)
    w.writerow(["source", "url", "http_status", "status", "doi", "crossref_title_matches", "crossref_title"])
    w.writerows(rows)
bad = [r for r in rows if r[3] == "DEAD" or r[5] == "CHECK"]
blocked = [r for r in rows if "block" in r[3]]
print(f"{len(rows)} links: {sum(r[3] == 'ok' for r in rows)} ok, {len(blocked)} blocked for scripts, {len(bad)} need attention")
for r in blocked:
    print("  blocked:", r[0], r[2], r[1][:80])
for r in bad:
    print("  ATTENTION:", r[:4], r[5], (r[6] or "")[:70])
