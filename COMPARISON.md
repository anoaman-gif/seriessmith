# With the repo vs. without it: measured results

The differentiation claim of this project is testable, so it was tested. Same model (Claude, Pro account), same input file (the National Bureau of Statistics release "Industrial Production Operation in September 2026"), two conditions:

- **Repo condition:** the release plus this repo's `CLAUDE.md` and `schema/product_schema.md`, with the instruction to follow them.
- **Control condition:** the release alone, plus one casual sentence: "Hi, can you turn this government statistics release into a clean dataset for me? A CSV I can actually use would be great. Thanks!" The control was run twice, in two fresh chats.

Every output was then checked independently: each number screened against the source text, structure compared, and the repo outputs run through `scripts/validate_product.py`.

## Results

| Dimension | Repo condition | Control (run 1) | Control (run 2) |
|---|---|---|---|
| Files produced | 3 (data.csv, report.md, audit.md) | 2 CSVs | 2 CSVs |
| Data rows | 151 | 80 | 80 |
| Output structure | The repo schema, 14 fixed columns | Invented: 10 columns | Invented: 9 columns, different from run 1 |
| Column names | Fixed by the standard | Hard-code this release (`sep_2026_value`, `jan_sep_2026_value`) | Same hard-coding, different column set |
| Section vocabulary | Fixed categories from the standard | "Value added", "Product output", "Other" | "headline", "by_sector", "by_industry", six labels, none matching run 1 |
| Provenance in the files | Publisher, release title, and date on every row | None | None |
| Audit trail | One audit entry per row, with a verbatim source quote | None | None |
| Validator | PASS (151 of 151 rows conform and are audited) | Cannot be run: no standard to validate against | Cannot be run |
| Uncertainties flagged | 14 flags (unit magnitudes, partial coverage, a source arithmetic discrepancy, revision handling, and more) | None | None |
| Fabricated values | 0 (every value traces to the source) | 0 | 0 |
| Headline figure | 5.5% YoY, correct | 5.5% YoY, correct | 5.5% YoY, correct |

## What this does and does not show

Plain Claude is accurate. In both control runs it invented nothing, and its headline figures were right. Anyone claiming a bare chatbot hallucinates its way through a task like this would be wrong on this evidence, and this project does not claim it.

What a bare chatbot does not do is hold a standard. Two identical requests produced two different schemas that cannot be merged without manual rework; both hard-code one release into their column names, so next month's output cannot extend this month's; neither carries provenance, an audit trail, or a single flag; and neither result can be checked by anything except reading it and hoping. One control run's first build attempt failed and was silently retried; the user was never told.

The repo condition produced the same structure the standard specifies, complete coverage of the release (151 rows against 80, including the percentage point changes, the count rows, and the revised history as data), provenance on every row, an audit entry for every value, and a validator verdict that does not depend on anyone's impression.

And the standard holds across runs and languages, with one honest qualification that testing exposed and the standard now fixes. The same release converted independently from its Chinese edition produced exactly 151 rows, and on every indicator-and-period key where the two runs used the same series identity, the growth rates were identical (78 of 78, zero differences). But the continuity test on the prior month's release showed that long-tail series IDs drifted between runs: the same concept could receive a variant ID, because v1.0 governed values and structure more tightly than identity. That is a real flaw, of exactly the kind a data vendor's series governance exists to prevent. Version 1.2 fixes it with a governed series registry (`schema/series_registry.csv`): canonical IDs and names that every run must reuse, with the pre-registry variants recorded rather than hidden. The corrected statement is the stronger one: the values and the structure never wavered, and the one dimension that did, identity, is now the most tightly governed part of the standard.

That is the whole argument. The model is a commodity. Accuracy is close to free. What the incumbent sells, and what this repo encodes, is the discipline that makes output accumulate into a database instead of expiring as a document: one structure, provenance, an audit, and a check, repeated identically by anyone.
