# Type (`modules/computer/type/`)

## What this folder is
The realization of [Type](../../../docs/type.md) in this repository: the Khayyam declarations that give semantic entities an identity, a contract, and a place in the type model. It is the module named after the concept it realizes, per the owner's ruling of 2026-10-05 recorded in [the Type handoff](../../../docs/type.handoff.md) — before that it was `datatype/`, a name chosen to dodge Go's `type` keyword, and that reason expired when the units became `.kh` and the language's declaration keywords are `tp` and `vr` ([`bundles/khayyam/core/src/scan.ts`](../../../bundles/khayyam/core/src/scan.ts)). Nothing in Khayyam reserves `type` or `Type`.

The folder was renamed from `datatype/` on 2026-10-08. It holds no document of its own beyond this README: the concept's definition, its four categories (Capsule, Method, Abstraction, Scope), and the boundary of what is not a Type are all stated in [`docs/type.md`](../../../docs/type.md), and this folder realizes rather than restates them.

## Membership criterion
A folder belongs under this module when it carries a Khayyam realization of a Type as [`docs/type.md`](../../../docs/type.md) defines one — a declaration that gives a domain concept an explicit identity and a defined contract — and when the abstractions beside it exist only to describe such a Type: what identifies it, what documents it, and what life cycle it is in. On that criterion the following are members and nothing else is:

- **`protocol/`** — the abstractions a Type is stated through: `DataType` and the identity (`Datatype_ID`), detail (`Details`, `Quiddity`), and life-cycle (`Datatype_LifeCycle`) abstractions composed into it, plus their `Observer_*` counterparts.
- **`services/id/`** and **`tests/`** — capsules that satisfy those abstractions, and the archived statements of that satisfaction.

## What does not belong here
- **The definition of Type, and any of its categories.** That belongs to [`type.md`](../../../docs/type.md); a module realizing a concept does not restate the concept, and this folder names nothing the document does not already settle.
- **A collection of Types.** A container or a registry over `DataType` is a different subject with its own boundary — how many of a thing there are, and how one is found — and it lives at [`modules/computer/datatypes/`](../datatypes/). The collision between the two folders' names, recorded as open in [the Modularity handoff](../../../docs/modularity.handoff.md), is settled by the rename above: `type/` takes the concept's own name and `datatypes/` keeps the plural, which is what its subject is.
- **The archived Go package path `memar/computer/datatype/protocol`.** Many files here, and files across the corpus, carry it inside `// TODO(go-migrate)` comments. It is residue of an attempt to develop these ideas in Go that failed, and the owner has ruled that it is neither evidence nor a premise in reasoning, so it is left as written rather than re-pointed at the folder's new name. The [Import Address rule](../../../bundles/khayyam/rules/import-address/import-address.md) governs the spelling of an `in` URI, and no `in` URI in these files names that path.
