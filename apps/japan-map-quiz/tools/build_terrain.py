"""地形コース（山・河川・平野）の図形データ data/terrain.json を作る。

使い方:  python3 tools/build_terrain.py [ne_10m_rivers_lake_centerlines.geojson]
  - 引数に Natural Earth の川データを渡すと、日本の川（石狩川・最上川・利根川）を抜き出して data/ne_rivers_jp.json に保存する
    入手先: https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_rivers_lake_centerlines.geojson
  - 引数なしなら保存済みの data/ne_rivers_jp.json を使う
  - それ以外の川・山地・山脈・平野は、主要な地点の緯度経度を結んだ「おおまかな図形」（教材の略地図程度の正確さ）
  - 平野は楕円を陸地（data/paths.json の県の形）で切り抜く
座標は build_paths.py と同じ投影（x = (経度-128)×cos36°×60、y = (45.8-緯度)×60）
"""
import json
import math
import re
import sys
from pathlib import Path
from shapely.geometry import Polygon, LineString, MultiPolygon
from shapely.ops import unary_union

DATA = Path(__file__).resolve().parent.parent / "data"
K = math.cos(math.radians(36))


def proj(lat, lon):
    return ((lon - 128) * K * 60, (45.8 - lat) * 60)


# 山地・山脈（主な尾根を北から南へ。緯度, 経度）と山。pref はコレクションで色をつける代表の都道府県
MOUNTS = [
    ("hidaka", "日高山脈", "ひだかさんみゃく", 1, [(43.15, 142.75), (42.75, 142.85), (42.35, 143.05), (42.0, 143.2)]),
    ("ou", "奥羽山脈", "おううさんみゃく", 3, [(40.65, 140.88), (40.0, 140.85), (39.5, 140.78), (39.0, 140.72), (38.5, 140.55), (38.0, 140.35), (37.5, 140.15), (37.1, 140.0)]),
    ("echigo", "越後山脈", "えちごさんみゃく", 15, [(37.55, 139.65), (37.25, 139.35), (36.95, 139.1), (36.8, 138.9)]),
    ("hida", "飛驒山脈", "ひださんみゃく", 20, [(36.85, 137.65), (36.55, 137.65), (36.25, 137.6), (35.95, 137.5)]),
    ("kiso", "木曽山脈", "きそさんみゃく", 20, [(35.95, 137.83), (35.75, 137.83), (35.5, 137.73)]),
    ("akaishi", "赤石山脈", "あかいしさんみゃく", 19, [(35.85, 138.22), (35.6, 138.2), (35.35, 138.12), (35.1, 138.0)]),
    ("kii", "紀伊山地", "きいさんち", 29, [(34.35, 135.95), (34.1, 135.88), (33.85, 135.7)]),
    ("chugoku", "中国山地", "ちゅうごくさんち", 34, [(35.3, 134.4), (35.2, 133.65), (35.0, 132.95), (34.65, 132.2), (34.35, 131.75)]),
    ("shikoku", "四国山地", "しこくさんち", 39, [(33.95, 134.2), (33.82, 133.7), (33.72, 133.2), (33.5, 132.8)]),
    ("kyushu", "九州山地", "きゅうしゅうさんち", 45, [(33.0, 131.25), (32.6, 131.1), (32.2, 130.95)]),
]
PEAKS = [("fuji", "富士山", "ふじさん", 22, (35.36, 138.73))]

# 川（みなもと → 河口）。ne があるものは Natural Earth の線を使う
RIVERS = [
    ("ishikari", "石狩川", "いしかりがわ", 1, "Ishikari", None),
    ("kitakami", "北上川", "きたかみがわ", 3, None, [(40.05, 141.2), (39.7, 141.15), (39.38, 141.12), (38.93, 141.13), (38.6, 141.2), (38.42, 141.3)]),
    ("mogami", "最上川", "もがみがわ", 6, "Mogami", None),
    ("abukuma", "阿武隈川", "あぶくまがわ", 7, None, [(37.13, 140.1), (37.15, 140.25), (37.4, 140.38), (37.76, 140.47), (37.95, 140.7), (38.1, 140.92)]),
    ("shinano", "信濃川", "しなのがわ", 15, None, [(35.9, 138.7), (36.25, 138.45), (36.4, 138.25), (36.65, 138.2), (36.85, 138.37), (37.13, 138.75), (37.45, 138.85), (37.93, 139.05)]),
    ("tone", "利根川", "とねがわ", 10, "Tone", None),
    ("tenryu", "天竜川", "てんりゅうがわ", 22, None, [(36.05, 138.08), (35.83, 137.95), (35.5, 137.82), (35.1, 137.85), (34.65, 137.79)]),
    ("kisogawa", "木曽川", "きそがわ", 21, None, [(35.95, 137.75), (35.84, 137.69), (35.6, 137.6), (35.5, 137.48), (35.38, 136.94), (35.03, 136.7)]),
    ("yoshino", "吉野川", "よしのがわ", 36, None, [(33.75, 133.2), (33.77, 133.55), (33.85, 133.75), (34.03, 133.8), (34.07, 134.2), (34.08, 134.6)]),
    ("chikugo", "筑後川", "ちくごがわ", 41, None, [(33.1, 131.1), (33.32, 130.94), (33.35, 130.7), (33.32, 130.5), (33.15, 130.35)]),
]

# 平野（中心の緯度・経度、東西の半径・南北の半径（度）、回転（度、時計回り））
PLAINS = [
    ("p_ishikari", "石狩平野", "いしかりへいや", 1, (43.15, 141.6), 0.35, 0.3, 0),
    ("p_tokachi", "十勝平野", "とかちへいや", 1, (42.85, 143.2), 0.4, 0.3, 0),
    ("p_shonai", "庄内平野", "しょうないへいや", 6, (38.85, 139.88), 0.12, 0.28, 0),
    ("p_sendai", "仙台平野", "せんだいへいや", 4, (38.25, 140.95), 0.15, 0.35, 0),
    ("p_echigo", "越後平野", "えちごへいや", 15, (37.75, 139.05), 0.22, 0.4, -40),
    ("p_kanto", "関東平野", "かんとうへいや", 11, (36.0, 139.75), 0.6, 0.45, 0),
    ("p_nobi", "濃尾平野", "のうびへいや", 23, (35.25, 136.75), 0.25, 0.22, 0),
    ("p_osaka", "大阪平野", "おおさかへいや", 27, (34.65, 135.55), 0.15, 0.2, 0),
    ("p_sanuki", "讃岐平野", "さぬきへいや", 37, (34.25, 133.9), 0.32, 0.08, 0),
    ("p_tsukushi", "筑紫平野", "つくしへいや", 41, (33.25, 130.4), 0.25, 0.14, 0),
]


def path_d(pts):
    return "M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def bbox(pts):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    return [round(min(xs), 1), round(min(ys), 1), round(max(xs), 1), round(max(ys), 1)]


def ne_rivers(src):
    d = json.load(open(src, encoding="utf-8"))
    want = {r[4] for r in RIVERS if r[4]}
    out = {}
    for f in d["features"]:
        name = f["properties"].get("name")
        if name in want and f["geometry"]:
            g = f["geometry"]
            lines = g["coordinates"] if g["type"] == "MultiLineString" else [g["coordinates"]]
            if all(128 < p[0] < 146 and 30 < p[1] < 46 for l in lines for p in l):
                out.setdefault(name, []).extend([[round(p[0], 3), round(p[1], 3)] for p in l] for l in lines)
    (DATA / "ne_rivers_jp.json").write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8")
    print("saved ne_rivers_jp.json:", {k: len(v) for k, v in out.items()})


def land():
    polys = []
    for o in json.load(open(DATA / "paths.json", encoding="utf-8")):
        for part in re.findall(r"M([^Z]+)Z", o["d"]):
            pts = [tuple(map(float, s.split(","))) for s in part.split("L")]
            if len(pts) >= 3:
                polys.append(Polygon(pts).buffer(0))
    return unary_union(polys).buffer(0.8).buffer(-0.8)


def main():
    if len(sys.argv) > 1:
        ne_rivers(sys.argv[1])
    ne = json.loads((DATA / "ne_rivers_jp.json").read_text(encoding="utf-8"))
    feats = []
    for fid, name, kana, pref, line in MOUNTS:
        pts = [proj(*p) for p in line]
        feats.append({"id": fid, "cat": "mount", "kind": "range", "name": name, "kana": kana, "pref": pref, "d": path_d(pts), "b": bbox(pts)})
    for fid, name, kana, pref, (lat, lon) in PEAKS:
        x, y = proj(lat, lon); s = 9
        pts = [(x, y - s), (x + s, y + s * 0.7), (x - s, y + s * 0.7)]
        feats.append({"id": fid, "cat": "mount", "kind": "peak", "name": name, "kana": kana, "pref": pref, "d": path_d(pts) + "Z", "b": bbox(pts)})
    for fid, name, kana, pref, ne_name, line in RIVERS:
        if ne_name:
            parts = [[proj(lat, lon) for lon, lat in l] for l in ne[ne_name]]
            parts = [list(LineString(p).simplify(0.6).coords) for p in parts if len(p) > 1]
        else:
            parts = [[proj(*p) for p in line]]
        allpts = [p for l in parts for p in l]
        feats.append({"id": fid, "cat": "river", "kind": "river", "name": name, "kana": kana, "pref": pref, "d": "".join(path_d(l) for l in parts), "b": bbox(allpts)})
    L = land()
    for fid, name, kana, pref, (lat, lon), rx, ry, rot in PLAINS:
        a = math.radians(rot)
        ring = []
        for i in range(32):
            t = 2 * math.pi * i / 32
            dx, dy = rx * math.cos(t), ry * math.sin(t)
            ring.append(proj(lat + (dx * math.sin(a) + dy * math.cos(a)), lon + (dx * math.cos(a) - dy * math.sin(a))))
        g = Polygon(ring).intersection(L)
        polys = list(g.geoms) if isinstance(g, MultiPolygon) else [g]
        polys = [p.simplify(0.4) for p in polys if p.area > 4]
        dd = "".join(path_d(list(p.exterior.coords)[:-1]) + "Z" for p in polys)
        feats.append({"id": fid, "cat": "plain", "kind": "plain", "name": name, "kana": kana, "pref": pref, "d": dd,
                      "b": bbox([c for p in polys for c in p.exterior.coords])})
    (DATA / "terrain.json").write_text(json.dumps(feats, ensure_ascii=False, separators=(",", ":")), encoding="utf-8", newline="\n")
    print("wrote terrain.json:", len(feats), "features")


if __name__ == "__main__":
    main()
