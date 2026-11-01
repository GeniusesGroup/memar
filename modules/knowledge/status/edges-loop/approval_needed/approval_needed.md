# Approval needed

## Model

- **Not Status attachment.** Candidate edges to a party, not a Status-kind label. Status-kind attach stays [Label edge](../../../label/edges/label/label.md). Approval capability home still open.
- Candidate (unconfirmed): `(thing)-[:approval_needed_by]->(user|group)` / inverse `(user|group)-[:approval_needed_for]->(thing)`

## Policies (rules)

- quiddity CAN be e.g. `request`, `transaction`, ...
