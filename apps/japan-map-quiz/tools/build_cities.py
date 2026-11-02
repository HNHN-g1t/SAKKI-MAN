"""県庁所在地・4択の選択肢・政令指定都市のデータを、総務省の公式一覧で確認して data/cities.json に書き出す。

使い方:  python3 tools/build_cities.py <総務省 都道府県コード及び市区町村コード.xlsx>
  入手先: https://www.soumu.go.jp/denshijiti/code.html （確認に使った版: 令和6年1月1日更新 000925835.xlsx）
政令指定都市の一覧: https://www.soumu.go.jp/main_sosiki/jichi_gyousei/bunken/shitei_toshi-ichiran.html （20市）

- 名前が公式一覧に無い・所属する都道府県が違うときは止まる
- 読み仮名は公式一覧のカナ（半角カタカナ）をひらがなにしたもの
"""
import json
import sys
import unicodedata
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 都道府県コード: [県庁所在地（東京都は都庁のある区）, 誤答に使う同じ都道府県の市区町村 x3]
CAPITALS = {
    1: ["札幌市", "函館市", "旭川市", "釧路市"],
    2: ["青森市", "弘前市", "八戸市", "十和田市"],
    3: ["盛岡市", "花巻市", "一関市", "宮古市"],
    4: ["仙台市", "石巻市", "気仙沼市", "名取市"],
    5: ["秋田市", "横手市", "大館市", "能代市"],
    6: ["山形市", "米沢市", "鶴岡市", "酒田市"],
    7: ["福島市", "郡山市", "いわき市", "会津若松市"],
    8: ["水戸市", "日立市", "つくば市", "土浦市"],
    9: ["宇都宮市", "日光市", "小山市", "足利市"],
    10: ["前橋市", "高崎市", "桐生市", "伊勢崎市"],
    11: ["さいたま市", "川越市", "所沢市", "川口市"],
    12: ["千葉市", "船橋市", "成田市", "銚子市"],
    13: ["新宿区", "千代田区", "港区", "渋谷区"],
    14: ["横浜市", "川崎市", "横須賀市", "相模原市"],
    15: ["新潟市", "長岡市", "上越市", "佐渡市"],
    16: ["富山市", "高岡市", "黒部市", "魚津市"],
    17: ["金沢市", "小松市", "加賀市", "輪島市"],
    18: ["福井市", "敦賀市", "鯖江市", "小浜市"],
    19: ["甲府市", "富士吉田市", "甲斐市", "笛吹市"],
    20: ["長野市", "松本市", "上田市", "諏訪市"],
    21: ["岐阜市", "大垣市", "高山市", "多治見市"],
    22: ["静岡市", "浜松市", "沼津市", "富士市"],
    23: ["名古屋市", "豊田市", "岡崎市", "豊橋市"],
    24: ["津市", "四日市市", "伊勢市", "鈴鹿市"],
    25: ["大津市", "彦根市", "草津市", "長浜市"],
    26: ["京都市", "舞鶴市", "宇治市", "福知山市"],
    27: ["大阪市", "堺市", "東大阪市", "豊中市"],
    28: ["神戸市", "姫路市", "西宮市", "尼崎市"],
    29: ["奈良市", "橿原市", "天理市", "生駒市"],
    30: ["和歌山市", "田辺市", "新宮市", "海南市"],
    31: ["鳥取市", "米子市", "倉吉市", "境港市"],
    32: ["松江市", "出雲市", "浜田市", "益田市"],
    33: ["岡山市", "倉敷市", "津山市", "玉野市"],
    34: ["広島市", "福山市", "呉市", "尾道市"],
    35: ["山口市", "下関市", "宇部市", "岩国市"],
    36: ["徳島市", "鳴門市", "阿南市", "小松島市"],
    37: ["高松市", "丸亀市", "坂出市", "観音寺市"],
    38: ["松山市", "今治市", "新居浜市", "宇和島市"],
    39: ["高知市", "南国市", "四万十市", "室戸市"],
    40: ["福岡市", "北九州市", "久留米市", "大牟田市"],
    41: ["佐賀市", "唐津市", "鳥栖市", "伊万里市"],
    42: ["長崎市", "佐世保市", "諫早市", "島原市"],
    43: ["熊本市", "八代市", "天草市", "人吉市"],
    44: ["大分市", "別府市", "中津市", "日田市"],
    45: ["宮崎市", "都城市", "延岡市", "日南市"],
    46: ["鹿児島市", "霧島市", "薩摩川内市", "鹿屋市"],
    47: ["那覇市", "沖縄市", "名護市", "浦添市"],
}

# 政令指定都市（総務省「指定都市一覧」の20市。移行年月日順）
DESIGNATED = [
    "大阪市", "名古屋市", "京都市", "横浜市", "神戸市", "北九州市", "札幌市", "川崎市", "福岡市", "広島市",
    "仙台市", "千葉市", "さいたま市", "静岡市", "堺市", "新潟市", "浜松市", "岡山市", "相模原市", "熊本市",
]

PREF_NAMES = ["北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県", "茨城県", "栃木県", "群馬県",
              "埼玉県", "千葉県", "東京都", "神奈川県", "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県",
              "岐阜県", "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県", "奈良県", "和歌山県",
              "鳥取県", "島根県", "岡山県", "広島県", "山口県", "徳島県", "香川県", "愛媛県", "高知県", "福岡県",
              "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"]

def hira(s):
    s = unicodedata.normalize("NFKC", s)
    return "".join(chr(ord(c) - 0x60) if "ァ" <= c <= "ヶ" else c for c in s)


def read_xlsx(path):
    ns = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
    z = zipfile.ZipFile(path)
    ss = ["".join(t.text or "" for t in si.iter(ns + "t"))
          for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall(ns + "si")]
    sheet = sorted(n for n in z.namelist() if n.startswith("xl/worksheets/sheet"))[0]
    out = {}
    for row in ET.fromstring(z.read(sheet)).iter(ns + "row"):
        vals = []
        for c in row.findall(ns + "c"):
            v = c.find(ns + "v")
            val = v.text if v is not None else ""
            vals.append(ss[int(val)] if c.get("t") == "s" else val)
        if len(vals) >= 5 and vals[2] and vals[0][:2].isdigit():
            out[(vals[1], vals[2])] = hira(vals[4])
    return out


def kana_of(official, pref, city):
    key = (pref, city)
    if key not in official:
        sys.exit(f"公式一覧に無い: {pref} {city}")
    return official[key]


def main():
    official = read_xlsx(sys.argv[1])
    data = {"capitals": {}, "designated": []}
    for code, names in CAPITALS.items():
        pref = PREF_NAMES[code - 1]
        assert len(set(names)) == 4, f"重複: {names}"
        data["capitals"][code] = [[n, kana_of(official, pref, n)] for n in names]
    for city in DESIGNATED:
        hits = [p for (p, c) in official if c == city]
        assert len(hits) == 1, f"{city} の都道府県が1つに決まらない: {hits}"
        code = PREF_NAMES.index(hits[0]) + 1
        data["designated"].append([city, kana_of(official, hits[0], city), code])
    out = ROOT / "data" / "cities.json"
    out.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8", newline="\n")
    print(f"wrote {out}: 県庁所在地 {len(data['capitals'])} / 政令指定都市 {len(data['designated'])}")


if __name__ == "__main__":
    main()
