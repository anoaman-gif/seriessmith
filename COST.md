# The cost ledger, and what the money actually buys

The obvious version of this argument ("AI is cheap, analysts are expensive") is not worth much. The sourced version is more interesting, because it shows what a data subscription actually pays for, line by line.

## Nobody pays for the data

Every figure CEIC sells originates in a public release that anyone can download free. The National Bureau of Statistics charges nothing. So a subscription has never bought data. It buys two kinds of labor:

1. **First-pass standardization.** Turning each messy release into stable series: consistent names, categories, units, and one delivery format, sense-checked before publication (CEIC's own description of its process).
2. **Perpetual maintenance.** Governments revise. Figures get restated, classifications change, series get rebased, sources change their formats. A data vendor's staff re-standardizes the past continuously so a series means the same thing across decades. This layer is valuable enough to sell separately: CEIC's Point-in-Time product, launched in 2025, is literally a subscription to maintained revision history, marketed as "over 10 years of meticulously maintained revised historical data."

The $180 million that Caixin Global and Citic Capital agreed to pay for CEIC and EMIS in 2018 was the price of that accumulated labor and the back catalog it produced: millions of series (CEIC currently markets more than 3 million, from more than 3,500 sources), already standardized, already maintained.

## What the repo changes, precisely

- First-pass standardization: a generation under this repo's instructions costs nothing beyond a consumer Claude subscription the user already holds. Every product in this repo's test suite was produced that way. Itemized additional spend: $0.
- Maintenance: re-running the standard on a restated or revised release costs the same as the first run, and the standard treats revisions as first-class data rather than an embarrassment. In the September 2026 industrial production test, the release republished a year of revised month-on-month rates; the product captured all twelve as rows marked revised, automatically. The thing CEIC sells as a premium tier fell out of the process as a byproduct.
- What the repo does not conjure: the back catalog. Decades of already-standardized history, and the institutional trust attached to it, took decades and real money. This project reproduces the process, not the archive. Anyone claiming otherwise is overselling, and the honest scope makes the claim stronger, not weaker.

## The asymmetry in one line

The incumbent's costs recur forever, because the maintenance never ends. The repo's cost was writing the standard once. After that, both first production and maintenance run at the marginal cost of a generation, which is effectively zero.
