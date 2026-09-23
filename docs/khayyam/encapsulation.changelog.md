# Encapsulation in Khayyam Changelog

## Changelog

### Created
- Time: 2026-07-15T00:00:00Z (approximated from Start Date)
- Type: Added
- Cited:
  - [Khayyam - Programming Language](./khayyam.md) — Reference: The canonical specification defines capsule, method, and abstraction syntax that this document elaborates and motivates.
  - [Khayyam Design Philosophy](./khayyam-design_philosophy.md) — Reference: The philosophy document recorded the recurring principles (behavior over type identity, domain modeling, syntactic atomicity) underpinning the encapsulation design decisions recorded here. *(That document has since been fully retired and deleted; its content was absorbed into khayyam.md and khayyam-abstraction.md — see khayyam.changelog.md. This citation is preserved as historical provenance only.)*
  - [Abstraction in Khayyam](./abstraction.md) — Reference: The abstraction mechanism is specified separately. This document records the encapsulation guarantees (capsules hide all internal state, all interaction occurs through methods) that make the abstraction model possible.
  - [Polymorphism in Khayyam](./polymorphism.md) — Reference: Polymorphism classification and dispatch strategy are specified separately. This document defines the capsule-level boundaries that constrain polymorphic behavior.
  - [Method in Khayyam](./method.md) — Reference: Method as Callable Capsule — the mechanical spec of the method signature itself (pass-by-reference, parenthesized separation, static-vs-instance invocation, body-less methods) — previously lived in this document's Explanation section and has moved there, since a capsule is an abstraction over `vr`/`mt`, not the other way around. This document now depends on that spec rather than restating it.
  - [Control Flow in Khayyam](./control_flow.md) — Reference: The Code Scope (`sc`) topic previously lived in this document's Explanation section and has moved there, since code scopes are structurally the mechanism control-flow libraries (IF/ELSE/LOOP) are built on, not a capsule-level concern.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed
  - [ChatGPT](../../CONTRIBUTORS.md#chatgpt) (GPT-5.5, medium effort) — critically reviewed
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM 5.2, medium effort) — rewrote
  - [Claude](../../CONTRIBUTORS.md#claude) (claude-sonnet-5, medium effort) — rewrote

#### What changed
- Initial creation as the authoritative document for Khayyam's encapsulation model.
- The capsule structure and method model were defined, along with the elimination of consumer-side mutability keywords in the canonical Khayyam specification (Omid Hekayati).
- Scattered encapsulation-related content was restructured into the canonical document template and consolidated from staging and specification files (Super Z).
- Reference-level elaborations were added on capsule structure, method dispatch, abstraction design, and primitive capsule specification (Super Z).
- The document structure was migrated to the current Explanation-facet specification (Claude).
- The standalone Absence of Closures and Anonymous Functions document was merged into the Explanation section as a topic following Method as Callable Capsule (Claude).
- Method as Callable Capsule was extracted to khayyam-method.md and Code Scope to khayyam-control_flow.md (Claude).
- Absence of Closures and Anonymous Functions was reframed from a negative ("we don't support X") framing to a positive one — closures as an implicit-capsule syntax we chose not to admit, and why (Claude).

#### Deliberation
- The original design decisions and the Sovereign Encapsulation concept were claimed (Omid Hekayati).
- The extraction of Method as Callable Capsule and Code Scope from this document rested on capsule being an abstraction over `vr`/`mt`, not the reverse (Claude).

### Positive reframing of closures
- Time: 2026-07-15T00:00:00Z (approximated; original time not recorded — relative order derived by reversing the base document's newest-first `Change Rationale` listing)
- Type: Changed
- Contributors: not recorded per-change in the source section

#### What changed
"Absence of Closures and Anonymous Functions" renamed to "Closures as Implicit Capsule Syntax" and its opening reframed: rather than starting from "Khayyam does not support closures," it now starts from the structural observation that a closure already *is* an implicit, unnamed capsule, and that Sovereign Encapsulation's existing requirement (state must be named and explicit) is sufficient on its own to explain why this syntax was not admitted — no separate prohibitive rule is needed. The Discussion subsections (Drawbacks, Rationale and alternatives, Prior art) were left unchanged, since the case they make does not depend on which framing introduces the topic. Cross-reference links elsewhere in this document were updated to the new heading.

### Extraction of non-capsule content
- Time: 2026-07-15T00:00:00Z (approximated; original time not recorded)
- Type: refactor
- Contributors: not recorded per-change in the source section

#### What changed
A capsule is an abstraction layered over `vr` and `mt`, not an independent primitive — so content specific to those underlying concepts should be defined in their own documents and only referenced here. Accordingly: "Method as Callable Capsule" (including its Method Invocation Rules and Body-less Methods subsections) moved to [Method in Khayyam](./method.md); "Code Scope" moved to [Control Flow in Khayyam](./control_flow.md), since `sc` is structurally the mechanism control-flow libraries are built on rather than a capsule-level concern. The Abstract and front-matter Citations were updated to reference both documents instead of restating their content.

### Closures merge
- Time: 2026-07-15T00:00:00Z (approximated; original time not recorded)
- Type: Added
- Contributors: not recorded per-change in the source section

#### What changed
Merged the standalone "Absence of Closures and Anonymous Functions" document into `Explanation` as a new topic, placed immediately after "Method as Callable Capsule," on the grounds that it is a direct corollary of Sovereign Encapsulation rather than an independent rule. All original content (summary, motivation, guide- and reference-level explanation, and the full Discussion bundle) was preserved; only the internal headings were removed as part of folding it into the topic-plus-Discussion shape. The document-wide `Discussion > Drawbacks` and `Rationale and alternatives` were extended with one clause each to reflect the newly merged topic. The standalone file has been retired.

### Structural migration
- Time: 2026-07-15T00:00:00Z (approximated; original time not recorded)
- Type: refactor
- Contributors: not recorded per-change in the source section

#### What changed
Brought the document in line with the current Explanation-facet specification (`documentation-explanation.md`): `Summary` renamed to `Abstract`; `Motivation` moved under a new `Introduction` wrapper alongside an (empty) `Methodology`; the former `Guide-level explanation` promoted to a named, first-listed `Explanation` topic ("Capsules and Methods at a Glance") and linked from the Abstract as "Guide"; the `Reference-level explanation` heading removed, its topics now sitting directly under `Explanation`; added an empty `Results` section per the fixed body-section order.

### Absorbed variable-mutability content
- Time: 2026-07-31T00:00:00Z (date recorded in the source listing; time approximated)
- Type: Added
- Contributors: not recorded per-change in the source section

#### What changed
The "Mutability Is a Type Concern, Not a Variable Concern" section was removed from `khayyam-variable.md` (2026-07-31 review) because it was framed entirely as negation and because the underlying rule is not variable-specific — a capsule's own fields need the identical rule. Its substance was folded into [Sovereign Encapsulation](./encapsulation.md#sovereign-encapsulation) as a generalization from capsule-level to reference-level (variables and fields alike): the "ill-posed question" framing, the conflation-of-concerns rationale, and the Rust `let`/`mut` prior-art detail were merged into the existing paragraphs rather than kept as a separate topic. One gap the removed text also left open was surfaced explicitly as a new unresolved question: whether a reference itself (not the instance it points to) can be rebound after initial assignment.

### Resolved field-rebinding question; clarified primitive-capsule inlining; documented rejected closure alternative
- Time: 2026-08-01T00:00:00Z (date recorded in the source listing; time approximated)
- Type: Changed
- Contributors: not recorded per-change in the source section

#### What changed
Three points raised in review (2026-08-01): (1) the reference-rebinding unresolved question was split — resolved for capsule fields (field rebinding is definitionally the same event as field mutation, gated by the same method-only-access rule; obtaining the new instance still requires a constructor or an explicit copy/clone abstraction per `khayyam-variable.md`'s Domain-Driven Arithmetic) and scoped out to `khayyam-variable.md` for bare local variables; (2) the Primitive Capsule Specification topic was clarified to state explicitly that inlining is a backend optimization orthogonal to "all interaction occurs through methods," that the listed behavioral guarantees are illustrative rather than mandatory, and that the cost/safety tradeoff for a given primitive capsule (e.g. `W32`) is local to that capsule's own design rather than a language default — resolving an apparent tension between the "zero-cost" framing and the guarantees discussion; (3) the Closures rationale gained a documented-and-rejected alternative (a lighter explicitly-captured inline syntax short of a full capsule declaration), added for completeness though the underlying design decision was not reopened.

### Fully resolved reference-rebinding; named representation exposure as a permanent, unclosable limitation
- Time: 2026-08-01T00:00:00Z (date recorded in the source listing; time approximated)
- Type: Changed
- Contributors: not recorded per-change in the source section

#### What changed
Further review (2026-08-01) closed the reference-rebinding question at both levels rather than leaving the local-variable half deferred: since Khayyam has no primitive types, obtaining any new instance — for a variable or a field — always goes through that type's own constructor or copy/clone contract, and local-variable rebinding touches no capsule's private state to begin with, so no invariant was ever at risk. Separately, the storage-aliasing unresolved question was split into two distinct cases: genuine low-level memory aliasing (still deferred to future memory-management documents, where an ownership/borrow-tracking policy could plausibly help) versus "representation exposure" — a capsule's own method surface returning a reference to a sub-capsule (or exposing an `unsafe` accessor) that itself has a wider mutation surface than intended, letting a caller bypass the outer capsule's control entirely through the sub-capsule's own legitimate, honestly-declared contract. This second case is documented as permanently unclosable by any compiler or linter policy — it is not a type-soundness gap but an architectural discipline question resting entirely on each capsule author's choice of how narrow a return type to expose, analogous to "representation exposure" / defensive-copying discussions in other OOP languages.

### Completed migration to the Explanation-facet specification
- Time: 2026-08-26T00:00:00Z
- Type: refactor
- Cited:
  - [Documentation](../documentation.md) — Reference: facet meta-layer defining Explanation/Practice/Changelog.
  - [Documentation — Explanation](../documentation-explanation.md) — Depends_on: governing structure the base document was brought fully in line with.
  - [Documentation — Changelog](../documentation-changelog.md) — Depends_on: entry structure used for this companion file.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — migrated

#### What changed
Completed the migration an earlier pass had started (this document already followed most of the current structure). Remaining steps done here: relocated all remaining provenance out of the base document — front-matter `Applied to`, `Citations`, and `Contributors` moved into this file's entries above (the citation to the retired `khayyam-design_philosophy.md` is preserved with a retirement annotation); the body's former `## Change Rationale` section became the dated entries above, ordered oldest-first by reversing its newest-first listing; the empty `### Methodology` heading was removed per the specification ("unused items are simply omitted, not left as empty headers"); and the empty `Results` section received the standard placeholder sentence used across sibling documents. No prose was summarized or shortened anywhere in the base document — all topics, examples, and Discussion bundles are verbatim. No design decision changed.

#### Deliberation
- Full migration to the latest documentation method, without any summarizing, was requested (Omid Hekayati).

### Second migration wave: `## Discussion` retired per the finalized method
- Time: 2026-09-08T00:00:00Z
- Type: refactor
- Propagates to:
  - khayyam-encapsulation.handoff.md: Created - open questions and anticipated work moved there.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) - requested
  - [OpenCode](../../CONTRIBUTORS.md#opencode) (qwen3.8-flash) - moved

#### What changed
- The body's fixed top-level sections are now Abstract, Introduction, Explanation, Results only; the document-level `## Discussion` and every topic-level `#### Discussion` wrapper were dissolved, and no Drawbacks, Rationale and alternatives, Prior art, Unresolved questions, or Future possibilities heading remains anywhere in the body.
- Genuine current-state cost claims stayed inline as folded paragraphs at the claims they qualify (Sovereign Encapsulation, Capsule Structure and Privacy, Closures as Implicit Capsule Syntax, Tuples Rejection, Primitive Capsule Specification, Constants as Capsule-Returned Values), together with the closures topic's "Reduced Optimization Surface" rationale paragraph and the two settled former unresolved questions — representation exposure as a permanent limit of the method-contract guarantee, and reference rebinding as no gap at either level — folded into Sovereign Encapsulation.
- The document-level Naming Conventions list graduated into `Explanation` as its own topic.
- Rejected alternatives (every topic-level and the document-level Rationale and alternatives) and the document-level Drawbacks are recorded below under Considered and not done; every topic-level and the document-level Prior art section is recorded below under Related work.
- Open questions (one from Sovereign Encapsulation, three from Primitive Capsule Specification, two from Constants as Capsule-Returned Values, two document-level) and anticipated work (the trivial-getter linter mode from Capsule Structure and Privacy, the primitive-capsule specification document from Primitive Capsule Specification, the standard-capsule library from document level) moved to the newly created paired handoff [khayyam-encapsulation.handoff.md](./encapsulation.handoff.md).
- Final audit pass: the Introduction's self-description no longer promises that the body records the alternatives considered and rejected; they are recorded in this entry's Considered and not done.

#### Considered and not done
- **Consumer-side `mut`/`const` mutability keywords (rejected; migrated from the Sovereign-Encapsulation topic's retired Rationale and alternatives)**: they allow behavior overrides at the call site that bypass the domain model's own invariants, and they add a constant low-grade decision burden to every variable declaration; they also conflate two distinct concerns Khayyam keeps separate — the identity of a reference (a variable or a field, which simply names a relationship to an instance) and the behavioral contract of the referenced instance (owned entirely by its type).
- **Allow selective field exposure, as in C# properties or Rust `pub` fields (rejected; migrated from the Capsule-Structure-and-Privacy topic's retired Rationale and alternatives)**: creates a two-tier system where some fields are public and others are private, with no principled rule for which should be which, and breaks the guarantee that a capsule's entire contract is discoverable through its method interface.
- **Allow friend/internal visibility, as in C++ or Java package-private (rejected; migrated from the same topic)**: introduces scope-based exceptions that weaken the encapsulation guarantee and create implicit coupling between files or modules.
- **A lighter, explicitly-captured inline syntax that lists captured state in the signature itself, short of a full named-capsule declaration (considered; rejected; migrated from the Closures topic's retired Rationale and alternatives)**: it would have kept captures explicit (addressing the hidden-dependency objection) while reducing ceremony, but once captured state must be written out explicitly at the call site the result is structurally indistinguishable from a small named capsule — the same fields, the same single method — and the only thing such syntax would save is the act of typing a name for it; since the friction the design accepts is naming and defining a type, not the mechanics of expressing fields or a method body, it does not address the actual source of the friction it targets and would add a second, redundant way to express what a capsule already expresses.
- **Tuple types, the conventional approach in Go, Rust, Python, and many other languages (rejected; migrated from the Tuples-Rejection topic's retired Rationale and alternatives)**: their positional, anonymous nature allows unnamed structural grouping of values without introducing a domain identity; while tuple types are a valid construct in formal type theory, in architectural modeling they serve as a primitive form of encapsulation — one that provides state grouping without ownership, without behavior, and without identity — a combination that facilitates the gradual emergence of anemic domain models, where data and behavior become separated across the codebase.
- **Primitive capsules as pure renames with no behavioral guarantees (rejected; migrated from the Primitive-Capsule-Specification topic's retired Rationale and alternatives)**: would make the "de-Primitive-ing" migration trivially zero-cost but would also make it meaningless — a rename without behavioral difference adds no value.
- **Primitive capsules with full behavioral specifications (Khayyam's apparent intent — the direction taken, recorded here as the considered alternative; migrated from the same topic)**: makes the migration more valuable but requires explicit specification of each primitive capsule's behavioral guarantees.
- **Dedicated `const` keyword, the conventional approach in most languages (rejected; migrated from the Constants-as-Capsule-Returned-Values topic's retired Rationale and alternatives)**: would reintroduce a consumer/producer-side modifier that Khayyam otherwise eliminates entirely in favor of behavior being intrinsic to the capsule; a dedicated `const` keyword was already rejected at the consumer side, and this addressed the producer side — how a value that should never change after initialization is expressed without introducing a separate keyword category.
- **`constexpr`/`comptime` keyword, as in C++ or Zig (rejected; migrated from the same topic)**: while closer in spirit to Khayyam's "constant as a compile-time function" framing, these still introduce a separate keyword category rather than making the behavior intrinsic to the capsule's method design.
- **Allow public fields for simple data carriers (rejected; migrated from the retired document-level Rationale and alternatives)**: would create a two-tier system where some capsules have public fields and others don't, with no principled rule for which should be which, and would break the guarantee that a capsule's entire contract is its method interface.
- **Allow tuples for "simple" multi-value returns (rejected; migrated from the same section)**: the boundary between "simple" and "complex" is subjective; once tuples are allowed for simple cases, they tend to proliferate to complex cases where they obscure domain meaning.
- **Allow consumer-side `const` for read-only references (rejected; migrated from the same section)**: the full rationale lives with the Sovereign Encapsulation decision — see [Sovereign Encapsulation](./encapsulation.md#sovereign-encapsulation).
- **Allow closures for simple, single-use callbacks (rejected; migrated from the same section)**: the full rationale lives with the closures decision — see [Closures as Implicit Capsule Syntax](./encapsulation.md#closures-as-implicit-capsule-syntax).
- **The model's aggregate cost in named types and method definitions (recorded from the removed document-level Drawbacks section; the audit-side counterpart to the per-topic cost claims that stayed inline at their claims)**: the encapsulation model's insistence on method-only interaction, no tuples, no closures, and no consumer-side mutability keywords creates a codebase with more named types and more method definitions than virtually any mainstream language; for simple data structures (a 2D coordinate, a key-value pair, a result type) or simple one-off behaviors (a sort comparator, a callback), the developer must define a named capsule with named fields and explicit methods, rather than using a tuple, a struct with public fields, or a closure; this is the price of guaranteed domain integrity and encapsulation — but it is a real price, and it is felt most acutely during rapid prototyping or when writing glue code between systems.

#### Related work
- Mutability prior art (migrated from the Sovereign-Encapsulation topic's retired Prior art): Rust's `mut`, C++'s `const`, TypeScript's `readonly` all place mutability responsibility at the consumer site; Rust's `let mut` is the closest single-keyword prior art at the declaration-site level, but it conflates several distinct concerns — binding, ownership, and mutation — into one modifier, which Khayyam keeps separate by never letting a reference declaration (variable or field) carry mutation semantics at all; Smalltalk-style strict message-passing encapsulation (no public fields at all) is closer to Khayyam's model.
- Field-privacy prior art (migrated from the Capsule-Structure-and-Privacy topic's retired Prior art): Smalltalk's object model (all instance variables are private, all interaction is through messages) is the closest prior art; Go's struct model with uppercase/lowercase visibility is a weaker form that still allows direct field access for exported fields.
- No-lambda prior art and its real-world cost (migrated from the Closures topic's retired Prior art): Java's pre-Java-8 model (no lambdas, only anonymous inner classes) followed the same philosophy Khayyam follows here, and it is informative evidence about the real-world cost of this constraint — the resulting boilerplate for simple, single-use callbacks (event listeners, one-off comparators) was significant enough that Java eventually added lambda expressions in Java 8 under sustained developer pressure.
- Dual-path usage evidence (migrated from the same topic): Go's standard `net/http` package offers two parallel ways to register a request handler for the same need — a closure-based form, `func HandleFunc(pattern string, handler func(http.ResponseWriter, *http.Request))`, and a capsule/struct-based form, `func Handle(pattern string, handler Handler)`. In practice, when both paths exist side by side, developers consistently default to the closure-based path, and encapsulation suffers in both forms regardless: `pattern` ends up living outside the handler type rather than being owned by it. This is read as evidence that offering closures alongside a capsule-based alternative does not lead to better modeling — it leads to the closure path being taken by default, with the encapsulation discipline silently degraded. Removing the closure path entirely is treated as a deliberate forcing function rather than an oversight, precisely because this dual-path failure mode is observed in real, widely-used code rather than hypothesized.
- Tuple prior art (migrated from the Tuples-Rejection topic's retired Prior art): Go's multiple return values, Rust's and Python's tuple types, and TypeScript's tuple types are all common prior art for this feature; Khayyam's rejection is closer in spirit to strongly nominal-typing-oriented languages and to general DDD advice discouraging "primitive obsession" and anonymous data bags.
- Primitive-integer prior art (migrated from the Primitive-Capsule-Specification topic's retired Prior art): Zig's integer types include comptime range checks and overflow semantics; Rust's integer types distinguish between wrapping (`wrapping_add`), checked (`checked_add`), and saturating (`saturating_add`) operations through methods, not through separate types; Ada's range types are closer to Khayyam's model of encoding range semantics in the type itself.
- Constant prior art (migrated from the Constants-as-Capsule-Returned-Values topic's retired Prior art): most languages provide an explicit `const`/`final`/`let` keyword; Khayyam's "constant as a compile-time function" framing is conceptually close to `constexpr` functions in C++ or `comptime` values in Zig, though without a dedicated keyword marking them as such.
- Document-level prior art (migrated from the retired document-level Prior art): Smalltalk's strict message-passing encapsulation (no public fields, all interaction through messages) is the closest mainstream prior art for the capsule model; prior art for abstractions and polymorphism is documented in their respective documents.

---

### Requested accessor generation is explicit source, not a public surface
- Time: 2026-09-15T09:00:00Z
- Type: Changed
- Cited:
  - [Linter](../protocols/linter.md) — Consumed contract: assistance writes source on request.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided (rule home is the subject's document)
  - [Grok](../../CONTRIBUTORS.md#grok) (Grok 4.6 via Cursor) — applied

#### What changed
- Capsule Structure and Privacy now states that a linter or companion generator MAY write `get`/`set` methods into explicit source when requested, and MUST NOT synthesize a public surface the author never asked for — content relocated from the retired Khayyam-shelf linter document.


---

### Bare name in a capsule body recorded as an open production
- Time: 2026-09-23T08:43:30Z
- Type: Fixed
- Cited:
  - [abstraction_p.Implements](../protocols/abstraction-implements.md) — Reference: the `ErrServiceNotFound` example places a bare `Implements` in a `cp` body.
  - [Metaprogramming in Khayyam](./metaprogramming.md) — Reference: the `UserRecord` example places a bare `Structural` in a `cp` body.
- Propagates to:
  - khayyam.md: Done — the capsule bullet states the same one-token composition line.
- Contributors:
  - [Grok](../../CONTRIBUTORS.md#grok) (Grok 4.7 via [Cursor](../../CONTRIBUTORS.md#cursor)) — reviewed, applied

#### What changed
- A one-token line in a capsule body is a bare abstraction name. The capsule composes that abstraction, on the same shape an `ab` block uses. The line allocates no state. What the composition requires is defined by the named abstraction. The `Implements` and `Structural` examples are that line.

#### Considered and not done
- **Leaving the one-token line unspecified (rejected)**: those examples were already the language's own illustrations of composing an abstraction into a capsule. A field line is two tokens; the one-token line is the composition form.

---

### A field-shaped value is one type plus one generator-facing method
- Time: 2026-09-23T10:20:00Z
- Type: Fixed
- Cited:
  - [abstraction_p.Implements](../protocols/abstraction-implements.md) — Depends_on: the author states implementation intent; a generator writes the method bodies.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Grok](../../CONTRIBUTORS.md#grok) (Grok 4.7 via [Cursor](../../CONTRIBUTORS.md#cursor)) — applied

#### What changed
- The `Field_UserUUID` procedure — one type, one method naming what a code generator implements — is in [Khayyam practice](./khayyam.practice.md), not in this document. This document keeps the language rule: access to a field is a method, and a generator may write those methods into source when requested.

#### Considered and not done
- **A hand-written pair of abstractions for every field (rejected)**: that repeats the generator's job in every file. The author names the intent once (Omid Hekayati — decided).
