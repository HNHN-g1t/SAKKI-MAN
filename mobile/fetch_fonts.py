"""アプリに入れるフォントを Google Fonts から取ってきて mobile/fonts/ に置く（一度だけ。取ったものはリポジトリに入れる）。
BIZ UDPGothic（400・700）と Dela Gothic One。どちらも SIL Open Font License 1.1。
使い方:  python3 mobile/fetch_fonts.py
"""
import re, urllib.request
from pathlib import Path
HERE = Path(__file__).resolve().parent
OUT = HERE / "fonts"; OUT.mkdir(exist_ok=True)
URL = "https://fonts.googleapis.com/css2?family=BIZ+UDPGothic:wght@400;700&family=Dela+Gothic+One&display=swap"
UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
css = urllib.request.urlopen(urllib.request.Request(URL, headers={"User-Agent": UA})).read().decode()
n = 0
def grab(m):
    global n
    url = m.group(1); n += 1
    name = f"f{n:03d}.woff2"
    (OUT / name).write_bytes(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA})).read())
    return f"url({name})"
css = re.sub(r"url\((https://fonts\.gstatic\.com/[^)]+)\)", grab, css)
css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
(OUT / "fonts.css").write_text(css, encoding="utf-8")
print(f"{n} files", sum(f.stat().st_size for f in OUT.glob('*.woff2')) // 1024, "KB")
