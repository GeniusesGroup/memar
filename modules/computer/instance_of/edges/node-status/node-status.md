# Node lifecycle status

## Model

- Candidate (unconfirmed): four flag groups on the node (iota flags in package `label`):
  - lifecycle — `Starting`, `Running`, `Stopping`, `Stopped`
  - power source — `Power_Failure`, `Power_Green`, `Power_UPS`, `Power_Diesel`
  - stability — `Stable`, `NotResponse`
  - cluster operations — `Splitting`, `ReAllocate`, `AcceptWrite`

## Policies (rules)

- `Starting` = "plan to start e.g. wait for hardware to be available".
- `Power_Green` = "provide by any recyclable sources".

## Placement

- **Core `instance_of` keeps lifecycle and stability; the cluster-operation group and power-source group are pending review (create now, decide later).** Node lifecycle is core-by-necessity for a running instance and stored flags are parameters in one module.
- If cluster operations (Splitting/ReAllocate/AcceptWrite) grow reallocation processing, that complete capability (edge + processing together) is a pluggable candidate — split only then, never flags here with behavior elsewhere.
- Power-source labels may belong to an estate/energy concern — flagged as open, not moved.

## Open questions

- Are lifecycle and cluster-operation states one state machine or two?
- Do power-source labels belong to this module or to an estate/energy concern?
- Is `NotResponse` a stored state or a computed observation (analytics is always pluggable)?

