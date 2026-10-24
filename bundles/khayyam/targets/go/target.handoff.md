# Khayyam Go Target Handoff
Open state for [target.md](./target.md). See [documentation-handoff.md](../../../../modules-plugable/knowledge/documentation/handoff/handoff.md) for what a handoff is.

## Topic & Purpose
Where the Go target stands beyond what its main document states: work that is owed to this folder, is not yet written, and is not visible from `target.md` alone. The record of the port's own inquiry is the paired [research](./target.research.001.md).

## Status
Active — the target exists as the bridge that reads Go sources and writes Khayyam ones; what it owes beyond that is stated below.

## Open Questions

### `memar-go`'s conventions are not written down as Rules
The owner ruled on 2026-10-05 that the architectural method is defined in Go, that the Go target stays as a target of the toolchain, and that the conventions `memar-go` held should exist as Rules rather than being lost with the repository that carried them. They belong in this folder's own catalog at [`rules/`](./rules/README.md), beside the three residue Rules already there.

They exist today only as conventions inside that archived repository's code. **The archive is not in this repository**, so nobody can write these Rules from what is here: no document states them, no file carries them, and reconstructing them would be fabrication rather than authorship. That is the whole of what blocks the work.

- Blocks continuation: yes, for authoring any of these Rules. It does not block the three residue Rules, which are written and applied.
- Path: a decision the owner's, on one of two grounds — where the `memar-go` archive is or may be reached from, or how the Rules get written without it. The first makes the conventions readable and the writing a matter of restating them as the Rule model requires; the second must say what a Rule drafted from a memory of the archive may claim, which is the standing question about a source that is not in the tree.
- What a session picking this up should not do: open a Rule folder under [`rules/`](./rules/README.md) and fill it from the residue sources or from the `.kh` files' clue blocks. Those carry the port's residue, not the method's conventions — the distinction is the one the [catalog's membership criterion](./rules/README.md#membership-criterion) draws, and filling a folder from them would put text in the catalog that no evidence here supports.

## Related Artifacts
- [rules/README.md](./rules/README.md) — the catalog these Rules join, and the criterion that says what belongs in it.
- [target.research.001.md](./target.research.001.md) — the port's own record; it names both archives and states that neither was consulted for that inquiry.
