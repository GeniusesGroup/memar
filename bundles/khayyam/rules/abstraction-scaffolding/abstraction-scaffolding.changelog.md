# Khayyam Rule — Abstraction Scaffolding Changelog

## Changelog

### Abstraction scaffolding rule added from language docs
- Time: 2026-09-29T16:00:00Z
- Type: Added
- Cited:
  - rules-in-docs audit (its session file was not kept in the repository) - Evidence: ORG-rule row for tooling support in abstraction.md.
- Contributors:
  - Auto (model not recorded) via [Cursor](../../../../CONTRIBUTORS.md#cursor) - applied

#### What changed
- Added [abstraction-scaffolding.md](./abstraction-scaffolding.md), [abstraction-scaffolding.handoff.md](./abstraction-scaffolding.handoff.md), and this changelog.
- Tooling-support and scaffolding content relocated from [Abstraction in Khayyam](../../../../docs/khayyam/abstraction.md).

---

### Inheritance Linter Rules scaffolding relocated here
- Time: 2026-09-29T20:30:00Z
- Type: Changed
- Propagates to:
  - Inheritance in Khayyam → Linter Rules (`docs/khayyam/inheritance.md#what-the-linter-may-add`, a heading since removed): Done
- Contributors:
  - Auto (model not recorded) via [Cursor](../../../../CONTRIBUTORS.md#cursor) - applied

#### What changed
- Smart remediation and scaffolding bullets relocated from Inheritance in Khayyam → Linter Rules (`docs/khayyam/inheritance.md#what-the-linter-may-add`, a heading since removed); TcpServer delegation example retained in [abstraction-scaffolding.md](./abstraction-scaffolding.md).

---

### Tooling material moved here from the language documents
- Time: 2026-10-12T11:13:47Z
- Type: Changed
- Propagates to:
  - [Abstraction in Khayyam](../../../../docs/khayyam/abstraction.md), [Agency in Khayyam](../../../../docs/khayyam/agency.md): Done - their tooling clauses were removed in the same change.
- Contributors:
  - [Claude](../../../../CONTRIBUTORS.md#claude) (Opus-5.5) — applied

#### What changed
- [Why it exists](./abstraction-scaffolding.md#why-it-exists) now carries, moved whole from Abstraction in Khayyam's "Abstraction Validation and DX Scaffolding", the discovery cost (tool-assisted graph traversal instead of a text search for `impl`, a tooling burden that is a real cost in ecosystem maturity next to Rust), and, from the tooling clauses of Abstraction in Khayyam and Agency in Khayyam, that a deliberate satisfaction is checked and found by the same means as any satisfier.
- Handoff: the dependency row on Inheritance in Khayyam's removed "What the Linter May Add" section now cites its [Rules](../../../../docs/khayyam/inheritance.md#rules) section.
