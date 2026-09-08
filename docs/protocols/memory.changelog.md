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
