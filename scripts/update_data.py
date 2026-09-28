#!/usr/bin/env python3
import csv, io, json, urllib.request
from pathlib import Path
from datetime import datetime, timezone

SERIES = ["BAMLH0A0HYM2","SAHMREALTIME","UNRATE","T10Y2Y","SP500","DFF"]

def fetch_series(series_id):
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    req = urllib.request.Request(url, headers={"User-Agent":"crisis-dashboard/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        text = r.read().decode("utf-8-sig")
    rows = []
    for row in csv.DictReader(io.StringIO(text)):
        raw = row.get(series_id, "")
        try:
            value = float(raw)
        except (TypeError, ValueError):
            continue
        rows.append({"date": row["DATE"], "v": value})
    return rows[-800:]

payload = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "source": "FRED",
    "series": {sid: fetch_series(sid) for sid in SERIES},
}

out = Path("data/data.json")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(f"Wrote {out} with {sum(len(v) for v in payload['series'].values())} observations")
