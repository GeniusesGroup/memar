# Math Changelog

## Changelog

### Initial Draft — the number tower protocol
- Time: 2026-09-29T11:17:00Z
- Type: Added
- Cited:
  - [Encapsulation in Khayyam → Primitive Capsule Specification](../../khayyam/encapsulation.md#primitive-capsule-specification) - Premise: numeric tower content belonged at the protocol layer, not in the language document.
  - [Encapsulation in Khayyam Handoff](../../khayyam/encapsulation.handoff.md) - Premise: numeric open questions and owner notes carried from the memar-go port session.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) - decided: implementation and protocol-domain content must not live under `docs/khayyam/`
  - Auto (model not recorded) via [Cursor](../../../CONTRIBUTORS.md#cursor) - applied

#### What changed
- `math.md`: initial Draft with the number tower (`I`/`W`/`R`), complex and platform-sized exceptions, and realization membership (from `modules/math/README.md`).
- `math.handoff.md`: numeric open questions, the owner's earlier notes, the `Bool`/`Boolean` question, and numeric implementation residue, moved from Khayyam handoffs and the deleted module documents.
- `modules/math/README.md`: replaced with a symbolic link to `../../docs/protocols/math/math.md`.

#### Considered and not done
- Keeping tower rules in `encapsulation.md`: rejected; they are protocol-domain, not Khayyam grammar.
