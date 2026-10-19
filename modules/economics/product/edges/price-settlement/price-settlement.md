# Price settlement

## Model

- `(product)-[:price_settlement_is]->(account)`
- `(account)-[:price_settlement_of]->(product)`

## Policies (rules)

- CAN set share percent to divide price to multiple account
- Priority order to prefer:: Batch >> Product >> POS >> Organization

## Open questions

- This priority already prefers the batch to the product; if a price moves to the batch, as the owner leans, is the settlement account always read from the same node the price was read from? — [Pricing Research 001](../../../../../modules-plugable/economics/pricing/pricing.research.001.md#open-questions).
