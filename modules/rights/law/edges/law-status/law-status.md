# Law status
## Model
- Candidate (unconfirmed): law lifecycle loop-edges — the source vocabulary is `Suggestion`, `Closed`, `Approved`, `Denied` (a `package label` comment file, no edge code). The domain backlog recorded only Closed/Denied; the recovered source carries the full four-label set.

## Policies (rules)
- Vocabulary: `Suggestion` (proposal stage), `Approved`, `Denied`, `Closed` — comment-level only; no who-may-set/what-it-triggers recorded (no bare edges).

## Placement
- **Law owns its Status-kind labels under `law/labels/`, attached only through [Label edge](../../../../knowledge/label/edges/label/label.md)** — declarations in one file per word under [`law/labels/`](../../labels/); kind+rule+event in [Status](../../../../../modules-plugable/knowledge/label/status/status.md). Precedent: [voting](../../labels/voting/voting.md). This doc holds any remaining candidate vocabulary until declared there.
- **Not a new module:** four labels are a value list, not processing semantics (parameters vs semantics) — configuration for the status reader, never grounds a module on its own.
- Transitions are rule decisions (core never knows Rule).
- Not the general status module's own list: [status](../../../../../modules-plugable/knowledge/label/status/status.md) defines *what a status is*; the vocabulary here is law-specific.
