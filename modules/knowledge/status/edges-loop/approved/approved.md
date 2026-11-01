# Approved

## Model

- **Not Status attachment.** These are candidate edges to a party (user/group), not a Status-kind label on the thing. Do not rewrite them as `(thing)-[:label]->(approved)` and do not keep them under a Status attach path. Attachment of Status-kind words stays [Label edge](../../../label/edges/label/label.md). Home of approval-as-capability is still open (Label Research 001 split).
- Candidate (unconfirmed): `(thing)-[:approved_by]->(user|group)` / inverse `(user|group)-[:approved]->(thing)`

## Policies (rules)

- quiddity CAN be e.g. `request`, `law`, `task`, `contract`, ...
- SignatureBy or ApprovedBy means user accept the contract agreements
- Signature will store by related request in `audit-request`.
- SignatureBy
