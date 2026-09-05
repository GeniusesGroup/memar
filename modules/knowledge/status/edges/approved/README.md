# Approved

## Model

- `(quiddity)-[:approved_by]->(user)`
- `(quiddity)-[:approved_by]->(group)`
- `(user)-[:approved]->(quiddity)`
- `(group)-[:approved]->(quiddity)`

## Policies (rules)

- quiddity CAN be e.g. `request`, `law`, `task`, `contract`, ...
- SignatureBy or ApprovedBy means user accept the contract agreements
- Signature will store by related request in `audit-request`.
- SignatureBy
