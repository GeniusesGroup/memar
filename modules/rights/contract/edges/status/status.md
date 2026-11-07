# Contract status
## Model
- Candidate (unconfirmed): contract lifecycle loop-edges — vocabulary: `Negotiation`, `PartlySigned`, `Signed`, `LegalAction`, `Done`, `Canceled`.

## Policies (rules)
- The six labels above — comment-level only; no who-may-advance/what-a-transition-triggers recorded (no bare edges).

## Placement
- **Contract owns its lifecycle vocabulary as Status-kind labels** declared under the domain's `labels/`. Attachment is only [Label edge](../../../../knowledge/label/edges/label/label.md); kind+rule+event is [Status](../../../../../modules-plugable/knowledge/label/status/status.md). Precedent reading for laws: [voting](../../../law/labels/voting/voting.md). This `edges/status/` folder is not a second attach mechanism.
- **Not a new module:** six labels are a value list, not processing (parameters vs semantics) — configuration for the status reader.
- Transitions are rule decisions (core never knows Rule): who may advance, and what each step triggers, must come from rules before any label is ratified (no bare edges).
