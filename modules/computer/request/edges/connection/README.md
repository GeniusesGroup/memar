# Connection

## Model

- `(request)-[:called_by]->(connection)`
- `(connection)-[:called]->(request)`

## Policies (rules)

- Store to help us answer these questions:
- AppInstance request came from
- UserID of hardware owner
- Is it official GUI app or SDK or API call
