"""Build faded Noto emoji thumbnails for the progress table.

Downloads Google's Noto emoji PNGs (Apache 2.0, github.com/googlefonts/noto-emoji),
resizes them to 56px and reduces their opacity to 25%, then stores them in n/
with short codepoint filenames (e.g. n/1f600.png). The progress table uses these
as "missing emoji" thumbnails. Run locally (needs pillow); re-run after bumping
UNICODE_VERSION to cover newly added emoji. Existing files are skipped.
"""

import io
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PIL import Image

UNICODE_VERSION = "17.0.0"
EMOJI_TEST_URL = f"https://unicode.org/Public/{UNICODE_VERSION}/emoji/emoji-test.txt"
NOTO_PNG_URL = "https://raw.githubusercontent.com/googlefonts/noto-emoji/main/png/72/emoji_u{}.png"
OUT_DIR = Path("n")
SIZE = 36
OPACITY = 0.25

def all_codepoints():
    text = urllib.request.urlopen(EMOJI_TEST_URL).read().decode("utf-8")
    row_re = re.compile(r"^([0-9A-F ]+)\s*;\s*fully-qualified\s*#")
    cps = []
    for line in text.splitlines():
        m = row_re.match(line)
        if m:
            cps.append("-".join(m.group(1).split()))
    return cps

def short_name(cps):
    parts = [f"{int(p, 16):04x}" for p in cps.split("-") if p.upper() != "FE0F"]
    return "_".join(parts)

def build_one(cps):
    short = short_name(cps)
    dest = OUT_DIR / f"{short}.png"
    if dest.exists():
        return "skip"
    url = NOTO_PNG_URL.format(short)
    try:
        data = urllib.request.urlopen(url, timeout=30).read()
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return "absent"
        raise
    img = Image.open(io.BytesIO(data)).convert("RGBA")
    img = img.resize((SIZE, SIZE), Image.LANCZOS)
    alpha = img.getchannel("A").point(lambda a: int(a * OPACITY))
    img.putalpha(alpha)
    img.save(dest, optimize=True)
    return "ok"

def main():
    OUT_DIR.mkdir(exist_ok=True)
    cps = all_codepoints()
    results = {"ok": 0, "skip": 0, "absent": 0, "error": 0}
    def safe(c):
        try:
            return build_one(c)
        except Exception as e:
            print(f"[!] {c}: {e}")
            return "error"
    with ThreadPoolExecutor(max_workers=24) as ex:
        for r in ex.map(safe, cps):
            results[r] += 1
    print(results)

if __name__ == "__main__":
    main()
