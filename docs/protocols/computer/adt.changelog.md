# Abstract Data Types Changelog

## Changelog

### Initial Draft — established ADT translations
- Time: 2026-09-29T11:17:00Z
- Type: Added
- Cited:
  - [Modularity Handoff](../modularity.handoff.md) - Premise: ADT module-placement question belonged with the ADT protocol, not modularity alone.
  - [`modules/computer/adt/`](../../modules/computer/adt/) - Evidence: existing protocol declarations.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) - decided: state only what the corpus already establishes
  - Auto (model not recorded) via [Cursor](../../CONTRIBUTORS.md#cursor) - applied

#### What changed
- `adt.md`: initial Draft recording raw ADT protocol location and the `Array_Dynamic`, `Array_Associative`, and `Container_Element` translations already in the corpus.
- `adt.handoff.md`: "Do the abstract data types belong under `computer`, or under `math`?" moved from `modularity.handoff.md`.

#### Considered and not done
- Deciding module placement in the body: left open in the handoff for the owner.

### Observer/mutator rule and ADT rules index
- Time: 2026-09-29T21:00:00Z
- Type: Changed
- Cited:
  - [Rule → Where Rules Live: rules/ Beside protocol/](../rule.md#where-rules-live-rules-beside-protocol) - Premise: ADT module owns observer/mutator governance.
  - [observer-mutator.handoff.md](../../modules/computer/adt/rules/observer-mutator/observer-mutator.handoff.md) - Premise: owner decisions on method naming and side files.
- Contributors:
  - Auto (model not recorded) via [Cursor](../../CONTRIBUTORS.md#cursor) - applied

#### What changed
- Relocated observer/mutator rule from Khayyam rules to [modules/computer/adt/rules/observer-mutator/](../../modules/computer/adt/rules/observer-mutator/observer-mutator.md); added ADT `rules/` README.
- Updated [adt.handoff.md](./adt.handoff.md) plan item to cite the new rule path.
