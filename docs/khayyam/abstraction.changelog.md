# Abstraction in Khayyam Changelog

## Changelog

### Initial consolidation, superseding two prior drafts
- Time: 2026-07-11T00:00:00Z
- Type: Added
- Cited:
  - [Control Flow in Khayyam](./control_flow.md) — Depends_on: this document builds on the precedent set by that document of keeping behavioral policies as ordinary library-driven mechanisms rather than new syntax.
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
- Every occurrence of "RFC" referring to Memar's own documents was replaced with "document," linking to [Polymorphism in Khayyam](./polymorphism.md) and [Control Flow in Khayyam](./control_flow.md) where those documents actually exist, and describing the two now-superseded, absorbed drafts ("Intentional Abstraction Satisfaction," "Rejection of Default Implementations") in plain text without a link, since they no longer exist as separate documents.
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
  - [OpenCode](../../CONTRIBUTORS.md#opencode) (qwen3.8-flash) - moved

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
