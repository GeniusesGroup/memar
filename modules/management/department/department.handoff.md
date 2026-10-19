# Department Handoff

## Topic & Purpose
Converting the Khayyam protocol layer of `modules/management/department`: the identity surface (`protocol/dt-uuid.kh`) and the node model (`protocol/model.kh`), under the governing rules in [`../../../Khayyam.practice.md`](../../../Khayyam.practice.md). `git ls-files modules/management/department` returns 10 files; two were sources with declarations and both were converted.

## Status
Protocol layer converted (2026-10-03). Both files accept against the Khayyam frontend, against a root where both `org/…` and `memar/…` resolve.

**The domain is not modelled.** What converted is identity and one model abstraction. The department↔group *typing link* the domain document asks about is answered at the type level by `DepartmentModel` composing `GroupModel`; the department↔group *edge* that the same question is really about has an undecided far end and no code.

## Decisions

- **A department's identity is the thing domain's identity.** *(Decided.)* The Go source wrote `type UUID group_p.UUID`; `group_p.UUID` is itself `user_p.UUID`, which is itself `thing_p.UUID`. Khayyam has no alias form, so the file includes `ThingUUID` from `modules/identity/thing/protocol/dt-uuid.kh` and declares no `DepartmentUUID`. Result parameter `t`, matching `Field_EdgeID` / `Field_EstateID`.
- **`DepartmentModel ab { ThingModel, GroupModel, Target }` — the department↔group typing link belongs here, as a composition.** *(Decided; this is the document's own question, answered.)* [`../group/group.md`](../group/group.md) → Resolved via source inspection settles it: "`department_p.Model` embeds both `thing_p.Model` and `group_p.Model` (Go interface embedding) — Department is a Group (and a Thing) at the compile-time type level, not just conceptually." So the typing link is not an edge here, it is the model's composition, and it is already answered in the document. Writing it as an edge as well would be the second, runtime mechanism the document's unresolved #1 is about.
- **`GroupModel` transitively carries `ThingModel`, and both were kept.** *(Decided.)* `GroupModel ab { ThingModel, UserModel, Target }`, so `DepartmentModel` composing `ThingModel` and `GroupModel` states "a department is a thing" twice. The Go interface embedded both; the redundancy is the source's, and dropping it would silently remove a claim.
- **`event_p.Target[DataModel]` became memar's unqualified `Target`, and the type restriction was lost.** *(Decided, and recorded as a real loss — identical to the group's.)* Khayyam has no generic syntax; memar's `Target` is already converted as `tp Target ab` and accepts any `Event`. `department_p.Model` named `DataModel` — and **this domain has no `data_model.kh`**, so the Go referenced a type its own package did not declare. See Open Questions.
- **`Field_DepartmentID` + `DepartmentID`.** *(Decided.)* The Go already used the `_ID` spelling.

## Open Questions

- **`department_p.Model` referenced a `DataModel` that the department package never declared.** *(Blocking for the record contract, not for the conversion.)* There is no `protocol/data_model.kh` under `modules/management/department/`, and no `DataModel` anywhere in the domain's Go residue. The Go interface embedded `event_p.Target[DataModel]`, so either the record contract was deleted before Phase 1.5 or the interface was always dangling. [`department.md`](department.md) → Idea backlog → Storage services records a `StorageServices` interface that was "entirely commented out in the source" with `Save(dm DataModel)` — the same missing `DataModel`. **A `DepartmentDataModel` was not written**, because nothing in the tree states what a department record holds beyond its identity, and an empty `ab` is what rule 6 forbids. The composition of `Target` above is what the Go did state, and it is all that was written.
- **The department↔group edge has an undecided far end and duplicates the type-level answer.** [`edges-loop/department/department.md`](edges-loop/department/department.md) reads `(group)-[:department]->(---)` — "It can use to show organizational chart. Also staffs can join to the related group." The far end is `---`. If `DepartmentModel` composing `GroupModel` is the typing link, this edge is either the *naming* link (which group in the chart is a department) or a redundant second mechanism — and [`../group/group.md`](../group/group.md) unresolved #1 (static embedding vs runtime type upgrade) is exactly the choice between them, and is unresolved for both domains. Note also that "staffs can join to the related group" is the *group* side of [`../staff/edges/group/group.md`](../staff/edges/group/group.md), which has no code either.
- **`FIND_DepartmentIDs_BY_ParentID` assumes a parent/child department tree, and the document asks whether that is the group parent edge.** ([`department.md`](department.md) → Idea backlog → Review questions.) The answer depends on [`../group/edges/parent/parent.md`](../group/edges/parent/parent.md), which is itself undecided between one edge (`parent_of`) and two (`parent_of` / `parent_is`), and whose open questions include "Does the department organizational chart read this same edge?" A department tree and a group tree are the same relation only if that question is answered yes.
- **The department↔estate edge is a candidate that its own source doubts.** [`edges/estate/estate.md`](edges/estate/estate.md) carries the source's "Isn't it a rule??" and flags convergence with [`../staff/edges/attendance/attendance.md`](../staff/edges/attendance/attendance.md). Nothing to convert; the placement question is live.
- **`edges-loop/recruit/recruit.md` — `(department)-[:recruit]->(---)`, "Recruitment in progress / Active membership recruitment" — has an undecided far end** and no source. A progress flag on a department is more likely a status on the department than an edge to something; whether it belongs to the hiring pipeline in [`../staff/edges/hiring-pipeline/hiring-pipeline.md`](../staff/edges/hiring-pipeline/hiring-pipeline.md) (whose target node is also unconfirmed) is open. Nothing converted.
- **Nothing composes `Field_DepartmentID`.** `git grep Department -- '*.kh'` returns only this domain's two files. The accessor has no consumer, which is the same state `calendar.handoff.md` recorded for `Field_CalendarID` and decided not to act on.

## Role research pointer (2026-10-18)
[`../role/role.research.001.md`](../role/role.research.001.md) analyses this domain with role, staff, shift and calendar. Proposals only (Tentative; nothing ratified) that reach this handoff:
- A department is a group classified as a unit and is the context of positions (`position_in`); the position-level reporting chart is a separate relation from the unit chart, because reporting does not give effective membership upward (Open Question 8).
- `edges-loop/recruit` names two facts, hiring into vacant positions (derived) and a group's open admission; neither is an edge of a department (contradiction 9 there; Open Question 16).

## Related Artifacts

| Artifact | Relation | Action |
| --- | --- | --- |
| [`department.md`](department.md) | Domain document; carries the extracted storage-services idea and the tree-vs-group-edge question | Keep in sync |
| [`../group/group.md`](../group/group.md) | Resolves the department↔group typing link and holds unresolved #1 | Read |
| [`../group/protocol/model.kh`](../group/protocol/model.kh) | The `GroupModel` this model composes | None |
| [`../group/group.handoff.md`](../group/group.handoff.md) | The same identity and `Target` decisions, one domain up | None (read) |
| [`../staff/edges/group/group.md`](../staff/edges/group/group.md) | The staff↔group edge the department doc's "staffs can join" points at | None |
| [`../calendar/calendar.handoff.md`](../calendar/calendar.handoff.md) | The wave that first hit the `Target[DataModel]` loss and the `Field_X` with no consumer | None (read) |
| [`../../../Khayyam.practice.md`](../../../Khayyam.practice.md) | Governing rules 1–7 | None (read) |

## Notes

- **Frontend result.** `modules/management/department/protocol/dt-uuid.kh` and `modules/management/department/protocol/model.kh` — **accept**, two of two. Nothing was suppressed and nothing was refused.
- **How it was verified.** Against `…\khroot_copy\`, built by copying every `.kh` in the organization repository to `org/` and every `.kh` in the memar repository to `memar/`, preserving relative paths (physically — Node does not follow Windows junctions). The run included all eight files this wave wrote across `group`, `task`, `staff` and `department` together: eight of eight accepted, so `DepartmentModel` was checked composing a real `GroupModel` rather than in isolation.
- **Line endings.** Both `.kh` files are CRLF, matching the converted `.kh` files in the repository; this file is LF, matching the Markdown. No BOM in any. Verified by reading the bytes.
- **The `Target` import is unqualified, and that is forced.** A first attempt imported memar's `Target` under the local spelling `Event_Target`; the frontend refused it with `name-not-declared`, because `in` resolves the name *declared* in the target file and memar declares it bare. The `ProcessLog_Event` spelling that appears in `computer/instance_of/edges/audit-log/protocol/data_model.kh` is not a local alias — it is declared *in memar itself*. An `org/` domain cannot rename a `memar/` one.
- **No empty abstraction was written without recording it.** Rule 6 is satisfied by argument: `Field_DepartmentID ab` is empty because the requirement it carries is the accessor beside it and the body is generated (rule 2). `DepartmentModel` is not empty — it carries three compositions the Go interface stated.
