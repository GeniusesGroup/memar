# Transaction order type - instant_withdrawal
Instant withdrawal means when transaction register, the first part of transaction with `account__from` edge MUST be executed to prevent from transaction CAN't be executed in future in many process trade, invoice, ... .

It usually use in a situation that transaction is part of bigger contract such as in [Pre-purchase inspection](https://en.wikipedia.org/wiki/Pre-purchase_inspection) that transaction MUST complete if and if third-party professional service evaluate seller statement about the (house, car, ...).

## Model

- `[transaction-[:instant_withdrawal]->(___)`

## Policies (rules)

## Fields
