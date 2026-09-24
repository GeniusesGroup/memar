# App relation - widget

## Model

- Candidate (unconfirmed): an app-to-widget relation; the source is an empty placeholder (`//`) and records no labels yet.

## Policies (rules)

- None recorded — placeholder only.

## Placement

- **Core `software` (app entry point) is the natural home, but no bare edges: the placeholder must gain semantics — who creates it, what it triggers — before any model claim ships.** If widget binding turns out to be GUI rendering processing, the complete capability belongs with the module that owns widgets, not to a bare edge here.

## Open questions

- What would trigger an app-to-widget edge (composition, rendering target, ownership)?
- Does a widget-owning module already claim this relation from its side (no `widget` module exists in this repository today)?

