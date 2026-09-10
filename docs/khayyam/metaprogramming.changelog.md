# Metaprogramming in Khayyam Changelog

## Changelog

### Initial draft — synthesis of the standalone Decorators and Macros documents
- Time: unknown (historical import — drafted 2026-07-30 per the document's Start Date; this changelog was created at migration time, so the entry is reconstructed from the document's former `## Change Rationale` section)
- Type: Added
- Contributors: none recorded — the source front matter carried only identity fields, with no contributor attribution; none was reconstructed.

#### What changed
Synthesizes the standalone "Decorators Rejection" and "Rejection of Syntactic Macros and Meta-Programming" documents into this document's Decorators Rejection and Rejection of Syntactic Macros topics. Reflective Programming is newly drafted rather than migrated from an existing document; treat it as more provisional than the rest of this document — several open questions are logged under its own Discussion, and the illustrative `reflect_p.Structural` naming is not a settled proposal.

---

### Migration to the Explanation-facet template
- Time: 2026-09-03T00:00:00Z
- Type: refactor
- Cited:
  - [The Error](../protocols/error.md) — Evidence: the document formerly cited under the title "Error Handling: Library-Driven and Syntax-Free" now exists in this document set under this path, closing the stale open question that recorded it as not yet supplied.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote.

#### What changed
The body already conformed to `documentation-explanation.md` (Abstract; Introduction with Motivation and Methodology; topic-first Explanation with per-topic Discussion bundles; Discussion); the migration work was provenance and staleness. The legacy `## Change Rationale` section moved into this file (entry above), per the rule that provenance lives in the paired changelog. The Results section received the standard placeholder. Document-wide Unresolved question 2 — which recorded the Error-handling document as "not yet been supplied to this document set for review" — was removed as stale: that document now exists as [The Error](../protocols/error.md). The body's link to `abstraction-implements.md` had already been repointed to its new `protocols/` location in the relocation pass recorded in that document's changelog. No position changed.

#### Deliberation
- Review of the documents touched by the abstractions-directory change for conformance with the current documentation method, applying the progressive-migration rule, was requested (Omid Hekayati — requested).

---

### Second migration wave: `## Discussion` retired per the finalized method
- Time: 2026-09-08T00:00:00Z
- Type: refactor
- Propagates to:
  - khayyam-metaprogramming.handoff.md: Created - open questions and anticipated work moved there.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) - requested
  - [OpenCode](../../CONTRIBUTORS.md#opencode) (qwen3.8-flash) - moved

#### What changed
- The body's fixed top-level sections are now Abstract, Introduction, Explanation, Results only; the document-level `## Discussion` and the four nested `Rationale and alternatives`, `Prior art`, `Unresolved questions`, `Future possibilities` subsection headings are gone from the body, as are the three topic-level `#### Discussion` wrappers (Decorators Rejection, Rejection of Syntactic Macros, Reflective Programming) dissolved at every heading level per the wave-1 precedent.
- Drawbacks from all four locations and the rejected-alternative rationales from all four `Rationale and alternatives` subsections are preserved in this entry's `Considered and not done` — no drawback was kept inline, because each was either a comparative cost evaluation (versus other languages' mechanisms or rejected alternatives) or a cost the body already states; see the bullets below.
- The prior-art / comparative surveys from all four `Prior art` subsections are preserved in this entry's `Related work`.
- Reflective Programming's four open questions and its anticipated `reflect_p` package moved to the paired handoff (`## Open Questions`, `## Anticipated Work`).
- The document-level `Unresolved questions` and `Future possibilities` entries were not carried as separate items: each was a pointer whose full substance is the Reflective Programming question and anticipated-work item migrated to the handoff.
- The Decorators Rejection topic's `Unresolved questions` block — recording the "Error Handling: Library-Driven and Syntax-Free" citation as not yet supplied — was not carried forward: the 2026-09-03 migration entry above already records this same question as stale and closed by the document's arrival as [The Error](../protocols/error.md), so migrating it to the handoff would have resurrected a resolved question.
- The empty placeholders ("None at this time", "None recorded yet" ×2) were removed with no destination; no premise-evidence inline folds were required — no retired block carried a fact supporting a retained body claim that the claim did not already carry itself.

#### Considered and not done
- **Explicit, repeated composition for cross-cutting concerns is more verbose than decorators (retained cost, not a rejection; migrated from the Decorators Rejection topic's retired Drawbacks)**: common cross-cutting concerns (retry, caching, timing/logging wrappers) that a decorator would express in a single line require explicit, repeated composition at every relevant call site or an explicitly named wrapping capsule, which is more verbose than the decorator-based equivalent in other languages.
- **Boilerplate reduction needs external tooling as a separate build step (retained cost, not a rejection; migrated from the Rejection of Syntactic Macros topic's retired Drawbacks)**: without a macro system, some categories of legitimate boilerplate reduction (e.g. deriving a family of trait implementations automatically at compile time) require external tooling to be run as a separate build step, rather than being handled inline by the compiler itself — adding a tooling dependency for cases a macro system would otherwise absorb into the language.
- **Opt-in reflection cannot serve exploratory tooling on arbitrary types (retained cost, not a rejection; migrated from the Reflective Programming topic's retired Drawbacks)**: compared to universal, always-on reflection (Java, Go, C#), a tool that wants to inspect an arbitrary, unknown type simply cannot, unless that type's author already anticipated the need and composed the relevant abstraction — a real limitation for exploratory tooling (a generic debugger or REPL that wants to inspect "whatever value is here") that universal reflection handles for free.
- **Capability gap relative to languages offering any of the three unconditionally (retained cost, not a rejection; migrated from the retired document-level Drawbacks)**: together, the three positions mean any tool wanting to alter a method's behavior invisibly, generate code invisibly, or inspect a type's structure without that type's author having opted in simply cannot — it must work through visible composition, external tooling, or an explicitly composed abstraction. Some legitimate tooling categories (universal serializers, generic debuggers, ORMs that work on arbitrary unannotated types) require more upfront cooperation from a type's author in Khayyam than they would elsewhere.
- **Decorator/annotation syntax (rejected; migrated from the Decorators Rejection topic's retired Rationale and alternatives)**: Python, TypeScript, Java, and C# decorator/annotation syntax lets a method's effective runtime behavior diverge silently from what its declaration shows — directly conflicting with Khayyam's explicitness principle.
- **Syntactic macro systems (rejected; migrated from the Rejection of Syntactic Macros topic's retired Rationale and alternatives)**: Rust's `macro_rules!`/proc-macros and C's preprocessor introduce a compile-time code-rewriting phase that is, by design, somewhat opaque to a reader inspecting only the source — directly in tension with the zero-hidden-magic principle running through [Metaprogramming in Khayyam](./metaprogramming.md), [Sovereign Encapsulation](./encapsulation.md#sovereign-encapsulation), and [Library-Defined Control Flow](./control_flow.md#library-defined-control-flow) (rejecting macros for the same reason those documents reject implicit mutability keywords and compiler-special-cased control flow, respectively).
- **Universal, always-on reflection (rejected; migrated from the Reflective Programming topic's retired Rationale and alternatives)**: the conventional approach in Java, Go, and C# gives every type an always-available introspection surface whether or not its author intended one, which is exactly the kind of hidden, unauthorized-by-declaration path this document's decorator and macro rejections also reject — the fact that reflection only *reads* rather than *rewrites* does not change that the path itself is not visible in the type's own declaration.
- **No reflection at all, rely entirely on macros for structure-dependent codegen (considered, not chosen; migrated from the same retired Rationale and alternatives)**: Rust's approach works, but only by keeping the macro system Khayyam has already rejected for unrelated, stronger reasons (see [Rejection of Syntactic Macros and Meta-Programming](./metaprogramming.md#rejection-of-syntactic-macros-and-meta-programming)). Opt-in reflection covers much of the same need (a tool asking a type what it looks like) without requiring a compile-time code-rewriting phase at all.
- **Rejecting reflection entirely, or adopting it universally (both rejected; migrated from the retired document-level Rationale and alternatives)**: all three positions trace to the same underlying test — does this capability require a hidden path into a type's behavior or structure that the type's own declaration doesn't show? Decorators and macros fail this test unconditionally and are rejected outright. Reflection can pass it, but only if implemented as an opt-in capability rather than a universal one — so that's the position Khayyam takes, rather than either rejecting reflection entirely (which would leave a real gap decorators/macros can't fill either, given they're also rejected) or adopting it universally (which would reopen the hidden-path problem from the other direction).

#### Related work
- Python decorators and Java/C# annotations are the primary prior art being rejected for decorators. Languages without a decorator mechanism (C, Go) instead rely on explicit wrapper functions/structs for the same cross-cutting needs, which is closer to Khayyam's chosen approach. (Migrated from the Decorators Rejection topic's retired Prior art)
- Rust's macro system and the C preprocessor are the primary prior art being rejected for macros. Languages and ecosystems that instead rely on external code generators emitting plain source (e.g. Go's `go generate` convention, or Protocol Buffers' code generation step) are closer in spirit to Khayyam's chosen approach. Notably, Rust — which also has no built-in reflection — leans on its macro system (e.g. `serde`'s derive macros) to cover needs Khayyam covers instead through opt-in reflection (see [Reflective Programming](./metaprogramming.md#reflective-programming)); rejecting macros without offering some other release valve for that category of need would leave a real gap. (Migrated from the Rejection of Syntactic Macros topic's retired Prior art)
- Java's `Class`/`getClass()` and Go's `reflect` package are the primary prior art for universal, always-on reflection, rejected here in favor of an opt-in model. Rust deliberately has no reflection and relies on derive macros (`serde`, `Debug`) for the same category of need — a useful contrast, since Khayyam rejects Rust's macro-based solution too but, unlike Rust, retains a non-macro path to the same underlying need. C#'s attribute-plus-reflection combination is closer to a hidden-by-default, opt-out model (nearly everything is reflectable unless deliberately hidden) — the inverse of Khayyam's opt-in-by-default stance. (Migrated from the Reflective Programming topic's retired Prior art)
- Taken as a whole, this document's stance — support the underlying need (introspection) while rejecting the specific mechanisms (decorators, macros, universal reflection) that would make it invisible or unconditional — mirrors the pattern already established by [`abstraction_p.Implements`](../protocols/abstraction-implements.md): solve the tooling problem with an ordinary, opt-in, composed method, not a language feature. (Migrated from the retired document-level Prior art, whose pointer that individual prior art is documented per topic is thereby superseded by the three bullets above, which reproduce it)
