# Claim service

## Model

- Candidate (unconfirmed): `(case)-[:claim_service]->(service)` — a claim must name a service run by a specific organization; endpoint noted as `service_p.UUID` (source was `package label` holding comments only, no edge code).
- Phase-0 draft: one case names one service. The UUID note is an implementation sketch. It is not part of the edge.

## Policies (rules)

- "Claim must be a service that run by specific organization"
- "Order of services is important. e.g. Identity theft"
- No who-may-create/what-it-triggers recorded — without those semantics the label must not be ratified as an edge (no bare edges).
- Phase-0 draft: the order of services is the [petition-next](../petition-next/petition-next.md) path of cases, one service on each case. It is not a list stored on one case. A registry inquiry is its own claim and is not a step the other cases must wait on. The chain may change after the inquiry, or it may not exist yet. The inquiry's defendant is the target organization. The identity-theft example has no recorded service list. Those steps are not invented here.
- The service is the request (darkhast). The case, with its grounds and evidence, is the subject. See [subject](../subject/subject.md).
- Accept on the [ruling](../../edges-shortcut/ruling/ruling.md) shortcut means this filed invocation may proceed. The ruling does not substitute a different service or a different amount. Accept of this service has no attachment. A consensus of other requests is a later case, not a substitute on this edge.
- Execution of this filed service, when the ruling is final, is a service invocation the system compels. The defendant is not the voluntary caller. The input is not only a number. A public apology invokes a service that writes a text on that person's timeline, addressed to the claimant. That write is another compelled service, not a second procedure and not a second edge on this case.
- This edge does not carry a quantity, and the case does not store one. A number is one possible input of the compelled service. The timeline write is another. A judge who wants a different execution rejects. That reject may point at one `computer/request`, born by editing the draft request. Editing produces a new request and leaves this filed service in place. Timeline text is the explanation. The registered request wins. The pointer is not drawn on this edge, and this edge is not retargeted to `computer/request`. This phase does not write the transaction module. The reversal of an execution that a later break undoes stays a note for that domain.

## Placement

- **Entry point is the claim.** Particular accusations already live in [claims](../../../../../modules-plugable/rights/claims/claims.md) (per [case.md](../../case.md)); if ClaimService survives ratification it moves *with* that capability — a pluggable owns its complete capability (edge + processing), never "edge here, behavior there".
- **Not economics [service](../../../../../modules-plugable/economics/service/service.md) by default:** the label says which organization's service a *claim* must call — that is claim/case semantics; the service module only runs. Economics service is a non-inventory offering. It is not, on its own record, this endpoint.
- Order-of-services sequence semantics is missing processing — until who-orders/what-order-triggers exists, no edge stands (no bare edges).
- Phase-0 draft: the structural edge stays on the case because every complaint names the service it invokes. That is Code. Which organization service is legal to name is a rule, and the identity-theft sequence is still missing, so the edge stays a candidate.

## Open questions

- Is ClaimService an edge to the service domain (economics) — and does the order-of-services need sequence semantics (an ordered claim path, not a list note)?
- Does it move into [claims](../../../../../modules-plugable/rights/claims/claims.md) with the accusations, or stay a case-side structural label?
- Direction and naming unconfirmed — nothing ratified.
- What else, if anything, the registry inquiry connects besides the target organization as defendant is open on [registry-inquiry](../../../../../modules-plugable/rights/claims/edges/registry-inquiry/registry-inquiry.md). Later claims do not wait on it.
