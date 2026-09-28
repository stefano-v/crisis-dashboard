#!/usr/bin/env python3
import csv, io, json, subprocess
from pathlib import Path
from datetime import datetime, timezone

SERIES = ["BAMLH0A0HYM2","SAHMREALTIME","UNRATE","T10Y2Y","SP500","DFF"]

def fetch_text(url):
    p = subprocess.run(
        ["curl","--fail","--silent","--show-error","--location",
         "--retry","3","--retry-delay","2",
         "-A","Mozilla/5.0 crisis-dashboard/1.0", url],
        check=True, capture_output=True, text=True
    )
    return p.stdout

def fetch_series(series_id):
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    text = fetch_text(url)
    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames or len(reader.fieldnames) < 2:
        raise RuntimeError(f"Unexpected CSV header for {series_id}: {reader.fieldnames}")
    date_field = reader.fieldnames[0]
    value_field = series_id if series_id in reader.fieldnames else reader.fieldnames[1]
    rows = []
    for row in reader:
        raw = row.get(value_field, "")
        try:
            value = float(raw)
        except (TypeError, ValueError):
            continue
        rows.append({"date": row.get(date_field, ""), "v": value})
    if not rows:
        raise RuntimeError(f"No numeric observations returned for {series_id}")
    return rows[-800:]

payload = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "source": "FRED",
    "series": {}
}

for sid in SERIES:
    print(f"Fetching {sid}...", flush=True)
    payload["series"][sid] = fetch_series(sid)
    print(f"  {len(payload['series'][sid])} observations", flush=True)

out = Path("data/data.json")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(f"Wrote {out}", flush=True)
