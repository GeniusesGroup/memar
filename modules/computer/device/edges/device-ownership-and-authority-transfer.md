---
RFC Number: 003000
Title: "Device Ownership and Command-Authority Transfer"
Status: Draft
Start Date: 2026-07-02
Applied to: []
Supersedes: null
Superseded by: null
Related:
  Depends_on: ["001003"]
  Extends: []
  Conflicts with: []
Author(s): []
---

## Summary
A device (e.g., an IoT sensor or appliance) needs a well-defined process for establishing who currently has command authority over it — starting from the manufacturer at production time, and changing hands as the device is sold, resold, or moved between organizations. This RFC starts the record of that process. It opens a new numbering series (003000+), separate from Chapar's own RFCs (001000–001999), because this problem is not specific to Chapar or even to networking — it is a cross-cutting concern that will eventually live as modules/services in the `organization` repository, not inside `memar`'s Chapar-related files.

**This RFC intentionally captures only what has been decided or proposed so far. Full design work is deferred to a dedicated future chat, at Omid's request, so it is not developed further inside the Chapar discussion.**

## Motivation
This question surfaced while working out Chapar's Discovery mechanism ([related RFC](./chapar-discovery-and-path-establishment.md)): before a device can be trusted to receive commands, something needs to establish who is currently authorized to command it, and how that authorization moves when the device changes hands. That is a bigger question than Discovery itself, so it is being split out here rather than folded into the Chapar RFC series.

## Guide-level explanation

### Fallback chain for authorizing an ownership/authority transfer
When a device needs its command authority transferred (e.g., it has been sold to a new organization), the following parties are checked in order, each acting only if the previous one is unavailable:

1. **The seller** declares the transfer directly.
2. If the seller is unavailable, the **invoice held by the buyer's governance organization** can itself serve as the basis for the transfer and for granting command-authority access to the device.
3. If the seller was not the original manufacturer (e.g., it was a reseller), that does not block the process — but if the original manufacturer is still operating, it is that manufacturer's responsibility to respond to the transfer request and to notify the governance organization.
4. If the manufacturer no longer exists, the **governance organization** itself can issue the transfer authorization.
5. If the governance organization is also unavailable, a **token embedded in the digital invoice** can finalize the transfer as a last resort.

The manufacturer is deliberately kept high in this priority chain when it is reachable, for reasons beyond just the transfer itself — e.g., a manufacturer typically needs to know current ownership for after-sales service, and if the manufacturer discloses to the original buyer that it collects some operational data from the device, that same disclosure needs to be made transparently to each subsequent owner as well. (This data-disclosure point is one illustrative example among others, not an exhaustive requirement.)

### Governance organizations do not need to agree on a shared arbiter
Earlier discussion (in the Chapar RFC series) assumed both the buying and selling organizations might need to agree on one mutually-trusted governance body per transaction. That assumption was corrected: under Omid's legal doctrine for this framework, **every organization is required to select a default governance organization for itself**. There is no need for buyer and seller to negotiate or agree on a shared arbiter per transaction — each side simply informs its own governance organization of the transfer.

How two different governance organizations then communicate and reconcile a transfer between them is explicitly **not** answered here — it is the subject of a separate, dedicated future chat about inter-governance-organization communication.

### Tiered functionality before full ownership transfer (plug-and-play)
Depending on a device's plug-and-play policy, it may offer some baseline functionality (e.g., allowing its data to be read) for a defined period without a full ownership transfer having occurred. However, full functionality — and specifically, accepting **commands** — always requires one of exactly two paths:
- the command passes through the manufacturer as an intermediary software layer, or
- a full ownership/authority transfer has occurred.

No third model for granting command authority is currently anticipated.

## Reference-level explanation
Not yet developed — deferred to the dedicated future chat referenced throughout this document.

## Drawbacks
Not yet developed. One tension worth flagging for that future discussion: the fallback chain above and the "no shared arbiter needed" rule interact in a way that is not yet fully specified — e.g., if a seller declares a transfer but the device also has a distinct original manufacturer, is the seller's declaration alone sufficient, or does the manufacturer always need independent notification regardless of who declares the transfer? This is left open rather than guessed at here.

## Rationale and alternatives
Not yet developed.

## Prior art
Not yet developed.

## Unresolved questions
- How do two different governance organizations (buyer's and seller's) communicate and reconcile an ownership transfer between themselves? (Explicitly deferred to a dedicated future chat.)
- Exact format and cryptographic scheme for the digital-invoice-embedded transfer token (step 5 of the fallback chain).
- Defined policy/duration for plug-and-play baseline functionality before a full transfer occurs.
- Exact mechanism for re-disclosing manufacturer data-collection consent to each subsequent owner.
- How this connects back to [this RFC](./chapar-discovery-and-path-establishment.md)'s open question about provisioning a device's initial trust anchor before its first Discovery.

## Future possibilities
- This RFC is expected to grow into one or more modules/services in the `organization` repository once the design is further along.
