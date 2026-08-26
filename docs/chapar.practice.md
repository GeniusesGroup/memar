---
name: implement-chapar
description: Use when implementing a Chapar data-link switch, a Chapar endpoint (sending Unicast, announcing or reacting to Discovery), or ChaparKhane path coordination. Procedures are derived step by step from chapar.md; it contains no design rationale (see chapar.md's Discussion bundles) and defines no wire-format changes of its own.
---

# Implementing Chapar
All steps below are imperative restatements of normative behavior defined in [chapar.md](./chapar.md). Do not introduce behavior absent from that document.

## Implement a switch
1. On frame receipt, parse the header: `FrameType`, `HopCount`, `Next Hop`, `First Hop Port Number`, then the hop-port list.
2. Stamp the physical port the frame arrived on into the frame — this is the port-rewrite rule and is mandatory at every hop, before any forwarding decision.
3. If `HopCount == 0x00` (Broadcast): the header carries the full 255-slot hop-port space with zero-length data in each slot; forward (flood) without declaring any next port. Never interpret why the Broadcast was sent — its semantics live in an [sRPC](./sRPC.md) service call elsewhere in the same packet.
4. If `HopCount` is `0x01`–`0xFF` (Unicast): verify the declared port for the current hop matches the physical arrival port, advance `Next Hop` past your stamped position, then send on the newly indicated port only.
5. Keep no state between frames: no MAC-style address table, no recently-seen-frame cache, nothing content-addressable. A switch that needs to search a dynamically-updated table to forward is implementing the wrong protocol.
6. Do not prevent forwarding loops specially: a Unicast frame cannot loop (its path is fixed in its header); a Broadcast copy is bounded by its declared path and is dropped as a stray frame once it reaches the end of it.
7. Implement as a Blocking Switch (transmit blocks the sender until success) or a Non-blocking Switch (queue frames under congestion); either class is valid.

## Send Unicast (endpoint)
1. Obtain the full hop-port path first — via [Discovery](#discovery) plus path composition below. There is no way to send before holding the path.
2. Build the header: FrameType per [networking rules](./networking.md); Hop Count = number of intermediate hops (`0x01`–`0xFF`; a Unicast frame has at least one hop); Next Hop = the hop index to execute next; First Hop Port Number = source port (in P2P it is also the destination port); append one byte per hop.
3. Transmit on the first-hop port.

## Participate in Discovery
1. Announce (shared, multi-node segments only): send a one-way Broadcast frame with `HopCount == 0x00` and all 255 slots zero-filled, carrying the Discovery [sRPC](./sRPC.md) service call elsewhere in the same packet. It is fire-and-forget — no response is defined on that stream. Announce at join time; stay silent afterward and announce again only when an upper-layer failure indication requires a fresh path. Every announcement is structurally identical, first or refresh.
2. Attached to your coordinator over a dedicated association (wireless cell, single wired uplink)? Skip flooding entirely: register with that coordinator via sRPC over the link. No Chapar header is needed on a link that performs no switching; after a failure indication, re-register the same way.
3. React (optional for ordinary nodes; ChaparKhane MUST, for broadcast announcements on shared segments): initiate a fresh Unicast frame to the announcer using the accumulated reverse path from the received announcement, reversed. Never answer as a coupled RPC response on the announcer's stream — a reaction is its own, separately-identified communication.
4. Treat every stored reverse path as ephemeral and receiver-relative: it reflects the topology at capture time and is only meaningful from where you hold it. Never copy another party's path bytes for your own use, and never assume a path survives a topology change.
5. Refresh: rely on an ordinary upper-layer timeout/retry on a failed send to trigger a fresh announcement (or re-registration). Chapar has no dedicated refresh signal; an optional "path changed" notification from ChaparKhane to authorized subscribers is an optimization, not a dependency.

## Compose device-to-device paths (ChaparKhane)
1. Collect reverse paths from devices' Discovery announcements; each completing device ends up reachable via a known path.
2. To give Device 1 a path to Device 2, join Path(D1→CK) with Path(CK→D2) reversed appropriately, using the virtual-switch-hop rule: when two joined legs connect through mismatched port numbering, insert a virtual switch hop, adding one more hop-port byte to the composed frame header.
3. Require no new Discovery round for either device — composition uses paths both parties already produced.
4. Offer the result as pull (request/response), push (proactive distribution), or both — the choice is yours; Chapar restricts none of them.
5. If multiple ChaparKhanes respond on a segment, Chapar arbitrates nothing between them; selection among multiple valid responses is a higher-layer concern.

## Edge cases and failure modes
- Port available when queued but broken when sending (Non-blocking Switch): the sender does not know; recovery is the upper layer's timeout triggering re-Discovery, not a switch notification.
- `Next Hop` pointing past the last hop-port entry, or an indicated port that is missing/down: drop the frame at that switch and emit nothing upward. A rising drop rate is a misbehavior signal for watching layers (traceability), not a condition this layer manages.
- Duplicated Broadcast copies arriving over redundant links: expected and acceptable; they are hop-bounded and die at path end. Do not add de-duplication state to eliminate them.
- Two peers wired through different port numbering: the usually higher-hop side acts as switching adaptor and adds the virtual switch hop.
- Mixed wired/wireless media (Fiber, WiFi, LAN, Bluetooth, ...): processing is identical; media and Energy||Frequency specs do not change any step above.
- Mutable port numbers due to physical link limits: endpoints must beware; never treat a stamped path as valid after rewiring.
