# Transaction order type - all_or_none
[All or none(AON)](https://en.wikipedia.org/wiki/All_or_none) is a finance term used in investment banking or securities transactions that refers to "an order to buy or sell a stock that must be executed in its entirety, or not executed at all". Partial execution is not acceptable; the order will execute "only if there are enough shares available in a single transaction to cover it".

## Model

- `[transaction-[:all_or_none]->(___)`

## Policies (rules)

- Whole order must be filled for matching deal or order must cancelled on timeout
- If this flag absent, allow matching engine to deal part of order.
- an order that must be executed in its entirety, or not executed at all

## Fields
