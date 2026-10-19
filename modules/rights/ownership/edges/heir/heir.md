# Heir

## Model

- `(ownership)-[:heir_is]->(user)`
- `(ownership)-[:heir_is]->(group)`
- `(user)-[:heir_of]->(ownership)`
- `(group)-[:heir_of]->(ownership)`
