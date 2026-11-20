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


# 地形の用語（小学校の教科書に出る地形）と、海岸・湾・半島。教材の略地図程度のおおまかな形
#   area：楕円を陸地で切り抜く（台地・盆地など）／poly：多角形（緯度経度の点）を陸地で切り抜く／sea：楕円から陸地をのぞく（湾・海）／line：海岸線ぞいの線
#   (id, cat, 名前, よみ, 代表の都道府県, 形, 中心または線の点, 東西の半径, 南北の半径, 回転, 解説)
LANDFORMS = [
    ("l_shirasu", "land", "シラス台地", "しらすだいち", 46, "area", (31.62, 130.78), 0.32, 0.36, 0,
     "火山の灰や軽石が厚く積もってできた台地。鹿児島県から宮崎県南部に広がる。水はけがよすぎて米づくりに向かず、さつまいもや茶、畜産がさかん。"),
    ("l_rias", "land", "リアス海岸", "りあすかいがん", 3, "line", [(40.2, 141.88), (39.95, 141.97), (39.6, 141.98), (39.27, 141.9), (38.95, 141.68), (38.7, 141.52)], 0, 0, 0,
     "山地が海にしずんでできた、出入りの多いぎざぎざの海岸。三陸海岸の南部や若狭湾、志摩半島、宇和海など。湾の中は波がおだやかで養殖がさかん。"),
    ("l_fan", "land", "扇状地", "せんじょうち", 19, "area", (35.7, 138.62), 0.13, 0.1, 0,
     "川が山から平地に出る所に、すなやじゃりを積もらせてできた扇の形の土地。甲府盆地に多い。水はけがよく、ぶどうやももの果樹園に使われる。"),
    ("l_delta", "land", "三角州", "さんかくす", 34, "area", (34.39, 132.45), 0.08, 0.07, 0,
     "川が海に流れこむ所に、運ばれた土やすなが積もってできた低い土地。広島市は太田川の三角州の上に広がる。"),
    ("l_dune", "land", "砂丘", "さきゅう", 31, "area", (35.53, 134.22), 0.14, 0.05, 0,
     "風に運ばれたすなが積もってできた丘。鳥取砂丘が有名。かんがい設備を整え、らっきょうやながいもをつくっている。"),
    ("l_caldera", "land", "カルデラ", "かるでら", 43, "area", (32.9, 131.06), 0.13, 0.16, 0,
     "火山のふん火のあとにできた大きなくぼ地。熊本県の阿蘇山のカルデラは世界最大級で、中に町や田畑がある。"),
    ("l_wajyu", "land", "輪中", "わじゅう", 21, "area", (35.2, 136.66), 0.08, 0.1, 0,
     "まわりを堤防で囲んで水害から守った集落。木曽川・長良川・揖斐川（木曽三川）が流れる濃尾平野の西部に多い。"),
    ("l_kantaku", "land", "干拓地", "かんたくち", 5, "area", (39.93, 140.02), 0.09, 0.11, 0,
     "湖や海を堤防で区切り、水をぬいて陸地にした土地。秋田県の八郎潟は大規模な干拓地で、大型機械で米をつくる。有明海や児島湾でも干拓が行われた。"),
    ("l_bonchi", "land", "盆地", "ぼんち", 6, "area", (38.3, 140.3), 0.12, 0.25, 0,
     "まわりを山に囲まれた平らな土地。夏は暑く冬は寒い。山形盆地ではさくらんぼ、甲府盆地ではぶどうやももの栽培がさかん。"),
    ("l_karst", "land", "カルスト地形", "かるすとちけい", 35, "area", (34.25, 131.3), 0.09, 0.07, 0,
     "石灰岩が雨水にとけてできた地形。山口県の秋吉台が日本最大で、地下には秋芳洞という大きな鍾乳洞がある。"),
    ("l_sandy", "land", "砂浜海岸", "すなはまかいがん", 12, "line", [(35.71, 140.86), (35.62, 140.66), (35.5, 140.5), (35.38, 140.43), (35.29, 140.41)], 0, 0, 0,
     "すなが積もってできた、なだらかでまっすぐな海岸。千葉県の九十九里浜は約60kmも続く。"),
    ("c_sanriku", "coast", "三陸海岸", "さんりくかいがん", 3, "line", [(40.5, 141.62), (40.2, 141.88), (39.95, 141.97), (39.6, 141.98), (39.27, 141.9), (38.95, 141.68), (38.7, 141.52), (38.42, 141.48)], 0, 0, 0,
     "青森県・岩手県・宮城県の太平洋側の海岸。南部はリアス海岸で、わかめ・かき・ほたての養殖がさかん。"),
    ("c_wakasa", "coast", "若狭湾", "わかさわん", 18, "sea", (35.62, 135.75), 0.45, 0.16, 0,
     "福井県から京都府にかけての日本海側の湾。リアス海岸で、原子力発電所が多い。"),
    ("c_shima", "coast", "志摩半島", "しまはんとう", 24, "area", (34.35, 136.78), 0.17, 0.11, 0,
     "三重県の半島。リアス海岸の英虞湾で真珠の養殖が行われている。"),
    ("c_uwa", "coast", "宇和海", "うわかい", 38, "sea", (33.2, 132.38), 0.12, 0.3, 0,
     "愛媛県の西側の海。リアス海岸で、まだいや真珠の養殖がさかん。"),
    ("c_kujukuri", "coast", "九十九里浜", "くじゅうくりはま", 12, "line", [(35.71, 140.86), (35.62, 140.66), (35.5, 140.5), (35.38, 140.43), (35.29, 140.41)], 0, 0, 0,
     "千葉県の太平洋側に約60km続く砂浜海岸。いわし漁がさかんで、地引き網でも知られる。"),
    ("c_noto", "coast", "能登半島", "のとはんとう", 17, "area", (37.2, 136.95), 0.32, 0.3, 0,
     "石川県の日本海につき出た半島。輪島塗や、「能登の里山里海」として知られる。"),
    ("c_boso", "coast", "房総半島", "ぼうそうはんとう", 12, "area", (35.15, 140.05), 0.27, 0.22, 0,
     "千葉県の南部の半島。東京湾と太平洋にはさまれ、あたたかい気候を生かした花や野菜づくりがさかん。"),
    ("c_izu", "coast", "伊豆半島", "いずはんとう", 22, "area", (34.85, 138.95), 0.14, 0.24, 0,
     "静岡県の東部の半島。温泉が多く、観光がさかん。"),
    ("c_shiretoko", "coast", "知床半島", "しれとこはんとう", 1, "poly", [(43.86, 144.95), (44.02, 144.72), (44.45, 145.3), (44.32, 145.48)], 0, 0, 0,
     "北海道の東部の半島。流氷が届き、豊かな自然が世界自然遺産に登録されている。"),
    ("c_ariake", "coast", "有明海", "ありあけかい", 41, "sea", (33.0, 130.3), 0.13, 0.27, 0,
     "福岡県・佐賀県・長崎県・熊本県に囲まれた海。干満の差が大きく、のりの養殖や干拓が行われてきた。"),
    ("c_mutsu", "coast", "陸奥湾", "むつわん", 2, "sea", (41.0, 140.95), 0.22, 0.13, 0,
     "青森県の湾。ほたての養殖がさかん。"),
    ("c_tokyo", "coast", "東京湾", "とうきょうわん", 13, "sea", (35.45, 139.85), 0.12, 0.22, 0,
     "東京都・神奈川県・千葉県に面した湾。まわりに京浜工業地帯・京葉工業地域が広がる。"),
    ("c_ise", "coast", "伊勢湾", "いせわん", 23, "sea", (34.85, 136.75), 0.16, 0.25, 0,
     "愛知県と三重県に面した湾。まわりに中京工業地帯が広がる。"),
    ("c_suruga", "coast", "駿河湾", "するがわん", 22, "sea", (34.85, 138.62), 0.13, 0.25, 0,
     "静岡県の湾。日本でいちばん深い湾で、さくらえびが有名。焼津港がある。"),
]


def ellipse(lat, lon, rx, ry, rot):
    a = math.radians(rot)
    ring = []
    for i in range(48):
        t = 2 * math.pi * i / 48
        dx, dy = rx * math.cos(t), ry * math.sin(t)
        ring.append(proj(lat + (dx * math.sin(a) + dy * math.cos(a)), lon + (dx * math.cos(a) - dy * math.sin(a))))
    return Polygon(ring)


def landforms(L, Lraw):
    out = []
    for fid, cat, name, kana, pref, shape, geo, rx, ry, rot, note in LANDFORMS:
        if shape == "line":
            pts = [proj(*p) for p in geo]
            out.append({"id": fid, "cat": cat, "kind": "range", "name": name, "kana": kana, "pref": pref, "d": path_d(pts), "b": bbox(pts), "note": note})
            continue
        e = Polygon([proj(*p) for p in geo]) if shape == "poly" else ellipse(geo[0], geo[1], rx, ry, rot)
        g = e.difference(Lraw) if shape == "sea" else e.intersection(L)
        polys = list(g.geoms) if isinstance(g, MultiPolygon) else [g]
        polys = [p.simplify(0.3) for p in polys if not p.is_empty and p.area > 1.5]
        polys.sort(key=lambda p: -p.area)
        if shape == "sea":
            polys = polys[:1]   # 湾・海は、楕円の中でいちばん大きな水面だけ
        dd = "".join(path_d(list(p.exterior.coords)[:-1]) + "Z" for p in polys)
        out.append({"id": fid, "cat": cat, "kind": "plain", "name": name, "kana": kana, "pref": pref, "d": dd,
                    "b": bbox([c for p in polys for c in p.exterior.coords]), "note": note})
    return out


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
    Lraw = unary_union([Polygon([tuple(map(float, q.split(","))) for q in part.split("L")]).buffer(0)
                        for o in json.load(open(DATA / "paths.json", encoding="utf-8")) for part in re.findall(r"M([^Z]+)Z", o["d"])
                        if len(part.split("L")) >= 3])
    feats += landforms(L, Lraw)
    (DATA / "terrain.json").write_text(json.dumps(feats, ensure_ascii=False, separators=(",", ":")), encoding="utf-8", newline="\n")
    print("wrote terrain.json:", len(feats), "features")


if __name__ == "__main__":
    main()
