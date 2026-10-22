# Appendix: what the tests actually taught

None of the following was the plan. All of it came out of running the standard against real releases and checking the results. It is recorded because a builder's honest findings are worth more than a builder's brochure.

## 1. The standard's own example was wrong

The schema's worked example cited the English edition of the September industrial production release (published October 20). The Chinese edition in front of the agent was published October 19 under a different title. The agent followed the source and flagged the schema. Lesson, now hard rule 8: a standard is a document, documents contain errors, and governance must say explicitly which authority wins. Ours ranks the source above the standard.

## 2. The agent ends up auditing the government

Twice, in two different months, the published components of China's electricity generation summed to one less than the published total (8,293 against 8,294; 9,437 against 9,438). The BLS release contradicted itself about which 2025 months are missing after the appropriations lapse. In every case the products reproduced the official figures exactly and flagged the discrepancy. This is the "sense-check" the incumbent advertises as human craft, made visible and routine. It also reframes the trust question: the risk in official data is not only model error; the sources themselves are imperfect, and a pipeline that silently "fixes" them is worse than one that shows its work.

## 3. Values converge; identities drift

The most consequential finding of the test suite. Across languages and months, every checked value was right, and the output structure never wavered. But series identity, the humble question of what a given series is called, drifted between runs until the standard governed it with a registry. Accuracy turns out to be the easy discipline; identity is the hard one, because nothing in a single run tells you that you have named a series differently from last month's run. Databases die of exactly this. The incumbent's deepest moat is not its analysts' care with numbers. It is seventy thousand governed identities, maintained for decades. Version 1.2 of this repo exists because the continuity test proved the point empirically.

## 4. The discipline matters most when there is least data

China's CPI release publishes no index levels at all, only growth rates and approximate contributions. There is nothing to compute your way out of that absence. The product is 103 rows of rates, each one traced, with the missing levels recorded as missing rather than reconstructed. A standardization process earns its keep precisely at the boundary between what a source says and what it does not.

## 5. Absence is data

The BLS release is missing months because the United States government ran out of funding in late 2025 and the statistics were never collected. The product records that absence, with the source's own contradictory footnotes flagged, instead of interpolating across it. Any analyst who has spliced a series across a gap knows the temptation. The standard forbids it, and the audit shows the gap to every future user.

## 6. The premium tier is a byproduct

CEIC sells revision history separately, as its Point-in-Time product, because tracking what a figure used to say is expensive when humans do it. Both Chinese industrial production runs captured a year of revised month-on-month rates as first-class, marked rows, because the standard says revised figures are marked, always. The premium feature fell out of the discipline for free. When a process is written down, its byproducts compound.

## 7. Completeness is bounded by evidence, and the bound is visible

Given the full release minus its tables, the agent produced 39 rows instead of 151 and said why, in its first flag. The system did not get less capable when the input shrank; it got more honest, measurably. That asymmetry, output size tracking evidence instead of ambition, is the behavior a data business is actually built on, and it only appears because the standard requires a flag where a guess would go.

## 8. The honest limit of the argument

Plain Claude, given the same release and a casual request, fabricated nothing either. Anyone whose pitch is "the chatbot hallucinates" will lose the room to the first prepared question. The measured difference is accumulation: stable form, governed identity, provenance, and a check, repeated by anyone. Which is, not coincidentally, a precise description of what the incumbent has been selling all along.
