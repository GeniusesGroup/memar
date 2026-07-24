---
ID: 001002
Title: "Chapar Broadcast: Scope, Privacy Rationale, and Known (Not New) Risks"
Status: Draft
Start Date: 2026-07-01
Applied to: ["chapar.md#frame-types", "chapar.md#non-goals-non-considering-that-can-be-treated-as-disadvantages"]
Supersedes: null
Superseded by: null
Citations:
  Depends_on: ["001000"]
  Extends: ["001003"]
  Conflicts with: []
Author(s): []
---

## Summary
Chapar restricts Broadcast frames to rare, low-frequency scenarios (device discovery, emergency signaling) rather than general content distribution. This document records why that restriction exists, why the resulting duplication cost in redundant topologies is acceptable, and clarifies that the security risks of an unrestricted layer-2 segment (e.g., a compromised device flooding traffic) are pre-existing risks shared with Ethernet and other layer-2 protocols, not something Chapar introduces or fails to solve.

## Motivation
Two separate objections tend to surface when reviewing Chapar's Broadcast rules: (1) "won't a Broadcast frame be duplicated across redundant paths, effectively creating an unbounded loop," and (2) "since Chapar declares security a Non-Goal, doesn't that make it worse than Ethernet." Both deserve a direct, recorded answer rather than a defensive aside in the spec.

## Guide-level explanation
Broadcast in Chapar is meant for exactly two things: a new device announcing itself to find a coordinator (see [related document](./chapar-discovery-and-path-establishment.md)), and emergency signaling. It is explicitly not meant for general content distribution (e.g., streaming video to many recipients on a segment).

There are two independent reasons for this restriction:
- **Privacy**: broadcasting general content to every node on a segment lets any node infer another node's activity — what is being watched, when it is paused or resumed, and so on. This is a form of surveillance the design rejects as a leftover assumption from physical-world broadcast constraints (e.g., a stadium crowd watching one shared screen) that a digital network is not obligated to repeat. Content genuinely meant for many recipients should be delivered as distinct application-layer streams, not layer-2 broadcast.
- **Bounded, non-persistent cost**: every frame — including Broadcast — carries an explicit HopCount and forwarding path, so a duplicated Broadcast frame in a redundant topology is bounded by the hop limit and is dropped as a stray frame once it reaches the end of its path. It cannot persist or re-circulate indefinitely. This differs materially — and is much cheaper — than an unresolved forwarding loop in a protocol without a hop bound, where a stray frame can remain alive in the network indefinitely and add to cumulative processing load with every subsequent frame like it. Given how rare legitimate Broadcast use is (device discovery, emergencies), this bounded duplication cost was judged not to be worth a dedicated mitigation (e.g., a new header field); no design was found where such a field's cost would be justified against how infrequently it would matter.

Misuse of Broadcast beyond these rare, intended scenarios is a runtime/security policy concern for ChaparKhane or the network operator to detect and enforce (e.g., raising an intrusion alert), not a defect of the Chapar protocol layer to prevent structurally. The next section argues this detection is also structurally cheaper in Chapar than the equivalent in Ethernet.

### Chapar's structural advantage for locating a misbehaving device
In Ethernet, tracing a misbehaving device (e.g., one generating a broadcast storm or forged traffic) back to a physical port requires switches with dedicated management capability — an SNMP agent, a MAC-table query CLI, or an equivalent "managed switch" feature set — which is a real, non-trivial cost most cheap/unmanaged switches simply do not have. Without it, locating the offending physical port on a large flat Ethernet segment can require walking the topology switch by switch.

Chapar does not need an equivalent dedicated management feature to get the same result, because every switch already performs the relevant work as an unavoidable part of ordinary forwarding, not as an optional add-on: the Rules above require every hop to rewrite the received port number into the frame based on the port it physically arrived on, and to verify a Unicast frame's declared port against the physical one. A device cannot make its frames claim a path other than the one they actually traveled, because that path is stamped by switch hardware, not asserted by the sender. So for any frame that reaches ChaparKhane (directly, as a Broadcast, or as a Unicast destined to it), the accumulated header already is a truthful physical trail back to the originating port — without any switch needing a management plane at all. The cost of traceability is paid once, in the base protocol design, rather than per-switch as a purchasing decision.

This is a genuine structural advantage, but it should not be overstated in one respect: it makes misbehavior *traceable*, not *undetectable-proof against being attempted*. Traceability only translates into an actual response if something (ChaparKhane, an operator, an observability tool) is actively watching for it — the same is true of a managed Ethernet switch's MAC table, which also does nothing on its own until someone queries it. A determined attacker seeking a brief, disruptive burst (rather than sustained, stealthy access) is not necessarily deterred by traceability alone, in Chapar or Ethernet. The claim that should be recorded here is narrower and still meaningful: Chapar makes this class of investigation possible on hardware where Ethernet would make it impossible (unmanaged switches) or expensive (managed switches), not that it eliminates the incentive to attempt an attack.

## Reference-level explanation
Broadcast frames use `HopCount == 0x00` and carry the full 255-slot hop-port space with zero-length data (see the Rules section of the main spec). Chapar itself does not interpret why a Broadcast was sent — the Discovery or Emergency semantics are carried in a higher-layer service-call frame elsewhere in the same packet (per `networking.md`'s multi-frame packet model), and packets are expected to be ordered following the OSI layering, since violating that ordering is costly to process at every layer.

On the security Non-Goal: the risk of a compromised device flooding a local segment with traffic (frames, broadcast storms, forged headers) is not a risk introduced by Chapar. Comparable attacks (e.g., MAC flooding) already exist against Ethernet and other layer-2 protocols today, on networks that do implement broadcast/multicast restrictions and address learning. Chapar does not attempt to solve this class of problem at the protocol layer, consistent with treating physical/access security as out of scope.

## Drawbacks
- "Bounded duplication is acceptable because it's rare" is a judgment call, not a proof; a future scenario with much more frequent legitimate Broadcast use (not currently anticipated) would need this trade-off re-evaluated.
- Deferring broadcast misuse detection entirely to ChaparKhane assumes a ChaparKhane (or equivalent coordinator) is always present and correctly configured; a segment without one has no enforcement of this policy at all.

## Rationale and alternatives
- Alternative: add a dedicated de-duplication mechanism (e.g., switches remembering recently seen FrameIDs) to eliminate Broadcast duplication in redundant topologies entirely. Rejected: this reintroduces per-switch state, directly contradicting the stateless-switch goal, for a cost (bounded, rare duplication) that was judged not to justify it.
- Alternative: forbid redundant/multi-link topologies to avoid the duplication scenario altogether. Rejected: multi-link topologies are explicitly used elsewhere in the spec to increase host capacity (see Topology Example), so forbidding them would conflict with a stated goal.

## Prior art
- Broadcast storm prevention in Ethernet (e.g., Spanning Tree Protocol) solves a structurally different problem: Ethernet's forwarding loops are unbounded without it, whereas Chapar's HopCount already bounds any single frame's lifetime.

## Unresolved questions
- None currently open; flag here if a legitimate high-frequency Broadcast use case is identified in the future, since it would invalidate the "rare enough not to mitigate" judgment above.

## Future possibilities
- If a future use case requires frequent Broadcast (not currently anticipated), revisit whether a lightweight de-duplication mechanism is worth its state cost at that time.
