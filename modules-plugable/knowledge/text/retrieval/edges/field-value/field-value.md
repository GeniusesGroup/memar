# Retrieval field value
## Model
- Derived with the same entry key as label posting: scope, holder, text id (`Field_TextID`), plus a `Type_UUID` key and a `MemoryAddress` value.
- Written by `Text_Index_Upsert_Fields.Do` (neighbour registrars supply the fields); removed when the entry is retired via `Text_Index_Store.Retire*`.
- Read by `Text_Index_Score_Service.Do` via `GetFieldValue*` / `EntryMatchesPreds` on `Text_Index_Store`.

## v1 bound
Membership under a neighbour-chosen `Type_UUID` only. No further field semantics here until a bounded neighbour contract exists. This module does not interpret the keys.

## Placement
Belongs to pluggable [Retrieval](../../retrieval.md); not a kernel Text edge.
