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
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested, decided
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote

#### What changed
This document previously predated the current documentation method: no front matter, no recorded drafting date, scattered across three sibling files with dead links. It was rewritten as a single Explanation-facet specification consolidating all three: the packet model (at least two frames, signature frame at packet end, OSI-ordering and post-layer-3 encryption suggestions, 8 KB bound with the video-call arithmetic), the frame concept with its `FrameType` byte, Go interface, and `NextFrame()` handler requirement, the frame-type registry (with the experimental-range ignore rule and signed extension), the special signature and padding frames, Internet-suite compatibility mapping, the hardware considerations (SFU, wireless access points, congestion), and the two generic switch classes — previously duplicated between files. The new Layer presence topic states the principle extracted from Chapar review in its general form: no layer of the network model is mandatory, every layer has its own identity, and presence on a link is decided per link by capacity and role — illustrated by the direct association, the phone-and-tower, and the multi-access switched segment. Repairs made in passing: the registry's dangling `networking-frame-signature.md` links now point at internal anchors, stray duplicate rows were dropped from the legacy table, and one truncated sentence (the signed-bit extension rule) was completed. The original drafting date being unrecorded, Start Date reflects this rewrite; the lineage is this entry.

Identified that part of what had been written into Chapar belongs to networking generally, ruled the general form ("no layer is mandatory; every layer has its own identity"), directed the rewrite of this old document under the current method, and approved merging the two sibling files into it. (Omid Hekayati)

Performed the consolidation. (Super Z)

#### Unresolved questions carried forward
Whether FrameType 11 (`Security`) is identical to the special signature frame — the legacy files implied but never stated it — is flagged in the base document's own Unresolved questions for an explicit ruling.

### Broadened the definition, grouped named frames, and recorded the self-describing-frame decision
- Time: 2026-08-26T08:12:10Z
- Type: revised
- Propagates to:
  - chapar.md: Rejected — no Chapar-level statement depends on the reworded definition or the new grouping; anchors it does not use remained stable.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested, decided
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — applied.

#### What changed
The Abstract and Scope no longer define networking as connections between 'computer systems': the definition is now between computing components generally, with the PCIe/GPU-CPU case asserted in the definition itself — such a link forms a real network whose principles this document governs — instead of appearing later as an example. All frames specified by this document now sit under a single ### heading (Frames defined here) with one #### entry per frame, so future additions join an existing category rather than scattering across top-level topics. A new subsection under Frames records the two identification approaches for packet sections: header-introduces-next chaining versus self-describing frames, with self-description mandatory here (first byte FrameType, eight bytes extended), noting QUIC's reliance on the same shape and tying the model together with the NextFrame() handler requirement.

Flagged the opening definition as inheriting the ecosystem's computer-to-computer assumption and required the GPU/CPU-over-PCIe case stated as definition rather than example; directed that all frames specified here live under one heading with per-frame subheadings as they multiply; and ruled that the two identification approaches be written down — header-introduces-next (the legacy shape, e.g. EtherType/protocol-field chaining) versus each frame introducing itself at its own first byte (adopted here; the shape modern protocols such as QUIC emphasize). (Omid Hekayati)

### Resolved review threads: trailer location, fragmentation denial, encryption nuance, registry honesty, MediaTypeID rationale, wireless addressing
- Time: 2026-08-26T09:03:51Z
- Type: revised
- Cited:
  - [Media Type Extension](./media-type.md) — Reference: its 64-bit hash-derived identifier definition supplied the recorded rationale for why FrameType deliberately does not reuse it.
- Propagates to:
  - chapar.md: Rejected — its capacity-table link to this document's Hardware topic is now satisfied by the added wireless-addressing rationale; nothing else it states depends on these revisions.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — applied

#### What changed
Six review threads closed in one pass. The signature frame now explains how a reader reaches the end-anchored trailer without walking forward: layer 1 delivers a delimited unit, and parsing proceeds backward from that edge through SignatureScheme/Length. Packets gained two corrections: the encryption suggestion reads as low-cost-default-after-layer-3 with deeper encryption as a knowingly expensive option rather than an absolute; and the 8 KB bound is attributed to its true origin — the model's 16-bit Length ceiling — demoting the video-call arithmetic to illustration, followed by the new architecture-wide principle that fragmentation does not exist in any layer (links carry whole packets or do not host them), with sRPC-level simulation noted as an application-side workaround and genuine end-to-end 8 KB MTU as the goal. Frames now record why FrameType deliberately parts ways with MediaTypeID: hash-derived decentralized minting justifies 64 bits there, while a small centrally-registered wire vocabulary paid on every frame justifies one byte here. The registry states its numbers are presentational until Memar's protocols settle. Wireless access points gained the missing rationale: connector-bounded silicon caps wired ports under one byte of addressing, while logical associations need the two-hop treatment to widen cell-local addressing to sixteen bits. Finally, the small-packet confidentiality-plus-integrity question was added to Unresolved questions, naming AEAD constructions as leading candidate without settling anything.

Approved making the trailer's backward-parse explicit; ruled that the 8 KB bound originates from the model's own 16-bit Length ceiling and that fragmentation is denied across every layer (simulable only above, via sRPC conventions, never a layer capability), with maximum-capacity operation as the stated direction; corrected the encryption suggestion to low-cost-after-L3 rather than always, with deeper encryption as a knowingly-expensive option; asked the small-packet confidentiality-plus-integrity pairing be kept an open question rather than settled, open to a definitively better proposal; ruled current registry numbers presentational until Memar's protocols settle; and delegated the wireless-addressing rationale text to Super Z (GLM-5.3-Flash). (Omid Hekayati)

Drafted all six revisions. (Super Z)

### Added the Commercial components statement
- Time: 2026-08-26T09:36:34Z
- Type: added
- Propagates to:
  - giti.md: Done — inline pointer added where ChaparKhane and Achaemenid are introduced.
  - README.md (repository root): Done — one-sentence pointer added.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — wrote.

#### What changed
New topic recording that ChaparKhane and Achaemenid are intended commercial software by Geniuses Group — the reason they sometimes appear without explanation — while stating explicitly that organizations remain free to develop their own implementations on top of the open protocols; the project's ask is support (funding the continuous development) rather than self-implementation, so that Memar moves faster.

See the paired entry in giti.changelog.md for the full ruling. (Omid Hekayati)

### Relocated the commercial statement to README
- Time: 2026-08-26T10:14:15Z
- Type: revised
- Propagates to:
  - README.md (repository root): Done — statement now lives in README's Enterprise section.
  - giti.md: Done — pointer repointed to it.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — applied.

#### What changed
The Commercial components topic added earlier this session was removed from this document after the owner judged its home wrong: the statement belongs to the project's business face, not a technical specification. It now lives in README's Enterprise section, which documents referencing these components point to instead.

The statement is enterprise material belonging under README's Enterprise heading, not inside a protocol specification. (Omid Hekayati)

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
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [ChatGPT](../../CONTRIBUTORS.md#chatgpt) — collaborated
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — applied.

#### What changed
Registry row 4 renamed from GP to GP-Thing and row 5 added as GP-App, matching GP's redesigned pair of routing frames. New Edge computing topic under Hardware records the principle that network cost is transmission plus routing plus state — minimizing a header is not minimizing the network — and that when locality reduces total cost, edge execution and storage should be possible and economically preferable, as a preference the ecosystem's tooling makes easy, never a mandate on applications.

GP's routing is now expressed by two frame types (Thing-level and App-level delivery) instead of one, and the Edge computing principle belongs here because it is an architecture-wide rule about where computation and storage live, not a GP packet property; see the paired entries in giti.changelog.md for the full rulings. (Omid Hekayati)

Partner model in the recorded design review that produced the two-frame decision and the edge-computing principle. (ChatGPT)

### Absorbed the stack overview and stated the low-capacity-media case of Layer presence
- Time: 2026-08-31T19:26:46Z
- Type: revised
- Cited:
  - [Giti (GP)](./giti.md) — Extends: the stack overview topic moved here from Giti, which no longer restates a private copy; the low-capacity shape completes the answer to the small-media question raised during GP's redesign.
- Propagates to:
  - giti.md: Done — its Place in the stack topic removed; it references this document's overview.
  - giti.practice.md: Done — created as GP's Practice facet during the same pass; its record lives in giti.changelog.md.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [ChatGPT](../../CONTRIBUTORS.md#chatgpt) — collaborated
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — applied.

#### What changed
New Place in the stack topic: the OSI-oriented table (Asb/Parvaz, Chapar, Giti (GP), sRPC) with the ecosystem roles (ChaparKhane, PersiaOS, Achaemenid unikernel generation) and the explicit rule that protocol documents reference this table instead of restating their own. Layer presence gained a fourth concrete shape: the low-capacity wireless association — layer 1 plus a compact sRPC call, no switching or routing layer expected on media too small to route on, which resolves the small-IoT-media question GP's redesign had raised.

The stack overview belongs to the parent document, since a protocol's own copy read as if that protocol were the whole stack; and on low-bandwidth media the goal is not layer-3 routing at all — such networks engage only layer 1 with a compact sRPC exchange (a sensor announcing telemetry; the access point decides what the data is worth above the link), because media too small for real routing even at layer 1 host no higher layer, a ruling that belongs here since it answers for all layers. (Omid Hekayati)

Its protocol-versus-architecture separation framing is what the stack relocation applies. (ChatGPT)

### Removed the MediaTypeID comparison from the Frames topic; the decision now stands alone
- Time: 2026-09-03T00:00:00Z
- Type: revised
- Cited:
  - [Media Type Extension](./media-type.md) — Reference: the source of the identifier this topic's removed rationale compared against. Its MediaTypeID is a 64-bit, hash-derived (first 64 bits of SHA3-256 over the structure), registrar-free identifier — that scheme was the comparison basis when FrameType's one-byte, centrally-registered registry was decided. The comparison itself now lives only in this entry; the base document states the decision without arguing why the other scheme does not fit.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — applied.

#### What changed
The Frames topic's passage explaining why FrameType deliberately parts ways with MediaTypeID (hash-derived decentralized minting justifying 64 bits there versus a small centrally-registered wire vocabulary justifying one byte here) was removed. The topic now states the FrameType decision definitively — one byte, centrally registered, paid on every frame, with the experimental range and signed extension — without reference to MediaTypeID. The removed rationale's substance is preserved in this entry and in the 2026-08-26 entry above, which first recorded it.

Base documents state definitive decisions, not justificatory comparisons against other Memar documents; where a comparison shaped a decision, its provenance belongs in the changelog, not in the normative text. (Omid Hekayati)

---

### Relocated to `docs/protocols/`
- Time: 2026-09-03T00:00:00Z
- Type: refactor
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) - directed, decided
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) - moved.

#### What changed
This document, its changelog, and its sibling files (networking-osi_1-Asb.md, networking-osi_1-Parvaz.md, networking-connection.md) moved from `docs/` to `docs/protocols/`. Relative links to documentation-system documents were adjusted for the added depth; no content change.

Memar's own protocol specifications are collected in `docs/protocols/`; networking is the shared foundation of the protocol set and moves together with the protocols built on it (Chapar, GP, sRPC, the OSI layer-1 documents, the codecs). (Omid Hekayati)

---

### Memar's position on the traditional network stack folded into this document
- Time: 2026-09-06T00:00:00Z
- Type: merged
- Propagates to:
  - os.md: Done — the OS-side half of the position (the embedded stack read as a compatibility library, never the foundation) added to that document's Networking topic in the same pass, with a pointer back to this document's new topic.
  - networking-connection.md, sRPC.md, concurrency.md: Done — references to the dissolved standalone document repointed to the new topic here.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — reviewed, decided
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote

#### What changed
The position — the traditional OS-embedded network stack is a compatibility library, chosen where its constraints are acceptable and replaced where they are not, never the foundation — now lives in this document as a full topic with its four examination points (state ownership, layer-seven discipline, budgets, checkable compliance), the justified-dependence cases, the userspace direction, and the filtration counter-argument. The OS-side half was added to os.md's Networking topic. No content was lost from the dissolved document; its "kernel" wording was corrected throughout.

The standalone position document "Memar's Position on the Kernel Network Stack" was judged ill-fitting and misworded — its use of "kernel" conflicted with this documentation set's own definition ([OS](./os.md) establishes kernel as a layer concept of any system, not an OS-exclusive component), and the position's two halves belong to the two documents that already own them. Directed that the standalone document be dissolved and its content folded here and into os.md (Omid Hekayati).

The standalone document (created earlier the same day) was dissolved and its position folded into the new "Memar's position on the traditional network stack" topic here, placed after Compatibility with existing protocols; the subject was renamed from "kernel network stack" to "traditional OS-embedded stack" to remove the terminology conflict; the OS-side transition-period paragraph was written in os.md's Networking topic; all inbound references were repointed; the earlier standalone-document decision was recorded in the topic's own Rationale so the reversal is explicit rather than silent (Super Z).

---

### Documentation-method migration completed: document-level Discussion dissolved per the finalized method
- Time: 2026-09-07T00:00:00Z
- Type: refactor
- Propagates to:
  - networking.handoff.md: Done - open questions and anticipated work moved there.
- Contributors:
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) - moved

#### What changed
- The body's fixed top-level sections are now `Abstract`, `Introduction`, `Explanation`, `Results` only (Super Z - applied the finalized documentation method).
- The document-level `Drawbacks`, `Rationale and alternatives`, and `Prior art` content preserved below; `Unresolved questions` and `Future possibilities` moved to the paired handoff (Super Z).

Dissolved the document-level `## Discussion` (Drawbacks, Rationale and alternatives, Prior art, Unresolved questions, Future possibilities), relocating all content without loss. (Super Z)

#### Considered and not done
- **Keep the three legacy files separate (rejected)**: the split followed no reader need — the packet model, its frame kinds, and the hardware considerations are consulted together; the separation produced dead links (`networking-frame-signature.md`) and duplicated switch-class definitions across files.
- **Leave the layer-presence principle inside [Chapar](./chapar.md) (rejected)**: it is not Chapar's rule — it binds every layer and every future protocol; keeping it there would force unrelated protocols to cite a layer-2 specification to justify their own absence.
- **Stating the traditional-stack position as a standalone document (rejected on review; migrated from the position topic's inline considered-and-rejected paragraph)**: the stance has two owners — the OS-side half belonging to [OS](./os.md), which had already stated it, and the network-side half belonging here; keeping a third file meant saying everything twice and coining a "kernel" meaning that OS's own definition contradicts.
- **Folding the entire position into OS (rejected; migrated from the same paragraph)**: the position binds protocol documents and systems that may run on any host; it is a networking position, not only an OS-contract position.

#### Considered and not done (from the removed document-level Drawbacks section)
- **Consolidating the packet model, registry, special frames, layering principle, and hardware notes into one file makes it the mandatory dependency of every protocol document — a change to the registry or packet rules touches all of them at once.** This is deliberate (one owner of truth beats three drifting files) but concentrates review responsibility here.

#### Related work
- [Enlightra](https://enlightra.com/).
- The OSI model's own layering, and the long practice of tunneling one layer over another (L2-over-L3 VPNs), show stacks being composed opportunistically — the [Layer presence](./networking.md#layer-presence) principle states explicitly what such practice implies: presence is per-link, never automatic.
