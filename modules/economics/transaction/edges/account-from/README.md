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
- At most one `account__from` per transaction (invariant #2 in [topic-accounting-invariants.md](../../../topic-accounting-invariants.md)).
- The effect on the source account MUST be booked before any effect of the same transaction on the destination; delay of the destination effect is allowed, reorder is not (invariant #3).
- The source account's `count_unit` defines the transaction's unit; `account__to` MUST share it (invariant #4).

## Fields
