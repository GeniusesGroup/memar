# Contract status

## Model

- Candidate (unconfirmed): contract lifecycle loop-edges — vocabulary: `Negotiation`, `PartlySigned`, `Signed`, `LegalAction`, `Done`, `Canceled`.

## Policies (rules)

- The six labels above — comment-level only; no who-may-advance/what-a-transition-triggers recorded (no bare edges).

## Placement

- **Contract (the domain) owns its lifecycle vocabulary; ratification form is loop-edge folders under `contract/status/<name>/`, read through [status](../../../../knowledge/status/status.md)** — status.md: "A domain defines the statuses that belong to it as loop-edges under `<domain>/status/<name>/`"; the precedent is [voting](../../../law/status/voting/voting.md) for laws (and the owner decided the same for law in [law.handoff.md](../../../law/law.handoff.md)). Ratified states move to the loop-edge folders — not a bare `edges/status/` flag family.
- **Not a new module:** six labels are a value list, not processing (parameters vs semantics) — configuration for the status reader.
- Transitions are rule decisions (core never knows Rule): who may advance, and what each step triggers, must come from rules before any label is ratified (no bare edges).

## Open questions

- No bare edges — who may advance a contract status and what each transition triggers is missing from the comments.
- Is contract lifecycle a status machine read through [status](../../../../knowledge/status/status.md) (the way [voting](../../../law/status/voting/voting.md) reads it for laws) or rule-driven state (core never knows rule)?
- How do `LegalAction`/`Done`/`Canceled` reconcile with the existing [legal_action](../legal_action/legal_action.md) edge and the case lifecycle — is `LegalAction` a status (loop-edge) or the trigger that creates the `legal_action` edge?
- Is `PartlySigned` a state of one signing process, or a distinct contract kind (the signed-partly file suggests a separate flag)?

