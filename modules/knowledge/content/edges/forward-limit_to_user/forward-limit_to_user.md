# Forward limit to user

## Model

- `(comment)-[:forward_limit_to_user]->(user)`
- `(forward_limit_to_user)-[:preference_for]->(forward)`

## Policies (rules)

- e.g. Just mentioned `user` can forward this `comment` in other timeline.
