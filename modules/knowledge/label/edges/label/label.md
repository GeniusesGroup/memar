# Label

## Model

- `(thing)-[:label]->(label)`
- reverse: `(label)-[:label_of]->(thing)`

The far end is the label's own vertex (its identifier). A Status-kind value is the same edge: `(task)-[:label]->(queued)` with `(queued)-[:label]->(Status)` on the definition ([Label → A name is one label](../../label.md#a-name-is-one-label); [Status](../../../status/status.md#what-a-status-is)). Code: [`attach.py`](../../services/attach.py). No other domain restates this relation.

## Policies (rules)

- Who may attach or withdraw, and what an attachment triggers, must be stated for the label (or a default the Label module owns). A bare `(thing)-[:label]` without that contract does not exist ([Modules → Placement](../../../../modules.md#placement)).
- Meta-labels that classify a word (`Status`, `TaskKind`, …) sit on the label's definition, never as intrinsic marks on every record that took the word.

## Placement

- **Label owns attachment.** Registries and domain `labels/` folders declare words; they cite this edge and add none ([thing labels](../../../../../modules-plugable/knowledge/thing-labels/thing-labels.md), [law labels](../../../../../modules-plugable/rights/law/labels/labels.md), …).
- The former loop spelling `(thing)-[:label]->(---)` under `edges-loop/label/` is retired; that folder points here.

## Open questions

- Default contract for who may attach/withdraw (rights vs Label kernel) — still open from Label Research 001 U2.
