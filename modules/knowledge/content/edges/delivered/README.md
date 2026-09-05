# Delivered

## Model

- `(comment)-[:delivered_to]->(user)`
- `(user)-[:delivered]->(comment)`

## Policies (rules)

- User `delivered` edge MUST store just in client not servers due to unneeded index.
