# Execution Research 001 — M1 readiness of the Khayyam specification

## Table of contents
- [Status](#status)
- [Question and Goals](#question-and-goals)
- [Participants](#participants)
- [Methodology](#methodology)
- [Findings](#findings)
- [Conclusion](#conclusion)
- [Related Artifacts](#related-artifacts)

## Status
Active

## Question and Goals
### Questions
1. Is the Khayyam specification precise enough for an M1 frontend to accept and refuse source on the core forms `tp`, `vr`, and `in`? — **Answered**
2. Are the `.kh` sources under `modules/` viable M1 acceptance inputs and M3 bootstrap inputs — do they hide FFI or body-less-method blockers? — **Answered**

### Goals
1. Produce the readiness record required by [execution.md → Readiness review (Gate)](./execution.md#readiness-review-gate) before M1 code begins. — **Met**
2. Replace the handoff's single question about `khayyam.md` precision with construct-level ratings and a bounded gap list routed for ruling. — **Met**
3. Select concrete `.kh` acceptance inputs and identify the real M3 bootstrap blockers. — **Met**

### Scope
The grammar statements for `tp`, `vr`, and `in` in [khayyam.md](../../docs/khayyam/khayyam.md) plus the companions carrying their rules ([variable.md](../../docs/khayyam/variable.md), [modularity.md](../../docs/khayyam/modularity.md), and [method.md](../../docs/khayyam/method.md) body-less section); all 24 `.kh` files under [`modules/`](../). It writes no compiler code, rates `cp`/`mt`/`ab`/`sc` only where they bear on `tp` shapes, and does not open [docs/protocols/](../../docs/protocols/README.md).

## Participants
- [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — **Questioner**, **Goal-setter**; review outcome: **Not yet reviewed**.
- [Mimo](../../CONTRIBUTORS.md#mimo) (mimo-v2.6-flash via [OpenCode](../../CONTRIBUTORS.md#opencode)) — **Researcher**.

## Methodology
1. Delegated one extraction pass over `docs/khayyam/` to rate each core form's accept/refuse sufficiency, with quotes and anchors for load-bearing claims.
2. Delegated one inventory pass over every `.kh` file under `modules/`, recording constructs used, body-less declarations, FFI markers, import edges, and empty directories.
3. Spot-verified the load-bearing quotes against the primary sources (khayyam.md Type, Scope, and Import sections; variable.md Declaration Syntax; if.kh; weak.kh) rather than trusting the reports wholesale.
4. Routed results per [execution.md → Readiness review (Gate)](./execution.md#readiness-review-gate): host-local findings stay in this folder, language-design gaps go to the paired handoff for ruling.

Limits: the delegated reports were spot-checked, not line-verified in full; no compiler code was written; the owner has not yet reviewed this record.

## Findings
### The three core forms are specified to different depths
`vr` is sufficient for accept/refuse: exactly one name and one type per declaration, no multi-declaration form, no inline initializer ([variable.md → Variable Declaration Syntax](../../docs/khayyam/variable.md#variable-declaration-syntax) — **Evidence**), and no assignment operators exist at all ([khayyam.md → Variable](../../docs/khayyam/khayyam.md#variable) — **Evidence**). `tp` has quotable canonical shapes ([khayyam.md → Type](../../docs/khayyam/khayyam.md#type) — **Evidence**: `tp {name} [Type] [subtype defined value]`, "All things MUST be defined in the shape below to be understood by the Khayyam compiler"), but the template's brackets are never ruled on: no example shows subtype-less `tp {name}` and the `[Type]` slot is not glossed, so negative `tp` tests cannot be written yet. `in`'s two line forms and the deliberate absence of `as` are exact ([khayyam.md → Import Mechanism (`in`)](../../docs/khayyam/khayyam.md#import-mechanism-in) — **Evidence**), while placement, ordering, and failure behavior are not stated.

### Refusal behavior belongs to the implementation
khayyam.md assigns enforcement to the compiler without stating how refusal is signaled — no message shape, diagnostic code, or recovery model appears anywhere under `docs/khayyam/` ([khayyam.md → Separation of Syntax and Governance: A Principle](../../docs/khayyam/khayyam.md#separation-of-syntax-and-governance-a-principle) — **Evidence**: "Syntax defines what exists… The compiler enforces the first"). M1 acceptance tests can therefore assert accept/refuse outcomes only; message text cannot be pinned to the specification.

### The precision gaps that block the M1 accept/refuse matrix
The gap list is recorded as Open Questions in the paired [execution.handoff.md](./execution.handoff.md#open-questions): subtype-less `tp` and the base-template gloss; `in` failure semantics and contracts-first ordering; statement separators and identifier lexics. The `sc` placement rule that gates `tp … sc` acceptance is already open in [khayyam.handoff.md](../../docs/khayyam/khayyam.handoff.md) and is cross-referenced rather than duplicated. Each gap needs a language ruling or an explicit deferral before the matrix freezes; none blocks starting the frontend skeleton.

### The `.kh` sources are an unreviewed idea archive, not a curated library
The 24 files under [`modules/`](../) were transferred here from the archived memar-khayyam repository without review — they were never committed even there — solely so their ideas would not be lost; their state reflects that archival purpose, not library readiness ([inventory] — **Evidence**: 16 carry no code: 2 zero-byte, 13 license-header-only, 1 prose-only; mem.kh and life_cycle.kh carry Go-draft syntax a conforming frontend must refuse). What the archive does establish holds regardless: no file contains an FFI or host-link marker, and the body-less declarations in the Khayyam-dialect files are only the two kinds the language itself names — `ab` contracts and body-less `mt` signatures ([method.md → Body-less Methods (FFI and Contracts)](../../docs/khayyam/method.md#body-less-methods-ffi-and-contracts) — **Evidence**: `tp WeakReference ab` and `tp mt ReferenceAlive …` in weak.kh). Curating which ideas graduate into library design is work to plan; it is not a defect this inquiry discovered, and M3's link-first design does not depend on the archive being finished.

### All five imports dangle
The only import edges in the tree point outside it: `memar/process/error/…` from if.kh, life_cycle.kh, and mutable.kh, and `memar/math/boolean` from concurrency.kh and blocking.kh — neither target exists under `modules/`, and no `.kh` file imports another `.kh` file. Path spelling is not uniform either: mutable.kh writes `tp Error "…"` without the `in` keyword, and if.kh alone appends `.kh` to its path. Both facts are consistent with the archive's unreviewed origin rather than with a designed import surface.

### The archive supplies negative and stress inputs, not positives
At review time six of the archive's files carried testable Khayyam syntax. The selection this finding first made from them is superseded and is not restated; what survives is the paired handoff's "M1 acceptance inputs selected" (revised 2026-09-25, amended the same day) — the M1 positives are fixtures derived from the documented forms, and the archive supplies negative, diagnostic and stress inputs only. On that basis mutable.kh (import written without `in`), weak.kh (the subtype written before the name), concurrency.kh and blocking.kh (a method declaration carrying no `mt`), and life_cycle.kh (mixed dialect) are negatives, if.kh is the dangling-import negative, and mem.kh is excluded as Go-draft; the 16 placeholder files are smoke inputs at best. Two of the original six changed sides, for the reasons in Notes: `panic-recovery.kh`'s empty `cp` is not a fault, and the method declarations in `weak.kh`, `concurrency.kh` and `blocking.kh` match no documented form.

## Conclusion
The specification is ready for M1 to begin the frontend skeleton and semantic representation; it is not yet ready to freeze the accept/refuse matrix, because the enumerated gaps decide negative tests for `tp` and `in`. The readiness gate in execution.md is satisfied by this record: findings are recorded, the gap list awaits ruling in the paired handoff, and the inventory resolves the FFI question negatively — no host-link convention is needed before M3. No governing document changed as a result of this inquiry. The research stays Active until the owner reviews it.

## Related Artifacts
- [execution.md](./execution.md) — the plan whose Readiness review (Gate) this record satisfies.
- [execution.handoff.md](./execution.handoff.md) — carries the gap list, input-selection and link-first decisions, and pending owner review.
- [khayyam.md](../../docs/khayyam/khayyam.md), [variable.md](../../docs/khayyam/variable.md), [modularity.md](../../docs/khayyam/modularity.md), [method.md](../../docs/khayyam/method.md) — the specification under test.
- [Documentation — Research](../../docs/documentation-research.md) — governs this artifact's structure.
- [`modules/`](../) — the `.kh` sources inventoried for M1 and M3.

## Notes
- Owner feedback (2026-09-24, inline review): the findings over-weighted the state of the `.kh` files — they were transferred from memar-khayyam without review, never committed even there, to preserve ideas rather than to seed a library. Provenance was added to the affected findings; the FFI and input-selection conclusions stand. Formal review outcome remains open.
- Owner feedback (2026-09-24, second review): the archive's code is not a syntax yardstick — its files may come from different development periods of Khayyam while the syntax is newly considered final; `docs/khayyam/` is the permanent evaluation ground. It follows that the M1-input selection this record first made is superseded as acceptance criteria: the M1 positives become fixtures derived from the documented forms, and the archive supplies negative/stress inputs only (handoff → Decisions, "M1 acceptance inputs selected", revised). Related discovery: the archive's method declarations (`tp mt ReferenceAlive …` in weak.kh; `tp IsAsync …` with no `mt` in concurrency.kh/blocking.kh) match no documented form — further evidence of the archive's mixed periods, not a language question in either direction.
- Rulings landed (2026-09-25): the Open Questions routed by this research are closed in the paired handoff — Q1 (subtype required, `[Type]` retired) and Q3 (separator, identifiers) applied to khayyam.md with a changelog entry; Q2's failure outcomes overruled out of language documentation and moved to the rule catalog. The `tp` template quoted in the Findings reflects the specification state at review time, which is what this record is evidence of; the live spec now carries the ruling.
- Correction (2026-09-25): the finding that `panic-recovery.kh` is a negative input on account of its empty `cp` is withdrawn — the documentation imposes no emptiness constraint on a capsule (encapsulation.md → Capsule Structure and Privacy states what a capsule can contain, never a minimum), so the file is reclassified as accepted smoke input; the handoff's input decision carries the amendment. The rest of the finding stands.
- Correction (2026-09-27): the finding that gave the M1-input selection is no longer stated as a selection, only as what the archive supplies; the two entries above had already reversed it, and a record that preserves a rejected position is a position that will be read as current.
- Ruling landed after this record (2026-09-26): the `sc` placement item the gap list cross-references is closed — where a code scope may be declared is this toolchain's rule, not the language's, and it is stated at [rules/scope-placement/](./rules/scope-placement/scope-placement.md). The `tp … sc` acceptance rows freeze on that rule, and the language documents no placement. Nothing else this record lists is still open.
