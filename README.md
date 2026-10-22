# Indicator Foundry

A free, public toolkit that turns official government statistics releases into standardized data products, using Claude (Claude Code or claude.ai) as the working agent.

The data behind premium economic databases is public. What subscribers have historically paid for is the labor of standardizing it: reading messy official releases, translating them, normalizing names and units, and arranging the figures into clean, comparable series. Indicator Foundry gives that capability away. It contains a data product schema, a set of agent instructions, and a verification protocol that together let anyone with a Claude subscription generate the same class of data products, from the same public sources, on demand.

## What this is

Indicator Foundry is a working method, packaged as a repository:

- A **schema** that defines exactly what a standardized data product looks like: the columns, the naming conventions, the unit conventions, and the layouts for the accompanying report and audit files.
- An **agent instruction file** (`CLAUDE.md`) that tells Claude how to convert one official release into one standards-compliant product, step by step.
- A **verification protocol** that requires every generated value to be mapped back to its exact location in the source release, with uncertainties flagged rather than smoothed over.
- A **validator script** that mechanically checks a finished product against the schema before anyone relies on it.

You supply a government statistics release. Claude does the standardization work that analyst teams have traditionally done by hand. You review the audit trail, run the validator, and use the product.

## Why it exists

Consider how a premium data company such as CEIC operates. Governments publish statistics for free, but they publish them the way governments do: as press releases, PDFs, spreadsheets, and web pages, in local languages, with local naming conventions, inconsistent units, and figures scattered across prose and tables. CEIC and its peers employ analyst teams to collect those releases, translate them, standardize them, and maintain them as clean time series. They then sell subscriptions to universities, banks, and research institutions, often at prices only institutions can pay.

The moat around that business was never the data. The data is public. The moat was the cost of the human standardization labor required to make the data usable, repeated across thousands of releases, month after month.

That cost structure has collapsed. A general-purpose AI agent, given a precise schema and a strict verification protocol, can perform the standardization step for a single release at negligible marginal cost. What remains valuable is judgment: defining the standard, verifying the output, and deciding what to build. This repository packages that judgment so it can be reused by anyone.

The point of the project is the demonstration itself: a business built on charging for access to repackaged public information is vulnerable to anyone who gives the repackaging capability away.

## Philosophy

This project is released publicly and free of charge, on purpose.

The belief behind it is simple: the most effective way to demonstrate what a tool makes possible is to hand people the working tool. Restricting access would prove little. Giving the solution away lets anyone run it on the releases they care about, see the quality for themselves, find its limits, improve it, and take it further than its authors imagined. Capability spreads faster than catalogs. A proprietary database is an inventory; a public method is a multiplier.

If you use this repository to build something larger, a teaching resource, a research pipeline, a public data commons for your country or your field, that is the intended outcome.

## What is inside

| Path | Contents |
| --- | --- |
| `README.md` | This file: the thesis, the method, and how to use the repo. |
| `CLAUDE.md` | The agent instructions. The heart of the repo. Load this into Claude before any conversion work. |
| `METHOD.md` | A fuller description of the method and the verification protocol, written for readers evaluating the project. |
| `COMPARISON.md` | The measured control test: the same release converted with this repo and by plain Claude with a casual request, compared on structure, provenance, coverage, and auditability. |
| `COST.md` | The cost ledger: what a data subscription actually pays for, and what changes when the standardization process is a public instruction set. |
| `APPENDIX.md` | What the tests actually taught: eight findings from production testing, including the ones that forced changes to the standard. |
| `CHANGELOG.md` | How the standard has changed, and which test result forced each change. |
| `schema/product_schema.md` | The output standard: CSV columns, naming and unit conventions, and the required report and audit layouts. |
| `schema/series_registry.csv` | The governed registry of series identities. Runs must reuse registered indicator IDs and names exactly; new series are appended here. |
| `scripts/validate_product.py` | A dependency-free Python validator that checks a finished product against the schema. |
| `scripts/export_wide.py` | Renders any product folder into the wide series workbook layout (series index plus period-by-series matrices) that data vendors deliver. |
| `inputs/` | Place source releases here (HTML, PDF, or text) before a conversion run. |
| `outputs/` | Five verified example products: China industrial production (September 2026, from both the English and Chinese editions, and August 2026), China CPI (September 2026), and US CPI from the Bureau of Labor Statistics (September 2026, 3,411 rows). |

## How to use it

You need a Claude subscription (Claude Code or claude.ai). No API key is required; the method is designed for the Claude products people already have.

1. **Clone this repository** and open the folder.
2. **Load the instructions.**
   - With Claude Code: open the folder in Claude Code. It reads `CLAUDE.md` automatically. You can start working.
   - With claude.ai: start a new conversation, upload `CLAUDE.md` and `schema/product_schema.md`, and tell Claude to follow them as its instructions for the session.
3. **Place a source release in `inputs/`.** Save an official statistics release as HTML, PDF, or plain text. Official sources only: national statistics offices, central banks, ministries, and other government publishers. Alternatively, give Claude the URL of the official release.
4. **Ask Claude to generate the product.** A typical request: "Convert the release in inputs/ into a data product following CLAUDE.md and the schema." Claude will identify the release, extract and standardize every quantitative indicator, and write the product to `outputs/<release-slug>/`: a tidy `data.csv`, a one-page `report.md`, and an `audit.md` mapping every value to its source location.
5. **Run the validator.** From the repo root: `python3 scripts/validate_product.py outputs/<release-slug>`. It checks the schema, the numbers, and the audit coverage, and prints a pass or fail summary.
6. **Review the audit trail and the flags.** Read `audit.md` for provenance and read the FLAGS section of `report.md` for anything Claude marked as ambiguous, missing, or uncertain. The flags are part of the product. Treat flagged values accordingly.

## The output standard

Every product follows [schema/product_schema.md](schema/product_schema.md). In brief: one CSV row per indicator per period, canonical English indicator names, explicit units on every value, year-on-year and month-on-month changes recorded where the source publishes them or where they can be computed from published levels, and full source attribution on every row. The standard is deliberately strict. Consistency across releases is what makes the products comparable, and comparability is the entire value of a data product.

## Verification and trust

A generated dataset is only worth using if every number in it can be defended. The verification protocol in this repo is built around three rules:

- **Every value is mapped to its source.** The audit file records, for each output value, exactly where it appears in the source release: a quoted passage or a table and row reference.
- **Uncertainties are flagged, never invented around.** If a figure is ambiguous, illegible, or absent, the product says so in its FLAGS section. A flagged gap is honest; a plausible-looking guess is a defect.
- **Nothing appears in the output that is not in the source.** If a figure is not in the release, it does not appear in the product. There are no exceptions for figures that "should" be there.

AI standardization can misread a table or confuse a unit. The protocol assumes this and is designed to catch it: the audit trail makes errors findable, and the validator makes structural errors mechanical to detect. Read `METHOD.md` for the protocol in full, including the known failure modes and how each is addressed.

## Scope and limits

- The method works on **machine-readable releases**: HTML, text-based PDF, spreadsheets, and structured web pages. Scanned images of tables require OCR first and carry higher error risk; treat such products with extra care.
- The repo replicates **a class of data products, series by series, on demand**. It does not mirror any company's proprietary database, and it does not need to: the point is that any given product can be regenerated from its public source when it is needed.
- The schema currently defines conventions suited to macroeconomic and sector statistics of the kind national statistics offices publish monthly. Extending it to other domains means extending the schema, which the format is designed to allow.
- Generated products are only as reliable as the review you give them. The verification protocol makes review fast and specific; it does not eliminate the need for it.

## License

The code, instructions, and documentation in this repository are released under the MIT License. Use them, adapt them, and build on them freely, including commercially.

The data in the source releases, and in products generated from them, is public government data published by the respective statistics authorities. This project claims no rights over it, which is rather the point.
