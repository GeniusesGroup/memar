# User active

## Model

- `(software_instance)-[:user_active]->(user)`

## Policies (rules)

- Just one user can be active on any instance.
- Active user CAN change only by valid connection and valid token.
