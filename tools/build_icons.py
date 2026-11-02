"""site/favicon-source.webp（ユーザー作の「記」マーク）から、ファビコン一式を site/ に書き出す。

使い方:  python3 tools/build_icons.py   （Windows は py -3。Pillow が必要）
"""
from pathlib import Path
from PIL import Image

SITE = Path(__file__).resolve().parent.parent / "site"
src = Image.open(SITE / "favicon-source.webp").convert("RGB")
src.resize((32, 32), Image.LANCZOS).save(SITE / "favicon-32.png", optimize=True)
src.resize((180, 180), Image.LANCZOS).save(SITE / "apple-touch-icon.png", optimize=True)
src.resize((192, 192), Image.LANCZOS).save(SITE / "icon-192.png", optimize=True)
src.save(SITE / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
print("wrote favicon-32.png, apple-touch-icon.png, icon-192.png, favicon.ico")
