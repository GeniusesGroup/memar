# Khayyam Linter & Tooling Rules Changelog

## Changelog

### Fix field-access enforcement wording; add suggested type-as-argument and event-abstraction rules
- Time: 2026-08-27T00:00:00Z
- Type: Fixed
- Cited:
  - [Encapsulation in Khayyam](./khayyam-encapsulation.md) — Depends_on: Sovereign Encapsulation that makes fields structurally private
  - [Control Flow in Khayyam](./khayyam-control_flow.md) — Depends_on: the compiler-event abstraction that analysis libraries subscribe to
  - [Method in Khayyam](./khayyam-method.md) — Reference: `sc`/`mt` as argument positions
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: clarified that which types are meaningful as type-arguments need not be restricted at language level, and that influencing→influenced transitions are organizational nudges
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote: content below

#### Summary
Corrects `Boilerplate Generation`: direct field read/write outside the capsule’s own methods is a **linter error** (previously misworded as “compiler throw compile error”); the compiler already makes fields structurally private. Adds two new suggested-rule sections (current state, not historical): `Type-as-Argument for `sc`/`mt`` — syntax allows a variable or, for `sc`/`mt`, the type itself as a type-level argument (compiler distinguishes from the expected type in the callee’s signature without ambiguity); linter should flag a bare type where a capsule/abstraction value is expected and discourage `mt`-as-value in closure style. And `Compiler Event Abstraction for Analysis` — the compiler emits `sc` entry/exit and jump events; DAA/linter should treat `sc` as the common denominator, not `IF` names. Both are *suggested* diagnostics, not language-level restrictions.

#### Rationale and alternatives
For the type-as-argument placement: (a) restrict at language level which types may be passed as type-arguments (rejected per author preference — keep syntax generic, put meaningfulness in linter); (b) keep syntax generic and document the meaningfulness rule here as a suggested diagnostic (chosen). For closure-style `mt` values: keep the existing discouragement via the linter, consistent with `Closures as Implicit Capsule Syntax`.

---

### Migrate to the Explanation-facet structure
- Time: 2026-08-30T00:00:00Z
- Type: refactor
- Cited:
  - [Documentation — Explanation](./documentation-explanation.md) — Depends_on: the structure this migration follows — YAML front matter, the `Abstract → Introduction → Explanation → Results → Discussion` body, and the per-topic Discussion pattern — is that specification's, applied to this document for the first time.
  - [Khayyam - Programming Language](./khayyam.md) — Reference: *Separation of Syntax and Governance*, which supplies the framing for the new Abstract, Motivation, and Discussion content — the linter is where governance lives, so this document's implementer-facing framing leans on that principle more heavily than its two siblings do.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: migrate this document (and its two sibling tooling documents) to the latest documentation methodology; clarified the framing constraint that governs the new sections — none of the three tooling documents may impose anything on Khayyam itself, since together they are recommendations to each component's developers about how Khayyam's own thinking should find concrete manifestation.
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote: content below.

#### Summary
This document is now structured per `documentation-explanation.md`: YAML front matter added (Status: Proposed; Start Date 2026-06-22 from the file's first commit; ID 495025 — ordered after `khayyam-compiler.md`'s 495024, which shares the same Start Date, per the ID spec's retroactive-numbering provision); Abstract, Motivation, per-topic Discussion sections, Results, and a document-wide Discussion added. New framing topic `Suggested Diagnostics` groups the diagnostics that are explicitly *not* language restrictions (the former `Linters`, `Type-as-Argument for sc/mt`, and `Compiler Event Abstraction` sections) under one heading that states their shared character; `Boilerplate Generation` stays a separate topic. No rule content was removed: Auto-Folding (MUST) and Structural Overview (SHOULD), the Orphan Rule with its local/distant-type distinction and composition escape hatch, getter/setter generation, the linter-error-not-compiler-error field-access wording, type-as-argument meaningfulness, and `sc`-as-common-denominator for DAA are all preserved. The new Discussion content is derived from Khayyam's own philosophy documents rather than new design decisions — in particular, the guard against the linter quietly becoming a second compiler, and the recognition that this document concentrates responsibilities other languages give their compiler (the safety trade-off already acknowledged in `khayyam-control_flow.md` and `khayyam-memory_model.md`). New open questions recorded: per-rule classification of MUST-defaults vs. suggested; the Orphan Rule's boundary unit (directory vs. repository vs. declared ownership); the promotion path for suggested diagnostics.

#### Rationale and alternatives
Considered splitting IDE behavior (folding) into a separate IDE-directives document during the migration. Rejected: the folding rules are governance-of-reading-order, the same subject as the rest of this document, and no second implementation exists yet that would need its own document — splitting now would be structure ahead of a real need, the mistake the methodology warns against. Also considered deduplicating the getter/setter content that existed in both `Boilerplate Generation` and the former `Linters` section; kept both topics but moved the field-access enforcement statement to the `Linters` bullet only, with `Boilerplate Generation` linking forward rather than restating it.
