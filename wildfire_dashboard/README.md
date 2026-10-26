# Wildfire Atlas

The HTML dashboard from Module 7, with its Python calculations and bundled
USDA wildfire data. Launch it from the **10-test folder**:

```text
uv run --extra dashboard python -m wildfire_dashboard.html_dashboard
```

Open http://127.0.0.1:8000. Leave the terminal running; Ctrl+C stops it.
If the port is occupied, add `--port 8010` and open http://127.0.0.1:8010.
The first launch installs Plotly and PyArrow. After installation, the app uses
local data and assets; no API key or data download is needed.

## Files

- `web/index.html` — the page; `app.js` and `styles.css` provide interactions and styling.
- `html_dashboard.py` — serves the page and answers its data requests.
- `wildfire_data.py` — filters, metrics, and chart calculations.
- `outputs/` — national fire records, source metadata, and the California monthly table.

## What the tests check

From `10-test`, run:

```text
uv run python -m pytest tests/test_dashboard.py -q
```

These tests call the same `metrics` and `seasonality` functions used by the
page. They use small synthetic inputs with independently known answers.
They do not test the browser controls, every calculation, or the full dataset.

The handout's `wildfire.py` is a separate teaching exercise, not a dependency
of this dashboard. Changing it will not change this page.

## Source

Copied from the instructor's Module 7 Wildfire Atlas. The original fire calculations and data are preserved. The server was adapted
to run inside this folder; the page now also includes complementary drought data.

Data: USDA Forest Service FPA FOD, seventh edition, 1992–2024.
[Dataset documentation](https://doi.org/10.2737/RDS-2013-0009.7).
`outputs/fires_national.json` records the service, fields, and record count.
Counts describe reported occurrences; summed final sizes are not distinct
land burned during the selected period.

## Complementary data: drought

The overview compares California fire counts with drought coverage.
Choose California and years overlapping 2000–2024. Other states show
an unavailable-data message. The cause filter changes fires, not drought.

- `outputs/drought_ca_weekly.csv` — original weekly U.S. Drought Monitor data.
- `outputs/wildfire_drought_ca_monthly.csv` — fire counts joined to monthly drought.
- `outputs/drought_source.json` — source URL, download date, and transformation.
- `drought_data.py` — aggregation and join used by the page.

[Source documentation](https://droughtmonitor.unl.edu/DmData/DataDownload/WebServiceInfo.aspx).
D1 measures state area in moderate **or worse** drought; it already includes
D2–D4. Do not add those columns. Monthly values average weekly maps dated
within each month; they are not daily averages. Before 2000, drought is
missing, not zero. Shared trends do not establish causation.

Both CSVs are linked on the page. The joined download always contains
California, all causes, and 1992–2024; it does not follow filters. Rebuild it:

```text
uv run --extra dashboard python -m wildfire_dashboard.build_drought_table
```

`tests/test_drought.py` checks averages, state matching, missing values, and
joins that could multiply rows. Run it:

```text
uv run python -m pytest tests/test_drought.py -q
```
