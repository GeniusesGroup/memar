# Owner

## Model

- `(ownership)-[:owner_is]->(user)`
- `(ownership)-[:owner_is]->(group)`
- `(user)-[:owner_of]->(ownership)`
- `(group)-[:owner_of]->(ownership)`
- `(user)-[:owner_of]->(account)`

## Policies (rules)

- Just owner MUST edit the related record in any domain
- Others CAN fork or update if owner allow.
