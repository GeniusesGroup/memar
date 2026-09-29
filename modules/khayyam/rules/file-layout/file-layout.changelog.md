# Khayyam Rule — File Layout Changelog

## Changelog

### One abstraction per protocol file advisory added
- Time: 2026-09-29T20:00:00Z
- Type: Updated
- Cited:
  - Owner position (2026-09-29) — multi-abstraction protocol files are confusing; split when concepts are distinct, keep tight families together; observer/mutator companion files are the stated exception.
- Contributors:
  - Auto (model not recorded) via [Cursor](../../../../CONTRIBUTORS.md#cursor) - applied

#### What changed
- Extended [file-layout.md](./file-layout.md) with a strong-default (not mandatory) one-abstraction-per-`protocol/` file guidance, its reasons, and the `<base>.observers.kh` / `<base>.mutators.kh` companion-file exception.
- Noted in [rule.handoff.md](../../../../docs/rule.handoff.md) that `file-layout` is a candidate to move to a module-organization rules home.

### File layout rule added from Khayyam import section
- Time: 2026-09-29T16:00:00Z
- Type: Added
- Cited:
  - [rules-in-docs audit](../../../../chats-context/memar-go-migration/decisions/rules-in-docs-audit.md) - Evidence: ORG-rule row for short files and contracts-first order under import mechanism.
- Contributors:
  - Auto (model not recorded) via [Cursor](../../../../CONTRIBUTORS.md#cursor) - applied

#### What changed
- Added [file-layout.md](./file-layout.md), [file-layout.handoff.md](./file-layout.handoff.md), and this changelog.
- Content relocated from [Khayyam → Import Mechanism (`in`)](../../../../docs/khayyam/khayyam.md#import-mechanism-in).
