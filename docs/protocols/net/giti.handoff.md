# Giti Handoff

## Topic & Purpose
Open questions and anticipated work for the Giti (GP) protocol document (`giti.md`), relocated here when the documentation method removed unresolved-question lists and the Discussion wrapper from base documents' bodies.

## Status
Active

Open work for `giti.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../documentation-handoff.md) for what a handoff is.

## Open Questions

### Which standard services harden into protocol-level services?
- State: moved 2026-09-11 from the retired Unresolved questions. The [Standard services](./giti.md#standard-services) topic records the capability needs but deliberately leaves the roster decision to ChaparKhane's development — which needs harden into protocol-level services, which stay implementation concerns, and (for those that harden) their identifiers, payload schemas, and message flows all remain to be specified.
- Next: settle when the ChaparKhane role itself is developed.

### Ownership proof
- State: moved 2026-09-11 from the retired Unresolved questions. The address rules state every Society/Router/Thing/App owns a true 32-byte identifier beneath its temporary GP locator — but nothing specifies how ownership is *proven*, i.e., how a temp address binds to its true identity for authentication. This is deliberately unsettled: fixing one binding scheme now would foreclose better ones. Two structural facts keep the gap smaller than IPv6's, where no path exists at all — every Router range has an identifiable organization behind it (recorded in the body's attack-reporting topic), and the coordination capabilities above are meant to carry attestation once defined. Still open, and pressing precisely because source validation and attack reporting consume it. Connects to the certificate/provisioning track noted in [Chapar](./chapar.md)'s Discovery discussion.
- Next: settle together with the ingress-attestation question below and Chapar's certificate/provisioning track.

### Ingress attestation for source validation
- State: moved 2026-09-11 from the retired Unresolved questions. The invariant is fixed — a router must not accept a packet whose claimed source is inconsistent with its validated ingress path (recorded in the body's Standard services) — but the mechanism that validates an ingress path is deliberately unspecified, and is expected to share a track with ownership proof above.
- Next: design on the same track as ownership proof.

### Whether a Thing-level destination accepts unsolicited App-level frames
- State: moved 2026-09-11 from the retired Unresolved questions. Under [OS](./os.md) a Thing's hypervisor and network driver are themselves independent applications that may hold App IDs, so a Thing speaking at Thing level presents a **default app** — the device's network driver, which is the application endpoint (recorded in the body's Frame architecture). The convention left open is the policy, not the mechanism: whether a Thing-level destination with no expected app accepts unsolicited App-level frames or must treat them as [incident reports](./giti.md#standard-services) is the device app's own rule, decided per device, not fixed by this protocol.
- Next: per-device decisions; revisit only if device practice converges on a protocol-level default.

### Society identifier allocation mechanism
- State: moved 2026-09-11 from the retired Unresolved questions. The [Society identifier allocation](./giti.md#standard-services) capability fixes the shape (governing-app announcement → temporary range → collective agreement for permanence); the exact agreement mechanism and temporary-range administration remain open.
- Next: specify when the standard-services roster question above is settled.

### Inter-society routing economy
- State: moved 2026-09-11 from the retired Unresolved questions. When the agreed-intermediary shape of [Inter-society delivery](./giti.md#inter-society-delivery) is exercised, how is the relaying society's routing cost paid — per packet, per agreement period, per capacity committed? GP records that mediation is a contract and leaves the payment model open, since it depends on the digital-economy concepts this project has not yet specified.
- Next: depends on the digital-economy concepts being specified.

### The Achaemenid document
- State: moved 2026-09-11 from the retired Unresolved questions. The Achaemenid document does not exist yet; legacy files linked it as if it did. Either author it or choose its eventual home.
- Next: author it or designate its home when the commercial-components documentation is next touched.

## Anticipated Work

### A mobility/topology guidance document
- State: from the retired Future possibilities. The routing architecture deliberately delegates mobility to topology and link-layer choices; worked patterns (roaming between APs, society hand-off) deserve their own pass.
- Next: draft when mobile-GP deployment experience accumulates.

### A real attack-reporting and society-enforcement design
- State: from the retired Future possibilities. The attack-reporting/society-enforcement sketch (including AI-based misbehaving-router detection) needs a real design before implementation claims.
- Next: design together with the standard-services roster decision.

### Society delegation rules
- State: from the retired Future possibilities. How a society splits its range among routers, renumbers, and handles router churn.
- Next: record once a first real delegation case exists to test the rules against.

### Scope-implied short frames
- State: from the retired Future possibilities. Both routing frames always carry the Society prefix, even for traffic that never leaves one router. If measurement ever shows those prefix bytes matter in the common path, additional frame types with scope-implied prefixes (router-scoped, society-scoped) are the designated extension point — the registry has room, the FrameType announces the layout, and adding them changes nothing already deployed. Nothing today justifies them; only measurement would.
- Next: measurement-driven; no action until the prefix bytes demonstrably matter.

### Society-level blocking via de-peering and signed reputation propagation
- State: from the retired Future possibilities, with its full recorded design preserved below.

The primitive is inter-society route withdrawal — a society blocks another by withdrawing route advertisements for its prefixes (BGP-style de-peering, simplified by the small, deliberately-peered society graph). Coordination rides the mandatory sRPC services: a signed incident-report service carries evidence (Chapar headers stamp physical paths, so ingress routers are provable); reports propagate peer-to-peer, each society sets its threshold for automatic route withdrawal. VPN bypass fails structurally — traffic exits via a router whose range belongs to an identifiable organization; victims block at the society boundary by Society/Router prefix, and the range owner must police its customers or face de-peering. Escalation is graduated (warn → border rate-limit → partial withdrawal → full de-peer) with re-entry via signed remediation attestation. This is recorded as an option, not a fixed method, to leave room for better designs.

The mechanism works in two tiers:
1. **Intra-society consensus first**: the routers of a society agree among themselves that another society is not responding to abuse reports or is harboring sustained abuse — all routers of one society agreeing is the first gate.
2. **Inter-society propagation**: the consensus result propagates as signed route withdrawals through the society graph. Each receiving society verifies the signatures and applies its own threshold policy (immediate full withdrawal, partial withdrawal of only the offending ranges, or border rate-limiting). Re-entry requires a signed remediation attestation.

Why VPN bypass fails structurally: an attacker may spoof source addresses inside their own society, but the traffic must eventually leave that society through a router whose range belongs to an identifiable organization. The victim society blocks at the Society/Router prefix boundary — no per-app identification needed. Accountability shifts from per-packet forensics (impossible at Internet scale) to organizational responsibility: the range owner must police its customers or face de-peering. This is exactly how email abuse *should* have worked, and why Internet BGP hijacking still plagues the Internet today.

Graduated escalation:
- **Warn**: signed notice to the offending society's routers with evidence.
- **Border rate-limit**: rate-limiting of the offending society's prefixes at the border.
- **Partial withdrawal**: withdrawal of only those prefixes implicated in the attacks.
- **Full de-peer**: complete route withdrawal; traffic from the offending society becomes unreachable.
- **Re-entry**: signed remediation attestation from the offending society's routers, propagated peer-to-peer.

This is recorded as an option, not a fixed method, to leave room for better designs.

- Next: a design pass of its own, together with the attack-reporting design above.
