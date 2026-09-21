# Price settlement

## Model

- `(pos)-[:price_settlement_is]->(account)`
- `(account)-[:price_settlement_of]->(pos)`

## Policies (rules)

- CAN set share percent to divide price to multiple account
- Priority order to prefer:: Batch >> Product >> POS >> Organization
