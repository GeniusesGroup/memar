# Node resource type (Desired / Actual)

## Model

- Candidate (unconfirmed): resource type labels `Desired`, `Actual` (iota `Type_*` flags in package `label`) typing the node's resource edge — see the sibling resource concept (protocol `ResourceType` / `ResourceAmount`) in [](../resource/).

## Policies (rules)

- Desired vs Actual duality: the intended resource amount vs the observed one, recorded as two type labels.

## Placement

- **Uncertain (create now, decide later) — the flag vocab stays core `instance_of` with the resource edge, because a type flag is a parameter inside one module (parameters vs semantics).** If Desired/Actual grows reconciliation processing, that complete capability is evaluated at its own entry point (pluggable candidate), never as flags here with behavior elsewhere.
- If the pattern generalizes (estate, production), the shared concept must be referenced by UUID across domains — no embedded duplicate types (see the reference-by-UUID rule in [bookkeeping](../../../../economics/account/edges/bookkeeping/README.md)).

## Open questions

- Is Desired/Actual a general pattern (also usable for estate/production)?
- Same edge as the [](../resource/) concept folder, or a separate typed facet?

