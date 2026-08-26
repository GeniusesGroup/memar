---
Title: "Chapar - Data Link Protocol"
Status: Draft
Start Date: 2015-01-01
ID: 394466
---

# Chapar - Data Link Protocol

## Abstract
Chapar is a layer-2 (data-link) switching protocol in which every frame carries its own complete forwarding path — the sequence of outgoing port numbers, hop by hop — so intermediate switches hold no per-frame or per-address state: all switching knowledge lives either in the frame itself or at the two communicating peers. Chapar supports Unicast and hop-bounded Broadcast forwarding, source-routed hop-port headers, and a Discovery mechanism in which flooded announcement frames accumulate their own reverse path. This document is the single specification for the protocol: each topic below states the normative behavior first, and keeps the design rationale in that topic's own `Discussion` bundle — a reader who wants only the "how" can stop at the topic statements, and a reader who wants the "why" reads on within the same topic.

## Introduction

### Motivation
Two distinct frictions motivated this protocol and this document.

The protocol-level friction is the state model layer-2 networking inherited from Ethernet. Every Ethernet switch must learn which port leads toward which address, store that knowledge in a MAC table built from associative (CAM) memory, and keep it consistent — so the ability to forward a frame comes to depend on per-switch state whose size caps how many addresses the network can hold, whose lookups consume power on every frame, and whose management features (querying the table, tracing traffic back to a physical port) are purchased only with managed hardware. Growing a flat layer-2 network past what those tables can hold forces the traffic up to layer 3, with the addressing and coordination costs that climb carries. A second, quieter friction is reachability: before its very first frame can be sent, a device needs a usable path, and Ethernet supplies that through ARP plus the same per-switch learning tables the forwarding itself depends on — the bootstrap presupposes the state that makes the hardware expensive.

The document-level friction is that a specification stating rules without the goals those rules serve reads as arbitrary: a future contributor cannot tell an intentional boundary from an oversight. Reviewers of earlier revisions kept re-raising the same questions — whether Ethernet is really "connection-oriented" in the way the spec implies, whether Chapar's header overhead is actually competitive with Ethernet's, whether the claimed CAM-table ceiling on "the best switch" is accurate, how an endpoint obtains the hop-port sequence it is required to place in every Unicast frame's header, and whether a Broadcast frame duplicated across redundant paths creates an unbounded loop — because the answers lived apart from the rules they explained. This revision therefore keeps every reason physically next to its rule: each topic below leads with the normative behavior, and the rationale for it lives in that topic's own Discussion bundle, which a reader wanting only the rules can skip wholesale.

### Methodology
The design was not reasoned out in the abstract; it was reached by decomposing the problem every data-link switching scheme must solve, then studying where known systems place the knowledge needed to solve it.

Decomposed, the problem has three parts: where does the knowledge needed to forward a frame live — in the sender, in the frame itself, or in the network's intermediate nodes; how does a sender acquire that knowledge before it can send its first frame; and what bounds a frame's lifetime so a failure cannot circulate forever. Each part already has working answers elsewhere, and each was studied as evidence rather than reinvented:

- Ethernet (datagram style) places forwarding knowledge in every intermediate switch, learned by watching traffic and held in CAM tables, with ARP resolving upper-layer addresses onto that machinery. Studying it isolated the actual cost center: not raw bandwidth, but per-switch state — the silicon it requires, the power it burns, the scale ceiling it imposes, and the management plane needed to operate it.
- Circuit switching (telephone exchanges) and its fast-packet descendants (ATM, Frame Relay) place the knowledge in a path established before use. Studying them showed the value of deciding a path once and carrying it forward — and equally the burden of connection state paid for every conversation.
- Flood-based route discovery in ad hoc/mesh routing (AODV-style requests) demonstrated that a flooded request can accumulate its own return path hop by hop as it travels, requiring no routing table in the nodes it passes.

Chapar is the synthesis drawn from comparing these placements: the path is decided once — by Discovery — and thereafter carried inside every frame (a virtual circuit taken down to per-frame granularity), so intermediate switches need none of Ethernet's learned state; the flood that bootstraps the very first path is the same flood that accumulates it; and an explicit HopCount bounds every frame by construction, replacing dedicated loop-prevention protocols such as Spanning Tree with arithmetic. Candidate results were then checked numerically against real constraints — the topology-capacity figures in [Goals and Non-Goals](#goals-and-non-goals) and the header-cost comparison in [State model compared with Ethernet](#state-model-compared-with-ethernet) are the surviving checks — and the whole design passed through repeated critical review in which each objection was either answered or converted into an explicit Non-Goal. Those reviews are preserved where they belong: as the Discussion bundle attached to each topic below.

## Explanation

### Why "Chapar"
["The Chapar"](https://en.wikipedia.org/wiki/Chapar_Khaneh) (Persian: چاپار‎) were express couriers of the Achaemenid-era Persian postal system, each station (a "Chapar Khaneh") keeping fresh horses and supplies so a message could keep moving without its courier having to rest or resupply. The name was not chosen only for its historical flavor — the parallel to this protocol's own design is fairly direct: in the old system, a letter was handed off to a new courier at each Chapar Khaneh station, continuing its journey under new hands rather than one courier carrying it the whole way. In this protocol, the same thing happens structurally: whenever a packet reaches a ChaparKhane, its Chapar frame is effectively handed to a new leg of routing — a fresh path is established or composed for the next stage of the journey, rather than the originating device having to have known the complete end-to-end route in advance. Horse and letter became switch and packet, but the underlying shape — relay stations that hand a message onward, each responsible only for the next leg — is the same one this protocol is built on.

### Scope and terminology
Anywhere in this document talk about [Ethernet](https://en.wikipedia.org/wiki/Ethernet), means ethernet in [layer two](https://en.wikipedia.org/wiki/Ethernet_frame#Frame_%E2%80%93_data_link_layer) not including layer one. Ethernet in layer one has its frame header and dedicated specs that usually engineers mix ethernet for two layer almost because they use and think to TCP/IP model instead of OSI model.

### Frame architecture
- Ports number can be mutable due to physical link limits. The endpoint must beware of this aspect.
- Each switch interface in any location of link can be wired or wireless with any Energy||Frequency specs (e.g. Fiber, WiFi, LAN, Bluetooth, ...)

| bit   | Length(byte-Octet) | Data                          |
| :---: | :---:              | :---:                         |
| 0     | 1                  | FrameType                     |
| 8     | 1                  | Hop Count                     |
| 16    | 1                  | Next Hop                      |
| 24    | 1                  | First Hop Port Number         |
| ...   | ~                  | x Hop Port Number (Optional)  |

- FrameType: Indicate by [networking rules](./networking.md).
- [Hop Count](https://en.wikipedia.org/wiki/Hop_(networking)#Hop_count): The hop count refers to the number of intermediate network devices through which data must pass between source and destination, and also indicate frame length.
- [Next Hop](https://en.wikipedia.org/wiki/Hop_(networking)#Next_hop): Indicate hop number that frame must send on indicate port by that hop.
- First Hop Port Number: Source Port Number, also can be Destination Port Number in P2P(Point to Point) connection.
- x Hop Port Number: Up to 255 hop port number can be in a frame.

A Chapar frame header is therefore: `FrameType (1B) + HopCount (1B) + NextHop (1B) + First Hop Port Number (1B) + hop-port-list (1B × hop count)`.

How the length derives from the fields — which is what "Hop Count … also indicate frame length" means concretely: a Unicast frame with `n` intermediate hops carries `4 + n` header bytes, the four fixed fields plus exactly one port byte per hop, so a receiver can parse the entire header from Hop Count alone, without any separate length field. The Broadcast frame (`HopCount == 0x00`) is the deliberate exception: it always carries the full 255-slot hop-port space with zero-length data in every slot, giving a constant maximum-size header regardless of how far the frame will actually flood — because those reserved slots are precisely where switches stamp their arrival ports as the frame propagates (see [Rules](#rules)).

When a link carries Chapar frames at all is a capacity-and-role decision, not a constant: a header appears where the link feeds a switching function. A plain two-device association can carry layer 1 plus upper-layer framing (in Memar, sRPC) with no Chapar header in between — the packet goes straight from the medium to layer 3 — and small-frame media that could never host a full Broadcast header remain fully usable in such directly-attached roles. The ~260-byte Broadcast form is therefore required only on media that actually host shared, flooded segments (see [Discovery](#discovery)).

### Frame types
Chapar support **UniCast** and **BroadCast** frame and not support **AnyCast** or **MultiCast**. We strongly suggest use broadcast frames just in network discoverable mechanism like find GP network coordinators. Also to broadcast emergency messages service, not to use to broadcast video channels, ...

Two kinds of statement are mixed in that paragraph, and separating them removes an apparent tension: which frame types *exist* is a structural property of the protocol — Unicast and Broadcast are provided by this layer, while AnyCast and Multicast are simply absent from it (many-recipient delivery, when wanted, is constructed above this layer, e.g. as distinct application-layer streams). Where Broadcast may legitimately be *used* is a usage policy rather than a structural fact: it is strongly restricted to the discovery and emergency scenarios named above, and because Chapar forwards Broadcast without interpreting it (next paragraph), enforcing that policy belongs to the layers above — see the Discussion below and [Misbehavior traceability](#misbehavior-traceability).

Chapar itself carries a Broadcast frame without interpreting why it was sent — the actual Discovery or Emergency semantics live in an [sRPC](./sRPC.md) service call (identified by `ServiceID`) elsewhere in the same packet, not a dedicated FrameType; no dedicated FrameType is registered per service, because Memar deliberately avoids repeating Ethernet/IP's history of exhausting a small FrameType/EtherType space one service at a time. Packets are expected to be ordered following the OSI layering, since violating that ordering is costly to process at every layer.

#### Discussion

##### Rationale and alternatives
Broadcast in Chapar is meant for exactly two things: a new device announcing itself to find a coordinator (see [Discovery](#discovery)), and emergency signaling. It is explicitly not meant for general content distribution (e.g., streaming video to many recipients on a segment). There are two independent reasons for this restriction:

- **Privacy**: broadcasting general content to every node on a segment lets any node infer another node's activity — what is being watched, when it is paused or resumed, and so on. This is a form of surveillance the design rejects as a leftover assumption from physical-world broadcast constraints (e.g., a stadium crowd watching one shared screen) that a digital network is not obligated to repeat. Content genuinely meant for many recipients should be delivered as distinct application-layer streams, not layer-2 broadcast.
- **Bounded, non-persistent cost**: every frame — including Broadcast — carries an explicit HopCount and forwarding path, so a duplicated Broadcast frame in a redundant topology is bounded by the hop limit and is dropped as a stray frame once it reaches the end of its path. It cannot persist or re-circulate indefinitely. This differs materially — and is much cheaper — than an unresolved forwarding loop in a protocol without a hop bound, where a stray frame can remain alive in the network indefinitely and add to cumulative processing load with every subsequent frame like it. Given how rare legitimate Broadcast use is (device discovery, emergencies), this bounded duplication cost was judged not to be worth a dedicated mitigation (e.g., a new header field); no design was found where such a field's cost would be justified against how infrequently it would matter.

Misuse of Broadcast beyond these rare, intended scenarios is a runtime/security policy concern for ChaparKhane or the network operator to detect and enforce (e.g., raising an intrusion alert), not a defect of the Chapar protocol layer to prevent structurally. See [Misbehavior traceability](#misbehavior-traceability) for why this detection is structurally cheaper in Chapar than the equivalent in Ethernet.

Alternative solutions considered and rejected:
- Add a dedicated de-duplication mechanism (e.g., switches remembering recently seen FrameIDs) to eliminate Broadcast duplication in redundant topologies entirely. Rejected: this reintroduces per-switch state, directly contradicting the stateless-switch goal, for a cost (bounded, rare duplication) that was judged not to justify it.
- Forbid redundant/multi-link topologies to avoid the duplication scenario altogether. Rejected: multi-link topologies are explicitly used elsewhere in the spec to increase host capacity (see [Topology capacity examples](#topology-capacity-examples)), so forbidding them would conflict with a stated goal.

##### Drawbacks
- "Bounded duplication is acceptable because it's rare" is a judgment call, not a proof; a future scenario with much more frequent legitimate Broadcast use (not currently anticipated) would need this trade-off re-evaluated.
- Deferring broadcast misuse detection entirely to ChaparKhane assumes a ChaparKhane (or equivalent coordinator) is always present and correctly configured; a segment without one has no enforcement of this policy at all.

##### Prior art
Broadcast storm prevention in Ethernet (e.g., Spanning Tree Protocol) solves a structurally different problem: Ethernet's forwarding loops are unbounded without it, whereas Chapar's HopCount already bounds any single frame's lifetime.

##### Unresolved questions
None currently open; flag here if a legitimate high-frequency Broadcast use case is identified in the future, since it would invalidate the "rare enough not to mitigate" judgment above.

##### Future possibilities
If a future use case requires frequent Broadcast (not currently anticipated), revisit whether a lightweight de-duplication mechanism is worth its state cost at that time.

### Discovery
A device announces itself with a one-way Broadcast frame (`HopCount == 0x00`) — a fire-and-forget [sRPC](./sRPC.md) call with no defined response. Announcement is event-driven, not scheduled: it happens at join time, and again only when an upper-layer failure indication (a timed-out send, see path refresh below) demands a fresh path; between those events a joined device stays silent, and periodic re-announcement is not part of the protocol.

Broadcast announcement is the join mechanism for *shared, multi-node segments* — places where a newcomer has no single designated peer and must reach whoever is listening. A device whose entire path to the network is a dedicated association to its coordinator — a wireless cell terminating on its access point, a single wired uplink to its ChaparKhane — does not flood an announcement at all: it registers directly with that coordinator using ordinary upper-layer messaging, exactly as a mobile phone attaching to a cell tower does not introduce itself to every other phone on that tower. On such point-to-point attachments a Chapar header may be absent altogether — layer 1 carries the link while the payload speaks sRPC and layer 3 directly — because whether layer 2 exists on a given link is decided by that link's capacity and role, not assumed by default (see [Frame architecture](#frame-architecture)). The reaction policy below applies to broadcast announcements on shared segments; direct registration is simply the coordinator doing its job as the attachment endpoint.

On the broadcast form itself: as it floods hop by hop, the port-rewrite [Rule](#rules) causes the frame to accumulate its own reverse path — each switch along every flooded path stamps its own receiving port into the corresponding header slot as the frame propagates outward, so by the time the frame reaches any given node, the frame's header already contains the exact reverse path back to the device that sent it. This falls directly out of a rule the protocol needed anyway, not a new mechanism bolted on for Discovery.

Chapar has no persistent, stable device address; where an upper layer needs to identify a sender, the accumulated reverse path is what serves that role. Nothing new is added to Chapar to support this — it reuses the same path data Discovery already produces for routing a Unicast toward the sender. Two properties of this "address" are important to state explicitly, so an implementer does not mistake it for something it is not:

- **Ephemeral, not persistent**: the reverse path reflects the topology at the moment it was captured. If the topology changes, the path — and therefore this "address" — becomes stale along with it (see path refresh below). Nothing should be built that assumes this value is durable across a topology change without a fresh Discovery.
- **Receiver-relative, not a single global value**: because a reverse path is "the path from here back to the sender," it is only meaningful relative to whoever holds it. ChaparKhane's path to Device 1 and Device 2's path to Device 1 are two different byte sequences for "the same" device — this is not an inconsistency to reconcile, it is why path composition (below) has to explicitly join two paths rather than compare or copy one party's "address" for use by another.

One more boundary completes this picture: a stable, portable identity — something that lets parties refer to *which* device across time — is deliberately absent from this layer, exactly as it is absent from every other layer-2 protocol. Ethernet exposes only MAC addresses; everything beyond them (ARP resolution, then names, directories, certificates) lives above. Chapar differs only in what its layer-2-level handle looks like — an ephemeral reverse path rather than a persistent MAC. Any deployment that must refer to devices across time therefore binds upper-layer identities to current paths in the layer that owns identity (GP/sRPC): a prerequisite this design shares with every alternative, Ethernet-based ones included, not a dependency Chapar uniquely introduces.

Any node may react (optional); ChaparKhane always must. Reacting means independently initiating a fresh Unicast frame to the new device using the accumulated path, reversed — not a coupled RPC response.

Device-to-device path establishment: Discovery alone only gives each device a path *to ChaparKhane* — it is the foundation, not the end goal. Because ChaparKhane ends up holding a known path to every device that has completed Discovery, it composes a full Path(D1→D2) by joining Device 1's path to ChaparKhane with ChaparKhane's known path to Device 2 (reversed appropriately), using the same virtual-switch-hop join rule the [Rules](#rules) already require for mismatched port numbering. This requires no new Discovery round for either device. Whether ChaparKhane exposes this as a pull (request/response) service, a push (proactively distributed directory) service, or both, is entirely a ChaparKhane-level service design decision — Chapar itself has no reason to restrict this to one model, and does not.

Composition shares a single header budget: the composed Path(D1→D2) carries both legs inside one 255-hop maximum, so the two legs' hop counts must sum within it — two legs of roughly 127 hops each already exhaust the space. This caps the reach of coordinated device-to-device pairing; single-legged coordinator contact keeps the full range, and tiered topologies whose depths are a handful of hops sit far below either bound.

If more than one ChaparKhane is present on a segment and responds, Chapar imposes no limit and arbitrates nothing between the responses — path selection among multiple valid responses is a ChaparKhane / higher-layer coordination concern, not a Chapar-layer one.

Path refresh after topology change: Chapar has no dedicated re-discovery mechanism. Because no Chapar frame travels without an accompanying higher-layer packet, an ordinary upper-layer timeout/retry on a failed send is expected to be what triggers a fresh Discovery — the endpoint whose send timed out re-announces itself, and the new flood rebuilds reverse paths toward it through whatever the topology looks like now. ChaparKhane may optionally propagate a "path changed" notification to authorized upper-layer subscribers (access-controlled) as an additional optimization, but this is not required for correctness.

Discoverability policy: whether a device responds to a Discovery broadcast at all is a decision made above the Chapar layer (by the host OS or application), comparable to a network-discovery toggle in general-purpose operating systems. Chapar neither mandates nor restricts this.

Discovery is very likely not the only service built on this pattern — Emergency signaling is another named use for Broadcast, and there may be others. Exactly how many such services exist and what each one does is a question for ChaparKhane's own service design, not for Chapar; nothing in this topic should be read as an exhaustive list.

#### Discussion

##### Motivation
Earlier review of the spec flagged a real gap: nothing in the protocol described how an endpoint obtains the hop-port sequence it is required to place in every Unicast frame's header. Without an answer, "stateless switching" and "source routing" are individually well-specified but the system as a whole is not — a device would have no way to send its first frame at all. This is not a problem unique to Chapar: Ethernet devices resolve the equivalent problem via ARP (address to MAC) plus each switch's own MAC-learning, so a reader should not conclude that path establishment is a novel cost Chapar introduces — only that Chapar's mechanism for it needed to be written down.

##### Rationale and alternatives
- Discovery is one-way by design: as an sRPC service call, it is request-only and defines no response. A device announcing itself is not opening an RPC exchange that something must complete — it is closer to a self-timed, event-driven broadcast, sent at join time and again only on an upper-layer failure indication; every announcement is identical whether it is the device's first or a refresh, and any interested party may act on it or ignore it. A fixed, well-known `StreamID` (e.g. `0`) is enough for this, precisely because there is no reply expected on that stream to disambiguate.
- The MAY/MUST split (any node may react; ChaparKhane must) is a deliberate policy placement: reacting is optional and a policy decision for ordinary nodes, while the network's mandatory coordinator always reacts, guaranteeing every completing device acquires at least one usable path.
- Reacting means independently initiating its own new contact with the new device — a fresh Unicast frame using the accumulated hop-port sequence, reversed, as the path — rather than sending a coupled RPC response on the announcer's stream. This distinction matters: it means the general sRPC mechanism for disambiguating multiple same-`StreamID` responses to a broadcast (by pairing `StreamID` with the sender's reverse-path address) is not actually needed for Discovery's own announcement stream, since Discovery never has a reply on that stream to disambiguate in the first place — any reaction to it is its own, separately-identified communication. That general sRPC mechanism may still matter for other broadcast scenarios; that is a question for sRPC's own documentation, not this document.
- Alternative: give ChaparKhane a dedicated route-computation and distribution protocol (link-state or distance-vector style) instead of relying on broadcast-flood reverse-path accumulation. Rejected for the common case: it would reintroduce meaningful state and a separate control protocol for a problem the existing port-rewrite rule already solves for the primary case (reaching a coordinator).
- Alternative: require every switch to cache recent FrameIDs to deduplicate the Discovery flood. Rejected: reintroduces per-switch state, and duplication cost during the rare Discovery event is already addressed as acceptable in [Frame types](#frame-types).

##### Drawbacks
- Relying entirely on upper-layer timeout for path-staleness detection means the delay before a broken path is noticed and re-discovered is whatever that upper-layer protocol's timeout is — Chapar contributes no faster signal of its own.
- Because announcements define no response, a freshly accumulated path is unvalidated until its first real traffic succeeds; nothing in this layer confirms reachability earlier. The first delivery attempt doubles as the path test, and the upper-layer timeout remains the sole failure detector.
- Device-to-device path composition makes ChaparKhane a required party in establishing *any* new device pairing, even between two devices that could otherwise reach each other directly — this is a deliberate centralization at the coordinator, not a free byproduct.

##### Prior art
- Reverse-path learning during flood-based route discovery is used in ad hoc/mesh routing protocols (e.g., AODV-style route requests), where a broadcast request accumulates path information that a unicast reply then uses in reverse — structurally similar to the mechanism here, at a different layer.
- Ethernet's ARP (resolving a network-layer address to a MAC address) combined with per-switch MAC-learning solves the equivalent problem — a device needing a usable path to another device before it can send — by different means (a broadcast query answered directly by the target, plus stateful learning in every switch, rather than reverse-path accumulation with stateless switches).

##### Unresolved questions
- None remaining at the Chapar-layer for the core mechanism described above. Two related items are explicitly out of scope rather than unresolved: the specific `ServiceID` values for Discovery and Emergency belong to sRPC's service registry, not this document; and whether ChaparKhane offers path lookup as pull, push, or both is a ChaparKhane service-design decision, not a Chapar protocol one.
- **Discovery response authenticity** is a genuinely open question for the Discovery service itself (not a Chapar concern, and not something Chapar's security Non-Goal has any bearing on): since any node may optionally respond to a Discovery broadcast, should the Discovery service require responses to be signed, verifiable against a certificate both parties trust? This is entirely decidable at the sRPC/Discovery-service level and is not blocked by anything in Chapar. One open sub-question worth flagging if this direction is taken: a certificate-based scheme still needs a trust anchor (the CA certificate itself) present on both the device and ChaparKhane *before* the device's very first Discovery — for a large population of low-cost devices (e.g., thousands of sensors), how that initial trust anchor gets provisioned is its own design question, not automatically answered by choosing to require signatures.

##### Future possibilities
- A future ChaparKhane-focused document could specify its path-directory service (pull, push, or both) in detail — that design is independent of anything decided here.
- A future Discovery-service document could specify the signed-response scheme above, including how the initial trust anchor is provisioned for low-cost devices at scale. This connects to a separate, larger planned document track (in the Organization private repository) covering manufacturer-issued default device certificates and organizational ownership transfer — that track is where the trust-anchor provisioning question above is expected to be resolved, not here.

### Switching

#### Blocking Switch
Transmitting will block sender until frame transmitted successfully. Sender can be sure frame transmitted.

This is the stronger guarantee of the two classes: the send call returning *is* the confirmation, so the sender knows the frame crossed the link without needing any higher-layer acknowledgement. The cost is that the sender waits for the full transmission to complete.

#### Non blocking Switch
Transmitting will not block caller to be non blocking and queue frames for congestion situations.
A situation might be occur that a port available when a frame queued but when the time to send is come, the port broken and sender don't know about this.

Nothing in this layer reports that loss back to the sender — its frame was accepted into the queue, so from the sender's side the transmission looked successful. Recovery belongs to the upper layer: its timeout on the unanswered communication is what eventually detects the dead path and triggers a fresh [Discovery](#discovery). That silent-loss window is the trade non-blocking operation makes in exchange for never stalling the caller under congestion.

### Rules
- HopCount encoding: `0x00` is reserved exclusively as the Broadcast sentinel, carrying the full 255-slot hop-port space with zero-length data in each slot. Values `0x01`–`0xFF` indicate a Unicast frame with 1 to 255 intermediate hops respectively.
- BroadCast frame must have all hop port number space with 0-byte data in the header, otherwise other frames in the packet manipulates(rewrite) by switches devices.
- When two peer connect by two different port number, one of them must be as switching adaptor. That means **usually higher hop** must add virtual switch hop to switching road. It will add one more hop port number in each chapar frame.
- In each hop, the Switch device must rewrite the received port number on the frame.
- A forwarding switch advances Next Hop past its own stamped position before sending onward; Next Hop is a moving index into the hop-port list, not a static field.
- Terminal cases are closed at this layer and produce no response from it: a Unicast frame whose Next Hop points past the last hop-port entry has no legitimate next hop and is dropped; a frame whose indicated port does not exist or is down is dropped as undeliverable at that switch; a Broadcast copy reaching the end of its flood path is dropped as a stray frame. Recovery in every case belongs to upper-layer timeouts ([Discovery](#discovery)). A rising rate of such drops is a misbehavior indicator for the layers that watch (see [Misbehavior traceability](#misbehavior-traceability)), not a condition this layer manages.

#### Discussion

##### Rationale and alternatives
- HopCount encoding: since a Unicast frame must have at least one hop, `0x00` would otherwise be unused by Unicast, so it is repurposed for Broadcast instead of adding a dedicated field.
- The port-rewrite rule exists for three reasons:
    - BroadcastFrame: To improve performance, the previous switch just sends a frame without declaring the next port.
    - UnicastFrame: To be sure receive port is the same with declaration one in a frame.
    - Rule&Security: To be sure the physical network port is the same on the sender and receiver switch.
- Why the Broadcast header must reserve the entire hop-port space: the rewrite happens in place, as an unavoidable side effect of forwarding — a receiving switch stamps its arrival port into the frame without negotiating with anyone about where writing is allowed. On a flooded Broadcast every traversed switch stamps, so the frame must arrive carrying room for the worst case: the full 255 zero-filled slots. If a Broadcast reserved less than the whole space, some switch's mandatory rewrite would eventually fall outside the reserved area and manipulate whatever bytes follow it in the packet — which belong to other frames' data. Reserving the whole space converts that hazard into harmless zero-fill.
- What the virtual-switch-hop rule is for: two peers each number their own physical ports independently, so when they connect directly, the port number one declares and the port number the other actually uses do not correspond. A path crossing that junction needs one extra, purely logical hop — the virtual switch hop, added by the adaptor side (usually the higher-hop side of the composed path) — so both halves of the path stay expressible in the same one-byte-per-hop format; the cost is exactly one additional hop-port byte on every Chapar frame crossing the junction. [Discovery](#discovery)'s device-to-device path composition joins two paths across precisely this kind of mismatched boundary at ChaparKhane, using this same rule.
- Why no header checksum exists, and why loops nevertheless stay impossible in practice: an end-to-end header integrity field is impossible over a header that every hop rewrites in place — the sender could never predict the bytes a receiver would check. Integrity is therefore delegated downward, to layer-1 frame CRCs, which discard corrupted media frames before they become a Chapar concern. Given a well-formed header, Unicast loop-freedom is structural — the port sequence is finite and fixed; corruption severe enough to forge a cycle is caught below this layer, and a rising rate of malformed drops is treated as misbehavior (see [Misbehavior traceability](#misbehavior-traceability)).
- This single rule is also what makes [Discovery](#discovery)'s reverse-path accumulation and [Misbehavior traceability](#misbehavior-traceability) fall out of ordinary forwarding for free, with no additional mechanism.

### Misbehavior traceability
In Ethernet, tracing a misbehaving device (e.g., one generating a broadcast storm or forged traffic) back to a physical port requires switches with dedicated management capability — an SNMP agent, a MAC-table query CLI, or an equivalent "managed switch" feature set — which is a real, non-trivial cost most cheap/unmanaged switches simply do not have. Without it, locating the offending physical port on a large flat Ethernet segment can require walking the topology switch by switch.

Chapar does not need an equivalent dedicated management feature to get the same result, because every switch already performs the relevant work as an unavoidable part of ordinary forwarding, not as an optional add-on: the [Rules](#rules) require every hop to rewrite the received port number into the frame based on the port it physically arrived on, and to verify a Unicast frame's declared port against the physical one. A device cannot make its frames claim a path other than the one they actually traveled, because that path is stamped by switch hardware, not asserted by the sender. So for any frame that reaches ChaparKhane (directly, as a Broadcast, or as a Unicast destined to it), the accumulated header already is a truthful physical trail back to the originating port — without any switch needing a management plane at all. The cost of traceability is paid once, in the base protocol design, rather than per-switch as a purchasing decision.

This is a genuine structural advantage, but it should not be overstated in one respect: it makes misbehavior *traceable*, not *undetectable-proof against being attempted*. Traceability only translates into an actual response if something (ChaparKhane, an operator, an observability tool) is actively watching for it — the same is true of a managed Ethernet switch's MAC table, which also does nothing on its own until someone queries it. A determined attacker seeking a brief, disruptive burst (rather than sustained, stealthy access) is not necessarily deterred by traceability alone, in Chapar or Ethernet. The claim made here is narrower and still meaningful: Chapar makes this class of investigation possible on hardware where Ethernet would make it impossible (unmanaged switches) or expensive (managed switches), not that it eliminates the incentive to attempt an attack.

On the security Non-Goal (see [Goals and Non-Goals](#goals-and-non-goals)): the risk of a compromised device flooding a local segment with traffic (frames, broadcast storms, forged headers) is not a risk introduced by Chapar. Comparable attacks (e.g., MAC flooding) already exist against Ethernet and other layer-2 protocols today, on networks that do implement broadcast/multicast restrictions and address learning. Chapar does not attempt to solve this class of problem at the protocol layer, consistent with treating physical/access security as out of scope.

### Goals and Non-Goals
Chapar's goals, in plain terms: keep switching logic simple enough to eliminate the need for expensive hardware; keep per-bit network cost down, not just raw bandwidth; support very large layer-2 networks (into the hundreds of millions or more of nodes, depending on topology depth) without needing a layer-3 protocol just to scale; and reduce power consumption both directly (switch hardware) and indirectly (cooling).

Equally important are the things Chapar explicitly does not try to do — each of these is a deliberate boundary, not an oversight:

- **Security** is left to physical access control and to ChaparKhane as network coordinator, since layer 2 is inherently tied to physical-layer access. Layer 1 can provide immediate containment when instructed by an authorized coordinator — shutting down a wired port, or de-associating a wireless client — but this is a mitigation step, not a resolution, and the two cases are not equivalent. For a wired link, cutting logical access is a reasonably complete containment of that specific connection, though the underlying physical-security issue (an unauthorized device or person on the premises) still needs a human/physical response. For wireless, containment is structurally weaker: the medium is inherently shared and broadcast, so a de-associated device can still jam the channel or passively eavesdrop on traffic within range regardless of its protocol-level connection state — de-authentication removes a device from the protocol, not from the physical medium. In both cases, disconnecting a misbehaving device buys time and starts the response; it does not substitute for physical security intervention.
- **Error detection** belongs to layer 1 (link health) or to upper layers (end-to-end data integrity), not to this layer.
- **Fragmentation** is not handled here; MTU limits are a concern for whichever layer decides how to split data.
- **Switching loops** do not need separate prevention logic, because the hop-bounded, source-routed frame structure makes them structurally impossible for Unicast (see [Frame types](#frame-types) for the Broadcast case specifically).
- **Backup links / fault tolerance** across multiple physical paths is left to endpoints and the network coordinator, since handling it here would require exactly the kind of per-switch state Chapar is designed to avoid.
- **Bandwidth management / QoS** is left to layer 1 and layer 3, since layer 2 cannot even distinguish inbound from outbound traffic on its own.
- **VLAN-equivalent segmentation** is left to layer 3 (via ChaparKhane), for the same state-avoidance reason as QoS.
- **Multi-path memory at peers** is not a Chapar concern; a peer may choose to remember more than one path to another peer, but Chapar does not require or manage this.
- **Recovery after wiring changes** has no dedicated mechanism; see [Discovery](#discovery) for how a broken path is typically re-established via ordinary upper-layer retry.

Each Non-Goal above is, by definition, a capability the protocol does not provide — a network operator who needs built-in QoS, VLAN-equivalent segmentation, automatic multi-path fault tolerance, or layer-2 security must get it from another layer or another tool. This is a deliberate scope choice, not an accidental limitation, but it does mean Chapar cannot be adopted as a drop-in Ethernet replacement wherever those capabilities are assumed to be present at layer 2.

#### Topology capacity examples
These examples show how many hosts a Chapar network can reach at different topology depths, assuming each switch has up to 256 ports (255 usable for downstream connections plus one reserved):

- **Two-tier (core/edge)**: 1 core switch + 256 edge switches connects 65,280 hosts (65,536 − 256) with a single physical link between core and each edge switch. With 2 core switches and dual links throughout, this becomes 65,024 hosts (65,536 − 256 − 256).
- **Three-tier (core/distribution/access)**: 1 core + 256 distribution + 65,280 access switches connects 16,646,400 hosts (65,280 × 255). With 2 core switches and dual-homed access switches, this becomes 16,516,096 hosts (65,024 × 254).
- **Three-tier with wireless access**: 1 core + 256 distribution + 65,280 wireless-access switches connects 4,261,478,400 hosts (65,280 × 65,280), given each wireless access point can address up to 65,536 devices (see [networking-hardware.md](./networking-hardware.md) for the wireless addressing rationale). With 2 core switches and dual-homed wireless-access switches, this becomes 4,228,120,576 hosts (65,024 × 65,024).

A ChaparKhane router with 32 GB of RAM can comfortably handle routing for a network in this range, as long as its own outer-network capacity satisfies the aggregate demand of its nodes. Nodes only depend on ChaparKhane for outer-network routing (with no need for anything like NAT); inner-network connections use ChaparKhane purely as a coordinator, secured via GP or IPsec.

[Reference topology diagrams](https://viewer.diagrams.net/?tags=%7B%7D&highlight=0000ff&edit=_blank&layers=1&nav=1#R7V1Lk5s4EP4te3Btcpgp3tjHzCTZpCqp3aqp2k2OMsigHYxYkF%2F59SuBZCOEsT3GwIx9GUPrAfT3davVEszIfJyv%2F0hBEn7HPoxGhuavR%2BbHkWGMxxr9ywSbQmCzMyYIUuQXIn0neEK%2FIBfydsEC%2BTCTKhKMI4ISWejhOIYekWQgTfFKrjbDkXzVBARQETx5IFKl%2FyCfhPyxDHcn%2FwJREIor686kKJkDUZk%2FSRYCH69KIvPTyHxMMSbF0Xz9CCOmO6GXot3nPaXbG0thTI5p8DWZLZdfn0P7aakB68fi8e%2Fg%2B92Y3xvZiAeGPn1%2BfopTEuIAxyD6tJM%2BpHgR%2B5D1qtGzXZ1vGCdUqFPhv5CQDQcTLAimopDMI14K14j8YM3vXZuf%2FuS9seOP6%2FLJRpzEJN0UrWxx%2BrNctmuWn4l2GQEp%2BcCYQAVeBLIMeUL8GUXingo9sIffq14uyvAi9WCDTgVNQRpA0lDP2JKAGg%2FEc0hvm7ZLYQQIWsr3ATiNg229HdL0gIN9AvCTfoF%2FEe7uGwHePBP4vCl9MrApVUgwiklW6vkvJqAV1sKhclvnjpj7qc97qttmU3V6UFx%2FR8Dtg7yckzb3lEsQLbgWknBDYQOsaUIJ1y9pjTJr9UbW9kS%2Bc0ml0MCVWbAdlkUPBdd5o4pLaoERukqInAXafLFWuEAH2IQdJin2YEZv8GEVIgKfEpArbkXjExnZKfCeg5wffy5IhGIoobKEKYHrZlxUffMGlqw3XeP%2BdrWLIXQRGISl%2BMHR9iN0lr8XwN%2BG%2BhZtzujI4Z%2BFvDW5edXzEG7dq%2FbtVo3X6lYH6FdrdHmzriOtq5VAWLEuq2frMl%2BrdVmDsy5LUaVhO1TwDqf0r2PbJj2jXWv39%2FfvVUOLfUHnGDNFPfggC3O70mWlMvlfgBCYxrnE0Myc%2BSl%2B3qZ9DMUwj7UEVeElhdo1%2BhSyMw3BHlfwNCdyF4WBKoZQMws40NGlpwGOwoNFkkDGgQhs2G%2F3Lvbl4HOlaveO47itAG25Ewkf8ziHd9Bznk4YURHPZhmU6pyar1DuxWhOWByof5mMhW6%2BLuqdmw1oh2YvZNmpDKpcxm3mT2PtC7FHHd4Ou7VvYAojmQ8gQgEbtzwKP21lPrAogEWgH3jBHPl%2BQT2YoV9gmvfHyMdVSDu3H0b2x6Ywgi%2Bw8Maj7bJGmXUNNtLgBl1duEGuexFBvZStYqlJbqC6pNZwtG%2FDU%2FN0tx2%2F0ZXjUK5zYOg5UF92HseMla0Rs9flPXGc5%2B62Kz5DmXvq7kWGSNNxZK5X50aXDpV7XdiTITeuFXPL7hRzo9fcvoT5dQBuTGTAjXHH%2BVu9T8BPWsx5O5g7PWNu9Iv5NUJu9gx5L9mFPWsH14K51jPmVq%2BYXx%2Fgutsz4PZgAL%2BagF3Xew7YneFgfq2QdzwvFxvGSznC4XDAvVYSuB3b%2FYDycdeCuZKc6Rrznnnfau0PeANTRXN2yOt4BNJiE3LUAPukZ8J4Tctdo42bPkPecjxv0xs6OkjOdY95vQu5owIePZDXr0jWSujody1AcUMCGv023qjtThBu9bdM11Y1MfMtzvk%2B3eTMMVQSRdVfsu33EEW293bo7o46qIjp%2B31MdWHV7ec%2FCxVRwce9tBRm3Bphq%2Bqk9YNSdSVcIjKHpEjCGpRpMt7Co%2B5lvsOzGgN5gUQeFK4TFHJ4XGyu4jAwnYuqe0oOA5A9eCGY4DzN2wDj%2FLbAouMvyGOsDraBbybpoxstFR1R3TBkRDZYNbbrw2ZudtL8VIl7IYOfXTUV9WhAyhsTRJv%2BBeeNAvABG44U8YFDaoTgjEPhMh2AJt00LihW0qzYREqrE4jEVcUkdB%2BnZ5q5hFrQWuj2J%2BS2w1XbGFbqqTmS74bSbd5bUYEhBo4tZw563qLdlg3mL2jr2uxmWUU%2BFc%2BciYsVXfOpCfMLnwLbi1j57UfPCYPUVUi1ezOnfvFTrOfMw5MSD1ewt7rR7rryzt7RXOHPk%2FPXkr7YY9dfZvxW9sX5%2FW9GFkZdIXholS%2B%2FHatMUMSYMeQZeAcV2aibgdRHS5cYcdZ73xnzESz8K0qJvse1jx6kLvdduHRinLpwzs4wjxqmhJ8%2BEpYg55%2BTI3Fn1naXWTNeuyZ01j%2F497xgb9vh%2FGdPrari3Thm%2BW7NrNf58vUOzOT5ibB53OjZ3mb1YhTBmQ9QKS0kLzQPx7yTXQgrVxAJmbTIwh5LHme7SHbeMQznjIL%2BtbNdlHOqGEPtiQ4gaW1%2BOYSkMFhFIR4dzYg6YM7uPp1lu%2FqUsV7V%2B4V14rizPtd7SYCeSciyT0u3b69k1K0%2BvL1jU5cFkANGiunIkeJ8lIK61bK9gG7PqNJi%2B04ovJomf97mqtNz8Z2COok1R9QuMlpAZQqm85B507h54QXFRVhLjdA6iUtkSpAjQX2pOgCxS9jHvxnoeSPZVWXEVs0JLK6Z3WgTZd5vu6ON7KA7UljhNQhDzLo1CxtzAHbd8Jt4avyhDNFiO%2BZU08ah5CUlpZzPav7gSN2HGifxr46XLrHDqyze27Ys%2By%2FQZ0e5Yn4WjuOOskurt2H1XwdFgJsYgLB%2B8L92pDz2c0qgXx3ckRN5znJsTa45iRJDQT7VuCcvGeqXbkerNIgxIVTk%2BypIIbET13EwN7Tc0Z54AxKR2qEmY%2B82nO1vPXpC82bkf8Bct%2BIXK57AcTXULVo1XMC7mFepeLrh5hZtXeLteYeg%2BwRarOr35hP3TzptPuPmEm0%2FowCdYtryXpv9AQf0W%2BM0p3JzCW3YKA5w%2BWLbRVaxAT3f%2FYapYMNj9my7z0%2F8%3D)

#### Discussion

##### Drawbacks
Two Non-Goals worth flagging together: **Backup links** and **Multi-path memory at peers** both note that Ethernet switches supporting multi-path forwarding suffer a large performance penalty — this observation motivates why Chapar does not attempt multi-path support either, rather than treating single-path-only as a mere simplification.

##### Rationale and alternatives
- Alternative: absorb one or more of these Non-Goals directly into Chapar (e.g., built-in QoS or multi-path support). Rejected in each case for the same underlying reason: doing so would require some form of per-switch state, which conflicts with the core stateless-switching goal this protocol exists to achieve.

##### Prior art
Chapar draws on ideas from several existing systems and standards rather than inventing every mechanism from scratch:
- [guifi.net](https://guifi.net/) — community-network topology and operation at scale.
- [Telephone exchange](https://en.wikipedia.org/wiki/Telephone_exchange) — circuit-switching heritage informing the peer/frame state model.
- [Fast packet switching](https://en.wikipedia.org/wiki/Fast_packet_switching)
- [SDU](https://en.wikipedia.org/wiki/Service_data_unit) vs [PDU](https://en.wikipedia.org/wiki/Protocol_data_unit) — framing terminology.
- [ETSI](https://www.etsi.org/) standards
- [Asynchronous Transfer Mode](https://en.wikipedia.org/wiki/Asynchronous_Transfer_Mode) — fixed-size cell switching heritage.
- [IEEE 802](https://www.ieee802.org/)
- [Frame Relay](https://en.wikipedia.org/wiki/Frame_Relay)
- Further background: [supporting articles](https://www.dropbox.com/sh/51l4x1p2e8lub5x/AABVgFyJ0fuia8QZt7SEZgBWa?dl=0)

##### Unresolved questions
None specific to this topic at the time of writing; individual Non-Goals may need their own follow-up document if a future requirement forces reconsideration (e.g., if a real deployment needs layer-2 fault tolerance badly enough to revisit the multi-path decision).

##### Future possibilities
If a specific deployment (e.g., a large greenhouse or industrial site) hits a hard requirement that a Non-Goal currently excludes, that should become its own document proposing a targeted extension, rather than reopening this document.

### State model compared with Ethernet
Ethernet switches build a MAC address table by watching traffic (a "learning" process) so that every switch on a path knows which port leads toward which address. This table is state, and it must be built, maintained, and kept consistent on every intermediate switch, in addition to whatever state the two communicating endpoints keep about each other.

Chapar frames instead carry the entire forwarding path — the sequence of outgoing port numbers, hop by hop — in the frame header. An intermediate switch does not need to know or remember anything about the network; it only reads the header field that applies to its own position in the path and forwards accordingly. All the "where does this go" knowledge lives either in the frame or at the two endpoints, never in the switches in between.

This has two independent consequences, and they should not be conflated:

- **Hardware cost**: a switch that never needs to search a large, dynamically-updated address table can be built from small, fixed-function comparison logic instead of power-hungry CAM. This — not header size — is the primary reason Chapar switching and network-adaptor hardware can be cheaper than Ethernet's.
- **Header economics**: Chapar's header cost scales with topology depth (one byte per hop) instead of being a fixed cost regardless of network size, as Ethernet's 6-byte MAC addresses are. This means the two protocols are not comparable at a single fixed overhead figure — the comparison must be made across a range of network depths.

#### State location
Ethernet requires state in three places: the frame (addresses), the two endpoint peers, and every intermediate switch (the learned MAC table). Chapar requires state only in the frame and at the two endpoint peers — intermediate switches hold none. This document deliberately avoids classifying either protocol as "connection-oriented" or "connectionless" in the formal networking-textbook sense; the terms carry established meanings elsewhere that this comparison does not need to invoke. The only claim made here is about the location and lifetime of the state each protocol requires, which is directly verifiable from each protocol's own mechanics.

#### Other cited Ethernet drawbacks
The original motivation for Chapar also cited three further Ethernet drawbacks, carried over here for completeness: high price relative to bandwidth delivered (cost per bit transferred matters more than raw bandwidth), high power usage tied to CAM-table lookups, and closed-source, vendor-specific switching hardware and algorithms. These are stated as motivating context rather than independently re-verified claims; if any of them needs its own sourced justification later, it should get one.

#### CAM table ceiling
The claim of up to 512,000 MAC-table entries as an upper bound on "the best switch" is consistent with publicly documented capacity: enterprise/data-center-class switches are commonly reported in the range of tens of thousands up to several hundred thousand MAC-table entries, depending on model and vendor. No single, precisely sourced switch model with exactly 512,000 entries has been confirmed at the time of writing; the figure should be treated as an order-of-magnitude ceiling rather than a citation to a specific product, unless a specific source is added later.

#### Header cost vs. topology depth
For a shallow network (a sensor a few hops from its gateway), Chapar's header is well under 10 bytes total. Ethernet's per-frame address overhead is fixed regardless of network size: 14 bytes (destination + source MAC + EtherType), 18 bytes including the trailing FCS, or 22 bytes with an 802.1Q VLAN tag.

At Chapar's own budget matching Ethernet's fixed cost — four fixed fields plus about sixteen hop-port bytes, a ~20-byte header sitting inside the same 14–22-byte range Ethernet itself spans across its plain, FCS-inclusive, and VLAN-tagged forms — Chapar's source-routed header addresses on the order of 255^16 nodes along that specific path depth — many orders of magnitude beyond Ethernet's flat 2^48 MAC address space (255^16 ≈ 10^38.5 vs. 2^48 ≈ 2.8×10^14, a difference on the order of 10^24). The comparison is therefore not "Chapar is cheaper for small networks" — it is that Chapar's cost buys topology depth and reach directly, while Ethernet pays the same fixed cost whether the network has ten nodes or ten million, and additionally needs CAM-table state to make that fixed-size address usable at scale.

This comparison is sometimes misread as conceding a weakness unique to Chapar — that its advantage holds only in shallow networks. Stated plainly: shallow-to-medium depth is where every practical layer-2 technology lives. Ethernet's usable layer-2 diameter is small in real deployments for its own structural reasons — spanning-tree convergence limits, the blast radius of a single failure domain, broadcast-domain growth, and address-table pressure drive organizations onto routers early, often for nothing more than a multi-floor building. Beyond that range both protocols hand off to layer 3; the difference is economic, not territorial: Chapar reaches the hand-off point on cheaper, lower-power switching hardware, because its switches never needed CAM silicon at all. What Chapar equally does not claim is deep, flat, dynamic meshes as home territory: per-frame headers grow with depth, mobility multiplies re-discovery events, and such networks belong to the mesh-routing space above this layer — the very space Chapar's own Discovery pattern was borrowed from.

#### Discussion

##### Drawbacks
- This topic's numeric comparisons (255^16 vs. 2^48, CAM table ranges) depend on assumptions (uniform hop-port width, symmetric port numbering) that may not hold in every real topology; they are illustrative, not a guarantee for any specific deployment.
- Avoiding the "connection-oriented / connectionless" classification sidesteps a question some readers will still ask; this document should link to, rather than re-open, that debate if raised again.

##### Rationale and alternatives
- Keeping this comparison inline interleaved with the normative rules, as it originally was, forced every reader of the rules to also evaluate an argument about a different protocol before understanding Chapar's own mechanics. Keeping it as its own topic — with the comparison confined to this bundle — keeps the rules clean while retaining the comparison.
- Dropping the Ethernet comparison entirely was rejected because the motivating "why" for several protocol decisions (no CAM dependency, source routing) is meaningfully clearer with the comparison than without it.

##### Prior art
Segment/source routing in general (e.g., IPv6 Segment Routing, MPLS explicit paths) trades per-hop state for path information carried in the packet — a similar state-location trade-off to Chapar's, at a different layer.

##### Unresolved questions
A precise, sourced figure (specific switch model and vendor documentation) for the "best switch" CAM ceiling has not been confirmed.

##### Future possibilities
A follow-up empirical comparison (real header-byte counts against real deployed Ethernet topologies of comparable scale) could replace the illustrative math above with measured data.

## Results
Insufficient deployment experience has been recorded for this specification to report real, observed outcomes. This section will be filled in once there is such experience to draw on.

## Discussion

### Drawbacks
Consolidating the specification and all of its rationale into one document makes the file long, and a reader seeking one specific piece of rationale must load the whole document. The mitigating factors are structural: the normative text is concentrated in each topic's leading statements and in the first half of the document, every `Discussion` bundle is skippable without losing normative content, and heading navigation reaches any topic directly.

### Rationale and alternatives
- **Keep the four companion documents as separate files (rejected)**: they formed one continuous argument — each depended on and extended the others — yet forced a reader following any rationale path to load three or four files, and turned the spec itself into a hub of "see related document" pointers.
- **Move all rationale into a single separate companion file instead of distributing it into topic-level `Discussion` bundles (considered, not chosen)**: this still splits one subject across two files and forces a reader who wants both the rule and its reason to keep two documents open; the chosen structure keeps each topic's "how" and "why" adjacent, and keeps placement predictable — rationale is always in the topic's `Discussion`, never somewhere else.
- **Keep the pre-consolidation structure unchanged (rejected)**: it was the older documentation method this revision migrates away from; the record of that migration lives in [chapar.changelog.md](./chapar.changelog.md), not in this document's body.

### Unresolved questions
Whether this document should be split again if its length ever becomes a real reading burden — mirroring the open question in [documentation-explanation.md](./documentation-explanation.md) about its own consolidated structure.

### Future possibilities
If a single topic's rationale grows unwieldy (for example, if the Discovery signed-response scheme becomes a full design), it should spin out as its own document at that point, following the progressive-migration rule rather than a dedicated restructuring pass.
