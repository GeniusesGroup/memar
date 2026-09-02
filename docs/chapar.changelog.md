# Chapar - Data Link Protocol Changelog

## Changelog

### Consolidated five Chapar documents into one Explanation-facet document
- Time: 2026-08-26T05:29:13Z
- Type: merged
- Cited:
  - [Documentation — Explanation](./documentation-explanation.md) — Reference: its merge-before-Final rules governed which ID the merged document kept and prohibited new citations pointing at the absorbed pre-Final documents.
  - [The Error](./error.md) — Reference: declared as `Depends_on` by absorbed document `001002` (Chapar Broadcast: Scope, Privacy Rationale, and Known Risks); on verification no body-level dependency on it survives in the merged content, so it is recorded here rather than linked from the base document.
- Propagates to:
  - networking.md: Done — its link target `./chapar.md` is unchanged; verified no edit needed.
  - sRPC.md: Done — its link target `./chapar.md` is unchanged; verified no edit needed.
  - README.md (repository root): Done — its link target `./docs/chapar.md` is unchanged; verified no edit needed.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: asked for migration of the Chapar documentation from the older per-section companion-document method to the current facet-based method.
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote: performed the consolidation.

#### Summary
The Chapar documentation previously consisted of five files written under the older documentation method: this base specification plus four companion documents (`001000` chapar-introduction-goals-and-topology.md, `001001` chapar-vs-ethernet-rationale.md, `001002` chapar-broadcast-scope-and-known-risks.md, `001003` chapar-discovery-and-path-establishment.md), each carrying rich front matter (`Applied to`, `Citations`, `Depends_on`, `Extends`) pointing at specific sections of the base spec. All four were Draft. Under the current method they are one continuous argument about one subject, so all four were merged into this base document without summarization: each topic's normative text leads and its rationale lives in that topic's own `Discussion` bundle, so readers who want only the "how" can skip every `Discussion` without losing normative content. The merged document keeps this file's original title unchanged ("Chapar - Data Link Protocol") and, having had no prior number of its own, received `ID: 394466` under the hour-value convention. The absorbed numbers `001000`–`001003` are retired and never reused. The absorbed front-matter provenance fields were migrated into this entry's metadata rather than kept in the base document.

#### Rationale and alternatives
- Keeping the four companion files separate was rejected: they cross-referenced each other heavily, so any rationale path loaded three or four files, and the spec degraded into a hub of "see related document" pointers.
- Merging all rationale into a single separate companion file (e.g. a dedicated rationale document) was considered and not chosen: it still splits one subject across two files; distributing rationale into per-topic `Discussion` bundles keeps each topic's how and why adjacent with predictable placement.

### Created the Practice companion for Chapar
- Time: 2026-08-26T05:29:13Z
- Type: added
- Cited:
  - [Chapar - Data Link Protocol](./chapar.md) — Depends_on: every step in chapar.practice.md restates normative behavior defined here; the procedures are meaningless without it.
  - [Documentation — Practice](./documentation-practice.md) — Reference: the schema followed (name/description-only front matter, imperative style).
- Propagates to:
  - chapar.md: Done — the practice file derives only from behavior already normative here; nothing needed to change in the spec.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: specified the four-file structure as part of migrating the Chapar documentation to the current method.
  - [Super Z](../CONTRIBUTORS.md#super-z) — wrote: derived and authored the procedures.

#### Summary
Created `chapar.practice.md` alongside the consolidated base specification during the same consolidation that merged the four companion documents into `chapar.md`. Its content is an imperative restatement of behavior that was already normative in the spec (switch frame processing, endpoint Unicast sending, Discovery participation, ChaparKhane path composition, and known failure modes); it introduces no new semantics, so the base document required no change.

### Rewrote the Introduction's Motivation/Methodology split and resolved ambiguities by expansion
- Time: 2026-08-26T06:11:59Z
- Type: revised
- Cited:
  - [Documentation — Explanation](./documentation-explanation.md) — Reference: its definitions of Motivation (the problem/friction) and Methodology (how the content was actually arrived at) governed the rewrite and the boundary between the two sections.
- Propagates to:
  - chapar.practice.md: Rejected — this revision changed ordering, Introduction prose, and rationale expansions only; no normative statement the procedures restate was altered.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested, reviewed: directed that Methodology describe how the problem was studied in Ethernet and other protocols rather than the documentation-production process, asked for a critical ordering review, and instructed that ambiguities be resolved with more explanation instead of summarization.
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote: performed the revision.

#### Summary
Methodology was rewritten from a documentation-production narrative (which belonged in this changelog and is now only here) into the design-inquiry narrative it should have been: decomposing what any data-link switching scheme must decide — where forwarding knowledge lives, how a sender bootstraps its first path, what bounds a frame's lifetime — and studying where Ethernet/datagram switching, circuit switching (telephone exchanges, ATM, Frame Relay), and flood-based ad hoc route discovery each place that knowledge; Chapar's design is presented as the synthesis of those placements, checked numerically against topology-capacity and header-cost figures. Motivation now carries only the frictions (per-switch state in Ethernet, reachability bootstrap cost, rules-without-goals ambiguity, the recurring reviewer questions), keeping an explicit boundary against Methodology. Topic order was critically reviewed; the placement of Why "Chapar" ahead of terminology scope (defining ChaparKhane before first use) was confirmed, and the remaining sequence was kept as dependency-sane. Ambiguities were resolved by adding explanation, never by compressing: concrete header-length arithmetic including the Broadcast exception to "Hop Count indicates frame length"; the structural-support vs. usage-policy distinction behind the Frame types paragraph; the delivery-guarantee consequences of Blocking vs. Non-blocking Switching and their tie to Discovery refresh; why Broadcast must reserve the full hop-port space (in-place rewrite containment); what junction problem the virtual-switch-hop rule solves; who re-announces after a topology change; and header-cost arithmetic aligned with the four-fixed-field layout (~20 bytes at sixteen hops, inside Ethernet's 14–22-byte span).

### Made announcements event-driven, documented the composition hop cap, and closed terminal-behavior gaps
- Time: 2026-08-26T06:58:10Z
- Type: revised
- Cited:
  - [Chapar - Data Link Protocol](./chapar.md) — Depends_on: the practice file's amended steps restate the new normative rules.
- Propagates to:
  - chapar.practice.md: Done — announcement timing, Next Hop advancement, and terminal-case drops mirrored into the procedures.
  - Frame architecture (media floor note): Pending — awaiting the owner's decision between keeping Discovery Broadcast-only (then documenting a ~300-byte minimum L1 frame requirement) and amending Discovery so a single-association device MAY introduce itself by Unicast directly to its coordinator.
  - Discovery (upper-layer identity note): Pending — awaiting approval of a note stating that stable identity binding above this layer is a universal layering property shared with Ethernet (ARP/name services), not specific to Chapar.
  - State model compared with Ethernet (depth scoping sentence): Pending — awaiting approval of one sentence recording that both protocols hand off to layer 3 beyond shallow-to-medium depth, with Chapar reaching that hand-off point on cheaper hardware.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided: ruled that devices are silent by default (announcement at join, re-announcement only on failure indication), approved documenting the composition hop cap and the terminal-semantics rules, and rebutted the identity-binding critique as a universal layering property rather than a Chapar-specific dependency.
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — applied: implemented the rulings and drafted the pending additions.

#### Summary
Three rulings from critical review were applied. First, periodicity was removed from Discovery everywhere it appeared: membership is silent by default; a device announces at join time and again only when an upper-layer timeout indicates a dead path, so Broadcast remains genuinely rare and the standing-load objection to the no-deduplication judgment collapses. Second, the composition paragraph now states that a composed Path(D1→D2) carries both legs inside the single 255-hop header budget, capping coordinated pairing reach while leaving single-legged coordinator contact at the full range. Third, terminal behavior became normative in Rules — Next Hop is a moving index advanced past each switch's stamped position; frames whose next hop is exhausted or whose indicated port is missing/down are dropped silently; stray Broadcast copies are dropped — with recovery explicitly delegated to upper-layer timeouts and rising drop rates delegated to watching layers as misbehavior signals.

### Made layer-2 presence a per-link decision and closed the remaining review threads
- Time: 2026-08-26T07:13:19Z
- Type: revised
- Cited:
  - [Chapar - Data Link Protocol](./chapar.md) — Depends_on: the practice file's amended steps restate the new normative guidance.
- Propagates to:
  - chapar.practice.md: Done — shared-segment scoping of Broadcast announcement, direct coordinator registration over dedicated associations, and the no-header-on-non-switching-links rule mirrored into the procedures.
  - Frame architecture (media floor note): Done — resolved by the owner's per-link principle rather than a blanket minimum-frame requirement.
  - Discovery (upper-layer identity note): Done — added with the universal framing the owner required.
  - State model compared with Ethernet (depth scoping): Done — expanded beyond the drafted single sentence at the owner's request, so the critique cannot resurface.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided: established that whether layer 2 exists on a link is a capacity-and-role decision (a two-device wireless association carries layer 1 plus sRPC directly, registering at ChaparKhane without any layer-2 introduction — as a phone does not announce itself to other phones on its tower); approved the identity note under its universal framing; asked for the depth-scoping explanation to be thorough enough to end the recurring critique; and instructed that further preemptive explanations be added wherever known.
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — applied: transcribed the rulings and added two further preemptive notes (first-traffic-as-path-validation; header-integrity delegation to layer-1 CRCs).

#### Summary
The owner's core correction was written in as an architectural principle: a Chapar header appears only where a link feeds a switching function. A point-to-point association may carry layer 1 plus upper-layer framing with no Chapar header at all — packets going straight from medium to layer 3 — so small-frame media remain fully usable in directly-attached roles, and the ~260-byte Broadcast form is required only on media hosting shared, flooded segments. Discovery was scoped accordingly: broadcast flooding joins shared multi-node segments; devices attached to their coordinator through a dedicated association register directly via sRPC, as a phone attaches to a cell tower without introducing itself to other phones. The stable-identity boundary was added to Discovery with the framing the owner demanded — it is a universal layering property shared with Ethernet (ARP, then names/directories above MAC), not a dependency Chapar uniquely introduces. The depth comparison gained a full paragraph stating that shallow-to-medium depth is where every practical layer-2 technology lives, that both protocols hand off to layer 3 beyond it, that the difference is economic (cheaper, lower-power switches reaching the same hand-off), and that deep dynamic meshes belong above this layer — where Chapar's Discovery pattern came from. Two preemptive notes were added on the owner's standing instruction: a freshly discovered path is validated by its first real traffic (no response exists to validate earlier), and Unicast loop-freedom holds structurally for well-formed headers while header integrity is delegated to layer-1 CRCs, since an end-to-end checksum over a rewritten-every-hop header is impossible.

### Extracted the general layer-presence principle to Networking
- Time: 2026-08-26T07:33:31Z
- Type: revised
- Cited:
  - [Networking](./networking.md) — Depends_for: now owns the layer-presence principle this document references; its rewrite merged the two sibling files this document previously linked for hardware rationale.
- Propagates to:
  - networking.md: Done — principle generalized there under Layer presence; switch-class definitions and hardware rationale now owned there.
  - chapar.practice.md: Rejected — procedures restate Chapar-level behavior only; the extracted material (generic switch-class definitions, media-existence principle) was never procedural content here.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested, decided: identified that part of what this document had absorbed belongs to networking generally, ruled the general form of the principle, and directed that other protocols later reference Networking rather than Chapar.
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — applied: performed the extraction and repointed the references.

#### Summary
Three pieces moved out of this document into [Networking](./networking.md), which was rewritten under the current method with the two sibling files merged in. First and principal: the media-existence discussion became Networking's Layer presence topic in its general form — no layer is mandatory; every layer has its own identity; presence on a link is a per-link capacity-and-role decision — with this document keeping only the Chapar application and referencing the rule. Second: the generic Blocking/Non-blocking switch definitions, which had existed verbatim in both this document and the hardware file, are now owned once by Networking's Hardware topic; this document keeps the class names, the reference, and the Chapar-specific consequences (synchronous confirmation under blocking; silent-loss window and timeout-driven re-Discovery under non-blocking). Third: minor ownership attributions — the OSI packet-ordering rule is attributed to Networking's packet model, and the topology-capacity table's wireless-addressing link now points at Networking — Hardware instead of the removed hardware file.
