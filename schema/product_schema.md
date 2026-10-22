# Product Schema

This document defines the standard data product for SeriesSmith. Every conversion must conform to it exactly. Consistency across releases is what makes products comparable, and comparability is the value of the product.

## 1. The dataset: `data.csv`

One row per indicator per period. Columns in this exact order:

| # | Column | Content |
| --- | --- | --- |
| 1 | `indicator_id` | Stable machine-readable identifier for the indicator (see Section 2). |
| 2 | `indicator_name` | Canonical English display name (see Section 2). |
| 3 | `category` | One of the fixed categories (see Section 3). |
| 4 | `geography` | Country or region the row describes, including area splits where the source makes them (for example, "China", "China, Urban", "China, Rural"). |
| 5 | `period` | The reference period (see Section 4). |
| 6 | `frequency` | "Monthly", "Quarterly", or "Annual", describing the indicator's reporting frequency. |
| 7 | `value` | The level or index value, exactly as published. Empty when the row exists only to carry a published change (see Section 5). |
| 8 | `unit` | The unit of `value`, spelled out (see Section 5). |
| 9 | `yoy_pct` | Year-on-year percent change, as published, or computed from published levels with a note. Empty if not available. |
| 10 | `mom_pct` | Month-on-month percent change (quarter-on-quarter for quarterly series), same rules as `yoy_pct`. Empty if not available. |
| 11 | `source_publisher` | The publishing body, in English. |
| 12 | `source_title` | The release title, in English. |
| 13 | `source_date` | Publication date, YYYY-MM-DD. |
| 14 | `notes` | Revisions, computations, approximations, and any other qualification of the row. Empty if none. |

Formatting rules for the CSV:

- Plain UTF-8 text, comma-separated, header row first, one row per line.
- Numeric values without thousands separators and without currency symbols: `4243.3`, not `4,243.3`.
- Negative values carry a leading minus sign: `-1.7`.
- No percent signs in numeric fields; the unit and the column name carry that meaning.

## 2. Indicator identity and naming

### indicator_id

Lowercase, underscore-separated, in the form `<geography_code>_<concept>_<qualifier>`:

- `cn_industrial_value_added_yoy` is not used; the change type lives in the columns, not the ID. Prefer `cn_value_added_industry`.
- Geography codes: ISO-style two-letter codes (`cn`, `us`, `de`, `jp`).
- The ID identifies the indicator's level concept. Its changes live in `yoy_pct` and `mom_pct` on the same row.

Examples drawn from real releases of the National Bureau of Statistics of China:

| indicator_id | indicator_name |
| --- | --- |
| `cn_value_added_industry` | Value Added of Industry |
| `cn_value_added_manufacturing` | Value Added of Manufacturing |
| `cn_value_added_mining` | Value Added of Mining |
| `cn_cpi` | Consumer Price Index |
| `cn_cpi_food` | Consumer Price Index, Food |
| `cn_cpi_pork` | Consumer Price Index, Pork |
| `cn_retail_sales_consumer_goods` | Total Retail Sales of Consumer Goods |
| `cn_retail_sales_consumer_goods_ex_autos` | Retail Sales of Consumer Goods Excluding Automobiles |
| `cn_online_retail_sales` | Online Retail Sales of Goods and Services |

### indicator_name

- Title Case, concept first, then qualifiers separated by commas, most specific last: "Consumer Price Index, Food, Tobacco, Liquor and Dining Out".
- Where a name is used in prose to discuss a change, append the change type in prose contexts only: "Value Added of Industry, YoY" refers to the `yoy_pct` of the row named "Value Added of Industry". The stored `indicator_name` does not carry the change type; the columns do.
- Names come from the official English edition of the release where one exists. Otherwise translate literally and record the choice in the audit file.
- The same concept always gets the same name, in every release, forever. If a source renames a concept, keep the canonical name and note the source's wording in `notes`.

## 3. Categories

Assign exactly one category per row, from this fixed list:

| Category | Covers |
| --- | --- |
| National Accounts | GDP, value added by broad sector, income aggregates. |
| Prices | Consumer and producer price indexes and their components. |
| Industry | Industrial production, value added by industry, output of industrial products. |
| Trade | Exports, imports, trade balances, trade by partner or commodity. |
| Investment | Fixed asset investment, real estate investment, infrastructure investment. |
| Consumption | Retail sales, catering income, online retail, consumer spending measures. |
| Energy | Energy production and consumption, electricity generation, power capacity. |
| Employment | Employment, unemployment, wages, labor market surveys. |
| Finance | Money supply, credit, interest rates, government revenue and expenditure, financial institution aggregates. |

If an indicator genuinely fits none of these, flag it in the report's FLAGS section and use the closest category. Do not invent new categories inside a product; schema changes happen in this document, deliberately.

## 4. Periods

- Single month: `2026-09`.
- Single quarter: `2026-Q3`.
- Single year: `2026`.
- Cumulative span: `2026-01/2026-09` (used, for example, for January to September year-to-date figures).
- A cumulative figure and a single-period figure are always separate rows. A release that reports both September and January-to-September values produces both rows.

## 5. Values, units, and changes

Units are spelled out in full. Standard forms include:

- `Percent` for a growth or change rate stored in `yoy_pct` or `mom_pct` context, and for rates published as levels (for example, an unemployment rate).
- `Percentage Points` for a difference between two rates, and for a stated contribution to a change. This is a distinct unit from `Percent` and the two are never interchanged. A release statement such as "0.3 percentage points higher than the previous month" produces a contribution or difference figure in `Percentage Points`, never a percent change.
- `CNY Billion`, `USD Billion`, and spelled-out currency forms generally, for monetary levels in the source's stated magnitude. Do not rescale billions to millions silently; if the schema ever requires rescaling, the audit file must show it.
- Physical units spelled out: `Million Tonnes`, `Billion Kilowatt-Hours`, `Million Units`, `Million Persons`.
- Index values: `Index, Same Period Last Year = 100` (so a CPI of 100.9), or `Index, Previous Period = 100` where the source uses that base. State the base in the unit, always.
- Magnitudes are the source's own. If the source publishes in ten-thousands or hundred-millions, store those exact digits and spell the unit to match (`Ten Thousand Tonnes`, `CNY Hundred Million`). Never rescale digits to a different magnitude: digit-for-digit fidelity to the source outranks unit elegance, and rescaling is a presentation choice for whoever consumes the product, never part of the product itself.
- Contribution rows: the change basis lives in the `indicator_id` suffix. A component's contribution to a year-on-year change uses `_contribution_yoy`; its contribution to a month-on-month change uses `_contribution_mom`. The same component may therefore hold both, as separate rows, without collision.

Rules for `value`, `yoy_pct`, and `mom_pct`:

- Record each exactly as published, digit for digit.
- A row may carry a level and both changes (a retail sales row with its level and its year-on-year change), or a level only, or changes only. Where the source publishes only a growth rate for a breakdown (common for industry detail in prose), the row carries that change with `value` and `unit` left empty, and the audit file quotes the prose.
- A change may be computed only from levels that both appear in the same source. Computed changes are marked "Computed from published levels" in `notes`.
- Hedged figures in the source ("about 0.26 percentage points") are recorded as published and marked "Approximate, as published" in `notes`.

## 6. The report: `report.md`

One page, in this layout:

1. **Title and identification block.** Release title, publisher, publication date, geography, reference period, and a link or citation to the source.
2. **Headline indicators.** A table of the release's headline rows: indicator name, period, value, unit, YoY, MoM. Headline means the figures the release itself leads with.
3. **Category sections.** One short section per category present in the product, each with a compact table of that category's rows and at most two sentences of prose, drawn only from the release.
4. **FLAGS.** Every ambiguity, gap, inconsistency, and uncertainty found during conversion, each tied to the affected indicator. If there are none, the section states "None."
5. **Methodology and source note.** How the product was produced (per `CLAUDE.md`), the source's own methodological notes where the release states them (for example, that industrial growth rates are real rates after deducting price factors), the original-language title if the source was translated, and the date the conversion was performed.

## 7. The audit trail: `audit.md`

One Markdown table with one row per row of `data.csv`, columns:

| Column | Content |
| --- | --- |
| `indicator_id` | Matches the data row. |
| `period` | Matches the data row. |
| `value_summary` | The value, YoY, and MoM carried on the data row, restated compactly. |
| `source_location` | Where the figure appears in the source: a short verbatim quote of the passage, or the source table's title plus the row label. |
| `confidence_flag` | "Confirmed" for a clean extraction, or the flag text for anything approximate, computed, translated without an official equivalent, revised, or otherwise qualified. |

The audit file is the product's defense. A reader with the audit file in one hand and the source release in the other should be able to verify every number in `data.csv` without searching.

## 8. Worked example (illustrative)

From the National Bureau of Statistics of China release "Industrial Production Operation in September 2026" (published 2026-10-20), the opening paragraph states that the total value added of industrial enterprises above the designated size rose 5.5 percent year on year and 0.61 percent month on month in September, with mining up 1.3 percent, manufacturing up 6.0 percent, and utilities up 5.6 percent year on year. Standardized rows (levels not published for these, so `value` is empty):

```csv
indicator_id,indicator_name,category,geography,period,frequency,value,unit,yoy_pct,mom_pct,source_publisher,source_title,source_date,notes
cn_value_added_industry,Value Added of Industry,Industry,China,2026-09,Monthly,,,5.5,0.61,National Bureau of Statistics of China,Industrial Production Operation in September 2026,2026-10-20,Enterprises above designated size; real growth rate after deducting price factors
cn_value_added_mining,Value Added of Mining,Industry,China,2026-09,Monthly,,,1.3,,National Bureau of Statistics of China,Industrial Production Operation in September 2026,2026-10-20,Enterprises above designated size
cn_value_added_manufacturing,Value Added of Manufacturing,Industry,China,2026-09,Monthly,,,6.0,,National Bureau of Statistics of China,Industrial Production Operation in September 2026,2026-10-20,Enterprises above designated size
```

And from "Total Retail Sales of Consumer Goods from January to September 2026" (published 2026-10-20), where levels are published:

```csv
indicator_id,indicator_name,category,geography,period,frequency,value,unit,yoy_pct,mom_pct,source_publisher,source_title,source_date,notes
cn_retail_sales_consumer_goods,Total Retail Sales of Consumer Goods,Consumption,China,2026-09,Monthly,4243.3,CNY Billion,1.1,,National Bureau of Statistics of China,Total Retail Sales of Consumer Goods from January to September 2026,2026-10-20,
cn_retail_sales_consumer_goods,Total Retail Sales of Consumer Goods,Consumption,China,2026-01/2026-09,Monthly,37000.1,CNY Billion,1.1,,National Bureau of Statistics of China,Total Retail Sales of Consumer Goods from January to September 2026,2026-10-20,Cumulative
```
