# Limit event per user

## Model

- `(timeline)-[:limit_event_per_user]->(---)`
- `(limit_event_per_user)-[:preference_for]->(event)`

## Policies (rules)

- In some timeline like vote for a law, We need to limit user JUST assign one comment to law timeline
- It will not limit user to reply to other comment, Just if other user has other preferences like just get reply from some specific users.
