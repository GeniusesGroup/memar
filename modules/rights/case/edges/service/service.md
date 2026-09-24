# Claim service

## Model

- Candidate (unconfirmed): `(claim/case)-[:claim_service]->(service)` — a claim must name a service run by a specific organization; endpoint noted as `service_p.UUID` (source was `package label` holding comments only, no edge code).

## Policies (rules)

- "Claim must be a service that run by specific organization"
- "Order of services is important. e.g. Identity theft"
- No who-may-create/what-it-triggers recorded — without those semantics the label must not be ratified as an edge (no bare edges).

## Placement

- **Entry point is the claim.** Particular accusations already live in [claims](../../../../../modules-plugable/rights/claims/claims.md) (per [case.md](../../case.md)); if ClaimService survives ratification it moves *with* that capability — a pluggable owns its complete capability (edge + processing), never "edge here, behavior there".
- **Not economics [service](../../../../../modules-plugable/economics/service/service.md) by default:** the label says which organization's service a *claim* must call — that is claim/case semantics; the service module only runs.
- Order-of-services sequence semantics is missing processing — until who-orders/what-order-triggers exists, no edge stands (no bare edges).

## Open questions

- Is ClaimService an edge to the service domain (economics) — and does the order-of-services need sequence semantics (an ordered claim path, not a list note)?
- Does it move into [claims](../../../../../modules-plugable/rights/claims/claims.md) with the accusations, or stay a case-side structural label?
- Direction and naming unconfirmed — nothing ratified.

