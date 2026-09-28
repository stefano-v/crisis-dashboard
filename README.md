# Crisis Dashboard USA

Dashboard statica per GitHub Pages che monitora alcuni indicatori macro-finanziari USA.

Versione corrente: **v1.1.0**

## Sito
https://stefano-v.github.io/crisis-dashboard/

## Serie
- BAMLH0A0HYM2 — US High Yield Option-Adjusted Spread
- SAHMREALTIME — Sahm Rule Recession Indicator
- UNRATE — Unemployment Rate
- T10Y2Y — 10Y minus 2Y Treasury spread
- SP500 — S&P 500
- DFF — Effective Federal Funds Rate

## Aggiornamento dati
La GitHub Action prova a scaricare i dati FRED lato server e genera `data/data.json`.
Se il refresh live fallisce, il deploy continua usando l'ultimo dataset disponibile nel repository.

## Interpretazione
High-Yield spread, Sahm Rule, disoccupazione e drawdown S&P 500 usano soglie semaforiche.
10Y–2Y ed Effective Fed Funds sono invece indicatori contestuali: vengono mostrati come **Monitoraggio**
perché il loro livello assoluto, da solo, non determina uno stato verde/giallo/rosso affidabile.

## Licenza
MIT. Vedi [LICENSE](LICENSE).

## Disclaimer
Strumento informativo di monitoraggio, non previsione certa e non consulenza finanziaria.
