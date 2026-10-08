# Claim relation

## Model

- Candidate (unconfirmed): `(case)-[:claim_relation]->(case)` — the proceeding relation between cases (source was `package label` holding comments only, no edge code).

## Policies (rules)

- "a comprehensive term for any proceeding in a court of law whereby an individual seeks a legal remedy"
- No who-may-create/what-it-triggers recorded — without those semantics the label must not be ratified as an edge (no bare edges).
- Phase-0 draft: this file still does not say the edge is an order. The petition order is drafted as [petition-next](../petition-next/petition-next.md) beside this candidate, not in place of it.
- Related claims that are not ordered must be linked. The defendant may say this was already claimed. A similar case may exist in another organization. This candidate is not chosen as that link. Kernel versus pluggable is open.

## Placement

- **Correct here** — case-to-case proceeding relation is case identity (the dispute node relating its own proceedings); entry point is the case, and it sits beside [settlement_for](../settlement_for/settlement_for.md) already in this folder (prefer the existing home).
- **Not [claims](../../../../../modules-plugable/rights/claims/claims.md):** claims holds particular *accusations*; this is the relation *between case nodes* — different subjects.
- Not a new module: labels only, no processing — a label set is parameters (parameters vs semantics); ratify only when who-may-create/what-it-triggers exists (no bare edges).
- Phase-0 draft: petition-next is not a ratification of this label. The dictionary gloss above is a proceeding in general. An order has a different cardinality (a path) and a different job from "any proceeding."

## Open questions

- Does `ClaimRelation` name the same concept as the claim links inside [claims](../../../../../modules-plugable/rights/claims/claims.md) — one proceeding relation or two (prefer one home)?
- Multi-case proceedings: one edge per related case, or a proceeding node both cases attach to (bare edge or node — cf. the open question in [ownership.md](../../../ownership/ownership.md))?
- Direction and naming unconfirmed — nothing ratified.
- Is `claim_relation` the same edge as `petition_next`? Blocks dropping one of them.
- Which edge links unordered related claims, and in which module? Blocks choosing this candidate for that job.
