"""Rebuild the downloadable table: python -m wildfire_dashboard.build_drought_table."""
from .drought_data import OUTPUTS, load_drought, join_monthly
from .wildfire_data import load_fires

if __name__ == "__main__":
    table = join_monthly(load_fires(), load_drought(), (1992, 2024))
    table.to_csv(OUTPUTS / "wildfire_drought_ca_monthly.csv", index=False)
    print(f"Saved {len(table)} monthly rows")
