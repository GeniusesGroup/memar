# Transaction trade
Add watcher to specific transactions to check min or max to make a deal (sell/buy) order.

## Model

- `[transaction-[:trade_by]->(market{rule})`

## Policies (rules)

- Use to send the transaction to desire matching engine
- use to register an order to e.g. exchange(an instruction to buy or sell) currencies
- A matching engine uses the orders book to determine which orders can be fully or partially executed.
- An DataModel submitted without a specified price, and sequentially matched at the best available price in the market or in other words
- if user want to limit price, must fill order-price record otherwise market price will choose for the deals.

## Fields
