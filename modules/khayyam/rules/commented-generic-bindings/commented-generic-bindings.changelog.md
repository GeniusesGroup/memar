# Khayyam Rule — Commented Generic Bindings Changelog

## Changelog

### Type-owned generic instantiations stay in the owner module
- Time: 2026-09-29T18:00:00Z
- Type: Changed
- Contributors:
  - Auto (model not recorded) via [Cursor](../../../../CONTRIBUTORS.md#cursor) - applied

#### What changed
- [commented-generic-bindings.md](./commented-generic-bindings.md): single-argument generic instantiations such as `Equivalence[T]` are emitted as owner-scoped methods on the concrete type's module and compose the concept abstraction there; they are no longer emitted as `Concept_Type` matrix abstractions in the concept module.
- [abstraction_bridge.py](../../targets/go/abstraction_bridge.py): `CorpusPort.name_instantiations`, `materialize`, and `render_target` honour type-owned instantiations; [test_abstraction_bridge.py](../../targets/go/test_abstraction_bridge.py) covers home placement.
