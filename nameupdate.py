#!/usr/bin/env python3
"""
nameupdate.py — inject name hyperlinks into _data/publications.yml

Reads the author→URL mapping from the people data files (leader.yml,
phds.yml, masters.yml, interns.yml, visitings.yml) so there is no need
to maintain a separate namelist.

Usage:
    python nameupdate.py                       # check consistency (warn) + inject links
    python nameupdate.py --check-only          # report issues, do NOT modify files
    python nameupdate.py --check-only --strict # exit 1 on any issue, do NOT modify files
    python nameupdate.py --strict              # inject links + exit 1 on any issue
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import yaml  # PyYAML — only non-stdlib dependency


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

PEOPLE_FILES = ["leader.yml", "phds.yml", "interns.yml", "masters.yml", "visitings.yml"]


# ---------------------------------------------------------------------------
# Core helpers
# ---------------------------------------------------------------------------

def load_people(repo_root: Path) -> Dict[str, str]:
    """
    Build a {name: url} mapping from all people data files.

    URL resolution order per person:
      1. 'web' field (used by leader.yml for external sites)
      2. 'url' field (used by phds.yml etc. for internal links)
      3. fallback: /people/#<slugified-name>
    """
    data_dir = repo_root / "_data"
    mapping: Dict[str, str] = {}

    for filename in PEOPLE_FILES:
        fpath = data_dir / filename
        if not fpath.exists():
            continue
        with fpath.open("r", encoding="utf-8") as f:
            parsed = yaml.safe_load(f)
        if not parsed:
            continue
        for entry in parsed:
            if not isinstance(entry, dict):
                continue
            name = entry.get("name")
            if not name:
                continue
            url = entry.get("web") or entry.get("url")
            if not url:
                # Fallback: anchor on the people page
                slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
                url = f"/people/#{slug}"
            mapping[name] = url

    return mapping


def strip_html_tags(text: str) -> str:
    """Remove anything between < and >, non-greedy to handle nested tags conservatively."""
    return re.sub(r"<[^>]*?>", "", text, flags=re.DOTALL)


def hyperlink_names(text: str, name_url: Dict[str, str]) -> str:
    """Replace longer names first to avoid partial overlaps."""
    for name in sorted(name_url.keys(), key=len, reverse=True):
        url = name_url[name]
        # Use word boundaries around the full name; escape the name for regex safety
        pattern = re.compile(rf"\b({re.escape(name)})\b", flags=re.UNICODE)

        def repl(m: re.Match, _url: str = url) -> str:
            matched = m.group(1)
            # Use single quotes in href to keep YAML double-quoted strings valid
            return f"<a href='{_url}'><u>{matched}</u></a>"

        text = pattern.sub(repl, text)
    return text


def process_publications(repo_root: Path, name_map: Dict[str, str]) -> None:
    """Strip existing HTML from publications.yml then re-inject name hyperlinks."""
    publications_path = repo_root / "_data" / "publications.yml"

    if not publications_path.exists():
        raise FileNotFoundError(f"publications.yml not found: {publications_path}")

    original_text = publications_path.read_text(encoding="utf-8")
    cleaned = strip_html_tags(original_text)
    updated = hyperlink_names(cleaned, name_map)
    publications_path.write_text(updated, encoding="utf-8")


# ---------------------------------------------------------------------------
# Consistency checking
# ---------------------------------------------------------------------------

def load_raw_author_strings(repo_root: Path) -> List[str]:
    """
    Parse publications.yml with PyYAML, extract each 'authors' field,
    and strip any embedded HTML. Returns one clean string per publication.
    """
    pub_path = repo_root / "_data" / "publications.yml"
    with pub_path.open("r", encoding="utf-8") as f:
        pubs = yaml.safe_load(f)
    if not pubs:
        return []
    result = []
    for pub in pubs:
        if isinstance(pub, dict) and "authors" in pub:
            raw = strip_html_tags(str(pub["authors"]))
            result.append(raw)
    return result


def check_consistency(
    repo_root: Path,
    name_map: Dict[str, str],
) -> Tuple[bool, List[str]]:
    """
    Check that every lab member who appears in publications has a URL mapping.

    Since the name map is now auto-generated from people files, the only
    useful check is whether any lab member appears in publication author
    strings — if they do, they'll be hyperlinked automatically.
    Members who don't appear in any publication get a notice (not an error).
    """
    author_strings = load_raw_author_strings(repo_root)
    all_authors = "\n".join(author_strings)

    messages: List[str] = []
    had_issues = False

    # Check: lab members that never appear in any publication
    for name in sorted(name_map.keys()):
        if not re.search(rf"\b{re.escape(name)}\b", all_authors):
            messages.append(
                f"NOTICE: '{name}' is in people files "
                f"but does not appear in any publication author list"
            )
            # This is informational, not an error

    return had_issues, messages


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Inject name hyperlinks into _data/publications.yml"
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Run consistency checks only; do NOT modify publications.yml",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with code 1 if any consistency issue is found",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent
    name_map = load_people(repo_root)

    if not name_map:
        print("WARNING: no people found in data files.", file=sys.stderr)

    had_issues, messages = check_consistency(repo_root, name_map)

    for msg in messages:
        print(msg, file=sys.stderr)

    if not messages:
        print(f"OK: {len(name_map)} people loaded from data files.", file=sys.stderr)

    if args.check_only:
        sys.exit(1 if (had_issues and args.strict) else 0)

    # Default mode: inject hyperlinks into publications.yml
    process_publications(repo_root, name_map)
    print("OK: publications.yml updated with name hyperlinks.", file=sys.stderr)

    if had_issues and args.strict:
        sys.exit(1)


if __name__ == "__main__":
    main()
