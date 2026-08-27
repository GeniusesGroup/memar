# Cash Transaction


## Graph
- `[transaction-[:cash_transaction]->(___)`
- `(transaction)-[:book_in]->(account)-[:cash_account]->(___)`

## Policy (rule)
- One account MUST have `cash_account` label

## Fields
