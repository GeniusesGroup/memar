# SDK Handoff

Open work for `protocols/sdk.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../documentation-handoff.md) for what a handoff is.

## Open Questions

### What the declaration artifact is
- State: the SDK is derived from the service's declared interface; what that declaration concretely is — a Memar protocol artifact, the media-type-identified structure inventory, the sRPC service frames, or something new — is undecided.
- Next: design with Media Type and sRPC; the founding prototype's generator input should be recovered before deciding.

### Cache-strategy variables and invalidation signals
- State: cache ownership is settled (the SDK carries the strategy; the service's developer chooses it); the strategy vocabulary — what to cache, for how long, against which invalidation signals — is not designed. The founding diagrams (SDK + cache with a few strategy variables, against the CQRS aggregation alternative) exist only as images in the chat exports, which are held in the working context (`chats-context/`) and not tracked in the repository.
- Next: recover the diagrams' content into prose, then design the strategy surface.

### Delivery and versioning
- State: one declaration revision yields substitutable SDK deliverables per language — the identity position — but nothing is settled about delivery (package publication, repository layout per `memar-{language}`) or about how SDK versions track declaration revisions and how consumers pin them.
- Next: design the delivery and versioning rules; check against the implementation-repositories structure in [protocols/README.md](./README.md).

### Generation mechanics
- State: generation is the declared mechanism and compile-time generation the position for compiled languages; the generator's architecture (one generator with per-language backends, templates, or AST-level output) is open, as is the balance between per-language idiomatic quality and uniform shape across languages.
- Next: a dedicated design session after the declaration-artifact question settles.

### The validation-sharing shape
- State: GUI's accessor/setter pattern is named as the mechanism the SDK's generation includes; how validation rules are declared once and surface in both the server and the generated client is undesigned.
- Next: design jointly with the GUI protocol.

### Aggregation placement in detail
- State: composition is a consumer-side capability, and coarse operations are allowed where the domain genuinely has them; the test for "genuinely" — what distinguishes a domain aggregate from a view-serving aggregate — is not drawn. The founding discussion's access-control example (an aggregated model mixing fields some consumers may not see, forcing per-field access decisions into the aggregate) is the standing test case.
- Next: settle with the GUI and Modeling documents during the design session.

### How "part of the module's protocol realization" binds concretely
- State: position 9 makes the delivered client face a conformance obligation of the module ([Part of the module, not beside it](./sdk.md#part-of-the-module-not-beside-it)); what enforces that obligation is undesigned — whether a module's protocol declaration is invalid without its client face, whether conformance is checked at release, and how it interacts with the implementation-repositories structure in [protocols/README.md](./README.md).
- Next: decide in the design session; the check belongs to a linter-conformance discussion if the protocol declaration carries it.

### The local/network realization decision surface
- State: both invocation kinds are behind one call surface, and the backing realization is a delivery decision ([Local and network invocation](./sdk.md#local-and-network-invocation)); who makes that decision per call — the SDK's generator, the module's packaging, deployment configuration, or a runtime resolution — and whether a consumer can ever observe or force one kind, is open. The security framing (execution crossing out of the consumer's agency space under the module's control) suggests some crossings must be non-bypassable, but the mechanism is not designed.
- Next: design after the declaration-artifact question settles; touches sRPC's transport role directly.

### Correctness ownership of non-generated consumption paths
- State: the declared interface binds no consumer language ([Working positions](./sdk.md#working-positions) 7) — FFI against a delivered SDK and ports are legitimate consumption paths (the founding example: a Go caller consuming a module whose SDK is delivered in Khayyam). Whether a consumer-made port inherits any ownership or support claim from the module, or is simply the consumer's own code over the same declared interface, is undecided.
- Next: settle in the design session; likely a boundary statement rather than machinery.

### The agreement artifact for delegation
- State: the delegation position requires a pre-existing agreement between the parties — both hold the same declared process, neither redefines it mid-execution ([The call as delegation](./sdk.md#the-call-as-delegation)). What that agreement *is* as an artifact is open: is it the service's declaration itself, a transaction/integrity agreement beside it (the transfer example's bookkeeping rule), or something the Agency document's [Contracts](../agency.md#contracts) topic should own generally? How integrity rules (all-or-nothing transitions) are declared so the generated SDK and the executing side enforce the same one is undesigned.
- Next: design jointly with Agency's Contracts topic and the Error protocol's transaction-adjacent rules.

### Whether the serving side becomes an Agent identity
- State: the delegation position borrows Agency's Principal / Execution Agent vocabulary; whether the module's node takes on a persistent Agent identity in the Agency document's sense (with `agent_for`, accountability, trust relationships), or whether the SDK call stays a nameless delegation realized per call, is undecided.
- Next: settle with the Agency document's [`agent_for`](../agency.md#the-agent_for-relationship) treatment during the design session.

## Anticipated Work
- The dedicated design session that turns this document into the protocol proper: the minimal obligation set, the declaration artifact, the generation pipeline, delivery and versioning.
- Propagation: media-type.md's goal line gains a link to this document when it stabilizes (Pending in [sdk.changelog.md](./sdk.changelog.md)); gui.md's "service contract" phrase may adopt the declaration vocabulary (Pending in [sdk.changelog.md](./sdk.changelog.md)).
- A naming review if the ecosystem word SDK proves too broad for the protocol's narrowed subject; any rename graduates through the changelog with full propagation (gui.md, media-type.md, process.md all use the word).
