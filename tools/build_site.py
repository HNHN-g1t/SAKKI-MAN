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
OUT.mkdir(exist_ok=True)   # Windows では rmtree 直後に作り直せないことがあるため
# 入口ページとファビコン（元画像 favicon-source.webp は公開しない）
for f in (ROOT / "site").iterdir():
    if f.is_file() and f.name != "favicon-source.webp":
        shutil.copy(f, OUT / f.name)
for name, src in APPS.items():
    (OUT / name).mkdir(exist_ok=True)
    shutil.copy(ROOT / src / "index.html", OUT / name / "index.html")
    # アプリが読みこむ素材フォルダ（BGM の mp3 など）もいっしょに公開する
    for sub in ("bgm",):
        if (ROOT / src / sub).is_dir():
            shutil.copytree(ROOT / src / sub, OUT / name / sub, dirs_exist_ok=True)
print(f"wrote {OUT}")
