"""Collecte d'offres d'alternance cloud / infra / DevOps en Île-de-France.

Sources : HelloWork (recherche), France Travail (recherche), AXA (recrutement.axa.fr).
Usage : python3 -I collect.py <out_dir>
"""
import html
import json
import re
import subprocess
import sys
import time
import urllib.parse

OUT = sys.argv[1]
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"


def fetch(url):
    r = subprocess.run(
        ["curl", "-sSL", "--max-time", "60", "-A", UA, url],
        capture_output=True,
    )
    return r.stdout.decode("utf-8", "replace")


def clean(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


offers = {}


def add(o):
    key = o["source"] + ":" + o["id"]
    if key not in offers:
        offers[key] = o
    else:
        offers[key]["queries"] = sorted(set(offers[key]["queries"]) | set(o["queries"]))


# ---------------- HelloWork ----------------
HW_KEYWORDS = [
    "ingénieur cloud", "cloud engineer", "cloud computing", "devops", "azure", "aws",
    "terraform", "kubernetes", "sre", "infrastructure cloud", "cloud ops",
    "ingénieur infrastructure", "ingénieur système", "platform engineer", "finops",
    "sécurité cloud", "ingénieur de production", "administrateur systèmes et réseaux",
]


def hellowork():
    for kw in HW_KEYWORDS:
        for page in range(1, 6):
            url = (
                "https://www.hellowork.com/fr-fr/emploi/recherche.html?"
                + urllib.parse.urlencode({"k": kw, "l": "Île-de-France", "c": "Alternance", "p": page})
            )
            doc = fetch(url)
            cards = doc.split('data-cy="serpCard"')[1:]
            if not cards:
                break
            for c in cards:
                m = re.search(r'href="(/fr-fr/emplois/(\d+)\.html)"\s+title="([^"]*)"', c)
                if not m:
                    continue
                spans = re.findall(r'<span class="[^"]*">([^<]*)</span>', c)
                title = clean(spans[0]) if spans else clean(m.group(3))
                company = clean(spans[1]) if len(spans) > 1 else ""
                loc = re.search(r'data-cy="localisationCard"\s*>\s*([^<]+)<', c)
                contract = re.search(r'data-cy="contractCard"\s*>\s*([^<]+)<', c)
                age = re.search(r'text-grey-500 pl-1 pt-1">([^<]+)<', c)
                salary = re.search(r'typo-s-bold w-fit border-0">([^<]+)<', c)
                add({
                    "source": "HelloWork", "id": m.group(2), "title": title, "company": company,
                    "location": clean(loc.group(1)) if loc else "", "contract": clean(contract.group(1)) if contract else "",
                    "date": clean(age.group(1)) if age else "", "salary": clean(salary.group(1)) if salary else "",
                    "url": "https://www.hellowork.com" + m.group(1), "queries": [kw],
                })
            if len(cards) < 20:
                break
            time.sleep(1)


# ---------------- France Travail ----------------
FT_KEYWORDS = [
    "alternance cloud", "alternance devops", "alternance azure", "alternance aws",
    "alternance infrastructure", "alternance kubernetes", "alternance terraform",
    "alternance sre", "apprentissage cloud", "apprentissage devops", "alternance cloud computing",
    "alternance ingenieur systeme", "alternance finops", "alternance ingenieur production",
]


def francetravail():
    for kw in FT_KEYWORDS:
        for start in range(0, 200, 20):
            url = (
                "https://candidat.francetravail.fr/offres/recherche?"
                + urllib.parse.urlencode({"motsCles": kw, "lieux": "11R", "offresPartenaires": "true",
                                          "range": f"{start}-{start + 19}", "tri": "0"})
            )
            doc = fetch(url)
            items = re.split(r'<li data-id-offre="', doc)[1:]
            if not items:
                break
            for it in items:
                oid = it.split('"', 1)[0]
                title = re.search(r'<h2[^>]*>.*?<span class="media-heading-title">(.*?)</span>', it, re.S)
                sub = re.search(r'<p[^>]*class="subtext">(.*?)</p>', it, re.S)
                company, loc = "", ""
                if sub:
                    parts = clean(sub.group(1)).split(" - ", 1)
                    company = parts[0].strip()
                    loc = parts[1].strip() if len(parts) > 1 else ""
                date = re.search(r'<p class="date">(.*?)</p>', it, re.S)
                contract = re.search(r'<p class="contrat">([^<]+)', it)
                desc = re.search(r'<p class="description">(.*?)</p>', it, re.S)
                add({
                    "source": "France Travail", "id": oid,
                    "title": clean(title.group(1)) if title else "", "company": company, "location": loc,
                    "contract": clean(contract.group(1)) if contract else "", "date": clean(date.group(1)) if date else "",
                    "salary": "", "desc": clean(desc.group(1)) if desc else "",
                    "url": f"https://candidat.francetravail.fr/offres/recherche/detail/{oid}", "queries": [kw],
                })
            if len(items) < 20:
                break
            time.sleep(1)


# ---------------- AXA ----------------
AXA_KEYWORDS = ["cloud", "devops", "azure", "aws", "infrastructure", "alternance", "apprentissage",
                "apprenticeship", "terraform", "kubernetes", "finops", "sre", "platform"]


def axa():
    for kw in AXA_KEYWORDS:
        url = ("https://recrutement.axa.fr/search-jobs/results?" + urllib.parse.urlencode({
            "ActiveFacetID": 0, "CurrentPage": 1, "RecordsPerPage": 200, "Distance": 50, "RadiusUnitType": 0,
            "Keywords": kw, "Location": "", "ShowRadius": "False", "IsPagination": "False", "FacetTerm": "",
            "FacetType": 0, "SearchResultsModuleName": "Search Results", "SearchFiltersModuleName": "Search Filters",
            "SortCriteria": 0, "SortDirection": 0, "SearchType": 5, "OrganizationIds": 3441}))
        try:
            doc = json.loads(fetch(url)).get("results", "")
        except ValueError:
            continue
        for m in re.finditer(r'<a href="([^"]+)" data-job-id="(\d+)">\s*<h2>(.*?)</h2>(.*?)</a>', doc, re.S):
            loc = re.search(r'job-location">(.*?)</span>', m.group(4), re.S)
            date = re.search(r'job-date-posted">(.*?)</span>', m.group(4), re.S)
            add({
                "source": "AXA", "id": m.group(2), "title": clean(m.group(3)), "company": "AXA",
                "location": clean(loc.group(1)) if loc else "", "contract": "", "date": clean(date.group(1)) if date else "",
                "salary": "", "url": "https://recrutement.axa.fr" + html.unescape(m.group(1)), "queries": [kw],
            })
        time.sleep(1)


for name, fn in [("hellowork", hellowork), ("francetravail", francetravail), ("axa", axa)]:
    before = len(offers)
    try:
        fn()
    except Exception as e:  # noqa: BLE001
        print(f"{name}: erreur {e!r}", file=sys.stderr)
    print(f"{name}: +{len(offers) - before}", file=sys.stderr)

with open(f"{OUT}/offers_raw.json", "w", encoding="utf-8") as f:
    json.dump(list(offers.values()), f, ensure_ascii=False, indent=1)
print(len(offers))
