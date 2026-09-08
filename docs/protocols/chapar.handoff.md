# Chapar Handoff

Open work for `protocols/chapar.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../documentation-handoff.md) for what a handoff is.

## Open Questions

### Discovery response authenticity
- State: a genuinely open question for the Discovery service itself (not a Chapar concern, and not something Chapar's security Non-Goal has any bearing on): since any node may optionally respond to a Discovery broadcast, should the Discovery service require responses to be signed, verifiable against a certificate both parties trust? This is entirely decidable at the sRPC/Discovery-service level and is not blocked by anything in Chapar.
- Consideration: one open sub-question worth flagging if this direction is taken — a certificate-based scheme still needs a trust anchor (the CA certificate itself) present on both the device and ChaparKhane *before* the device's very first Discovery; for a large population of low-cost devices (e.g., thousands of sensors), how that initial trust anchor gets provisioned is its own design question, not automatically answered by choosing to require signatures.
- Next: decide at the sRPC/Discovery-service level; the trust-anchor provisioning question is expected to be resolved by the certificate/provisioning document track noted under Anticipated Work. (Migrated from the Discovery topic's retired `Unresolved questions` in chapar.md.)

### The "best switch" CAM-table ceiling figure
- State: a precise, sourced figure (specific switch model and vendor documentation) for the CAM ceiling cited in [State model compared with Ethernet](./chapar.md#state-model-compared-with-ethernet) has not been confirmed; the body carries the figure as an order-of-magnitude ceiling pending a source.
- Next: add a specific vendor-product source, or keep treating the figure as an order of magnitude. (Migrated from the State-model topic's retired `Unresolved questions` in chapar.md.)

### Should this document be split again if its length becomes a real reading burden?
- State: carried from the document-level retired `Unresolved questions` in chapar.md, mirroring the open question in [documentation-explanation.handoff.md](../documentation-explanation.handoff.md) about its own consolidated structure (where that question now lives).
- Next: revisit if length measurably hurts reading or session loading.

## Anticipated Work

- A future ChaparKhane-focused document could specify its path-directory service (pull, push, or both) in detail — that design is independent of anything decided in chapar.md. (Migrated from the Discovery topic's retired `Future possibilities` in chapar.md.)
- A future Discovery-service document could specify a signed-response scheme for Discovery (see Open Questions above), including how the initial trust anchor is provisioned for low-cost devices at scale. This connects to a separate, larger planned document track (in the Organization private repository) covering manufacturer-issued default device certificates and organizational ownership transfer — that track is where the trust-anchor provisioning question is expected to be resolved, not here. (Migrated from the Discovery topic's retired `Future possibilities` in chapar.md.)
- If a specific deployment (e.g., a large greenhouse or industrial site) hits a hard requirement that a Non-Goal in chapar.md currently excludes, that should become its own document proposing a targeted extension, rather than reopening chapar.md; individual Non-Goals may need their own follow-up document if a future requirement forces reconsideration (e.g., a real deployment needing layer-2 fault tolerance badly enough to revisit the multi-path decision). No follow-up specific to the Goals and Non-Goals topic is open at the time of writing. (Migrated from the Goals and Non-Goals topic's retired `Unresolved questions` and `Future possibilities` in chapar.md.)
- If a legitimate high-frequency Broadcast use case is ever identified — none currently open — it would invalidate the Frame types topic's "rare enough not to mitigate" judgment (recorded in chapar.changelog.md) and should prompt revisiting whether a lightweight de-duplication mechanism is worth its state cost. (Migrated from the Frame types topic's retired `Unresolved questions` and `Future possibilities` in chapar.md.)
- A follow-up empirical comparison (real header-byte counts against real deployed Ethernet topologies of comparable scale) could replace the illustrative math in chapar.md's State model topic with measured data. (Migrated from the State-model topic's retired `Future possibilities` in chapar.md.)
- If the connection-oriented / connectionless classification question is raised again, chapar.md should link to that debate rather than re-open it — the State location topic deliberately avoids the classification, and the drawback record notes that some readers will still ask. (Migrated from the State-model topic's retired `Drawbacks` in chapar.md.)
- If a single topic's rationale grows unwieldy (for example, if the Discovery signed-response scheme becomes a full design), it should spin out as its own document at that point, following the progressive-migration rule rather than a dedicated restructuring pass. (Migrated from the document-level retired `Future possibilities` in chapar.md.)
