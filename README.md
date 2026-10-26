# Module 10 — Test the business rule

## Main activities

Open `pytest_business_in_class.ipynb` in VS Code. In the terminal, run
`uv sync --extra notebook`, then select this folder’s `.venv` as the notebook
kernel. Run cells in order. Response cells are collapsed for now; expand
them when needed. Worked solutions are kept in the instructor package.

Session 1: guided shipping tests, then hotel refunds in [Pair Up](https://dso576.vercel.app/pair).
Session 2: customer conversion, then tests of the wildfire dashboard.
Discounts and retention are optional extensions.

The notebook creates exercise files under `pytest_business_lab/`. Edit and save
those `.py` files in VS Code, then rerun the notebook’s test cell. Starter cells
preserve existing files; editing their quoted text does not update files already created.
The guided shipping boundary test deliberately fails until you repair the function.

## Wildfire project and extra practice

In the terminal:

```text
uv sync --frozen
uv run python -m pytest -q
```

- `wildfire.py` — practice implementations; some are deliberately incorrect.
- `contracts.md` — what each function receives and returns.
- `sample_data.py` — small fixed inputs; each function returns a fresh table.
- `tests/test_existing.py` — supplied tests.
- `tests/test_my_checks.py` — add your in-class tests here.

## Run and view the wildfire dashboard

1. Open your cloned **10-test** folder in VS Code. Choose **Terminal → New Terminal**.
   Run the command below from `10-test`, not from `wildfire_dashboard`:

   ```text
   uv run --extra dashboard python -m wildfire_dashboard.html_dashboard
   ```

2. Wait for `HTML dashboard: http://127.0.0.1:8000`, then open
   [the dashboard in your browser](http://127.0.0.1:8000).
   Keep the terminal running while you use the page.

3. Select **California** and years within **2000–2024** to see wildfire and drought
   together. Try the filters and download the complementary CSV files.

4. Press **Ctrl+C** in the terminal when finished.

The first run installs the dashboard packages. All data is included.
**Do not double-click `index.html`**: its charts need the Python server.
If port 8000 is busy, see the [dashboard README](wildfire_dashboard/README.md).

`tests/test_dashboard.py` and `tests/test_drought.py` test the dashboard’s Python
calculations. `wildfire.py` contains separate, simplified class exercises.

## Extra wildfire exercises

The wildfire handout provides additional practice. The class tests need no data downloads, server, API keys, or Module 7 files. The winter counts come from Module 7's
unchanged-source example; the other inputs are synthetic practice tables.

Run one file:

```text
uv run python -m pytest tests/test_my_checks.py -q
```

Keep the course exercises local; do not push to the shared course repo.
For homework, work in your team project's repository on your own branch.
