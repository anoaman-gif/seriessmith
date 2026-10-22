# The Method

This document describes how SeriesSmith turns a government statistics release into a standardized data product, how the verification protocol works, and where the method can fail. It is written for a reader evaluating the project: a reviewer, a collaborator, or a skeptic. The claims here are deliberately plain. The method's credibility is the project.

## 1. From release to product

A government statistics release is a document written for journalists and officials, not for analysis. A typical monthly release from a national statistics office mixes prose and tables, leads with headline growth rates, buries breakdowns in paragraphs, states some figures as levels and others only as changes, and hedges some numbers with words like "about". A data product is the opposite: one row per indicator per period, every value carrying a unit, every name consistent with every other release, every figure traceable to its source.

The conversion has five steps:

1. **Identification.** The release is identified and its metadata fixed: publisher, title, publication date, geography, reference period. These become the attribution columns carried on every row of the product.
2. **Extraction.** Every quantitative indicator in the release is extracted: headline levels, published growth rates, breakdowns by sector, industry, region, area, ownership, product, and category, including figures stated only in prose.
3. **Standardization.** Each indicator is re-expressed in the schema (`schema/product_schema.md`): a canonical English name, a fixed category, an explicit spelled-out unit, a normalized period, and year-on-year and month-on-month changes recorded where published or computable from published levels. This is the step premium data companies perform with analyst teams, and the step the agent performs here.
4. **Audit generation.** Alongside the dataset, an audit file is produced that maps every output value to its exact location in the source release, as a verbatim quote or a table and row reference.
5. **Validation and review.** A script (`scripts/validate_product.py`) mechanically checks the product against the schema, and a human reviews the audit trail and the flags before the product is used.

The deliverable of one conversion is a folder containing `data.csv`, `report.md`, and `audit.md`. The three files are one product: the data, the summary, and the defense.

## 2. The verification protocol

The protocol rests on a single principle: **a generated value is a claim, and every claim needs a citation.**

- **Traceability.** Every row of `data.csv` has a matching row in `audit.md`, and every audit row names the source location of its figures. The validator enforces the match mechanically; a product with an untraced row fails validation.
- **Exactness.** Values must match the source digit for digit. The workflow requires a dedicated re-read of the source, hunting only for numbers, to catch omissions and transcription slips before completion.
- **No invention.** A figure absent from the source may not appear in the product, however plausible. Interpolation, estimation, seasonal adjustment, and annualization are prohibited operations, not discouraged ones.
- **Flagging over guessing.** Ambiguity is recorded, not resolved silently. Hedged source figures are marked approximate, as published. Prose and table disagreements are flagged with both values shown. Unclear units are flagged rather than assumed. The FLAGS section of the report collects all of this in one place, so a reader can see the product's weaknesses at a glance.
- **Computation discipline.** A change may be computed only when both underlying levels are present in the same source, and computed values are labeled as computed. This keeps the line between published fact and derived figure visible at all times.
- **Revision honesty.** Figures the source marks as revised or preliminary are labeled as such. The protocol treats silently overwriting a prior figure as a defect, because time series are used precisely to compare what was known at different times.

The protocol cannot make an error impossible. It makes errors findable: any reviewer can take the audit file and the source and check any value in moments, and can see exactly which values the converter itself was unsure about.

## 3. Failure modes, honestly stated

**Misread tables.** Dense statistical tables, especially multi-level headers and cumulative-versus-monthly column pairs, can be misaligned during extraction, attaching a value to the wrong indicator or period.
*Mitigation:* the audit row for a table value must name the table and the row label, so a misalignment is visible on review; the re-read step specifically compares table totals and subtotals against the prose, which usually leads with the same figures.

**Unit confusion.** The most dangerous failure in economic data work is a quiet one: a percent recorded where percentage points were meant, a figure in billions treated as millions, a cumulative total read as a single month.
*Mitigation:* units are mandatory, spelled out, and part of the schema rather than a formatting choice; percent and percentage points are distinct units by rule; cumulative and single periods have distinct period formats and can never share a row; conversions are prohibited unless the schema requires them, and then must be shown in the audit file.

**Translation drift.** Statistical terminology is technical, and a careless translation can create a phantom indicator or merge two distinct ones (for example, distinct Chinese terms for industry groupings that both translate loosely as "manufacturing").
*Mitigation:* canonical names are defined once and reused; the official English edition of a release, where one exists, is the terminology authority; where no official equivalent exists, the translation is literal and the choice is flagged in the audit file so a bilingual reviewer can correct it in one place.

**Revision handling.** Statistical offices revise. A series built by stacking monthly products can silently mix original and revised figures, and a converter working from a reposted release may never notice.
*Mitigation:* source-identified revisions and preliminary figures are labeled in the row notes and the audit file; every row carries its source date, so mixed vintages are visible rather than hidden.

**Prose-only figures.** Breakdowns published only in narrative text are easy to miss entirely, which biases a product toward headline numbers.
*Mitigation:* the workflow's extraction standard is completeness, with the number-hunting re-read as a separate pass; the audit file's quotes make the prose basis of each such figure explicit.

**Overconfidence.** A fluent agent produces fluent output, and fluency invites trust the numbers may not deserve.
*Mitigation:* the FLAGS section is a required part of every product, the validator fails products with untraced values, and this document exists so that evaluators know exactly what to distrust and how to check it.

## 4. What the method does not do

It does not guarantee correctness; it guarantees traceability, which is the precondition for correctness being checkable. It does not replace a statistics office's own databases for high-volume programmatic access. It does not mirror any proprietary database, and it does not need to: its claim is narrower and stronger, that the standardization step between a public release and a usable product, the step an industry charges institutions to perform, can now be performed by an agent under a strict protocol, at negligible marginal cost, by anyone.
