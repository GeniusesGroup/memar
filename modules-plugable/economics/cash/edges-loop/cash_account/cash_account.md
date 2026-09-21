# Cash Account
In cash transaction, an account with `cash_account` MUST be engage.

## Model

- `(account)-[:cash_account]->(___)`

## Policies (rules)

## Fields

## Flow

- Get money from a user account: `user account` withdraw, `org account` deposit, `cash account` withdraw
- Give money to a user account: `cash account` deposit, `org account` withdraw, `user account` deposit
- Pay an invoice: `POS cash account` deposit and reference related transaction to the `invoice`
- Refund an invoice: `POS cash account` withdraw and reference related transaction to the `invoice`
