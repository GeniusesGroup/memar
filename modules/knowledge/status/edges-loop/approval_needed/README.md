# Approval needed

## Model

- `(thing)-[:approval_needed_by]->(user)`
- `(thing)-[:approval_needed_by]->(group)`
- `(user)-[:approval_needed_for]->(thing)`
- `(group)-[:approval_needed_for]->(thing)`

## Policies (rules)

- quiddity CAN be e.g. `request`, `transaction`, ...
