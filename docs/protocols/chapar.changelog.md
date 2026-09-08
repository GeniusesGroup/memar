# Chapar - Data Link Protocol Changelog

## Changelog

### Consolidated five Chapar documents into one Explanation-facet document
- Time: 2026-08-26T05:29:13Z
- Type: merged
- Cited:
  - [Documentation — Explanation](../documentation-explanation.md) — Reference: its merge-before-Final rules governed which ID the merged document kept and prohibited new citations pointing at the absorbed pre-Final documents.
  - [The Error](./error.md) — Reference: declared as `Depends_on` by absorbed document `001002` (Chapar Broadcast: Scope, Privacy Rationale, and Known Risks); on verification no body-level dependency on it survives in the merged content, so it is recorded here rather than linked from the base document.
- Propagates to:
  - networking.md: Done — its link target `./chapar.md` is unchanged; verified no edit needed.
  - sRPC.md: Done — its link target `./chapar.md` is unchanged; verified no edit needed.
  - README.md (repository root): Done — its link target `./docs/chapar.md` is unchanged; verified no edit needed.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote

#### What changed
- The Chapar documentation previously consisted of five files written under the older documentation method: this base specification plus four companion documents (`001000` chapar-introduction-goals-and-topology.md, `001001` chapar-vs-ethernet-rationale.md, `001002` chapar-broadcast-scope-and-known-risks.md, `001003` chapar-discovery-and-path-establishment.md), each carrying rich front matter (`Applied to`, `Citations`, `Depends_on`, `Extends`) pointing at specific sections of the base spec; all four were Draft.
- Under the current method the four companions are one continuous argument about one subject, so all four were merged into this base document without summarization: each topic's normative text leads and its rationale lives in that topic's own `Discussion` bundle, so readers who want only the "how" can skip every `Discussion` without losing normative content.
- The merged document keeps this file's original title unchanged ("Chapar - Data Link Protocol") and, having had no prior number of its own, received `ID: 394466` under the hour-value convention.
- The absorbed numbers `001000`–`001003` are retired and never reused.
- The absorbed front-matter provenance fields were migrated into this entry's metadata rather than kept in the base document.

#### Deliberation
- Migration of the Chapar documentation from the older per-section companion-document method to the current facet-based method was requested (Omid Hekayati).

#### Considered and not done
- Keeping the four companion files separate was rejected: they cross-referenced each other heavily, so any rationale path loaded three or four files, and the spec degraded into a hub of "see related document" pointers.
- Merging all rationale into a single separate companion file (e.g. a dedicated rationale document) was considered and not chosen: it still splits one subject across two files; distributing rationale into per-topic `Discussion` bundles keeps each topic's how and why adjacent with predictable placement.

### Created the Practice companion for Chapar
- Time: 2026-08-26T05:29:13Z
- Type: added
- Cited:
  - [Chapar - Data Link Protocol](./chapar.md) — Depends_on: every step in chapar.practice.md restates normative behavior defined here; the procedures are meaningless without it.
  - [Documentation — Practice](../documentation-practice.md) — Reference: the schema followed (name/description-only front matter, imperative style).
- Propagates to:
  - chapar.md: Done — the practice file derives only from behavior already normative here; nothing needed to change in the spec.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Super Z](../../CONTRIBUTORS.md#super-z) — wrote

#### What changed
- `chapar.practice.md` was created alongside the consolidated base specification during the same consolidation that merged the four companion documents into `chapar.md`.
- Its procedures were derived and authored as an imperative restatement of behavior that was already normative in the spec (switch frame processing, endpoint Unicast sending, Discovery participation, ChaparKhane path composition, and known failure modes); the file introduces no new semantics, so the base document required no change.

#### Deliberation
- The four-file structure was specified as part of migrating the Chapar documentation to the current method (Omid Hekayati).

### Rewrote the Introduction's Motivation/Methodology split and resolved ambiguities by expansion
- Time: 2026-08-26T06:11:59Z
- Type: revised
- Cited:
  - [Documentation — Explanation](../documentation-explanation.md) — Reference: its definitions of Motivation (the problem/friction) and Methodology (how the content was actually arrived at) governed the rewrite and the boundary between the two sections.
- Propagates to:
  - chapar.practice.md: Rejected — this revision changed ordering, Introduction prose, and rationale expansions only; no normative statement the procedures restate was altered.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested, reviewed
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote

#### What changed
- Methodology was rewritten from a documentation-production narrative (which belonged in this changelog and is now only here) into the design-inquiry narrative it should have been: decomposing what any data-link switching scheme must decide — where forwarding knowledge lives, how a sender bootstraps its first path, what bounds a frame's lifetime — and studying where Ethernet/datagram switching, circuit switching (telephone exchanges, ATM, Frame Relay), and flood-based ad hoc route discovery each place that knowledge; Chapar's design is presented as the synthesis of those placements, checked numerically against topology-capacity and header-cost figures.
- Motivation now carries only the frictions (per-switch state in Ethernet, reachability bootstrap cost, rules-without-goals ambiguity, the recurring reviewer questions), keeping an explicit boundary against Methodology.
- Topic order was critically reviewed; the placement of Why "Chapar" ahead of terminology scope (defining ChaparKhane before first use) was confirmed, and the remaining sequence was kept as dependency-sane.
- Ambiguities were resolved by adding explanation, never by compressing: concrete header-length arithmetic including the Broadcast exception to "Hop Count indicates frame length"; the structural-support vs. usage-policy distinction behind the Frame types paragraph; the delivery-guarantee consequences of Blocking vs. Non-blocking Switching and their tie to Discovery refresh; why Broadcast must reserve the full hop-port space (in-place rewrite containment); what junction problem the virtual-switch-hop rule solves; who re-announces after a topology change; and header-cost arithmetic aligned with the four-fixed-field layout (~20 bytes at sixteen hops, inside Ethernet's 14–22-byte span).

#### Deliberation
- Methodology was to describe how the problem was studied in Ethernet and other protocols rather than the documentation-production process (Omid Hekayati).
- A critical ordering review was asked for (Omid Hekayati).
- Ambiguities were to be resolved with more explanation instead of summarization (Omid Hekayati).

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
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — applied

#### What changed
- Three rulings from critical review were applied.
- Periodicity was removed from Discovery everywhere it appeared: membership is silent by default; a device announces at join time and again only when an upper-layer timeout indicates a dead path, so Broadcast remains genuinely rare and the standing-load objection to the no-deduplication judgment collapses.
- The composition paragraph now states that a composed Path(D1→D2) carries both legs inside the single 255-hop header budget, capping coordinated pairing reach while leaving single-legged coordinator contact at the full range.
- Terminal behavior became normative in Rules — Next Hop is a moving index advanced past each switch's stamped position; frames whose next hop is exhausted or whose indicated port is missing/down are dropped silently; stray Broadcast copies are dropped — with recovery explicitly delegated to upper-layer timeouts and rising drop rates delegated to watching layers as misbehavior signals.
- The pending additions recorded under Propagates to were drafted.

#### Deliberation
- It was ruled that devices are silent by default: announcement at join, re-announcement only on failure indication (Omid Hekayati).
- Documenting the composition hop cap and the terminal-semantics rules was approved (Omid Hekayati).
- The identity-binding critique was rebutted as a universal layering property rather than a Chapar-specific dependency (Omid Hekayati).

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
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — applied

#### What changed
- The core correction was written in as an architectural principle: a Chapar header appears only where a link feeds a switching function.
- A point-to-point association may carry layer 1 plus upper-layer framing with no Chapar header at all — packets going straight from medium to layer 3 — so small-frame media remain fully usable in directly-attached roles, and the ~260-byte Broadcast form is required only on media hosting shared, flooded segments.
- Discovery was scoped accordingly: broadcast flooding joins shared multi-node segments; devices attached to their coordinator through a dedicated association register directly via sRPC, as a phone attaches to a cell tower without introducing itself to other phones.
- The stable-identity boundary was added to Discovery with the framing demanded — it is a universal layering property shared with Ethernet (ARP, then names/directories above MAC), not a dependency Chapar uniquely introduces.
- The depth comparison gained a full paragraph stating that shallow-to-medium depth is where every practical layer-2 technology lives, that both protocols hand off to layer 3 beyond it, that the difference is economic (cheaper, lower-power switches reaching the same hand-off), and that deep dynamic meshes belong above this layer — where Chapar's Discovery pattern came from.
- Two further preemptive notes were added (first-traffic-as-path-validation; header-integrity delegation to layer-1 CRCs): a freshly discovered path is validated by its first real traffic (no response exists to validate earlier), and Unicast loop-freedom holds structurally for well-formed headers while header integrity is delegated to layer-1 CRCs, since an end-to-end checksum over a rewritten-every-hop header is impossible.

#### Deliberation
- Whether layer 2 exists on a link was established as a capacity-and-role decision: a two-device wireless association carries layer 1 plus sRPC directly, registering at ChaparKhane without any layer-2 introduction — as a phone does not announce itself to other phones on its tower (Omid Hekayati).
- The identity note was approved under its universal framing (Omid Hekayati).
- The depth-scoping explanation was asked to be thorough enough to end the recurring critique (Omid Hekayati).
- Further preemptive explanations were instructed to be added wherever known (Omid Hekayati).

### Extracted the general layer-presence principle to Networking
- Time: 2026-08-26T07:33:31Z
- Type: revised
- Cited:
  - [Networking](./networking.md) — Depends_for: now owns the layer-presence principle this document references; its rewrite merged the two sibling files this document previously linked for hardware rationale.
- Propagates to:
  - networking.md: Done — principle generalized there under Layer presence; switch-class definitions and hardware rationale now owned there.
  - chapar.practice.md: Rejected — procedures restate Chapar-level behavior only; the extracted material (generic switch-class definitions, media-existence principle) was never procedural content here.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested, decided
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — applied

#### What changed
- Three pieces moved out of this document into [Networking](./networking.md), which was rewritten under the current method with the two sibling files merged in.
- First and principal: the media-existence discussion became Networking's Layer presence topic in its general form — no layer is mandatory; every layer has its own identity; presence on a link is a per-link capacity-and-role decision — with this document keeping only the Chapar application and referencing the rule.
- The generic Blocking/Non-blocking switch definitions, which had existed verbatim in both this document and the hardware file, are now owned once by Networking's Hardware topic; this document keeps the class names, the reference, and the Chapar-specific consequences (synchronous confirmation under blocking; silent-loss window and timeout-driven re-Discovery under non-blocking).
- Minor ownership attributions: the OSI packet-ordering rule is attributed to Networking's packet model, and the topology-capacity table's wireless-addressing link now points at Networking — Hardware instead of the removed hardware file.

#### Deliberation
- Part of what this document had absorbed was identified as belonging to networking generally (Omid Hekayati).
- The general form of the layer-presence principle was ruled (Omid Hekayati).
- Other protocols were directed to reference Networking rather than Chapar (Omid Hekayati).

---

### Relocated to `docs/protocols/`
- Time: 2026-09-03T00:00:00Z
- Type: refactor
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) - directed, decided
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) - moved.

#### What changed
- This document and its companions (practice, changelog) moved from `docs/` to `docs/protocols/` - the new home for Memar's own protocol specifications.
- Relative links to documentation-system documents and to Khayyam documents at `docs/` root were adjusted for the added depth; no content change.

#### Deliberation
- Memar's own protocol specifications are collected in `docs/protocols/`, so a reader (or agent) needing only to *use* an implementation goes to the implementing repository instead of loading specification documents; this document is a protocol specification and moved with its siblings (Omid Hekayati).

---

### Second migration wave: `## Discussion` retired per the finalized method
- Time: 2026-09-08T00:00:00Z
- Type: refactor
- Propagates to:
  - chapar.handoff.md: Created - open questions and anticipated work moved there.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) - requested
  - [OpenCode](../../CONTRIBUTORS.md#opencode) (qwen3.8-flash) - moved

#### What changed
- The body's fixed top-level sections are now `Abstract`, `Introduction`, `Explanation`, `Results` only: the document-level `## Discussion` and all five topic-level `#### Discussion` wrappers (Frame types, Discovery, Rules, Goals and Non-Goals, State model compared with Ethernet) are retired; no `Discussion`, `Drawbacks`, `Rationale and alternatives`, `Prior art`, `Unresolved questions`, or `Future possibilities` wrapper heading survives in the body.
- Premise evidence and current-state consequences were folded inline at the claims they support: the path-acquisition gap Discovery answers (with the non-uniqueness-versus-Ethernet point and the fixed well-known announcement `StreamID`) at the head of Discovery; the coordinator-presupposition cost of the Broadcast usage-policy placement at Frame types; the upper-layer-timeout staleness delay, first-traffic-as-path-validation, and the deliberate ChaparKhane centralization of device-to-device pairing at Discovery; the assumptions qualifier of the numeric comparisons at State model compared with Ethernet; the Ethernet multi-path performance-penalty premise at Goals and Non-Goals.
- Two open questions and the document-level split question — Discovery response authenticity with its trust-anchor sub-question, the unsourced CAM-ceiling figure, and whether this document should be split again if its length becomes a real reading burden — moved to the paired handoff's Open Questions; the topic and document-level Future possibilities items (ChaparKhane path-directory document, Discovery signed-response document, Non-Goal follow-up documents, empirical header-cost comparison, classification-debate link rule, high-frequency-Broadcast re-evaluation trigger, topic spin-out rule) moved there as Anticipated Work.
- The retired wrappers' rejected alternatives and decision rationale — the Broadcast restriction's two reasons and its two rejected alternatives, the judgment-call drawback, Discovery's one-way design, MAY/MUST placement, uncoupled-reaction rationale and two rejected alternatives, the Rules encoding/rewrite/reservation/virtual-hop/no-checksum rationale, the Non-Goal absorption rejection, the comparison-placement rationale, and the consolidation-era alternatives — are preserved below under Considered and not done.
- The four comparative prior-art blocks (Ethernet broadcast-storm prevention, AODV reverse-path learning, ARP-plus-MAC-learning, the systems-and-standards list behind the design, segment/source routing) are preserved below under Related work.
- Verified graduated, not copied: the Rules wrapper's closing claim (the port-rewrite rule is what makes Discovery's reverse-path accumulation and Misbehavior traceability fall out of ordinary forwarding for free) is already carried by Discovery ("falls directly out of a rule the protocol needed anyway, not a new mechanism bolted on") and Misbehavior traceability ("every switch already performs the relevant work as an unavoidable part of ordinary forwarding, not as an optional add-on"); the Discovery wrapper's pull/push/both scope note is already carried by the body's Discovery composition paragraph; and the document-level `Rationale and alternatives` bullets for keeping the four companion files separate and for merging all rationale into one separate file were verified as already recorded in this file's first entry — dropping them from the body loses nothing.
- The Abstract, the Introduction's Motivation and Methodology close, and the Frame types policy pointer now reference the paired changelog and handoff where the rationale now lives, replacing the only stale textual references to the retired `Discussion` bundles; no hyperlink in the body or in any other document pointed at the retired sections' anchors, so no link repointing was needed.
- Final audit pass: `chapar.practice.md`'s front-matter description no longer refers to chapar.md's Discussion bundles (retired); it now points to the paired changelog and handoff.

#### Considered and not done
- **Broadcast beyond discovery and emergency — the restriction's reasons (rationale; migrated from the Frame types topic's retired `Rationale and alternatives`)**: Broadcast in Chapar is meant for exactly two things — a new device announcing itself to find a coordinator, and emergency signaling — and explicitly not for general content distribution (e.g., streaming video to many recipients on a segment). Two independent reasons. **Privacy**: broadcasting general content to every node on a segment lets any node infer another node's activity — what is being watched, when it is paused or resumed, and so on — a form of surveillance the design rejects as a leftover assumption from physical-world broadcast constraints (e.g., a stadium crowd watching one shared screen) that a digital network is not obligated to repeat; content genuinely meant for many recipients should be delivered as distinct application-layer streams, not layer-2 broadcast. **Bounded, non-persistent cost**: every frame — including Broadcast — carries an explicit HopCount and forwarding path, so a duplicated Broadcast frame in a redundant topology is bounded by the hop limit and dropped as a stray frame once it reaches the end of its path; it cannot persist or re-circulate indefinitely — materially, and much more cheaply, than an unresolved forwarding loop in a protocol without a hop bound, where a stray frame can remain alive in the network indefinitely and add to cumulative processing load with every subsequent frame like it; given how rare legitimate Broadcast use is (device discovery, emergencies), this bounded duplication cost was judged not to be worth a dedicated mitigation (e.g., a new header field), and no design was found where such a field's cost would be justified against how infrequently it would matter. Misuse of Broadcast beyond these rare, intended scenarios is a runtime/security policy concern for ChaparKhane or the network operator to detect and enforce (e.g., raising an intrusion alert), not a defect of the Chapar protocol layer to prevent structurally — see [Misbehavior traceability](./chapar.md#misbehavior-traceability) for why this detection is structurally cheaper in Chapar than the equivalent in Ethernet.
- **A dedicated Broadcast de-duplication mechanism (rejected; migrated from the Frame types topic's retired `Rationale and alternatives`)**: switches remembering recently seen FrameIDs to eliminate Broadcast duplication in redundant topologies entirely — this reintroduces per-switch state, directly contradicting the stateless-switch goal, for a cost (bounded, rare duplication) that was judged not to justify it.
- **Forbidding redundant/multi-link topologies (rejected; migrated from the Frame types topic's retired `Rationale and alternatives`)**: avoiding the duplication scenario altogether — rejected because multi-link topologies are explicitly used elsewhere in the spec to increase host capacity (see [Topology capacity examples](./chapar.md#topology-capacity-examples)), so forbidding them would conflict with a stated goal.
- **Leaving path acquisition undescribed by the specification (rejected; migrated from the Discovery topic's retired `Motivation`)**: earlier review of the spec flagged a real gap — nothing in the protocol described how an endpoint obtains the hop-port sequence it is required to place in every Unicast frame's header. Without an answer, "stateless switching" and "source routing" are individually well-specified but the system as a whole is not — a device would have no way to send its first frame at all. The gap is not unique to Chapar: Ethernet devices resolve the equivalent problem via ARP (address to MAC) plus each switch's own MAC-learning, so path establishment is not a novel cost Chapar introduces — only Chapar's mechanism for it needed to be written down; the premise now leads the Discovery topic and the review narration is recorded here.
- **A two-way (request/response) Discovery (rationale for one-way; migrated from the Discovery topic's retired `Rationale and alternatives`)**: Discovery is one-way by design — as an sRPC service call it is request-only and defines no response. A device announcing itself is not opening an RPC exchange that something must complete; it is closer to a self-timed, event-driven broadcast, sent at join time and again only on an upper-layer failure indication; every announcement is identical whether it is the device's first or a refresh, and any interested party may act on it or ignore it; a fixed, well-known `StreamID` (e.g. `0`) is enough for this, precisely because there is no reply expected on that stream to disambiguate.
- **Making reaction to Discovery mandatory for all nodes (rationale for the MAY/MUST split; migrated from the Discovery topic's retired `Rationale and alternatives`)**: the split (any node may react; ChaparKhane must) is a deliberate policy placement — reacting is optional and a policy decision for ordinary nodes, while the network's mandatory coordinator always reacts, guaranteeing every completing device acquires at least one usable path.
- **Discovery reactions as coupled RPC responses (rationale for the independent-Unicast design; migrated from the Discovery topic's retired `Rationale and alternatives`)**: reacting means independently initiating its own new contact with the new device — a fresh Unicast frame using the accumulated hop-port sequence, reversed, as the path — rather than sending a coupled RPC response on the announcer's stream. This distinction matters: the general sRPC mechanism for disambiguating multiple same-`StreamID` responses to a broadcast (by pairing `StreamID` with the sender's reverse-path address) is not actually needed for Discovery's own announcement stream, since Discovery never has a reply on that stream to disambiguate in the first place — any reaction to it is its own, separately-identified communication. That general sRPC mechanism may still matter for other broadcast scenarios; that is a question for sRPC's own documentation, not this document.
- **A dedicated route-computation and distribution protocol for ChaparKhane (rejected; migrated from the Discovery topic's retired `Rationale and alternatives`)**: giving ChaparKhane a link-state or distance-vector style protocol instead of relying on broadcast-flood reverse-path accumulation — rejected for the common case: it would reintroduce meaningful state and a separate control protocol for a problem the existing port-rewrite rule already solves for the primary case (reaching a coordinator).
- **FrameID caching to deduplicate the Discovery flood (rejected; migrated from the Discovery topic's retired `Rationale and alternatives`)**: requiring every switch to cache recent FrameIDs — rejected because it reintroduces per-switch state, and the duplication cost during the rare Discovery event is already addressed as acceptable in [Frame types](./chapar.md#frame-types).
- **Recording open questions at the Chapar layer for the core Discovery mechanism (resolved: none remain; migrated from the Discovery topic's retired `Unresolved questions`)**: none remain at the Chapar layer for the core mechanism; two related items are explicitly out of scope rather than unresolved — the specific `ServiceID` values for Discovery and Emergency belong to sRPC's service registry, not this document, and whether ChaparKhane offers path lookup as pull, push, or both is a ChaparKhane service-design decision, not a Chapar protocol one (already stated in the body). The genuinely open item — Discovery response authenticity and its trust-anchor sub-question — moved to the paired handoff's Open Questions.
- **A dedicated Broadcast field for HopCount (rationale for the sentinel encoding; migrated from the Rules topic's retired `Rationale and alternatives`)**: since a Unicast frame must have at least one hop, `0x00` would otherwise be unused by Unicast, so it is repurposed as the Broadcast sentinel instead of adding a dedicated field.
- **A Broadcast header without declared-next-port freedom (rationale for the port-rewrite rule; migrated from the Rules topic's retired `Rationale and alternatives`)**: the port-rewrite rule exists for three reasons — BroadcastFrame: to improve performance, the previous switch just sends a frame without declaring the next port; UnicastFrame: to be sure receive port is the same with declaration one in a frame; Rule&Security: to be sure the physical network port is the same on the sender and receiver switch.
- **A partial hop-port reservation for Broadcast frames (rationale for reserving the full space; migrated from the Rules topic's retired `Rationale and alternatives`)**: the rewrite happens in place, as an unavoidable side effect of forwarding — a receiving switch stamps its arrival port into the frame without negotiating with anyone about where writing is allowed. On a flooded Broadcast every traversed switch stamps, so the frame must arrive carrying room for the worst case: the full 255 zero-filled slots. If a Broadcast reserved less than the whole space, some switch's mandatory rewrite would eventually fall outside the reserved area and manipulate whatever bytes follow it in the packet — which belong to other frames' data; reserving the whole space converts that hazard into harmless zero-fill.
- **A header carrying junction-mismatched port numbers without an extra logical hop (rationale for the virtual-switch-hop rule; migrated from the Rules topic's retired `Rationale and alternatives`)**: two peers each number their own physical ports independently, so when they connect directly, the port number one declares and the port number the other actually uses do not correspond. A path crossing that junction needs one extra, purely logical hop — the virtual switch hop, added by the adaptor side (usually the higher-hop side of the composed path) — so both halves of the path stay expressible in the same one-byte-per-hop format; the cost is exactly one additional hop-port byte on every Chapar frame crossing the junction. [Discovery](./chapar.md#discovery)'s device-to-device path composition joins two paths across precisely this kind of mismatched boundary at ChaparKhane, using this same rule.
- **An end-to-end header checksum (rationale for delegation to layer-1 CRCs; migrated from the Rules topic's retired `Rationale and alternatives`)**: an end-to-end header integrity field is impossible over a header that every hop rewrites in place — the sender could never predict the bytes a receiver would check. Integrity is therefore delegated downward, to layer-1 frame CRCs, which discard corrupted media frames before they become a Chapar concern. Given a well-formed header, Unicast loop-freedom is structural — the port sequence is finite and fixed; corruption severe enough to forge a cycle is caught below this layer, and a rising rate of malformed drops is treated as misbehavior (see [Misbehavior traceability](./chapar.md#misbehavior-traceability)). (This rule is also what makes [Discovery](./chapar.md#discovery)'s reverse-path accumulation and [Misbehavior traceability](./chapar.md#misbehavior-traceability) fall out of ordinary forwarding for free, with no additional mechanism — already carried by those body topics.)
- **Absorbing Non-Goals into Chapar (rejected; migrated from the Goals and Non-Goals topic's retired `Rationale and alternatives`)**: absorbing one or more Non-Goals directly into Chapar (e.g., built-in QoS or multi-path support) — rejected in each case for the same underlying reason: doing so would require some form of per-switch state, which conflicts with the core stateless-switching goal this protocol exists to achieve.
- **Keeping the Ethernet comparison interleaved with the normative rules (the earlier layout; rejected; migrated from the State model topic's retired `Rationale and alternatives`)**: interleaving forced every reader of the rules to also evaluate an argument about a different protocol before understanding Chapar's own mechanics; keeping the comparison as its own topic keeps the rules clean while retaining the comparison.
- **Dropping the Ethernet comparison entirely (rejected; migrated from the State model topic's retired `Rationale and alternatives`)**: the motivating "why" for several protocol decisions (no CAM dependency, source routing) is meaningfully clearer with the comparison than without it.
- **Keeping the pre-consolidation five-document structure unchanged (rejected; migrated from the removed document-level `Rationale and alternatives`)**: it was the older documentation method the consolidation migrated away from; the record of that migration lives in this changelog, not in the base document's body.

#### Considered and not done (from the removed document-level Drawbacks section)
- Consolidating the specification and all of its rationale into one document makes the file long, and a reader seeking one specific piece of rationale must load the whole document. The mitigating factors are structural: the normative text is concentrated in each topic's leading statements and in the first half of the document, every `Discussion` bundle is skippable without losing normative content, and heading navigation reaches any topic directly.
- "Bounded duplication is acceptable because it's rare" is a judgment call, not a proof; a future scenario with much more frequent legitimate Broadcast use (not currently anticipated) would need this trade-off re-evaluated.

#### Related work
- Broadcast storm prevention in Ethernet (e.g., Spanning Tree Protocol) solves a structurally different problem: Ethernet's forwarding loops are unbounded without it, whereas Chapar's HopCount already bounds any single frame's lifetime. (Migrated from the Frame types topic's retired `Prior art`.)
- Reverse-path learning during flood-based route discovery is used in ad hoc/mesh routing protocols (e.g., AODV-style route requests), where a broadcast request accumulates path information that a unicast reply then uses in reverse — structurally similar to the mechanism here, at a different layer. (Migrated from the Discovery topic's retired `Prior art`.)
- Ethernet's ARP (resolving a network-layer address to a MAC address) combined with per-switch MAC-learning solves the equivalent problem — a device needing a usable path to another device before it can send — by different means: a broadcast query answered directly by the target, plus stateful learning in every switch, rather than reverse-path accumulation with stateless switches. (Migrated from the Discovery topic's retired `Prior art`.)
- Chapar draws on ideas from several existing systems and standards rather than inventing every mechanism from scratch: [guifi.net](https://guifi.net/) — community-network topology and operation at scale; [Telephone exchange](https://en.wikipedia.org/wiki/Telephone_exchange) — circuit-switching heritage informing the peer/frame state model; [Fast packet switching](https://en.wikipedia.org/wiki/Fast_packet_switching); [SDU](https://en.wikipedia.org/wiki/Service_data_unit) vs [PDU](https://en.wikipedia.org/wiki/Protocol_data_unit) — framing terminology; [ETSI](https://www.etsi.org/) standards; [Asynchronous Transfer Mode](https://en.wikipedia.org/wiki/Asynchronous_Transfer_Mode) — fixed-size cell switching heritage; [IEEE 802](https://www.ieee802.org/); [Frame Relay](https://en.wikipedia.org/wiki/Frame_Relay); further background: [supporting articles](https://www.dropbox.com/sh/51l4x1p2e8lub5x/AABVgFyJ0fuia8QZt7SEZgBWa?dl=0). (Migrated from the Goals and Non-Goals topic's retired `Prior art`.)
- Segment/source routing in general (e.g., IPv6 Segment Routing, MPLS explicit paths) trades per-hop state for path information carried in the packet — a similar state-location trade-off to Chapar's, at a different layer. (Migrated from the State model topic's retired `Prior art`.)
