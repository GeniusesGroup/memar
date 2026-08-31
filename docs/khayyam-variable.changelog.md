# Variable in Khayyam Changelog

## Changelog

### Initial creation and consolidation
- Time: 2026-07-15T00:00:00Z
- Type: Added
- Cited:
  - [Khayyam — Programming Language](./khayyam.md) — Reference: defines the canonical `vr` declaration syntax, `in` inclusion syntax, and logical-reference semantics elaborated here.
  - [Khayyam Design Philosophy](./khayyam-design_philosophy.md) — Reference: provides the self-documenting-code, syntactic-atomicity, and domain-modeling principles used to motivate the variable design. *(That document has since been fully retired and deleted; its content was absorbed into khayyam.md and khayyam-abstraction.md — see khayyam.changelog.md. This citation is preserved as historical provenance only.)*
  - [Type](./type.md) — Depends_on: variables name instances of types, and the type model determines which kinds of type may be referenced.
  - [Encapsulation in Khayyam](./khayyam-encapsulation.md) — Reference: defines the capsule-owned behavioral contract, including the constant model and the rule that mutability is not a variable-level property.
  - [Abstraction in Khayyam](./khayyam-abstraction.md) — Reference: defines the abstraction category that may be named in a variable declaration.
  - [Polymorphism in Khayyam](./khayyam-polymorphism.md) — Reference: specifies dispatch for a variable declared against an abstraction.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed: original variable semantics, including logical references, no assignment operators, and the rejection of privileged primitive types.
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) (GPT-5.5, medium effort) — reviewed: critically reviewed the initial design.
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM 5.2, high effort) — rewrote: consolidated scattered variable content and expanded the declaration, initialization, scope, and inclusion explanations.
  - [Claude](../CONTRIBUTORS.md#claude) (claude-sonnet-5, extended thinking) — reviewed: critically reviewed the resulting document.

#### Summary
Created the variable document and consolidated the design's declaration syntax, explicit-type rule, assignment prohibition, logical-reference model, scope and inclusion mechanism, arithmetic treatment, constants, and deferred resource-lifecycle concerns.

---

### Migration to the current Explanation-facet structure
- Time: 2026-08-19T00:00:00Z
- Type: refactor
- Cited:
  - [Documentation — Explanation](./documentation-explanation.md) — Depends_on: defines the current required front matter, top-level body sections, topic-first organization, and progressive migration rules.
  - [Documentation — Changelog](./documentation-changelog.md) — Depends_on: defines the companion changelog that receives migrated provenance and change rationale.
  - [How to make a new explanation document](./documentation-explanation.practice.md) — Reference: supplies the revision procedure used for this migration.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: requested alignment with the latest documentation methodology without summarizing away existing content.
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) (GPT-5.6) — rewrote: migrated the document to the current Explanation-facet structure; moved historical provenance out of front matter; created this companion changelog; corrected the stale `khayyam-type.md` link to `type.md`; and replaced an empty executable-documentation subtopic with its substantive explanation.

#### Summary
Migrated the base document from the retired `Summary` / `Guide-level explanation` / `Reference-level explanation` layout to `Abstract`, `Introduction`, `Explanation`, `Results`, and `Discussion`. Removed legacy `Citations`, `Contributor(s)`, and `Applied to` front-matter fields and the obsolete `Change Rationale` section; their historical information is preserved here. Existing explanatory topics and their detailed discussion were retained rather than condensed.

---

### Clarify aliasing scope and code-level vs. field-level variable
- Time: 2026-08-27T00:00:00Z
- Type: Fixed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: noted the rebinding discussion belongs at capsule level, not `vr` level, and should be a clarifying nudge only
  - [Super Z](../CONTRIBUTORS.md#super-z) — rewrote: narrowed the aliasing sentence and added the scope-clarification note

#### Summary
Narrows the aliasing claim in `No Assignment Operators` from a broad “eliminates aliasing” to the specific sub-class that `b = a` would create; explicit reference sharing through method parameters remains the intended mechanism (e.g., passing the same `conn` to a registry). Adds a scope-clarification note to `Variable as Logical Reference` distinguishing a code-level `vr x W32` inside a method body from a field `Timeout Duration` inside a capsule — rebinding questions belong to the capsule level (field rebinding *is* mutation, gated by Sovereign Encapsulation), not to `vr` as such.

#### Rationale and alternatives
Alternatives for aliasing wording: (a) keep broad wording (rejected — misleading), (b) soften to “reduces” (rejected — elimination of `b = a` aliasing is total). For the scope note: (a) add a general rebinding rule at `vr` level (rejected per author preference), (b) add only a clarifying nudge distinguishing code-level vs. capsule-level variables (chosen).
