# Authenticated by

## Model

- `(connection)-[:authenticated_by]->(token)`
- `(token)-[:authenticated]->(connection)`

## Policies (rules)

- Use to authenticate by other organization for this user in this org as `SameIdentification`.
