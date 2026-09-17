# Software Handoff

Open work for `software.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](./documentation-handoff.md) for what a handoff is.

## Open Questions

### Design versus Engineering as distinct concerns
- State: recovered 2026-09-17 from an audit of Omid Hekayati's Telegram-group messages (Go Engineers, Gommunity, 2023-2025). A recurring owner position, stated multiple times across sessions: **design and engineering are distinct modes of development work that must not be conflated** — design creates or reshapes the requirements themselves (what the data and processes should be), while engineering implements existing requirements into software; architecture belongs on the design side of that line, which is why it demands cross-disciplinary knowledge beyond software engineering alone, and the industry's conflation of the two (software engineers drifting into service design) is named a recurring failure. The framework's documents treat Design and Engineering as ordinary vocabulary and never define or separate them — no document owns the distinction, and software.md's lifecycle treatment will need it (its concern-space mapping uses the IEEE family, which mixes both).
- Next: the dedicated session that refines the software definition should state the distinction in Memar's own vocabulary (likely as a [Process](./process.md)/[System](./system.md)-level pair of modes or a terminology layer entry), after checking what prior design/engineering discussions in the project's chats may have already settled.

### Refining the definition into Memar's vocabulary
"Software is the objective manifestation of a system of aggregated processes" is the directed position, recorded as settled in the document; its refinement into the framework's own vocabulary is owed: how "aggregated processes" maps to [Process → Process Composition](./process.md#process-composition), whether software is a *kind* of System or a lens on systems that carry process compositions ([System](./system.md)), and what "objective manifestation" implies for the definition/execution boundary ([Type → Structure Is Fixed by Definition](./type.md#structure-is-fixed-by-definition)).

### Scope boundary of the software system
Whether a software system includes its data, its deployment environment, and its documentation — or only its definitional artifacts — is undecided. The IEEE family treats configuration items broadly (code, documents, and environments are all configuration items); the dedicated session should take a position rather than inherit the breadth silently.

### Standard successor verification
The IEEE numbers cited (730, 828, 829, 830, 1012, 1016, 1028, 1058, 1063) reflect the classic family; several have been superseded by joint ISO/IEC/IEEE revisions (e.g. 830 by 29148, 829 by 29119-3, 1063 by 26514) — verify each at citation time in the dedicated session before relying on any successor mapping.

## Anticipated Work

- Dedicated session to refine the definition and produce the lifecycle treatment — the direction the [Immutable Infrastructure handoff](./protocols/immutable_infrastructure.handoff.md) points to as the home for deployment/change governance's lifecycle working-out.
