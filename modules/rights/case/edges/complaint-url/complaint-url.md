# Complaint URL

## Model

- Candidate (unconfirmed): a complaint intake URL recorded as a case-entry channel — `sabz.city/complaints?tel=xxxxxxxxxx&orgID=xxx` (complainant telephone + organization ID as query parameters).

## Policies (rules)

- URL parameters: `tel` (complainant telephone), `orgID` (organization) — an identification/routing sketch only; no who-may-submit/what-it-triggers semantics recorded (no bare edges).

## Placement

- **Not an edge — UI, not model.** The standing review already says so: a URL sketch is an intake channel, not a relation, so it never ratifies as an edge. It still gets this own doc so the sketch's explanation lives in an edge folder rather than in a domain document; the verdict is to keep it documentation-only.
- If pursued at all, it is an *entry trigger* for a [Case](../../case.md) node — that question stays with [case.md](../../case.md) ("What triggers the creation of a Case node"); the GUI/service that receives the complaint owns the parameter handling (placement by entry point: UI layer).
- Not [claims](../../../../../modules-plugable/rights/claims/claims.md): it names no accusation, only an org to route to.

## Open questions

- Does `orgID` select the *receiving* organization (routing) or the *accused* organization?
- Does complaint intake feed [claims](../../../../../modules-plugable/rights/claims/claims.md) (particular accusations), or open a bare [Case](../../case.md)?
- The domain backlog attributed this sketch to `case.go`, but no tracked copy of that comment ever lived there — is the cited source mislabeled (the only tracked copy sat in a POS page-label file)?

