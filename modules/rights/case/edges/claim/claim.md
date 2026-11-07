# Claim relation
## Model
- Candidate (unconfirmed): `(case)-[:claim_relation]->(case)` — the proceeding relation between cases (source was `package label` holding comments only, no edge code).

## Policies (rules)
- "a comprehensive term for any proceeding in a court of law whereby an individual seeks a legal remedy"
- No who-may-create/what-it-triggers recorded — without those semantics the label must not be ratified as an edge (no bare edges).
- Phase-0 draft: this file still does not say the edge is an order. The petition order is drafted as [petition-next](../petition-next/petition-next.md) beside this candidate, not in place of it.
- Related claims that are not ordered must be linked. The defendant may say this was already claimed. A similar case may exist in another organization. This candidate is not chosen as that link.

## Placement
- **Correct here** — case-to-case proceeding relation is case identity (the dispute node relating its own proceedings); entry point is the case, and it sits beside [settlement_for](../settlement_for/settlement_for.md) already in this folder (prefer the existing home).
- **Not [claims](../../../../../modules-plugable/rights/claims/claims.md):** claims holds particular *accusations*; this is the relation *between case nodes* — different subjects.
- Not a new module: labels only, no processing — a label set is parameters (parameters vs semantics); ratify only when who-may-create/what-it-triggers exists (no bare edges).
- Phase-0 draft: petition-next is not a ratification of this label. The dictionary gloss above is a proceeding in general. An order has a different cardinality (a path) and a different job from "any proceeding."
