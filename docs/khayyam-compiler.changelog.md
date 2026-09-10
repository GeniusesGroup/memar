# Khayyam Compiler Changelog

## Changelog

### Correct control-flow and compile-time-function contracts
- Time: 2026-08-27T00:00:00Z
- Type: Fixed
- Cited:
  - [Control Flow in Khayyam](./khayyam-control_flow.md) — Depends_on: `sc` and event abstraction that the compiler exposes
  - [Variable in Khayyam](./khayyam-variable.md) — Reference: domain-driven arithmetic and `FromString` human-readable text concerns
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Super Z](../CONTRIBUTORS.md#super-z) — rewrote

#### What changed
- Replaces `Control Flow via Framework Intrinsics` (which claimed the compiler “treats the framework’s `IF` as an intrinsic” and listed `goto` as the only native branching keyword) with `Control Flow via `sc` and Jump Primitives`: the AST recognizes only `sc` and low-level jump intrinsics (lowered to `goto` at IR, not a source keyword); framework `IF`/`ELSE` are ordinary library code; the compiler emits `sc` entry/exit and jump events to which DAA/linter subscribe.
- Corrects the `closeIdleSocket` example that inlined `Config.CNF_KeepAlive_Idle()` as an argument to `checkIdlePass` to the statement form with a named `idleDur` variable per the no-expression-chaining rule.
- Clarifies `Compile-Time Functions`: `W32`/`NanoSecond` are not privileged types; eligibility is a property of an explicitly designated pure/const method whose inputs are constants; the string `"7200"` is human-readable text for a typed variable, not a magic number.

#### Deliberation
- That `goto` as a keyword is retired thinking was clarified (Omid Hekayati).
- That the compiler is an independent app emitting events for DAA was clarified (Omid Hekayati).

#### Considered and not done
- Control-flow wording — keep `goto` as keyword and `IF` as intrinsic (rejected): reintroduces the coupling the design exists to avoid.
- Control-flow wording — move branching into syntax (rejected).
- Compile-time text — treat `W32` as privileged (rejected): violates Zero-Magic.
- Compile-time text — move all work to runtime (rejected): loses pre-compilation guarantee.

---

### Clarify runtime patching vs. Immutable Infrastructure
- Time: 2026-08-27T00:00:00Z
- Type: Changed
- Cited:
  - [Khayyam Runtime Specification](./khayyam-runtime.md) — Reference: the same `unsafe` runtime-patching description
  - [Polymorphism in Khayyam](./khayyam-polymorphism.md) — Reference: the Dynamic Dispatch Reducibility note that expects reducibility under Immutable Infrastructure
- Contributors:
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote

#### What changed
- Appends to `Change logic in runtime` a relation note: the default/safe deployment model is Immutable Infrastructure (no runtime capability addition without recompilation); the described `unsafe` WASM-like module replacement is an explicit, opt-in escape hatch, audited and never used for normal evolution, and therefore does not contradict the principle.

---

### Migrate to the Explanation-facet structure
- Time: 2026-08-30T00:00:00Z
- Type: refactor
- Cited:
  - [Documentation — Explanation](./documentation-explanation.md) — Depends_on: the structure this migration follows — YAML front matter, the `Abstract → Introduction → Explanation → Results → Discussion` body, and the per-topic Discussion pattern — is that specification's, applied to this document for the first time.
  - [Khayyam - Programming Language](./khayyam.md) — Reference: *Khayyam Is Not Its Own Compiler or Runtime* and *Separation of Syntax and Governance*, which supply the framing for the new Abstract, Motivation, and Discussion content.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote

#### What changed
- The document is now structured per `documentation-explanation.md`: YAML front matter added (Status: Proposed; Start Date and ID assigned retroactively from the file's first commit date, 2026-06-22); Abstract, Motivation, per-topic Discussion sections, Results, and a document-wide Discussion added.
- The framing thread through every new section: this document binds compiler *implementers*, never the language — each directive records how Zero-Magic Core, no-privileged-types, and Separation of Syntax and Governance must manifest in an implementation, and the specific shortcuts that would quietly reintroduce magic (special-casing a framework's `IF`, hardcoding `main`, privileged numeric types, normalized runtime patching).
- No construct-level content was removed: Control Flow via `sc` and Jump Primitives (with GOTO lowering detail and the commands-break rule), Environment-Agnostic Entry Points (with Delegation/Adaptability bullets), Compile-Time Functions (with the `CNF_KeepAlive_Idle` example and no-privileged-types clarification), and Change Logic in Runtime (with the Immutable Infrastructure relation note) are all preserved, reorganized under Explanation with their new Discussion sections derived from Khayyam's own philosophy documents rather than from new design decisions.
- New open questions recorded: the compiler event schema needs its own specification; the purity-designation mechanism is unspecified; what `unsafe` gates is unspecified; the "what Khayyam specifies vs. what an implementation provides" boundary remains shared with `khayyam.md`.

#### Deliberation
- Migrating this document (and its two sibling tooling documents) to the latest documentation methodology was requested (Omid Hekayati).
- The framing constraint that governs the new sections was clarified: none of the three tooling documents may impose anything on Khayyam itself, since together they are recommendations to each component's developers about how Khayyam's own thinking should find concrete manifestation (Omid Hekayati).

#### Considered and not done
- Writing the new Discussion content as fresh design contributions, e.g. proposing a concrete event schema or designation syntax while at it (rejected): this migration's purpose is structural, and the document's own framing forbids it from deciding things onto the language — new design belongs in its own session with Omid's review.
- Assigning an ID at current time instead of retroactively (rejected): the Start-Date-derived hour value was chosen per the ID spec's retroactive-numbering provision.

---

### Implementation-start plan recorded — readiness review, JS prototype, repository question
- Time: 2026-09-06T10:30:00Z
- Type: Added
- Cited:
  - [protocols/lexer.md](./protocols/lexer.md) — Reference: the first Future-possibilities item pointing at the lexer protocol is now satisfied by a real document; the readiness-review item below generalizes the same gate to the whole compiler effort.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — directed, reviewed
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash, via the OpenCode agent) — applied

#### What changed
- Three Future-possibilities entries added, transferring the implementation-start decisions from the design chat:
  - An Implementation Readiness Review gate — per open item, settle concept definition, boundary clarity, explicit semantic rule, language-vs-implementation ownership, foundational-law-vs-policy status, multi-implementation realizability, and cross-implementation invariants — before any compiler code.
  - The JavaScript-first prototype strategy (Khayyam source to language frontend to a semantic representation to memar-js on V8, WebAssembly second) with its two binding disciplines — the JS backend must not become the semantics' hidden source of truth, and two backends behind one semantic representation serve as the implementation-independence test — plus the seven questions the frontend abstraction must answer before code, with the note that the name `Parser` is deliberately not pre-assumed.
  - The repository question — no dedicated `khayyam` repository for now, language work starts in `memar-khayyam`, and a separate repository is justified only once the language can be understood and specified independently of Memar, holding the language as an artifact rather than an implementation.

#### Deliberation
- While consolidating the 2026-08-11/12 design-chat transcript into the documentation, it was decided that the three implementation-strategy outcomes of that chat belong in this document's Future possibilities rather than staying only in the chat record (Omid Hekayati).
- The wording of the added entries was reviewed (Omid Hekayati).

---

### Second migration wave: `## Discussion` retired per the finalized method
- Time: 2026-09-08T00:00:00Z
- Type: refactor
- Propagates to:
  - khayyam-compiler.handoff.md: Created - open questions and anticipated work moved there.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - requested
  - [OpenCode](../CONTRIBUTORS.md#opencode) (qwen3.8-flash) - moved

#### What changed
- The body retains only the fixed top-level sections `Abstract`, `Introduction`, `Explanation`, `Results`; the document-level `## Discussion` is gone.
- All four topic-level `#### Discussion` wrappers are gone — `Control Flow via sc and Jump Primitives`, `Environment-Agnostic Entry Points`, `Compile-Time Functions`, and `Change Logic in Runtime (Unsafe)`.
- Drawbacks that are current-state claims about the design's cost are folded inline into their topics: the no-hand-tuned-lowering performance cost and the event-contract stability surface (Control Flow); the boot-discoverability and quieter-misconfiguration cost (Entry Points); the second-interpreter divergence cost and purity-designation authoring burden (Compile-Time Functions). The review-only enforcement status (no conformance suite yet) is folded into the document preamble.
- The document-level Drawbacks' boundary caveat is dropped as graduated: the preamble already states the document is addressed to compiler developers and adds nothing to Khayyam's syntax or semantics, and the Abstract already states each directive constrains an implementation, never the language; the boundary's unsettled status rides with the boundary open question to the handoff.
- The retired `Unresolved questions` — event schema, multi-runtime boot resolution order, purity-designation mechanism and failure reporting, `unsafe` gating and patch auditing, the language-vs-implementation boundary — are now the paired handoff's `Open Questions`; the retired `Future possibilities` items are its `Anticipated Work`.
- The retired `Rationale and alternatives` blocks are preserved below under `Considered and not done`, and the retired `Prior art` surveys under `Related work`.

#### Considered and not done
- **Treat the framework's `IF`/`ELSE` as compiler intrinsics (rejected; migrated from the `Control Flow via sc and Jump Primitives` topic's retired Rationale and alternatives)**: promotes one library's names to privileged status inside the toolchain — exactly the coupling Khayyam's control-flow model exists to avoid. Every other control-flow library would remain second-class, and an organization swapping the framework's library for its own would silently lose whatever optimization the special case provided.
- **Keep `goto` as a source-level keyword (rejected; retired thinking; migrated from the same topic)**: it made the unstructured paradigm privileged rather than one library-built option among many — see the retired-draft note preserved in the body's Control Flow topic.
- **Silence instead of events (rejected; migrated from the same topic)**: without emitted control-flow events, each analysis tool would have to re-derive branch structure by re-recognizing library names in the AST — reimplementing, per tool, the coupling the event design avoids.
- **Hardcode `main`/`init`/`deinit` into the language (rejected; migrated from the `Environment-Agnostic Entry Points` topic's retired Rationale and alternatives)**: permanently couples one execution model to the grammar, forcing a breaking language change whenever the execution paradigm evolves, and making the language wrong-by-default for environments (event-driven, serverless, WASM, embedded) whose boot model differs.
- **Let the compiler pick one canonical boot convention (rejected; migrated from the same topic)**: moves the coupling from the grammar to the only implementation most users will ever touch — nearly the same coupling with a thinner layer of deniability; boot remains a *configuration* choice, resolved per target.
- **Privilege specific types or methods as compiler builtins (rejected; migrated from the `Compile-Time Functions` topic's retired Rationale and alternatives)**: violates Zero-Magic Core; there are no privileged types (see [No Privileged Types](./khayyam-variable.md#no-privileged-types)) — `W32` and `NanoSecond` are ordinary capsules, and the compiler knowing `FromASCII` "by name" would be exactly the magic this directive exists to prevent.
- **Let the compiler decide purity automatically by analysis (considered, not chosen; migrated from the same topic)**: silently deciding on the author's behalf conflicts with the principle that design decisions belong to the author and remain visible in source. Automatic analysis may be layered on top of explicit designation as a convenience or diagnostic, but designation stays the source of truth.
- **Evaluate nothing at compile time (rejected; migrated from the same topic)**: loses the pre-compilation guarantee and pushes genuinely static configuration cost into every runtime startup.
- **Make runtime module replacement a first-class, always-available capability (rejected; migrated from the `Change Logic in Runtime (Unsafe)` topic's retired Rationale and alternatives)**: contradicts Immutable Infrastructure as the default deployment model — no runtime addition of capability without recompilation — and would normalize the uncontrolled capability evolution that principle exists to prevent.
- **Omit the capability entirely (rejected; migrated from the same topic)**: microservice-style module turnover has genuine uses; removing it entirely would push adopters toward out-of-band binary manipulation with no audit story at all.
- **Keep it opt-in and tagged `unsafe` (chosen; migrated from the same topic as the recorded decision)**: the capability exists, is visibly dangerous at the call site, and sits outside the normal path — the same shape as the [runtime-side resolution](./khayyam-runtime.md#change-logic-in-runtime-unsafe) of this topic.
- **Fold compiler decisions into [Khayyam](./khayyam.md) (rejected; migrated from the retired document-level Rationale and alternatives)**: Khayyam's own Methodology keeps that document a short overview that links outward; implementation directives there would couple language evolution to implementation detail and grow exactly the document the language spec deliberately keeps small.
- **Leave compiler behavior unspecified (rejected; migrated from the same block)**: the handoff from language to implementation is Khayyam's central architectural move; leaving the receiving side undocumented means each compiler team re-derives — or silently ignores — the philosophy the handoff exists to preserve, reproducing the convenience-pressure failure mode the separation was designed to prevent.

#### Related work
- **`Control Flow via sc and Jump Primitives`:** Mainstream compilers do special-case well-known library symbols for optimization — C compilers' builtin recognition of `memcpy`/`strlen`, Go's compiler magic for `map`, `chan`, and `append`. Khayyam's directive is the deliberate inverse: lower everything through the same primitives and expose events, so no library gains toolchain privilege by being first or bundled. LLVM's design — analyses consuming a lowered IR rather than source-level library names — is the closest structural precedent for the event abstraction. (Migrated from the topic's retired Prior art)
- **`Environment-Agnostic Entry Points`:** C distinguishes hosted and freestanding environments: the standard requires a `main` function only for hosted implementations, freestanding (embedded) C has no required entry point, and startup code (crt0) is supplied by the environment's toolchain — long-standing evidence that entry-point conventions can live outside a language's grammar. Go, by contrast, requires a `main` package as a language-level rule — the coupling Khayyam's directive avoids. (Migrated from the topic's retired Prior art)
- **`Compile-Time Functions`:** Zig's `comptime`, C++ `constexpr`, and D's CTFE all evaluate pure code at compile time over ordinary language constructs rather than a separate macro language. Zig's approach is closest in spirit; Khayyam differs in tying eligibility to explicit designation of the method (author-owned, visible in source) rather than to a language-level `const` typing discipline. (Migrated from the topic's retired Prior art)
- **`Change Logic in Runtime (Unsafe)`:** WebAssembly's module add/remove at runtime is the design Khayyam's own text names. Erlang/OTP's hot code loading shows runtime replacement can be industrialized — but only behind significant surrounding machinery (supervision trees, versioned state-transition code), evidence that the feature is legitimate yet never free; the machinery is the runtime's concern, not the language's. (Migrated from the topic's retired Prior art)
- **Document-level:** Go's language specification is deliberately implementation-neutral, with gc, gollvm, and gccgo as independent consumers of it, and compiler-specific behavior documented separately from the spec. Khayyam's split follows the same shape at smaller scale — directives rather than conformance chapters — for the same reason: the language's stability should not depend on any one implementation's details. (Migrated from the retired document-level Prior art)

---

### Unsafe-patching note re-anchored to Structure Is Fixed by Definition
- Time: 2026-09-09T00:00:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — corrected
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — applied

#### What changed
- The "Relation to Immutable Infrastructure" note mirrors khayyam-runtime.md's re-anchoring: the compile-time-fixed default is now cited from the base principle Structure Is Fixed by Definition (type.md), and the Immutable Infrastructure brand no longer appears in this document. The escape-hatch reading is unchanged.
- The Abstract's directive sentence now cites the same base principle.
