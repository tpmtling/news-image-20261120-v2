"""Entry point: copy the pre-rendered news image to /output/entry.png.

Uses only the Python standard library. The image itself is produced by
render.py (Pillow) and committed as news_image.png next to this file.
"""
import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "news_image.png")
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst)


if __name__ == "__main__":
    main()
