# Networking Connection Changelog

## Changelog

### Initial draft — connection state ownership and liveness budgets
- Time: 2026-09-06T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — claimed, argued
  - [Super Z](../../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — reviewed, rewrote

#### What changed
- Initial Draft defining the connection concept in Networking's packet model and the framework's core rule: connection state is owned by the component that runs the protocol logic and is exposed to layers above; timeouts and liveness are the owning component's budgets; blocking-read as an interface failure, not a property of networking (Omid Hekayati).
- The positive contract (connection concept, state-ownership-with-exposure rule, half-open resolution rule) was stated as the complement to networking.md's position on the traditional network stack (Super Z).
- The blocking-read failure was linked to the interface-design level rather than to a specific language (Super Z).
- Frame-level mechanics were kept out of scope per protocol-document ownership (Super Z).

#### Deliberation
- The positions were brought from public discussions: the blocking-socket-read critique (no first-class "no data yet" outcome; goroutine-spawning and read-deadline answers are workarounds around a mis-shaped interface) and the stateful/stateless contradiction (HTTP called stateless while its specifications define persistent state; Transport state re-created badly at the Application layer) (Omid Hekayati).
- The timeout-as-component-budget rule was contributed, later formalized in process.md's context critique (Omid Hekayati).

---

### Documentation-method migration: rejected alternatives and anticipated work relocated
- Time: 2026-09-06T00:00:00Z
- Type: refactor
- Propagates to:
  - networking-connection.handoff.md: Done - anticipated work recorded there under `Anticipated Work`.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) - claimed, decided
  - [Super Z](../../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) - moved

#### What changed
- The body's `Discussion` wrappers dissolved entirely, per the finalized documentation method (documentation-explanation.changelog.md, same date) (Omid Hekayati - decided; Super Z - applied).
- The topic-level `Discussion`'s evidence paragraph (QUIC's userspace model as existence proof; the "stateless HTTP" contradiction visible in the cookie and session specifications) folded into its topic as inline evidence (Super Z).
- The document-level `Drawbacks` removed from the body; its content preserved below without loss (Super Z).
- Rejected-alternative reasoning moved from the body's `Rationale and alternatives` sections into this entry's `Considered and not done`, without loss (Super Z).
- Anticipated work moved from the body's `Future possibilities` into the paired handoff's `Anticipated Work` (Super Z).

#### Considered and not done
- **Keep the socket arrangement and expose state through side-channels (rejected)**: side-channel views of kernel state drift from the state itself by construction - exactly the failure the ownership rule prevents. (Omid Hekayati)
- **Declare connections an application-layer concept only (rejected)**: the same state-sharing need exists at every layer maintaining per-peer context; dissolving the concept upwards would forbid stating Transport-level rules where they are true. (Omid Hekayati)
- **Specify the userspace TCP realization in this document (rejected)**: the realization is one implementation of this contract; mixing them couples the contract to one codebase's decisions. (Omid Hekayati)

#### Considered and not done (from the removed document-level Drawbacks section)
- **Exposing connection state widens the component's surface.** A component that hides state has a narrow interface by construction; one that exposes it must keep that exposure stable and correct. The framework takes this cost deliberately - invisibility is what produced the shadow-copy failures - but it is a cost. (Omid Hekayati)
- **The realization does not exist yet.** The positions here are currently ahead of the code that would validate them; the socket arrangement, whatever its faults, is running infrastructure today. (Omid Hekayati)

---

### HTTP cookie/"stateless" instance moved to the HTTP position document
- Time: 2026-09-21T15:36:36Z
- Type: Changed
- Propagates to:
  - http.md: Done — owns the HTTP cookie versus "stateless" reconstruction.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — requested, decided
  - [Grok](../../../CONTRIBUTORS.md#grok) (Grok 4.6 via [Cursor](../../../CONTRIBUTORS.md#cursor)) — applied

#### What changed
- Motivation, Methodology, and the closing evidence sentence no longer prosecute HTTP. Hidden connection state is stated as the general failure; the positive contract (state owned by the protocol's logic and exposed upward) is unchanged.
- QUIC remains the existence proof for ownership-with-exposure.
- The Event link in the paired handoff now points at `../process.md#events` (it previously went one directory too high).

#### Considered and not done
- **Keep HTTP cookies as this document's motivating example** (rejected): that writes the connection contract as "why not HTTP." (Omid Hekayati)

---

### State-exposure surface settled on state query and EventTarget
- Time: 2026-10-04T21:26:14Z
- Type: Added
- Propagates to:
  - networking-connection.handoff.md: Done — the state-exposure open question and its anticipated-work line removed.
- Contributors:
  - [Space Bunny Alpha](../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- The state-ownership section gained `What the exposure surface is`: a connection's exposing component offers a read-only state query and the [Event → The EventTarget capability](../process/event.md#the-eventtarget-capability) capability, and nothing else.
- Facts a layer above must react to rather than read — half-open detection and its resolution, an exhausted budget, a lifecycle change — are stated as their own kinds of Event, dispatched through that capability rather than through a notification channel of the connection's own.
- Subscriptions are `AddEventListener` and `RemoveEventListener`, and [Type → Explicit Behavior Ownership](../../type.md#explicit-behavior-ownership) is cited as what forbids a layer above from composing one.
- The members of the read-only state query — which facts it returns and in what form — are left to each protocol's own document, as the half-open rule already leaves frame-level mechanics.

#### Considered and not done
- **Declare a connection-specific subscription abstraction beside `EventTarget` (rejected)**: Abstraction → Abstraction Realization (Implicit Satisfaction) (`docs/khayyam/abstraction.md#abstraction-realization-implicit-satisfaction`) holds that a narrowed `DispatchEvent` parameter satisfies nothing, and a bespoke channel would be the shadow copy the ownership rule forbids. (Space Bunny Alpha — argued)
- **Fix the members of the read-only state query in this document (not taken)**: the query's shape is each protocol's own to state, the same division the half-open rule already draws for frame-level mechanics. (Space Bunny Alpha — argued)

---

### Per-exchange bounds question removed as already stated by the owning-component budget
- Time: 2026-10-05T09:47:47Z
- Type: Changed
- Propagates to:
  - networking-connection.handoff.md: Done — the entry is deleted with no replacement marker.
- Contributors:
  - [Space Bunny Alpha](../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- The Open Questions entry "Per-exchange explicit bounds" is deleted from this handoff, with no replacement marker.
- [Timeouts and liveness are budgets of the owning component](./networking-connection.md#timeouts-and-liveness-are-budgets-of-the-owning-component) already states the answer: "Where an individual exchange genuinely carries a caller-meaningful bound, that bound is an explicit parameter of that exchange — modeled where it is meaningful, not threaded invisibly everywhere". [Process → Timeout is an internal budget, not a per-request promise](../../process.md#timeout-is-an-internal-budget-not-a-per-request-promise) states the same rule at the layer that owns it.
- The entry's choice — a dedicated parameter convention in sRPC, or an application-level modeling choice — is answered: the bound is a parameter of the exchange, and the exchange is modeled where it is meaningful, which for sRPC is sRPC's own frame model rather than a per-call convention threaded through every layer.
- No line under Anticipated Work changed; the other two entries are untouched.

---

### Review of the uncommitted changes of 2026-10-12
- Time: 2026-10-12T09:45:50Z
- Type: Reviewed
- Contributors:
  - [Claude](../../../CONTRIBUTORS.md#claude) (Sonnet-5.5) — reviewed

#### What changed
- Reviewed; no change needed. The handoff lost two questions and gained link and path corrections. Both removals are already recorded in this changelog ("State-exposure surface settled on state query and EventTarget", 2026-10-04T21:26:14Z, and "Per-exchange bounds question removed as already stated by the owning-component budget", 2026-10-05T09:47:47Z), and the answers stand in `networking-connection.md` (the quoted caller-meaningful-bound sentence is present). The remaining edits are `protocols/` to `modules/` and the HTTP link to `../lib/net/http.md`.
