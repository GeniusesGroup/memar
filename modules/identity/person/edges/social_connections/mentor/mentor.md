# Mentor

## Model

- `(user)-[:knowledge_unit]->(mentor)`
- `(group)-[:knowledge_unit]->(mentor)`

## Policies (rules)

- User CAN get `mentor` label because of `OrganizationStaff`, `SelfStatement`, `UsersVote`, `AI`, ...
