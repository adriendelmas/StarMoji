import re
import urllib.request
from pathlib import Path
from collections import defaultdict
from urllib.parse import quote

UNICODE_VERSION = "17.0.0"
EMOJI_TEST_URL = f"https://unicode.org/Public/{UNICODE_VERSION}/emoji/emoji-test.txt"
SVG_DIR = Path("sources/svg")
README_PATH = Path("README.md")
START, END = "<!-- PROGRESS:START -->", "<!-- PROGRESS:END -->"
PER_ROW = 12

def fetch():
    return urllib.request.urlopen(EMOJI_TEST_URL).read().decode("utf-8")

def parse(text):
    groups = defaultdict(lambda: defaultdict(list))
    group = subgroup = None
    row_re = re.compile(r"^([0-9A-F ]+)\s*;\s*(\S+)\s*#\s*\S+\s+E\d+\.\d+\s+(.*)$")
    for line in text.splitlines():
        if line.startswith("# group:"):
            group = line.split(":", 1)[1].strip()
        elif line.startswith("# subgroup:"):
            subgroup = line.split(":", 1)[1].strip()
        elif not line.startswith("#") and line.strip():
            m = row_re.match(line)
            if m and m.group(2) == "fully-qualified":
                cps = "-".join(m.group(1).split())
                groups[group][subgroup].append((cps, m.group(3).strip()))
    return groups

def done_map():
    return {p.stem.upper(): p for p in SVG_DIR.rglob("*.svg")}

def cell(cps, name, done):
    if cps in done:
        return f'<img src="{quote(done[cps].as_posix())}" width="28" align="top" title="{name}">'
    short = "_".join(f"{int(p, 16):04x}" for p in cps.split("-") if p.upper() != "FE0F")
    if (Path("n") / f"{short}.png").exists():
        return f'<img src="n/{short}.png" width="28" align="top" title="{name}">'
    return f'<img src="assets/placeholder.svg" width="28" align="top" title="{name}">'

def render(groups, done):
    total = sum(len(v) for sg in groups.values() for v in sg.values())
    made = sum(1 for sg in groups.values() for v in sg.values() for cps, _ in v if cps in done)
    out = [f"**Overall: {made}/{total} emoji ({round(100*made/total)}%)**\n"]
    for group, subgroups in groups.items():
        g_all = [item for sg in subgroups.values() for item in sg]
        g_made = sum(1 for cps, _ in g_all if cps in done)
        out.append(f"<details><summary><b>{group}</b> — {g_made}/{len(g_all)} ({round(100*g_made/len(g_all))}%)</summary>\n")
        out.append("<table><tr>")
        for i, (cps, name) in enumerate(g_all):
            if i and i % PER_ROW == 0:
                out.append("</tr><tr>")
            out.append(f'<td>{cell(cps, name, done)}</td>')
        out.append("</tr></table>\n</details>\n")
    return "\n".join(out)

def write_readme(block):
    text = README_PATH.read_text(encoding="utf-8")
    wrapped = f"{START}\n{block}\n{END}"
    pattern = re.compile(f"{re.escape(START)}.*?{re.escape(END)}", re.DOTALL)
    text = pattern.sub(wrapped, text) if pattern.search(text) else text + f"\n\n{wrapped}\n"
    README_PATH.write_text(text, encoding="utf-8")

if __name__ == "__main__":
    write_readme(render(parse(fetch()), done_map()))
