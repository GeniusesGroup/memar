# Abstraction in Khayyam Handoff

Open work for `abstraction.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../documentation-handoff.md) for what a handoff is.

## Open Questions

### Does Khayyam allow an abstraction with no methods?
Open. The form is `tp Name ab` with no methods attached to it. Whether a concept that requires no behavior is a finished model is a modeling question, in [Modeling Handoff → A concept that requires no behavior](../modeling.handoff.md#a-concept-that-requires-no-behavior). This question is only the language's: is that form legal Khayyam?

### Is structural satisfaction sufficient, or does it need an intentional-satisfaction mechanism?
This is the central open question, carried forward from the two documents `abstraction.md` absorbs, with several sub-questions:
- Should this be resolved before Khayyam leaves Draft-equivalent status for the abstraction model, given how disruptive option (b) or (c) below would be if decided later?
- Which of options (a)/(b)/(c) below best balances the accidental-satisfaction risk against Khayyam's minimalism and structural-satisfaction goals?
- This document should not advance past its current status on the intentional-satisfaction question until the previous sub-question is resolved.

Three potential resolutions exist for the question of intentional vs. accidental satisfaction. None is chosen yet (the candidate directions moved here together with the question they answer):

**(a) Keep the current structural model as documented.** Simplest, matches [Khayyam](./khayyam.md) as written today, but leaves the accidental-satisfaction risk open at the language level for any marker-like abstraction — not just `Error`, but any small abstraction the standard library or an organization defines going forward.

**(b) Require explicit, nominal declaration for every abstraction implementation.** Along the lines of Rust's `impl Trait for Type`. Eliminates the risk entirely, but adds ceremony to every implementation site and is a significant, backward-incompatible change to a philosophy Khayyam currently states as a feature (structural satisfaction with no `impl` keyword).

**(c) A hybrid model.** Structural satisfaction remains the default, but specific abstractions — those identified as small, marker-like, or identity-bearing — can opt into requiring an explicit declaration. This would need a formal criterion for which abstractions qualify, and a library-driven (not new-keyword) mechanism for declaring it, consistent with [Control Flow](../protocols/control-flow.md)'s precedent of keeping such behaviors as ordinary method calls rather than new syntax.

### Linter delegation verification mechanism
The precise mechanism by which the Linter verifies explicit delegation (in the no-default-implementations model) is not yet specified.

### Cross-language compiler implications
How does implicit structural satisfaction interact with cross-language compiler backends that expect nominal declarations (e.g. generating Rust `impl` blocks or Java `implements` clauses from Khayyam source)?

### Abstraction design and over-abstraction risk
Khayyam's abstractions are intended as architectural specifications that express meaningful behavioral boundaries. The language currently provides no formal guideline for where one abstraction should end and another begin — should a `Sortable` abstraction also imply `Equatable`? Should `Serializable` imply `Cloneable`? Where inclusion is the mechanism, the question becomes: what is the minimum coherent behavioral boundary? This is not only a style question — it affects API surface area, compilation strategy (more conforming capsules means less monomorphization), and onboarding friction. A possible heuristic: an abstraction should represent a domain concept, not a technical capability — `UserRepository` is a valid abstraction; `Filterable` is probably not. The largest non-technical risk may be abstraction inflation: if developers misunderstand the role of abstractions, they may begin creating `Readable`, `Writable`, `Searchable`, `Filterable`, `Sortable`, `Composable`, and so on, as generic reuse mechanisms, recreating the same problems seen in interface-heavy ecosystems. The intended role of abstractions is architectural specifications that express meaningful behavioral boundaries, not general-purpose code reuse tools; Khayyam's success may depend on preserving this distinction.
- Is the domain-concept-vs-technical-capability heuristic sufficient, or does it need more specific supplementary criteria?
- Should the Memar framework define a curated set of canonical abstractions as reference examples for appropriate granularity?
- Are there realistic algorithms that genuinely require type identity rather than behavioral specifications, and if so, how should Khayyam handle them?

### Abstraction stability and versioning
When an abstraction's behavioral specification changes — a new method is added, a return type changes, a precondition is tightened — what happens to every capsule that conforms to it? In Rust, adding a method to a trait is a breaking change; in Go, it is not (structural typing); Java introduced default methods specifically to solve this problem. Khayyam's inclusion-based model needs its own answer, and since Smart Compilation may monomorphize based on the current set of conforming capsules, an abstraction change could trigger recompilation across the entire dependency graph — not only a compiler problem but an ecosystem-governance one: if core Memar-framework abstractions evolve frequently, upgrade cost becomes a function of the abstraction-stability model, not of the code change itself.
- What is the minimal safe evolution operation on an abstraction? Can a new method be added non-breakingly if it has a default implementation expressed as a standalone method?
- Should Khayyam define a formal versioning scheme for abstractions, similar to semantic versioning but adapted for behavioral specifications?

### Residual inheritance-wording re-audit
The vr-ab review session closed with an open suggestion to re-audit this document (and `polymorphism.md`) for surviving "inheritance" phrasing that conflicts with the extension-not-inheritance terminology established in [Type → Explicit Behavior Ownership](../type.md#explicit-behavior-ownership); the pass was never run.

## Anticipated Work

- **Compiler-generated dispatch metadata.** Once the intentional-satisfaction question is resolved (in any direction), the compiler could emit metadata files (e.g. a JSON manifest) listing every capsule and the abstractions it satisfies — valuable for IDE tooling (jump-to-implementation, find-all-satisfiers), cross-language compiler backends (generating `impl` blocks for Rust, `implements` for Java), and documentation generation (automated "implemented by" pages per abstraction).
- **Abstraction-level documentation annotations.** A future document could define a convention (not a language feature) for attaching documentation, examples, or invariants to an abstraction — similar to Rust's doc comments on traits or Go's interface documentation conventions. An organizational tooling concern, not a grammar change.
- **Composable abstraction constraints.** A future extension could allow organizations to define "abstraction constraints" — predicates a given abstraction's satisfiers must meet (e.g. "any capsule satisfying `Serializable` must also satisfy `Clone`") — enforced at the Linter level and expressed as configuration, not language syntax.
- **Curated canonical abstractions.** A curated reference set of canonical abstractions in the Memar framework, as examples of appropriate granularity and domain-concept framing, giving new developers concrete templates and reducing over-abstraction risk.
- **Abstraction-granularity Linter rules.**
