# Approval needed

## Model

- `(quiddity)-[:approval_needed_by]->(user)`
- `(quiddity)-[:approval_needed_by]->(group)`
- `(user)-[:approval_needed_for]->(quiddity)`
- `(group)-[:approval_needed_for]->(quiddity)`

## Policies (rules)

- quiddity CAN be e.g. `request`, `transaction`, ...
