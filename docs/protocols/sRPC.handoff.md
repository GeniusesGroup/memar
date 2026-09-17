# sRPC Handoff

Open work for `protocols/sRPC.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../documentation-handoff.md) for what a handoff is.

## Open Questions

### The address/identity decomposition as this protocol's design rationale
- State: recovered 2026-09-16 from an audit of the retired `sRPC - chatgpt.md` chat (2025-07 → 2026-08 sessions). The chat's convergent conclusion, judged by both participants a candidate for a Memar architectural principle, was that routing identity, service identity, operation identity, and request identity are four distinct concepts that HTTP's URL collapses into one string for convenience, and that sRPC — if it is to be a genuinely new protocol rather than a re-encoded URL — must model them independently (Service Frame and Error ID fields, per-request stream identity, payload separate from addressing), with HTTP demoted to one transport/adaptation possibility rather than the conceptual foundation. The chat's stated caution — record it as design rationale and critique of existing network addressing first, formalize the principle only with more evidence — was never carried into any document: the protocol document's body states the frame mechanics ([Service Frame](./sRPC.md#service-frame), [Service ID](./sRPC.md#service-id)) without the four-identity decomposition or the URL critique behind them, and the frame model is indeed built that way (self-describing frames, no URL semantics, transport-independent over Chapar/GP/IP), so the *design* followed the principle while the *record* of why was lost.
- Next: when this protocol's document next grows its rationale layer, add the four-identity decomposition as design rationale (with the path/query mixing critique as prior-art analysis); the deeper principle — an address should contain only information required to determine the destination; request data does not belong in the routing address — belongs at the [Networking](./networking.md) or protocol-concept layer, not here.

### The wire-level cancellation contract
- State: [Process → Requests, Cancellation, and Timeout](../../process.md#requests-cancellation-and-timeout) defers the wire-level contract here: the shape of a cancellation request, who is authorized to issue one for a given in-flight call, what acknowledgment the executing side returns, and what the requester may conclude from silence. The frame model will need a frame type (or an agreement on payload semantics) — not yet designed.
- Next: design jointly with the frame registry's next revision.

### The library-broker delivery machinery's wire shape
- State: the Position on Message Brokers wraps the application's own store with this protocol's acknowledgement discipline; what that wrapping looks like on the wire (persistent-queue frames, retry semantics, durable-delivery flags) is unspecified.
- Next: design after the cancellation contract settles, on the same frame model.
