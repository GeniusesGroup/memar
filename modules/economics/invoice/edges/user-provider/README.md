# User provider

## Model

- `(invoice)-[:provider]->(user)` (note: product)
- `(user)-[:provides]->(invoice)`

## Policies (rules)

- Usually a `rule` set this relation and that rule call a `staff` not random user.
