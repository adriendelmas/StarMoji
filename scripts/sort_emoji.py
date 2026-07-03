import re
import shutil
import urllib.request
from pathlib import Path
from difflib import get_close_matches

UNICODE_VERSION = "17.0.0"
EMOJI_TEST_URL = f"https://unicode.org/Public/{UNICODE_VERSION}/emoji/emoji-test.txt"
INCOMING_DIR = Path("incoming")
SVG_DIR = Path("sources/svg")

def normalize(name):
    name = name.lower().strip()
    name = re.sub(r"[_\-]+", " ", name)
    name = re.sub(r"[^a-z0-9 ]", "", name)
    return re.sub(r"\s+", " ", name).strip()

def load_lookup():
    text = urllib.request.urlopen(EMOJI_TEST_URL).read().decode("utf-8")
    lookup = {}
    group = subgroup = None
    row_re = re.compile(r"^([0-9A-F ]+)\s*;\s*(\S+)\s*#\s*\S+\s+(.*)$")
    for line in text.splitlines():
        if line.startswith("# group:"):
            group = line.split(":", 1)[1].strip()
        elif line.startswith("# subgroup:"):
            subgroup = line.split(":", 1)[1].strip()
        elif not line.startswith("#") and line.strip():
            m = row_re.match(line)
            if m and m.group(2) == "fully-qualified":
                cps = "-".join(m.group(1).split())
                lookup[normalize(m.group(3))] = (cps, group, subgroup)
    return lookup

def sort_incoming():
    if not INCOMING_DIR.exists():
        print("Pas de dossier incoming/, rien a trier.")
        return
    lookup = load_lookup()
    names = list(lookup.keys())
    for file in INCOMING_DIR.glob("*.svg"):
        key = normalize(file.stem)
        if key not in lookup:
            close = get_close_matches(key, names, n=3, cutoff=0.6)
            print(f"[?] Pas de correspondance pour '{file.name}'. Suggestions : {close}")
            continue
        cps, group, subgroup = lookup[key]
        dest_dir = SVG_DIR / group / subgroup
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / f"{cps}.svg"
        shutil.move(str(file), str(dest))
        print(f"[OK] {file.name} -> {dest}")

if __name__ == "__main__":
    sort_incoming()
