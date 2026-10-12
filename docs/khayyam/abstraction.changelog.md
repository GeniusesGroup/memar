# Abstraction in Khayyam Changelog

## Changelog

### Initial consolidation, superseding two prior drafts
- Time: 2026-07-11T00:00:00Z
- Type: Added
- Cited:
  - [Control Flow in Khayyam](../modules/process/control-flow.md) — Depends_on: this document builds on the precedent set by that document of keeping behavioral policies as ordinary library-driven mechanisms rather than new syntax.
- Propagates to:
  - khayyam.md: Reference — this document elaborates and motivates `khayyam.md#Abstraction`.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed
  - [Gemini](../../CONTRIBUTORS.md#gemini) (3.1 pro, extended thinking) — drafted
  - [Claude](../../CONTRIBUTORS.md#claude) (claude-sonnet-5, medium effort with extended thinking) — reviewed, rewrote
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM, medium effort) — rewrote

#### What changed
- Consolidated all design decisions, resolved policies, and open questions related to the `ab` (abstraction) type in Khayyam into a single authoritative document, superseding two prior drafts ("Intentional Abstraction Satisfaction" and "Rejection of Default Implementations") and merging them with existing DX Scaffolding content.
- Established: abstractions carry no type parameters and no default method bodies; satisfaction is purely structural (no `implements`-equivalent); shared behavior across implementations requires explicit delegation, not inheritance-like defaults; the central open question is whether structural ("accidental") satisfaction is sufficient or whether Khayyam needs an intentional-satisfaction mechanism, with three candidate resolutions identified and none chosen.
- The core abstraction model was defined and the pure-contract philosophy authored (Omid Hekayati).
- The initial draft text was drafted (Gemini).
- The intentional-satisfaction problem statement was drafted (Claude).
- Multiple prior drafts were consolidated into this unified document (Claude).
- The prior drafts' content was merged into this document (Super Z).

#### Deliberation
- The structural-vs-nominal tension was identified (Claude).
- Alternatives were argued for and against (Claude).

---

### Migration to the current documentation methodology, and Behavior Over Type Identity merged in from khayyam-design_philosophy.md
- Time: 2026-08-17T00:00:00Z
- Type: refactor
- Cited:
  - [khayyam-design_philosophy.md] — Depends_on: "Behavior Over Type Identity" and "Reassessment of Parametric Polymorphism" are migrated from that document's Reference-level explanation into this document's Explanation, as part of that document's planned retirement. No stable link is given because that document is slated for removal once its remaining content is redistributed; see this entry's Rationale and alternatives.
- Propagates to:
  - khayyam-agency.md: Done — a related migration ("Khayyam Is Not Its Own Compiler or Runtime") was carried out there in the same review effort; see khayyam-agency.changelog.md.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Claude](../../CONTRIBUTORS.md#claude) — reviewed, rewrote

#### What changed
- This document is now structured per `documentation-explanation.md`: restructured from `Summary/Motivation/Guide-level explanation/Reference-level explanation/Drawbacks/Rationale and alternatives/Prior art/Unresolved questions/Future possibilities` (each a top-level section, with "Unresolved questions" items 4 and 5 themselves containing full nested Drawbacks/Rationale/Prior art/Unresolved-questions blocks — the same kind of structural artifact found and fixed in `modularity.md` earlier in this review) into the current template (`Abstract → Introduction → Explanation → Results → Discussion`).
- A structural artifact — two "Unresolved questions" items that were actually full sub-topics with their own nested Discussion blocks — is resolved by moving their substantive content into Explanation and their actual open questions into this document's own Discussion.
- Former "Unresolved questions" items 4 ("Abstraction Design and Over-Abstraction Risk") and 5 ("Abstraction Stability and Versioning") were moved into the document-level Discussion's own Unresolved questions, since their substantive prose was genuine Explanation-level content, not merely restatements of an open question.
- Front-matter `Citations`, `Contributor(s)`, and `Applied to` were moved into this changelog.
- Every occurrence of "RFC" referring to Memar's own documents was replaced with "document," linking to [Polymorphism in Khayyam](./polymorphism.md) and [Control Flow in Khayyam](../modules/process/control-flow.md) where those documents actually exist, and describing the two now-superseded, absorbed drafts ("Intentional Abstraction Satisfaction," "Rejection of Default Implementations") in plain text without a link, since they no longer exist as separate documents.
- "Behavior Over Type Identity" and "A Note on Parametric Polymorphism" are added, migrated from `khayyam-design_philosophy.md`, which is being retired; this document keeps only the abstraction-satisfaction-relevant portion of that content, since the more general vision-level material in the source document belongs elsewhere. The additions connect the already-present "Pure Contract Philosophy" to the more general principle behind it and to why Khayyam needs fewer of the classic parametric-polymorphism patterns (`identity<T>()`, `swap<T>()`, `Option<T>`, `Result<T,E>`) than languages that motivated them by constraints Khayyam does not have.

#### Deliberation
- This document was asked to be checked for an Agency connection (see khayyam-agency.md's "Agency Beyond Concurrency" topic, added in the same pass) (Omid Hekayati — requested).
- While reviewing it, it was asked for the document to be brought fully up to the current documentation methodology regardless of whether the Agency check changed anything (Omid Hekayati — requested).
- It was separately confirmed that `khayyam-design_philosophy.md` is slated for full retirement, and asked that any of its content transferable to documents already in scope for this review be transferred now rather than lost (Omid Hekayati — confirmed, requested).

#### Rationale and alternatives
Considered migrating "Reassessment of Parametric Polymorphism" to `khayyam-polymorphism.md` instead of here, since it is arguably more about polymorphism mechanics than about abstraction satisfaction specifically, and `khayyam-design_philosophy.md`'s own text names a "dedicated document" for the compilation mechanism this content leads into. Deferred: `khayyam-polymorphism.md` was not supplied for this review, and guessing at its existing content and structure risks duplicating or contradicting something already stated there — the same mistake this review has corrected elsewhere (`modularity.md`'s Protocol paraphrase, this document's own now-corrected structural artifact). Placed here instead, next to the closely related "Pure Contract Philosophy" it elaborates, with a note that `khayyam-polymorphism.md` may be the better long-term home once it can be checked directly.

---

### Corrected: restored full original prose that the previous migration had compressed
- Time: 2026-08-17T00:00:00Z
- Type: Fixed
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — argued
  - [Claude](../../CONTRIBUTORS.md#claude) — rewrote, corrected

#### What changed
- The previous migration entry, despite its own description, had in practice summarized several sections rather than reorganizing them intact — the most serious instance being “Abstraction Validation and DX Scaffolding,” which was replaced with a placeholder note rather than the section's real content. This entry corrects that: the document now carries the full original prose, code examples, and paragraph-level reasoning throughout, reorganized into the current template but not condensed.
- The entire original document was re-read in full before rewriting, rather than working from section headings and partial excerpts as the previous pass had.
- “Abstraction Validation and DX Scaffolding”'s actual Scaffolding/Proactive Warnings content was restored; all four Drawbacks were restored to their full original paragraphs, including the `FileLogger`/`Stringer` example; all six Prior art entries were restored to their full original paragraphs; the `Reader`/`FileReader`, `PresenceHelper`/`Cache`, and `DefaultValidator`/`UserRecord` code examples and the surrounding explanatory text that had been dropped were restored; and the full “Tooling support for boilerplate reduction” subsection and its four bullets were restored.
- No content beyond the original document's own text was removed in this correction — only front matter (already migrated in the previous entry) and the mechanical RFC-to-document conversions remain different from the source.

#### Deliberation
- The previous entry's migration was pointed out to have summarized and shortened substantial parts of this document — including replacing “Abstraction Validation and DX Scaffolding” with a meta-note instead of its actual content, condensing four full-paragraph Drawbacks into one-line summaries, and condensing six full-paragraph Prior art entries (Go, Rust, Java, TypeScript, Zig, Haskell) into one-line summaries (Omid Hekayati — argued).
- Shortening a foundational document like this produces future ambiguity rather than clarity (Omid Hekayati — argued).

#### Considered and not done
Considered treating the previous entry's version as good enough, since the current template's own conventions do not forbid concise writing. Rejected: conciseness introduced here was not a stylistic choice, it was an accidental loss of substance during migration — several sections lost their only citable reasoning (e.g., why `FileLogger`/`Stringer` is a real accidental-satisfaction case, not a hypothetical one) and their only worked examples. A foundational, heavily-cross-referenced document like this one is exactly the case where under-specification compounds into future ambiguity, which is the concrete harm this correction addresses.

---

### Correct the receiver-type rule in Abstraction Realization
- Time: 2026-08-27T00:00:00Z
- Type: Fixed
- Cited:
  - [Polymorphism in Khayyam](./polymorphism.md) — Reference: examples there use `tp Read mt (self FileReader)…` vs. `self Reader`, exposing the drift
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Super Z](../../CONTRIBUTORS.md#super-z) — rewrote

#### What changed
- Corrects the rule in `Abstraction Realization (Implicit Satisfaction)`: the rule was corrected to exclude the receiver, and a covariant-return reference was added.
- The previous wording required “receiver type, parameter types, and return types all match” identically, yet every normative example declared `tp Read mt (self Reader)…` on the abstraction and `tp Read mt (self FileReader)…` on the capsule with a different receiver.
- The rule now states that for each method the influencing-variable types must match exactly, the influenced-variable types must match exactly or via covariant return, and the receiver is definitionally the implementing capsule itself.

#### Deliberation
- It was noted that examples and the “identical signatures” rule contradicted (Omid Hekayati — noted).

#### Considered and not done
Alternatives: (a) keep the identical-receiver wording and change examples to use the abstraction as receiver (rejected — capsule would not own its method); (b) add an explicit `as Reader` annotation (rejected — reintroduces `impl` ceremony). The chosen wording preserves structural satisfaction while making receiver ownership explicit.

---

### Second migration wave: `## Discussion` retired per the finalized method
- Time: 2026-09-08T00:00:00Z
- Type: refactor
- Propagates to:
  - khayyam-abstraction.handoff.md: Created - open questions and anticipated work moved there.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) - requested
  - [Qwen](../../CONTRIBUTORS.md#qwen) (qwen3.8-flash via [OpenCode](../../CONTRIBUTORS.md#opencode)) - moved

#### What changed
- The body's fixed top-level sections are now Abstract, Introduction, Explanation, Results; the document-level `## Discussion` and its Drawbacks, Rationale and alternatives, Prior art, Unresolved questions, and Future possibilities subsections no longer appear in the body (no topic-level Discussion wrappers remained).
- The accidental-satisfaction risk's premise detail — the `FileLogger`/`Stringer` example and the small-versus-large-abstraction collision analysis — folded inline into "Abstraction Realization (Implicit Satisfaction)" at the claim that structural satisfaction inherits Go's accidental-satisfaction risk.
- The discoverability cost of implicit satisfaction — satisfier lookup requires a tool-assisted graph traversal rather than a text search — folded inline into "Abstraction Validation and DX Scaffolding" at the claim that the developer-assistance burden shifts to tooling.
- "The Pure Contract Philosophy" folded inline into "What Is an Abstraction in Khayyam?": it states the design's current doctrine rather than a rejected alternative, and "Behavior Over Type Identity" argues from it; that topic's former plain-text reference to it now links to the section carrying it.
- Unresolved questions 1-5, with the three candidate directions on intentional satisfaction moved alongside the question they answer, went to the paired handoff's Open Questions; Future possibilities went to its Anticipated Work.
- Rejected alternatives and the audit-record drawbacks are preserved below under Considered and not done; the six-language comparative survey is preserved below under Related work.
- The plain-text "see Unresolved questions" pointer in "Abstraction Realization (Implicit Satisfaction)" now links to the paired handoff.
- The "Against explicit generic syntax" block dropped as graduated: the Abstract's second property already states its substance — "Abstractions carry no type parameters. Polymorphism classification and the rejection of generic syntax are documented in Polymorphism in Khayyam."

#### Considered and not done
- **Explicit delegation boilerplate as a recorded cost (relocated from the retired document-level Drawbacks, item 2; no change applied)**: the rejection of default implementations means every capsule sharing common behavior must carry its own explicit delegation line — deliberate, visible boilerplate repeated across every implementer; while Linter tooling can auto-generate these lines, the resulting source code is still longer than it would be with default methods. The counter-argument recorded at migration: the boilerplate is *honest* — it makes the execution path visible and auditable in a way that default methods do not.
- **No backward-compatible path to explicit satisfaction (relocated from the retired document-level Drawbacks, item 4)**: if the open question on intentional satisfaction is later resolved in favor of requiring some form of explicit declaration (option (b) or (c), recorded in the paired handoff), this would be a backward-incompatible change to the current model — every existing capsule-abstraction relationship would need to be audited and potentially annotated. The earlier the question is resolved, the lower the migration cost.
- **Rust's `impl` ceremony (rejected; migrated from the retired document-level Rationale and alternatives, "Why This Design Over Alternatives")**: while Rust's explicit `impl Trait for Type` eliminates accidental satisfaction, it adds boilerplate at every implementation site; in a large codebase with many abstraction-capsule pairs this scales poorly and is in tension with Khayyam's minimalism goals for the common case. The current structural model is simpler and more ergonomic; the accidental-satisfaction risk is recorded as an open question for targeted mitigation, not as a reason to adopt full nominal typing.
- **Default implementations (Rust traits, Java interfaces) (rejected; migrated from the same subsection)**: default method bodies in abstractions violate the "abstraction as pure contract" principle and create implicit inheritance-like behavior that conflicts with Khayyam's explicitness goals. The alternative — explicit delegation to shared capsules — is more verbose but completely transparent: the execution path is always visible, and the compiler's optimization decisions are never obscured by hidden routing logic.
- **Doing nothing, no abstraction mechanism (rejected; migrated from the same subsection)**: without abstractions, polymorphism would require either raw function pointers (erasing type safety) or code duplication; neither is acceptable for a language that aims to support high-performance library development.

#### Related work
- **Go — Interfaces (Structural Typing, No Defaults).** Go's interfaces are the closest existing model to Khayyam's abstraction design. Go uses fully structural typing: a type satisfies an interface if it has all the required methods, with no `implements` declaration. Go interfaces carry no default implementations. This simplicity is widely praised, but it comes with the accidental-satisfaction problem documented extensively in the Go community. The Go community's pragmatic response has been to accept this risk for large interfaces (where it is negligible) and use unexported marker methods for small, identity-carrying interfaces — a workaround at the library level, not a language-level solution. (Migrated from the retired document-level Prior art.)
- **Rust — Traits (Nominal Typing, Default Methods).** Rust's traits use fully nominal typing with explicit `impl Trait for Type` declarations. This eliminates accidental satisfaction entirely. Rust also supports default method bodies in traits, which provide shared behavior without requiring implementers to write delegation code. The cost is mandatory ceremony at every implementation site and the implicit routing behavior of default methods (a trait's default method body executes in the context of the concrete type, creating a form of multiple dispatch that can be surprising). Khayyam explicitly rejects default method bodies. (Migrated from the retired document-level Prior art.)
- **Java — Interfaces (Nominal Typing, Default Methods, Generics).** Java's interfaces use nominal typing with `implements` declarations. Since Java 8, interfaces support `default` methods with executable bodies. Java also has full generic syntax (`<T>`), whose rejection is documented in [Polymorphism in Khayyam](./polymorphism.md). This combination provides maximum flexibility but at the cost of significant syntax complexity and the same implicit routing concerns as Rust's default methods. Khayyam explicitly rejects the default method mechanism. (Migrated from the retired document-level Prior art.)
- **TypeScript — Structural Typing (Compile-Time Only).** TypeScript's type system uses structural typing for interface satisfaction, closely mirroring Go's model. TypeScript interfaces can describe object shapes, and any object with matching properties satisfies the interface. TypeScript has no default method implementations (its interfaces are purely type-level, erased at runtime). The accidental-satisfaction risk exists but is less practically concerning because TypeScript interfaces are not used as runtime dispatch mechanisms. Khayyam's abstractions, by contrast, have runtime implications (VTable generation), making accidental satisfaction a potentially more serious issue. (Migrated from the retired document-level Prior art.)
- **Zig — No Built-in Interfaces (Comptime-Based Alternatives).** Zig takes the most radical minimalist approach: it has no interface or trait mechanism at all. Generic behavior is achieved through `comptime` (compile-time code execution) and duck typing at the generic function level. This provides maximum simplicity but shifts the entire burden of polymorphism to the developer. Khayyam's design occupies a middle ground: it provides a first-class abstraction type for cleaner API contracts while keeping the language grammar minimal. (Migrated from the retired document-level Prior art.)
- **Haskell — Typeclasses (Nominal, No Defaults in the Language Core).** Haskell's typeclasses use nominal typing with explicit `instance` declarations. Typeclasses in their pure form carry no default implementations (though GHC extensions add them). Haskell's approach is closest to a "pure contract" model, and it demonstrates that nominal typing and zero-cost abstraction can coexist. However, Haskell's typeclass resolution happens at compile time through a separate mechanism (instance resolution), which is a form of implicit behavior that Khayyam's explicit delegation model avoids. (Migrated from the retired document-level Prior art.)

---

### Element and Error declared as abstractions in the Read/Close example
- Time: 2026-09-23T04:38:49Z
- Type: Fixed
- Cited:
  - [Polymorphism in Khayyam](./polymorphism.md) — Reference: the primitive-return examples corrected there under this same review round.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Mimo](../../CONTRIBUTORS.md#mimo) (mimo-v2.6-flash via [OpenCode](../../CONTRIBUTORS.md#opencode)) — applied

#### What changed
- The Read/Close example now declares `tp Element ab` and `tp Error ab` alongside `tp Reader ab`, so the signature types in the example are defined in the example itself.
- The following prose states that `Element` and `Error` in these examples are abstractions — declared behavior, not capsule types — and that only abstractions may appear in an abstraction-owned method signature; earlier polymorphism examples that showed a primitive there have been corrected in the paired changelog.
- The document's conflation of abstraction with contract is corrected against [Protocol vs Contract](../protocol.md#protocol-vs-contract): Abstract, What Is an Abstraction, Motivation bullets, What You Cannot Do, and Rejection of Default Implementations now say *behavioral specification* / *declaration of required behavior* rather than *pure contract* / *contractual agreement* / *Contract-First*; the IDL opening states explicitly that an abstraction is not a contract (no parties, obligations, commitments). An intermediate wording of the example paragraph had called abstractions "contracts" and told the reader to treat non-answering examples as illustrative; both were corrected on the owner's review.

#### Deliberation
- The critique that abstraction examples read as if primitives were legal signature types was accepted as an example/docs defect (Omid Hekayati — decided).
- Collapsing "abstraction" into "contract," and hedging wrong examples as "illustrative, ignore what they fail to answer," were rejected on review: fix the example; do not instruct the reader to look past it (Omid Hekayati — decided).
- The owner stated that contract is a distinct architecture concept (what parties commit to each other) while abstraction merely declares behavior; the body text is aligned to that distinction (Omid Hekayati — decided).

---

### Whether an abstraction with no methods is legal stays a Khayyam question
- Time: 2026-09-23T10:20:00Z
- Type: Fixed
- Propagates to:
  - abstraction.handoff.md: Done — the open question is whether Khayyam allows an abstraction with no methods (handoff: no entry of its own).
  - modeling.handoff.md: Done — whether a concept with no required behavior is a finished model is recorded there.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Grok](../../CONTRIBUTORS.md#grok) (Grok 4.7 via [Cursor](../../CONTRIBUTORS.md#cursor)) — applied

#### What changed
- The Khayyam body does not judge empty abstractions. The language question — whether `tp Name ab` with no methods is legal — is open in the abstraction handoff. Whether a concept with no required behavior is a finished model is in the modeling handoff.

#### Considered and not done
- **Stating in the Khayyam body that an empty abstraction is unfinished modeling (rejected)**: that is a modeling question. Khayyam's question is whether the form is legal (Omid Hekayati — decided).

---

### A concept is an abstraction and a concrete instance a capsule; the `Bool`/`Boolean` question carried here
- Time: 2026-09-29T10:40:00Z
- Type: Changed
- Cited:
  - [Documentation → Content Rule](../documentation.md#content-rule-no-fabricated-or-redundant-provenance) - Premise: a rule stated in two documents is given one home.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) - decided: code under `modules/` introduces itself, and language rules go to `docs/khayyam/`
  - Auto (model not recorded) via [Cursor](../../CONTRIBUTORS.md#cursor) - applied

#### What changed
- [A Concept Is an Abstraction; a Concrete Instance Is a Capsule](./abstraction.md#a-concept-is-an-abstraction-a-concrete-instance-is-a-capsule): a new section stating that a name carrying a concept is an abstraction and a concrete width, unit, or value representation is a capsule; that the owner of a signature decides whether it names the concept or a capsule; and why a contract that names the concept loses nothing. The rule was stated twice, in the module documents `modules/math/math.md` and `modules/time/time.md`, both deleted.
- `abstraction.handoff.md`: the `Bool`/`Boolean` question and runtime-signature residue moved to [Math Handoff](../modules/math/math.handoff.md) and [Runtime Handoff](../modules/computer/runtime.handoff.md) respectively.

#### Considered and not done
- Stating the rule in [Encapsulation in Khayyam](./encapsulation.md) as well: it is one rule, and Primitive Capsule Specification links here instead.

---

### Abstraction scaffolding relocated to rules catalog
- Time: 2026-09-29T16:00:00Z
- Type: Changed
- Propagates to:
  - abstraction scaffolding (`bundles/khayyam/rules/abstraction-scaffolding/abstraction-scaffolding.md`): Done
- Contributors:
  - Auto (model not recorded) via [Cursor](../../CONTRIBUTORS.md#cursor) - applied

#### What changed
- Tooling-support and DX scaffolding bullets replaced with links to abstraction scaffolding (`bundles/khayyam/rules/abstraction-scaffolding/abstraction-scaffolding.md`).

---

### Compiler-attributed enforcement removed from the abstraction document
- Time: 2026-10-03T11:16:28Z
- Type: Changed
- Propagates to:
  - [Computer — Compiler](../modules/computer/compiler.md): Done - the zero-cost and dispatch-strategy material removed here is the compiler's to state. [see compiler.md:42-47]
- Contributors:
  - [Space Bunny Alpha](../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../CONTRIBUTORS.md#opencode)) — applied

#### What changed
- [Motivation → The Problem This Document Solves](./abstraction.md#the-problem-this-document-solves): the compiler requirement was removed — "**Enable zero-cost abstraction where possible.** When the compiler knows the concrete type behind an abstraction, it should be able to inline the call — eliminating VTable overhead entirely — without the developer writing different code."
- [Satisfying an Abstraction](./abstraction.md#satisfying-an-abstraction): the verifying sentence became a statement of when satisfaction is judged — "The compiler verifies satisfaction at the point where the abstraction type is expected (assignment, parameter passing, etc.)" became "Satisfaction is judged wherever an abstraction type is required — where a value is declared as one, or where it is passed to a position declared with one." The example's comment became "`r` may name a `FileReader` here: `FileReader` satisfies `Reader`".
- [Abstraction Realization (Implicit Satisfaction)](./abstraction.md#abstraction-realization-implicit-satisfaction): the validation bullet was replaced rather than deleted, because whether a signature matches is what the rule turns on — "**Validation point**: The compiler validates abstraction satisfaction during assignment or parameter passing where an abstraction type is expected. Missing or mismatched methods will result in a strict compile-time error." became "**Where it is judged**: wherever an abstraction type is required — a `vr` declared as one, or a value passed to a position declared with one. A capsule missing a required method, or declaring one with a signature that does not match, does not satisfy the abstraction." The rule's own wording also no longer says realization is structural "at the compiler level".
- [Sharing Behavior Across Implementations](./abstraction.md#sharing-behavior-across-implementations): "free of compiler magic or implicit routing" became "with no implicit routing".
- [Rejection of Default Implementations](./abstraction.md#rejection-of-default-implementations): the optimization clause was removed — "and it clouds compile-time optimization because the compiler can no longer assume the call target is a simple VTable entry or a monomorphized concrete method."
- [Dispatch Strategy](./abstraction.md#dispatch-strategy): the pointer to a dispatch section in another language document became a boundary statement — "The compiler's mechanism for resolving polymorphic calls (monomorphization vs. dynamic dispatch) is documented in [Polymorphism in Khayyam](./polymorphism.md)." became "The grammar states no strategy for resolving a call through an abstraction and offers no syntax to choose one; what a Khayyam compiler does at a given call site is [Compiler](../modules/computer/compiler.md)'s business."
- Two sentences narrating superseded drafts were removed from the body, per [Documentation → Written surface](../documentation.md#written-surface): the document's opening claim that it "supersedes two prior, now-absorbed drafts — one on intentional abstraction satisfaction, one on the rejection of default implementations", and the note that "earlier polymorphism examples that showed one have been corrected in the paired changelog".

---

### The method-less abstraction entry repointed at the settled modeling answer
- Time: 2026-10-04T18:55:00Z
- Type: Fixed
- Propagates to:
  - abstraction.handoff.md: Done — the entry's cross-reference now names the section of modeling.md that answers the modeling half (Action: None).
- Contributors:
  - [Space Bunny Alpha](../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../CONTRIBUTORS.md#opencode)) — applied

#### What changed
- The method-less-abstraction entry in [abstraction.handoff.md](./abstraction.handoff.md) linked to `../modeling.handoff.md#a-concept-that-requires-no-behavior` — an entry that [Modeling → Concept Existence vs. Model Existence](../modeling.md#concept-existence-vs-model-existence) has since answered and removed from its own handoff. The link names that section instead, and the sentence records that the modeling half is settled.
- The language question the entry actually raises — whether the form `tp Name ab` with no methods attached is legal Khayyam — stays open, and this entry does not touch it.

#### Considered and not done
- **Closing the language question in the same edit (rejected)**: the modeling answer settles what a concept owning rules, lifecycle, or validation requirements is worth without behavior of its own, which is not a statement about which forms the grammar accepts.

---

### Deliberate satisfaction is composed and delegated; the language does not intervene
- Time: 2026-10-05T08:57:12Z
- Type: Changed
- Cited:
  - [abstraction_p.Implements](../modules/computer/abstraction-implements.md) — Premise: the protocol-level declaration of an intent to implement an abstraction, expressed as an abstraction a capsule composes rather than as syntax the language enforces.
  - [Type → Explicit Behavior Ownership](../type.md#explicit-behavior-ownership) — Premise: every method of a component is either defined in its own source or explicitly delegated by it, with no other route.
- Propagates to:
  - [abstraction.handoff.md](./abstraction.handoff.md): Done — the intentional-satisfaction question with its sub-questions and its three options, and the linter delegation-verification entry, are removed (Action: None).
  - [agency.md](./agency.md): Not done — [see agency.md:54-58] — its *Agency Beyond Concurrency* section still presents this question as `abstraction.md`'s own unresolved one and takes no position; not edited here, being outside this session's ownership.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Space Bunny Alpha](../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- [Abstract](./abstraction.md#abstract): the fourth item is now the resolved property *no language-level intent marker* rather than an open question, and the preamble counts four resolved design properties.
- A new section, [*Deliberate Satisfaction Is Composed, Not Declared*](./abstraction.md#deliberate-satisfaction-is-composed-not-declared), states the position as what holds: the language does not intervene in satisfaction — no `impl`-style keyword, no sealed declaration, no grammar-level intent marker — and deliberate satisfaction is an ordinary abstraction the capsule composes into its own definition, with the methods that abstraction requires explicitly delegated to a capsule that owns the behavior. The intent abstraction is judged by the ordinary structural check, at the same places and by the same signature comparison as any other abstraction; declaring the intent grants no exemption from satisfaction and no guarantee beyond it, and verification needs no mechanism of its own because the delegations are ordinary source.
- [Abstraction Realization (Implicit Satisfaction)](./abstraction.md#abstraction-realization-implicit-satisfaction): the accidental-satisfaction risk now ends at its own answer — composition and delegation — and the pointer into the paired handoff is gone, that question being closed.
- [Motivation → The Problem This Document Solves](./abstraction.md#the-problem-this-document-solves): the Go pain-point bullet no longer records the risk as an open question and points at the section that answers it.
- [What You Cannot Do](./abstraction.md#what-you-cannot-do): the bullet forbidding an explicit declaration by keyword now also says where deliberate satisfaction is expressed instead — composition and delegation, never grammar.
- `abstraction.handoff.md`: the intentional-satisfaction entry, its sub-questions, and its options (a), (b), and (c) removed; the linter delegation-verification entry removed, the ordinary structural check answering it; the compiler-generated dispatch-metadata item in Anticipated Work no longer conditioned on the question being resolved.

#### Deliberation
- The owner ruled that the language must not intervene in satisfaction, and named the project's own protocol-level precedent for expressing the intent — `docs/protocols/computer/abstraction-implements.md`, where an implementation intent is an abstraction a capsule composes rather than a declaration the language recognizes (Omid Hekayati — decided).
- The handoff's own sequencing rule had held this document's front-matter `Status` pending this question; that condition is discharged, and the status itself is left for the reviewing session to decide (Space Bunny Alpha — noted).

#### Considered and not done
- **Option (b), nominal declaration required for every implementation (rejected)**: it makes the language intervene at every satisfaction site, adding `impl Trait for Type` ceremony to every implementation site and a grammar keyword that contradicts the structural satisfaction this document states as a feature. The risk it removes is negligible for large abstractions, and where it is acute — small, marker-like abstractions — a capsule composing an intent abstraction answers it without the language knowing anything (Omid Hekayati — decided).
- **Option (c), a hybrid in which marker-like abstractions opt into requiring a declaration (rejected)**: it needs a formal criterion for which abstractions qualify, and a declaration mechanism the language must be able to check. The intent abstraction delivers the same per-abstraction opt-in without either: an abstraction whose satisfiers should say so composes an intent abstraction of its own, and nothing in the language distinguishes it from any other composition (Omid Hekayati — decided).
- **Promoting this document's front-matter `Status` (not done)**: the handoff's sequencing rule held it on this question, and the question is now closed, but promotion is the reviewing session's call (Space Bunny Alpha — noted).

---

### The satisfaction tension recorded as an open question, and researched to the point where it can be ruled
- Time: 2026-10-10T05:17:06Z
- Type: Added
- Propagates to:
  - [abstraction.handoff.md](./abstraction.handoff.md): Done — carries the open question *Do declared Types and structural satisfaction both stand?*, its state, and its next step.
  - [abstraction.satisfaction.research.001.md](./abstraction.satisfaction.research.001.md): Added — the evidence record for that question.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — asked, ruled that the tension is not to be declared resolved
  - [Space Bunny Alpha](../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../CONTRIBUTORS.md#opencode)) — argued, researched, drafted, applied
- Related work:
  - [Type](../type.md) → *Type vs Implementation Type* and *Abstract* — the two rulings the question turns between
  - [Agency in Khayyam](./agency.md) → *Agency Beyond Concurrency* — supplies the bounding sentence about the receiving side
  - [Modeling](../modeling.md) → *One Authoritative Location per Concern's Data* — where the inter-organization reading of the `type.md` ruling enters the record
  - [abstraction_p.Implements](../modules/computer/abstraction-implements.md) — the protocol-level home of the intent declaration, and the passage that removes one candidate boundary
#### What changed
- `abstraction.handoff.md` gains one open question: *Do declared Types and structural satisfaction both stand?* It states the two rulings in tension — this document's *Deliberate Satisfaction Is Composed, Not Declared*, which keeps satisfaction structural with no declaration mechanism, and `type.md`'s foundational ruling that every semantic entity is a Type and that a counterpart across a boundary is modeled as Types or not modeled at all — records that a session's derivation from the second ruling toward declared satisfaction was never applied, gives the narrower reading on which both stand because they address different boundaries, and names the deciding case: a `Reader`-shaped capsule in one organization consumed by another that never saw how it was written.
- `abstraction.satisfaction.research.001.md` is added, `Status` `Active`. It quotes both rulings whole at their decisive sentences with file and line, works the four candidate scopes, and reports four collisions with their files and lines — the conformance level, what "a boundary" reaches, accidental satisfaction at a boundary, and how the shape of the check is located — together with the places where the documents already dissolve the tension (`type.md:103`, `type.md:185`, `type.md:247`) and the passages a reader would expect to carry it and do not. It declares no resolution and edits no other document.
#### Deliberation
- Two owner rulings in the same week bear on the same question and neither was withdrawn. The owner was asked to declare the matter resolved and answered that it is not (Omid Hekayati — decided).
- The research's most consequential finding is that the inter-organization reading is not in `type.md` at all: `type.md:112`'s demonstrative points at the modeling/implementation gap, and the organizational extension enters through `modeling.md:401`, which cites `type.md` for it. A reader following only the ruling and a reader following the citation reach different boundaries, and the deciding case turns on that difference (Space Bunny Alpha — found, argued).
- The research also records, against its own filing, that every source it consulted is a document of this project, which `documentation-research.md` says makes the work an audit rather than a research; the tension is recorded rather than resolved (Space Bunny Alpha — noted).
#### Considered and not done
- **Reversing *Deliberate Satisfaction Is Composed, Not Declared* to a declared-satisfaction rule (not done)**: a session's derivation argued that resemblance deciding conformance is what a structural counterpart type system would be, and `type.md` forbids one; the reversal was not applied, because the owner ruled the matter open and `type.md` itself grants structural satisfaction permission twice (Space Bunny Alpha — argued, not applied).
- **Naming the collision in either base document's body (not done)**: the question is one of scope between two documents, and `docs/khayyam/abstraction.handoff.md` and the research record are its home until it is ruled (Space Bunny Alpha — noted).
- **Recording the research at `abstraction.research.001.md` (not done)**: the facet pairs a research to its base by the dot, and the owner named this path; recorded in the research's own Open Questions rather than corrected (Space Bunny Alpha — noted).

---

### Satisfaction-mechanism specification received from Type's handoff
- Time: 2026-10-10T07:40:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Cursor](../../CONTRIBUTORS.md#cursor) (Auto; underlying model not reported) — applied

#### What changed
- [The handoff](./abstraction.handoff.md)'s Anticipated Work gains "Formal specification of the satisfaction mechanism", which is moved from type.handoff.md. The mechanism by which a capsule satisfies an abstraction is this language's to state, and the base document no longer carries work about it, under the owner's ruling of 2026-10-10.

---

### Review of the uncommitted changes of 2026-10-12
- Time: 2026-10-12T09:45:50Z
- Type: Changed
- Contributors:
  - [Claude](../../CONTRIBUTORS.md#claude) (Sonnet-5.5) — reviewed, revised

#### What changed
- Reviewed the working-tree change to `abstraction.md`, `abstraction.handoff.md`, this changelog, and the new `abstraction.satisfaction.research.001.md`. The settled intentional-satisfaction question (handoff entry and options (a)/(b)/(c) removed, the linter-verification entry removed, answer placed in `abstraction.md` with its reason and recorded in the 2026-10-05 entry), the compiler-attributed removals (recorded in the 2026-10-03 entry), the repointed modeling answer, and the link repoints (folder move to `modules/` and `bundles/`; targets exist; the only removed changelog lines are those links, history otherwise kept) hold.
- [abstraction.satisfaction.research.001.md](./abstraction.satisfaction.research.001.md): the quoted passage "A Capsule satisfies an Abstraction through implicit structural satisfaction…" cited at `type.md:185` is in no revision of `type.md` that exists in the tree or HEAD; the citation, and the claim that `type.md` grants structural satisfaction permission "twice", were removed — `type.md:103` is the one place. `type.md:201`, `:209`, and `:217` were listed as restatements of structural satisfaction and are not; removed. Stale lines repointed: `type.md:247` to `:244`, `type.md:271` to `:268`, `modeling.md:401` to `:417`. The `protocol.md:228` quotation "did not write the rules" was corrected to the text's "without having written the rules". Two broken link brackets in Participants were closed.
- [abstraction.md](./abstraction.md): "delegates the methods that abstraction requires" (Abstract item 4, and *Deliberate Satisfaction Is Composed, Not Declared*) read as the intent abstraction's own methods, which has none; now "the abstraction it declares". The research record's quotation of that sentence was updated with it. The opening sentence no longer claims the document holds open questions, which now live only in the handoff.

#### Considered and not done
- This changelog's 2026-10-10T05:17:06Z entry repeats the `type.md:185` citation, "twice", and `modeling.md:401`: left, being history; this entry corrects it.
- Front-matter `Status: Proposed` of `abstraction.md`, which the 2026-10-05 entry left to a reviewing session: not promoted, the owner's call while the handoff's *Do declared Types and structural satisfaction both stand?* is open.
- Line numbers in the research record drift as other sessions edit `type.md` and `modeling.md`; they were correct on 2026-10-12.

---

### Tooling material leaves for the abstraction-scaffolding rule
- Time: 2026-10-12T11:13:47Z
- Type: Changed
- Propagates to:
  - Abstraction Scaffolding, a rule of this repository's Khayyam toolchain (bundles/khayyam/rules/abstraction-scaffolding): Done - the discovery-cost paragraph and the intent-declaration check now stand in its Why it exists.
- Contributors:
  - [Claude](../../CONTRIBUTORS.md#claude) (Opus-5.5) — applied

#### What changed
- Deliberate Satisfaction Is Composed, Not Declared: "so tooling — see [abstraction scaffolding] — checks a deliberate declaration the way it checks any other satisfier" became "so a deliberate declaration is judged the way any other satisfier is"; what tooling checks moved to the rule (on the owner's request that docs/ carry no implementation and no link into bundles/ (citation runs down the layers)).
- Removed: "Delegation boilerplate reduction and abstraction-satisfaction assists for this repository are organizational rules in [abstraction scaffolding]." The rule states it.
- Abstraction Validation and DX Scaffolding: "Because the language syntax avoids explicit implementation keywords, discovering which capsules satisfy a given abstraction requires a tool-assisted graph traversal rather than a simple text search for `impl AbstractionName`. That is a tooling burden, not a language burden, but it is a real cost in ecosystem maturity — a new Khayyam project will have less mature tooling than a new Rust project where `impl` blocks are trivially searchable. What the linter may generate or verify is stated in [abstraction scaffolding]." moved whole to the rule; the section keeps the language fact that no one place in source names an abstraction's satisfiers, and that finding them is tooling's work.
