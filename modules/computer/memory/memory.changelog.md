# Memory Changelog

## Changelog

### Initial draft — memory semantics as contract (as "Memory Management")
- Time: 2026-09-06T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — claimed, argued
  - [Super Z](../../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — reviewed, rewrote

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
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — claimed, argued, corrected
  - [Super Z](../../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — reviewed, argued, rewrote

#### What changed
- The document now moves definition-first: memory defined as the class of all state-retaining capacities.
- Volatility (volatile/semi-volatile/non-volatile) is adopted as the classifier.
- The memory/storage dichotomy is rejected as an industry convention, with the attribution correction recorded.
- The reclamation question is shown inescapable: manager inescapable, collector optional; cost moves, never disappears.
- The reclamation mechanisms are classified, with runtime tracing GC as one family among several.
- The contract rules of the initial draft are retained unchanged as the document's second half.
- The concept-vs-label pattern this rejection exercises was written into [type.md](../../../docs/type.md) as "Concepts Outlive Their Labels" (Super Z).

#### Deliberation
- The initial draft's jump into "management" without definitions was judged a writing defect, and the restructure was directed: define memory first, then manage it (Omid Hekayati — directed).
- The definitional positions were brought from public discussions (Omid Hekayati — claimed).
- The correct classifier for memory is **volatility** — volatile, semi-volatile, non-volatile per the standard taxonomy — not the ecosystem's memory/storage two-name split, which is rejected outright, including its attribution to the von Neumann architecture tradition (Omid Hekayati).
- The GC concept is misplaced in the ecosystem: **no language with dynamic allocation escapes the reclamation question** — what languages like Rust actually distance themselves from is *runtime GC mechanisms*, and their ownership scheme is itself automatic reclamation requiring its own tooling, so the mechanisms marketed as "GC" must be classified as one subcategory (runtime GC mechanisms) under the broader spread, or the term becomes incoherent (Omid Hekayati).
- The framing argument from the OS document: a founding layer grants bounded memory entitlements, never per-variable allocation services — so the manager inside the grant is the system's own, and reclamation policy is meaning defined above the guarantee boundary (Omid Hekayati).
- It was directed that the OOP/FP concept-vs-label pattern be recorded in [type.md](../../../docs/type.md) rather than only alluded to here (Omid Hekayati — directed).
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
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — reviewed, decided
  - [Super Z](../../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote

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
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Super Z](../../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — moved, folded

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
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) - claimed, decided
  - [Super Z](../../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) - moved

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
  - [Linter](../linter/linter.md) — Consumed contract: safety checks are governance this protocol states and that protocol checks.
  - [Compiler](../compiler/compiler.md) — Consumed contract: uninitialized reads are ontology; teardown automation may emit source.
- Propagates to:
  - memory.handoff.md: Done — Khayyam-shelf relocation item closed; generated-source convention and binary-mutation questions recorded.
  - memory_model.md: Done — retired and deleted; managerial positions absorbed here.
  - memory_model.handoff.md: Done — retired and deleted; surviving questions merged.
  - khayyam.md: Done — grammar facts kept; pointers retargeted here; later entry places realization notes.
  - variable.md / variable.handoff.md: Pending at absorb time — closed in the following entry.
  - control-flow.md: Done — presence/absence candidate retargeted to Absence is a type's contract.
  - agency.md / agency.handoff.md: Done — safety-trade-off and teardown-path pointers retargeted.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [Grok](../../../CONTRIBUTORS.md#grok) (Grok 4.6 via [Cursor](../../../CONTRIBUTORS.md#cursor)) — rewrote

#### What changed
- The document now carries a third movement: reclamation, teardown, and layout optimization are toolchain and library concerns, not language-syntax concerns, and the same requirements bind a C or Go toolchain without those languages growing new grammar.
- Automation of path-complete release, when a toolchain performs it, emits explicit source the program includes — a generated file, a temporary compilation unit, or a checked-in companion — rather than hidden insertion or lifetime annotations in the author's source.
- Safety checks are governance, relaxable by organization; uninitialized reads remain a compiler or linter refusal of existence; allocators are libraries; layout optimization is a separable orchestration concern stated as a long-term goal; emptiness is a type's contract term, not a universal machine condition.
- Methodology no longer defers reclamation-mechanism choice to a Khayyam-shelf document.
- `memory_model.md` and its handoff are retired and deleted. Grammar facts that document mixed in (`vr` as logical reference, no assignment operator, pass-by-reference) already live in Khayyam (`docs/khayyam/khayyam.md`) and Variable (`docs/khayyam/variable.md`).

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
  - Khayyam (`docs/khayyam/khayyam.md`) — Realization: no raw pointers, no `nil` keyword, `Deinit()`/`Free()`/`IsNull()` conventions, escape-analysis and PGO placement.
  - Variable (`docs/khayyam/variable.md`) — Realization: Resource Lifecycle no longer defers to a missing document.
- Propagates to:
  - memory.handoff.md: Done — compatibility-contract future possibility and generated-name candidate recorded.
  - khayyam.md: Done — `How Khayyam realizes Memory` topic added; Variable bullets gain pointer/`nil` facts.
  - variable.md / variable.handoff.md: Done — Resource Lifecycle retargeted here; deferred open questions removed.
  - khayyam.changelog.md / variable.changelog.md: Done — paired entries.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Composer](../../../CONTRIBUTORS.md#composer) (Composer via [Cursor](../../../CONTRIBUTORS.md#cursor)) — applied

#### What changed
- The audit of the retired shelf file found managerial positions already absorbed, but Khayyam-specific mechanisms and the variable-layer deferral still had no live home; those gaps are closed without reopening a shelf document.
- Surviving deliberative material from the retired draft's Drawbacks, Rationale, and Prior art is preserved in the absorb entry's `Considered and not done` above; the compatibility-contract future possibility lands in this document's handoff.

#### Deliberation
- Realization facts that name Khayyam constructs must live in Khayyam documents, not in this protocol — the same split the absorb entry already decided (Omid Hekayati — decided).
- `variable.md`'s "future document on resource management" was the old shelf by another name; after retirement it would have been a dangling deferral (Omid Hekayati — claimed).

#### Considered and not done
- **Re-creating a Khayyam `memory_model.md` only for realization notes (rejected again)**: a short topic under Khayyam (`docs/khayyam/khayyam.md`) is enough; a separate file would re-shelf the misreading.
- **Editing historical changelog links that still name `memory_model.md` (not done)**: left as provenance, matching the Control Flow merger's practice.

---

### The address-sized integer is carried as a memory-domain question
- Time: 2026-09-28T14:34:08Z
- Type: Added
- Cited:
  - [Math Handoff → Does the tower hold widths the reference does not declare?](../../math/math.handoff.md#does-the-tower-hold-widths-the-reference-does-not-declare) - Premise: the owner ruled that Go `uintptr` belongs to the memory domain, not to the numeric tower.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) - decided
  - Auto (model not recorded) via [Cursor](../../../CONTRIBUTORS.md#cursor) - recorded

#### What changed
- `memory.handoff.md`: a question on which memory declaration receives `uintptr` — `MemoryAddress`, `Memory_Pointer`, or a concept of its own — with the reference's two uses.

#### Considered and not done
- Mapping `uintptr` onto `MemoryAddress` or `Memory_Pointer` now: no document ties either to it, so the choice is left to the owner.

---

### The address-sized integer ruling is cited at its new home
- Time: 2026-09-29T10:40:00Z
- Type: Fixed
- Contributors:
  - Auto (model not recorded) via [Cursor](../../../CONTRIBUTORS.md#cursor) - applied

#### What changed
- `memory.handoff.md → Where does an address-sized integer (uintptr) go?` and this changelog's 2026-09-28 entry cite the owner's ruling at [Math Handoff → Does the tower hold widths the reference does not declare?](../../math/math.handoff.md#does-the-tower-hold-widths-the-reference-does-not-declare).

---

### Numeric tower content moved to protocol documents
- Time: 2026-09-29T11:17:00Z
- Type: Changed
- Cited:
  - [Math](../../math/math.md) - Premise: protocol layer owns the number tower.
- Contributors:
  - Auto (model not recorded) via [Cursor](../../../CONTRIBUTORS.md#cursor) - applied

#### What changed
- `memory.md`: address-sized integers are not numeric widths.
- `memory.handoff.md`: ruling citation repointed to `math.handoff.md`.
- This changelog's 2026-09-28 entry: `Cited` link repointed to `math.handoff.md`.

---

### `heap.kh` and `mem.kh` placement relocated from Modularity handoff
- Time: 2026-09-29T14:00:00Z
- Type: Changed
- Cited:
  - [Modularity Changelog](../../knowledge/modularity/modularity.changelog.md) - Premise: allocator file placement belongs with the memory module, not the Modularity concept.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided
  - Auto (model not recorded) via [Cursor](../../../CONTRIBUTORS.md#cursor) — applied

#### What changed
- `memory.handoff.md`: "Where do `heap.kh` and `mem.kh` belong?" moved from `modules/knowledge/modularity/modularity.handoff.md`.

---

### OS storage topic's volatility vocabulary narrowed to the missing cross-link
- Time: 2026-10-05T09:47:47Z
- Type: Changed
- Propagates to:
  - os.md: Pending — the Storage topic gains a cross-link to [Memory → Volatility: the real classifier](memory.md#volatility-the-real-classifier) and one sentence naming the block grant as non-volatile memory, at its next revision.
- Contributors:
  - [Space Bunny Alpha](../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- The paired handoff's Open Questions entry "Volatility vocabulary in the OS contract's storage topic" narrowed to its residue; no line under Anticipated Work changed, and the entry's title is kept so its anchor survives.
- Recorded as settled: [OS → Storage](../os/os.md#storage-block-abstractions-not-filesystems) already applies the vocabulary — the block grant is "the same kind of answer it provides for volatile memory" and "Non-volatile storage deserves the same restraint" — and already keeps the block-grant framing. Both alternatives the entry weighed are therefore in force, so what was open was not which to choose but what the two documents have not said to each other.
- Residue recorded: the OS storage topic carries no cross-link to this document's volatility classification and never states that the block grant is non-volatile memory under this definition rather than a separate class the two documents happen to name alike.
- The base document's body is unchanged; the other thirteen entries under Open Questions are untouched.

---

### Contract-term requirement stated in the three forms the section already names
- Time: 2026-10-05T17:18:32Z
- Type: Changed
- Contributors:
  - [Space Bunny Alpha](../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- `memory.md` → [Copy and ownership semantics are contract members](./memory.md#copy-and-ownership-semantics-are-contract-members): the requirement as it now stands is that an optimization whose memory semantics no contract term states in the three forms above — whether the caller retains ownership, whether the callee may retain a view, and how long a returned view remains valid — is an optimization the library does not get to make.
- The check that now decides it is per optimized value: the paired contract term read against those three questions, and a term leaving any one of them unanswered is the violation.
- The replaced wording, "an optimization whose contract term cannot be stated simply", named a property no reader can observe, and the three forms it now names are the ones the same section already states as what a method's contract includes.

#### Considered and not done
- Declaring the three forms closed against any fourth contract term: not taken. Whether a form is admitted is the contract's own evolution, and stating it here would make a wording fix carry a design decision it has no evidence for.

---

### Non-volatile memory is reached through a port
- Time: 2026-10-23T17:30:00Z
- Type: Added
- Cited:
  - [Memory Record](../../../modules-plugable/computer/memory/store/record/record.md) - Reference: the contract the new section points to
- Tasks:
  - main:.agents/tasks/20261023-T074641Z-5420/: Partial - the design task of the memory-port programme; the build tasks are queued after it
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — requested the work (2026-10-22/23), ruled the premises it rests on
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — researched and drafted
  - Three sub-agents (Claude, model claude-opus-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — reviewed; their findings are applied, the corrected text was not reviewed again, so no `approved` is recorded

#### What changed
- [memory.md](memory.md) gains the section Non-volatile memory is reached through a port, as the rule against the shadow tier applied.
- [memory.handoff.md](memory.handoff.md) notes under the erasure question that the port offers no removal until it is ruled, and that contents labelled scratch are kept.

---

### The parts of the memory module: state and target
- Time: 2026-10-23T18:10:00Z
- Type: Changed
- Cited:
  - [Record](../../../modules-plugable/computer/memory/store/record/record.md) - Reference: the contract that becomes the one abstraction of retention
- Tasks:
  - main:.agents/tasks/20261023-T074641Z-5420/: Partial - the design task of the memory-port programme
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — steered: the record is the abstraction and no separate port module is wanted; File and Directory belong to the filesystem; the pluggable floor of `computer` is too crowded
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — drafted

#### What changed
- [memory.handoff.md](memory.handoff.md) gains the Tentative decision on where each part of the module belongs: memory proper stays; `record` is the abstraction; `file` and `directory` move to the filesystem module (task queued); `index`, `services` and `sql` are optional and move under the pluggable mirror of `record` when converted.

---

### Retention is reached through one contract: the model of the memory layer
- Time: 2026-10-24T16:10:00Z
- Type: Changed
- Cited:
  - [Memory Handoff](memory.handoff.md#the-model-of-the-memory-layer-2026-10-24-decided-by-the-owner-in-task-20261024-t052936z-22844) - Reference: the rulings the model carries out
  - [Kernel Neutrality](../../knowledge/modularity/rules/kernel-neutrality/kernel-neutrality.md#the-rule) - Reference: the test that leaves the contract in the kernel and the capsules out
- Tasks:
  - main:.agents/tasks/20261024-T052936Z-22844/: Partial - the modelling task; the build tasks it queues carry it out
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — ruled each premise in the chat of the task: one contract parametric in the address, no module of its own for it, the adapters independent of `record`, the file system under memory, `key_value` on `page`, `cluster` a module of its own, and that Task, timeline and Request refer to an address through the memory module
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — proposed, drafted
  - A sub-agent (Claude, model claude-opus-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — critiqued; its findings are applied or recorded in the handoff, the corrected text was not reviewed again, so no `approved` is recorded

#### What changed
- The section "Non-volatile memory is reached through a port" becomes "Retention is reached through one contract": the contract (address, `get`, `list`, `batch`, `state`, `changes`, the guarantees, the capabilities, the suite and `volatile`) is this module's protocol, realized by every capsule; it is also what other kernel modules refer to an address through; and the table of what stays in the kernel and what is pluggable under `modules-plugable/computer/memory/`.
- [memory.handoff.md](memory.handoff.md) gains the decided model, supersedes in part the Tentative entries of 2026-10-23, and opens the questions the critique found: the order of `block` and `page`, the fate of `version.kh` and of the kernel importers of `Storage_Block` and `Storage_Page`, what `services/batch.kh` is, the responsibility of `cluster`, the names of the git adapter and the allocator module, and the Go-era content with no home.

#### Considered and not done
- Keeping `record` in the kernel because Task, timeline and Request name nodes: the critique proposed it; the owner ruled that their link is only the reference to an address, which this module offers.
- A module of its own for the contract: the owner ruled it would be this module's definition under another name.

---

### The contract returns the token, and its added cases are named
- Time: 2026-10-24T17:20:00Z
- Type: Changed
- Cited:
  - [Memory Record](../../../modules-plugable/computer/memory/store/record/record.md#the-contract-suite) - Reference: the suite the new cases join
- Tasks:
  - main:.agents/tasks/20261023-T074641Z-5420/: Partial - the last review of the design before the build
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — ruled the model this completes
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — drafted
  - A sub-agent (Claude, model claude-opus-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — reviewed whether the build could start; its findings are applied, the corrected text was not reviewed again, so no `approved` is recorded

#### What changed
- The token joins the contract; the cases for `state`, `changes` and the address parameters are named; the byte form of a `record` address is stated.

---

### Memory becomes a category: the contract is divided into modules
- Time: 2026-10-26T13:00:00Z
- Type: Changed
- Cited:
  - [Category](../../knowledge/label/labels/category.md#the-rules) - Reference: a category holds no contract and a module holds no module
  - [Category Depth](../../knowledge/label/rules/category-depth/category-depth.md#the-rule) - Reference: where a pluggable module stands
  - [Memory Handoff](memory.handoff.md#the-division-of-the-memory-contract-into-modules-2026-10-26-tentative) - Reference: the division and its reasons
- Tasks:
  - main:.agents/tasks/20261026-T120259Z-16244/: Partial - the division is written and the moves task has its paths; the second division of this document's rules is queued
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — ruled on 2026-10-26 that a category holds no contract and that the contract divides into independent modules
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — designed, drafted
  - A sub-agent (Claude, no CONTRIBUTORS.md entry) — critiqued; its findings are applied, the corrected text was not reviewed again, so no `approved` is recorded

#### What changed
- The section "Retention is reached through one contract" is now a short pointer, with its anchor kept, to the new modules [Address](address/address.md), [Store](store/store.md) (which carries the contract and the table of what stands where), [Volatile](volatile/volatile.md) and [Conformance](conformance/conformance.md). The capsules stand at `modules-plugable/computer/memory/store/`; the guest surfaces and the allocator at `modules-plugable/computer/memory/`.
- The pointer and the address-sized integer are read to the `reference` module, and the ordered contract address is the `address` module's alone.
- The document states that this category is provisional until its remaining rules are divided into modules.

#### Considered and not done
- Task, timeline and Request depending on `address` alone: the critique found the Request and the Task also read and write, so they depend on `store` where they do.
- A home for `protocol/version.kh`: three kernel files import it; the open entry decides it before any move.
- Merging `volatile` into `conformance` or into `store`: the suite needs `volatile` and `volatile` needs `store`, so the suite cannot be the store's tests.

---

### The capsules moved out of the kernel and the memory protocol folder is gone
- Time: 2026-10-26T14:10:00Z
- Type: Changed
- Cited:
  - [Memory Handoff](memory.handoff.md#the-division-of-the-memory-contract-into-modules-2026-10-26-tentative) - Reference: the division and the paths the moves use
- Tasks:
  - main:.agents/tasks/20261024-T160310Z-25344/: Partial - the files moved with `git mv` and the links and addresses repaired; the second division and the build tasks are still owed
- Contributors:
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — carried out the move and repaired the links; no `approved` is recorded

#### What changed
- `block`, `page`, `record`, `index` (with `index-one_one`), `cluster` (`cluster`, `manifest`, `metrics-v0`, `errors`), `lockable`, `nonvolatile`, `view`, `key_value` and `graph` stand at `modules-plugable/computer/memory/store/`; `sql` and `allocator` (`heap.kh`, `mem.kh`) at `modules-plugable/computer/memory/`; `file` and `directory` in the `filesystem` module.
- The file extension declarations moved to `modules/computer/mediatype/protocol/` (that module keeps no changelog). `protocol/version.kh` moved to the kernel module `version/`; `protocol/` is gone. The `Clone_Storage_*`, `Copy_Storage_Block` and `Move_Storage_Page` declarations left the marker protocols for the capsules that own the types.
- `services/` keeps `batch.kh` and `transaction-manager.kh` until the open entry on `batch` is resolved.

#### Considered and not done
- Moving `address/pointer.kh` and the pointer declarations to `reference`: the build of the contract does it.
