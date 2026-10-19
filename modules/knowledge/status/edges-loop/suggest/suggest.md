# Suggest

## Model

- `(thing)-[:suggest_by]->(user)`
- `(thing)-[:suggest_by]->(group)`
- `(user)-[:suggest]->(thing)`
- `(group)-[:suggest]->(thing)`

## Policies (rules)

- suggest for any thing like `budget` for `quiddity`, `transaction` for a `budget`, `law` for an `organization`, ...
