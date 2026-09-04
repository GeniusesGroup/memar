# Giti (GP) Changelog

## Changelog

### Rewrote under the current method, merging the legacy vision read-me into the protocol specification
- Time: 2026-08-26T09:13:01Z
- Type: merged
- Cited:
  - [Documentation — Explanation](../documentation-explanation.md) — Reference: the Explanation-facet structure this rewrite follows, including its prefix-free/layer-free file-naming rule that decided the filename.
  - [Networking](./networking.md) — Depends_on: GP frames ride Networking's packet model; the self-describing-frame and Layer presence principles are referenced rather than restated.
  - [Chapar - Data Link Protocol](./chapar.md) — Reference: supplies the ChaparKhane router/coordinator role and the link-layer carrier this document suggests.
- Propagates to:
  - networking-osi_3-Giti-Network.md: Done — all content merged here; file removed.
  - giti.md (legacy read-me): Done — this very file was the second source; its entire content is merged and superseded by this rewrite.
  - networking.md: Done — Frames topic example link and registry row 4 repointed to this document.
  - sRPC.md: Done — GP example link repointed.
  - README.md (repository root): Done — GP link repointed to `./docs/giti.md`, which also repairs its previously broken relative path.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested: directed the migration of this protocol to the current method and asked for an explicit ruling on the filename (prefix removal vs. umbrella prefix vs. keeping the OSI-layer reference).
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote: recommended and applied `giti.md`, performed the consolidation.

#### Summary
The protocol documentation previously lived in two pre-method files: the original Giti read-me (`giti.md` — vision, stack overview, societies, security posture, transition plan, related-work lists) and the GP specification (`networking-osi_3-Giti-Network.md` — goals, frame format, addresses, routing architecture). Both were undated and carried dead links. The two were consolidated into this single Explanation-facet document without summarization, with every design statement preserved and IPv6 kept as the recorded measuring stick. The filename question was resolved per the current method's own rule (`<slug>.md`, no number, no domain prefix) and for consistency with the Layer presence principle — a layer number in a filename would encode exactly the fixed-layer assumption that principle rejects — giving `giti.md`, parallel to `chapar.md`; umbrella-prefixing Chapar under networking was rejected on the same rule. Repairs made in passing: the `ChaparKhane.md` links (a document that never existed) now point at the ChaparKhane role's home in chapar.md; the `chapa.md` typo became chapar.md; `PersiaOS.md` case-corrected to persia_os.md; the legacy "Transport (OSI Layer 3)" mislabel corrected to Network; the dangling Achaemenid links replaced with a plain-text mention and an Unresolved questions entry since no such document exists; the empty standard-services roster flagged inline and as an open question alongside the unrecorded ownership-proof mechanism for the true 32-byte identities — the latter noted as especially pressing because two of the document's own IP criticisms target that exact weakness.

### Rewrote Methodology as design-origin narrative and pointed at the commercial-components statement
- Time: 2026-08-26T09:36:34Z
- Type: revised
- Cited:
  - [Networking](./networking.md) — Depends_for: owns the new Commercial components topic this document points at.
- Propagates to:
  - networking.md: Done — the authoritative Commercial components topic added there.
  - README.md (repository root): Done — one-sentence pointer to that topic added.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided: ruled that documentation-production history belongs to this changelog, not the base document's Methodology (which now tells how the protocol design was actually reached); and defined the commercial statement — ChaparKhane and Achaemenid are intended commercial software from Geniuses Group, unexplained mentions exist for that reason, organizations stay free to build their own implementations on the open protocols, but support rather than self-implementation is the path that speeds Memar's development.
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — applied.

#### Summary
Methodology was replaced: the consolidation story (already recorded here in the previous entry) left the base document, and the section now records the design's actual origin — the inversion of IP's unit of connection from devices to applications, the derivation of the five-level address hierarchy from global application-to-application routing without a registrar, and IPv6 as the standing measuring stick each mechanism had to answer. The commercial clarification was authored into Networking under Commercial components and referenced from this document's stack-placement paragraph and the repository root README.

### Recorded the deliberate openness of enforcement design and the layering scope of interplanetary claims
- Time: 2026-08-26T10:14:15Z
- Type: revised
- Propagates to:
  - README.md (repository root): Done — Commercial components content moved into README's existing Enterprise section; this document's pointer repointed there.
  - networking.md: Done — its temporary Commercial components topic removed; ownership of the statement now belongs to README.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided: relocated the commercial statement from Networking to README's Enterprise section; ruled that GP deliberately fixes no definitive identity-attestation or blocking method so creativity is not foreclosed, while correcting the critique's framing — IPv4/IPv6 has no accountability path at all (origins dissolve behind VPNs), whereas GP's router ranges have identifiable organizational owners and the mandatory services exist precisely to exercise that accountability; confirmed that interplanetary reach is an addressing/routability claim whose delivery belongs to lower layers; and elevated the mandatory sRPC services to first-priority open work as the carrier of the whole accountability model. QoS scheduling likewise left unspecified as a ChaparKhane implementation concern.
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — applied.

#### Summary
Five revisions. The stack-placement pointer now targets README's Enterprise section, which absorbed the full commercial-components statement (and shed a dangling empty bullet). Attack reporting gained its governing stance: no definitive attestation/blocking scheme is fixed on purpose, with GP's structural advantage over IP recorded — organizational ownership of Router ranges makes reports terminate at accountable parties where IP's origins dissolve behind VPNs. Standard services were elevated: they carry attack reporting, reputation, blocking coordination, and identity attestation, making them the highest-priority open work. Routing architecture opens with a scoping note — this layer owes addressing and routability only; inter-planetary delivery belongs to lower layers and topology. Quality of Service points at ChaparKhane as the deliberately-unspecified implementation home. Unresolved question 2 was reframed accordingly: binding remains open by choice, with the gap explicitly smaller than IPv6's rather than inherited-equal.

### Recorded the society-blocking via de-peering design as a future option
- Time: 2026-08-26T19:21:44Z
- Type: added
- Propagates to:
  - None — this is a future direction recorded for the first time.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — ruled: the de-peering + signed reputation design is recorded as a future option, not a fixed method, consistent with the deliberate openness of enforcement design.
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — wrote.

#### Summary
Added the society-level blocking design to Future possibilities: de-peering via route withdrawal (BGP-style, simplified by small deliberately-peered society graph), signed incident reports carried on mandatory sRPC services with Chapar-stamped evidence, VPN bypass structural failure because egress lands in an identifiable org-owned range, graduated escalation (warn → rate-limit → partial/full withdrawal → re-entry via signed attestation). Recorded as an option, not a fixed rule, consistent with the deliberate openness stance.

### Expanded the society-blocking de-peering design to full detail
- Time: 2026-08-26T19:27:05Z
- Type: revised
- Propagates to:
  - None — future direction expanded in place.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — ruled: the abbreviated bullet did not do justice to the discussed design; the full two-tier consensus, VPN bypass explanation, and graduated escalation must be recorded.
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — applied.

#### Summary
Replaced the abbreviated bullet with the full design: two-tier consensus (intra-society agreement then inter-society propagation), structural VPN bypass failure explanation (egress through identifiable org-owned range), graduated escalation (warn → rate-limit → partial/full withdrawal → re-entry), and the two-tier consensus model matching the owner's description. Still recorded as an option, not a fixed rule.

### Redesigned the address and frame architecture: Planet removed from addressing, two routing frames, capacity-derived widths
- Time: 2026-08-31T17:29:51Z
- Type: revised
- Cited:
  - [Networking](./networking.md) — Depends_on: the two GP frame types are registered there (4 GP-Thing, 5 GP-App); the self-describing-frame rule is what lets a FrameType announce its own address layout.
  - [Chapar - Data Link Protocol](./chapar.md) — Reference: supplies the physically-adjacent-hop carriage model that inter-society delivery sits one abstraction above.
- Propagates to:
  - networking.md: Done — registry row 4 renamed GP-Thing, row 5 added as GP-App; Edge computing topic added.
  - README.md (repository root): Rejected — no statement outside the protocol documents depends on the address layout.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested, decided: opened the critique that GP was doing several jobs at once and paying real runtime cost for it; ruled through a full design review that (a) planetary location is reachability/topology knowledge about a society, not destination identity, so Planet left the address entirely; (b) Thing-level and App-level delivery are two different destination concepts, realized as two independent self-contained frames, with single-application devices addressed at Thing level and no App bytes ever paid; (c) field widths follow operational capacity of scope, not IPv6-inherited total address size — Thing ID reduced to 2 bytes (65,536 Things per router; ≈2⁴⁸ Things per society via hierarchy composition); (d) inter-society reachability is evaluated at Society + Router granularity, direct delivery is the encouraged norm, single mediation is legitimate with last-delivering-society responsibility, longer chains costly and discouraged, and physical hops never conflated with inter-society responsibility hops; (e) source addresses are never dropped — they ground reply addressing and accountability; (f) the standard-services roster is filled with reachability coordination, source validation, incident reporting to Router plus society authority, and router accountability — all as sRPC service calls, no GP control frame types.
  - [ChatGPT](../../CONTRIBUTORS.md#chatgpt) — collaborated: partner model in the design review; contributed the data-plane/control-plane and locator/identity separations, the per-intermediary information-need framing (which intermediary needs which field), the "rare capability must not tax the common path" principle that decided Planet's removal, the Source-must-stay argument, the ingress-vs-origin distinction behind source validation, and the last-deliverer responsibility model.
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — applied: drafted all document revisions from the review's conclusions and this document's edits.

#### Summary
The address stopped being a fixed 128-bit five-level blob inherited (through IPv6's example) before its capacity was questioned, and became a locator hierarchy whose every field is justified by its scope's operational capacity. Frame architecture: one 21-byte Thing Routing Frame (Society + Router + Thing per side) and one 25-byte App Routing Frame (Society + Router + Thing + App per side), self-contained and never rewritten in flight, with the FrameType announcing the layout. GP address topic rewritten around the locator-not-identity principle and the sizing rule; a dedicated topic records that planetary location is society-level topology knowledge, never address data, so interplanetary reachability is a routing problem rather than an addressing dimension. IPv6-comparison section rewritten: the old IANA /16 interoperation contract is dropped as unnecessary (Internet interoperation is packet-level tunneling, noted in the Transition topic). Society registration gained the logical-routing-domain statement (routers anywhere, no layer-2 adjacency required). Standard services roster filled with four named capabilities as sRPC calls — resolving the long-standing empty-roster debt. Routing architecture gained the Inter-society delivery topic (direct vs. mediated, Society+Router granularity, last-delivering-society responsibility, physical-vs-responsibility hop distinction). Local network rewritten to state honestly that router-less networks cannot back their locators. Attack reporting references the two-recipient model. Unresolved questions re-rostered: contract-level service specification, ingress attestation for source validation, and the mixed-level (Thing↔App) communication ruling replace the resolved roster and IANA questions; a scope-implied-short-frames extension point recorded under Future possibilities.

### Added Edge computing as a Networking-level architectural principle
- Time: 2026-08-31T17:29:51Z
- Type: added
- Propagates to:
  - giti.md: Done — its Frame architecture topic points at this principle so header economy is never read as license for gratuitous data movement.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided: network cost is transmission plus routing plus state; GP's small headers must never be read as removing the obligation to keep data, processing, and storage local where locality reduces total cost; recorded at Networking level because it is an architecture-wide principle, not a GP packet property.
  - ChatGPT — collaborated: shaped the principle's placement and its non-mandate formulation (enable and incentivize locality; force no topology).
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — applied.

#### Summary
New topic under Hardware in networking.md: total network cost is the sum of transmission, routing, and state, so minimizing a header is not minimizing the network; data movement must be justified, execution and storage belong at the edge where locality pays, the ecosystem's tooling should make the local choice the easy choice, and no topology is imposed on applications. GP's frame architecture cross-references it.

### Applied the owner's follow-up rulings: practice split, stack relocation, allocation service, mixed-level resolution
- Time: 2026-08-31T19:26:46Z
- Type: revised
- Cited:
  - [Giti — Practice](./giti.practice.md) — Extends_by: the Internet-bridge procedure moved out of this document now lives there as the Practice facet.
  - [Networking](./networking.md) — Depends_on: owns the Place in the stack overview this document no longer restates.
  - [OS](./os.md) — Reference: its unikernel reading (the hypervisor and drivers as parts of the system; an OS image as an app binary) grounds the mixed-level communication resolution.
- Propagates to:
  - giti.practice.md: Done — created; the Transition from the Internet topic's procedure restated as steps.
  - networking.md: Done — Place in the stack moved there as the stack-wide overview; this document no longer restates it.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided: the Internet-transition procedure is a practice, not protocol — it evolves over time and belongs in the Practice facet; the stack overview belongs to the parent Networking document, since Giti's own copy read as if Giti were the whole stack; a fifth standard service must record the society-identifier allocation shape (governing-app announcement → temporary range → collective agreement for permanence under conditions such as minimum active routers or bandwidth); and the mixed-level communication question resolves through os.md — the hypervisor and even the network driver are themselves independent applications that may hold App IDs, so a Thing-level endpoint is just an app that has not leased an App ID.
  - ChatGPT — collaborated: its earlier diagnosis (protocol versus architecture-concern separation) is the framing the practice split and stack relocation apply.
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — applied.

#### Summary
Four moves in one pass. Transition from the Internet left this document for giti.practice.md (with the IPv6-comparison pointer repointed and a one-line pointer left in Implementation and status). Place in the stack left for Networking, where the stack overview belongs to all protocols instead of Giti restating it as if it owned the stack; the software-router code-generation sentence stayed here in Implementation and status. The standard services roster gained Society identifier allocation as service five, fixing the allocation shape while leaving the agreement mechanism open — and the Society registration topic and Unresolved question 5 now reference it. Unresolved question 4 was rewritten from open problem to resolved principle with only the lease-default convention open: a Thing-level endpoint is its hypervisor or driver, itself an app under os.md that may hold an App ID.

### Applied the owner's second-round rulings: general practice document, local routing knowledge, app-not-user, Thing-level complaint policy
- Time: 2026-09-01T16:16:25Z
- Type: revised
- Cited:
  - [Giti — Practice](./giti.practice.md) — Extends_by: broadened from the single Internet-bridge topic into the general GP-practices document.
  - [OS](./os.md) — Depends_for: its Networking topic now answers the driver-as-app cost objection (isolation by granting, NIC-direct delivery) that this document's mixed-level ruling rests on.
- Propagates to:
  - giti.practice.md: Done — rewritten as the general GP practices document (router operation, Internet bridge, edge cases).
  - os.md: Done — Networking topic gained the cost-objection paragraph (paired entry in os.changelog.md).
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided: (a) the practice document must cover every GP-related procedure, not the Internet bridge alone, and explanatory documents must not link to it — the transmission pointers were removed from giti.md; (b) routing knowledge must stay local: no router holds global reachability state — a router knows only its direct connections, hands packets to any router of the destination society when the destination router is not directly reachable, and relays for others only under prior agreement, which surfaces the routing-economy question (how relay cost is paid) as a new Unresolved question; (c) "user" must not appear anywhere — the concept was deliberately renamed to app throughout Memar (as in os.md), so "first users" became "first apps" and service-number assignment was attributed to sRPC, not this document; (d) a Thing-level endpoint is effective precisely when the device has a default app — the driver as the application endpoint — and whether an unexpected App-level packet is merely delivered or reported as an attack is that device app's own rule, not the protocol's.
  - ChatGPT — collaborated: partner in the reviews whose conclusions these rulings apply.
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — applied.

#### Summary
Inter-society delivery was rewritten around local routing knowledge — the three-rung ladder (direct to destination router → hand-off to the destination society's router, which owns completion → agreed-intermediary relay as a contract, never a default), with the digital-economy routing-cost question recorded as Unresolved question 6. The practice document was generalized and decoupled: giti.md no longer links to it anywhere. Terminology was aligned: "first users" → "first apps"; service-number assignment moved out of GP's scope into sRPC's. Unresolved question 4 was completed per the default-app reading: the Thing-level endpoint's effective app is the driver, and the deliver-vs-report decision belongs to the device app's rules.

### Created the practice document
- Time: 2026-08-31T19:26:46Z
- Type: created
- Cited:
  - [Giti (GP)](./giti.md) — Depends_on: the transition rules giti.practice.md restates as imperative steps; it owns the protocol, the practice file owns the deployment procedure.
  - [Documentation — Practice](../documentation-practice.md) — Reference: the Practice-facet schema the practice file follows (frontmatter exactly `name` and `description`; imperative body; edge cases).
- Contributors:
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — applied.

#### Summary
Created giti.practice.md carrying the Internet-bridge procedure (listen on UDP 80; deliver the whole GP packet to the registered app's GP address only when it exists and requested Internet reachability; full App-level addresses at both ends inside the tunneled frame), restated as imperative steps with edge cases, including the honesty note that the UDP path carries no Chapar-grade ingress validation and the scaffolding note that the practice ends where native paths begin. The protocol itself keeps no copy of the procedure.

### Rewritten as the general GP-practices document
- Time: 2026-09-01T16:16:25Z
- Type: revised
- Cited:
  - [Giti (GP)](./giti.md) — Depends_on: the procedures here are imperative restatements of protocol rules giti.md deliberately leaves open (implementation choices, deployment steps).
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided: the practice document must cover every GP-related procedure rather than the Internet bridge alone — the bridge was an example, not the scope — and explanatory documents must never link to a practice document.
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — applied.

#### Summary
The document was rewritten as "GP Practices": a general procedures file for operating GP networks whose topics grow over time. It now carries the router-operation procedure (ChaparKhane role as an ordinary app holding a hardware entitlement; the Inter-society delivery ladder applied locally; the source-validation invariant; QoS/path/pipelining as free choices) alongside the Internet-bridge procedure, with shared edge cases. giti.md holds no links to this file — the protocol document states the protocol; this file states the procedures. Provenance for the practice document lives in this changelog, per the ruling that practice documents carry no changelog of their own.

### Applied the owner's third-round rulings: standard services deferred to ChaparKhane, interior routing freed, changelog consolidation
- Time: 2026-09-02T06:06:19Z
- Type: revised
- Cited:
  - [Giti — Practice](./giti.practice.md) — Extends_by: receives the interior-organization freedom as router-operation guidance.
- Propagates to:
  - giti.practice.md: Done — router procedure gained the interior-organization step; its standard-services links repointed.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided: (a) the standard-services roster must not harden at document level — which capabilities become protocol-level services and which stay ChaparKhane implementation concerns is decided when ChaparKhane itself is developed, following the IP/BGP lesson (routing left IP and grew its own protocol so the IP document never had to change; had BGP's plaintext design been fixed at the IP layer, the data-ecosystem damage would have been far harder to repair), so the roster was rewritten as capability *needs* with the decision explicitly deferred; (b) the interior-routing critique's "border router holds a table of the whole 2³² router space" reading is too strong for the protocol to prescribe — a society may create core routers that everything is handed to, and routing its own router space is a creativity-and-testing problem fitted to the society's physical realities, so the freedom was recorded in Society registration and mirrored into the practice document's router procedure; (c) practice documents carry no changelog of their own — the merged giti.practice.changelog.md was deleted and both its entries now live here (the stray file was removed in this pass).
  - ChatGPT — collaborated: partner in the reviews behind these rulings.
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — applied.

#### Summary
Standard services was restructured from a five-service roster into a five-capability needs list, with an explicit paragraph deferring the roster decision to ChaparKhane's development under the least-protocol-interference principle and the IP/BGP precedent recorded as evidence; the "first apps (`== 0`)" semantics left the document with the roster decision. Society registration gained the interior-organization freedom paragraph (border-spread or core-router concentration are examples, not rules — nothing interior changes a frame on the wire). All internal references were realigned: needs wording in the registry/accountability/UQ pointers, UQ1 rewritten around the deferral, and the practice document's router procedure gained the corresponding step. The consolidated changelog policy was completed: giti.practice.changelog.md is deleted and its two entries live here.

---

### Relocated to `docs/protocols/`
- Time: 2026-09-03T00:00:00Z
- Type: refactor
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) - directed, decided: Memar's own protocol specifications are collected in `docs/protocols/`, so a reader (or agent) needing only to *use* an implementation goes to the implementing repository instead of loading specification documents; this document is a protocol specification and moved with its siblings.
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) - moved.

#### Summary
This document and its companions (practice, changelog) moved from `docs/` to `docs/protocols/` - the new home for Memar's own protocol specifications. Relative links to documentation-system documents and to Khayyam documents at `docs/` root were adjusted for the added depth; no content change.
