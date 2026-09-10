# Software Handoff

Open work for `software.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](./documentation-handoff.md) for what a handoff is.

## Open Questions

### Refining the definition into Memar's vocabulary
"Software is the objective manifestation of a system of aggregated processes" is the directed position, recorded as settled in the document; its refinement into the framework's own vocabulary is owed: how "aggregated processes" maps to [Process → Process Composition](./process.md#process-composition), whether software is a *kind* of System or a lens on systems that carry process compositions ([System](./system.md)), and what "objective manifestation" implies for the definition/execution boundary ([Type → Structure Is Fixed by Definition](./type.md#structure-is-fixed-by-definition)).

### Scope boundary of the software system
Whether a software system includes its data, its deployment environment, and its documentation — or only its definitional artifacts — is undecided. The IEEE family treats configuration items broadly (code, documents, and environments are all configuration items); the dedicated session should take a position rather than inherit the breadth silently.

### Standard successor verification
The IEEE numbers cited (730, 828, 829, 830, 1012, 1016, 1028, 1058, 1063) reflect the classic family; several have been superseded by joint ISO/IEC/IEEE revisions (e.g. 830 by 29148, 829 by 29119-3, 1063 by 26514) — verify each at citation time in the dedicated session before relying on any successor mapping.

## Anticipated Work

- Dedicated session to refine the definition and produce the lifecycle treatment — the direction the [Immutable Infrastructure handoff](./protocols/immutable_infrastructure.handoff.md) points to as the home for deployment/change governance's lifecycle working-out.
