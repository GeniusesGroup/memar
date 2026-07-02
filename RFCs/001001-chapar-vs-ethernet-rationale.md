---
RFC Number: 001001
Title: "Chapar vs. Ethernet: State Model, Header Economics, and Hardware Cost"
Status: Draft
Start Date: 2026-07-01
Applied to: ["networking-osi_2-Chapar.md#chapar---data-link-protocol"]
Supersedes: null
Superseded by: null
Related:
  Depends_on: ["001000"]
  Extends: []
  Conflicts with: []
Author(s): []
---

## Summary
Chapar removes per-frame associative (content-addressable) state from intermediate switches by carrying the full forwarding path in the frame itself (source routing), instead of Ethernet's approach of learning and storing a MAC-to-port table (CAM) in every switch on the path. This document records why that trade-off was chosen and quantifies its cost/benefit against Ethernet, so the comparison does not need to live inline in the protocol specification.

## Motivation
Reviewers repeatedly ask the same three questions when first reading the Chapar spec: (1) is Ethernet really "connection-oriented" in the way the spec implies, (2) is Chapar's header overhead actually competitive with Ethernet's, and (3) is the claimed CAM-table ceiling on "the best switch" accurate. Answering these inline in the protocol document turns a specification into an argument; this RFC exists so the specification can stay a specification.

## Guide-level explanation
Ethernet switches build a MAC address table by watching traffic (a "learning" process) so that every switch on a path knows which port leads toward which address. This table is state, and it must be built, maintained, and kept consistent on every intermediate switch, in addition to whatever state the two communicating endpoints keep about each other.

Chapar frames instead carry the entire forwarding path — the sequence of outgoing port numbers, hop by hop — in the frame header. An intermediate switch does not need to know or remember anything about the network; it only reads the header field that applies to its own position in the path and forwards accordingly. All the "where does this go" knowledge lives either in the frame or at the two endpoints, never in the switches in between.

This has two independent consequences, and they should not be conflated:
- **Hardware cost**: a switch that never needs to search a large, dynamically-updated address table can be built from small, fixed-function comparison logic instead of power-hungry CAM. This — not header size — is the primary reason Chapar switching and network-adaptor hardware can be cheaper than Ethernet's.
- **Header economics**: Chapar's header cost scales with topology depth (one byte per hop) instead of being a fixed cost regardless of network size, as Ethernet's 6-byte MAC addresses are. This means the two protocols are not comparable at a single fixed overhead figure — the comparison must be made across a range of network depths.

## Reference-level explanation

### State location
Ethernet requires state in three places: the frame (addresses), the two endpoint peers, and every intermediate switch (the learned MAC table). Chapar requires state only in the frame and at the two endpoint peers — intermediate switches hold none. This document deliberately avoids classifying either protocol as "connection-oriented" or "connectionless" in the formal networking-textbook sense; the terms carry established meanings elsewhere that this comparison does not need to invoke. The only claim made here is about the location and lifetime of the state each protocol requires, which is directly verifiable from each protocol's own mechanics.

### Other cited Ethernet drawbacks (context, not independently re-verified here)
The original motivation for Chapar also cited three further Ethernet drawbacks, carried over here for completeness: high price relative to bandwidth delivered (cost per bit transferred matters more than raw bandwidth), high power usage tied to CAM-table lookups, and closed-source, vendor-specific switching hardware and algorithms. These are stated as motivating context rather than independently re-verified claims in this RFC; if any of them needs its own sourced justification later, it should get one.

### CAM table ceiling
The protocol document's claim of up to 512,000 MAC-table entries as an upper bound on "the best switch" is consistent with publicly documented capacity: enterprise/data-center-class switches are commonly reported in the range of tens of thousands up to several hundred thousand MAC-table entries, depending on model and vendor. No single, precisely sourced switch model with exactly 512,000 entries has been confirmed at the time of writing; the figure should be treated as an order-of-magnitude ceiling rather than a citation to a specific product, unless a specific source is added later.

### Header cost vs. topology depth
A Chapar frame header is: `FrameType (1B) + HopCount (1B) + NextHop (1B) + hop-port-list (1B × hop count)`. For a shallow network (a sensor a few hops from its gateway), this is well under 10 bytes total. Ethernet's per-frame address overhead is fixed regardless of network size: 14 bytes (destination + source MAC + EtherType), 18 bytes including the trailing FCS, or 22 bytes with an 802.1Q VLAN tag.

At Chapar's own budget matching Ethernet's fixed cost (roughly 16 hop-port bytes, i.e. ~18-19 bytes total header), Chapar's source-routed header addresses on the order of 255^16 nodes along that specific path depth — many orders of magnitude beyond Ethernet's flat 2^48 MAC address space (255^16 ≈ 10^38.5 vs. 2^48 ≈ 2.8×10^14, a difference on the order of 10^24). The comparison is therefore not "Chapar is cheaper for small networks" — it is that Chapar's cost buys topology depth and reach directly, while Ethernet pays the same fixed cost whether the network has ten nodes or ten million, and additionally needs CAM-table state to make that fixed-size address usable at scale.

## Drawbacks
- This RFC's numeric comparisons (255^16 vs. 2^48, CAM table ranges) depend on assumptions (uniform hop-port width, symmetric port numbering) that may not hold in every real topology; they are illustrative, not a guarantee for any specific deployment.
- Avoiding the "connection-oriented / connectionless" classification sidesteps a question some readers will still ask; this document should link to, rather than re-open, that debate if raised again.

## Rationale and alternatives
- Alternative: keep the comparison inline in the protocol spec, as it originally was. Rejected because it forced every reader of the spec to also evaluate an argument about a different protocol before understanding Chapar's own rules.
- Alternative: drop the Ethernet comparison entirely. Rejected because the motivating "why" for several protocol decisions (no CAM dependency, source routing) is meaningfully clearer with the comparison than without it — it just belongs in a rationale document, not the spec itself.

## Prior art
- Segment/source routing in general (e.g., IPv6 Segment Routing, MPLS explicit paths) trades per-hop state for path information carried in the packet — a similar state-location trade-off to Chapar's, at a different layer.

## Unresolved questions
- A precise, sourced figure (specific switch model and vendor documentation) for the "best switch" CAM ceiling has not been confirmed.

## Future possibilities
- A follow-up empirical comparison (real header-byte counts against real deployed Ethernet topologies of comparable scale) could replace the illustrative math above with measured data.
