# Claim relation

## Model

- Candidate (unconfirmed): `(case)-[:claim_relation]->(case)` — the proceeding relation between cases (source was `package label` holding comments only, no edge code).

## Policies (rules)

- "a comprehensive term for any proceeding in a court of law whereby an individual seeks a legal remedy"
- No who-may-create/what-it-triggers recorded — without those semantics the label must not be ratified as an edge (no bare edges).

## Placement

- **Correct here** — case-to-case proceeding relation is case identity (the dispute node relating its own proceedings); entry point is the case, and it sits beside [settlement_for](../settlement_for/settlement_for.md) already in this folder (prefer the existing home).
- **Not [claims](../../../../../modules-plugable/rights/claims/claims.md):** claims holds particular *accusations*; this is the relation *between case nodes* — different subjects.
- Not a new module: labels only, no processing — a label set is parameters (parameters vs semantics); ratify only when who-may-create/what-it-triggers exists (no bare edges).

## Open questions

- Does `ClaimRelation` name the same concept as the claim links inside [claims](../../../../../modules-plugable/rights/claims/claims.md) — one proceeding relation or two (prefer one home)?
- Multi-case proceedings: one edge per related case, or a proceeding node both cases attach to (bare edge or node — cf. the open question in [ownership.md](../../../ownership/ownership.md))?
- Direction and naming unconfirmed — nothing ratified.

