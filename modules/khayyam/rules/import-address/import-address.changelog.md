# Khayyam Rule — Import Address Changelog

## Changelog

### Repository-root-relative URI convention cited from modularity doc
- Time: 2026-09-29T16:00:00Z
- Type: Changed
- Cited:
  - [rules-in-docs audit](../../../../chats-context/memar-go-migration/decisions/rules-in-docs-audit.md) - Evidence: ORG-rule row for modularity dependency-resolution URI spelling.
- Contributors:
  - Auto (model not recorded) via [Cursor](../../../../CONTRIBUTORS.md#cursor) - applied

#### What changed
- Confirmed [The rule](./import-address.md#the-rule) already records repository-root-relative `in` URIs; duplicate organizational wording removed from [Modularity in Khayyam → Dependency Resolution and Companion Manifest](../../../../docs/khayyam/modularity.md#dependency-resolution-and-companion-manifest) in favor of a link here.

---

### The base is a default, and it is the writing module's manifest
- Time: 2026-09-30T00:00:00Z
- Type: Changed
- Ruling: owner, 2026-09-29
- Contributors:
  - opencode (space-bunny-free) - applied

#### What changed
- [The rule](./import-address.md#the-rule) states the base as a **default** rather than as a fact: by default it is the manifest of the module that wrote the address, and a project may resolve from somewhere else provided it says so, while no project may resolve from something undeclared. The previous version named the repository root as a plain fact and this toolchain read that as licence, so the rule's whole reason for existing — keeping a choice explicit — was defeated by its own wording. This is a change to how the rule states a default, not to what a default is.
- A URI need not be path-shaped: the rule now accepts one carrying no path separator at all, alongside the no-extension and foreign-extension cases it already accepted.
- The rule points at [dependency management](../../../docs/protocols/modules/dependency-management.md) for what a module's manifest claims and how one reaches it, and no longer restates any of it. A rule about the shape of an address has no business carrying the design of the thing that resolves it — that mistake put a manifest's obligations and its file name into this rule's changelog, where a later session would have read them as language decisions.

#### Considered and not done
- **Stating the manifest's name or its obligations in this rule.** Considered and removed: they were recorded here and are [dependency management's subject](../../../docs/protocols/modules/dependency-management.md), and a session reading this changelog would have concluded that the language had examined dependency management, which it has not.
- **Rewriting the corpus's 663 `in` URIs as claims rather than paths.** Considered; not done, and out of this rule's reach — the rule requires that a reader of a URI be able to say who answers for it, not that the spelling change.
