# Edge
The relation itself. Every other relation in the graph — a label, a loop, a preference, a membership — is an edge with a name and MAY hold data, so the edge is what those relations are instances of.

This module keeps the edge's own contract. The individual relations live in the folder that owns each one; the edge domain owns none of them, and the documents in [`edges/`](edges) are where each one's Model line and policies are stated.

## Identity
An edge is a thing: it is stored as a record, it has an identity, and that identity is a [`MemoryAddress`](../../computer/memory/address/protocol/address.kh). So this module imports `MemoryAddress` rather than declaring an `EdgeUUID` of its own — the same collapse `time`, `uri`, `text`, `calendar` and `label` already made. `user/protocol/dt-uuid.kh` still keeps a `UserUUID`, and that fork is open.

The edge's identity is therefore readable two ways over the same value: the address says what record this is, `EdgeID` says what relation this is. Nothing requires an edge identity to differ from the record identity, and nothing yet requires two records to answer the same `EdgeID`.

## What the protocol requires of an edge
`EdgeModel` requires the thing domain's model and the edge's own identity. That is the whole contract today, and it is deliberately small: an edge is identified, and what an edge does with the two things it joins is not written down anywhere yet.
