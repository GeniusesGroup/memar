# Approved

## Model

- `(thing)-[:approved_by]->(user)`
- `(thing)-[:approved_by]->(group)`
- `(user)-[:approved]->(thing)`
- `(group)-[:approved]->(thing)`

## Policies (rules)

- quiddity CAN be e.g. `request`, `law`, `task`, `contract`, ...
- SignatureBy or ApprovedBy means user accept the contract agreements
- Signature will store by related request in `audit-request`.
- SignatureBy
