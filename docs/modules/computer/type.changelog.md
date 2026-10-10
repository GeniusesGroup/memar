# The Type Changelog

## Changelog

### Created as the Type module's specification
- Time: 2026-10-10T07:40:00Z
- Type: Added
- Cited:
  - [Type](../../type.md) — Depends_on: every requirement here is derived downward from its identity, stateless-Type, Type-metadata, and structure-fixed-by-definition sections.
  - [The Error](../process/error.md) — Evidence: the consumer whose composition shows what is read off a Type — its identity, its details, and its four named life-cycle positions.
  - [Modules](../README.md) — Depends_on: module specifications are language-independent, so declaration names stay with the realization.
- Propagates to:
  - [Type](../../type.md): Done — the companion-artifact layout, generated bindings, and translator-workflow requirement left its Human-facing identity section and are stated here; its abstract principle stays there.
  - [Type Practice](../../type.practice.md): Done — the per-language companion-artifact example, generated bindings, and editing-workflow item left Carrying Type metadata and are stated here.
  - [Type handoff](../../type.handoff.md): Done — the life-cycle position-set question and the rule-checking-strategy question moved to [this document's handoff](./type.handoff.md), with the delegation-pattern-library item.
  - [`modules/computer/type/README.md`](../../../modules/computer/type/README.md): Done — links this document as the module's specification, and cites this changelog for the folder rename instead of Type's handoff.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Cursor](../../../CONTRIBUTORS.md#cursor) (Auto; underlying model not reported) — drafted, applied

#### What changed
- Created under the owner's ruling of 2026-10-10 that base documents at `docs/` root engage their concept abstractly and carry no realization content, and that module specifications are language-independent as well: what was wrong in the Type base documents moved to the document it belongs to, and this one was opened to receive the module-level part.
- The body states what the module owns, a Type's two identifiers, its details and human-facing identity, its life-cycle position, reading a Type, crossing implementation languages, implementation intent, and where the module is realized. It names no declaration of the realization.
- Open points found while drafting went to the handoff rather than the body: the life-cycle position set, the rule-checking strategy, the short identifier's uniqueness context and whether the universally unique identifier is read through the Type, and how companion artifacts relate to text returned by methods.

---

### Realization folder renamed from `datatype/` to `type/`
- Time: 2026-10-10T07:40:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Cursor](../../../CONTRIBUTORS.md#cursor) (Auto; underlying model not reported) — recorded

#### What changed
- The realization folder `modules/computer/datatype/` was renamed [`modules/computer/type/`](../../../modules/computer/type/) on 2026-10-08, under the owner's ruling of 2026-10-05 that the module takes the concept's own name. Every `in` URI naming the old path was migrated with it: 41 URIs across 37 `.kh` files, as the applying session counted them.
- The reason for the old name had expired: `datatype` was chosen to dodge Go's `type` keyword, and the units are now `.kh`, whose declaration keywords are `tp` and `vr` ([`bundles/khayyam/core/src/scan.ts`](../../../bundles/khayyam/core/src/scan.ts)), so nothing reserves `type` or `Type`.
- This entry records a result first held in Type's handoff, which no longer carries it. The same handoff entry reported on 2026-10-08 that the rename could not be committed apart from another session's uncommitted edits in the same `.kh` files; that state was not re-measured when this entry was written.

---

### `modules/computer/datatypes/` kept as the collection-of-Types module
- Time: 2026-10-10T07:40:00Z
- Type: Decided
- Contributors:
  - [Cursor](../../../CONTRIBUTORS.md#cursor) (Auto; underlying model not reported) — recorded

#### What changed
- Judged on 2026-10-08 and recorded here from Type's handoff: [`modules/computer/datatypes/`](../../../modules/computer/types/) is kept beside `type/`, and keeps its plural.
- Its declarations are about what the Type folder declares nothing of: a registry keyed by a Type's identifier, a container of Types, and an observer over that container. A collection of Types is a different subject from a Type, so the folder is not a duplicate of this module.
- It is also live: other modules import it, and a test matrix row accepts it, so retiring it would have deleted reachable declarations rather than residue.
- The `dt-` filename prefix and the `Computer_`-prefixed declaration in that folder are a naming question about the computer layer's vocabulary, recorded in [the Modularity handoff](../../modularity.handoff.md), not about this module.

---

### Declaration family renamed from `DataType` to `Type`
- Time: 2026-10-10T07:40:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Cursor](../../../CONTRIBUTORS.md#cursor) (Auto; underlying model not reported) — recorded

#### What changed
- On 2026-10-10 the owner ruled that the realization's declarations take the concept's own name, and the whole family in `modules/computer/type/` was renamed: `DataType` → `Type`, `DataType_Details` → `Type_Details`, `Datatype_ID` → `Type_ID`, `Datatype_UUID` → `Type_UUID`, `Datatype_LifeCycle` → `Type_LifeCycle`, `Observer_DataType` → `Observer_Type`, `Observer_Datatype_*` → `Observer_Type_*`, `GetDataType` → `GetType`, `GetDataTypeID*` → `GetTypeID*`, and `GetDataTypeUUID*` → `GetTypeUUID*`.
- The rename was applied with Khayyam's binding-aware rename tool, [`bundles/khayyam/services/rename/rename.ts`](../../../bundles/khayyam/services/rename/rename.ts). The toolchain's accept/refuse check stood at 1210/6 before and after. The first step, `DataType` alone, touched 29 files and 61 bound occurrences.
- The folder's membership criterion in its README now names the renamed declarations.
- Names of the same family in other modules were deliberately left for those modules' own sessions: the `*_DataType` names in `adt/container`, the `DataTypes_*` names in `datatypes/`, and `GetDataType` in `process/event`.
- This resolves the naming question Type's handoff carried, which no longer carries it.

---

### `DataType` names renamed outside the realization folder
- Time: 2026-10-10T07:44:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Cursor](../../../CONTRIBUTORS.md#cursor) (Auto; underlying model not reported) — renamed, recorded

#### What changed
- On 2026-10-10 the owner ruled that every `DataType` trace leaves the corpus: `datatype` was a name chosen to dodge Go's `type` keyword, and it is a deficient form of the concept Type. The names the previous entry left for other modules were renamed with the same binding-aware rename tool, [`bundles/khayyam/services/rename/rename.ts`](../../../bundles/khayyam/services/rename/rename.ts):
  - In `modules/computer/adt/container/protocol/`: `READONLY_DataType` → `READONLY_Type`, `Accessor_DataType` → `Accessor_Type`, `Contain_`, `Count_`, `GetElement_`, `Index_`, `Iteration_`, `Iterate_` and `Peek_DataType` → `…_Type`, and `Container_<X>_DataType_<X>` → `Container_<X>_Type_<X>` for the same seven operations.
  - `modules/computer/datatypes/` → [`modules/computer/types/`](../../../modules/computer/types/), with its files `data-types.kh` → `types.kh`, `dt-data-types.kh` → `dt-types.kh` and `dt-data-types.observers.kh` → `dt-types.observers.kh`, and its declarations `DataTypes_Map`, `DataTypes_Map_Register`, `DataTypes_Map_GetByID` → `Types_Map`, `Types_Map_Register`, `Types_Map_GetByID`, `Computer_DataTypes` → `Computer_Types`, `Observer_DataTypes` → `Observer_Types`, and `GetDataTypes` → `GetTypes`. The folder keeps the plural, because its subject is a collection of Types.
  - In `modules/process/event/event.kh`, Event's `GetDataType` → `GetType`, the method by which it satisfies `Observer_Type`.
- The toolchain's accept/refuse check stood at 1210/6 throughout.
- Archived Go and JS residue inside `// TODO(go-migrate)` and `// TODO(js-idea)` comment blocks, and `//memar:impl memar/computer/datatype/...` markers, are left as written: the owner's ruling holds them residue, not evidence.
- Live mentions in documents were updated to the new names and paths; the `dt-` filename prefix and the `Computer_`-prefixed declaration stay an open question in [the Modularity handoff](../../modularity.handoff.md) under their new names.
