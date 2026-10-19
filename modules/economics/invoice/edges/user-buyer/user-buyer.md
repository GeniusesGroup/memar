# User buyer

## Model

- `(invoice)-[:buyer_is]->(user)` (note: product)
- `(user)-[:buyer_for]->(invoice)`

## Policies (rules)

- someone whose job is to choose and buy the goods for a shop or company

## Open questions

- When the buyer is another organization, is this invoice inserted automatically in the buyer's organization too — one invoice both organizations see, or a counterpart in each — and may the buyer book it before the seller accepts? — [invoice exchange](../../invoice.handoff.md#open-questions).
