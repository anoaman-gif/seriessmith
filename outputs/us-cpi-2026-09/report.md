# Consumer Price Index – September 2026

| | |
| --- | --- |
| Publisher | U.S. Bureau of Labor Statistics (release USDL-26-1574) |
| Publication date | 2026-10-14 (embargoed until 8:30 a.m. ET) |
| Geography | United States (U.S. city average), plus Census regions, size classes and 23 local areas (Table 4) |
| Reference period | September 2026; 1-month changes for July, August and September 2026; 12-month changes to September 2026; history of all-items changes December 2013 to September 2026 (Table 5) |
| Source | www.bls.gov/cpi; source file `bls_cpi_sep2026.txt` |
| Product | `data.csv` (3,411 rows, 2,284 indicators), `audit.md` (3,411 rows) |

## Headline indicators

| Indicator | Period | Value | Unit | YoY | MoM |
| --- | --- | --- | --- | --- | --- |
| CPI-U, All Items | 2026-09 | 336.940 | Index, 1982-84 = 100 | 3.7 | 0.6 |
| CPI-U, All Items, Seasonally Adjusted | 2026-09 | | | | 0.6 |
| CPI-U, All Items Less Food and Energy | 2026-09 | 339.287 | Index, 1982-84 = 100 | 2.6 | 0.4 |
| CPI-U, All Items Less Food and Energy, Seasonally Adjusted | 2026-09 | | | | 0.3 |
| CPI-U, Energy, Seasonally Adjusted | 2026-09 | | | | 5.2 |
| CPI-U, Gasoline (All Types), Seasonally Adjusted | 2026-09 | | | | 9.1 |
| CPI-U, Shelter, Seasonally Adjusted | 2026-09 | | | | 0.4 |
| CPI-U, Food, Seasonally Adjusted | 2026-09 | | | | 0.0 |
| CPI-W, All Items | 2026-09 | 330.654 | Index, 1982-84 = 100 | 3.9 | 0.7 |
| C-CPI-U, All Items (preliminary) | 2026-09 | | | 3.5 | 0.5 |

YoY is unadjusted. MoM on unadjusted rows is the unadjusted 1-month change; seasonally adjusted rows carry only MoM.

## Prices

| Item (CPI-U) | Index, Sep 2026 | YoY (NSA) | MoM (SA) |
| --- | --- | --- | --- |
| Food | 350.905 | 2.5 | 0.0 |
| Food at home | 321.758 | 1.8 | -0.1 |
| Food away from home (NSA series) | 398.783 | 3.5 | 0.2 (NSA) |
| Energy | 341.573 | 20.4 | 5.2 |
| Gasoline (all types) | 383.182 | 34.2 | 9.1 |
| Electricity | 309.852 | 4.4 | 0.2 |
| Utility (piped) gas service | 264.250 | 5.0 | -0.3 |
| Shelter | 432.092 | 3.2 | 0.4 |
| Owners' equivalent rent of residences (Dec 1982 = 100) | 445.381 | 3.3 | 0.3 |
| Used cars and trucks | 184.395 | -1.5 | 0.7 |
| Airline fares | 315.948 | 22.4 | 1.2 |
| Motor vehicle insurance | 846.102 | -5.0 | 0.1 |

Gasoline rose 9.1 percent seasonally adjusted and, per the release, accounted for over half of the monthly all items increase (its Table 6 effect is 0.337 of the 0.6). Every product row is in the Prices category; the full set covers Tables 1 to 7 and the release text.

## FLAGS

1. **November 2025 availability (us_cpi_u_all_items, us_c_cpi_u_all_items, 2025-11).** The release carries two conflicting notes: "Oct and Nov 2025 data values are not available" and "Oct 2025 data values are not available". Table 5 prints 12-month changes for November 2025 (2.7 CPI-U, 2.7 C-CPI-U) and "–" for the 1-month change. Values recorded as printed; no October 2025 rows exist.
2. **Table A.** The text contains Table A's title and a footnote but no figures. Nothing extracted from it.
3. **Limited service meals (us_cpi_u_limited_service_meals_and_snacks, 2026-09).** Prose says "increased 0.2 over the month" with no unit. Table 2 gives 0.2 percent; table value used.
4. **C-CPI-U revisions (us_c_cpi_u_all_items).** The technical note says C-CPI-U is subject to "three subsequent quarterly revisions"; the Table 5 footnote says "four revisions". The text says "the past 10 to 12 months" are subject to revision. Rows 2025-11 to 2026-09 are marked preliminary.
5. **Effect columns (`*_effect_1m`, `*_effect_12m`, 616 rows).** Tables 6 and 7 do not state a unit. "Percentage Points" follows from footnote 1, which defines the effect as a contribution subtracted from the all items percent change. Table 6 publishes effects for not seasonally adjusted series in its "seasonally adjusted effect" column; noted per row.
6. **Standard error columns (`*_standard_error_*`, 752 rows).** The column is headed "Standard error, median price change", while footnote 2 describes it as the standard error of the percent change, in percent. Recorded in "Percent".
7. **Effect or standard error without a change.** Motor vehicle body work has a Table 6 effect (0.001) and standard error while its 1-month change is "–". Food at elementary and secondary schools and Inpatient hospital services have Table 6 standard errors with no 1-month change.
8. **"Largest or smallest change since" columns (Tables 6 and 7) not extracted.** The release never defines which period the adjacent "Percent change" value belongs to, several rows contradict footnote 3 as printed (Table 6: Household furnishings and supplies, S-Jun.2026 -0.1 against a current -0.2; Other furniture; Outdoor equipment and supplies. Table 7: Other furniture), and the text layer displaces the date cells for Telephone hardware and Smartphones in Table 7. Recording these would mean guessing a period.
9. **Six Table 2 items with no figures** (all columns "–"): Household operations, Domestic services, Repair of household items, Services by other medical professionals, Intracity mass transit, Legal services. No rows produced.
10. **Relative importance (`*_relative_importance`, 309 rows).** No unit in source; labelled "Relative Importance, All Items = 100" because All items is 100.000.
11. **Table 4 areas.** The table does not say whether changes are seasonally adjusted (U.S. figures match the unadjusted series). Pricing-schedule 1 and 2 areas are bimonthly; the schema has no bimonthly frequency, so they are recorded as Monthly with a note. Two-month changes are carried in `value` (unit Percent) under `us_cpi_u_all_items_two_month_change` because the schema has no column for them.
12. **Not seasonally adjusted series.** For the 154 series footnoted "Not seasonally adjusted", July and August 1-month changes come from the table columns labelled seasonally adjusted. For every such series, the September column equals the unadjusted 1-month change, which confirms the reading.
13. **Text-layer reconstruction.** Tables arrive as separated label and value columns. Columns were realigned and checked: Table 1 and Table 3 levels reproduce every published change, Table 1 matches Table 2, and the weights and changes in Tables 6 and 7 match Tables 2 and 3 exactly. One Table 6 page (Video discs through Checking account services) had two valid alignments; the one kept is the only one where effects appear exactly for items with a relative importance, as the footnotes require.
14. **Prose terms.** "Natural gas", "rent", "owners' equivalent rent", "beef" and "full/limited service meals" map to Utility (piped) gas service, Rent of primary residence, Owners' equivalent rent of residences, Beef and veal, and Full/Limited service meals and snacks. All 70 prose figures match the tables.
15. **Footnote marker.** Table 1's footnote 2 marker for Tobacco and smoking products is displaced in the text; read as December 2024 = 100, which matches Table 2.

## Methodology and source note

Produced per `CLAUDE.md`: every table and the release text were read, figures recorded digit for digit, nothing computed, rounded, annualized or seasonally adjusted. Unadjusted and seasonally adjusted series are separate indicators (`_sa` suffix). Per the release, CPI-U and CPI-W use a 1982-84 = 100 reference base unless footnoted, C-CPI-U uses December 1999 = 100, CPI-U and CPI-W are final when released, C-CPI-U is preliminary, and seasonally adjusted data are revised for up to 5 years. Prices are collected in 75 urban areas from about 6,000 housing units and 22,000 retail establishments; these sample counts, and the illustrative Item A/B/C example, are methodology and are not in `data.csv`. The source is in English; no translation was needed. `source_date` comes from the embargo line. Conversion performed 2026-10-21.
