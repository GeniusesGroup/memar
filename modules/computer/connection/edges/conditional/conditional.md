# Authorize by

## Model

- `(connection)-[:authorize_by]->(rule)`

## Policies (rules)

- Use to authorize request send by this connection. Exact rule that allow the request will store in `request` domain.
- Related rules MUST have `access_control` label
