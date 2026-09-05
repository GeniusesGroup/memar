# Request

## Model

- `(thing)-[:request_by]->(user)`
- `(thing)-[:request_by]->(group)`
- `(user)-[:request]->(thing)`
- `(group)-[:request]->(thing)`

## Policies (rules)

- request for any thing like `budget` for `quiddity`, `transaction` for a `budget`, `law` for an `organization`, ...
