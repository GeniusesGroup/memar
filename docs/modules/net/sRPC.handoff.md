# sRPC — Application Protocol Handoff
Open work for `protocols/net/sRPC.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../../documentation-handoff.md) for what a handoff is.

## Open Questions

### The wire-level cancellation contract
- State: [Process → Requests, Cancellation, and Timeout](../../process.md#requests-cancellation-and-timeout) defers the wire-level contract here: the shape of a cancellation request, who is authorized to issue one for a given in-flight call, what acknowledgment the executing side returns, and what the requester may conclude from silence. The frame model will need a frame type (or an agreement on payload semantics) — not yet designed. This does not block reading the rest of the protocol; it blocks treating cancellation as specified on the wire.
- Next: design jointly with the frame registry's next revision.

### The library-broker delivery machinery's wire shape
- State: the [Position on Message Brokers](../net/sRPC.md#position-on-message-brokers) wraps the application's own store with this protocol's acknowledgement discipline; what that wrapping looks like on the wire (persistent-queue frames, retry semantics, durable-delivery flags) is unspecified. This does not block the position itself; it blocks implementing durable delivery as a wire contract.
- Next: design after the cancellation contract settles, on the same frame model.

### Close-Stream `Reason` identification
- State: [Close-Stream](../net/sRPC.md#close-stream-frame) carries `Reason uint64`. Whether `Reason` is an Error ID — the same identification as the Error frame's `ErrorID` / [MediaTypeID](../identifier/media-type.md) of an error media type — is unsettled. The field exists; its identifier space does not. This does not block the rest of the protocol; it blocks treating Close-Stream as an error-carrying frame.
- Next: decide when Error identification is next revised, jointly with [Error ID](../net/sRPC.md#error-id).

### A reserved service that delivers a service's SDK
- State: owner proposal (Omid Hekayati, 2026-10-10), not designed: one well-known service, at a reserved [Service ID](sRPC.md#service-id), that any agent or consumer calls to obtain an application's SDK in its own language, or as the signed WASM bundle, so the consumer understands the service locally as text while every exchange on the wire stays binary. A Service ID is the [MediaTypeID](../identifier/media-type.md) of the service media type, so the request is keyed by the service's media type, the consumer's language or form, and the declaration revision. Nothing in [Service ID](sRPC.md#service-id) reserves an identifier today, and a MediaTypeID is computed from a hash of the media type ([Media Type](../identifier/media-type.md)), so "reserved" may mean one well-known service media type whose ID every party computes rather than a number set aside — which of the two is undecided. The proposal ties to [What the declaration artifact is](../process/service-sdk.handoff.md#what-the-declaration-artifact-is), since what the service returns is derived from that artifact, and to [The local/network realization decision surface](../process/service-sdk.handoff.md#the-localnetwork-realization-decision-surface); the consumer side is [The agent as an SDK consumer](../process/service-sdk.handoff.md#the-agent-as-an-sdk-consumer). This does not block the frame model; it blocks specifying SDK delivery over this protocol.
- Next: owner ruling on whether the delivering service is reserved by this protocol or is a well-known service media type, then design jointly with the SDK's [Delivery and versioning](../process/service-sdk.handoff.md#delivery-and-versioning) rules.
