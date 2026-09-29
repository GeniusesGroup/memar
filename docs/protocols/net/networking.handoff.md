# Networking Handoff

Open work for `protocols/net/networking.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../documentation-handoff.md) for what a handoff is. Legacy unresolved questions in this document's pre-existing topics migrate here progressively, per the documentation method's progressive-migration rule.

## Open Questions

### The address carries only destination information
- State: an address should contain only the information required to determine the destination — request data does not belong in the routing address; one concept, one representation, decided once per resource class. This remains a Networking-layer principle, not an sRPC frame-design detail. The HTTP appearance of the collapse (query versus payload, URL overload) now lives in [http.md](../net/http.md); sRPC's independent identities are stated as a positive contract in [sRPC.md](../net/sRPC.md#independent-identities).
- Next: formalize as a Networking-layer principle (or route to the protocol-concept layer) when this document's principles section is next developed.

### The traditional-stack dependence check's home
- State: whether the dependence check (use the host's embedded stack or not) needs its own practice document — the pattern [filesystem.practice.md](../memory/filesystem.practice.md) set for storage — or folds into the protocol documents themselves. Not decided.
- Next: decide when the check is first exercised against a real system.

### The userspace transport realization's scope
- State: which protocol features the userspace TCP implementation must cover (congestion control variants, option handling, offload interactions) is a specification question for [networking-connection](../net/networking-connection.md). The archived Go implementation's notes (`memar-go/libgo/net/tcp/README.md`, [GitHub](https://github.com/GeniusesGroup/memar-go/blob/dev/libgo/net/tcp/README.md)) record the goals that work was pursuing, unratified by any document here. Goals: per stream, one buffer with no bulk copies, one lock, and one timeout mechanism in place of parallel kernel and userspace timers; congestion control merged with rate limiting; keep-alive costing only the stream's few bytes of state; connection and stream metrics available for security and other uses; transport logic changeable without a host-kernel upgrade; protocol logic in userspace so an application can ship as a unikernel image. Non-goal: TCP does not depend on how its packets arrive from the layer below. Open in those notes: whether to support Packetization Layer Path MTU Discovery ([RFC 4821](https://www.rfc-editor.org/rfc/rfc4821)) for networks without IP/ICMP service, and why TCP's checksum computation depends on the layer below. Each item is a candidate for this question, not a decided requirement.
- Next: settle during that document's next revision.

### Relationship to GP's application-connection model
- State: how the userspace-TCP work relates to [GP](../net/giti.md)'s application-connection model — bridge, fallback, or replacement — is undecided.
- Next: decide when GP matures enough to compare concretely.

### FrameType 11 (`Security`) versus the special signature frame
- State: is FrameType 11 (`Security`) the same frame as the [special signature frame](../net/networking.md#special-signature-frame)? The legacy registry pointed both Padding and Security at the signature document without ever stating the mapping; the table in networking.md preserves the association, but the identification needs an explicit ruling.
- Next: explicit ruling during the frame registry's next revision.

### The Internet-suite compatibility range's sub-frame-type layout
- State: the exact sub-frame-type layout for the compatibility range (`FrameType == 100`) is sketched but not specified — how Ethernet's EtherType and IP's protocol numbers map into it needs its own pass.
- Next: dedicated specification pass.

### A single primitive for confidentiality plus integrity on small packets
- State: can one primitive give a *small* packet both goals at once — confidentiality (unreadable by third parties in transit) and integrity/authenticity (tamper-evident)? Today the pieces split: the signature frame provides integrity only, and the encryption suggestions provide confidentiality only. Modern AEAD constructions (e.g., AES-GCM, ChaCha20-Poly1305 — the family TLS 1.3 standardized) solve exactly this pairing with a single key and roughly a 16-byte tag, making them the leading candidate if the model adopts a dedicated answer; recorded deliberately as an open direction for dedicated review, not a settled method.
- Next: dedicated review of an AEAD-based answer.

## Anticipated Work

- The registry grows by appending rows; if it ever becomes machine-consumed, extract it into a formal registry per the pattern discussed in [Documentation](../documentation.md).
- More compatibility mappings (ATM, MPLS, ...) follow the same FrameType-plus-sub-frame pattern as the Internet suite.
