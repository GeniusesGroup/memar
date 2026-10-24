# Software Handoff
Open work for `software.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../../../modules-plugable/knowledge/documentation/handoff/handoff.md) for what a handoff is.

## Open Questions

### Design versus Engineering as distinct concerns
- State: recovered 2026-09-17 from an audit of Omid Hekayati's Telegram-group messages (Go Engineers, Gommunity, 2023-2025). A recurring owner position, stated multiple times across sessions: **design and engineering are distinct modes of development work that must not be conflated** — design creates or reshapes the requirements themselves (what the data and processes should be), while engineering implements existing requirements into software; architecture belongs on the design side of that line, which is why it demands cross-disciplinary knowledge beyond software engineering alone, and the industry's conflation of the two (software engineers drifting into service design) is named a recurring failure. The framework's documents treat Design and Engineering as ordinary vocabulary and never define or separate them — no document owns the distinction, and software.md's lifecycle treatment will need it (its concern-space mapping uses the IEEE family, which mixes both).
- Next: the dedicated chat that refines the software definition should state the distinction in Memar's own vocabulary (likely as a [Process](../process.md)/[System](../../../docs/system.md)-level pair of modes or a terminology layer entry), after checking what prior design/engineering discussions in the project's chats may have already settled.

### Refining the definition into Memar's vocabulary
"Software is the objective manifestation of a system of aggregated processes" is the directed position, recorded as settled in the document; its refinement into the framework's own vocabulary is owed: how "aggregated processes" maps to [Process → Process Composition](../process.md#process-composition), whether software is a *kind* of System or a lens on systems that carry process compositions ([System](../../../docs/system.md)), and what "objective manifestation" implies for the definition/execution boundary ([Type → Structure Is Fixed by Definition](../../../docs/type.md#structure-is-fixed-by-definition)).

### Scope boundary of the software system
Whether a software system includes its data, its deployment environment, and its documentation — or only its definitional artifacts — is undecided. The IEEE family treats configuration items broadly (code, documents, and environments are all configuration items); the dedicated chat should take a position rather than inherit the breadth silently.

### Standard successor verification
The IEEE numbers cited (730, 828, 829, 830, 1012, 1016, 1028, 1058, 1063) reflect the classic family; several have been superseded by joint ISO/IEC/IEEE revisions (e.g. 830 by 29148, 829 by 29119-3, 1063 by 26514) — verify each at citation time in the dedicated chat before relying on any successor mapping.

### Do the life-cycle declarations of `computer/type` and `computer/capsule` belong to this module
- State: read on 2026-10-17 and not moved. `modules/computer/type/protocol/life-cycle.kh` declares `Type_LifeCycle`, whose Go archive block is the release life cycle of software (`PreAlpha`, `Alpha`, `Beta`, `ReleaseCandidate` and the rest, with a link to the software release life cycle); `life-cycle.observers.kh` gives every Type an `Observer_Type_LifeCycle` with `GetLifeCycle`; `software-life_cycle.kh` in the same place declares an empty abstraction, `SoftwareLifeCycle`; and `computer/capsule/protocol/life_cycle.kh` declares a capsule's own. The bundles' sources implement the Go `LifeCycle()` method on commands and services with `LifeCycle_PreAlpha`, which is a statement about a piece of software's maturity.
- Options:
  1. Move the state set here and leave the observer on Type.
  2. Move the whole declaration here.
  3. Move only the empty `SoftwareLifeCycle` here and leave the rest.
- Anchor: `modules/computer/type/protocol/life-cycle.kh`, `life-cycle.observers.kh`, `software-life_cycle.kh`.
- The question: the state set is software's, since [Software](./software.md) is the document that anchors the software life cycle's concern space, but a Type's carrying a life-cycle state is a property of Type; is the set moved here and the observer left on Type, is the whole declaration moved, or does the empty `SoftwareLifeCycle` alone belong here?
- Path: owner ruling after the life-cycle treatment this document owes; nothing moves before it. The declarations are archive-shaped (a Go block under an empty abstraction), so a move now would carry the block and no decision.
- Blocks continuation: no.

## Anticipated Work
- Dedicated chat to refine the definition and produce the lifecycle treatment — the direction the Immutable Infrastructure handoff ([`immutable_infrastructure.handoff.md`](../../computer/runtime/immutable_infrastructure/immutable_infrastructure.handoff.md)) points to as the home for deployment/change governance's lifecycle working-out.
- Requirements home decision: keep Test's umbrella-requirement reading (a user story is the developed Process's written expectations) as the standing interpretation, or give requirements a named home — under the domain-generality constraint that concrete per-feature artifact sets belong to consuming projects, never to Memar, with no software-only narrowing.
