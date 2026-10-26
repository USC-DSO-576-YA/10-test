# Module 10 — Test the wildfire report

Open this folder in VS Code. In its terminal:

```text
uv sync --frozen
uv run python -m pytest -q
```

- `wildfire.py` — practice implementations; some are deliberately incorrect.
- `contracts.md` — what each function receives and returns.
- `sample_data.py` — small fixed inputs; each function returns a fresh table.
- `tests/test_existing.py` — supplied tests.
- `tests/test_my_checks.py` — add your in-class tests here.

## See the wildfire dashboard

The original **Wildfire Atlas** is in [`wildfire_dashboard/`](wildfire_dashboard/README.md). From this folder, run:

```text
uv run --extra dashboard python -m wildfire_dashboard.html_dashboard
```

Open http://127.0.0.1:8000. Stop the server with Ctrl+C. The first launch installs
the dashboard packages; its data is included. Do not double-click the HTML: the
charts use the local Python server.

`tests/test_dashboard.py` checks two calculations in the actual dashboard backend.
The functions in `wildfire.py` are separate, simplified class exercises.

## Class exercises

Follow the handout for the activities. The class tests need no data downloads, server, API keys, or Module 7 files. The winter counts come from Module 7's
unchanged-source example; the other inputs are synthetic practice tables.

Run one file:

```text
uv run python -m pytest tests/test_my_checks.py -q
```

Keep the course exercises local; do not push to the shared course repo.
For homework, work in your team project's repository on your own branch.
