# Compiler Changelog

## Changelog

### Correct control-flow and compile-time-function contracts
- Time: 2026-08-27T00:00:00Z
- Type: Fixed
- Cited:
  - [Control Flow in Khayyam](../process/control-flow.md) — Depends_on: `sc` and event abstraction that the compiler exposes
  - Variable in Khayyam (`docs/khayyam/variable.md`) — Reference: domain-driven arithmetic and `FromString` human-readable text concerns
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Super Z](../../../CONTRIBUTORS.md#super-z) — rewrote

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
  - [Khayyam Runtime Specification](runtime.md) — Reference: the same `unsafe` runtime-patching description
  - Polymorphism in Khayyam (`docs/khayyam/polymorphism.md`) — Reference: the Dynamic Dispatch Reducibility note that expects reducibility under Immutable Infrastructure
- Contributors:
  - [Super Z](../../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote

#### What changed
- Appends to `Change logic in runtime` a relation note: the default/safe deployment model is Immutable Infrastructure (no runtime capability addition without recompilation); the described `unsafe` WASM-like module replacement is an explicit, opt-in escape hatch, audited and never used for normal evolution, and therefore does not contradict the principle.

---

### Migrate to the Explanation-facet structure
- Time: 2026-08-30T00:00:00Z
- Type: refactor
- Cited:
  - [Documentation — Explanation](../../documentation-explanation.md) — Depends_on: the structure this migration follows — YAML front matter, the `Abstract → Introduction → Explanation → Results → Discussion` body, and the per-topic Discussion pattern — is that specification's, applied to this document for the first time.
  - Khayyam - Programming Language (`docs/khayyam/khayyam.md`) — Reference: *Khayyam Is Not Its Own Compiler or Runtime* and *Separation of Syntax and Governance*, which supply the framing for the new Abstract, Motivation, and Discussion content.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Super Z](../../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote

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
  - [protocols/computer/lexer.md](./lexer.md) — Reference: the first Future-possibilities item pointing at the lexer protocol is now satisfied by a real document; the readiness-review item below generalizes the same gate to the whole compiler effort.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — directed, reviewed
  - [Super Z](../../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash via [OpenCode](../../../CONTRIBUTORS.md#opencode)) — applied

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
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) - requested
  - [Qwen](../../../CONTRIBUTORS.md#qwen) (qwen3.8-flash via [OpenCode](../../../CONTRIBUTORS.md#opencode)) - moved

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
- **Privilege specific types or methods as compiler builtins (rejected; migrated from the `Compile-Time Functions` topic's retired Rationale and alternatives)**: violates Zero-Magic Core; there are no privileged types (see No Privileged Types (`docs/khayyam/variable.md#no-privileged-types`)) — `W32` and `NanoSecond` are ordinary capsules, and the compiler knowing `FromASCII` "by name" would be exactly the magic this directive exists to prevent.
- **Let the compiler decide purity automatically by analysis (considered, not chosen; migrated from the same topic)**: silently deciding on the author's behalf conflicts with the principle that design decisions belong to the author and remain visible in source. Automatic analysis may be layered on top of explicit designation as a convenience or diagnostic, but designation stays the source of truth.
- **Evaluate nothing at compile time (rejected; migrated from the same topic)**: loses the pre-compilation guarantee and pushes genuinely static configuration cost into every runtime startup.
- **Make runtime module replacement a first-class, always-available capability (rejected; migrated from the `Change Logic in Runtime (Unsafe)` topic's retired Rationale and alternatives)**: contradicts Immutable Infrastructure as the default deployment model — no runtime addition of capability without recompilation — and would normalize the uncontrolled capability evolution that principle exists to prevent.
- **Omit the capability entirely (rejected; migrated from the same topic)**: microservice-style module turnover has genuine uses; removing it entirely would push adopters toward out-of-band binary manipulation with no audit story at all.
- **Keep it opt-in and tagged `unsafe` (chosen; migrated from the same topic as the recorded decision)**: the capability exists, is visibly dangerous at the call site, and sits outside the normal path — the same shape as the [runtime-side resolution](./runtime.md#mutating-a-running-artifact-is-unsafe) of this topic.
- **Fold compiler decisions into Khayyam (`docs/khayyam/khayyam.md`) (rejected; migrated from the retired document-level Rationale and alternatives)**: Khayyam's own Methodology keeps that document a short overview that links outward; implementation directives there would couple language evolution to implementation detail and grow exactly the document the language spec deliberately keeps small.
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
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — corrected
  - [Super Z](../../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — applied

#### What changed
- The "Relation to Immutable Infrastructure" note mirrors khayyam-runtime.md's re-anchoring: the compile-time-fixed default is now cited from the base principle Structure Is Fixed by Definition (type.md), and the Immutable Infrastructure brand no longer appears in this document. The escape-hatch reading is unchanged.
- The Abstract's directive sentence now cites the same base principle.

---

### Lifted to a language-independent Compiler protocol
- Time: 2026-09-15T09:00:00Z
- Type: Changed
- Propagates to:
  - compiler.handoff.md: Done — rewritten; Khayyam-to-JS prototype and event schema kept as anticipated work.
  - khayyam.md: Done — `sc` lowering, command newline, and `return` IR marker stated as realization facts.
  - lexer.md: none — already a consumed protocol; historical changelog links left as provenance.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [Grok](../../../CONTRIBUTORS.md#grok) (Grok 4.6 via [Cursor](../../../CONTRIBUTORS.md#cursor)) — rewrote

#### What changed
- The document is now the Compiler protocol: a compiler consumes a language specification and produces a target representation; it is not identified with one language or one target (native, JavaScript, WebAssembly).
- Requirements stated without owning Khayyam's AST: recognize language primitives not library names; emit analysis events; entry/lifecycle are configuration plus Runtime; designated pure operations may run at compile time; consume the Lexer; runtime mutation of the artifact is `unsafe`.
- Khayyam-specific lowering (`sc` to internal jumps, `return` as newline-terminated IR marker) moved to Khayyam (`docs/khayyam/khayyam.md`).
- Status returns to Draft. Title is "Compiler".

#### Deliberation
- Compiler is not uniquely Khayyam-to-machine-code; a precise definition is needed so other uses (Khayyam to JS) share it (Omid Hekayati — claimed).
- The document must move to the protocols folder as a general concept (Omid Hekayati — decided).

---

### Repository and realization placement settled — Khayyam modules live here
- Time: 2026-09-24T12:35:12Z
- Type: Decision
- Propagates to:
  - compiler.handoff.md: Done — the repository-question bullet is removed and the first JavaScript prototype points to the local `modules/khayyam/` toolchain.
  - content.md: Done — implementation is separated from the language itself, and the Khayyam modules are identified as one current realization.
  - filesystem.md: Done — the local Khayyam-backed modules serve as the implementation example.
  - giti.md: Done — the protocol remains language-independent and names the local Khayyam modules as its current realization surface.
  - protocols/README.md: Done — implementation modules are placed under this repository's `modules/`, with language-independent protocol meaning and a language choice made at realization time.
  - docs/README.md and docs/khayyam/README.md: Done — Khayyam's local realization is located in this repository.
  - knowledge.handoff.md: Done — executable knowledge work points to this repository's `modules/`.
  - khayyam.handoff.md and khayyam.md: Done — the language/toolchain boundary is stated in terms of a Khayyam toolchain or module.
  - .agents/skills/memar/SKILL.md: Done — implementation discovery is routed to local `modules/`, and the protocol's language independence is stated.
  - README.md, framework.md, knowledge.md, software.md, and comparisons/superpowers.001.md: Done — the local Khayyam realization is described without making it a prerequisite for Memar's concepts or protocols.
  - protocols/net/sRPC.md, protocols/process/test.md (recorded then as protocols/tdd.md), protocols/process/error.md, protocols/process/error.handoff.md, and protocols/codec/syllab.md: Done — implementation details are scoped to their realization while the main documents state language-independent rules directly.
  - protocols/computer/abstraction-implements.md and protocols/process/control-flow.md: Done — the protocol contracts are stated independently, with Khayyam retained as a realization example.
  - dependency-management.handoff.md, sdk.handoff.md, protocol.handoff.md, and system.handoff.md: Done — local module dependencies and external-consumer questions remain open without making a programming language a prerequisite.
  - framework.handoff.md, type.md, khayyam/polymorphism.md, and protocols/runtime/immutable_infrastructure.handoff.md: Done — external-repository citations are removed from live documents; their conclusions are stated directly and provenance remains in changelog history.
  - modules/khayyam/README.md, modules/khayyam/execution.md, and modules/khayyam/execution.handoff.md: Done — placement, build paths, and handoff language describe the local toolchain and `modules/` tree.
  - modules/computer/runtime/protocol/blocking.kh, modules/computer/runtime/protocol/concurrency.kh, modules/process/control-flow/protocol/if.kh, and modules/process/control-flow/protocol/panic-recovery.kh: Done — executable Khayyam declarations are staged as local material; empty and copied host-language drafts remain outside the repository change.
  - .gitignore: Done — the local Khayyam build directory is excluded.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Mimo](../../../CONTRIBUTORS.md#mimo) (mimo-v2.6-flash via [OpenCode](../../../CONTRIBUTORS.md#opencode)) — applied
  - [Space Bunny Alpha](../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../CONTRIBUTORS.md#opencode)) — audited, applied

#### What changed
- The repository question recorded on 2026-09-06 is closed as final: Khayyam has no dedicated repository. Its language documents and the current local Khayyam toolchain plan and modules now live in this repository; the earlier "for now" formulation is superseded by this settled arrangement.
- Memar's concepts and protocols remain language-independent. Khayyam is one local realization, not a prerequisite or a default that defines every Memar detail.
- Live references to the former `memar-khayyam` repository were replaced with the local realization language. Where outside evidence informed a claim, the conclusion is now stated directly in the main document and the provenance remains in changelog history.
- The scratch `main.kh`, empty placeholders, and copied host-language drafts used to inspect the former repository remain outside this staged repository change; the staged repository change contains the Khayyam toolchain plan, the executable Khayyam declarations selected for this change, and the documentation and scope corrections.
- The transferred Khayyam content was placed under `modules/` rather than `libs/`; local paths and the build-output ignore rule follow that placement.

---

### The compiler's obligation to flow management stated
- Time: 2026-10-03T11:40:44Z
- Type: Added
- Cited:
  - [Control Flow](../process/control-flow.md) - Depends_on: its Library-Defined Control Flow and Structured and Unstructured Flow as Libraries sections are what the guarantee list and the guarantee-versus-freedom line are written against, and its Error Propagation section is where a mid-scope return is named without saying what it returns from.
  - [Type](../../type.md) - Depends_on: the Scope category is what makes visibility a property of a boundary's own rules, which is the rule the seventh and sixth guarantees state for a branch body.
  - [Memory](../memory/memory.md) - Depends_for: the refusal of an uninitialized read is what makes deciding which paths reach a use a compiler obligation rather than a library's.
  - Khayyam (`docs/khayyam/khayyam.md`) - Reference: the Scope section's inertness statement is the primitive every guarantee is about, and the Method section's body-less-method form is what the first finding quotes.
  - The JavaScript target's emitter (`bundles/khayyam/targets/js/src/emit.ts`) - Evidence: the scope-to-nested-function lowering, the call-to-call lowering, the `return` emitted inside that function, and the refusal of a scope as a receiver, measured as facts about one realization.
  - The JavaScript target's link map (`bundles/khayyam/targets/js/link_map.json`) - Evidence: the map is empty, which is what makes the deciding half of a conditional unsupplied.
  - Control Flow Model (`modules/process/control-flow/control-flow.md`) - Reference: the consumer whose need each guarantee answers, and the model that holds the driver question open.
  - Construction Model (`modules/process/construction/construction.md`) - Reference: the consumer whose per-path reachability need is the analysis half of this obligation.
  - Binding Model (`modules/computer/binding/binding.md`) - Reference: the consumer whose provisioning need is the third of the three named needs.
- Propagates to:
  - compiler.handoff.md: Done - three open questions carry the mechanism, the decision's provenance, and the mid-scope return, plus one anticipated conformance check.
  - ../khayyam/khayyam.md: Rejected - the guarantee about what a branch body may see belongs to the compiler's obligation and not to the language documents, which is the placement the owner ruled.
  - ../process/control-flow.md: Pending - its conditional-pair topic can state a driver contract against named guarantees rather than against a mechanism; which mechanism serves the drive stays open there as it does here.
  - ../../../modules/process/control-flow/control-flow.md: Pending - its driver question is answered on the guarantee side and remains open only on the mechanism side.
  - ../../../modules/process/construction/construction.md: Pending - its one dependency on the control-flow model is now a stated obligation, and the compiler in this repository does not yet meet it.
  - ../../../modules/computer/binding/binding.md: Pending - its provisioning need is stated; the address convention stays that model's own.
  - ../computer/linter.md: Done - branch exclusivity depends on events this document makes a constraint on the mechanism as well as on the events. [see linter.md:53-54]
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) - decided
  - [Space Bunny Alpha](../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../CONTRIBUTORS.md#opencode)) - claimed, wrote

#### What changed
- `compiler.md` gained five topics under Explanation: the compiler's obligation to flow management, the branch body a flow-control module receives, what this obligation does not decide, what no option delivers, the statement that this repository's implementation is not this protocol, and the statement that a protocol may be written for an obligation nothing discharges.
- Each of three consumers' needs is stated in one sentence and classified. The control-flow module's need, the construction module's need, and the binding module's need are guarantees; the mechanism that serves them is a freedom. The test that draws the line is stated: a guarantee is a property of what a drive means, and a freedom is a property of how it is served.
- Seven guarantees about the object a flow-control module receives are stated as meaning: what it is, what driving it does, what a second driving does, what it returns, whether it is the same object across calls, what it may see of its enclosing method, and what happens to it when the enclosing method returns. The fourth is stated as open, and the visibility half of the sixth is stated here rather than in any language document.
- Four mechanisms a compiler might serve a drive by are named as options - a call, a jump, a step of a state machine, a returned continuation - each with what choosing it would commit the compiler to. No preference is stated and none is implied by the order.
- Two findings are recorded. The deciding half of a conditional is unimplemented and no option covers it: the decision is a body-less method the link map holds no entry for, which leaves a dilemma between the compiler's refusal to privilege a library by name and a library whose decision has no supplied implementation. And what a `return` written inside a body returns from is unstated by every document and answered differently by every option.
- The sentence in The compiler recognizes language primitives, not library names that attributed a jump lowering to a Khayyam realization is replaced by a statement of where the primitive is described and where the guarantees about it live. The lowered mechanism now appears only under the topic that names it as this repository's implementation.
- The Abstract names the obligation, the guarantees, and the withheld mechanism. The Methodology records that the obligation was derived from its consumers and that each guarantee was checked to hold under every option named.

#### Considered and not done
- Selecting one of the four mechanisms. The owner has not stated what abstraction the compiler places at the disposal of flow-management modules, and a protocol that chose would foreclose the realizations this document exists to keep open. The options are named with their commitments instead.
- Writing the visibility guarantee into the language documents. The guarantee about what a branch body may see was placed here because it is a guarantee about what the compiler must keep true, and because a language document stating it would read as a claim about how a scope is compiled.
- A separate protocol document for this obligation. It was written into `compiler.md` because the sentence it replaces stood in that topic as the compiler's only statement about the branch-grouping primitive, and because a guarantee the reader must hold alongside the primitive's definition belongs beside it.
- The obligation inside the Control Flow protocol. That protocol owns what a flow construct means and is explicit that it governs a process independently of any one language; the compiler's obligation is a claim about a compiler, and the compiler protocol already owns what a compiler may recognize and how it reports.
- Reopening the analysis-event schema. It is already an open item under The compiler emits analysis events, and this change only adds a constraint that the events be derivable from whatever serves a drive.

#### Decision
- The owner ruled that a scope may refer to any outer name while its own variables are not visible outside, because it may never execute (Omid Hekayati). That ruling is stated in `compiler.md` as the sixth guarantee, and the decision it settles — where the rule lives — is the one this change applied: the protocol, not the language documents.
- No mechanism was chosen, and the document says so in its own body rather than leaving the absence to be inferred from the omission (Space Bunny Alpha).

---

### The question a `return` command posed is withdrawn
- Time: 2026-10-03T00:00:00Z
- Type: Removed
- Propagates to:
  - Khayyam → Scope (`docs/khayyam/khayyam.md#scope`): Done — the language document now states that the grammar has no keyword for leaving a method early.
  - Control Flow Model → `return` is a command, not a method (`modules/process/control-flow/control-flow.md`): Pending — that section's reason for keeping the exit out of the library is a reason the library no longer needs. Not this session's file to write.
  - Control Flow Rule — Method Exit (`modules/process/control-flow/rules/method-exit/method-exit.md`): Done — its third bullet cites `:72` and `:81` for the question this entry removes. Not this session's file to write. [see method-exit.md:28]
  - The Construction model (`modules/process/construction/construction.md`): Pending — it states a body may hold four commands and counts two of them as the substrate its construction library needs. Not this session's file to write.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Space Bunny Alpha](../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../CONTRIBUTORS.md#opencode)) — applied

#### What changed
- [What this obligation does not decide](./compiler.md#what-this-obligation-does-not-decide) lists two further open questions rather than three: what a body hands back to its driver, and whether a body may be re-entered at a point other than its start. The third — what a `return` written inside a body returns from — is gone from the list and from the paired [handoff entry](./compiler.handoff.md) that carried it as its own question.
- The **A call** option no longer commits the compiler to the fate of a `return`, since that fate was a property of a command the language does not have.
- [What no option delivers](./compiler.md#what-no-option-delivers) states one finding rather than two, and the finding is now that what leaves a method early is a library's business: a language may realize it as a command of the grammar and the language this repository develops does not, so the question becomes one a library answers by declaring it. The seven guarantees are unchanged and no option states it.
- [The implementation in this repository is not this protocol](./compiler.md#the-implementation-in-this-repository-is-not-this-protocol) is re-measured against the toolchain as it now stands: the JavaScript target lowers a scope to a nested function (`emit.ts:423-428`) and a call to a call (`emit.ts:464`), refuses a scope used as a receiver, holds an empty link map, and its frontend carries three commands for a body — declare, scope, invoke — with no jump among them (`core/src/body.ts:15-24`). It no longer emits a `return` inside the function it lowers a scope to.
- What is untouched. Guarantee 7 — what happens to a body when the enclosing method returns — still holds on its own terms: a body's meaning ends with the execution that declared it. The **A jump** option's reference to [Control Flow → Error Propagation](../process/control-flow.md#error-propagation) naming a mid-scope return as ordinary control flow is about that protocol's own operation, not about a command of a grammar.

#### Considered and not done
- **Restating the question as "what does the exit method mean".** The removal could have been followed by a replacement question naming the library's method. Not done: the guarantee-versus-freedom test this document states applies to it too, and what such a method would mean is a fact about the library's declaration rather than about how a compiler serves a drive. Where a reader needs it, the method-exit Rule (`modules/process/control-flow/rules/method-exit/method-exit.md`) already says the exit operation's target is specified by where its own declaration says it lands (Omid Hekayati — decided).
- **Rewriting the seven guarantees to name the loss.** A guarantee that assumed a body could end early would have had to be withdrawn, and none does: each of the seven is stated as what a drive means and holds under all four options without it (Omid Hekayati — decided).

---

### The eight implementation-prescription removals given their proper homes
- Time: 2026-10-04T09:00:00Z
- Type: Added
- Cited:
  - Inheritance in Khayyam — Changelog (`docs/khayyam/inheritance.changelog.md`) — Evidence: entry "Compiler and linter prescriptions removed from the inheritance document" (`:169`), quotes the removed *Interaction with Smart Compilation* section at `:186` and the two compiler-analysis arguments it overlapped at `:182`.
  - Polymorphism in Khayyam — Changelog (`docs/khayyam/polymorphism.changelog.md`) — Evidence: the removed dispatch-strategy section at `:326`, the removed cross-language-compilation bullet at `:321`, the closed/open-set definition that survives at `:306`, and the entry's own *Considered and not done* at `:334`.
  - Abstraction in Khayyam — Changelog (`docs/khayyam/abstraction.changelog.md`) — Evidence: the removed zero-cost requirement at `:221` and the removed default-implementation optimization clause at `:225`.
  - Encapsulation in Khayyam — Changelog (`docs/khayyam/encapsulation.changelog.md`) — Evidence: the removed *Reduced Optimization Surface* claim at `:287`.
  - Method in Khayyam — Changelog (`docs/khayyam/method.changelog.md`) — Evidence: the removed method-ownership expectation at `:225`.
  - Variable in Khayyam — Changelog (`docs/khayyam/variable.changelog.md`) — Evidence: the removed file-level-initialization sentence at `:223` and its pending propagation to this document at `:216`.
  - Polymorphism in Khayyam — Handoff (`docs/khayyam/polymorphism.handoff.md`) — Evidence: the surviving definition of *devirtualization* at `:18`, used to state what the elided part of the inheritance removal meant.
  - The JavaScript target (`bundles/khayyam/targets/js/target.md`) — Reference: `:60` states this repository's realization's answer to the same question.
- Propagates to:
  - Khayyam → Abstraction (`docs/khayyam/abstraction.md`), Polymorphism (`docs/khayyam/polymorphism.md`), Inheritance (`docs/khayyam/inheritance.md`), Encapsulation (`docs/khayyam/encapsulation.md`), Variable (`docs/khayyam/variable.md`), Method (`docs/khayyam/method.md`): Rejected — restoring the sentences in the language documents was the position the owner's ruling removed them from; they are stated here instead, in a language that does not name one language's constructs.
  - The JavaScript target (`bundles/khayyam/targets/js/target.md`): Reference — it already states the realization's own mechanism, which this document points at rather than restates.
  - [docs/modularity.md](../../modularity.md): Done — the name-collision reasoning the same audit removed, which is not this document's subject.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — requested, ruled
  - [Space Bunny Alpha](../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../CONTRIBUTORS.md#opencode)) — applied, classified

#### What changed
- A new topic, [How a call against a declared specification may be served](compiler.md#how-a-call-against-a-declared-specification-may-be-served), states as a **freedom** what the audit removed from two language documents: the closed/open distinction a compiler applies at a call site; inlining the concrete implementation for a closed site (*monomorphization*); generating a dispatch structure and emitting one indirection per call for an open site; and *devirtualization* as a further step of the same freedom rather than a second decision a language defers. Its third item states that **zero-cost abstraction is promised by nothing** — the removed claim that "when the compiler knows the concrete type behind an abstraction, it should be able to inline the call — eliminating VTable overhead entirely — without the developer writing different code" is quoted as one compiler's freedom and one language's expectation, not a property a module may be written against.
- The same topic's closing paragraph carries the removed **cross-language compilation** bullet as a **rationale**: a compiler whose target is itself a language must decide at each such site which of the target's mechanisms to emit, and the closed/open distinction is the classification that makes that decision answerable. Which target mechanism corresponds to which case is left to a realization.
- A new topic, [What a Language's Discipline Gives and Costs](compiler.md#what-a-languages-discipline-gives-and-costs), holds three **rationales and observations**, stated as binding on no compiler: that a language refusing acquired behavior keeps a call's target single, with the removed clause that allowing it "clouds compile-time optimization because the compiler can no longer assume the call target is a simple VTable entry or a monomorphized concrete method"; that named, explicitly declared state is more consistently analyzable than an implicitly captured environment whose shape varies per use, with the removed claim's own hedge that the two are equivalent in the worst case; and that a language reaching a value only through a declared operation never hands a compiler a chain to resolve, which is the escape-analysis claim the inheritance document carried.
- [Entry and lifecycle are not grammar](compiler.md#entry-and-lifecycle-are-not-grammar) gained the **freedom** the variable document's removal left open: where a declaration standing outside any operation's body receives its first instance, and from what source, is the realization's — guaranteed none, forbidden none, and never a feature of the grammar.
- [The implementation in this repository is not this protocol](compiler.md#the-implementation-in-this-repository-is-not-this-protocol) now points at the target's own statement that it resolves a call by the receiver's declared type and refuses a call whose receiver is typed as an abstraction, so the realization's mechanism is cited where the realization keeps it.
- The Abstract states both new topics and the new freedom, so the enumeration a reader gets from it matches the body.
- **The eighth removal was found by reading the audit's own propagation ledgers, not from the summary this session began with.** The seven items named in the request account for the compiler destinations recorded at `abstraction.changelog.md:216` (`docs/khayyam/abstraction.changelog.md`), `inheritance.changelog.md:175` (`docs/khayyam/inheritance.changelog.md`), `polymorphism.changelog.md:314` (`docs/khayyam/polymorphism.changelog.md`), and `khayyam.changelog.md:629` (`docs/khayyam/khayyam.changelog.md`). The eighth is `variable.changelog.md:216` (`docs/khayyam/variable.changelog.md`) — "where a file-level variable's first instance is established, and from what source" — recorded there as pending against this document's entry-and-lifecycle topic and discharged nowhere until now.
- **The inheritance removal is the one record that is incomplete, and its text was re-derived rather than reconstructed from the summary.** Its changelog quote elides two passages with `[...]` (`inheritance.changelog.md:186`), so the optimization claims it named — perfectly linear escape analysis, devirtualization, inlining — were taken from the two places the same audit recorded them whole: the Motivation arguments at `inheritance.changelog.md:182`, which carry the escape-analysis substance verbatim, and the polymorphism handoff at `polymorphism.handoff.md:18`, which defines devirtualization. What the elisions hid and no document in the repository now holds is the wording of the introduction to that optimization list; the three named items are what survived into the protocol, and nothing was invented to fill the gaps.

#### Considered and not done
- **The method-ownership expectation.** The removed claim that "abstraction composition in particular is central to Memar-style design, so methods attached to abstractions should be plentiful" (`method.changelog.md:225`) was not placed here. It is not a guarantee, a freedom, or a rationale of this protocol's subject: it is an expectation about how much of a language's method surface attaches to specifications rather than to concrete kinds, which is a fact about a language and its use. Its facet is a Practice companion — `docs/khayyam/khayyam.practice.md`, whose reader is an agent writing code in that language — and that file was not this session's to write. It is recorded here so that the second search for it finds the judgment rather than only the removal.
- **Restoring the removed sentences as they stood.** Each was rewritten into a language that names no construct of one language, because a protocol states what must hold for every compiler rather than what Khayyam's compiler does. The removed wording is quoted in the body where the claim is load-bearing (zero-cost abstraction, the clouds-optimization clause) and lives in full in the language documents' changelogs.
- **Naming a mechanism.** The freedom states what a compiler may do and not what it should do, and the closed/open distinction is stated as a criterion rather than as a rule that a site be closed. Stating it as a rule would have been a mechanism in a guarantee's clothes, which is the third discipline under [The implementation in this repository is not this protocol](compiler.md#the-implementation-in-this-repository-is-not-this-protocol).
- **The rest of the same audit's unplaced removals.** Reading all nine of its entries turned up four more removals recorded with no destination, none of them this document's subject and none of them placed here: the green-thread scheduling account removed from the agency document (pending against [Runtime → Concurrency is hosted, not defined, here](runtime.md#concurrency-is-hosted-not-defined-here)), the method-naming bullet removed from the encapsulation document (pending against this repository's identifier-naming rule), the compile-time evaluation of string formulas removed from the variable document (already answered by [Designated pure operations may run at compile time](compiler.md#designated-pure-operations-may-run-at-compile-time)), and the container type-safety check removed from the polymorphism document (pending against [Linter](linter.md)). Each keeps its own recorded owner; none is restated here, and none is closed by this entry.

#### Decision
- A language document states what a construct is and not how a compiler lowers it, and the compiler protocol owns what a compiler is; these eight claims are therefore stated there, each marked as the guarantee, freedom, or rationale the protocol's own test requires (Omid Hekayati — decided).
- Base documents take none of them. The name-collision reasoning went to [`docs/modularity.md`](../../modularity.md) instead, stated in terms of Responsibility and identity that hold for any kind of development, because the audit's own removal record named that document as its destination (`khayyam.changelog.md:630`) and `khayyam.md`'s Import Mechanism still points there (`khayyam.md:62`).

---

### Review-only enforcement reframed as an unchecked requirement rather than an accepted form of enforcement
- Time: 2026-10-05T17:24:41Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Space Bunny Alpha](../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- The last sentence of [Methodology](./compiler.md#methodology) no longer says the directives are "currently enforced by review against this document — there is no conformance suite yet". It now says the directives are stated so that a party that did not write them can decide each against a named input, and that no suite running today is a gap in this project's checking rather than a limit on what the protocol decides.

#### Deliberation
- The edit was proposed in this session's earlier read-only sweep of `docs/` against the ruling and applied once it landed here. The sweep's reasoning is the record's: a Protocol is meaningful only where a procedure settles its conformance, and a sentence presenting review as the standing form of enforcement described the private-reading case the ruling names as the failure (Space Bunny Alpha).
- The distinction the replacement draws is between what the document decides and what this project has built to check it, and it is drawn without claiming a suite exists: the conformance suite remains Anticipated Work in `compiler.handoff.md`, and nothing here moved it (Space Bunny Alpha).

#### Considered and not done
- **Deleting the sentence outright (rejected)**: the fact that no suite runs is current state a reader needs, and the Relevance discipline keeps current state in the body. What changed is the shape of the fact, not its presence.
- **Also reframing the matching sentences in `runtime.md` and its changelog (rejected)**: that document carries the same shape and is not this session's to write. It is named here so the residue is visible rather than lost.

---

### Review of the uncommitted changes of 2026-10-12
- Time: 2026-10-12T09:46:30Z
- Type: Changed
- Contributors:
  - [Claude](../../../CONTRIBUTORS.md#claude) (Sonnet-5.5) — reviewed, revised

#### What changed
- Reviewed the uncommitted changes to `compiler.md` and `compiler.handoff.md` against HEAD. The `compiler.md` changes restore the topics the entries of 2026-10-03, 2026-10-04 and 2026-10-05 above already record (the obligation to flow management, the branch body's seven guarantees, the four unchosen mechanisms, the two findings, the repository-implementation topic, the call-against-a-specification freedom, the discipline rationales, the first-instance freedom, and the reworded Methodology sentence), plus link re-pointing for the folder move. The handoff gains five open questions (flow-management mechanism, the branch decision's implementation, serving a call against a specification, first instance outside any body, the method-ownership expectation) and one anticipated conformance check, as the 2026-10-03 entry's propagation records. No answer is placed or removed; every anchor and link resolves, and the line citations into the JavaScript target (`link.ts:93-96`, `emit.ts:223-228`, `423-428`, `464`, `body.ts:15-24`) hold at HEAD (the working tree's `body.ts` has since shifted the type to lines 17-26).
- Fixed in [A protocol may be written for an obligation nothing discharges](./compiler.md#a-protocol-may-be-written-for-an-obligation-nothing-discharges), commitment 2: it said the construction model records that thirty-three declarations "name a responsibility that makes an instance exist, and not one of them discharges it". The construction model says something narrower and warns against that reading: the `From*` declarations attach to the type they produce and none carries an influenced variable of it, "a record of this repository rather than a failure of the language", and not a showing that nothing fills the slot. The sentence now states that.
- Fixed in `compiler.md` → What no option delivers: the link labelled "the target's own model handoff" points at the control-flow model's handoff, which is where the driver question is recorded; the label now says so.
