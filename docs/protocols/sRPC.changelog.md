# sRPC Changelog

## Changelog

### Wire-level cancellation and message-broker position recorded as Open Questions / Position
- Time: 2026-09-06T00:00:00Z
- Type: Added
- Propagates to:
  - process.md: Done — the *Requests, Cancellation, and Timeout* topic added there in the same pass; its first unresolved question defers the wire-level cancellation contract to this document.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed, argued
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — reviewed, rewrote

#### What changed
- Added two new sections: *Position on Message Brokers* and *Open Questions* (the wire-level cancellation contract deferred from process.md's context critique).
- *Position on Message Brokers* records that the standalone message broker duplicates durable persistence per message (application store plus broker store plus the hop between them), which at IoT volumes dominates the storage budget, and that the broker's mechanism belongs in a library within the application's own architecture, with the application's own store as the durability point (Omid Hekayati).
- The section also records the observation that both broker client models (sync session-driven, async trust-the-broker) lose data or structure logic around the broker precisely because the broker is a separate process (Omid Hekayati).
- *Open Questions* records the cancellation position: the framework's application protocol will need an explicit wire-level cancellation contract, whose shape is not yet designed — recorded as an open question rather than an invented frame (Omid Hekayati).
- The broker position was placed in this document rather than chapar.md or a new document, since the delivery machinery it references (acknowledgement scheme, durable queues, retry initiation) is this protocol's own subject matter (Super Z).
- The position was verified against process.md's Events principle (producer-consumer independence) so the library-relocation is not misread as coupling producers to consumers (Super Z).
- The sync/async irrationality observation was kept as a supporting note rather than letting it expand into a redesign proposal (Super Z).
