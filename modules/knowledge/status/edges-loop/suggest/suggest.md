# Suggest

## Model

- **Not Status attachment.** Candidate edges to a party, not a Status-kind label. Status-kind attach stays [Label edge](../../../label/edges/label/label.md).
- Candidate (unconfirmed): `(thing)-[:suggest_by]->(user|group)` / inverse `(user|group)-[:suggest]->(thing)`

## Policies (rules)

- suggest for any thing like `budget` for `quiddity`, `transaction` for a `budget`, `law` for an `organization`, ...
