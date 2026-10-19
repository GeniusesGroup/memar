# Reply limit to user

## Model

- `(comment)-[:reply_limit_to_user]->(user)`
- `(reply_limit_to_user)-[:preference_for]->(reply)`

## Policies (rules)

- Just mentioned `user` can made a `comment` relation to this `comment` with `reply` label.
- When comment limit to creator user, means no one can made a relation to this `comment` with `reply` label except the creator user.
