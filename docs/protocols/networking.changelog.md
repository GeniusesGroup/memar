# Networking Changelog

## Changelog

### Rewrote under the current method, merging the two sibling files and absorbing the layer-presence principle
- Time: 2026-08-26T07:33:31Z
- Type: merged
- Cited:
  - [Documentation — Explanation](../documentation-explanation.md) — Reference: the Explanation-facet structure this rewrite follows.
  - [Chapar - Data Link Protocol](./chapar.md) — Extends_by: Chapar's media-existence discussion was found during critical review to be an instance of a general principle; that principle now lives here (Layer presence) and Chapar references it.
- Propagates to:
  - networking-frames.md: Done — content merged into [Special signature frame](#special-signature-frame) and [Padding frame](#padding-frame); file removed.
  - networking-hardware.md: Done — content merged into [Hardware](#hardware); file removed.
  - chapar.md: Done — general principle extracted to Layer presence; Chapar references it instead of restating it; its capacity table link repointed from the removed hardware file to [Hardware](#hardware).
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested, decided: identified that part of what had been written into Chapar belongs to networking generally, ruled the general form ("no layer is mandatory; every layer has its own identity"), directed the rewrite of this old document under the current method, and approved merging the two sibling files into it.
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote: performed the consolidation.

#### Summary
This document previously predated the current documentation method: no front matter, no recorded drafting date, scattered across three sibling files with dead links. It was rewritten as a single Explanation-facet specification consolidating all three: the packet model (at least two frames, signature frame at packet end, OSI-ordering and post-layer-3 encryption suggestions, 8 KB bound with the video-call arithmetic), the frame concept with its `FrameType` byte, Go interface, and `NextFrame()` handler requirement, the frame-type registry (with the experimental-range ignore rule and signed extension), the special signature and padding frames, Internet-suite compatibility mapping, the hardware considerations (SFU, wireless access points, congestion), and the two generic switch classes — previously duplicated between files. The new Layer presence topic states the principle extracted from Chapar review in its general form: no layer of the network model is mandatory, every layer has its own identity, and presence on a link is decided per link by capacity and role — illustrated by the direct association, the phone-and-tower, and the multi-access switched segment. Repairs made in passing: the registry's dangling `networking-frame-signature.md` links now point at internal anchors, stray duplicate rows were dropped from the legacy table, and one truncated sentence (the signed-bit extension rule) was completed. The original drafting date being unrecorded, Start Date reflects this rewrite; the lineage is this entry.

#### Unresolved questions carried forward
Whether FrameType 11 (`Security`) is identical to the special signature frame — the legacy files implied but never stated it — is flagged in the base document's own Unresolved questions for an explicit ruling.

### Broadened the definition, grouped named frames, and recorded the self-describing-frame decision
- Time: 2026-08-26T08:12:10Z
- Type: revised
- Propagates to:
  - chapar.md: Rejected — no Chapar-level statement depends on the reworded definition or the new grouping; anchors it does not use remained stable.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested, decided: flagged the opening definition as inheriting the ecosystem's computer-to-computer assumption and required the GPU/CPU-over-PCIe case stated as definition rather than example; directed that all frames specified here live under one heading with per-frame subheadings as they multiply; and ruled that the two identification approaches be written down — header-introduces-next (the legacy shape, e.g. EtherType/protocol-field chaining) versus each frame introducing itself at its own first byte (adopted here; the shape modern protocols such as QUIC emphasize).
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — applied.

#### Summary
The Abstract and Scope no longer define networking as connections between 'computer systems': the definition is now between computing components generally, with the PCIe/GPU-CPU case asserted in the definition itself — such a link forms a real network whose principles this document governs — instead of appearing later as an example. All frames specified by this document now sit under a single ### heading (Frames defined here) with one #### entry per frame, so future additions join an existing category rather than scattering across top-level topics. A new subsection under Frames records the two identification approaches for packet sections: header-introduces-next chaining versus self-describing frames, with self-description mandatory here (first byte FrameType, eight bytes extended), noting QUIC's reliance on the same shape and tying the model together with the NextFrame() handler requirement.

### Resolved review threads: trailer location, fragmentation denial, encryption nuance, registry honesty, MediaTypeID rationale, wireless addressing
- Time: 2026-08-26T09:03:51Z
- Type: revised
- Cited:
  - [Media Type Extension](./media-type.md) — Reference: its 64-bit hash-derived identifier definition supplied the recorded rationale for why FrameType deliberately does not reuse it.
- Propagates to:
  - chapar.md: Rejected — its capacity-table link to this document's Hardware topic is now satisfied by the added wireless-addressing rationale; nothing else it states depends on these revisions.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided: approved making the trailer's backward-parse explicit; ruled that the 8 KB bound originates from the model's own 16-bit Length ceiling and that fragmentation is denied across every layer (simulable only above, via sRPC conventions, never a layer capability), with maximum-capacity operation as the stated direction; corrected the encryption suggestion to low-cost-after-L3 rather than always, with deeper encryption as a knowingly-expensive option; asked the small-packet confidentiality-plus-integrity pairing be kept an open question rather than settled, open to a definitively better proposal; ruled current registry numbers presentational until Memar's protocols settle; and delegated the wireless-addressing rationale text to Super Z (GLM-5.3-Flash).
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — applied: drafted all six revisions.

#### Summary
Six review threads closed in one pass. The signature frame now explains how a reader reaches the end-anchored trailer without walking forward: layer 1 delivers a delimited unit, and parsing proceeds backward from that edge through SignatureScheme/Length. Packets gained two corrections: the encryption suggestion reads as low-cost-default-after-layer-3 with deeper encryption as a knowingly expensive option rather than an absolute; and the 8 KB bound is attributed to its true origin — the model's 16-bit Length ceiling — demoting the video-call arithmetic to illustration, followed by the new architecture-wide principle that fragmentation does not exist in any layer (links carry whole packets or do not host them), with sRPC-level simulation noted as an application-side workaround and genuine end-to-end 8 KB MTU as the goal. Frames now record why FrameType deliberately parts ways with MediaTypeID: hash-derived decentralized minting justifies 64 bits there, while a small centrally-registered wire vocabulary paid on every frame justifies one byte here. The registry states its numbers are presentational until Memar's protocols settle. Wireless access points gained the missing rationale: connector-bounded silicon caps wired ports under one byte of addressing, while logical associations need the two-hop treatment to widen cell-local addressing to sixteen bits. Finally, the small-packet confidentiality-plus-integrity question was added to Unresolved questions, naming AEAD constructions as leading candidate without settling anything.

### Added the Commercial components statement
- Time: 2026-08-26T09:36:34Z
- Type: added
- Propagates to:
  - giti.md: Done — inline pointer added where ChaparKhane and Achaemenid are introduced.
  - README.md (repository root): Done — one-sentence pointer added.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided: see the paired entry in giti.changelog.md for the full ruling.
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — wrote.

#### Summary
New topic recording that ChaparKhane and Achaemenid are intended commercial software by Geniuses Group — the reason they sometimes appear without explanation — while stating explicitly that organizations remain free to develop their own implementations on top of the open protocols; the project's ask is support (funding the continuous development) rather than self-implementation, so that Memar moves faster.

### Relocated the commercial statement to README
- Time: 2026-08-26T10:14:15Z
- Type: revised
- Propagates to:
  - README.md (repository root): Done — statement now lives in README's Enterprise section.
  - giti.md: Done — pointer repointed to it.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided: the statement is enterprise material belonging under README's Enterprise heading, not inside a protocol specification.
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — applied.

#### Summary
The Commercial components topic added earlier this session was removed from this document after the owner judged its home wrong: the statement belongs to the project's business face, not a technical specification. It now lives in README's Enterprise section, which documents referencing these components point to instead.

### Renamed GP's registry row, added GP-App, and recorded the Edge computing principle
- Time: 2026-08-31T17:29:51Z
- Type: revised
- Cited:
  - [Giti (GP)](./giti.md) — Depends_on: owns both GP frame definitions this registry now names, and points back at this document's Edge computing topic from its frame architecture.
  - `chats-context/giti - chatgpt.md` — Reference: the recorded design review behind the GP redesign this change follows.
- Propagates to:
  - giti.md: Done — defines both frames and cross-references Edge computing.
  - giti.changelog.md: Done — paired entries recorded.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided: GP's routing is now expressed by two frame types (Thing-level and App-level delivery) instead of one, and the Edge computing principle belongs here because it is an architecture-wide rule about where computation and storage live, not a GP packet property; see the paired entries in giti.changelog.md for the full rulings.
  - [ChatGPT](../../CONTRIBUTORS.md#chatgpt) — collaborated: partner model in the recorded design review that produced the two-frame decision and the edge-computing principle.
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — applied.

#### Summary
Registry row 4 renamed from GP to GP-Thing and row 5 added as GP-App, matching GP's redesigned pair of routing frames. New Edge computing topic under Hardware records the principle that network cost is transmission plus routing plus state — minimizing a header is not minimizing the network — and that when locality reduces total cost, edge execution and storage should be possible and economically preferable, as a preference the ecosystem's tooling makes easy, never a mandate on applications.

### Absorbed the stack overview and stated the low-capacity-media case of Layer presence
- Time: 2026-08-31T19:26:46Z
- Type: revised
- Cited:
  - [Giti (GP)](./giti.md) — Extends: the stack overview topic moved here from Giti, which no longer restates a private copy; the low-capacity shape completes the answer to the small-media question raised during GP's redesign.
- Propagates to:
  - giti.md: Done — its Place in the stack topic removed; it references this document's overview.
  - giti.practice.md: Done — created as GP's Practice facet during the same pass; its record lives in giti.changelog.md.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided: the stack overview belongs to the parent document, since a protocol's own copy read as if that protocol were the whole stack; and on low-bandwidth media the goal is not layer-3 routing at all — such networks engage only layer 1 with a compact sRPC exchange (a sensor announcing telemetry; the access point decides what the data is worth above the link), because media too small for real routing even at layer 1 host no higher layer, a ruling that belongs here since it answers for all layers.
  - [ChatGPT](../../CONTRIBUTORS.md#chatgpt) — collaborated: its protocol-versus-architecture separation framing is what the stack relocation applies.
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — applied.

#### Summary
New Place in the stack topic: the OSI-oriented table (Asb/Parvaz, Chapar, Giti (GP), sRPC) with the ecosystem roles (ChaparKhane, PersiaOS, Achaemenid unikernel generation) and the explicit rule that protocol documents reference this table instead of restating their own. Layer presence gained a fourth concrete shape: the low-capacity wireless association — layer 1 plus a compact sRPC call, no switching or routing layer expected on media too small to route on, which resolves the small-IoT-media question GP's redesign had raised.

### Removed the MediaTypeID comparison from the Frames topic; the decision now stands alone
- Time: 2026-09-03T00:00:00Z
- Type: revised
- Cited:
  - [Media Type Extension](./media-type.md) — Reference: the source of the identifier this topic's removed rationale compared against. Its MediaTypeID is a 64-bit, hash-derived (first 64 bits of SHA3-256 over the structure), registrar-free identifier — that scheme was the comparison basis when FrameType's one-byte, centrally-registered registry was decided. The comparison itself now lives only in this entry; the base document states the decision without arguing why the other scheme does not fit.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided: base documents state definitive decisions, not justificatory comparisons against other Memar documents; where a comparison shaped a decision, its provenance belongs in the changelog, not in the normative text.
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — applied.

#### Summary
The Frames topic's passage explaining why FrameType deliberately parts ways with MediaTypeID (hash-derived decentralized minting justifying 64 bits there versus a small centrally-registered wire vocabulary justifying one byte here) was removed. The topic now states the FrameType decision definitively — one byte, centrally registered, paid on every frame, with the experimental range and signed extension — without reference to MediaTypeID. The removed rationale's substance is preserved in this entry and in the 2026-08-26 entry above, which first recorded it.

---

### Relocated to `docs/protocols/`
- Time: 2026-09-03T00:00:00Z
- Type: refactor
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) - directed, decided: Memar's own protocol specifications are collected in `docs/protocols/`; networking is the shared foundation of the protocol set and moves together with the protocols built on it (Chapar, GP, sRPC, the OSI layer-1 documents, the codecs).
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) - moved.

#### Summary
This document, its changelog, and its sibling files (networking-osi_1-Asb.md, networking-osi_1-Parvaz.md, networking-connection.md) moved from `docs/` to `docs/protocols/`. Relative links to documentation-system documents were adjusted for the added depth; no content change.
