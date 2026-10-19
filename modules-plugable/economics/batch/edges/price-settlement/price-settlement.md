# Price settlement

## Model

- `(batch)-[:price_settlement_is]->(account)`
- `(account)-[:price_settlement_of]->(batch)`

## Policies (rules)

- CAN set share percent to divide price to multiple account
- Priority order to prefer:: Batch >> Product >> POS >> Organization

## Open questions

- [Pricing Research 001](../../../pricing/pricing.research.001.md#recommendation-unratified) reads this priority as the precedent for resolving a stated sale price most-specific-first if a price moves to the batch (the owner's leaning, open in [pricing](../../../pricing/edges/pricing/pricing.md#open-questions)). Is one priority order shared by where a price settles and where it is stated, or are they two orders that happen to agree?

