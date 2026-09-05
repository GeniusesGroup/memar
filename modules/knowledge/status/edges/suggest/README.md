# Suggest

## Model

- `(quiddity)-[:suggest_by]->(user)`
- `(quiddity)-[:suggest_by]->(group)`
- `(user)-[:suggest]->(quiddity)`
- `(group)-[:suggest]->(quiddity)`

## Policies (rules)

- suggest for any thing like `budget` for `quiddity`, `transaction` for a `budget`, `law` for an `organization`, ...
