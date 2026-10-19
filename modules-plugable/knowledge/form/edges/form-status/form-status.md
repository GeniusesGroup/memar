# Form status

## Model

- Candidate (unconfirmed): a form status loop-edge — `Terminated` (one status in the source; direction/shape unconfirmed).

## Policies (rules)

- Only the status name recorded — what Terminated blocks (answering? editing? viewing?) is absent from the source (no bare edges).

## Placement

- **Correct here — a domain status belongs to the domain that defines it** (the status domain's own rule: "A domain defines the statuses that belong to it as loop-edges under `<domain>/status/<name>/`" — [status](../../../../../modules/knowledge/status/status.md); the form domain states its record here, never repeating the list in [form.md](../../form.md)).
- **Not the status module's own list:** the general status domain holds the account of what a status is and the shared loop-edges; `Terminated` is form-specific vocabulary — placed with the form capability that gives it meaning (placement by entry point; pluggable owns complete capability: edge + the answering-session rules that read it).
- **Not a new module:** one status name is not processing semantics (parameters vs semantics; prefer existing homes over inventing new modules).
- Status vs label distinction per [status](../../../../../modules/knowledge/status/status.md): labels check in business-rule logic (async), status checks in service logic (sync) — which side Terminated serves must be recorded before ratifying (no bare edges).

## Open questions

- Reconcile with the general status domain (knowledge/status) — own form status set or shared labels? (Receiving [form.md](../../form.md) backlog question.)
- What does Terminated block, and who moves the status (no bare edges)?
- Interaction with `Type_Duration`/`Type_StartPoint` type flags ([types](../types/types.md)) — does termination follow the duration, or is it an explicit move?

