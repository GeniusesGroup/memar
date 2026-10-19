# Spam flaged user

## Model

- `(user)-[:own]->(request)-><-[:spam]->(text)`
- `(text)-[:spam_flagged__user_by]->(user)`
- `(user)-[:spam_flagged__user_for]->(text)`
