"""iOS アプリに入れる Web の中身（mobile/www/）を作る。
1. 公開サイトと同じものを tools/build_site.py で _site/ に組み立てる（タイトル画面＋日本地図タップドリル）
2. それを www/ にうつし、フォントをアプリの中のもの（mobile/fonts/）に差しかえる（電波がなくても同じ文字で出す）
3. 「はじめる」のリンクを japan-map-quiz/index.html にする（アプリの中ではフォルダ名だけだと開けないことがあるため）
使い方:  python3 mobile/build_www.py   （そのあと npx cap sync ios）
"""
import re, shutil, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
WWW = HERE / "www"
subprocess.run([sys.executable, str(ROOT / "tools/build_site.py")], check=True)
shutil.rmtree(WWW, ignore_errors=True)
shutil.copytree(ROOT / "_site", WWW)
shutil.copytree(HERE / "fonts", WWW / "fonts")
FONT_LINKS = re.compile(r'\s*<link rel="preconnect" href="https://fonts\.(googleapis|gstatic)\.com"[^>]*>|\s*<link rel="stylesheet" href="https://fonts\.googleapis\.com/[^"]*">')
for page, up in ((WWW / "index.html", ""), (WWW / "japan-map-quiz" / "index.html", "../")):
    h = page.read_text(encoding="utf-8")
    h, n = FONT_LINKS.subn("", h)
    assert n >= 1, f"{page}: Google Fonts のリンクが見つからない"
    h = h.replace("</title>", f'</title>\n<link rel="stylesheet" href="{up}fonts/fonts.css">', 1)
    h = h.replace('href="japan-map-quiz/"', 'href="japan-map-quiz/index.html"')
    page.write_bytes(h.encode("utf-8"))  # Python 3.9 でも動くように
print(f"wrote {WWW}")
