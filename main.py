"""Copy the pre-rendered front page to /output/entry.png.

Only the Python standard library is used here. The picture itself is
drawn by render.py (Pillow) and shipped in this repository as
news_image.png, next to this file.
"""

import shutil
from pathlib import Path


def main():
    folder = Path(__file__).resolve().parent
    source = folder / "news_image.png"
    target = Path("/output") / "entry.png"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    print("wrote", target, target.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
