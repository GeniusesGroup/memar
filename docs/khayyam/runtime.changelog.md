# Khayyam Runtime Specification Changelog

## Changelog

### Clarify runtime patching vs. Immutable Infrastructure
- Time: 2026-08-27T00:00:00Z
- Type: Changed
- Cited:
  - [Khayyam Compiler Directives](./compiler.md) — Reference: the same `unsafe` runtime-patching description there
  - [Polymorphism in Khayyam](./polymorphism.md) — Reference: the Dynamic Dispatch Reducibility note that expects reducibility under Immutable Infrastructure
- Contributors:
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote

#### What changed
- A relation note was appended to `Change logic in runtime`: the default/safe deployment model is Immutable Infrastructure (no runtime capability addition without recompilation); the described `unsafe` WASM-like module replacement is an explicit, opt-in escape hatch, audited and never used for normal evolution, and therefore does not contradict the principle.

---

### Migrate to the Explanation-facet structure
- Time: 2026-08-30T00:00:00Z
- Type: refactor
- Cited:
  - [Documentation — Explanation](../documentation-explanation.md) — Depends_on: the structure this migration follows — YAML front matter, the `Abstract → Introduction → Explanation → Results → Discussion` body, and the per-topic Discussion pattern — is that specification's, applied to this document for the first time.
  - [Khayyam - Programming Language](./khayyam.md) — Reference: *Khayyam Is Not Its Own Compiler or Runtime* and *Separation of Syntax and Governance*, which supply the framing for the new Abstract, Motivation, and Discussion content.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested, clarified
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote

#### What changed
- The document is now structured per `documentation-explanation.md`: YAML front matter added (Status: Proposed; Start Date and ID assigned retroactively from the file's first commit date, 2026-06-26); Abstract, Motivation, per-topic Discussion sections, Results, and a document-wide Discussion added.
- The opening note (Khayyam does not dictate a runtime; this is the Memar Framework's reference architecture) is preserved and now does double duty as the anchor of the new framing: this document binds runtime *implementers*, never the language, and is deliberately one-runtime opinionated without elevating the Memar Framework's choices to Khayyam requirements.
- No rule content was removed: the Concurrency and Execution Model section (User-Space Scheduling, Library-Driven Primitives, the MUST-level Core Affinity & Lock-Free Design commitment) and Change Logic in Runtime with its Immutable Infrastructure relation note are both preserved under Explanation.
- The new Discussion content is derived from Khayyam's own philosophy documents rather than new design decisions — in particular, the motivation that the runtime is the last layer where hidden magic could quietly return, and the caution against readers mistaking Memar-Framework choices for language requirements.
- New open questions were recorded: the user-space/kernel-boundary interaction for pinned tasks; what the `unsafe` tag gates at the runtime layer; whether any part of this reference architecture should eventually become a conformance floor for *any* Khayyam runtime, versus remaining Memar-specific.

#### Deliberation
- Migration of this document — and its two sibling tooling documents — to the latest documentation methodology was requested (Omid Hekayati — requested).
- The framing constraint governing the new sections was clarified: none of the three tooling documents may impose anything on Khayyam itself, since together they are recommendations to each component's developers about how Khayyam's own thinking should find concrete manifestation (Omid Hekayati — clarified).

#### Considered and not done
- **Renaming the document (e.g., to "Memar Runtime Reference Architecture") (rejected)**: would have resolved the Khayyam/Memar naming tension the migration's Discussion now describes, but renaming is a title/concept decision belonging to Omid's review, not a structural migration step — recorded as an open thread in the Discussion instead.
- **Moving the Immutable Infrastructure relation note into a proper `#### Rationale and alternatives` under the Change Logic topic (rejected)**: kept it as the blockquote the previous entry added, since it is a cross-document relation statement, not this topic's own alternatives record.

---

### Second migration wave: `## Discussion` retired per the finalized method
- Time: 2026-09-08T00:00:00Z
- Type: refactor
- Propagates to:
  - khayyam-runtime.handoff.md: Created - open questions and anticipated work moved there.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) - requested
  - [OpenCode](../../CONTRIBUTORS.md#opencode) (qwen3.8-flash) - moved

#### What changed
- The body now carries only the fixed top-level sections — `Abstract`, `Introduction`, `Explanation`, `Results`: the document-level `## Discussion` and both topic-level `#### Discussion` wrappers (under Concurrency and Execution Model and Change Logic in Runtime (Unsafe)) are retired; no other body content changed.
- The Concurrency and Execution Model topic's Drawbacks stayed in the body, folded inline at the end of that topic as a current-state claim about the delegated model's costs (no universally-optimized primitive; per-deployment syscall-composition work; correctness responsibility relocated into replaceable framework code) — those statements bear on reading the design as it stands, so they serve the current-state reader.
- The document-level Drawbacks stayed as an audit record below: the runtime-does-not-yet-exist enforcement gap and the one-runtime-opinionated misreading risk are statements about this document's maturity, already carried in the body by the opening note, the Abstract's implementation-not-language bound, and the empty Results.
- Rejected alternatives and recorded decisions from all three retired Rationale and alternatives blocks (both topics plus the document-level section) relocated below; the three comparative prior-art surveys relocated to Related work; the three Unresolved questions and both Future possibilities items moved to the newly created paired handoff, `khayyam-runtime.handoff.md`.

#### Considered and not done
- **Build channels/mutexes/async-await into a Khayyam core (rejected; migrated from the Concurrency and Execution Model topic's retired Rationale and alternatives)**: hardcodes one concurrency paradigm into the grammar — the same coupling Khayyam declines for control flow, applied to scheduling. It would also make primitive behavior invisible: a keyword-synchronized operation reads as atomic without revealing its cost or its failure modes.
- **Delegate to the OS kernel's scheduler (rejected as the default; migrated from the same topic)**: kernel context switches are the overhead this model exists to avoid, and kernel scheduling policies are neither swappable nor inspectable from source — a black-box dependency in the exact layer Khayyam requires to be explicit.
- **User-space framework ownership (chosen; migrated from the same topic as the recorded decision)**: scheduling and synchronization become ordinary capsules — visible in imports, swappable per domain, and governable by linter policy like any other library decision.
- **Make runtime module replacement a first-class, always-available capability (rejected; migrated from the Change Logic in Runtime (Unsafe) topic's retired Rationale and alternatives)**: would contradict Immutable Infrastructure as the default deployment model — no runtime addition of capability without recompilation — and normalize the uncontrolled capability evolution that principle exists to prevent.
- **Omit the capability entirely (rejected; migrated from the same topic)**: microservice-style module turnover has genuine uses; removing it entirely would push adopters toward out-of-band binary manipulation with no audit story at all.
- **Keep it opt-in and tagged `unsafe` (chosen; migrated from the same topic as the recorded decision)**: the capability exists, is visibly dangerous at the call site, and sits outside the normal path — the same shape as the [compiler-side resolution](./compiler.md#change-logic-in-runtime-unsafe) of this topic.
- **Declare no runtime document at all (rejected; migrated from the retired document-level Rationale and alternatives)**: Khayyam genuinely does not dictate a runtime — but leaving the execution layer entirely unspecified hands the last, least-visible layer of the stack to whoever implements it first, with no record of how the framework is expected to honor the philosophy. The magic-prevention argument that justifies keeping the compiler out of the language applies equally here, one layer down.
- **Elevate this document to "the Khayyam runtime" (rejected; migrated from the same section)**: would convert a reference architecture into a de-facto language requirement, contradicting the runtime-agnostic stance the document itself opens with. Its Status and framing remain that of one framework's design, consumable and replaceable.
- **Fold runtime concerns into [Khayyam](./khayyam.md) (rejected; migrated from the same section)**: Khayyam's own Methodology keeps that document a short overview linking outward; execution-layer detail there would couple language evolution to framework implementation choices.
- **A reference architecture for a runtime that does not yet exist in implemented form (drawback record; migrated from the retired document-level Drawbacks)**: the MUST-level commitments (core pinning, user-space scheduling) are currently enforced only by review against this document, not by shipped, measured behavior. The document is also deliberately one-runtime opinionated — a reader might mistake the Memar Framework's choices for Khayyam's requirements, when Khayyam itself remains runtime-agnostic; the opening note exists to prevent exactly that reading, and the boundary between the two is still being worked out (the question is carried in `khayyam-runtime.handoff.md`).

#### Related work
- Erlang/BEAM and Go's runtime are the closest precedents for user-space scheduling with language-level integration; Go is the cautionary half of the comparison — its channels and scheduler are exceptional engineering, but permanently privileged, which is precisely the coupling Khayyam refuses. Seastar (the ScyllaDB framework) is the closest precedent for the core-affinity/lock-free model: shared-nothing, pin-per-core task ownership at framework level, below the language. Unikernel systems (MirageOS, IncludeOS) demonstrate the deployment end of the same philosophy — the runtime is the application's actual operating environment, not a guest above someone else's scheduler. (Migrated from the Concurrency and Execution Model topic's retired Prior art)
- WebAssembly's module add/remove at runtime is the design the text itself names. Erlang/OTP's hot code loading shows runtime replacement can be industrialized — but only behind significant surrounding machinery (supervision trees, versioned state-transition code), evidence that the feature is legitimate yet never free; the machinery is the runtime's concern, not the language's. (Migrated from the Change Logic in Runtime (Unsafe) topic's retired Prior art)
- The runtime-as-separate-specification pattern is common in language ecosystems — Go's memory model and scheduler docs, the JVM specification, Erlang/OTP's design principles — each documenting execution semantics the language grammar deliberately does not carry. This document follows that shape, with the Memar Framework in the role those projects' runtimes occupy, and Unikernel/Exokernel literature as the deployment-side tradition it targets. (Migrated from the retired document-level Prior art)

---

### Unsafe-patching note re-anchored to Structure Is Fixed by Definition
- Time: 2026-09-09T00:00:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — corrected
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — applied

#### What changed
- The "Relation to Immutable Infrastructure" note under Change Logic in Runtime (Unsafe) is re-anchored to the base principle Structure Is Fixed by Definition (type.md): the runtime executes a fixed definition, and `unsafe` patching is the controlled exception admitting definition changes into a running instance. The note no longer routes readers through khayyam-polymorphism.md's retired topic anchor, and the Immutable Infrastructure brand — whose home is the protocol layer — no longer appears in this document.
- The escape-hatch reading of `unsafe` patching is unchanged.
- The Abstract's deployment-commitment sentence now cites the same base principle instead of describing the default.
