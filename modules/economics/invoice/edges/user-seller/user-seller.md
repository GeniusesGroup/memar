# User seller

## Model

- `(invoice)-[:seller_is]->(user)` (note: product)
- `(user)-[:seller_of]->(invoice)`

## Open questions

- When the seller is another organization, which organization registers this invoice, and does it reach the seller's organization automatically, as a purchase request the seller may reject by hand or by rule, for example on a price difference? — [invoice exchange](../../invoice.handoff.md#open-questions).
