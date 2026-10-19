# Refund

## Model

- `(invoice)-[:refund]->(rule)`

## Open questions

- An invoice item holds the price it was issued at as its own fact ([pricing → Open questions](../pricing/edges/pricing/pricing.md#open-questions)). Does a refund repay that issued price, or does a refund rule account for the replacement cost having moved since issue ([replacement cost](../replacement-cost/replacement-cost.md)), and which party bears the price movement between issue and return?
