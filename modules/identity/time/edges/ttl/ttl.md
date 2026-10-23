# TTL
Time-to-live: the span after which a record expires.

## Model
- `(time)-[:TTL]->(thing)`

## Policies
- The span is named as a duration. The unit is the realizing capsule's choice and not part of the contract; nanoseconds were the older record's choice, not a floor.

## Open questions
- The edge's near end is a time — an instant — while the surface this edge's protocol states is a span held by a record. The two cannot both be the edge; which one is it? Answering needs a `Time` this repository does not declare (see [`../../time.handoff.md`](../../time.handoff.md)).
- Overlap with law validity, `modules-plugable/rights/law/edges/validity` (time-bounding a law), is unexamined, and it is the same question one level over: a law's validity is a span, and this edge's near end is an instant.
