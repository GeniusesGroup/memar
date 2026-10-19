# Quote limit to user

## Model

- `(comment)-[:quote_limit_to_user]->(user)`
- `(quote_limit_to_user)-[:preference_for]->(quote)`

## Policies (rules)

- e.g. Just mentioned `user` can embed this `comment` in other `comment`s.
