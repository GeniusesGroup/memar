# Department
Department is a group distinguished as an organizational unit (see group README for the Group-vs-Department decision).

## Idea backlog
Review discipline per `vocabulary-discipline.handoff.md`. Nothing below is ratified. The edge-comment entry lives in the per-edge doc.

### Storage services
- **Idea**: a `StorageServices` interface — entirely commented out in the source: `Save(dm DataModel)`, `Count(departmentID UUID)`, `Get(departmentID UUID, vo VersionOffset)`, `FIND_DepartmentIDs_BY_ParentID(parentID UUID, offset, limit uint64)` — each returning `storage_p.NumberOfVersion` and `error_p.Error`.
