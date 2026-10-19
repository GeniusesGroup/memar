# Vote disagree
A citizen's recorded disagreement with a law. This is a consent record, not a field of what a law is.

## Model
- `(law)-[:vote_disagree_by]->(citizen(user))`

## Policies (rules)
- The signature binds to the digest of the whole payload. A later change of any companion is a different digest.
- ["VAT", `vote_disagree_by`, "Omid"]
