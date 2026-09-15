# Linter Changelog

## Changelog

### Fix field-access enforcement wording; add suggested type-as-argument and event-abstraction rules
- Time: 2026-08-27T00:00:00Z
- Type: Fixed
- Cited:
  - [Encapsulation in Khayyam](./encapsulation.md) — Depends_on: Sovereign Encapsulation that makes fields structurally private
  - [Control Flow in Khayyam](./control_flow.md) — Depends_on: the compiler-event abstraction that analysis libraries subscribe to
  - [Method in Khayyam](./method.md) — Reference: `sc`/`mt` as argument positions
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested, clarified
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote

#### What changed
Corrects `Boilerplate Generation`: direct field read/write outside the capsule’s own methods is a **linter error** (previously misworded as “compiler throw compile error”); the compiler already makes fields structurally private. Adds two new suggested-rule sections (current state, not historical): `Type-as-Argument for `sc`/`mt`` — syntax allows a variable or, for `sc`/`mt`, the type itself as a type-level argument (compiler distinguishes from the expected type in the callee’s signature without ambiguity); linter should flag a bare type where a capsule/abstraction value is expected and discourage `mt`-as-value in closure style. And `Compiler Event Abstraction for Analysis` — the compiler emits `sc` entry/exit and jump events; DAA/linter should treat `sc` as the common denominator, not `IF` names. Both are *suggested* diagnostics, not language-level restrictions. For closure-style `mt` values, the existing discouragement is kept via the linter, consistent with `Closures as Implicit Capsule Syntax`.

#### Deliberation
- Restricting at language level which types are meaningful as type-arguments was clarified as unnecessary (Omid Hekayati — clarified).
- Influencing→influenced transitions were clarified as organizational nudges (Omid Hekayati — clarified).

#### Considered and not done
- **Restrict at language level which types may be passed as type-arguments (rejected)**: keep syntax generic, put meaningfulness in linter.

---

### Migrate to the Explanation-facet structure
- Time: 2026-08-30T00:00:00Z
- Type: refactor
- Cited:
  - [Documentation — Explanation](../documentation-explanation.md) — Depends_on: the structure this migration follows — YAML front matter, the `Abstract → Introduction → Explanation → Results → Discussion` body, and the per-topic Discussion pattern — is that specification's, applied to this document for the first time.
  - [Khayyam - Programming Language](./khayyam.md) — Reference: *Separation of Syntax and Governance*, which supplies the framing for the new Abstract, Motivation, and Discussion content — the linter is where governance lives, so this document's implementer-facing framing leans on that principle more heavily than its two siblings do.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested, clarified
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote

#### What changed
This document is now structured per `documentation-explanation.md`: YAML front matter added (Status: Proposed; Start Date 2026-06-22 from the file's first commit; ID 495025 — ordered after `khayyam-compiler.md`'s 495024, which shares the same Start Date, per the ID spec's retroactive-numbering provision); Abstract, Motivation, per-topic Discussion sections, Results, and a document-wide Discussion added. New framing topic `Suggested Diagnostics` groups the diagnostics that are explicitly *not* language restrictions (the former `Linters`, `Type-as-Argument for sc/mt`, and `Compiler Event Abstraction` sections) under one heading that states their shared character; `Boilerplate Generation` stays a separate topic. No rule content was removed: Auto-Folding (MUST) and Structural Overview (SHOULD), the Orphan Rule with its local/distant-type distinction and composition escape hatch, getter/setter generation, the linter-error-not-compiler-error field-access wording, type-as-argument meaningfulness, and `sc`-as-common-denominator for DAA are all preserved. The new Discussion content is derived from Khayyam's own philosophy documents rather than new design decisions — in particular, the guard against the linter quietly becoming a second compiler, and the recognition that this document concentrates responsibilities other languages give their compiler (the safety trade-off already acknowledged in `khayyam-control_flow.md` and `khayyam-memory_model.md`). New open questions recorded: per-rule classification of MUST-defaults vs. suggested; the Orphan Rule's boundary unit (directory vs. repository vs. declared ownership); the promotion path for suggested diagnostics.

#### Deliberation
- Migration of this document and its two sibling tooling documents to the latest documentation methodology was requested (Omid Hekayati — requested).
- The framing constraint that governs the new sections was clarified: none of the three tooling documents may impose anything on Khayyam itself, since together they are recommendations to each component's developers about how Khayyam's own thinking should find concrete manifestation (Omid Hekayati — clarified).

#### Considered and not done
- **Split IDE behavior (folding) into a separate IDE-directives document (considered during the migration, rejected)**: the folding rules are governance-of-reading-order, the same subject as the rest of this document, and no second implementation exists yet that would need its own document — splitting now would be structure ahead of a real need, the mistake the methodology warns against.
- **Deduplicate the getter/setter content that existed in both `Boilerplate Generation` and the former `Linters` section (considered, not chosen)**: both topics were kept; the field-access enforcement statement was moved to the `Linters` bullet only, with `Boilerplate Generation` linking forward rather than restating it.

---

### Second migration wave: `## Discussion` retired per the finalized method
- Time: 2026-09-08T00:00:00Z
- Type: refactor
- Propagates to:
  - khayyam-linter.handoff.md: Created - open questions and anticipated work moved there.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) - requested
  - [OpenCode](../../CONTRIBUTORS.md#opencode) (qwen3.8-flash) - moved

#### What changed
- Every `Discussion` wrapper is dissolved — the four per-topic wrappers (IDE Behavior & Visual Formatting, Cross-file Methods — The Orphan Rule, Boilerplate Generation, Suggested Diagnostics) and the document-level `## Discussion`; the body now carries only the fixed top-level sections Abstract, Introduction, Explanation, Results.
- Each topic's Drawbacks stayed inline at the claims they qualify: the folding rules depend on fold-state persistence and per-project overrides as mitigations; the Orphan Rule carries its monorepo-boundary and import-graph-resolution costs; Boilerplate Generation carries the accessor-surface-accumulation cost; Suggested Diagnostics carries the tier's revision-or-retraction posture.
- The document-level Drawbacks — safety guarantees resting on linter configuration with no language-level fallback, a cost accepted knowingly under Separation of Syntax and Governance — are recorded below as the audit record of that acceptance.
- Rejected alternatives from every retired `Rationale and alternatives` block, plus the Orphan Rule's chosen-and-recorded decision, are recorded under Considered and not done below.
- All `Prior art` surveys — per-topic and document-level — are recorded under Related work below.
- Six open questions (fold-state granularity, small-file folding degradation, Orphan boundary unit, setter validation hooks, per-diagnostic compiler/linter classification, boundary-unit configurability) moved to the newly created paired handoff's Open Questions.
- The three document-level Future possibilities items (reference linter configuration, organization-diagnostic extension point, linter conformance suite) moved to the paired handoff's Anticipated Work.
- The Boilerplate Generation chosen alternative ("Linter/IDE-generated on explicit request") is not copied: the body already states it — the topic's MUST-assist-on-request rule and the source-visible, reviewable-accessor rationale restate it verbatim — and its remaining "removes the mechanical cost" content survives in this entry's "Provide no assist" rejection.

#### Considered and not done
- **Leave folding entirely to user preference (rejected as a *default*; migrated from the IDE Behavior & Visual Formatting topic's retired Rationale and alternatives)**: the folded-by-default view is the design's statement of what a file is — contracts and structure first, implementation second. Individual developers may unfold; the default expresses the intended reading order rather than enforcing it.
- **Let the linter warn about over-long import blocks instead (rejected; migrated from the same topic)**: warning changes nothing about reading order; folding solves the actual problem (inclusion bloat crowding out architecture) rather than nagging about it.
- **Language-level restriction, an orphan rule like Rust's, compiler-enforced (rejected; migrated from the Cross-file Methods — The Orphan Rule topic's retired Rationale and alternatives)**: Khayyam's grammar deliberately allows attaching a method to any imported type; hardening the boundary into syntax would move a governance preference into ontology, and organizations with different extension policies would have no escape hatch.
- **Permit external extension freely (rejected as default; migrated from the same topic)**: Monkey Patching breaks the referential trust a reader places in an external library's documented behavior — the same hidden-behavior problem Khayyam's no-magic principles target, arriving through the back door of tooling permissiveness.
- **Linter-enforced with organizational override (chosen; migrated from the same topic as the recorded decision)**: the default protects the common case; an organization that genuinely owns both sides of the boundary can relax it by configuration, making the policy decision visible in the linter config rather than silently available to everyone.
- **Have the compiler auto-generate accessors for all fields (rejected; migrated from the Boilerplate Generation topic's retired Rationale and alternatives)**: synthesizes a public surface the author never declared, weakening Information Hiding by default; a capsule's contract should contain only behavior its author wrote or explicitly requested.
- **Provide no assist (rejected; migrated from the same topic)**: without a generation assist the accessor requirement becomes heavy boilerplate, and boilerplate fatigue is exactly the pressure that produces demands to reopen field exposure — the failure this rule exists to prevent.
- **Promote the suggested diagnostics to language rules (rejected; migrated from the Suggested Diagnostics topic's retired Rationale and alternatives)**: each would either deny existence (ontology — the compiler's side of the line) or harden one organization's flow preference into universal law. The type-as-argument case is the concrete example: the language deliberately leaves which types may be passed as type-arguments unrestricted, keeping syntax generic and placing the meaningfulness rule in tooling.
- **Scatter the suggested diagnostics across the construct documents they relate to (rejected; migrated from the same topic)**: each construct document states its own language-level semantics; collecting the tooling-side diagnostics in one place keeps the governance layer reviewable as a whole, and keeps the construct documents free of implementation advice that could drift from actual linter behavior.
- **Fold tooling rules into the construct documents ([Khayyam](./khayyam.md), [Encapsulation](./encapsulation.md), [Control Flow](./control_flow.md), ...) (rejected; migrated from the document-level retired Rationale and alternatives)**: each construct document states what the language does and why; sprinkling IDE and linter behavior through them would blur the syntax/governance line the documents exist to demonstrate, and would couple language-document stability to tooling decisions that change far more often.
- **Keep linter behavior unspecified (rejected; migrated from the same section)**: governance is the linter's entire job under Khayyam's architecture; leaving it undocumented makes each implementation's policy an accident of whichever team built it, and quietly converts "governance is tunable" into "governance is whatever the default build does."
- **A dedicated document per tool — linter.md, ide.md, lsp.md (rejected for now; migrated from the same section)**: at the current stage the tooling surface is one coherent set of recommendations; splitting it would multiply cross-referencing overhead before there are distinct implementations to govern. Revisit if the IDE and linter concerns genuinely diverge.

#### Considered and not done (from the removed document-level Drawbacks section)
- **Concentrating safety enforcement in the linter leaves no language-level fallback (cost accepted knowingly)** (migrated from the removed document-level Drawbacks): Khayyam's architecture concentrates unusual responsibility in its linter: safety disciplines that other languages enforce structurally (error-inspection, memory-rule adherence, encapsulation etiquette) are only as strong as the linter configuration in force. A team running a weak or disabled linter loses those guarantees with no language-level safety net — a cost accepted knowingly under the Separation of Syntax and Governance, but a real one. These rules also speak for tools that do not yet exist; until implementations mature, the document governs by intention rather than by enforced behavior.

#### Related work
- Code-folding as a default view for structure-first reading is common in IDEs (Visual Studio's region folding, JetBrains' structural collapse), though rarely as opinionated about *what* the default view should teach. The stronger precedent for "contracts before implementation" is interface-first file organization in Go's idiom of reading a file's declarations top-down; the folding rule makes that reading order mechanical rather than customary. (Migrated from the IDE Behavior & Visual Formatting topic's retired Prior art)
- Rust's orphan rule is the closest mainstream mechanism, but it is compiler-enforced — a language-level ontology decision Khayyam explicitly declines to make. Go's prohibition on defining methods on types from other packages is similarly structural. C#'s extension methods and Kotlin's extension functions permit external extension as an ordinary, visible-language feature — evidence that extension itself is not inherently unsafe, but that its *governance* is where the design decision belongs. Khayyam takes the middle path: syntactically free, governed by default. (Migrated from the Cross-file Methods — The Orphan Rule topic's retired Prior art)
- Java's IDE-generated getter/setter convention is the direct precedent, including its well-known failure mode (bean-shaped classes whose encapsulation is nominal). Go's explicit-methods-only culture shows the opposite pole: no generation, maximal ceremony. Khayyam's position is the middle one — generation is available and expected, but each generated method enters the source and the capsule's contract as if hand-written. (Migrated from the Boilerplate Generation topic's retired Prior art)
- Go's `vet` and `staticcheck` occupy the same tier: official-tooling diagnostics that encode community consensus without being language rules. The naming/type-suggestion requirements mirror LSP-based assists in modern IDEs generally. The `sc`-as-common-denominator rule is Khayyam-specific, mirroring the compiler's own event contract (see the compiler-side treatment under [Control Flow via `sc` and Jump Primitives](./compiler.md#control-flow-via-sc-and-jump-primitives)). (Migrated from the Suggested Diagnostics topic's retired Prior art)
- Go is the closest structural precedent: a deliberately minimal language paired with official tooling (`gofmt`, `vet`) that carries community standards the grammar does not. The difference is degree — Go's tooling is conventionally important, while Khayyam's linter is architecturally load-bearing by design, holding responsibilities (safety enforcement, orphan governance) that Go's compiler or Rust's compiler own structurally. This inversion is Khayyam's own; the prior art establishes the pattern, not the weight. (Migrated from the document-level retired Prior art)

---

### Lifted to a language-independent Linter protocol
- Time: 2026-09-15T09:00:00Z
- Type: Changed
- Propagates to:
  - linter.handoff.md: Done — rewritten around rule-authorship notation; Khayyam-specific UX questions kept with new homes named.
  - khayyam.md: Done — type-as-argument and newline/lowering facts stated as grammar; contracts-first reading order named.
  - khayyam/modularity.md: Done — orphan-rule realization.
  - khayyam/encapsulation.md: Done — requested accessor generation.
  - khayyam/method.md: Done — type-level `sc`/`mt` argument grammar.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [Grok](../../CONTRIBUTORS.md#grok) (Grok 4.6 via Cursor) — rewrote

#### What changed
- The document is now the Linter protocol: what a linter is, the compiler/linter split, that a rule lives in its subject's document, required members of a governance rule pending notation, configuration and override, event consumption, and that assistance writes source on request.
- Khayyam-syntax diagnostics left this body: orphan rule to [Modularity in Khayyam](../khayyam/modularity.md), accessor generation to [Encapsulation](../khayyam/encapsulation.md), type-as-argument to [Method](../khayyam/method.md) with a pointer from [Khayyam](../khayyam/khayyam.md), command-newline/lowering to Khayyam. Declaration-block folding stayed here as a general tooling assist ([Tooling may present structure first](./linter.md#tooling-may-present-structure-first)); the Khayyam-specific `tp ... in ...` forms are realization facts of that language's declaration shape, not this protocol.
- Status returns to Draft because the authorship notation is unsettled.
- Title is "Linter"; the changelog heading follows.

#### Deliberation
- Khayyam itself has no special linter rules; the protocol did not previously say how rules are authored (Omid Hekayati — claimed).
- Two aspects stay distinct: how a linter works, and the rules it checks — the latter belong to subject documents (Omid Hekayati — decided).

