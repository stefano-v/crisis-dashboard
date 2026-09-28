# Crisis Dashboard USA

Dashboard statica per GitHub Pages. Legge dal browser alcune serie pubbliche FRED e applica le soglie concordate.

## Pubblicazione
Il repository include una GitHub Action in `.github/workflows/pages.yml` che pubblica automaticamente il contenuto su GitHub Pages ad ogni push su `main`.

## Serie
- BAMLH0A0HYM2 — US High Yield Option-Adjusted Spread
- SAHMREALTIME — Sahm Rule Recession Indicator
- UNRATE — Unemployment Rate
- T10Y2Y — 10Y minus 2Y Treasury spread
- SP500 — S&P 500
- DFF — Effective Federal Funds Rate

## Nota tecnica
Il sito usa `fetch()` verso il CSV pubblico di FRED. Se FRED dovesse bloccare richieste cross-origin, la UI mostrerà N/D.

## Disclaimer
Strumento informativo di monitoraggio, non previsione certa e non consulenza finanziaria.
