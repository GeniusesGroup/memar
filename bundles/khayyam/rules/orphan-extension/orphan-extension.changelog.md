# Khayyam Rule — Orphan Extension Changelog

## Changelog

### Orphan extension rule added from inheritance doc
- Time: 2026-09-29T16:00:00Z
- Type: Added
- Cited:
  - rules-in-docs audit (its session file was not kept in the repository) - Evidence: ORG-rule row for orphan/monkey-patching rule in inheritance.md.
- Contributors:
  - Auto (model not recorded) via [Cursor](../../../../CONTRIBUTORS.md#cursor) - applied

#### What changed
- Added [orphan-extension.md](./orphan-extension.md), [orphan-extension.handoff.md](./orphan-extension.handoff.md), and this changelog.
- Orphan-rule content relocated from Inheritance in Khayyam → Linter Rules (`docs/khayyam/inheritance.md#what-the-linter-may-add`, a heading since removed).

---

### Modularity inclusion section cited as normative source
- Time: 2026-09-29T20:30:00Z
- Type: Changed
- Propagates to:
  - [Modularity in Khayyam → Inclusion Is Not Module Definition](../../../../docs/khayyam/modularity.md#inclusion-is-not-module-definition): Done
- Contributors:
  - Auto (model not recorded) via [Cursor](../../../../CONTRIBUTORS.md#cursor) - applied

#### What changed
- [orphan-extension.md](./orphan-extension.md): cites [Modularity in Khayyam → Inclusion Is Not Module Definition](../../../../docs/khayyam/modularity.md#inclusion-is-not-module-definition) for local-directory extension syntax; monkey-patching governance text removed from that section in favor of this rule.

---

### Inheritance link repointed after its linter section left
- Time: 2026-10-12T11:13:47Z
- Type: Fixed
- Contributors:
  - [Claude](../../../../CONTRIBUTORS.md#claude) (Opus-5.5) — applied

#### What changed
- [orphan-extension.md](./orphan-extension.md) and its handoff cited `inheritance.md#linter-rules` and `#what-the-linter-may-add`; the first named no heading and the second section was removed on 2026-10-12. Both now cite [Inheritance in Khayyam → Rules](../../../../docs/khayyam/inheritance.md#rules), which records the language-level separation.
