# Transaction account by
`account by` or `account takes` used when transaction made for two (or more) account that don't have same unit e.g. $ and €. Usually use in `exchange` and `order` logic that a user make a transaction that two account will engage as `account__from` and `account__by` that both will own to the same user. In `order` other transaction CAN made a `deal` relation and will be processed. e.g. a user make a transaction to give 50$ from `account__from` to get 40€ in its `account__by` with anyone that need opposite transaction (give 40€ to get 50$).

## Dictionary
take  [teɪk]

n.
1. the income or profit arising from such transactions as the sale of land or other property

## Graph
- `(transaction)-[:account__by]->(account)`

## Policy (rule)
-    =~ BUY
- but `buy` is not good name as other side MUST be `money` not other types.
-
- Indicate what will takes in this transaction
- It is optional! It means a `user` want to `gives` something without `takes` anything!
- Be aware about [negative pricing](https://en.wikipedia.org/wiki/Negative_pricing)
- It isn't limited to money; it can be any other asset too, like giving the bond and getting the money or another bond.

## Fields
