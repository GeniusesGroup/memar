---
Title: "Giti (GP)"
Status: Draft
Start Date: 2026-08-26
ID: 496593
---

# Giti (GP) - Decentralized Interplanetary Network Protocol

## Abstract
Giti or the Giti Protocol (**GP**) is this project's network-layer protocol, built on one deliberate inversion of today's Internet: it connects **applications**, not devices or operating systems. Every GP packet carries self-describing frames inside the [Networking](./networking.md) packet model; every endpoint holds a hierarchical 128-bit address spanning Planet / Society / Router / Thing / App so traffic can route across societies and even planets without any central registrar; routers are expected to be network *coordinators* (the [ChaparKhane](./chapar.md) role) rather than bare gateways, running over [Chapar](./chapar.md)'s stateless switching or any existing data link. This document consolidates Giti's two legacy files — the project-vision read-me and the GP protocol specification — into a single specification; its frame type is registered as number 4 in [Networking](./networking.md)'s registry.

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
The design was reached by inverting the unit of connection. Instead of IP's question — how do devices attach and address each other — GP asks how applications address and reach each other directly, then derives what an address space must encode for that to route globally without a registrar; answering that produced the five-level hierarchy ending at App, with the lower levels existing only to deliver traffic toward the application level. IPv6 served throughout as the standing measuring stick: each candidate mechanism was required to answer a specific IP criticism — centralized human registration answered by automatic society/router registration, costly leases answered by free floating leases, gateway-only routers answered by coordinator-capable routers, spoofable and unprovable addresses answered by true 32-byte identities beneath temporary addresses, and single-frame packets answered by multi-frame self-describing frames under the [Networking](./networking.md) model. Interplanetary reach entered as a boundary condition on the address arithmetic — enough levels that no level ever runs out — rather than as a runtime concern.

## Explanation

### Goals
- Connect applications instead of things or OSs
- Connect things anywhere in the universe (different planets)
- Best use of addressing space allocation and assignment
- Decentralized and automatic process to register routers in any layer
- Free, automated, and floating to lease new GP addresses
- GP routers can be network coordinators alongside being a gateway

### Frame architecture

| bit     | Length(Byte-Octet)| Data                  |
| :---:   | :---:             | :---:                 |
| 0       | 1                 | FrameType             |
| 8       | 16                | Destination GP        |
| 136     | 16                | Source GP             |

#### Compared with the IPv6 packet
- **Versioning**: unlike IP, GP offers no versioning for the protocol — if a fundamentally different protocol is needed after official release, the right move is a new protocol with a new `FrameType` (or another existing solution such as Ethernet's [EtherType](https://en.wikipedia.org/wiki/Ethertype) in the [Ethernet frame](https://en.wikipedia.org/wiki/Ethernet_frame) header), not reinvented version fields.
- **Flow Label**: almost the same role as the Packet Number carried by sRPC's PacketSequenceNumber frame.
- **Payload Length**: a GP packet is not a chain of related frames and has no primary frame; each frame carries its own length where needed, as forced by the [Networking](./networking.md) model.
- **Next Header**: for the same reason there is nothing for a Next Header field to point at — every frame introduces itself with its own `FrameType`, per Networking's self-describing-frame decision.
- **Extended header**: standalone frames replace both the primary-frame/extension-header chain.
- **Hop Limit**: GP suggests the mechanism provided by the ChaparKhane role ([Chapar](./chapar.md)) as its network router/coordinator to reach this requirement.

### GP address

| bit    | Length(byte-Octet)| Data            |
| :---:  | :---:             | :---:           |
| 0      | 2                 | Planet ID       |
| 16     | 4                 | Society ID      |
| 48     | 4                 | Router ID       |
| 80     | 4                 | Thing ID        |
| 112    | 2                 | App ID          |

A GP address is 128 bits (16 bytes). Unlike IPv6, GP regards every bit of the address. The structure below is suggested for all levels and layers, but only Planet ID & Society ID must always respect it — each society network may set its own rules for the routing parts beneath. **All IDs are temporary IDs**: each Society, Router (thing), Thing, and App actually owns a unique 32-byte identifier underneath.

- **Planet ID**: each planet in the universe gets a 2-byte unique immutable identifier until it exists.
- **Society ID**: each society civilization — what a country is today — announces itself and receives a 4-byte unique immutable identifier until it exists.
- **Router ID**: each society delegates its range to some routers to do routing, improving performance and consistency of its own network. A Router always has a 4-byte unique mutable identifier until it exists (society scope). Usually each organization claiming a land (physical location), like a complex building, owns one Router ID.
- **Thing ID**: each `Thing` or device gets a unique mutable identifier from a router (router scope). The device's `Hypervisor OS` obtains this ID and routes applications to register against the hardware driver.
- **App ID**: each app gets a unique mutable identifier from the hypervisor. An app here means a unikernel OS image running one application over a dedicated OS kernel.

#### Compared with IPv6 addresses
IPv6 and GP addresses are interchangeable, but doing so needs some contract with IANA to register a /16 range for at least Earth.

- **Routing Prefix** (48 bits): very close to GP's `Planet ID + Society ID` — where IPv6 uses the first 48 bits as site prefix (global unicast address), GP routes packets to any global society.
- **SubNet ID** (16 bits): can map in some way to `Router ID`, though at 32-bit length.
- **Interface ID** (64 bits): has no real counterpart in GP. Where IPv6 has no strong rule for the last 64 bits and suggests [EUI-64](https://en.wikipedia.org/wiki/Organizationally_unique_identifier#64-bit_extended_unique_identifier_(EUI-64)), GP strongly advises a better rule for its final 48 bits.

Some other IPv6 address-renumbering suggestions, with their GP counterparts:
- **Type** (3 bits)
- **Registry ID** (5 bits) — can map in some way to `Planet ID`
- **Provider ID** (16 bits) — an Internet access provider maps in some way to `Society ID`
- **Subscriber ID** (24 bits) — no counterpart in GP
- **SubNet ID** (32 bits) — can map in some way to `Router ID`
- **Interface ID** (48 bits) — no counterpart in GP

### Society registration
Each society in Giti must pick a primary name that is a combination of at least three Unicode characters and use the hash (SHA3-256) of it as the UUID of the society. The picked name also serves as a TLD, letting the society register any domain under its name — e.g. society name "persia", and "athenafarm.persia" is a domain belonging to that society.

Each society registers one unique 32-bit unsigned integer by a specific algorithm for routing in its database, and tells all physically adjacent connected societies about its existence.

### Standard services
Each society must implement the standard services below, such that all first users (`== 0`) registered under the primary society name get responses to these services from any router in the society.

*This list arrived empty in the legacy text — completing it is owed; see [Unresolved questions](#unresolved-questions).*

These services are not auxiliary conveniences: they carry the network's entire accountability model — attack reporting, reputation, blocking coordination, and identity attestation are all designed to ride on them, and their numbers are assigned by collective agreement. Writing them well is among the highest-priority open work this document owes; until they exist, the enforcement structures above remain scaffolding.

### Routing architecture
A scoping note before the mechanisms: this layer's whole obligation is addressing and routability — that a packet *can* be addressed to any society and routed toward it. Carrying packets between networks, up to and across planetary distances, is the job of layers 1 and 2 and of the topology built from them; GP claims the map, not the vehicle.

#### Routers
We strongly suggest using the ChaparKhane role ([Chapar](./chapar.md)) for the router mechanism, with [Chapar](./chapar.md) as the link-layer protocol carrying GP packets instead of Ethernet frames.

#### Mobile GP
[Mobile GP](https://en.wikipedia.org/wiki/Mobile_IP) allows location-independent routing of GP packets across the network. This specification sets no rules for mobility implementation itself: mobility is achieved by having a proper topology in your society network and data link layer.

#### Quality of Service
QoS must be handled in routers, not protocol packets — consistent with the congestion treatment in [Networking — Hardware](./networking.md#hardware). How routers actually schedule, queue, and prioritize is a ChaparKhane implementation concern — a commercial component (see [Enterprise](../README.md#enterprise)) — deliberately left unspecified here so that neither creativity nor the product is constrained by premature rules.

#### Local network
When no GP router exists in a network, GP cannot be used properly. Nodes can still set the first 10 bytes (Planet ID, Society ID, Router ID) of the GP address to arbitrary data and send packets to other nodes, but peers cannot prove their identities strongly to each other.

#### Multicast & anycast & broadcast
Because this spec must stay decentralized — and because these requirements belong at the application layer to protect user privacy — GP offers no way to multicast, anycast, or broadcast a packet in Giti networks.

### Place in the stack
Giti defines four distinct protocol layers in its network, mapped onto OSI for orientation:

| Layer | OSI mapping | Protocol |
| :---- | :---------- | :------- |
| Physical | Layer 1 | Any suitable medium spec, e.g. Ethernet (its layer-one part only) |
| Link | Layer 2 | [Chapar](./chapar.md) |
| Network | Layer 3 | Giti (GP) — this document |
| Application | Layers 4–7 | [sRPC](./sRPC.md) |

Per Networking's [Layer presence](./networking.md#layer-presence) principle this mapping describes capability, not obligation — a given link realizes whichever of these layers justify themselves on it. Above the stack sit the rest of the ecosystem: the router/network-coordinator role is the ChaparKhane ([Chapar](./chapar.md)), the operating system is [PersiaOS](./persia_os.md), and applications run as unikernel images produced by the Achaemenid auto-generation mechanism, which also removes most upper-layer development overhead — you do not need old IPv4/IPv6-era ideas like UDP or TCP here (ChaparKhane and Achaemenid are commercial offerings of Geniuses Group — see [Enterprise](../README.md#enterprise)). The software routers of this ecosystem differ in internal service call, security, pipelining, and multiplexing, and are based on code-generation development while remaining usable through plain package APIs.

### Attack reporting and society enforcement
Routers, OSs, and apps can request action from each other — report attackers and block them. If routers do not respect a reported node or router, whole societies can block the offending society. AI must be added to router applications to detect infected or misbehaving routers that don't respect the rules.

What this topic deliberately does *not* fix is the binding/authentication method behind a report: GP intentionally specifies no definitive identity-attestation scheme here, so that no single approach hardens into law and crowds out better ones. What the protocol does provide is the structure accountability needs — every Router ID range belongs to a specific, identifiable organization, and the mandatory society/router services below exist precisely to exercise that accountability. This is where GP structurally parts ways with IPv4/IPv6: there, a report's origin dissolves behind VPNs and shared carriers with no one answerable; here, a report always terminates at an accountable range owner. Spoofing inside a range remains possible — but the range owner answers for it, which shifts enforcement from per-packet forensics (impossible at Internet scale) to organizational responsibility (enforceable).

### Transition from the Internet
Every PersiaOS transition application with Internet access must listen on UDP port 80 for incoming packets carrying GP packets, and route the whole Internet packet to the registered app's GP address if it exists and has requested to listen on the Internet network.

### Implementation and status
GP is simple enough to encode and decode easily in any programming language. Implementations exist or are in progress in C, Go ([libgo/GP](https://github.com/GeniusesGroup/libgo/blob/master/GP)), JavaScript, and more. The current implementation is considered alpha; compatibility with future versions is neither guaranteed nor expected. GP will ship inside [PersiaOS](./persia_os.md) but can be used by any other device and OS due to its very simple spec.

## Results
Insufficient deployment experience has been recorded under this consolidated structure to report real, observed outcomes. This section will be filled in once there is such experience to draw on.

## Discussion

### Prior art
Direct ancestors and peers:
- [Application-Layer Traffic Optimization (ALTO) Protocol](https://www.rfc-editor.org/rfc/rfc7285.html)
- [QUIC](https://en.wikipedia.org/wiki/QUIC) — [RFC 9000](https://datatracker.ietf.org/doc/html/rfc9000)
- [HTTP2](https://tools.ietf.org/html/rfc7540)
- [IPv6](https://en.wikipedia.org/wiki/IPv6)
- [Blockchain models for universal connectivity](https://www.semanticscholar.org/paper/Blockchain-models-for-universal-connectivity-Navarro-Castro/788b7a634b369d98e72ed37c5fdf71f7fd62ef0b) — [PDF](https://pdfs.semanticscholar.org/788b/7a634b369d98e72ed37c5fdf71f7fd62ef0b.pdf)
- [Matrix, an open network for secure, decentralized communication](https://matrix.org/)
- [Homa](https://github.com/PlatformLab/HomaModule/)
- [RFC 1106](https://datatracker.ietf.org/doc/html/rfc1106)

Decentralized-network projects consulted:
- https://code.google.com/p/phantom/
- https://github.com/cjdelisle/cjdns
- https://libremesh.org/
- https://yggdrasil-network.github.io
- https://github.com/redecentralize/alternative-internet
- https://github.com/LibreWeb/LibreWeb
- https://github.com/openspace42/LibreFibre
- https://github.com/loki-project
- https://sudoroom.org/wiki/Mesh
- https://www.opencompute.org/
- https://github.com/gdamdam/awesome-decentralized-web
- https://book.systemsapproach.org

Articles and ideas drawn on:
- https://apenwarr.ca/log/20170810
- https://apenwarr.ca/log/20200708
- https://github.com/alecthomas/go_serialization_benchmarks
- https://tools.ietf.org/html/rfc4506
- https://github.com/google/flatbuffers
- https://capnproto.org/
- https://pdfs.semanticscholar.org/3488/cb985ce0fb102608d5d9aeca7b9a7319c5e6.pdf

Reference topology diagram: [Overall suggested network topology at a glance](https://www.draw.io/?lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1#R7V1tc6M2F%2F01mWk%2FJIPEi%2BBj4mx2t087u83uPtt%2BymBMbBrbuIDjJL%2B%2BEiAMkjCKLQxO2M40toxlkI7OPbq6ujrTR4unj5G7mv0RTvz5GdQmT2f69RmEFtQA%2FkNKnrMSgHQ9K5lGwSQv2xZ8C178vFDLS9fBxI8rFyZhOE%2BCVbXQC5dL30sqZW4UhZvqZffhvPqrK3fqcwXfPHfOl%2F4MJsksL7VMY%2FvBJz%2BYzuhPA8vJPhm73sM0CtfL%2FAfPoH6f%2Fss%2BXri0svxJ45k7CTelIv3DmT6KwjDJXi2eRv6ctC5tt%2Bx7NzWfFjce%2BctE5gtT%2B%2BZ2lDz7%2FwdP07vvq7V5Dm7PgZF316M7X%2Fv0QdLbTZ5pG%2BF6cHfgN1f4GVak0JuHa1zt1WYWJP63leuRwg2GCC6bJYs5fgfwS%2F4W87t%2B9KPEfyoV5bf80Q8XfhI940vyT891XUPZl3KIWbqVvd9s%2Bws6KG%2FlWbmvLJRf6uYomRb1bxsKv8jbStxuhtXcQqVnDtfJPFj6owKvGi68D%2BbzUTgPo%2FRy3QcT00ekPZMofPBLnzgW0l0LfzKN3EmAm%2B06iHA1QbjEny%2FDiDxw%2Fi0KV1jql8XTlIzTi6WfbMLoIb6gHaWiJ3DLOxdmpS8AsnVaVOoOQ9gbjnZ4Z5iQ64xvmyDxZlyX3IfLpNSwmmZZoxFuCfLAAR7%2Fl%2FNgSho1CVel0t%2FdsT%2F%2FGsZB3uTjMEnCBb5gznzg4Yb0cd1Xbl5PUfBKLIzSfyIsWLYNrvQSFuhny3Dpq4NInLWfIozghq4ixNRFCAGaACG6CoBIjNYBGpLQmLurrA2UQMOEVSIHCBqy0DBNBdBAAzSUQWPlqYIFQCZnVaisbIIFUsEY9gALZbAgtYR3SbhJ714FPoBlVy0KMkQGhRJERXFoKuDhDPBQpzXchEwmEv9uEsSqNAcwbaM6Q7AQhw9HpEhV4MPSBnwow8c69qO7e3%2BRTs8VqQ7AqA7b5I2L0Ro6AIeOn7iJ5n4c49JLz8tefA0D%2FIgDbPaEzSZv0rvZeqwKN4ZpsLLEQDyvCGWJrUCtWqaAV6x5Qpo%2FJGDRYupMs%2F5dEyfSFdi%2BxK%2Bm%2Bd%2F0K%2BMKsuhVpKLzrJpLfAE0Vk98FTfBGIMCar8HywdaHb75MfsTuCy7MVrMoBm3fFLFVhUuOSTK2MqLOHyyA2ARTCYpY4j8UamLzp%2Fk0G3F4NjUx1cCBnUTlnFhqWCUYRajjjgW4ThQZ2qgozPzGGALpCr1kFeQoYAxEO8bG5BxiBKJldkS3WZtiUiFtKZRkYSTf0DGazSqSoWqQ05pHFWjItEMN7Ppk%2BBRKByILT%2FPe5Ioh7wza%2BUHVSxNCsQUKpAPT97MXU79rVDWfvnr66%2B1wiOXPJHML1q26BdLVadNIC1pSO35Iqdl0%2Ff5FwQrdnssh2l07FKsANMU%2BUMMgUNExQqMI%2BEPObUh7YWLxR2%2BzYc7f0KWi8s9%2Bo%2BfJM95l7rrJCTPhH8gnIZLTH8hYUO256GB3%2BO7ip7%2FIg984QD6%2Fu%2F0vUnePgVJ9qlm5W9LH5Jrv%2FpRgHuHcGTaaOQStqwWUXG4jjy6xE3X2hM3mvrFOnbebdkT70Be02SnKMRzMDcJHqsL6yKo5b9Bx3Ihq6EFLzQd2fQ%2FmwE6KBx%2FtNbsMbez55vauk0EqrVp1O9L68pah6srHQ9Fc0gNEaCJ7O3rmBDs5KV45S4Ldrz%2B%2BAF%2FYRQuVuskWE5L3FW%2BrEyL9ZV9XhKczAjVxu6C%2FPnrK6Hbmkp%2FfCafkjsmN31jGb%2BKKq3%2F6Zp7rPxETO7iPoxShLnz8yRI78tdrWJ8jbsgcmQ5jlfN1e5%2B9FtMVUTzwdFB1fweuhN8e1jnuEuP2MTDqsOUM8ODG2utlN4Orc3z8Gw4Q8lhNX0Ov6dVaBcXFw0VNTkGOOVJ%2Fg3KU7S44j0wlsZqQ2OAIn5juyDHOzgKs1I2BkW00yESo6j5TWmMPBKHQXseMqbIMWWYbISOYUNRgI5tCfpOxWoqttLKZhOZwtGkvJQNcwSh6dlb2qcCT%2F2w0yFies8yBLFuNDSx3HcGVNF1Eg6kYdgJZvAOqDr%2BTCCYvrc45OrlZptDTihGG6fq0sKwZ6MTItqBdGwi0bwbGqit0Vm%2FIJS1qaCbvQzxpA%2Bj6fgXjXRwqtpKr37d3evlzzb5M5FPU0lQu9wU7QuIgW4k1hl0hm54cdYm26iPh%2B6%2B29p1ABU%2BnczFo9lnNT6eWnhU%2FTk5E%2FTdn2Nr3LKHYR7gwrGqLhyrRQ8O5FdZb758FLlZtlSX%2Bk7cyT8uMabUcxLekz5ZEpcAWTh4pSUzeSoppsdVCyeY3irhGluvhs8gxxEtaUIB3dh2PWSk2Qby7uZRyrESXbF8pr2wCfCd0pJJECfEN0NGUHjavQOYkGpdEIjQXt%2FobetOYDXrTglXqrCWD66XQmK1wv8nNEouHAfkb5QLlvUy%2BBc%2F2OucjJx7tMk3trfOBdYO%2FHF4Uy%2BITcStWzrC2FxdtHRJdfJBCDR4Z8MNVgIbl1zW5GYcFrjFYuietmAFbY4qzirQUKzrCJyLUODjoGWHIKZmE6RETNWp9WIrkrZYtITVRUvS48IFSlJ2%2FVR%2B8%2Fw6qStcujT7JnWRblwYVfcAsuD%2BUhca1gVkuFUzcZm2%2Fae3JX5%2FrL78eXMb3YbB03Vo%2Bt7j5mWJ1beET56C8X7uP12SzdnpPGeSv7z25m4cB16KYzdK%2BOKynasOp4nr2%2FeecDh5tj%2FeObV%2BDUxMAUpMRSDZbnrPu9Rho3ekAQINhkQRO7VvHQ4SlKkQDlvmMcvEs5NhRHykEFZlnqJBub2BmmEwwROW7eyLNd1iDLbJxhG1DjaJLXqdcs8WnrZ%2BED6l0Eb3OPcGbQiyaEN7o82AnaNNIsKtfWq70FBf2M3sG7tZiMUb2BtvkEtYYB8Zb5ZEdPagrHZ6mpHOKit9TzwATlkZR4aDLVrna%2FJlDCFTHYdM6YDd%2B3PUkKkaKO2TDGWAUsdQKqbavYISP98bEi%2F1KPESgA5gvfGmMPavtdRLNcDp%2B9yt%2F%2BqGm4BbziG%2BRYfZCWEBrrbWNc5xp1hvERTQcFSCwmDki6UfHRR0nj%2BAYm9QcNLhMFCwU2MLHh8UonDyQcL2W8I6fO4USxfkTjmyhnXggKWTwxJy2E0R%2FcDSPikVBix1iyVL7ycvGRyWhrl1j%2BbWCFVDO4AJREGwR55YOxJ%2B4kEu75LLtsHTAXT21suIT2RrGlx1rQtmCZ%2FvAIvdwVy6UlhwuzqBaR0fFseN13mDsBCJhwNgYdlcdabZIixqIl957%2By73OfC%2BViRMKtSa3sp5hoYjy%2BXPzffRy641a5WGwRrDmdRusECaLt2WEgnqxFXc%2B2TX4%2Fw3bz4k4ZsXexGiNN5yh9LTCpR7P8SkHtYzV0sQt3ouSk92ek%2B8Gfy00uyY0ZB%2FjW0c2v5IdtjkNHGFJIkaagQhWVzLAEgEmwC16n76RCeWALg%2FvYy%2FzT7%2BCPQ1uD7w%2B3jv%2BeA%2Flz5zCZsNemDb2P7P2xLmby4wvh%2FwT4BYeAaffd36RP5qLUaNZEW3wRzQdfu3ItSjlxzfr6c3z%2FZn5PR%2Bc%2FF5f9A9NufwZZWy5sKahrWkNQg0uJCtqNnX65c6%2FmDZj5qX6dfZh%2Bup%2BtP%2BM4lPJhH6HnJHhO2ncI%2Bq2mjY3XR7hsdnDn9dObghuaEtyiDQmvenBrU8j7ANzeyd41XqZGtd0q%2BFCRdWdlyePjrrWxdOooiN%2Bm2qvTdc%2Fndnia7bZiIjXaWofYAmKRfxU%2FnPpcuWJE5eFyqmYsk1xBDKzpgTuTkg42ZuGX2K%2FhFdh%2F7zvp3t%2BVgo9qyUZxBEqB%2Bh40CfErwPtgoCdfyG7VR8urT7NZGOd3aKEeVjXJO0kZJwyTbUnV0GwVsmjyyMDhGk41idy2zX2nLRg3zqF7bKODwq6d9sFGdusLKjrCtYN%2BHAMv0V1LsLRDgxI1n6bMrZ0NBmrqWFPuBRhN0iZl3P7ETwGSXa%2B34RhMBdmIHG4zm9jzamq%2B0ZTT5mKDBaPbJaCKrW6Mp5l%2BaUOJNrx9JUZS4feQXjKgpOf6CkfB%2BIN0H31XPakxOi0Mk0YXD5tFtUxbts9x4KHoofatDz56uTEBP%2BaIHnKKmWSIyzF3fONje7W7akr1Lo5EGo9enFTfIrbjZNjpmAHUNeE7KnSmYpu3HRoY0G%2Bm9smVSWTrfdX8ptx4H9he%2FpD2Qc%2B%2FImT1PtBfUTHdEnfwyRlWxnoZclXfb9c1A8N6PgXD6RjjAZhKs9YJwUMfz5MNcwMfnCJvniN3hkL3hCFE6IvWnaEmflCUbiy8%2Bgi07fzc7ubZ5v8HOk7YGNpTdrJ61tqpoVD5VRhHl3R0d0pOWBofwbjdvs0ai28r6soOga1e%2Fo9IhXCxx9nO981DsHBxLtq%2F316x6fx2zyftrs%2Fl3zWN4f2lLDqud%2FZT65Khixrg5CHQv9k0o0IAsKW73vectXHHoHRj7U9u6fdnsDgEzom3oXJQOn9FgtUr5pHKObr6mYnUb4GuwwK8g%2FSAnwqUnA6ZHbWsVH4IWkDnCfRDF5Knm7nMqvPEABaRfA7ILPqaXevlQx9fhge9G82dase96szCZ1e%2BTj3ws%2Fd1xWkoqzkkbX2JenZnXIqphuWwRTCap9U7Z6sr1HqapHRcdS1tLaHVUWFSO5xQeyRKgX%2Bvbd7c5IMmdEzGQTWPSt3guNXdXcbB9tPRRC3balnzyy7WM43COdfdl5H3bVhYs3Kl%2FGa8yPk3HZRgFL5jsXTo6s4cPo4kfMYzJj8EGtuAjP%2FIOzvvpLE8RVU%2BI5KAsuiJ%2F4AiFTByvwWaOCO%2FvY7%2BdMWN17J3t%2B%2ByAan4JhWd3NTvYfeeDouqpohJsXtXMzgWVJZGK7N0LKkvjHD2mqUZTIcSlmGqou21ZZfGxFaysqvguR%2FDsUguXuTTCf9arVZrfJBbTzyCT%2BiaTCg7ol0xiDopiKmhTJEmkuH%2F3nKjbnDWzFM0zbY3LxthQd9uciHhxxXJiMcscqPCUqZAO%2FYEKM%2BBL5PB%2F91TIpBVzbEsRDzKegoaKWydB3vc6kOBbJEFUN7t9ryRo85x3Ok6z0w5ppGn8JBL%2B9SyGmt754JDrq0OOj9%2FRqaOtO4ccPV%2FtNOOnj88PgpBnuuzTFyZwurUfrxDbr0lsgU7DfgjwYcnOII5lKYat%2F%2F22FAa%2FdGNQ%2FdmhpZA4x%2Bq9z82hzhyOqZPUR0qCYdgTFhtqbnt2bvNyc5idv8XZeTHsh9l51h7DCnYzDSKLM2BQ0Qq2Y3BnLjXU3ToVNq9gD1T4JqhwWLiutodMmoV3ToWAOS0KmIatarkGvarm1mmQ3y850OCbpEE67AcazPxtfLTGQIPsiQcmQ4NI1S4RBNCram6bBh0%2BhIGLZ0yPPdSu%2FcfA8wc2PG02LEb%2FwIZZHslOz75Rl1b7FFev6bmBsnm0JQzEsdasoMCGDsk2hiWYbpJtAIv6t3uUasPpOiFDiVvfW1yQI52Z1%2BksLqgmjUfHWzDV5nUuI%2BdU0njIY6ezYwtsJvdC01E%2FZNfYrm%2B0lMbDGU766XXkAkBOdZrfiyQeTsdnXr9ruymfIhT2bEYyREn1nGt0xsfR%2FfZ2qJ10NrwTpxqHp5ofqy9%2F3txGt2HwdB2avve4eVluFzC6PjwDGIhdHNQbz1ik89Car7SjvCD1og%2FAbhPYu04AlQE2TYbeObAhowOL46trgY0gG9SjGNc1bStK8nt8oHcxKxXQZUsn0B4oxPj0CIMQ65MQM2xmsPfgcFeTD00aQNOn4w11Np69TdDgt1FIVmi2toM82x%2FhxCdX%2FAc%3D)

### Unresolved questions
1. The standard-services roster for first users (`== 0`) arrived empty in the legacy text; the services a society's routers must answer remain undefined.
2. Ownership proof: the address rules state every Society/Router/Thing/App owns a true 32-byte identifier beneath its temporary 128-bit address — but nothing specifies how ownership is *proven*, i.e., how a temp address binds to its true identity for authentication. This is deliberately unsettled here: fixing one binding scheme now would foreclose better ones. Two structural facts keep the gap smaller than IPv6's, where no path exists at all — every Router range has an identifiable organization behind it (accountability survives spoofed sources), and the mandatory services above are designed to carry attestation once defined. Still open, and pressing precisely because attack reporting consumes it. (Connects to the certificate/provisioning track noted in [Chapar](./chapar.md)'s Discovery discussion.)
3. Interchangeability with IPv6 depends on a contract with IANA to register a /16 range for Earth; no process or owner for pursuing that is recorded.
4. The "specific algorithm" by which a society registers its unique 32-bit routing integer is unspecified.
5. The Achaemenid document does not exist yet; legacy files linked it as if it did. Either author it or choose its eventual home.

### Future possibilities
- A mobility/topology guidance document: the routing architecture deliberately delegates mobility to topology and link-layer choices; worked patterns (roaming between APs, society hand-off) deserve their own pass.
- The attack-reporting/society-enforcement sketch (including AI-based misbehaving-router detection) needs a real design before implementation claims.
- Society delegation rules: how a society splits its range among routers, renumbers, and handles router churn.
- **Society-level blocking via de-peering and signed reputation propagation**: the primitive is inter-society route withdrawal — a society blocks another by withdrawing route advertisements for its prefixes (BGP-style de-peering, simplified by the small, deliberately-peered society graph). Coordination rides the mandatory sRPC services: a signed incident-report service carries evidence (Chapar headers stamp physical paths, so ingress routers are provable); reports propagate peer-to-peer, each society sets its threshold for automatic route withdrawal. VPN bypass fails structurally — traffic exits via a router whose range belongs to an identifiable organization; victims block at the society boundary by Society/Router prefix, and the range owner must police its customers or face de-peering. Escalation is graduated (warn → border rate-limit → partial withdrawal → full de-peer) with re-entry via signed remediation attestation. This is recorded as an option, not a fixed method, to leave room for better designs.

The mechanism works in two tiers:
1. **Intra-society consensus first**: the routers of a society agree among themselves that another society is not responding to abuse reports or is harboring sustained abuse. This mirrors the user's description — "all routers of one society agree" — and is the first gate.
2. **Inter-society propagation**: the consensus result propagates as signed route withdrawals through the society graph. Each receiving society verifies the signatures and applies its own threshold policy (immediate full withdrawal, partial withdrawal of only the offending ranges, or border rate-limiting). Re-entry requires a signed remediation attestation.

Why VPN bypass fails structurally: an attacker may spoof source addresses inside their own society, but the traffic must eventually leave that society through a router whose range belongs to an identifiable organization. The victim society blocks at the Society/Router prefix boundary — no per-user identification needed. Accountability shifts from per-packet forensics (impossible at Internet scale) to organizational responsibility: the range owner must police its customers or face de-peering. This is exactly how email abuse *should* have worked, and why Internet BGP hijacking still plagues the Internet today.

Graduated escalation:
- **Warn**: signed notice to the offending society's routers with evidence.
- **Border rate-limit**: rate-limiting of the offending society's prefixes at the border.
- **Partial withdrawal**: withdrawal of only those prefixes implicated in the attacks.
- **Full de-peer**: complete route withdrawal; traffic from the offending society becomes unreachable.
- **Re-entry**: signed remediation attestation from the offending society's routers, propagated peer-to-peer.

This is recorded as an option, not a fixed method, to leave room for better designs.
