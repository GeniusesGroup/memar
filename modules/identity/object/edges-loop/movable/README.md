# Movable

## Model

- `(thing)-[:movable]->(---)`

## Policies (rules)

- It will use to not render for map service like `google maps` or `open-street-map` or just org internal map.
- IT CAN not use for `estate`

## Open questions (from the Estate session, 2026-08-05..09)

- The estate discussion left "are movable objects estates?" **open** (furniture was the boundary case — it can sit *in* an estate), while the rule above forbids `movable` for estates. Reconcile: is this rule the *current* answer to that open question, or orthogonal to it (qualification for estate via runtime policy, versus rendering policy here)? Decide explicitly in [estate.handoff.md](../../../estate/estate.handoff.md) — and note the discussion's confirmed principle that what qualifies as an estate is organization runtime policy, not a hard-coded exclusion.
