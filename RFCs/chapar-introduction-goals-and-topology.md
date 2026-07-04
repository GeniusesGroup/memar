---
RFC Number: 001000
Title: "Chapar: Introduction, Goals, Non-Goals, and Topology Capacity"
Status: Draft
Start Date: 2026-07-01
Applied to: ["networking-osi_2-Chapar.md#chapar---data-link-protocol"]
Supersedes: null
Superseded by: null
Related:
  Depends_on: []
  Extends: []
  Conflicts with: []
Author(s): []
---

## Summary
Chapar is a stateless, source-routed layer-2 protocol. This RFC records the goals it is designed against, the things it deliberately does not attempt to solve (and why), and worked capacity examples showing what its addressing scheme can reach at different topology depths. The protocol specification itself (`networking-osi_2-Chapar.md`) stays limited to wire format and normative behavior; the narrative context for it lives here.

## Motivation
A protocol spec that only states rules, without the goals those rules serve or the boundaries they deliberately stop at, is hard to extend correctly later — a future contributor can't tell whether an omission was intentional or an oversight. This RFC exists to make every intentional boundary explicit and give it a recorded reason, separately from the wire-format spec.

### Why "Chapar"
["The Chapar"](https://en.wikipedia.org/wiki/Chapar_Khaneh) (Persian: چاپار‎) were express couriers of the Achaemenid-era Persian postal system, each station (a "Chapar Khaneh") keeping fresh horses and supplies so a message could keep moving without its courier having to rest or resupply. The name was not chosen only for its historical flavor — the parallel to this protocol's own design is fairly direct: in the old system, a letter was handed off to a new courier at each Chapar Khaneh station, continuing its journey under new hands rather than one courier carrying it the whole way. In this protocol, the same thing happens structurally: whenever a packet reaches a ChaparKhane, its Chapar frame is effectively handed to a new leg of routing — a fresh path is established or composed for the next stage of the journey, rather than the originating device having to have known the complete end-to-end route in advance. Horse and letter became switch and packet, but the underlying shape — relay stations that hand a message onward, each responsible only for the next leg — is the same one this protocol is built on.

## Guide-level explanation
Chapar's goals, in plain terms: keep switching logic simple enough to eliminate the need for expensive hardware; keep per-bit network cost down, not just raw bandwidth; support very large layer-2 networks (into the hundreds of millions or more of nodes, depending on topology depth) without needing a layer-3 protocol just to scale; and reduce power consumption both directly (switch hardware) and indirectly (cooling).

Equally important are the things Chapar explicitly does not try to do — each of these is a deliberate boundary, not an oversight:
- **Security** is left to physical access control and to ChaparKhane as network coordinator, since layer 2 is inherently tied to physical-layer access. Layer 1 can provide immediate containment when instructed by an authorized coordinator — shutting down a wired port, or de-associating a wireless client — but this is a mitigation step, not a resolution, and the two cases are not equivalent. For a wired link, cutting logical access is a reasonably complete containment of that specific connection, though the underlying physical-security issue (an unauthorized device or person on the premises) still needs a human/physical response. For wireless, containment is structurally weaker: the medium is inherently shared and broadcast, so a de-associated device can still jam the channel or passively eavesdrop on traffic within range regardless of its protocol-level connection state — de-authentication removes a device from the protocol, not from the physical medium. In both cases, disconnecting a misbehaving device buys time and starts the response; it does not substitute for physical security intervention.
- **Error detection** belongs to layer 1 (link health) or to upper layers (end-to-end data integrity), not to this layer.
- **Fragmentation** is not handled here; MTU limits are a concern for whichever layer decides how to split data.
- **Switching loops** do not need separate prevention logic, because the hop-bounded, source-routed frame structure makes them structurally impossible for Unicast (see [RFC 001002](./001002-chapar-broadcast-scope-and-known-risks.md) for the Broadcast case specifically).
- **Backup links / fault tolerance** across multiple physical paths is left to endpoints and the network coordinator, since handling it here would require exactly the kind of per-switch state Chapar is designed to avoid.
- **Bandwidth management / QoS** is left to layer 1 and layer 3, since layer 2 cannot even distinguish inbound from outbound traffic on its own.
- **VLAN-equivalent segmentation** is left to layer 3 (via ChaparKhane), for the same state-avoidance reason as QoS.
- **Multi-path memory at peers** is not a Chapar concern; a peer may choose to remember more than one path to another peer, but Chapar does not require or manage this.
- **Recovery after wiring changes** has no dedicated mechanism; see the Discovery mechanism ([RFC 001003](./001003-chapar-discovery-and-path-establishment.md)) for how a broken path is typically re-established via ordinary upper-layer retry.

## Reference-level explanation

### Topology capacity examples
These examples show how many hosts a Chapar network can reach at different topology depths, assuming each switch has up to 256 ports (255 usable for downstream connections plus one reserved):

- **Two-tier (core/edge)**: 1 core switch + 256 edge switches connects 65,280 hosts (65,536 − 256) with a single physical link between core and each edge switch. With 2 core switches and dual links throughout, this becomes 65,024 hosts (65,536 − 256 − 256).
- **Three-tier (core/distribution/access)**: 1 core + 256 distribution + 65,280 access switches connects 16,646,400 hosts (65,280 × 255). With 2 core switches and dual-homed access switches, this becomes 16,516,096 hosts (65,024 × 254).
- **Three-tier with wireless access**: 1 core + 256 distribution + 65,280 wireless-access switches connects 4,261,478,400 hosts (65,280 × 65,280), given each wireless access point can address up to 65,536 devices (see [networking-hardware.md](../networking-hardware.md) for the wireless addressing rationale). With 2 core switches and dual-homed wireless-access switches, this becomes 4,228,120,576 hosts (65,024 × 65,024).

A ChaparKhane router with 32 GB of RAM can comfortably handle routing for a network in this range, as long as its own outer-network capacity satisfies the aggregate demand of its nodes. Nodes only depend on ChaparKhane for outer-network routing (with no need for anything like NAT); inner-network connections use ChaparKhane purely as a coordinator, secured via GP or IPsec.

[Reference topology diagrams](https://viewer.diagrams.net/?tags=%7B%7D&highlight=0000ff&edit=_blank&layers=1&nav=1#R7V1Lk5s4EP4te3Btcpgp3tjHzCTZpCqp3aqp2k2OMsigHYxYkF%2F59SuBZCOEsT3GwIx9GUPrAfT3davVEszIfJyv%2F0hBEn7HPoxGhuavR%2BbHkWGMxxr9ywSbQmCzMyYIUuQXIn0neEK%2FIBfydsEC%2BTCTKhKMI4ISWejhOIYekWQgTfFKrjbDkXzVBARQETx5IFKl%2FyCfhPyxDHcn%2FwJREIor686kKJkDUZk%2FSRYCH69KIvPTyHxMMSbF0Xz9CCOmO6GXot3nPaXbG0thTI5p8DWZLZdfn0P7aakB68fi8e%2Fg%2B92Y3xvZiAeGPn1%2BfopTEuIAxyD6tJM%2BpHgR%2B5D1qtGzXZ1vGCdUqFPhv5CQDQcTLAimopDMI14K14j8YM3vXZuf%2FuS9seOP6%2FLJRpzEJN0UrWxx%2BrNctmuWn4l2GQEp%2BcCYQAVeBLIMeUL8GUXingo9sIffq14uyvAi9WCDTgVNQRpA0lDP2JKAGg%2FEc0hvm7ZLYQQIWsr3ATiNg229HdL0gIN9AvCTfoF%2FEe7uGwHePBP4vCl9MrApVUgwiklW6vkvJqAV1sKhclvnjpj7qc97qttmU3V6UFx%2FR8Dtg7yckzb3lEsQLbgWknBDYQOsaUIJ1y9pjTJr9UbW9kS%2Bc0ml0MCVWbAdlkUPBdd5o4pLaoERukqInAXafLFWuEAH2IQdJin2YEZv8GEVIgKfEpArbkXjExnZKfCeg5wffy5IhGIoobKEKYHrZlxUffMGlqw3XeP%2BdrWLIXQRGISl%2BMHR9iN0lr8XwN1G%2BhZtzujI4Z%2BFvDW5edXzEG7dq%2FbtVo3X6lYH6FdrdHmzriOtq5VAWLEuq2frMl%2BrdVmDsy5LUaVhO1TwDqf0r2PbJj2jXWv39%2FfvVUOLfUHnGDNFPfggC3O70mWlMvlfgBCYxrnE0Myc%2BSl%2B3qZ9DMUwj7UEVeElhdo1%2BhSyMw3BHlfwNCdyF4WBKoZQMws40NGlpwGOwoNFkkDGgQhs2G%2F3Lvbl4HOlaveO47itAG25Ewkf8ziHd9Bznk4YURHPZhmU6pyar1DuxWhOWByof5mMhW6%2BLuqdmw1oh2YvZNmpDKpcxm3mT2PtC7FHHd4Ou7VvYAojmQ8gQgEbtzwKP21lPrAogEWgH3jBHPl%2BQT2YoV9gmvfHyMdVSDu3H0b2x6Ywgi%2Bw8Maj7bJGmXUNNtLgBl1duEGuexFBvZStYqlJbqC6pNZwtG%2FDU%2FN0tx2%2F0ZXjUK5zYOg5UF92HseMla0Rs9flPXGc5%2B62Kz5DmXvq7kWGSNNxZK5X50aXDpV7XdiTITeuFXPL7hRzo9fcvoT5dQBuTGTAjXHH%2BVu9T8BPWsx5O5g7PWNu9Iv5NUJu9gx5L9mFPWsH14K51jPmVq%2BYXx%2Fgutsz4PZgAL%2BagF3Xew7YneFgfq2QdzwvFxvGSznC4XDAvVYSuB3b%2FYDycdeCuZKc6Rrznnfau0PeANTRXN2yOt4BNJiE3LUAPukZ8J4Tctdo42bPkPecjxv0xs6OkjOdY95vQu5owIePZDXr0jWSujody1AcUMCGv023qjtThBu9bdM11Y1MfMtzvk%2B3eTMMVQSRdVfsu33EEW293bo7o46qIjp%2B31MdWHV7ec%2FCxVRwce9tBRm3Bphq%2Bqk9YNSdSVcIjKHpEjCGpRpMt7Co%2B5lvsOzGgN5gUQeFK4TFHJ4XGyu4jAwnYuqe0oOA5A9eCGY4DzN2wDj%2FLbAouMvyGOsDraBbybpoxstFR1R3TBkRDZYNbbrw2ZudtL8VIl7IYOfXTUV9WhAyhsTRJv%2BBeeNAvABG44U8YFDaoTgjEPhMh2AJt00LihW0qzYREqrE4jEVcUkdB%2BnZ5q5hFrQWuj2J%2BS2w1XbGFbqqTmS74bSbd5bUYEhBo4tZw563qLdlg3mL2jr2uxmWUU%2BFc%2BciYsVXfOpCfMLnwLbi1j57UfPCYPUVUi1ezOnfvFTrOfMw5MSD1ewt7rR7rryzt7RXOHPk%2FPXkr7YY9dfZvxW9sX5%2FW9GFkZdIXholS%2B%2FHatMUMSYMeQZeAcV2aibgdRHS5cYcdZ73xnzESz8K0qJvse1jx6kLvdduHRinLpwzs4wjxqmhJ8%2BEpYg55%2BTI3Fn1naXWTNeuyZ01j%2F497xgb9vh%2FGdPrari3Thm%2BW7NrNf58vUOzOT5ibB53OjZ3mb1YhTBmQ9QKS0kLzQPx7yTXQgrVxAJmbTIwh5LHme7SHbeMQznjIL%2BtbNdlHOqGEPtiQ4gaW1%2BOYSkMFhFIR4dzYg6YM7uPp1lu%2FqUsV7V%2B4V14rizPtd7SYCeSciyT0u3b69k1K0%2BvL1jU5cFkANGiunIkeJ8lIK61bK9gG7PqNJi%2B04ovJomf97mqtNz8Z2COok1R9QuMlpAZQqm85B507h54QXFRVhLjdA6iUtkSpAjQX2pOgCxS9jHvxnoeSPZVWXEVs0JLK6Z3WgTZd5vu6ON7KA7UljhNQhDzLo1CxtzAHbd8Jt4avyhDNFiO%2BZU08ah5CUlpZzPav7gSN2HGifxr46XLrHDqyze27Ys%2By%2FQZ0e5Yn4WjuOOskurt2H1XwdFgJsYgLB%2B8L92pDz2c0qgXx3ckRN5znJsTa45iRJDQT7VuCcvGeqXbkerNIgxIVTk%2BypIIbET13EwN7Tc0Z54AxKR2qEmY%2B82nO1vPXpC82bkf8Bct%2BIXK57AcTXULVo1XMC7mFepeLrh5hZtXeLteYeg%2BwRarOr35hP3TzptPuPmEm0%2FowCdYtryXpv9AQf0W%2BM0p3JzCW3YKA5w%2BWLbRVaxAT3f%2FYapYMNj9my7z0%2F8%3D)

### Non-goal drawback details
- Two Non-Goals worth flagging together: **Backup links** and **Multi-path memory at peers** both note that Ethernet switches supporting multi-path forwarding suffer a large performance penalty — this observation motivates why Chapar does not attempt multi-path support either, rather than treating single-path-only as a mere simplification.

## Drawbacks
Each Non-Goal above is, by definition, a capability the protocol does not provide — a network operator who needs built-in QoS, VLAN-equivalent segmentation, automatic multi-path fault tolerance, or layer-2 security must get it from another layer or another tool. This is a deliberate scope choice, not an accidental limitation, but it does mean Chapar cannot be adopted as a drop-in Ethernet replacement wherever those capabilities are assumed to be present at layer 2.

## Rationale and alternatives
- Alternative: absorb one or more of these Non-Goals directly into Chapar (e.g., built-in QoS or multi-path support). Rejected in each case for the same underlying reason: doing so would require some form of per-switch state, which conflicts with the core stateless-switching goal this protocol exists to achieve.

## Prior art
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

## Unresolved questions
- None specific to this RFC at the time of writing; individual Non-Goals may need their own follow-up RFC if a future requirement forces reconsideration (e.g., if a real deployment needs layer-2 fault tolerance badly enough to revisit the multi-path decision).

## Future possibilities
- If a specific deployment (e.g., a large greenhouse or industrial site) hits a hard requirement that a Non-Goal currently excludes, that should become its own RFC proposing a targeted extension, rather than reopening this document.
