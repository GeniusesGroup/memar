# sRPC — Application Protocol Handoff
Open work for `protocols/sRPC.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../documentation-handoff.md) for what a handoff is.

## Open Questions

### The wire-level cancellation contract
- State: [Process → Requests, Cancellation, and Timeout](../process.md#requests-cancellation-and-timeout) defers the wire-level contract here: the shape of a cancellation request, who is authorized to issue one for a given in-flight call, what acknowledgment the executing side returns, and what the requester may conclude from silence. The frame model will need a frame type (or an agreement on payload semantics) — not yet designed. This does not block reading the rest of the protocol; it blocks treating cancellation as specified on the wire.
- Next: design jointly with the frame registry's next revision.

### The library-broker delivery machinery's wire shape
- State: the [Position on Message Brokers](./sRPC.md#position-on-message-brokers) wraps the application's own store with this protocol's acknowledgement discipline; what that wrapping looks like on the wire (persistent-queue frames, retry semantics, durable-delivery flags) is unspecified. This does not block the position itself; it blocks implementing durable delivery as a wire contract.
- Next: design after the cancellation contract settles, on the same frame model.

### Close-Stream `Reason` identification
- State: [Close-Stream](./sRPC.md#close-stream-frame) carries `Reason uint64`. Whether `Reason` is an Error ID — the same identification as the Error frame's `ErrorID` / [MediaTypeID](./media-type.md) of an error media type — is unsettled. The field exists; its identifier space does not. This does not block the rest of the protocol; it blocks treating Close-Stream as an error-carrying frame.
- Next: decide when Error identification is next revised, jointly with [Error ID](./sRPC.md#error-id).
