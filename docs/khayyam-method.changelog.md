# Method in Khayyam Changelog

## Changelog

### Initial creation, merging Function as Capsule and Composition Depth
- Time: 2026-07-28T00:00:00Z
- Type: Added
- Cited:
  - [Khayyam - Programming Language](./khayyam.md) — Reference: the canonical specification defines the `mt` subtype and the method signature grammar this document elaborates and motivates.
  - [Encapsulation in Khayyam](./khayyam-encapsulation.md) — Depends_on: Method Structure relies on the capsule model — Capsule Structure and Privacy, Sovereign Encapsulation — defined there, for its common-case examples and for the state-protection guarantee described under Pass-by-Reference and State Protection. Encapsulation in Khayyam references this document back for the method-signature mechanics.
  - [Logic in Khayyam](./khayyam-control_flow.md) — Reference: Logic in Khayyam's IF/ELSE model relies on the same pass-by-reference, explicit-influenced-variable mechanic specified here under Method Structure — no chaining, in either document, is a consequence of that mechanic.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed: original design decisions for the absence of a `fn`/`func` keyword, for rejecting expression chaining, and for the method signature grammar in the canonical Khayyam specification; reframed method parameters away from an input/output model toward owner, influencing, and influenced variables; identified the open dual-role-variable question (a variable that is both influencing and influenced in the same call).
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM 5.2, medium effort) — rewrote: reference-level elaboration of method dispatch (static-vs-instance invocation, body-less methods for FFI/contracts).
  - [Claude](../CONTRIBUTORS.md#claude) (claude-sonnet-5, high effort) — rewrote: merged the standalone Function as Capsule and Composition Depth documents into the current Explanation-facet specification; specified Method Structure (signature grammar, pass-by-reference, static-vs-instance invocation, body-less methods for FFI/contracts); reframed method parameters as owner/influencing/influenced variables in place of the traditional arguments/return-values framing, with a dedicated Explanation topic for the reasoning; wrote "No Dedicated fn/func Keyword," leading with the argument that a seemingly type-independent behavior (e.g. `Sum`) almost always turns out to belong to a specific type once examined, with the wrapper-capsule-plus-`Do` pattern presented as the fallback rather than the default.

#### Summary
Synthesized the standalone "Function as Capsule (No fn/func Keyword)" and "Composition Depth as a Decomposition Signal (No Expression Chaining)" documents into one Explanation-facet document, alongside a newly specified Method Structure topic (signature grammar, pass-by-reference, static-vs-instance dispatch, body-less methods for FFI/contracts). Method parameters were renamed owner / influencing variable / influenced variable rather than the conventional "arguments"/"return values," since a pass-by-reference model where types carry their own mutating methods makes the input/output framing actively misleading, not merely old-fashioned.

---

### Migration to the current documentation methodology
- Time: 2026-08-17T00:00:00Z
- Type: refactor
- Cited:
  - [System](./system.md) — Reference: the new "When Is a Responsibility Coherent?" section is cited from Composition Depth as a Decomposition Signal, since that topic's decomposition test is a Khayyam-specific, syntactically-enforced application of the general one stated there.
  - [Modularity](./modularity.md) — Reference: cited alongside System for the same reason, at the architectural rather than conceptual level.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: asked for this document's method-ownership content to be checked in light of the Agency/Khayyam discussion happening in the same review effort, and, regardless of whether that check produced any content change, for the document to be brought fully up to the current documentation methodology, since it still carried old-style front-matter `Citations`/`Contributors`/`Applied to` and a body-level `## Change Rationale` section despite already having been restructured into `Abstract`/`Introduction`/`Explanation`/`Results`/`Discussion` at some earlier point.
  - [Claude](../CONTRIBUTORS.md#claude) — reviewed, rewrote: checked "owner" as used in Method Structure (the type a method is attached to — a capsule, an abstraction, or another method) against Agency's Principal/Agent/delegation model, and found them unrelated despite the shared word — Method's "owner" is a type-system attachment point, not a party responsible for or delegating an action, so no Agency connection was added here; the corresponding speculative Unresolved question in `khayyam-agency.md` was corrected to record this finding rather than left open. Moved front-matter `Citations` and `Contributors` into this changelog; removed the stale `Applied to: []` field; removed the body-level `## Change Rationale` section, whose two items are preserved above and in the Initial creation entry. Added a cross-reference from Composition Depth as a Decomposition Signal to `system.md`'s new "When Is a Responsibility Coherent?" section and to `modularity.md`, since that topic's decomposition-signal argument is a Khayyam-specific instance of the same independent-responsibility test, and had no cross-reference to either despite predating both.

#### Summary
This document already used the current template's top-level structure but had not been fully migrated: front matter still carried old-style `Citations`, `Contributors`, and `Applied to` fields, and the body still ended with a `## Change Rationale` section. Both are now moved to this changelog. No definitional content changed, aside from one small addition: a cross-reference tying Composition Depth as a Decomposition Signal to `system.md`'s Responsibility coherence test and `modularity.md`, which the document's own argument already matched without citing either.

#### Rationale and alternatives
Considered adding a connection between Method's owner/influencing/influenced reframing and Agency, on the theory that "owner" is shared vocabulary between the two documents. Rejected on inspection: Method's owner is about which type a callable behavior is structurally attached to, not about who is responsible for or delegates an action — the two documents use the same word for genuinely different concepts, and forcing a connection between them would be exactly the kind of unforced, decorative cross-referencing this project's review has been trying to avoid, not the kind that resolves real duplication or drift.

---

### Correct static/instance dispatch enforcement and clarify influencing/influenced code smell
- Time: 2026-08-27T00:00:00Z
- Type: Fixed
- Cited:
  - [Khayyam — Programming Language](./khayyam.md) — Depends_on: the new Separation of Syntax and Governance principle that classifies “which entity a call targets” as syntax
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: clarified that `CF.Return` mid-method is not automatically a smell and that an influencing→influenced transition is a code-smell nudge, not a language error
  - [Super Z](../CONTRIBUTORS.md#super-z) — rewrote: content below

#### Summary
Corrects `Method Invocation Rules` from “enforced strictly at the tooling/linter layer” / “flagged as an error” to “enforced by the compiler” / “is a compile-time error” — dispatch determines which entity a call targets (`what exists`), so it belongs to syntax under the Separation principle; the linter may add additional diagnostics. Keeps the future linter rule for flagging an influencing variable that receives a mutating call, and treats an influencing→influenced transition in one call as an organizational code-smell to be flagged and refactored (e.g., return an error and let the caller `Close()` the `net.Conn`), not as a language-level error.
