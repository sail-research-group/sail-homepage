import re
from pathlib import Path
from typing import Dict


def load_namelist(path: Path) -> Dict[str, str]:
	mapping: Dict[str, str] = {}
	with path.open("r", encoding="utf-8") as f:
		for line in f:
			line = line.strip()
			if not line or line.startswith("#"):
				continue
			# Expect format: <name>, <url>
			parts = [p.strip() for p in line.split(",", 1)]
			if len(parts) != 2:
				continue
			name, url = parts
			if name and url:
				mapping[name] = url
	# print(f"Loaded {len(mapping)} names from {path}")
	# print(mapping)
	return mapping


def strip_html_tags(text: str) -> str:
	# Remove anything between < and >, non-greedy to handle nested tags conservatively
	return re.sub(r"<[^>]*?>", "", text, flags=re.DOTALL)


def hyperlink_names(text: str, name_url: Dict[str, str]) -> str:
	# Replace longer names first to avoid partial overlaps
	for name in sorted(name_url.keys(), key=len, reverse=True):
		url = name_url[name]
		# Use word boundaries around the full name; escape the name for regex safety
		pattern = re.compile(rf"\b({re.escape(name)})\b", flags=re.UNICODE)

		def repl(m: re.Match) -> str:
			matched = m.group(1)
			# Use single quotes in href to keep YAML double-quoted strings valid
			return f"<a href='{url}'><u>{matched}</u></a>"

		text = pattern.sub(repl, text)
	return text


def process_publications(repo_root: Path) -> None:
	namelist_path = repo_root / "namelist.txt"
	publications_path = repo_root / "_data" / "publications.yml"

	if not namelist_path.exists():
		raise FileNotFoundError(f"namelist not found: {namelist_path}")
	if not publications_path.exists():
		raise FileNotFoundError(f"publications.yml not found: {publications_path}")

	name_map = load_namelist(namelist_path)

	original_text = publications_path.read_text(encoding="utf-8")

	# Backup original
	# backup_path = publications_path.with_suffix(".yml.bak")
	# backup_path.write_text(original_text, encoding="utf-8")

	cleaned = strip_html_tags(original_text)
	updated = hyperlink_names(cleaned, name_map)

	publications_path.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
	process_publications(Path(__file__).resolve().parent)

