# Vote abstention
A citizen's recorded refusal to decide a law, leaving the outcome to those who vote. This is a consent record, not a field of what a law is.

## Model
- `(law)-[:vote_abstention_by]->(citizen(user))`

## Policies (rules)
- Used when a citizen does not want to vote a law, so other voters decide.
- The record binds to the digest of the whole payload, same as agree and disagree.
