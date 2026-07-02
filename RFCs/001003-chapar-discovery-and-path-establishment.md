---
RFC Number: 001003
Title: "Chapar Discovery and Path Establishment"
Status: Draft
Start Date: 2026-07-01
Applied to: ["networking-osi_2-Chapar.md#discovery"]
Supersedes: null
Superseded by: null
Related:
  Depends_on: ["001000"]
  Extends: ["001002"]
  Conflicts with: []
Author(s): []
---

## Summary
Every layer-2/3 stack has to solve the same underlying problem: a sender needs to know how to reach a destination before it can send to it. Ethernet solves it with switch MAC-learning plus ARP; Chapar, being source-routed, needs the sender to hold the actual hop-port path. This RFC records how any pair of Chapar devices — not only a device and ChaparKhane — ends up with that path, using nothing beyond rules the protocol already defines, and records what is deliberately left to higher layers.

## Motivation
Earlier review of the spec flagged a real gap: nothing in the protocol described how an endpoint obtains the hop-port sequence it is required to place in every Unicast frame's header. Without an answer, "stateless switching" and "source routing" are individually well-specified but the system as a whole is not — a device would have no way to send its first frame at all. This is not a problem unique to Chapar: Ethernet devices resolve the equivalent problem via ARP (address to MAC) plus each switch's own MAC-learning, so a reader should not conclude that path establishment is a novel cost Chapar introduces — only that Chapar's mechanism for it needed to be written down.

## Guide-level explanation
A device introduces itself by sending a Broadcast frame (`HopCount == 0x00`). As required by the existing port-rewrite Rule (every switch rewrites the port it received a frame on into that frame's header), each switch along every flooded path stamps its own receiving port into the corresponding header slot as the frame propagates outward. By the time the frame reaches any given node, the frame's header already contains the exact reverse path back to the device that sent it — this falls directly out of a rule the protocol needed anyway, not a new mechanism bolted on for Discovery.

Any node **may** respond to a Discovery broadcast (this is optional and a policy decision — see below). ChaparKhane, as the network's mandatory coordinator, **must** respond. Its response is a Unicast frame using the accumulated hop-port sequence, reversed, as the path — no separate route computation, lookup, or additional protocol exchange is required.

This alone only gives each device a path *to ChaparKhane*, though — it is not the end goal, just the foundation. Because ChaparKhane ends up holding a known path to every device that has completed Discovery, it can act as a low-cost hub for establishing a path between any two ordinary devices: Device 1's path to ChaparKhane, joined with ChaparKhane's known path to Device 2 (reversed appropriately), composes into a full Device-1-to-Device-2 path — using the same path-joining logic the Rules already require when two peers connect through mismatched port numbering ("virtual switch hop"). Device-to-ChaparKhane discovery is therefore the building block, not the whole answer, for general device-to-device path establishment.

## Reference-level explanation
- Discovery is carried as a Broadcast Chapar frame; the semantic payload ("this is a discovery request," any accompanying identity data) belongs to an [sRPC](../sRPC.md) service call elsewhere in the same packet — Discovery and Emergency are each just a `ServiceID` under sRPC's single shared FrameType, the same mechanism every service call at any layer uses. No dedicated FrameType is registered per service; Memar deliberately avoids repeating Ethernet/IP's history of exhausting a small FrameType/EtherType space one service at a time. Chapar itself never interprets frame content — it only floods and, on response, unicasts.
- If more than one ChaparKhane is present on a segment and responds, Chapar imposes no limit and arbitrates nothing between the responses — path selection among multiple valid responses is a ChaparKhane / higher-layer coordination concern, not a Chapar-layer one.
- **Path refresh after topology change**: Chapar has no dedicated re-discovery mechanism. Because no Chapar frame travels without an accompanying higher-layer packet, an ordinary upper-layer timeout/retry on a failed send is expected to be what triggers a fresh Discovery. ChaparKhane may optionally propagate a "path changed" notification to authorized upper-layer subscribers (access-controlled) as an additional optimization, but this is not required for correctness.
- **Discoverability policy**: whether a device responds to a Discovery broadcast at all is a decision made above the Chapar layer (by the host OS or application), comparable to a network-discovery toggle in general-purpose operating systems. Chapar neither mandates nor restricts this.
- **Device-to-device path composition**: once Device 1 holds Path(D1→CK) and ChaparKhane holds (or can derive) Path(CK→D2) from D2's own earlier Discovery, a full Path(D1→D2) is obtained by joining the two at ChaparKhane, using the existing virtual-switch-hop join rule. This requires no new Discovery round for either device. Whether ChaparKhane exposes this as a pull (request/response) service, a push (proactively distributed directory) service, or both, is entirely a ChaparKhane-level service design decision — Chapar itself has no reason to restrict this to one model, and does not.

## Drawbacks
- Relying entirely on upper-layer timeout for path-staleness detection means the delay before a broken path is noticed and re-discovered is whatever that upper-layer protocol's timeout is — Chapar contributes no faster signal of its own.
- Device-to-device path composition makes ChaparKhane a required party in establishing *any* new device pairing, even between two devices that could otherwise reach each other directly — this is a deliberate centralization at the coordinator, not a free byproduct.

## Rationale and alternatives
- Alternative: give ChaparKhane a dedicated route-computation and distribution protocol (link-state or distance-vector style) instead of relying on broadcast-flood reverse-path accumulation. Rejected for the common case: it would reintroduce meaningful state and a separate control protocol for a problem the existing port-rewrite rule already solves for the primary case (reaching a coordinator).
- Alternative: require every switch to cache recent FrameIDs to deduplicate the Discovery flood. Rejected: reintroduces per-switch state, and duplication cost during the rare Discovery event is already addressed as acceptable in [RFC 001002](./001002-chapar-broadcast-scope-and-known-risks.md).

## Prior art
- Reverse-path learning during flood-based route discovery is used in ad hoc/mesh routing protocols (e.g., AODV-style route requests), where a broadcast request accumulates path information that a unicast reply then uses in reverse — structurally similar to the mechanism here, at a different layer.
- Ethernet's ARP (resolving a network-layer address to a MAC address) combined with per-switch MAC-learning solves the equivalent problem — a device needing a usable path to another device before it can send — by different means (a broadcast query answered directly by the target, plus stateful learning in every switch, rather than reverse-path accumulation with stateless switches).

## Unresolved questions
- None remaining at the Chapar-layer for the core mechanism described above. Two related items are explicitly out of scope rather than unresolved: the specific `ServiceID` values for Discovery and Emergency belong to sRPC's service registry, not this RFC; and whether ChaparKhane offers path lookup as pull, push, or both is a ChaparKhane service-design decision, not a Chapar protocol one.
- **Discovery response authenticity** is a genuinely open question for the Discovery service itself (not a Chapar concern, and not something Chapar's security Non-Goal has any bearing on): since any node may optionally respond to a Discovery broadcast, should the Discovery service require responses to be signed, verifiable against a certificate both parties trust? This is entirely decidable at the sRPC/Discovery-service level and is not blocked by anything in Chapar. One open sub-question worth flagging if this direction is taken: a certificate-based scheme still needs a trust anchor (the CA certificate itself) present on both the device and ChaparKhane *before* the device's very first Discovery — for a large population of low-cost devices (e.g., thousands of sensors), how that initial trust anchor gets provisioned is its own design question, not automatically answered by choosing to require signatures.

## Future possibilities
- A future ChaparKhane-focused RFC could specify its path-directory service (pull, push, or both) in detail — that design is independent of anything decided here.
- A future Discovery-service RFC could specify the signed-response scheme above, including how the initial trust anchor is provisioned for low-cost devices at scale. This connects to a separate, larger planned RFC track (numbered from 003000 onward) covering manufacturer-issued default device certificates and organizational ownership transfer — that track is where the trust-anchor provisioning question above is expected to be resolved, not here.
