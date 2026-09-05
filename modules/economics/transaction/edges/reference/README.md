# Transaction reference
Transaction reference or `is_financial_settlement_for` use in relation to any domain to track for any purpose like invoice payment, ...

## Model

- `(transaction)-[:transaction_reference_is]->(thing)`
- `(thing)-[:financial_transaction_is]->(transaction)`

## Policies (rules)

- domains like `Budget`, `Contract`, `Order`, ...
- `batch` for `Invoice` for `product_inventory` purpose
- CAN relate multiple transactions for the same reference.
- It can't be changed after registered for any reason. The transaction MUST get `ReadOnly` label.
- Referencing MUST be automatic process.

## Fields
