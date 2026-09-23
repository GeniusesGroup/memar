# Annul law for conflict
A dispute that annuls the later of two contradictory laws.

## Model
- `(case)-[:annul_law_for_conflict]->(law)`

## Policies (rules)
- This edge is an optional kind of dispute. The case node stays in the case domain. An organization that does not hear this dispute leaves the edge out.
- The law on this edge is the later law, the one the dispute annuls if it succeeds. The earlier law stays in force.
- The annulled law remains in the graph. It does not supersede the earlier law.
- The edge type lives in this module, with the other optional kinds of dispute.
