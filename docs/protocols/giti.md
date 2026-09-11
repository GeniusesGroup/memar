---
Title: "Giti (GP)"
Status: Draft
Start Date: 2026-08-26
ID: 496595
---

# Giti (GP) - Decentralized Interplanetary Network Protocol

## Abstract
Giti or the Giti Protocol (**GP**) is this project's network-layer protocol, built on one deliberate inversion of today's Internet: it connects **applications**, not devices or operating systems. Every GP packet carries self-describing frames inside the [Networking](./networking.md) packet model; endpoints are addressed by hierarchical locators — Society / Router / Thing, optionally ending at App — whose field widths are justified by the operational capacity of each scope rather than inherited from any predecessor, and whose reach extends across societies without a central registrar, across the world, and even across planets — where a destination's planetary position is routing knowledge about societies, never a per-packet address field. GP defines two independent routing frames, one delivering to a Thing and one delivering to an App, so each packet carries only the destination level it actually needs; routers are expected to be network *coordinators* (the [ChaparKhane](./chapar.md) role) rather than bare gateways, running over [Chapar](./chapar.md)'s stateless switching or any existing data link. This document consolidates Giti's two legacy files — the project-vision read-me and the GP protocol specification — into a single specification; its two routing frame types are registered as numbers 4 and 5 in [Networking](./networking.md)'s registry.

## Introduction

### Motivation
In the IoE era (the Internet of Everything, beyond today's IoT — Internet of Things), the main goal of computer networks must be connecting **applications**, instead of connecting OSs and devices. As DevOps culture takes part in improving how software is developed, the global network deserves the same care: administrator tasks around addressing and registration should shrink toward zero, which is what a decentralized, automatic protocol buys. IP(v6) is a good protocol, but it was designed to connect devices in a very manual manner; GP differs in internal service calls, security, pipelining, multiplexing, and more, and those differences compound into a large advantage for application-level network performance. Software routers based on this model — built on code-generation tooling but also usable through plain package APIs — carry the same promise.

The concrete case against carrying GP's role on IP, point by point:

- IP Routers can just be a gateway or can't be as network coordinator
- Registering system is centralized and manual human base
- IP leases fee is high
- IP addresses can't (or very hard to) register by end-user devices and usually register by ISPs
- IP addresses can't prove their ownership to use in the authentication process due to the above problem
- IP addresses can easily be spoofed. Spoofing can be used as part of a DoS attack and can't determine the source of an attack
- IP packets want to be multi-frame carriers, but almost always carry just one main frame per packet, indicated by the [Next Header](https://en.wikipedia.org/wiki/IPv6_packet#Fixed_header) field, using extension headers only for some internal protocol mechanisms — not for all the connecting-applications requirements. And unfortunately those frames are introduced by the previous frame instead of introducing themselves.

### Methodology
The design was reached by inverting the unit of connection. Instead of IP's question — how do devices attach and address each other — GP asks how applications address and reach each other directly, then asks two questions of every address component before admitting it: which intermediary on a packet's path actually needs this information, and is the component's width justified by the operational capacity of the scope it names rather than by the maximum imaginable population. Answering those produced the locator hierarchy Society / Router / Thing / App — the levels above the endpoint exist only to deliver traffic toward it, the endpoint level (Thing versus App) is a property of the destination itself, and a destination's planetary location never enters the per-packet common path at all, because a rare capability must not become a mandatory cost carried by every packet. IPv6 served throughout as the standing measuring stick — of what happens when an address size is chosen before any capacity is questioned — and each GP mechanism was still required to answer a specific IP criticism: centralized human registration answered by automatic society/router registration, costly leases answered by free floating leases, gateway-only routers answered by coordinator-capable routers, spoofable and unprovable addresses answered by true 32-byte identities beneath temporary addresses, and single-frame packets answered by multi-frame self-describing frames under the [Networking](./networking.md) model.

## Explanation

### Goals
- Connect applications instead of things or OSs
- Connect things anywhere in the universe (different planets)
- Best use of addressing space allocation and assignment
- Decentralized and automatic process to register routers in any layer
- Free, automated, and floating to lease new GP addresses
- GP routers can be network coordinators alongside being a gateway

### Frame architecture

GP defines two routing frames, one per destination level: a frame that delivers to a **Thing**, and a frame that delivers to an **App** on a Thing. Which level a destination actually has is a property of the destination, not of the topology between the peers — a single-application device (a lamp, a sensor, a camera) presents its application at Thing level, its network driver *is* the application's endpoint, and no App frame is ever needed to reach it. A packet carries at most one GP routing frame, because the App frame is self-contained: it repeats the full Thing hierarchy instead of depending on a Thing frame elsewhere in the packet, so app-level delivery pays the Thing-level bytes exactly once. Frames are never rewritten, expanded, or compressed in flight — what the sender emits is what every intermediary sees, and what the packet signature covers.

The `FrameType` itself announces which destination level the frame addresses and therefore which address layout follows — a reader dispatches on the first byte before parsing anything else, per [Networking](./networking.md)'s self-describing-frame rule.

#### Thing Routing Frame (FrameType 4)
Delivers to a Thing; 21 bytes.

|  bit  | Length(Byte-Octet) |          Data          |
| :---: | :----------------: | :--------------------: |
|   0   |         1          |       FrameType        |
|   8   |         4          | Destination Society ID |
|  40   |         4          | Destination Router ID  |
|  72   |         2          |  Destination Thing ID  |
|  88   |         4          |   Source Society ID    |
|  120  |         4          |    Source Router ID    |
|  152  |         2          |    Source Thing ID     |

#### App Routing Frame (FrameType 5)
Delivers to an App on a Thing; 25 bytes.

|  bit  | Length(Byte-Octet) |          Data          |
| :---: | :----------------: | :--------------------: |
|   0   |         1          |       FrameType        |
|   8   |         4          | Destination Society ID |
|  40   |         4          | Destination Router ID  |
|  72   |         2          |  Destination Thing ID  |
|  88   |         2          |   Destination App ID   |
|  104  |         4          |   Source Society ID    |
|  136  |         4          |    Source Router ID    |
|  168  |         2          |    Source Thing ID     |
|  184  |         2          |     Source App ID      |

Source and destination are always both present and structurally symmetric: the source locator grounds reply addressing and the whole accountability and [source validation](#standard-services) model — trading it away would trade a few bytes for an unattributable network. For scale: the Thing frame carries network and endpoint addressing in 21 bytes, where IPv6 plus UDP spend 48 bytes before any payload arrives. This economy is deliberate, but it is not a license to move data and computation across the network gratuitously — header cost is only one term of total network cost (see [Edge computing](./networking.md#edge-computing)).

#### Compared with the IPv6 packet
- **Versioning**: unlike IP, GP offers no versioning for the protocol — if a fundamentally different protocol is needed after official release, the right move is a new protocol with a new `FrameType` (or another existing solution such as Ethernet's [EtherType](https://en.wikipedia.org/wiki/Ethertype) in the [Ethernet frame](https://en.wikipedia.org/wiki/Ethernet_frame) header), not reinvented version fields.
- **Flow Label**: almost the same role as the Packet Number carried by sRPC's PacketSequenceNumber frame.
- **Payload Length**: a GP packet is not a chain of related frames and has no primary frame; each frame carries its own length where needed, as forced by the [Networking](./networking.md) model.
- **Next Header**: for the same reason there is nothing for a Next Header field to point at — every frame introduces itself with its own `FrameType`, per Networking's self-describing-frame decision.
- **Extended header**: standalone frames replace both the primary-frame/extension-header chain.
- **Hop Limit**: GP suggests the mechanism provided by the ChaparKhane role ([Chapar](./chapar.md)) as its network router/coordinator to reach this requirement.

### GP address
A GP address is a **locator**, not an identity: it says where an endpoint currently sits in the routing hierarchy and nothing about who it is. **All IDs are temporary IDs**: each Society, Router, Thing, and App actually owns a unique 32-byte identifier underneath, and the GP locator is freely re-leased as things move — a Thing that leaves its Router's domain takes a new address, exactly as its Chapar path changes. Binding identity to locator is not this layer's job; see [Ownership proof](./giti.handoff.md#ownership-proof).

Two address forms exist, matching the two routing frames:

|  bit  | Length(byte-Octet) |            Data             |
| :---: | :----------------: | :-------------------------: |
|   0   |         4          |         Society ID          |
|  32   |         4          |          Router ID          |
|  64   |         2          |          Thing ID           |
|  80   |         2          | App ID *(App address only)* |

The Thing address (10 bytes) is what the Thing Routing Frame carries per side; the App address (12 bytes) is what the App Routing Frame carries per side.

- **Society ID**: each society civilization — what a country is today — announces itself and receives a 4-byte unique immutable identifier until it exists.
- **Router ID**: each society delegates its range to some routers to do routing, improving performance and consistency of its own network. A Router always has a 4-byte unique mutable identifier until it exists (society scope). Usually each organization claiming a land (physical location), like a complex building, owns one Router ID.
- **Thing ID**: each `Thing` or device gets a unique mutable identifier from a router (router scope). The device's `Hypervisor OS` obtains this ID and routes applications to register against the hardware driver. Two bytes name 65,536 simultaneously addressable Things per router domain — sized against the per-Thing state a router actually operates (Chapar paths, identity validation, accounting), not against a theoretical population; a larger population is the business of more routers, which is what the hierarchy is for.
- **App ID**: each app gets a unique mutable identifier from the hypervisor (thing scope). An app here means a unikernel OS image running one application over a dedicated OS kernel.

One sizing rule governs every field: **a field's width is justified by the operational capacity of its scope, not by the maximum imaginable global population.** Society (4 bytes → 2³² societies), Router (4 bytes → 2³² routers per society), and Thing (2 bytes → 2¹⁶ per router) compose to a theoretical reach of 2⁴⁸ ≈ 281 trillion Things per society — capacity comes from the hierarchy composing, never from one oversized field.

#### Planetary location is not address data
GP carries no Planet field. A Society is a logical routing domain whose routers may sit in different buildings, different continents, or on different planets; which planet its routers currently inhabit is topology and reachability knowledge distributed through the society's routing — not a cost paid in every packet. A society can move part of its infrastructure to another planet without any address changing: what changes is the routing knowledge that says how its routers are currently reachable. Interplanetary reachability is a routing problem answered by routing knowledge, not an addressing dimension; a rare capability must not become a mandatory cost of the common path.

#### Compared with IPv6 addresses
The correspondence is conceptual, not embeddable: GP addresses encode society hierarchy rather than planetary position, so no IPv6 prefix range can hold them — and none is sought, since interoperation with the Internet is packet-level tunneling. Conceptually, IPv6's Routing Prefix maps to `Society ID`; SubNet ID to `Router ID`; Interface ID to `Thing ID`, with `App ID` refining delivery the way ports do above IP — except this port-equivalent is an address component, present only when the destination actually discriminates applications. Where IPv6 fixed 128 bits first and searched for justification afterward, GP derives each width from the operational capacity of its scope.

Some other IPv6 address-renumbering suggestions, with their GP counterparts:
- **Type** (3 bits)
- **Registry ID** (5 bits) — can map in some way to `Planet ID`
- **Provider ID** (16 bits) — an Internet access provider maps in some way to `Society ID`
- **Subscriber ID** (24 bits) — no counterpart in GP
- **SubNet ID** (32 bits) — can map in some way to `Router ID`
- **Interface ID** (48 bits) — can map in some way to `App ID`

### Society registration
Each society in Giti must pick a primary name that is a combination of at least three Unicode characters and use the hash (SHA3-256) of it as the UUID of the society. The picked name also serves as a TLD, letting the society register any domain under its name — e.g. society name "persia", and "athenafarm.persia" is a domain belonging to that society.

Each society registers one unique 32-bit unsigned integer by a specific algorithm for routing in its database, and tells all physically adjacent connected societies about its existence. How that integer is acquired is recorded as the [Society identifier allocation](#standard-services) capability: a temporary number at first, made permanent by collective agreement.

A society is a logical routing domain, not a physically contiguous one: its routers may sit anywhere — different buildings, different regions, different planets — and need no direct layer-2 adjacency to each other. What binds them is the routing knowledge its routers exchange through the society's [standard services](#standard-services) capabilities; physical carriage between non-adjacent points is [Chapar](./chapar.md)'s business over whatever graph of physically-adjacent hops exists. This split — GP owns the logical destination, the layers below realize each hop — is the same fundamental division IP has always had; GP's difference lies in its address model and accountability, not in inventing the split.

How a society organizes delivery *inside* its own 32-bit router space is entirely its own affair — routing at this scale is a small problem only on paper; it takes creativity, testing, and methods fitted to the society's physical realities. A society may spread the work across every border router, or concentrate it in dedicated core routers that all incoming packets are handed to; this protocol prescribes neither, and no society's interior choice ever changes a frame on the wire.

### Standard services
Societies need a set of capabilities to operate as routing domains — reachability coordination, source validation, incident reporting, router accountability, and society identifier allocation are the needs the routing architecture and the accountability model above already assume. Which of these capabilities harden into protocol-level standard services, and which stay ChaparKhane implementation concerns, is a decision owed when the ChaparKhane role itself is developed: the goal is the least protocol interference — a service fixed at document level becomes part of GP's identity and resists change, exactly as the Internet learned when routing knowledge left IP and grew its own protocol (BGP) so the IP document would not have to change; had BGP's plaintext exchanges been fixed at the IP layer instead, the data-ecosystem damage of that choice would have been much harder to repair. Keeping the roster out of this document is what preserves that same freedom here. The known needs are therefore recorded as needs, not yet as a service roster.

1. **Reachability coordination** — the need: societies must exchange route and topology knowledge — which Society + Router pairs are reachable, through what mediation, including current planetary location where relevant — so that [inter-society delivery](#inter-society-delivery) works without any global routing table.
2. **Source validation** — the need: a router must be able to establish that a packet's claimed source hierarchy is consistent with its validated ingress path — a router MUST NOT accept a packet whose claimed source society could not legitimately originate traffic through the path it arrived on. Which attestation mechanism proves this is deliberately unspecified.
3. **Incident reporting** — the need: complaints and evidence must reach *both* the offending traffic's Router and that society's governing application (the society authority) — never merely router-to-router, since a router may itself be infected or impersonated and must not be the only recipient of accusations about its own behavior.
4. **Router accountability** — the need: a society must be able to accept, answer, and remediate reports about its routers' behavior; the service face of [attack reporting](#attack-reporting-and-society-enforcement).
5. **Society identifier allocation** — the need: how a society acquires its unique 32-bit routing integer — the governing application announces itself and is assigned a number from the societies' temporary range; a collective agreement across societies, under conditions such as a minimum number of active routers or active bandwidth, may convert a temporary identifier into a permanent one. The agreement mechanism is deliberately unspecified.

These capabilities are not auxiliary conveniences: they carry the network's entire accountability model — attack reporting, reputation, blocking coordination, and identity attestation are all designed to ride on them. Writing them well is among the highest-priority open work this document owes; until they exist, the enforcement structures above remain scaffolding.

### Routing architecture
A scoping note before the mechanisms: this layer's whole obligation is addressing and routability — that a packet *can* be addressed to any society and routed toward it. Carrying packets between networks, up to and across planetary distances, is the job of layers 1 and 2 and of the topology built from them; GP claims the map, not the vehicle.

#### Routers
We strongly suggest using the ChaparKhane role ([Chapar](./chapar.md)) for the router mechanism, with [Chapar](./chapar.md) as the link-layer protocol carrying GP packets instead of Ethernet frames. Chapar realizes delivery over a graph of physically-adjacent hops — it is not limited to one hop per relationship; what it requires is that every edge be a real physical or wireless link. GP's goal sits one abstraction above: connecting two endpoints that need not be physically adjacent at all.

#### Inter-society delivery
Reachability between societies is evaluated at **Society + Router** granularity — one router of a society may hold a direct connection to another society that its sibling routers lack, so the Router is part of the inter-society identity. But no router is expected to hold reachability knowledge beyond its own direct connections; the world's (Society, Router) pairs are nobody's table. Delivery follows the connection the sending router actually has, in this ladder:

- **Direct to the destination router** — the sending router is directly connected to it and hands the packet over. This is the normal and encouraged shape: [Chapar](./chapar.md)'s capacity makes direct peering practical at a scale and decentralization where no IXP-like exchange point is needed or wanted.
- **Hand-off to the destination society** — the destination router is not directly reachable, but some router of the destination society is: the packet is handed to that router, which then owns completing the delivery inside its own society — onward carriage to the destination router it has no direct connection to included. Society membership is what makes this hand-off safe: the ingress router is accountable inside a domain whose authority can answer for it.
- **Agreed intermediary** — neither the destination router nor any router of the destination society is reachable: the packet goes through a relaying router the parties agreed on in advance. Mediation is a contract, never a forwarding default; the destination may keep state recording that the origin's traffic currently arrives through that intermediary, and the intermediary is visible and attributable. This shape also raises the digital-economy question this document deliberately leaves open for now: how routing cost is paid between societies (see [Inter-society routing economy](./giti.handoff.md#inter-society-routing-economy)).

In every shape the **last delivering society owns the immediate delivery responsibility**: whatever is wrong with what it handed to the destination — a spoofed source, an ignored block request, abusive traffic — it is the first answerable party and the natural candidate for blocking. Societies earlier in the path remain attributable participants, and evidence can still establish their part; responsibility does not dissolve into the chain.

Physical hops and inter-society responsibility hops are different counts and must never be conflated: a packet may cross a hundred Chapar hops inside one society-to-society relationship, while a four-society mediation chain may consist entirely of physically direct links.

#### Mobile GP
[Mobile GP](https://en.wikipedia.org/wiki/Mobile_IP) allows location-independent routing of GP packets across the network. This specification sets no rules for mobility implementation itself: mobility is achieved by having a proper topology in your society network and data link layer.

#### Quality of Service
QoS must be handled in routers, not protocol packets — consistent with the congestion treatment in [Networking — Hardware](./networking.md#hardware). How routers actually schedule, queue, and prioritize is a ChaparKhane implementation concern — a commercial component (see [Enterprise](../README.md#enterprise)) — deliberately left unspecified here so that neither creativity nor the product is constrained by premature rules.

#### Local network
When no GP router exists in a network, GP cannot be used properly. Nodes can still fill the Society and Router fields with arbitrary data and send Thing-level packets to other nodes, but peers cannot prove their identities strongly to each other — which this shape states honestly, since nothing in such a network backs the locator it claims.

#### Multicast & anycast & broadcast
Because this spec must stay decentralized — and because these requirements belong at the application layer to protect user privacy — GP offers no way to multicast, anycast, or broadcast a packet in Giti networks.

### Attack reporting and society enforcement
Routers, OSs, and apps can request action from each other — report attackers and block them. If routers do not respect a reported node or router, whole societies can block the offending society. AI must be added to router applications to detect infected or misbehaving routers that don't respect the rules. A complaint travels to the offending traffic's Router *and* to that society's governing application — a compromised or impersonated router must not be left alone to receive accusations about its own behavior.

What this topic deliberately does *not* fix is the binding/authentication method behind a report: GP intentionally specifies no definitive identity-attestation scheme here, so that no single approach hardens into law and crowds out better ones. What the protocol does provide is the structure accountability needs — every Router ID range belongs to a specific, identifiable organization, and the mandatory society/router services below exist precisely to exercise that accountability. This is where GP structurally parts ways with IPv4/IPv6: there, a report's origin dissolves behind VPNs and shared carriers with no one answerable; here, a report always terminates at an accountable range owner. Spoofing inside a range remains possible — but the range owner answers for it, which shifts enforcement from per-packet forensics (impossible at Internet scale) to organizational responsibility (enforceable).

### Implementation and status
GP is simple enough to encode and decode easily in any programming language. Implementations exist or are in progress in Khayyam ([memar-khayyam/net/GP](https://github.com/GeniusesGroup/memar-khayyam/blob/master/net/GP)), C, Go ([memar-go/net/GP](https://github.com/GeniusesGroup/memar-go/blob/master/net/gp)), JavaScript, and more. The current implementation is considered alpha; compatibility with future versions is neither guaranteed nor expected. GP can ship inside os, device drivers, apps, ... due to its very simple spec. The software routers of this ecosystem differ in internal service call, security, pipelining, and multiplexing, and are based on code-generation development while remaining usable through plain package APIs.
