#!/usr/bin/env python3
"""
fetch_metadata.py — pull publication metadata from CrossRef (Zotero-style)

Uses a 3-tier lookup strategy for each paper in _data/publications.yml:
  1. If DOI exists     → CrossRef direct lookup
  2. If PDF URL exists → extract DOI from URL/page, then CrossRef lookup
  3. Fallback          → CrossRef title search with fuzzy matching

Usage:
    python fetch_metadata.py              # fetch metadata for papers missing it
    python fetch_metadata.py --force      # re-fetch even if fields already exist
    python fetch_metadata.py --dry-run    # show what would be fetched, don't write
"""

import argparse
import re
import sys
import time
from pathlib import Path

import requests
import yaml

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

CROSSREF_BASE = "https://api.crossref.org"
# Polite pool: include mailto in User-Agent for 50 req/sec instead of ~1 req/sec
HEADERS = {
    "User-Agent": "SAILHomepage/1.0 (mailto:haiyu.mao@kcl.ac.uk)"
}
COURTESY_DELAY = 0.5  # seconds between requests (well under polite pool limit)

REPO_ROOT = Path(__file__).resolve().parent
PUB_PATH = REPO_ROOT / "_data" / "publications.yml"

# Regex to find a DOI anywhere in text
DOI_RE = re.compile(r'\b(10\.\d{4,9}/[^\s"<>]+)', re.IGNORECASE)


# ---------------------------------------------------------------------------
# Title matching
# ---------------------------------------------------------------------------

def normalize(title: str) -> str:
    """Lowercase, strip punctuation, collapse whitespace."""
    t = title.lower()
    t = re.sub(r"[^a-z0-9\s]", "", t)
    return re.sub(r"\s+", " ", t).strip()


def titles_match(a: str, b: str) -> bool:
    """Check if two titles are similar enough to be the same paper."""
    na, nb = normalize(a), normalize(b)
    if na == nb:
        return True
    shorter, longer = sorted([na, nb], key=len)
    if len(shorter) > 20 and longer.startswith(shorter):
        return True
    wa, wb = set(na.split()), set(nb.split())
    if not wa or not wb:
        return False
    overlap = len(wa & wb) / max(len(wa), len(wb))
    return overlap >= 0.80


# ---------------------------------------------------------------------------
# CrossRef API
# ---------------------------------------------------------------------------

def crossref_by_doi(doi: str) -> dict | None:
    """Look up a DOI directly on CrossRef. Returns parsed metadata or None."""
    doi = re.sub(r'^https?://(dx\.)?doi\.org/', '', doi.strip())
    url = f"{CROSSREF_BASE}/works/{requests.utils.quote(doi, safe='')}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        return _parse_crossref(resp.json().get("message", {}))
    except requests.RequestException as e:
        print(f"    CrossRef DOI error: {e}", file=sys.stderr)
        return None


def crossref_by_title(title: str) -> dict | None:
    """Search CrossRef by title, return best fuzzy match."""
    params = {
        "query.title": title,
        "rows": 5,
        "select": "DOI,title,author,abstract,container-title,published,type,subject",
    }
    try:
        resp = requests.get(f"{CROSSREF_BASE}/works", params=params,
                            headers=HEADERS, timeout=15)
        resp.raise_for_status()
        items = resp.json().get("message", {}).get("items", [])
    except requests.RequestException as e:
        print(f"    CrossRef search error: {e}", file=sys.stderr)
        return None

    for item in items:
        cr_title = (item.get("title") or [""])[0]
        if titles_match(title, cr_title):
            return _parse_crossref(item)
    return None


def _parse_crossref(msg: dict) -> dict:
    """Parse a CrossRef work message into a flat metadata dict."""
    title = (msg.get("title") or [""])[0]

    authors = []
    for a in msg.get("author", []):
        name = f"{a.get('given', '')} {a.get('family', '')}".strip()
        if name:
            authors.append(name)

    abstract = msg.get("abstract", "")
    if abstract:
        # CrossRef abstracts often have JATS XML tags
        abstract = re.sub(r"<[^>]+>", "", abstract)
        # Strip leading "Abstract" label and excessive whitespace
        abstract = re.sub(r"^\s*Abstract\s*", "", abstract, flags=re.IGNORECASE)
        abstract = re.sub(r"\s+", " ", abstract).strip()

    year = None
    published = msg.get("published") or msg.get("issued") or {}
    date_parts = published.get("date-parts", [[]])
    if date_parts and date_parts[0]:
        year = date_parts[0][0]

    venue = (msg.get("container-title") or [""])[0]

    # Pages and volume/number for BibTeX generation
    pages = msg.get("page", "")
    volume = msg.get("volume", "")
    issue = msg.get("issue", "")
    publisher = msg.get("publisher", "")
    cr_type = msg.get("type", "")  # e.g. "proceedings-article", "journal-article"

    # Keywords from CrossRef subject field
    keywords = msg.get("subject", [])

    return {
        "doi": msg.get("DOI"),
        "title": title,
        "authors": authors,
        "abstract": abstract,
        "year": year,
        "venue": venue,
        "pages": pages,
        "volume": volume,
        "issue": issue,
        "publisher": publisher,
        "cr_type": cr_type,
        "keywords": keywords,
    }


def fetch_abstract_s2(doi: str) -> str | None:
    """Fetch abstract from Semantic Scholar as fallback (better coverage for CS papers)."""
    try:
        resp = requests.get(
            f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}",
            params={"fields": "abstract"},
            headers=HEADERS,
            timeout=10,
        )
        if resp.status_code == 429:
            return None  # rate limited, skip
        if resp.status_code != 200:
            return None
        abstract = resp.json().get("abstract", "")
        if abstract:
            return abstract.strip()
    except requests.RequestException:
        pass
    return None


def fetch_keywords_s2(doi: str) -> list[str]:
    """Fetch topic keywords from Semantic Scholar's s2FieldsOfStudy + externalIds for IEEE keywords."""
    try:
        resp = requests.get(
            f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}",
            params={"fields": "s2FieldsOfStudy,fieldsOfStudy,tldr"},
            headers=HEADERS,
            timeout=10,
        )
        if resp.status_code != 200:
            return []
        data = resp.json()

        keywords = []
        seen = set()

        # s2FieldsOfStudy with "external" source = publisher-provided keywords (detailed)
        for f in (data.get("s2FieldsOfStudy") or []):
            cat = f.get("category", "")
            source = f.get("source", "")
            if cat and source == "external" and cat.lower() not in seen:
                seen.add(cat.lower())
                keywords.append(cat)

        # If no external keywords, fall back to model-predicted ones
        if not keywords:
            for f in (data.get("s2FieldsOfStudy") or []):
                cat = f.get("category", "")
                if cat and cat.lower() not in seen:
                    seen.add(cat.lower())
                    keywords.append(cat)

        return keywords
    except requests.RequestException:
        return []


def fetch_bibtex(doi: str) -> str | None:
    """Fetch BibTeX directly from doi.org via content negotiation."""
    doi = re.sub(r'^https?://(dx\.)?doi\.org/', '', doi.strip())
    try:
        resp = requests.get(
            f"https://doi.org/{doi}",
            headers={**HEADERS, "Accept": "application/x-bibtex"},
            timeout=15,
            allow_redirects=True,
        )
        if resp.status_code == 200 and "@" in resp.text[:20]:
            return resp.text.strip()
    except requests.RequestException:
        pass
    return None


# ---------------------------------------------------------------------------
# DOI extraction from URLs
# ---------------------------------------------------------------------------

def extract_doi_from_url(url: str) -> str | None:
    """Try to extract a DOI from a paper/PDF URL."""
    if not url:
        return None

    # arXiv URLs → DOI via convention
    arxiv_match = re.search(r'arxiv\.org/(?:abs|pdf)/(\d+\.\d+)', url, re.I)
    if arxiv_match:
        return f"10.48550/arXiv.{arxiv_match.group(1)}"

    # Check if the URL itself contains a DOI
    doi_in_url = DOI_RE.search(url)
    if doi_in_url:
        return doi_in_url.group(1).rstrip(".")

    # Try fetching the URL and look for DOI in headers/HTML
    try:
        resp = requests.get(url, headers={**HEADERS, "Accept": "text/html"},
                            timeout=10, allow_redirects=True)

        # Check response headers
        for header in ("x-doi", "doi"):
            if header in resp.headers:
                return resp.headers[header]

        # Check final redirect URL for DOI
        doi_in_final = DOI_RE.search(resp.url)
        if doi_in_final:
            return doi_in_final.group(1).rstrip(".")

        # For HTML responses, check meta tags
        if "text/html" in resp.headers.get("content-type", ""):
            text = resp.text[:10000]  # only scan first 10KB

            # <meta name="citation_doi" content="...">
            meta_match = re.search(
                r'<meta\s+name=["\'](?:citation_doi|dc\.identifier)["\']'
                r'\s+content=["\']([^"\']+)["\']',
                text, re.I
            )
            if meta_match:
                val = meta_match.group(1)
                doi_match = DOI_RE.search(val)
                if doi_match:
                    return doi_match.group(1).rstrip(".")

            # Broad DOI regex in page text
            doi_in_html = DOI_RE.search(text)
            if doi_in_html:
                return doi_in_html.group(1).rstrip(".")

    except requests.RequestException:
        pass  # URL might be a direct PDF download, skip

    return None


# ---------------------------------------------------------------------------
# Publication update logic
# ---------------------------------------------------------------------------

def needs_fetch(pub: dict, force: bool) -> bool:
    if force:
        return True
    return not pub.get("doi") or not pub.get("abstract") or not pub.get("bibtex") or not pub.get("keywords")


def update_pub(pub: dict, metadata: dict, bibtex: str | None, keywords: list[str] | None) -> list[str]:
    """Update a publication dict with fetched metadata. Returns list of fields updated."""
    updated = []

    doi = metadata.get("doi")
    if doi and not pub.get("doi"):
        pub["doi"] = doi
        updated.append("doi")

    abstract = metadata.get("abstract")
    if abstract and not pub.get("abstract"):
        pub["abstract"] = abstract
        updated.append("abstract")

    if bibtex and not pub.get("bibtex"):
        pub["bibtex"] = bibtex
        updated.append("bibtex")

    if keywords and not pub.get("keywords"):
        pub["keywords"] = keywords
        updated.append("keywords")

    return updated


# ---------------------------------------------------------------------------
# YAML writing
# ---------------------------------------------------------------------------

class YamlDumper(yaml.SafeDumper):
    pass


def str_representer(dumper, data):
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    if len(data) > 80 or any(c in data for c in ":{}\n[]&*!|>'\"%@`"):
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style='"')
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


YamlDumper.add_representer(str, str_representer)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch publication metadata from CrossRef (Zotero-style)"
    )
    parser.add_argument("--force", action="store_true", help="Re-fetch all papers")
    parser.add_argument("--dry-run", action="store_true", help="Don't write changes")
    args = parser.parse_args()

    if not PUB_PATH.exists():
        print(f"ERROR: {PUB_PATH} not found", file=sys.stderr)
        sys.exit(1)

    with PUB_PATH.open("r", encoding="utf-8") as f:
        pubs = yaml.safe_load(f)

    if not pubs:
        print("No publications found.", file=sys.stderr)
        return

    total = len(pubs)
    fetched = 0
    skipped = 0
    not_found = 0

    for i, pub in enumerate(pubs):
        if not isinstance(pub, dict):
            continue

        title = pub.get("title", "")
        if not title:
            continue

        short = title[:60] + ("..." if len(title) > 60 else "")

        if not needs_fetch(pub, args.force):
            print(f"[{i+1}/{total}] SKIP: {short}", file=sys.stderr)
            skipped += 1
            continue

        print(f"[{i+1}/{total}] {short}", file=sys.stderr)
        metadata = None

        # Tier 1: existing DOI
        existing_doi = pub.get("doi")
        if existing_doi:
            print(f"  T1: DOI lookup ({existing_doi})", file=sys.stderr)
            metadata = crossref_by_doi(existing_doi)
            time.sleep(COURTESY_DELAY)

        # Tier 2: extract DOI from PDF URL
        if not metadata:
            pdf_url = pub.get("pdf", "")
            if pdf_url:
                print(f"  T2: extracting DOI from URL...", file=sys.stderr)
                extracted_doi = extract_doi_from_url(pdf_url)
                if extracted_doi:
                    print(f"  T2: found DOI {extracted_doi}", file=sys.stderr)
                    metadata = crossref_by_doi(extracted_doi)
                    time.sleep(COURTESY_DELAY)
                else:
                    print(f"  T2: no DOI in URL", file=sys.stderr)

        # Tier 3: title search
        if not metadata:
            print(f"  T3: CrossRef title search...", file=sys.stderr)
            metadata = crossref_by_title(title)
            time.sleep(COURTESY_DELAY)

        if not metadata:
            print(f"  -> NOT FOUND", file=sys.stderr)
            not_found += 1
            continue

        # If CrossRef didn't have an abstract, try Semantic Scholar
        resolved_doi = metadata.get("doi") or pub.get("doi")
        if not metadata.get("abstract") and not pub.get("abstract") and resolved_doi:
            print(f"  Fetching abstract from Semantic Scholar...", file=sys.stderr)
            s2_abstract = fetch_abstract_s2(resolved_doi)
            if s2_abstract:
                metadata["abstract"] = s2_abstract
                print(f"  Found abstract via S2", file=sys.stderr)
            else:
                print(f"  No abstract on S2 either", file=sys.stderr)
            time.sleep(COURTESY_DELAY)

        # Fetch keywords: merge CrossRef subjects + Semantic Scholar fields
        keywords = None
        if not pub.get("keywords") and resolved_doi:
            cr_keywords = metadata.get("keywords", [])
            print(f"  Fetching keywords from S2...", file=sys.stderr)
            s2_keywords = fetch_keywords_s2(resolved_doi)
            time.sleep(COURTESY_DELAY)
            # Merge and deduplicate (case-insensitive)
            seen = set()
            merged = []
            for kw in cr_keywords + s2_keywords:
                kw_lower = kw.lower()
                if kw_lower not in seen:
                    seen.add(kw_lower)
                    merged.append(kw)
            if merged:
                keywords = merged
                print(f"  Found {len(merged)} keywords", file=sys.stderr)
            else:
                print(f"  No keywords found", file=sys.stderr)

        # Fetch BibTeX via content negotiation on the DOI
        bibtex = None
        if resolved_doi and not pub.get("bibtex"):
            print(f"  Fetching BibTeX...", file=sys.stderr)
            bibtex = fetch_bibtex(resolved_doi)
            time.sleep(COURTESY_DELAY)

        if args.dry_run:
            doi = metadata.get("doi", "")
            has_abs = "yes" if metadata.get("abstract") else "no"
            has_bib = "yes" if bibtex else "no"
            has_kw = f"{len(keywords)}" if keywords else "no"
            print(f"  -> Would add: doi={doi}, abstract={has_abs}, bibtex={has_bib}, keywords={has_kw}", file=sys.stderr)
        else:
            fields = update_pub(pub, metadata, bibtex, keywords)
            print(f"  -> Updated: {', '.join(fields) if fields else 'no new fields'}", file=sys.stderr)

        fetched += 1

    print(f"\nDone: {fetched} fetched, {skipped} skipped, {not_found} not found.", file=sys.stderr)

    if not args.dry_run and fetched > 0:
        with PUB_PATH.open("r", encoding="utf-8") as f:
            original = f.read()

        # Preserve leading comment block
        lines = original.split("\n")
        comment_lines = []
        for line in lines:
            if line.startswith("#") or line.strip() == "":
                comment_lines.append(line)
            else:
                break
        header = "\n".join(comment_lines)
        if header and not header.endswith("\n"):
            header += "\n"

        body = yaml.dump(pubs, Dumper=YamlDumper, default_flow_style=False,
                         allow_unicode=True, sort_keys=False, width=10000)

        with PUB_PATH.open("w", encoding="utf-8") as f:
            f.write(header)
            f.write(body)

        print(f"Written to {PUB_PATH}", file=sys.stderr)


if __name__ == "__main__":
    main()
