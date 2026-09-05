# Transaction account to
`account to` or `gives to` or `transfer to` or `deposit into` or `receiver` indicate which account deposit into from this transaction.

## Model

- `(transaction)-[:account__to]->(account)`

## Policies (rules)

- If this edge exist, `takes` edges MUST not exist in this transaction. In other word it can't be a match logic and get `deal` edge.
- e.g. User want to pay for a service based `invoice`, ...
- e.g. pay by other org (bank) for an `invoice`
- e.g. Move some `good` to other warehouse without any invoice.

## Fields
