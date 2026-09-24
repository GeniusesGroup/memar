# App relation - module

## Model

- Candidate (unconfirmed): an app-to-module relation; the source is an empty placeholder (`//`) and records no labels yet.

## Policies (rules)

- None recorded — placeholder only.

## Placement

- **Core `software` is the natural entry point (app side), but the edge must not ship bare** — no bare edges: who may create/remove it and what it triggers must be identifiable. Either the placeholder gains semantics (then re-evaluate edge vs module: independent processing would make it a capability module) or it stays an empty code placeholder with no model claim.

## Open questions

- What semantics would app-to-module ownership carry (manifest, deployment, dependency)?
- Does the existing [manifest](../manifest/protocol/data_model.go) edge already cover app-to-module structure instead of a new edge?

