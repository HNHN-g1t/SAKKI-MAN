"""src/template.html の CLIMATE_CITIES（雨温図のデータ）を、月の値と年の値で照合する。

使い方:  python3 tools/check_climate.py   （Windows は py -3）
- 月の降水量の合計と年降水量の差が 1mm 以内（気象庁の値は平年値どうしの丸めで少しずれる）
- 月の平均気温の平均と年平均気温の差が 0.2℃ 以内
- 12か月そろっていること
値そのものは 気象庁「過去の気象データ検索 平年値（1991〜2020年）」と見比べて入れる（station は地点番号）
"""
import re
import sys
from pathlib import Path

src = (Path(__file__).resolve().parent.parent / "src" / "template.html").read_text(encoding="utf-8")
block = src[src.index("const CLIMATE_CITIES = ["):src.index("const zoneOf")]
bad = 0
for m in re.finditer(r'name:"([^"]+)".*?rain:\[([^\]]+)\], temp:\[([^\]]+)\], year:\[([^\]]+)\]', block, re.S):
    name = m.group(1)
    rain = [float(x) for x in m.group(2).split(",")]
    temp = [float(x) for x in m.group(3).split(",")]
    yr, yt = [float(x) for x in m.group(4).split(",")]
    ok = len(rain) == 12 and len(temp) == 12 and abs(sum(rain) - yr) <= 1 and abs(sum(temp) / 12 - yt) <= 0.2
    bad += not ok
    print(f"{name}: 降水量 月合計 {sum(rain):.1f} / 年 {yr}　気温 月平均 {sum(temp) / 12:.2f} / 年 {yt}　{'OK' if ok else 'NG'}")
sys.exit(1 if bad else 0)
