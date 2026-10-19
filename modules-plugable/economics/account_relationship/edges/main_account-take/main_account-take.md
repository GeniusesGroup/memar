# Main account take

## Model

- `(account)-[:main_account-take_for]->(user)`
- `(user)-[:main_account-take_is]->(account)`

## Policies (rules)

- like `main_account_give` it is main account when others want to transfer money to the `user`
