---
name: apply-gp-practices
description: Use when implementing, deploying, or operating any GP network component where the protocol document deliberately leaves the how open — running software routers or ChaparKhane-role coordinators, bridging GP traffic over today's Internet, or executing any other GP-related procedure that evolves over time. Procedures only; the protocol's own rules live in giti.md.
---

# GP Practices
Procedures for operating GP networks. [giti.md](./giti.md) owns the protocol — frames, addressing, and normative rules — and says nothing here binds it; each practice below is a working procedure, expected to evolve with experience, and none defines a GP frame, field, or rule.

## Run a GP software router (ChaparKhane role)
1. Implement the router as an ordinary application holding an exclusive entitlement to its network hardware — under [OS](./os.md) a router is a service, not a sanctified OS subsystem.
2. Carry GP packets over [Chapar](./chapar.md) as the link-layer protocol; every inter-router edge must be a real physical or wireless hop.
3. Apply the [Inter-society delivery](./giti.md#inter-society-delivery) ladder locally: forward to a directly connected destination router when connected; hand off to any router of the destination society when the destination router itself is not; relay only under an explicit prior agreement — never as a default.
4. Enforce the source-validation invariant before forwarding: reject any packet whose claimed source could not legitimately originate traffic through the path it arrived on.
5. Choose the society's interior organization freely — spread across border routers, dedicated core routers taking hand-offs from the rest, or any tested arrangement fitted to the society's physical realities; routing the society's own 32-bit router space is a design problem to solve, test, and refine, not a rule to follow.
6. Treat QoS scheduling, path selection among multiple valid coordinators, and internal pipelining as free implementation choices — the protocol fixes outcomes, not mechanisms.

## Bridge GP over the Internet (transition)
1. Run a transition application on every host with Internet access that must exchange GP traffic with the legacy network.
2. Listen on UDP port 80 for incoming packets carrying GP packets.
3. For each received Internet packet carrying a GP packet, route the whole GP packet to the registered destination — the app's GP address — if it exists and has requested to listen on the Internet network.
4. Outbound carries full App-level GP addresses at both ends inside the tunneled GP frame; no IPv6-range registration is involved in either direction.
5. Coverage change: when two points gain a direct Chapar/GP path, stop bridging between them; the bridge is scaffolding, not part of the network's end state.

## Edge cases and failure modes
- Destination GP address not registered, or not requesting Internet reachability: drop the packet; do not invent a delivery.
- The Internet bridge rides UDP: no Chapar-grade ingress validation holds on that path; apply the [source validation](./giti.md#standard-services) invariant wherever a GP router processes the packet.
- A Thing-level destination that never requested App-level delivery: its device app's own rules decide — forward as usual, or report as an incident (see giti.md's [Unresolved questions](./giti.md#unresolved-questions) on mixed-level communication).
- No agreed intermediary exists and no direct connection is possible: the packet is undeliverable at this layer; do not flood or guess — recovery belongs to upper layers.
