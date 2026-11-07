# Retrieval label posting
## Model
A **derived index entry**, not a second meaning of Label’s attach edge.
- Far ends for lookup: a [Label](/modules/knowledge/label/label.md) (word or phrase) and a text id (`Field_TextID`).
- On the same record: **scope** (`Field_Text_Scope`) and **holder** (`Field_Text_Holder`) — which population, and which thing holds that text for this entry.
- Written by `Text_Index_Upsert_Labels.Do` via `Text_Index_Label_Postings.Replace`; retired with the entry through `Text_Index_Store.Retire*`. Read through store postings by score/find.
- Not `(thing)-[:label]->(label)`. That edge is Label’s. This posting only materializes “this label appears in this held text” for retrieval.

## Why holder is on the posting
Find and rank answer **holders** (e.g. tasks), not text nodes alone.
One text can have many holders: document `D` named by tasks `A` and `B`. A hit on a label of `D` must surface both `A` and `B`. Scope only says the population (e.g. task texts); it does not separate `A` from `B`. A posting that stored only `(label → text)` would force every search to re-discover holders outside the index.
So the stored fact is the entry `(scope, holder, text, label)`. Authoritative “who holds this text” still belongs with the caller/holder relation; the posting copies it for lookup.

## Placement
Belongs to pluggable [Retrieval](../../retrieval.md); not a kernel Text edge.
