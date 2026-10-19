# Inventory

## Model

- `(batch)-[:product_inventory]->(invoice)`

## Discussion

### Unresolved questions

- Inventory valuation basis: FIFO, weighted-average, and batch recorded cost stay for accounting, while [replacement cost](../replacement-cost/replacement-cost.md) is the pricing basis ([decision](../pricing/edges/pricing/pricing.md#decisions-2026-10-10)). Does a valuation of stock held read one of them, or show both with the holding gain between them, and is the basis a field of the valuation so neither is shown as the other ([replacement cost → Unresolved questions](../replacement-cost/replacement-cost.md#unresolved-questions))?

## Idea backlog

Nothing below is ratified.

### Transfer re-index sketch
- **Idea**: a comment-only `Transfer` migration: read each record file of a legacy product-inventory datastore, parse it (`FromSyllab`), move the record's old `QuiddityID+OwnerID` / `QuiddityID+DCID` index hash files out of the hash store into the delete buckets, and rewrite the daily indexes (`IndexRecordIDForQuiddityIDOwnerIDDaily`, `IndexRecordIDForQuiddityIDDCIDDaily`, plus the `ReferenceID` owner chain) — a one-shot re-index of old inventory records (paths hard-coded to one SabzCity datastore).
- **Review questions**: is this a supported migration the module must keep, or throwaway tooling to discard (hard-coded absolute paths) before the module shape is fixed?

### Record indexes
- **Idea**: primary indexes — a RecordID chain per `QuiddityID+OwnerID` and per `QuiddityID+DCID`, written "in each update to the exiting record!" via a Ganjine broadcast `HashSetValue`; secondary — `ReferenceID` daily chain; each key is `sha512.Sum512_256(structureID + ids + field name)`.
- **Review questions**: do these keys belong to the module's storage contract (`protocol/`) or stay infrastructure-internal? Who owns the "Daily" roll-up semantics?

### Index write retry
- **Idea**: unresolved TODO recurring in both primary index setters — the record write already succeeded, so a failed index write must be retried: "TODO::: we must retry more due to record wrote successfully!" (today the error is only logged, debug-gated by `protocol.AppDebugMode`).
- **Review questions**: retry owner — storage layer, [inventory-notify.kh](protocol/inventory-notify.kh), or a rule/event? Does the daily secondary index need the same guarantee?
