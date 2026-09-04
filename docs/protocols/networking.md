---
Title: "Networking"
Status: Draft
Start Date: 2015-01-01
ID: 394460
---

# Networking

## Abstract
Networking is the making of connections between computing components — wherever two computing entities exchange data, a network exists and its principles govern, whether that is two machines over a cable or a GPU negotiating traffic with a CPU across PCIe. In this project every network exchange is modeled as a **packet**: an ordered sequence of **frames**, each frame belonging to a registered frame type, read by devices along the path to perform their logic — switching, routing, multiplexing. This document is the single specification of that model: the packet structure, the frame concept and its type registry, the special signature and padding frames, the principle that **no layer of the network model is mandatory** (each layer's presence on a link is justified by that link's own capacity and role), and the hardware considerations shared by protocols built on this model. Protocol-specific frame formats live in each protocol's own document and are cross-referenced from the registry here.

## Introduction

### Motivation
This subject predates the project's current documentation method: what is consolidated here was previously scattered across three sibling files (`networking.md`, `networking-frames.md`, `networking-hardware.md`), carrying stale cross-links and no recorded identity. Worse, the old text silently inherited an ecosystem assumption — that every hop of a network necessarily carries a layer-2 framing — which surfaced as a real design confusion during critical review of [Chapar](./chapar.md): part of what had been written into Chapar (when a link carries a data-link header at all) turned out to be a general networking principle, not a Chapar rule. Implementers need one authoritative place defining the packet model, owning the frame-type registry, and stating the layering principle explicitly, so that every protocol document — Chapar, GP, sRPC, those still unwritten — can reference it instead of restating or privately assuming it.

### Methodology
The consolidation merged the three legacy files without summarization, repaired their dead links, and extracted the general from the specific: during review of Chapar's media-existence discussion, the owner identified that the underlying idea — whether layer 2 exists on a link is a capacity-and-role decision — is not Chapar's rule at all but an instance of a wider principle, which is stated here in its general form: no layer is obligatory; each layer has its own identity. The principle was checked against concrete cases (a two-device wireless association that needs no data-link framing, a phone attaching to a cell tower without announcing itself to tower-mates, and a multi-access switched segment that genuinely earns a data-link layer) before being recorded here.

## Explanation

### Scope
Networking means making connections between computing components. It is needed almost everywhere in computing, and "components" is meant broadly: a GPU exchanging traffic with a CPU over PCI Express is as much a network as two complete computers connecting over a cable — traffic arbitration, framing, and delivery concerns arise there identically, and the principles in this document apply to them unchanged. Nothing in this document assumes a particular physical medium or a particular set of layers present on a given link; see [Layer presence](#layer-presence).

### Packets
A packet carries many frames in a desired order; devices on the network read the frames to perform their logic (switching, routing, multiplexing, ...). Strongly suggest respecting the OSI network model and ordering frames in any packet in OSI-layers order. On encryption: applying it after layer 3 is the low-cost default suggestion; encrypting deeper — even right after layer 1 — remains available to whoever needs it, taken knowingly, since every packet then owes decryption at both ends of the encrypted span, which is expensive.

- A packet has at least two frames — always including the special signature frame, which appears at the end (see [Special signature frame](#special-signature-frame)) — and usually more, in [sRPC format](./sRPC.md).
- Packet size can be up to 8192 bytes (8 KB). The bound comes from this model itself — a 16-bit `Length` ceiling on what a frame may declare — not from any external law. The familiar arithmetic (`1.5/8*1024/1000*40 = 7.68 KB`, a 1.5 Mbps video call in 40 ms frames) shows only that the bound is comfortably sufficient for such workloads; it is illustration, not foundation. The deliberate direction is toward the ceiling, not away from it: protocols built on this model are expected to operate at maximum capacity, exactly as existing stacks push toward jumbo frames.

A principle this model states once and owns everywhere: **fragmentation does not exist in this architecture.** No layer defines any mechanism for splitting a packet to fit a smaller unit, or for reassembling one afterward — delivering its own unit intact is each layer's whole obligation. Links are therefore expected to carry whole packets; a medium whose units cannot hold the traffic simply does not host it ([Layer presence](#layer-presence) decides that per link). Anything resembling segmentation can only be simulated above the model, through sRPC-level exchange conventions — workable, but an application-side workaround bending the model rather than a capability of it. The goal remains a genuine 8 KB MTU end to end.

### Frames
Frames indicate in each protocol's own RFC — e.g. [GP](./giti.md), [sRPC Protocol](./sRPC.md), [Chapar](./chapar.md). Each packet can carry many frames as long as it respects the network MTU. All frames have a fixed first field named `FrameType`, one byte wide. FrameType is a small, centrally-registered set of wire framings maintained in one table here — and it appears in every frame of every packet, so its width is paid continuously by all traffic. One byte covers the real population with room for an experimental range and a signed-extension escape hatch.

```go
type Frame interface {
    FrameType() byte
    ExtendFrameType() [8]byte
    FrameBody() []byte

    IsFrameTypeExtend() bool
}
```

Some frames work without needing a `Length` field of their own; therefore all frame handlers must provide a `NextFrame() []byte` method, letting a reader advance through the packet without relying on per-frame lengths.

#### Two ways to identify a packet's parts
Older stacks delimit a packet's sections by having each header introduce the next one: an Ethernet header's EtherType names what follows it, an IPv4 header's protocol field names the header after that — a reader parses outside-in, each layer interpreting the previous layer's pointer. The frame approach, which we reviewed and adopted, inverts this: every frame introduces *itself*. Modern protocols such as QUIC lean on this shape heavily, and it is mandatory here — the first byte of every frame is its FrameType declaration (extending to eight bytes through the signed extension), so a reader always knows what it is looking at before reading anything else, and frames can be parsed, skipped, or dispatched uniformly. The `NextFrame()` handler requirement completes the model: uniform advancement even for frames carrying no Length of their own.

### Frame type registry
Frame type numbers are registered here, in this table, and must be respected by everyone. Rules:

- Numbers between 100 and 127 are reserved for experimental protocols; any device that does not want to process them SHOULD ignore them.
- The sign bit extends the one-byte frame number to an eight-byte signed value (63-bit number range) supporting more frame types; the extension is carried by `ExtendFrameType`/`IsFrameTypeExtend` above.
- Until Memar's own protocols settle further, the specific numbers in the table carry presentational weight only: they fix relative order and let documents reference one another consistently; no formal allocation authority or process exists yet for the free range between them.

|            Num.            |      Frame name      |                   Doc                    |
| :------------------------: | :------------------: | :--------------------------------------: |
|             0              |        Unset         |                 --------                 |
|             1              |         Asb          |  [Protocol](./networking-osi_1-Asb.md)   |
|             2              |        Parvaz        | [Protocol](./networking-osi_1-Parvaz.md) |
|             3              |        Chapar        |         [Protocol](./chapar.md)          |
|             4              |       GP-Thing       |          [Protocol](./giti.md)           |
|             5              |        GP-App        |          [Protocol](./giti.md)           |
|             6              | PacketSequenceNumber |          [Protocol](./sRPC.md)           |
|             10             |       Padding        |         [Frame](#padding-frame)          |
|             11             |       Security       |    [Frame](#special-signature-frame)     |
|            ...             |                      |                                          |
|         100 ~ 127          |                      |          experimental protocols          |
| 128  ~ 9223372036854775807 |    Extended Frame    |    Just exist in signed frame numbers    |

### Frames defined here
Named frames live under this single heading; each new frame this document specifies becomes its own `####` entry beneath it.

#### Special signature frame
A special frame that always appears at the end of a packet; because it sits at the end, its fields are read in reverse order. Reaching it requires no forward walk through the packet: layer 1 delivers the packet as a delimited unit, so the packet's end edge is known, and the reader parses backward from that edge — taking the trailing `SignatureScheme` and `Length` fields first, then using `Length` to bound the rest of the frame. Depending on the crypto mode it authenticates the transmitted data and checks packet health at network hops — though usually only the first router and the receiver check the packet signature.

```go
type PacketSignature struct {
    FrameType       byte
    Signature       []byte
    SignatureScheme uint16 // SignatureScheme identifies a signature algorithm supported by TLS. See RFC 8446, Section 4.2.3.
    Length          uint16 // including the header fields
}
```

#### Padding frame
When a block cipher is used, random padding data is added so the packet keeps a fixed size, placed at random locations within the frame.

```go
type Padding struct {
    Length   uint16
    Padding  []byte
}
```

### Compatibility with existing protocols
A way to process all older protocols — e.g. Ethernet, ATM, IPv4, IPv6 — inside this packet model.

#### Internet protocol suite
Suggest the Internet protocol suite use `FrameType == 100` (experimental range) plus a sub-frame type indicating the concrete protocol: Ethernet, IP, TCP, UDP, ...

- **Ethernet protocol**: it CAN support and carry many protocols through its `EtherType`, a 2-octet number; further values can be found on the [EtherType wikipedia page](https://en.wikipedia.org/wiki/EtherType).

|  Num.  | Frame name |                                              Doc                                               |
| :----: | :--------: | :--------------------------------------------------------------------------------------------: |
| 0x0806 |    ARP     | [ARP - Address Resolution Protocol](https://en.wikipedia.org/wiki/Address_Resolution_Protocol) |
| 0x8100 |   VLANs    |                       [VLANs](https://en.wikipedia.org/wiki/IEEE_802.1Q)                       |
| 0x0800 |    IPV4    |               [IPv4 - Internet Protocol v4](https://en.wikipedia.org/wiki/IPv4)                |
| 0x86DD |    IPV6    |               [IPv6 - Internet Protocol v6](https://en.wikipedia.org/wiki/IPv6)                |

- **NDP**: the [Neighbor Discovery Protocol](https://en.wikipedia.org/wiki/Neighbor_Discovery_Protocol) is based on the IPv6 protocol.
- **NTP**: the [Network Time Protocol](https://en.wikipedia.org/wiki/Network_Time_Protocol) is based on the UDP protocol.

### Layer presence
No layer of the network model is mandatory. Every layer has its own identity — a job it does and a reason to exist on a particular link — and whether a layer is present on any given hop is decided by that hop's capacity and role, never assumed by default. A stack diagram describes what layers *can* do together, not what must always be stacked on top of each other.

A note on the classic classification vocabulary: the ecosystem's "connection-oriented / connectionless" distinction carries established meanings elsewhere ([connection-oriented](https://en.wikipedia.org/wiki/Connection-oriented_communication), [connectionless](https://en.wikipedia.org/wiki/Connectionless_communication)) that are easy to invoke carelessly. This document does not classify its protocols by that pair; comparisons between Memar protocols and others (e.g. [Chapar](./chapar.md) vs. Ethernet) are stated in terms of directly verifiable mechanics — where state lives, how forwarding knowledge is distributed — rather than by re-opening that classification.

Three concrete shapes make the principle tangible:

- **A plain two-device association** (a wireless pairing, a direct cable) carries layer 1 plus whatever upper-layer framing the payload uses — in Memar, sRPC frames speaking directly for layer 3. Registration and introduction happen directly with the coordinator above; the packets may contain no data-link header at all, going straight from the medium upward.
- **A phone attaching to a cell tower** does not introduce itself to every other phone on that tower. Attachment — a layer-1 identity — creates connectivity; upper-layer messaging registers membership with whoever coordinates the cell; a shared broadcast data-link segment is simply not part of that topology.
- **A multi-access switched segment** — many peers, no designated single peer — is exactly where a data-link switching layer earns its existence, because forwarding knowledge must live somewhere and the alternatives are flooding or state in every node.
- **A low-capacity wireless association** (a sensor radio whose media frames sit far below the packet model's bound): only layer 1 plus a compact sRPC exchange appear — a sensor announcing a few bytes of telemetry is a service call on layer 1, not a routed conversation, and no bulk or two-way transfer is expected on such a link. Real routing needs header room media this small do not have, so no switching or routing layer is expected on them at all; the receiving access point decides above the link what the announced data is worth.

The corollary for protocol documents: a protocol declares the conditions under which it applies instead of presuming it rides beneath every packet, and upper layers must be able to traverse a link that realizes fewer layers than the textbook stack draws. See [Chapar](./chapar.md)'s Frame architecture topic for this principle applied to a real protocol.

### Hardware
Chapar functions can be added to any device through a switching fabric unit (SFU) attached by any interface, e.g. PCIe. An SFU provides 1 to 256 wired ports, or 2^16 (65,536) wireless ports.

#### Wireless access point
Chapar can help layer-1 protocols make connections between an AP and its clients. If a wireless AP device handles two Chapar hops of the frame instead of the regular one hop per switching hop, it can serve 2^16 (65,536) devices.

A single low-cost, single-AP wireless device contributes exactly one hop to the frame, regardless of how many client devices it ultimately serves — the number of devices a channel can practically carry depends on its medium-access mechanism (contention-based vs. scheduled), a physical/MAC-layer decision outside this document's scope. A full-scale wireless-capable Chapar node can instead be composed of one wired switch as the aggregation point plus a set of physical APs, each on its own channel and each contributing one hop, all connected to that shared switch by cable or fiber.

Why the wireless port space is sixteen bits while wired ports stop at eight: a wired port exists only where a connector and a switch-fabric lane exist, so silicon realistically tops out under 256 lanes — one address byte fits it with room to spare (255 downstream ports plus the reserved one). Wireless has no connector bound: associations are logical, and a busy cell plausibly hosts thousands of clients — more than one byte can name. The two-hop treatment above is the way through: spending a second hop byte inside the cell widens local client addressing to sixteen bits — 65,536 identities — at the cost of one extra header byte on frames crossing the cell. This is the accounting behind the 255 × 255 wireless tier in [Chapar](./chapar.md)'s capacity examples.

#### Packet congestion
Congestion on any port still forces caching on port interfaces, which can drop efficiency by up to 50%. Suggest using computer hardware studies, e.g. PCI Express (PCIe), to handle this consideration on a best-effort basis.

Port-level congestion is a fundamental property of any statistically-multiplexed frame-switched network, independent of forwarding-decision complexity — it is not eliminated by simpler switching logic, and Ethernet does not solve it at the header level either. Chapar does not add a header field for congestion signaling: the cost is not justified against the available operational approach — per-port link observability paired with the SFU hardware model, allowing capacity to be monitored and links upgraded as real usage demands.

#### Switching
[Diagram showing how packets route in their way!](https://www.draw.io/?lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1#R7VrbctowEP0aZtqHdizfMI8JTdPMpE2mTKbNo7AV49ZYjhAB9%2Bu7RhK%2BCAhNjLmkLx5ptZJXZ492V4aO1R%2FPLxlOR19pQOKOaQTzjvWpY5qe68EzF2RC4JiGEIQsCoQIFYJB9IdIoVKbRgGZVBQ5pTGP0qrQp0lCfF6RYcborKr2QOPqW1McEk0w8HGsS39EAR9JqevYxcAXEoUj9Wrk9sTIGCttuZXJCAd0VhJZFx2rzyjlojWe90mcg6eAEfM%2BrxldWsZIwreZ4IgJTzieys1Ju3imdksC2LzsUsZHNKQJji8K6Tmj0yQg%2BYoG9EZ8HEMTQfMX4TyT%2FsNTTkFUrHBNaSr1dKvlRiZ0ynxph7SMYxYSqSXxzi0sTZM7vSR0TDjLQIGRGPPoqeo%2BLFkQLvUKnKAhoVoNm6nB9u2qryEHzk3zpp%2FFEQDEYKezUcTJIMWLTc3gdFQBGwokr4dLAfZ%2Fhwt8b6YcViFSHkQMmB3RBPoAUs6q9Sg%2BEcbJfCNCclTRMlNd2Z%2BVaS5loxLDlew1mHaPh4q2TkV3X1TsHQRsgBbLfubzPzqqe%2F9KSL2mIZVTb2kEhiw5b3lV0iNUI7OwSc6qOWZpxla%2BQnrcOCaOI7QTj5wxhrOSQpojPVnvMNutRSmrluOe0be6Rs2PwoKXetVe4VQ3BszOJylOoB3m7burW1D6DrEaEoEch5XLKko8ZHVJWQtBqDGGUb5BhhPwxLrF9puNcByFed8Hki1e1kR6qnu%2BzfyEVvn5QA%2BvOqmV02vtK0Upa0rInaWpzva7JHoEBdO4GcDjCvSMd4rt7%2FfN5wbo6xi1QGS3SV9rbZh6oItwWWDrPk6pGvgwWXDyDBQQSufFYDWwQQ%2BPc7zFEyR9cfvKUazHvcLlpWAm1qmEtJKe6Qktv7xqPf6JjZxu%2FOvaeySQuYpABxT%2FyrFOmbbr2rFXP9HdGtAiKDdROx7IVZ3MI16q86F3LxfbLjFZK5zV%2BDX%2BRWVlz9pYJj6rXytDX11WHsiFeBcOb%2FyyvBeHO6hhh%2Bu3w3IOradEx%2Bs57qorw9HXST1vn2nuMD6obHW41EGqHK7GP5tsjZz7T%2FxFhuEadvdNMNj2WmSwpV%2B3jjBxrOK2CsB7ThwIdTdmgucnNP0JyjqM2nwXLt9NJd%2B%2By12n4WrB01w%2B4IzgsR5Q7ZOMsaj%2Ba1W7QVYv1tbBf5pFmga%2Fa7YJv7E1%2FObbgL%2FdIln%2FFr6x1DtJF9SLvFZ%2FjdCj%2F%2F9P6jksLbpAv%2B78d8GOjwF0i%2F9GiaKp%2BIeZdfEX)

Two generic switch classes exist, defined here once so every protocol document can reference them:

##### Blocking Switch
Transmitting will block sender until frame transmitted successfully. Sender can be sure frame transmitted.

##### Non blocking Switch
Transmitting will not block caller to be non blocking and queue frames for congestion situations.
A situation might be occur that a port available when a frame queued but when the time to send is come, the port broken and sender don't know about this.

### Edge computing
Network cost is transmission plus routing plus state — minimizing a header's byte count is not minimizing the total. Moving data across a network to be processed or stored far from where it arose must be justified by more than habit; when locality reduces total cost, the architecture should make execution and storage at the edge possible and economically preferable — the low-power Chapar switching fabric and nearby coordinators included. This is an architectural preference, not a mandate on applications: no topology is forced on anyone, and the ecosystem's tooling (code generation, coordinator services) is expected to make the local choice the easy choice.

### Place in the stack
The project's network protocols map onto OSI for orientation:

| Layer       | OSI mapping | Protocol                                                                                                                                    |
| :---------- | :---------- | :------------------------------------------------------------------------------------------------------------------------------------------ |
| Physical    | Layer 1     | Any suitable medium spec, e.g. Ethernet (its layer-one part only); [Asb](./networking-osi_1-Asb.md), [Parvaz](./networking-osi_1-Parvaz.md) |
| Link        | Layer 2     | [Chapar](./chapar.md)                                                                                                                       |
| Network     | Layer 3     | [Giti (GP)](./giti.md)                                                                                                                      |
| Application | Layers 4–7  | [sRPC](./sRPC.md)                                                                                                                           |

Per the [Layer presence](#layer-presence) principle this mapping describes capability, not obligation — a given link realizes whichever of these layers justify themselves on it; a protocol document declares the conditions under which it applies rather than presuming it rides beneath every packet. Above the stack sit the rest of the ecosystem: the router/network-coordinator role is the ChaparKhane ([Chapar](./chapar.md)), the operating system is [PersiaOS](./persia_os.md), and applications run as unikernel images produced by the Achaemenid auto-generation mechanism (see the [Enterprise](../README.md#enterprise) statement for the commercial components). Protocol documents own their own layer's content; this table is the single stack overview, and protocol documents reference it instead of restating a private copy.

## Results
Insufficient deployment experience has been recorded under this consolidated structure to report real, observed outcomes. This section will be filled in once there is such experience to draw on.

## Discussion

### Drawbacks
Consolidating the packet model, registry, special frames, layering principle, and hardware notes into one file makes it the mandatory dependency of every protocol document — a change to the registry or packet rules touches all of them at once. This is deliberate (one owner of truth beats three drifting files) but concentrates review responsibility here.

### Rationale and alternatives
- **Keep the three legacy files separate (rejected)**: the split followed no reader need — the packet model, its frame kinds, and the hardware considerations are consulted together; the separation produced dead links (`networking-frame-signature.md`) and duplicated switch-class definitions across files.
- **Leave the layer-presence principle inside [Chapar](./chapar.md) (rejected)**: it is not Chapar's rule — it binds every layer and every future protocol; keeping it there would force unrelated protocols to cite a layer-2 specification to justify their own absence.

### Prior art
- [Enlightra](https://enlightra.com/)
- The OSI model's own layering, and the long practice of tunneling one layer over another (L2-over-L3 VPNs), show stacks being composed opportunistically — the [Layer presence](#layer-presence) principle states explicitly what such practice implies: presence is per-link, never automatic.

### Unresolved questions
1. Is FrameType 11 (`Security`) the same frame as the [Special signature frame](#special-signature-frame)? The legacy registry pointed both Padding and Security at the signature document without ever stating the mapping; the table above preserves the association, but the identification needs an explicit ruling.
2. The exact sub-frame-type layout for the Internet-suite compatibility range (`FrameType == 100`) is sketched but not specified — how Ethernet's EtherType and IP's protocol numbers map into it needs its own pass.
3. Can one primitive give a *small* packet both goals at once — confidentiality (unreadable by third parties in transit) and integrity/authenticity (tamper-evident)? Today the pieces split: the signature frame provides integrity only, and the encryption suggestions provide confidentiality only. Modern AEAD constructions (e.g., AES-GCM, ChaCha20-Poly1305 — the family TLS 1.3 standardized) solve exactly this pairing with a single key and roughly a 16-byte tag, making them the leading candidate if the model adopts a dedicated answer; recorded deliberately as an open direction for dedicated review, not a settled method.

### Future possibilities
- The registry grows by appending rows; if it ever becomes machine-consumed, extract it into a formal registry per the pattern discussed in [Documentation](../documentation.md).
- More compatibility mappings (ATM, MPLS, ...) follow the same FrameType-plus-sub-frame pattern as the Internet suite.
