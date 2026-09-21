# Creator

## Model

- `(ownership)-[:creator_is]->(user)`
- `(user)-[:creator_of]->(ownership)`

## Policies (rules)

- User CAN be any type such as person, group, organization, bot, ...
- picture, image, ... CAN have creator that not owner of them
- ID can be even other organizations like `ISO`
- RegisteredBy
