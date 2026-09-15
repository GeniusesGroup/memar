# Memory Changelog

## Changelog

### Initial draft — memory semantics as contract (as "Memory Management")
- Time: 2026-09-06T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed, argued
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — reviewed, rewrote

#### What changed
- Initial Draft stating three rules — copy/ownership semantics are contract members, the boundary copy default is stated rather than folklore, allocation claims are measurement claims — with the header-copy and pooling-library evidence that motivates them.
- The positions were framed as contract-level requirements (explicitness, not manual management) so the document stays backend-neutral and consistent with the multi-language posture (Super Z).
- The boundary-copy default was linked to the Error protocol's boundary discipline as an interaction to resolve (Super Z).
- The ecosystem counter-arguments were recorded inside the rejected alternatives (Super Z).

#### Deliberation
- The positions were brought from public memory-management discussions (Omid Hekayati — claimed).
- The slice/string header-copy mechanics and the invisible-sharing hazard were claimed (Omid Hekayati).
- The ecosystem's unwritten callee-copies-before-return convention, and the opposite contract of pooling HTTP libraries — "things will go wrong here" as a documented, contract-shaped caveat — were claimed (Omid Hekayati).
- Benchmark-first discipline for allocation claims was claimed, adopted after repeatedly observing folklore ("zero alloc", "GC handles it") contradicted by measurement — including the project's own benchmarks showing a pooling library allocating more than the default at realistic request sizes (Omid Hekayati).

---

### Reworked as "Memory": definition first, reclamation taxonomy, GC concept corrected
- Time: 2026-09-06T00:00:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed, argued, corrected
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — reviewed, argued, rewrote

#### What changed
- The document now moves definition-first: memory defined as the class of all state-retaining capacities.
- Volatility (volatile/semi-volatile/non-volatile) is adopted as the classifier.
- The memory/storage dichotomy is rejected as an industry convention, with the attribution correction recorded.
- The reclamation question is shown inescapable: manager inescapable, collector optional; cost moves, never disappears.
- The reclamation mechanisms are classified, with runtime tracing GC as one family among several.
- The contract rules of the initial draft are retained unchanged as the document's second half.
- The concept-vs-label pattern this rejection exercises was written into [type.md](../type.md) as "Concepts Outlive Their Labels" (Super Z).

#### Deliberation
- The initial draft's jump into "management" without definitions was judged a writing defect, and the restructure was directed: define memory first, then manage it (Omid Hekayati — directed).
- The definitional positions were brought from public discussions (Omid Hekayati — claimed).
- The correct classifier for memory is **volatility** — volatile, semi-volatile, non-volatile per the standard taxonomy — not the ecosystem's memory/storage two-name split, which is rejected outright, including its attribution to the von Neumann architecture tradition (Omid Hekayati).
- The GC concept is misplaced in the ecosystem: **no language with dynamic allocation escapes the reclamation question** — what languages like Rust actually distance themselves from is *runtime GC mechanisms*, and their ownership scheme is itself automatic reclamation requiring its own tooling, so the mechanisms marketed as "GC" must be classified as one subcategory (runtime GC mechanisms) under the broader spread, or the term becomes incoherent (Omid Hekayati).
- The framing argument from the OS document: a founding layer grants bounded memory entitlements, never per-variable allocation services — so the manager inside the grant is the system's own, and reclamation policy is meaning defined above the guarantee boundary (Omid Hekayati).
- It was directed that the OOP/FP concept-vs-label pattern be recorded in [type.md](../type.md) rather than only alluded to here (Omid Hekayati — directed).
- Strong counter-argument against his own positions was requested before acceptance (Omid Hekayati — requested).
- The claims were verified and strengthened before recording (Super Z — verified).
- The von Neumann attribution was corrected: the architecture's stored-program core is a *unification* of instruction and data memory; the two-name split is a later industry convention, making the rejection stronger, not weaker (Super Z — corrected).
- "no language needs GC" was sharpened to "no language with dynamic allocation escapes reclamation", pure stack-discipline languages being the only genuine exception, and none of the marketed "no-GC" languages are in it (Super Z — sharpened).
- The hypervisor framing was corrected: even the traditional per-allocation allocator was never a guarantee-layer service but a library on top of the grant, so the sharp claim is *manager inescapable, collector optional* — Rust's allocator library and Swift's ref-count runtime both confirm (Super Z — corrected).
- The mainstream mechanism-based definition of "GC" was recorded as a recorded alternative rather than silently overridden, so the definitional choice is visible (Super Z — recorded).

#### Considered and not done
- **Keeping the title "Memory Management" and adding definitions on top (rejected)**: the title promised management while the subject turned out to be the concept first — the document is now "Memory" and its title, abstract, and structure all follow the definitional order (Omid Hekayati — directed; Super Z — applied).

---

### Provenance stripped from body; shadow-tier working-out absorbed from modeling
- Time: 2026-09-06T00:00:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — reviewed, decided
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote

#### What changed
- The document's body now contains only positions, arguments, and their verification discipline; every trace of where and with whom the positions were formed lives in the changelog.
- The dichotomy topic gained the full shadow-tier treatment absorbed from modeling.md, keeping the reference direction one-way (protocol document citing root concept document).
- The provenance sentence was removed from Methodology; the Wikipedia references and the source-checking discipline remain — both are directly relevant (Super Z).
- The Motivation's "from public discussions" framing was replaced with the direct claim (Super Z).
- The shadow-tier paragraphs from modeling.md were absorbed into the dichotomy topic with the modeling citation kept one-directional (Super Z).
- It was verified that no other body text carries discussion-origin provenance — the changelog entries above keep it all (Super Z).

#### Deliberation
- Two corrections were raised against this document's earlier pass (Omid Hekayati — reviewed).
- Explanatory documents must carry only what is strongly relevant — the Methodology's origin provenance (communities, years) belongs in this changelog, not in the document's body; the same stripping was applied across the framework's new protocol documents (Omid Hekayati — the first correction).
- The modeling document must not link down into this folder for its definitions — the dependency direction is inverted (memory is developed on modeling's method), so the modeling-level rule stays stated there while this document absorbs the working-out: the shadow-tier pattern (the dichotomy's practical product), the invalidation argument, and the one-authoritative-location consequence now live in the dichotomy topic here, citing modeling.md for the rule's modeling-level statement (Omid Hekayati — the second correction).

---

### Documentation-method migration: Prior art split, Unresolved questions to handoff
- Time: 2026-09-06T00:00:00Z
- Type: refactor
- Propagates to:
  - memory.handoff.md: Created — the volatility-vocabulary and notation questions moved there.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — moved, folded

#### What changed
- The Boundary-discipline topic's Prior art (the fault-boundary-translation echo of DDD and clean-architecture literature; the enrichment-before-logging step's grounding in observability engineering) is premise evidence for the translation rule and stays inline with the rule.
- The comparative positioning was already inside the same paragraph and remains.
- The topic-level Unresolved question (companion naming convention) moved to the handoff.
- The document-wide Prior art (volatility taxonomy's source, the filesystem-parallel for the dichotomy critique, the stored-program unification, the reclamation taxonomy's standard status) was premise evidence and folded into the topics carrying those claims.
- The body was reduced to wrapping only Drawbacks, Rationale and alternatives, and Future possibilities.
- Open questions live in the paired handoff.
- The claims that needed external support carry their support inline.

---

### Documentation-method migration: rejected alternatives and anticipated work relocated
- Time: 2026-09-06T00:00:00Z
- Type: refactor
- Propagates to:
  - memory.handoff.md: Done - anticipated work recorded there under `Anticipated Work`.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) - claimed, decided
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) - moved

#### What changed
- The body's `Discussion` wrappers dissolved entirely, per the finalized documentation method (documentation-explanation.changelog.md, same date) (Omid Hekayati - decided; Super Z - applied).
- The topic-level `Discussion`'s evidence paragraph (arena-allocation experiments as evidence allocation placement is a felt cost) folded into its topic as inline evidence (Super Z).
- The document-level `Drawbacks` removed from the body; its content preserved below without loss (Super Z).
- Rejected-alternative reasoning moved from the body's `Rationale and alternatives` sections into this entry's `Considered and not done`, without loss (Super Z).
- Anticipated work moved from the body's `Future possibilities` into the paired handoff's `Anticipated Work` (Super Z).

#### Considered and not done
- **"Let the language's memory model decide everything" (rejected)**: leaves contracts underspecified and re-creates the copy-semantics lottery this document exists to end; a framework that spans multiple languages cannot have per-language contract meanings. (Omid Hekayati - argued across the source discussions)
- **Manual memory management as a framework requirement (rejected)**: contradicts the framework's multi-language posture and ignores that the failure patterns occur identically in collector-equipped systems; the target is explicitness, not manual labor. (Omid Hekayati)
- **Recording the buffer-lifetime rule only in per-library API documentation (rejected)**: per-library documentation is where the information lives today and precisely why it is missed; the framework-level rule makes the term's presence contractually significant. (Omid Hekayati)
- **Adopting the ecosystem's memory/storage vocabulary with only a warning (rejected)**: the two-name split is the root cause of the shadow-tier modeling pattern; property-based classification expresses everything the split expressed without the false division. (Omid Hekayati)
- **Defining "GC" by mechanism and calling compile-time reclamation something else (rejected as this document's primary vocabulary)**: shelters the "no GC" marketing error; the function-based definition is adopted, with the mechanism-based reading recorded so the definitional choice stays visible. (Omid Hekayati) (Super Z - recorded the alternative rather than silently overriding)
- **A dedicated one-time migration pass for the pattern across existing documents (rejected)**: the progressive-migration rule applies; each file migrates at its next natural edit. (Super Z)

#### Considered and not done (from the removed document-level Drawbacks section)
- **The contract-explicitness requirement adds real specification and documentation burden to every Memar library, including ones whose language's default semantics would have made most terms trivially safe** — a cost the framework accepts deliberately: the burden is where the cost of the decisions actually is. (Omid Hekayati)
- **The definitional positions — one memory class, three volatility properties, one reclamation question — ask readers to abandon vocabulary they have used their whole careers, and the transition generates friction this document cannot remove, only justify** — accepted deliberately for the same reason. (Omid Hekayati)

---

### Absorb managerial requirements; retire the Khayyam-shelf memory-model document
- Time: 2026-09-15T09:00:00Z
- Type: Changed
- Cited:
  - [Linter](./linter.md) — Consumed contract: safety checks are governance this protocol states and that protocol checks.
  - [Compiler](./compiler.md) — Consumed contract: uninitialized reads are ontology; teardown automation may emit source.
- Propagates to:
  - memory.handoff.md: Done — Khayyam-shelf relocation item closed; generated-source convention and binary-mutation questions recorded.
  - memory_model.md: Done — retired and deleted; managerial positions absorbed here.
  - memory_model.handoff.md: Done — retired and deleted; surviving questions merged.
  - khayyam.md: Done — grammar facts kept; pointers retargeted here; later entry places realization notes.
  - variable.md / variable.handoff.md: Pending at absorb time — closed in the following entry.
  - control-flow.md: Done — presence/absence candidate retargeted to Absence is a type's contract.
  - agency.md / agency.handoff.md: Done — safety-trade-off and teardown-path pointers retargeted.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [Grok](../../CONTRIBUTORS.md#grok) (Grok 4.6 via Cursor) — rewrote

#### What changed
- The document now carries a third movement: reclamation, teardown, and layout optimization are toolchain and library concerns, not language-syntax concerns, and the same requirements bind a C or Go toolchain without those languages growing new grammar.
- Automation of path-complete release, when a toolchain performs it, emits explicit source the program includes — a generated file, a temporary compilation unit, or a checked-in companion — rather than hidden insertion or lifetime annotations in the author's source.
- Safety checks are governance, relaxable by organization; uninitialized reads remain a compiler or linter refusal of existence; allocators are libraries; layout optimization is a separable orchestration concern stated as a long-term goal; emptiness is a type's contract term, not a universal machine condition.
- Methodology no longer defers reclamation-mechanism choice to a Khayyam-shelf document.
- `memory_model.md` and its handoff are retired and deleted. Grammar facts that document mixed in (`vr` as logical reference, no assignment operator, pass-by-reference) already live in [Khayyam](../khayyam/khayyam.md) and [Variable](../khayyam/variable.md).

#### Deliberation
- A Khayyam-shelf memory-model document implies the language owns memory management, which the grammar-refusal principle contradicts (Omid Hekayati — claimed).
- The managerial requirements must be stated independently of Khayyam, because they are implementable on a C or Go compiler without syntax change; C's currently-manual acquire/release can be automated by writing explicit code into a file, not by magic in the author's source (Omid Hekayati — decided).
- Concatenating the retired file's Khayyam-specific mechanisms into this protocol was rejected; absorbing the positions and deleting the shelf document follows the Control Flow merger (Omid Hekayati — decided).

#### Considered and not done
- **Keeping a Khayyam `memory_model.md` as a realization stub (rejected)**: a near-empty body would still occupy the language shelf and re-create the misreading; grammar facts already have homes.
- **Dumping the retired file's body into this document as a Khayyam chapter (rejected)**: would make the protocol a language specification.
- **Adopting compile-time binary mutation of dynamically-valued constants (not adopted)**: was explicitly undecided in the retired draft's source material; recorded as an open question, not as a requirement.
- **A Rust-style mandatory, unbypassable borrow checker as the default enforcement (rejected in the retired draft; preserved here)**: considered and rejected as the *default* mechanism in favor of a linter-based, organization-swappable one, consistent with framework-over-language placement — the strength of the safety guarantee is then a toolchain-configuration decision, not a language guarantee. (Omid Hekayati — decided in the retired draft's source material)
- **Reading profile-guided heap↔stack migration as an already-solved engineering problem (rejected in the retired draft; preserved here)**: PGO as a discipline is established in toolchains such as LLVM/GCC for performance optimization, but not typically at the scope of automatic allocation-site migration described in the retired draft; that scope remains a long-term architectural goal. Go's Escape Analysis is cited as the motivating counter-example of implicit, non-overridable runtime memory magic; Rust's lifetime annotations as the motivating counter-example of syntactic cost for safety. (from the retired draft's Drawbacks / Prior art)

---

### Place Khayyam realization notes; close variable deferrals after the shelf retirement
- Time: 2026-09-15T13:00:00Z
- Type: Changed
- Cited:
  - [Khayyam](../khayyam/khayyam.md) — Realization: no raw pointers, no `nil` keyword, `Deinit()`/`Free()`/`IsNull()` conventions, escape-analysis and PGO placement.
  - [Variable](../khayyam/variable.md) — Realization: Resource Lifecycle no longer defers to a missing document.
- Propagates to:
  - memory.handoff.md: Done — compatibility-contract future possibility and generated-name candidate recorded.
  - khayyam.md: Done — `How Khayyam realizes Memory` topic added; Variable bullets gain pointer/`nil` facts.
  - variable.md / variable.handoff.md: Done — Resource Lifecycle retargeted here; deferred open questions removed.
  - khayyam.changelog.md / variable.changelog.md: Done — paired entries.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Cursor](../../CONTRIBUTORS.md#cursor) (Composer) — applied

#### What changed
- The audit of the retired shelf file found managerial positions already absorbed, but Khayyam-specific mechanisms and the variable-layer deferral still had no live home; those gaps are closed without reopening a shelf document.
- Surviving deliberative material from the retired draft's Drawbacks, Rationale, and Prior art is preserved in the absorb entry's `Considered and not done` above; the compatibility-contract future possibility lands in this document's handoff.

#### Deliberation
- Realization facts that name Khayyam constructs must live in Khayyam documents, not in this protocol — the same split the absorb entry already decided (Omid Hekayati — decided).
- `variable.md`'s "future document on resource management" was the old shelf by another name; after retirement it would have been a dangling deferral (Omid Hekayati — claimed).

#### Considered and not done
- **Re-creating a Khayyam `memory_model.md` only for realization notes (rejected again)**: a short topic under [Khayyam](../khayyam/khayyam.md) is enough; a separate file would re-shelf the misreading.
- **Editing historical changelog links that still name `memory_model.md` (not done)**: left as provenance, matching the Control Flow merger's practice.
