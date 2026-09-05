# Transaction account from
`account from` or `gives from` or `transfer from` or `sender` or `SELL` indicate which account withdraw.

## Model

- `(transaction)-[:account__from]->(account)`

## Policies (rules)

- Indicate what will gives in this transaction
- It is optional! It means a `user` want to `takes` something without `gives` anything!
- `sell` is not good name as other side MUST be `money` not other types.
- Be aware about [negative pricing](https://en.wikipedia.org/wiki/Negative_pricing)
- Use financial account to support almost all transaction types
- e.g. bond be exchanged for currency and deposits
- e.g. sell product and buy other product by JUST move inventory to middle temp accounts.

## Fields
