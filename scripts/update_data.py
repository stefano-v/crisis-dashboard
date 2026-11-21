#!/usr/bin/env python3
import csv, io, json, subprocess, sys
from pathlib import Path
from datetime import datetime, timezone

FRED_SERIES = ["BAMLH0A0HYM2","SAHMREALTIME","UNRATE","T10Y2Y","SP500","DFF"]
MARKETS = {"^GSPC":"S&P 500","^IXIC":"Nasdaq Composite","^DJI":"Dow Jones"}
OUT = Path("data/data.json")

def fetch_text(url):
    p = subprocess.run(
        ["curl","--fail","--silent","--show-error","--location",
         "--retry","2","--retry-delay","2",
         "-A","Mozilla/5.0 crisis-dashboard/1.2", url],
        check=True, capture_output=True, text=True
    )
    return p.stdout

def fetch_fred(series_id):
    text = fetch_text(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}")
    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames or len(reader.fieldnames) < 2:
        raise RuntimeError(f"Unexpected CSV header for {series_id}: {reader.fieldnames}")
    date_field = reader.fieldnames[0]
    value_field = series_id if series_id in reader.fieldnames else reader.fieldnames[1]
    rows = []
    for row in reader:
        try:
            value = float(row.get(value_field, ""))
        except (TypeError, ValueError):
            continue
        rows.append({"date": row.get(date_field, ""), "v": value})
    if not rows:
        raise RuntimeError(f"No numeric observations returned for {series_id}")
    return rows[-800:]

def fetch_market(symbol):
    encoded = symbol.replace("^", "%5E")
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{encoded}?range=1y&interval=1d&events=history&includeAdjustedClose=true"
    obj = json.loads(fetch_text(url))
    result = (obj.get("chart",{}).get("result") or [None])[0]
    if not result:
        raise RuntimeError(f"No market result for {symbol}")
    ts = result.get("timestamp") or []
    closes = (((result.get("indicators") or {}).get("adjclose") or [{}])[0].get("adjclose")
              or (((result.get("indicators") or {}).get("quote") or [{}])[0].get("close")) or [])
    rows=[]
    for t,v in zip(ts,closes):
        if v is None:
            continue
        d=datetime.fromtimestamp(t, timezone.utc).date().isoformat()
        rows.append({"date":d,"v":float(v)})
    if len(rows)<2:
        raise RuntimeError(f"Insufficient market history for {symbol}")
    return rows[-300:]

existing={"series":{},"market":{}}
if OUT.exists():
    try:
        existing=json.loads(OUT.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"WARNING: cannot read existing fallback: {e}", file=sys.stderr)

payload={
    "generated_at":datetime.now(timezone.utc).isoformat(),
    "source":"FRED + Yahoo Finance; checked-in fallback on fetch errors",
    "series":dict(existing.get("series") or {}),
    "market":dict(existing.get("market") or {})
}

for sid in FRED_SERIES:
    try:
        print(f"Fetching FRED {sid}...", flush=True)
        payload["series"][sid]=fetch_fred(sid)
    except Exception as e:
        print(f"WARNING: FRED {sid} failed: {e}; keeping fallback.", file=sys.stderr)

for symbol,name in MARKETS.items():
    try:
        print(f"Fetching market {name} ({symbol})...", flush=True)
        payload["market"][symbol]=fetch_market(symbol)
    except Exception as e:
        print(f"WARNING: market {symbol} failed: {e}; keeping fallback.", file=sys.stderr)

if payload["market"].get("^GSPC"):
    payload["series"]["SP500"]=payload["market"]["^GSPC"]

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(f"Wrote {OUT}; FRED={len(payload['series'])} market={len(payload['market'])}", flush=True)
