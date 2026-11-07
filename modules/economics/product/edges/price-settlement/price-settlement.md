# Price settlement

## Model

- `(product)-[:price_settlement_is]->(account)`
- `(account)-[:price_settlement_of]->(product)`

## Policies (rules)

- CAN set share percent to divide price to multiple account
- Priority order to prefer:: Batch >> Product >> POS >> Organization
