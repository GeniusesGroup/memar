# Account limit transfer

## Dictionary

## Model

- `(account)-[:main_account-give_for]->(user)`
- `(user)-[:main_account-give_is]->(account)`

## Policies (rules)

- Each two type of records just can on active `primary` relation.
- e.g. a `user` just can have one `primary` `account` or just have one `primary` `picture`
- rule::: each user in a FinancialCurrency MUST have just one account get this label.
- TODO::: When get this label `Owner` label can get back or not??
- MainAccount
- PrimaryAccount

## Fields
