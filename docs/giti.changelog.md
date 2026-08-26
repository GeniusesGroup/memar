# Giti (GP) Changelog

## Changelog

### Rewrote under the current method, merging the legacy vision read-me into the protocol specification
- Time: 2026-08-26T09:13:01Z
- Type: merged
- Cited:
  - [Documentation — Explanation](./documentation-explanation.md) — Reference: the Explanation-facet structure this rewrite follows, including its prefix-free/layer-free file-naming rule that decided the filename.
  - [Networking](./networking.md) — Depends_on: GP frames ride Networking's packet model; the self-describing-frame and Layer presence principles are referenced rather than restated.
  - [Chapar - Data Link Protocol](./chapar.md) — Reference: supplies the ChaparKhane router/coordinator role and the link-layer carrier this document suggests.
- Propagates to:
  - networking-osi_3-Giti-Network.md: Done — all content merged here; file removed.
  - giti.md (legacy read-me): Done — this very file was the second source; its entire content is merged and superseded by this rewrite.
  - networking.md: Done — Frames topic example link and registry row 4 repointed to this document.
  - sRPC.md: Done — GP example link repointed.
  - README.md (repository root): Done — GP link repointed to `./docs/giti.md`, which also repairs its previously broken relative path.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: directed the migration of this protocol to the current method and asked for an explicit ruling on the filename (prefix removal vs. umbrella prefix vs. keeping the OSI-layer reference).
  - [ox-alpha](../CONTRIBUTORS.md#ox-alpha) — rewrote: recommended and applied `giti.md`, performed the consolidation.

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
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided: ruled that documentation-production history belongs to this changelog, not the base document's Methodology (which now tells how the protocol design was actually reached); and defined the commercial statement — ChaparKhane and Achaemenid are intended commercial software from Geniuses Group, unexplained mentions exist for that reason, organizations stay free to build their own implementations on the open protocols, but support rather than self-implementation is the path that speeds Memar's development.
  - [ox-alpha](../CONTRIBUTORS.md#ox-alpha) — applied.

#### Summary
Methodology was replaced: the consolidation story (already recorded here in the previous entry) left the base document, and the section now records the design's actual origin — the inversion of IP's unit of connection from devices to applications, the derivation of the five-level address hierarchy from global application-to-application routing without a registrar, and IPv6 as the standing measuring stick each mechanism had to answer. The commercial clarification was authored into Networking under Commercial components and referenced from this document's stack-placement paragraph and the repository root README.

### Recorded the deliberate openness of enforcement design and the layering scope of interplanetary claims
- Time: 2026-08-26T10:14:15Z
- Type: revised
- Propagates to:
  - README.md (repository root): Done — Commercial components content moved into README's existing Enterprise section; this document's pointer repointed there.
  - networking.md: Done — its temporary Commercial components topic removed; ownership of the statement now belongs to README.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided: relocated the commercial statement from Networking to README's Enterprise section; ruled that GP deliberately fixes no definitive identity-attestation or blocking method so creativity is not foreclosed, while correcting the critique's framing — IPv4/IPv6 has no accountability path at all (origins dissolve behind VPNs), whereas GP's router ranges have identifiable organizational owners and the mandatory services exist precisely to exercise that accountability; confirmed that interplanetary reach is an addressing/routability claim whose delivery belongs to lower layers; and elevated the mandatory sRPC services to first-priority open work as the carrier of the whole accountability model. QoS scheduling likewise left unspecified as a ChaparKhane implementation concern.
  - [ox-alpha](../CONTRIBUTORS.md#ox-alpha) — applied.

#### Summary
Five revisions. The stack-placement pointer now targets README's Enterprise section, which absorbed the full commercial-components statement (and shed a dangling empty bullet). Attack reporting gained its governing stance: no definitive attestation/blocking scheme is fixed on purpose, with GP's structural advantage over IP recorded — organizational ownership of Router ranges makes reports terminate at accountable parties where IP's origins dissolve behind VPNs. Standard services were elevated: they carry attack reporting, reputation, blocking coordination, and identity attestation, making them the highest-priority open work. Routing architecture opens with a scoping note — this layer owes addressing and routability only; inter-planetary delivery belongs to lower layers and topology. Quality of Service points at ChaparKhane as the deliberately-unspecified implementation home. Unresolved question 2 was reframed accordingly: binding remains open by choice, with the gap explicitly smaller than IPv6's rather than inherited-equal.

### Recorded the society-blocking via de-peering design as a future option
- Time: 2026-08-26T19:21:44Z
- Type: added
- Propagates to:
  - None — this is a future direction recorded for the first time.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — ruled: the de-peering + signed reputation design is recorded as a future option, not a fixed method, consistent with the deliberate openness of enforcement design.
  - [ox-alpha](../CONTRIBUTORS.md#ox-alpha) — wrote.

#### Summary
Added the society-level blocking design to Future possibilities: de-peering via route withdrawal (BGP-style, simplified by small deliberately-peered society graph), signed incident reports carried on mandatory sRPC services with Chapar-stamped evidence, VPN bypass structural failure because egress lands in an identifiable org-owned range, graduated escalation (warn → rate-limit → partial/full withdrawal → re-entry via signed attestation). Recorded as an option, not a fixed rule, consistent with the deliberate openness stance.

### Expanded the society-blocking de-peering design to full detail
- Time: 2026-08-26T19:27:05Z
- Type: revised
- Propagates to:
  - None — future direction expanded in place.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — ruled: the abbreviated bullet did not do justice to the discussed design; the full two-tier consensus, VPN bypass explanation, and graduated escalation must be recorded.
  - [ox-alpha](../CONTRIBUTORS.md#ox-alpha) — applied.

#### Summary
Replaced the abbreviated bullet with the full design: two-tier consensus (intra-society agreement then inter-society propagation), structural VPN bypass failure explanation (egress through identifiable org-owned range), graduated escalation (warn → rate-limit → partial/full withdrawal → re-entry), and the two-tier consensus model matching the owner's description. Still recorded as an option, not a fixed rule.
