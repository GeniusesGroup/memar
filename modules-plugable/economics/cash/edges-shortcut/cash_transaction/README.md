# Cash Transaction

## Model

- `[transaction-[:cash_transaction]->(___)`
- `(transaction)-[:book_in]->(account)-[:cash_account]->(___)`

## Policies (rules)

- One account MUST have `cash_account` label

## Fields
