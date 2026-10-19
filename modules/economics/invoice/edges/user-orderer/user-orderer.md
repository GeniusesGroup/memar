# User orderer

## Model

- `(invoice)-[:orderer_is]->(user)` (note: product)
- `(user)-[:orderer_of]->(invoice)`

## Policies (rules)

- Orderer is creator of the invoice e.g. restaurant waiter, doctor drug prescription, sales agent,
