# Request

## Model

- `(quiddity)-[:request_by]->(user)`
- `(quiddity)-[:request_by]->(group)`
- `(user)-[:request]->(quiddity)`
- `(group)-[:request]->(quiddity)`

## Policies (rules)

- request for any thing like `budget` for `quiddity`, `transaction` for a `budget`, `law` for an `organization`, ...
