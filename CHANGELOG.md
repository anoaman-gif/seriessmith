# Changelog

## v1.2 (identity governance, from the continuity test)

The prior-month (August 2026) continuity run exposed the standard's real weakness. Values were exact and structure held, but series identity drifted: converting the same release family in different runs produced variant indicator IDs for the same concepts (25 series names carried differing IDs across the three industrial production products; for example the percentage point change row appeared under three different IDs). The values were never wrong; the names for the series were not yet governed tightly enough, and ungoverned identity is exactly how a catalog quietly stops being a database.

Fixes:
1. **`schema/series_registry.csv`** now governs identity: 71 canonical series seeded from the September 2026 English product, with the variant IDs observed in earlier runs recorded per series so nothing is lost. CLAUDE.md Step 3 requires registry lookup before any ID is assigned, and hard rule 9 makes inventing a variant ID for a known series an error on par with inventing a value.
2. The headline percentage point change ID is normalized to `cn_value_added_industry_yoy_rate_change` in every published product, and the August product's count units are normalized to the standard forms (`Number of Industries`, `Number of Products`). Values were not touched; all products re-validated after normalization.
3. The comparison evidence in `COMPARISON.md` is corrected to state the convergence result precisely: values matched on every comparable key, while long-tail IDs drifted before the registry. The correction is kept visible rather than edited away, because a standard's changelog is part of its credibility.
4. The validator gained two checks from the same findings: duplicate series keys (indicator_id, geography, period) are now a hard failure, and IDs missing from the registry surface as a visible warning. The China CPI family (55 series) is absorbed into the registry. The US BLS product's 2,284 series are catalogued in its own audit file and are the registry's next absorption task; the validator reports them as unregistered rather than pretending otherwise.

## v1.1 (from production testing)

Three decisions that test runs surfaced as recurring flags are now settled in the standard itself. The test products were generated under v1.0; every v1.1 rule below codifies behavior the agent already exhibited, so the published test products conform to v1.1 unchanged.

1. **Magnitudes are the source's own** (schema Section 5). All three full test runs kept source magnitudes (ten-thousand and hundred-million units) and flagged the absence of a rule. The standard now states it: store the source's digits, spell the unit to match, never rescale.
2. **Contribution naming** (schema Section 5). The CPI run needed one component to hold both a year-on-year and a month-on-month contribution. The standard now places the change basis in the indicator_id suffix (_contribution_yoy, _contribution_mom).
3. **The source outranks the examples** (CLAUDE.md hard rule 8). The Chinese-edition run found the schema's worked example cited the English edition's title and date, which differ from the Chinese edition in front of it. The agent followed the source and flagged the conflict; that behavior is now a written rule.

Also added: `scripts/export_wide.py`, which renders any product folder into the wide series workbook layout (series index plus period-by-series matrices) that data vendors deliver to customers, and `COMPARISON.md`, the measured control-test results.
