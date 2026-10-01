# SDK Handoff
Open work for `protocols/modules/sdk.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../../documentation-handoff.md) for what a handoff is.

## Open Questions

### What the declaration artifact is
- State: the SDK is derived from the service's declared interface; what that declaration concretely is — a Memar protocol artifact, the media-type-identified structure inventory, the sRPC service frames, or something new — is undecided.
- Next: design with Media Type and sRPC; the founding prototype's generator input should be recovered before deciding.

### Cache-strategy variables and invalidation signals
- State: cache ownership is settled (the SDK carries the strategy; the service's developer chooses it); the strategy vocabulary — what to cache, for how long, against which invalidation signals — is not designed. The founding diagrams (SDK + cache with a few strategy variables, against the CQRS aggregation alternative) are not recoverable: the chat exports audited on 2026-09-30 carry no images at all, and the earlier context files that may have held them are retired. What survives of that discussion is this entry and the protocol's changelog, which name the strategy variables as a class without enumerating them — so the enumeration has to come from the owner, not from a source.
- Next: owner states the strategy variables, then design the strategy surface.

### Delivery and versioning
- State: one declaration revision yields substitutable SDK deliverables per consumer language — the identity position — but nothing is settled about delivery (package publication, the local module layout under [`modules/`](../../../modules/), or consumer-side placement) or about how SDK versions track declaration revisions and how consumers pin them.
- Next: design the delivery and versioning rules; check against the local module placement in [protocols/README.md](.././README.md).

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
- State: position 9 makes the delivered client face a conformance obligation of the module ([Part of the module, not beside it](../modules/sdk.md#part-of-the-module-not-beside-it)); what enforces that obligation is undesigned — whether a module's protocol declaration is invalid without its client face, whether conformance is checked at release, and how it interacts with the local module placement in [protocols/README.md](.././README.md).
- Next: decide in the design session; the check belongs to a linter-conformance discussion if the protocol declaration carries it.

### The local/network realization decision surface
- State: both invocation kinds are behind one call surface, and the backing realization is a delivery decision ([Local and network invocation](../modules/sdk.md#local-and-network-invocation)); who makes that decision per call — the SDK's generator, the module's packaging, deployment configuration, or a runtime resolution — and whether a consumer can ever observe or force one kind, is open. The security framing (execution crossing out of the consumer's agency space under the module's control) suggests some crossings must be non-bypassable, but the mechanism is not designed.
- Next: design after the declaration-artifact question settles; touches sRPC's transport role directly.

### Correctness ownership of non-generated consumption paths
- State: the declared interface binds no consumer language ([Working positions](../modules/sdk.md#working-positions) 7) — FFI against a delivered SDK and ports are legitimate external consumption paths (the founding example: an external Go caller consuming a module whose SDK is delivered in Khayyam). Whether a consumer-made port inherits any ownership or support claim from the module, or is simply the consumer's own code over the same declared interface, is undecided.
- Next: settle in the design session; likely a boundary statement rather than machinery.

### The agreement artifact for delegation
- State: the delegation position requires a pre-existing agreement between the parties — both hold the same declared process, neither redefines it mid-execution ([The call as delegation](../modules/sdk.md#the-call-as-delegation)). What that agreement *is* as an artifact is open: is it the service's declaration itself, a transaction/integrity agreement beside it (the transfer example's bookkeeping rule), or something the Agency document's [Contracts](../../agency.md#contracts) topic should own generally? How integrity rules (all-or-nothing transitions) are declared so the generated SDK and the executing side enforce the same one is undesigned.
- Next: design jointly with Agency's Contracts topic and the Error protocol's transaction-adjacent rules.

### Revocation and integrity of a delegated credential
- State: the two entries above carry the delegation position and its agreement artifact; the credential that travels with the call is not carried anywhere. The owner's design, recovered 2026-09-30 from an audit of Omid Hekayati's Go-community Telegram-group messages (Gommunity), is that an authenticated holder mints a derived credential to hand a third party, and that service instances accept short-lived secondary credentials precisely so that one revocation need not reach every instance at once — a design whose own cost the owner named in the same breath, since a secondary credential that is cheap to issue is also cheap to leak. Nothing in `docs/` states what a revocation is, how it propagates when the verifying side holds only local state, what makes a derived credential's integrity checkable, or how a credential's expiry interacts with revocation. One boundary the owner drew explicitly and which no document records: identification — establishing who the subject is, including by biometric factor — is a different concern from authentication, and biometric material is not authentication input.
- Question for the owner: is a revocation a domain fact recorded like any other, which would give it history under [Process → Events](../../process.md#events) and [Modeling → Modeling State Change as Events, Not Destructive Updates](../../modeling.md#modeling-state-change-as-events-not-destructive-updates), or a property of the verifying side's current state; and does the credential need a protocol document of its own, or does the answer belong to Agency's [Contracts](../../agency.md#contracts) and [Principal](../../agency.md#principal) vocabulary?
- Next: settle together with [Framework Handoff → Does Memar need authentication, session, and authorization protocols?](../../framework.handoff.md#does-memar-need-authentication-session-and-authorization-protocols). No protocol document covers any part of this today, so the two questions have one answer or none; splitting them would produce a credential vocabulary owned by nothing.

### Whether the serving side becomes an Agent identity
- State: the delegation position borrows Agency's Principal / Execution Agent vocabulary; whether the module's node takes on a persistent Agent identity in the Agency document's sense (with `agent_for`, accountability, trust relationships), or whether the SDK call stays a nameless delegation realized per call, is undecided.
- Next: settle with the Agency document's [`agent_for`](../../agency.md#the-agent_for-relationship) treatment during the design session.

## Anticipated Work
- **Generate a service from its name and path** — owner position (2026-09-29): a Memar server capability that materializes a service given only its name and module path, without hand-authored Rule text or Practices narrating each artifact. Relates to [Knowledge → Knowledge and Code](../../knowledge.md#knowledge-and-code) (generative work belongs in callable services). No `docs/` document yet defines the Memar server; nearest record is [Khayyam execution handoff → Rule model](../../../modules/khayyam/execution.handoff.md).
- The dedicated design session that turns this document into the protocol proper: the minimal obligation set, the declaration artifact, the generation pipeline, delivery and versioning.
- Propagation: media-type.md's goal line gains a link to this document when it stabilizes (Pending in [sdk.changelog.md](../modules/sdk.changelog.md)); gui.md's "service contract" phrase may adopt the declaration vocabulary (Pending in [sdk.changelog.md](../modules/sdk.changelog.md)).
- A naming review if the ecosystem word SDK proves too broad for the protocol's narrowed subject; any rename graduates through the changelog with full propagation (gui.md, media-type.md, process.md all use the word).
