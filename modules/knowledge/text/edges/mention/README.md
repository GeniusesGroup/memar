# Mention

## Model

- `(text)-[:mention]->(user)`
- `(user)-[:mention_in]->(text)`

## Policies (rules)

- User CAN be any type such as person, group, organization, bot, ...
