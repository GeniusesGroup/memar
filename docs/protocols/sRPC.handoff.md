# sRPC Handoff

Open work for `protocols/sRPC.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../documentation-handoff.md) for what a handoff is.

## Open Questions

### The wire-level cancellation contract
- State: [Process → Requests, Cancellation, and Timeout](../../process.md#requests-cancellation-and-timeout) defers the wire-level contract here: the shape of a cancellation request, who is authorized to issue one for a given in-flight call, what acknowledgment the executing side returns, and what the requester may conclude from silence. The frame model will need a frame type (or an agreement on payload semantics) — not yet designed.
- Next: design jointly with the frame registry's next revision.

### The library-broker delivery machinery's wire shape
- State: the Position on Message Brokers wraps the application's own store with this protocol's acknowledgement discipline; what that wrapping looks like on the wire (persistent-queue frames, retry semantics, durable-delivery flags) is unspecified.
- Next: design after the cancellation contract settles, on the same frame model.
