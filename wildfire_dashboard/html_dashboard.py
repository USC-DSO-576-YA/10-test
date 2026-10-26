"""Serve the HTML wildfire dashboard using the same local data as dashboard.py.

Run from the repo root: uv run --extra dashboard python -m wildfire_dashboard.html_dashboard
"""

from __future__ import annotations

import argparse
import json
import math
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import plotly.offline

from .drought_data import load_drought, join_monthly

from .wildfire_data import (
    DATA_PATH, MONTHLY_PATH, STATE_CODES, STATE_NAMES, cause_yearly, causes,
    filter_fires, load_fires, load_notebook_monthly, metrics, seasonality,
    sizes, state_comparison, yearly,
)

ROOT = Path(__file__).resolve().parent
WEB = ROOT / "web"


def records(frame):
    """Turn pandas values into JSON-safe chart rows."""
    return json.loads(frame.to_json(orient="records", date_format="iso"))


def finite(value):
    return value if value is not None and math.isfinite(value) else None


def years_from(query, bounds):
    try:
        start = int(query.get("start", [bounds[0]])[0])
        end = int(query.get("end", [bounds[1]])[0])
    except (ValueError, TypeError) as exc:
        raise ValueError("Years must be integers") from exc
    if not (bounds[0] <= start <= end <= bounds[1]):
        raise ValueError(f"Choose years between {bounds[0]} and {bounds[1]}")
    return start, end


def make_handler(fires, monthly, plotly_js):
    drought = load_drought()
    bounds = (int(fires["year"].min()), int(fires["year"].max()))
    causes_list = sorted(str(value) for value in fires["reported_cause"].dropna().unique())
    available_states = sorted(
        set(fires["state"].dropna().unique()).intersection(STATE_CODES),
        key=lambda code: STATE_NAMES[code],
    )

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            pass

        def send_bytes(self, body: bytes, content_type: str, status=200):
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def send_json(self, data, status=200):
            self.send_bytes(json.dumps(data, allow_nan=False).encode(), "application/json; charset=utf-8", status)

        def do_GET(self):
            request = urlsplit(self.path)
            query = parse_qs(request.query)
            try:
                if request.path == "/api/meta":
                    self.send_json({
                        "years": bounds,
                        "records": len(fires),
                        "states": [{"code": code, "name": STATE_NAMES[code]} for code in available_states],
                        "causes": causes_list,
                    })
                elif request.path == "/api/overview":
                    years = years_from(query, bounds)
                    state = query.get("state", ["CA"])[0]
                    cause = query.get("cause", [""])[0] or None
                    if state not in available_states or (cause is not None and cause not in causes_list):
                        raise ValueError("Unknown state or reported cause")
                    state_year = filter_fires(fires, years, state=state)
                    selected = filter_fires(state_year, years, cause=cause)
                    summary = metrics(selected)
                    state_summary = metrics(state_year)
                    payload = {
                        "metrics": {
                            "fires": summary.fires,
                            "acres": finite(summary.acres),
                            "median_size": finite(summary.median_size),
                            "unknown_pct": finite(state_summary.unknown_pct),
                        },
                        "annual": records(yearly(selected, years)),
                        "seasonality": records(seasonality(selected)),
                        "causes": records(causes(selected)),
                        "sizes": records(sizes(selected)),
                        "cause_yearly": records(cause_yearly(selected)),
                        "monthly": None,
                        "drought": records(join_monthly(selected, drought, years, state)),
                    }
                    if state == "CA" and cause is None and monthly is not None:
                        subset = monthly.loc[monthly["month"].dt.year.between(*years)]
                        payload["monthly"] = records(subset)
                    self.send_json(payload)
                elif request.path == "/api/comparison":
                    years = years_from(query, bounds)
                    table = state_comparison(filter_fires(fires, years))
                    self.send_json({"states": records(table)})
                elif request.path in ("/data/drought_ca_weekly.csv", "/data/wildfire_drought_ca_monthly.csv"):
                    self.send_bytes((ROOT / "outputs" / request.path.rsplit("/", 1)[1]).read_bytes(), "text/csv; charset=utf-8")
                elif request.path == "/plotly.min.js":
                    self.send_bytes(plotly_js, "text/javascript; charset=utf-8")
                else:
                    assets = {
                        "/": ("index.html", "text/html; charset=utf-8"),
                        "/styles.css": ("styles.css", "text/css; charset=utf-8"),
                        "/app.js": ("app.js", "text/javascript; charset=utf-8"),
                        "/topojson/usa_110m.json": ("topojson/usa_110m.json", "application/json"),
                    }
                    if request.path not in assets:
                        self.send_error(404)
                        return
                    filename, content_type = assets[request.path]
                    self.send_bytes((WEB / filename).read_bytes(), content_type)
            except ValueError as exc:
                self.send_json({"error": str(exc)}, 400)
            except (BrokenPipeError, ConnectionResetError):
                pass

    return Handler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    if not DATA_PATH.exists():
        parser.error("Bundled data missing: wildfire_dashboard/outputs/fires_national.parquet. Restore it from the course repository.")
    fires = load_fires()
    monthly = load_notebook_monthly() if MONTHLY_PATH.exists() else None
    handler = make_handler(fires, monthly, plotly.offline.get_plotlyjs().encode())
    server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
    print(f"HTML dashboard: http://127.0.0.1:{args.port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
