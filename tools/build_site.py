"""公開用フォルダ _site/ を組み立てる（GitHub Pages と Vercel の共通ビルド）。

使い方:  python3 tools/build_site.py   （Windows は py -3）
アプリを増やしたら APPS に1行足す。
"""
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_site"

# 公開パス: ビルド済み index.html のある apps/ 配下のフォルダ
APPS = {
    "japan-map-quiz": "apps/japan-map-quiz",
}

subprocess.run([sys.executable, str(ROOT / "apps/japan-map-quiz/tools/build.py")], check=True)

shutil.rmtree(OUT, ignore_errors=True)
OUT.mkdir()
shutil.copy(ROOT / "site/index.html", OUT / "index.html")
for name, src in APPS.items():
    (OUT / name).mkdir()
    shutil.copy(ROOT / src / "index.html", OUT / name / "index.html")
print(f"wrote {OUT}")
