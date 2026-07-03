"""Build faded flag thumbnails from Noto's waved region flags.

Flag emoji are not part of Noto's png/ directory; they live as waved SVGs in
third_party/region-flags. This script downloads them, rasterizes them with
resvg (pip install resvg-py pillow), centers them on a square transparent
canvas, fades them to 25% opacity and stores them in n/ alongside the
thumbnails produced by build_faded_noto.py. Existing files are skipped.
"""

import io
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import resvg_py
from PIL import Image

FLAGS_URL = ("https://raw.githubusercontent.com/googlefonts/noto-emoji/main/"
             "third_party/region-flags/waved-svg/{}")
LIST_URL = "https://api.github.com/repos/googlefonts/noto-emoji/git/trees/main?recursive=1"
OUT_DIR = Path("n")
SIZE = 36
OPACITY = 0.25

def list_flag_files():
    import json
    data = json.loads(urllib.request.urlopen(LIST_URL, timeout=120).read())
    return [p["path"].rsplit("/", 1)[1] for p in data["tree"]
            if p["path"].startswith("third_party/region-flags/waved-svg/")
            and p["path"].endswith(".svg")]

def build_one(fname):
    short = fname.removeprefix("emoji_u").removesuffix(".svg")
    dest = OUT_DIR / f"{short}.png"
    if dest.exists():
        return "skip"
    svg = urllib.request.urlopen(FLAGS_URL.format(fname), timeout=30).read().decode("utf-8")
    # certains fichiers sont des symlinks git : le contenu est le nom du fichier cible
    hops = 0
    while not svg.lstrip().startswith("<") and hops < 3:
        target = svg.strip().rsplit("/", 1)[-1]
        svg = urllib.request.urlopen(FLAGS_URL.format(target), timeout=30).read().decode("utf-8")
        hops += 1
    png = bytes(resvg_py.svg_to_bytes(svg_string=svg, width=SIZE))
    img = Image.open(io.BytesIO(png)).convert("RGBA")
    canvas = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    canvas.paste(img, ((SIZE - img.width) // 2, (SIZE - img.height) // 2))
    alpha = canvas.getchannel("A").point(lambda a: int(a * OPACITY))
    canvas.putalpha(alpha)
    canvas.save(dest, optimize=True)
    return "ok"

def main():
    OUT_DIR.mkdir(exist_ok=True)
    files = list_flag_files()
    print(f"{len(files)} drapeaux a traiter")
    results = {"ok": 0, "skip": 0, "error": 0}
    def safe(f):
        try:
            return build_one(f)
        except Exception as e:
            print(f"[!] {f}: {e}")
            return "error"
    with ThreadPoolExecutor(max_workers=16) as ex:
        for r in ex.map(safe, files):
            results[r] += 1
    print(results)

if __name__ == "__main__":
    main()
