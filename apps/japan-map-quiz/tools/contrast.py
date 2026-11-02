"""src/template.html の色変数（ライト／ダーク）を読み、文字色と背景色の組み合わせのコントラスト比を表にする。

使い方:  python3 tools/contrast.py   （Windows は py -3）
基準: 本文 4.5 以上、28px 以上の見出し 3 以上（WCAG 2.x の相対輝度で計算）
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
css = (ROOT / "src" / "template.html").read_text(encoding="utf-8")


def block(selector_regex):
    m = re.search(selector_regex + r"\s*\{([^}]*)\}", css)
    return dict(re.findall(r"--([\w-]+)\s*:\s*(#[0-9A-Fa-f]{6})", m.group(1)))


light = block(r":root")
dark = {**light, **block(r':root\[data-theme="dark"\]')}


def lum(hex_):
    rgb = [int(hex_[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    rgb = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]


def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


# (文字, 背景, 用途, 必要な比)
PAIRS = [
    ("ink", "paper", "本文・問題文（白の帯・シート）", 4.5),
    ("ink", "cream", "地名・ボタン文字（クリームの陸・カード）", 4.5),
    ("muted", "paper", "補足文字（白）", 4.5),
    ("muted", "cream", "補足文字（クリーム）", 4.5),
    ("on-brand", "brand", "黄色ボタン・札の文字", 4.5),
    ("on-strong", "ok", "正解の丸・ボタンの白文字", 4.5),
    ("on-strong", "ng", "不正解の丸・ボタン・県名タグの白文字", 4.5),
    ("ink", "ok-soft", "正解済みの県の上の地名", 4.5),
    ("ink", "ng-soft", "不正解の県・まちがえた県の札", 4.5),
    ("ink", "land-none", "まだ正解していない県の上の地名", 4.5),
    ("ink", "tier-c", "淡い黄の地方の上の地名", 4.5),
    ("ink", "rich", "色が濃くなった県（レベル2）の上の地名", 4.5),
    ("ink", "rich2", "色が濃くなった県（レベル3）の上の地名", 4.5),
    ("ink", "bg", "ページ背景の上の文字", 4.5),
]

bad = 0
for name, vars_ in (("ライト", light), ("ダーク", dark)):
    print(f"\n### {name}\n\n| 文字 | 背景 | 用途 | 比 | 基準 | 判定 |\n|---|---|---|---|---|---|")
    for fg, bg, use, need in PAIRS:
        r = ratio(vars_[fg], vars_[bg])
        ok = r >= need
        bad += not ok
        print(f"| {fg} {vars_[fg]} | {bg} {vars_[bg]} | {use} | {r:.2f} | {need} | {'OK' if ok else 'NG'} |")
sys.exit(1 if bad else 0)
