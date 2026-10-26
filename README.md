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

Follow the handout for the activities. No downloads, dashboard server, API
keys, or Module 7 files are needed. The winter counts come from Module 7's
unchanged-source example; the other inputs are synthetic practice tables.

Run one file:

```text
uv run python -m pytest tests/test_my_checks.py -q
```

Keep the course exercises local; do not push to the shared course repo.
For homework, work in your team project's repository on your own branch.
