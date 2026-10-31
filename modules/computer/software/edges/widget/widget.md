# App relation - widget

## Model

- Candidate (unconfirmed): an app-to-widget relation; the source is an empty placeholder (`//`) and records no labels yet.

## Policies (rules)

- None recorded — placeholder only.

## Placement

- **Core `software` (app entry point) is the natural home, but no bare edges: the placeholder must gain semantics — who creates it, what it triggers — before any model claim ships.** A widget is not bound to a screen ([Widget](../../../ui/widget/widget.md)), so this relation is not rendering; whatever the relation turns out to carry belongs with the module that owns widgets, `computer/ui/widget`, not to a bare edge here.

## Open questions

- What would trigger an app-to-widget edge (composition, rendering target, ownership)?
- The widget module, [Widget](../../../ui/widget/widget.md), claims this relation from its side as its Model line; does that line state the same relation as this placeholder, and which of the two documents then keeps it?

