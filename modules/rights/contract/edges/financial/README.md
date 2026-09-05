# Financial

## Model

- `(contract)-[:financial_by]->(transaction)`
- `(transaction)-[:reference]->(contract)`

## Policies (rules)

- A settlement reference may be used by companies like Adyen to automatically generate and track settlement details reports.
- When a financial transaction is settled or a report is generated, a unique reference number is often used for tracking and reconciliation.
