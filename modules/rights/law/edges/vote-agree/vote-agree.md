# Vote agree
A citizen's recorded agreement with a law: a digital signature over the digest of that law's frozen payload. This is a consent record, not a field of what a law is.

## Model
- `(law)-[:vote_agree_by]->(citizen(user))`

## Policies (rules)
- The signature binds to the digest of the whole payload. A later change of any companion is a different digest, so this signature is not agreement with the changed record.
- Whether a departed member's signature is deleted, or kept as history and omitted only from a live count, is not decided on this edge. See the law handoff.
