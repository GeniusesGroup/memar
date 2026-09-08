# Polymorphism in Khayyam Changelog

## Changelog

### Initial creation and container-content consolidation
- Time: 2026-07-11T00:00:00Z
- Type: Added
- Cited:
  - [Abstraction in Khayyam](./khayyam-abstraction.md) — Extends: supplies the abstraction type and its mechanics; this document classifies the polymorphism it enables and the syntaxes Khayyam rejects.
  - [Protocol](./protocol.md) — Depends_on: defines Protocol as a pure declarative specification used to explain why abstractions carry no behavior.
  - [Type](./type.md) — Depends_on: the type model defines the concepts and categories on which polymorphism operates.
  - [Explicit Behavior Ownership](./type.md#explicit-behavior-ownership) — Depends_on: its requirement for a single visible behavior owner grounds the rejection of generic type-parameter syntax.
- Propagates to:
  - [Khayyam — Programming Language](./khayyam.md#abstraction): Done — the canonical Abstraction section reflects the abstraction mechanism on which this document builds.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed
  - [Gemini](../CONTRIBUTORS.md#gemini) (3.1 pro, extended thinking) — drafted
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) (GPT-5.5, medium effort) — critically reviewed
  - [Claude](../CONTRIBUTORS.md#claude) (claude-sonnet-5, extended thinking) — researched and rewrote
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM, medium effort) — merged

#### What changed
- The polymorphism document was created, consolidating the former container/generics-elimination material (Gemini — drafted the original containers/generics-elimination material and its alternatives; Super Z — merged, preserving the former containers-without-generics document's detail in this document).
- The resulting specification defines abstraction conformance and extension, Smart Compilation dispatch, domain-specific containers, the rejection of generic syntax, overloading, and coercion, together with their rationale, prior art, and open questions.
- Abstraction-conformance polymorphism, and abstraction extension and subtyping, were defined (Omid Hekayati).
- The Strachey/Cardelli–Wegner taxonomy was researched, Khayyam mechanisms were mapped to it, and prior-art comparisons and open questions were developed (Claude).

#### Deliberation
- The domain-specific-container alternative was defined (Omid Hekayati).
- The anemic-domain-model argument against generic syntax was claimed (Omid Hekayati).
- The closed-versus-open type-parameter analysis was contributed (Claude).

---

### Migration to the current Explanation-facet structure
- Time: 2026-08-19T00:00:00Z
- Type: refactor
- Cited:
  - [Documentation — Explanation](./documentation-explanation.md) — Depends_on: defines the current front matter, top-level body sections, and topic-first organization.
  - [Documentation — Changelog](./documentation-changelog.md) — Depends_on: defines this companion file as the home for migrated provenance and change history.
  - [How to make a new explanation document](./documentation-explanation.practice.md) — Reference: supplies the revision procedure applied in this migration.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) (GPT-5.6) — rewrote

#### What changed
- The base document was migrated from the retired `Summary` / `Guide-level explanation` / `Reference-level explanation` structure to `Abstract`, `Introduction`, `Explanation`, `Results`, and `Discussion`.
- Provenance moved out of front matter: historical citations, contributor information, and propagation tracking are preserved here instead; this companion changelog was created.
- The EBO prerequisite moved into Introduction as an explicit constraint.
- Global discussion categories nested under one `Discussion` section.
- The stale Variable-document anchor for explicit typing repaired.
- The detailed explanatory, analytical, prior-art, and open-question content remains intact.

#### Deliberation
- The same up-to-date documentation migration applied to the Variable document was requested (Omid Hekayati).

---

### Fix example naming and annotate dual-role call
- Time: 2026-08-27T00:00:00Z
- Type: Fixed
- Contributors:
  - [Super Z](../CONTRIBUTORS.md#super-z) — rewrote

#### What changed
Corrects `tp hash`/`tp salt` to `tp Hash`/`tp Salt` per the PascalCase convention and `UInt64`/`UInt32` to `W64`/`W32` per the `W`/`R` capsule naming in sibling documents (also `h.hash` → `h.Hash`). Annotates the `ConnectionList` example's `self.container.Add(conID, con) (con, err)` call where `con` occupies both roles — influencing in `(conID, con)` and influenced in `(con, err)` — as an exhibit of the open dual-role question in `khayyam-method.md`; no settled notation exists yet.
