# Function contracts

These functions use the Module 7 wildfire definitions. Counts are reported
records. Known acres are final reported sizes grouped by discovery month.

All functions leave their input tables unchanged.

## first_threshold(counts, target=5)

Input: nonempty county-month rows, sorted by county then month, with unique
county-month keys and nonnegative integer `fires`. `target` is positive.

Return the original columns plus `running`, `hit`, and `reached`.
`running` accumulates within each county; `hit` means at least the target.
`reached` is True only at the first hit in each county, or nowhere if it
never reaches the target. Preserve the input order.

## month_changes(counts)

Input: a nonempty, complete monthly sequence with unique month-start dates
and nonnegative integer `fires`; rows may arrive in any order.

Return rows in chronological order, with `previous`, `change`, `average_3m`,
and `running`. The average includes this month and up to two previous calendar
months. The running count starts at the first supplied month. The first
`previous` and `change` are missing. Neither calculation restarts in January.

## selected_year_report(counts, year)

Input: the same table as `month_changes` and an integer year.

Return that year's rows with all four trend columns. Calculate trends on the
full supplied sequence before selecting the year. If the year is absent,
return an empty table with the same columns.

## select_year(monthly, year)

Input: a monthly table with a datetime `month` column and a unique row index.

Return only the selected year's rows, preserving their order, index, and
columns. An absent year returns an empty table. Repeated calls on the same
input must work for any year.

## monthly_summary(fires)

Input: `DISCOVERY_DATE` is datetime, possibly missing; `FIRE_SIZE` is numeric,
nonnegative or missing. There is at least one usable discovery date.

Return one row per calendar month from the earliest through latest discovery
month, ordered by month: `month`, `fires`, `known_acres`, `sizes_known`.
Count records with usable dates, sum known sizes, and count known sizes.
Insert absent months with zeros. A month with records but all sizes missing
has `known_acres=0` and `sizes_known=0`; it does not establish zero burned acres.
