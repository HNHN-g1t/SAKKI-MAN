from pathlib import Path
DATA = Path(__file__).resolve().parent.parent / "data"
import json, sys
src = sys.argv[1]
with open(src, encoding="utf-8") as f:
    d = json.load(f)
jp = [ft for ft in d["features"] if ft["properties"].get("adm0_a3") == "JPN"]
print(len(jp))
for ft in jp:
    p = ft["properties"]
    print(p.get("iso_3166_2"), p.get("name"), p.get("name_ja"), ft["geometry"]["type"])
with open(str(DATA / "jp_raw.json"), "w", encoding="utf-8") as f:
    json.dump({"type": "FeatureCollection", "features": jp}, f, ensure_ascii=False)
