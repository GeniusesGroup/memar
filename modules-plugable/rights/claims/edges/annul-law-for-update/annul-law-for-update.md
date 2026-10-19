# Annul law for update
A dispute that lets a new law take the place of a previous one.

## Model
- `(case)-[:annul_law_for_update]->(law)`

## Policies (rules)
- This edge is an optional kind of dispute, beside annul-law-for-conflict. The case node stays in the case domain.
- The law on this edge is the new law. If the dispute succeeds, that law [supersedes](../../../../../modules/identity/thing/edges/supersedes/supersedes.md) the previous one. The previous law stays in the graph and is no longer the one in that place.
- An organization that does not hear this dispute does not create the edge.
