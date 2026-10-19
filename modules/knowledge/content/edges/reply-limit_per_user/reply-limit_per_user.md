# Reply limit per user

## Model

- `(comment)-[:reply_limit_per_user]->(---)`
- `(reply_limit_per_user)-[:preference_for]->(reply)`

## Policies (rules)

- In some comment like comment for a law, We need to limit user JUST reply one to each comment to law timeline to prevent discussion entropy.
- It will not limit user to reply to the comment, Just if other user has other preferences like just get reply from some specific users.
