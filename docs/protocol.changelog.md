# Protocol Changelog

## Changelog

### Original split from the monolithic Protocol document
- Time: 2026-06-21T00:00:00Z
- Type: Added
- Cited:
  - [Terminology](./terminology.md) — Foundation Alignment: terminology governs how concepts are understood across protocol.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued, claimed
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) (GPT-5.5) — drafted, argued
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM, high effort) — rewrote

#### What changed
Core ontological definition of Protocol; the Protocol–Process–System relationship; the Protocol–Science–Methodology connection; the critique of "standard" as third-party attestation; the diplomatic and scientific protocol examples; the methodology-based distinction between Protocol and Specification. (Omid Hekayati)

Drafted the initial text; argued for and against alternatives; incorporated revisions. (ChatGPT)

Split the original monolithic document (Protocol, Explicit Behavior Ownership, and Khayyam Rejection of Inheritance) into three focused documents; restructured this document to be purely ontological; enriched it with the Protocol–Process–System relationship (systems theory) and the Protocol–Science–Methodology connection; diversified domain examples (diplomatic, scientific, medical, legal, aviation, sports); corrected Protocol vs Standard to define standard as third-party attestation; added the methodology dimension to Protocol vs Specification; relabeled Formal Definition as a language-level illustration; strengthened the ontology candidate analysis with the process argument. (Super Z)

#### What changed
Split out of an earlier monolithic document that mixed ontological questions about Protocol with design principles about behavior ownership and language-level decisions about inheritance — a conflation that made it difficult to discuss any one topic without being pulled into the others. The Protocol portion was refined to remove all Khayyam-specific implementation details, code examples, and entity references, so the document defines Protocol as a general, domain-independent concept. Content from working notes — Protocol Ontology Candidates, Protocol Relationships, Inheritance Terminology Concerns — was incorporated to enrich the ontological discussion.

#### Considered and not done
- **Defining Protocol purely in terms of Khayyam's `ab` construct (rejected).** Ties the concept to one language's implementation; Protocol existed long before Khayyam and exists in domains outside software.
- **Using "Interface" as the primary term, following Java/Go convention (rejected).** "Interface" carries strong associations with programming-language type systems; "Protocol" captures the broader reality that interaction rules exist in networking, diplomacy, science, industry, and other non-software domains.

---

### Protocol–Process–System and Protocol–Science connections
- Time: 2026-06-25T00:00:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued.
  - [Super Z](../CONTRIBUTORS.md#super-z) — rewrote.

#### What changed
Established the inseparable relationship between protocols, processes, and systems, drawing on systems theory; established the connection between protocols and science, showing that protocols are foundational to knowledge production through methodology; diversified domain examples beyond networking and software to diplomacy, medicine, law, aviation, sports, and industry; corrected the Protocol vs Standard distinction (standard as third-party attestation, not a synonym for "ratified protocol"); enhanced Protocol vs Specification with the methodology dimension; relabeled Formal Definition as a language-level illustration rather than the general definition; strengthened the ontology candidate analysis by evaluating each candidate against the process and system requirements; added "Process-bound" and "Methodologically produced" to Protocol Properties.

---

### Critical review with Claude
- Time: 2026-07-01T00:00:00Z
- Type: Fixed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Claude](../CONTRIBUTORS.md#claude) (Claude Sonnet 5, medium effort with thinking) — reviewed, rewrote

#### What changed
Distinguished idea/discovery from structured lifecycle development within the "Methodologically produced" property, so it does not read as requiring committee-style production from the first moment of ideation, while still holding that an unrefined idea or draft does not by itself carry Protocol status; added non-software methodology examples (diplomatic treaty negotiation, clinical research ethics review) alongside the existing Khayyam `ab` example; corrected process cardinality ("one or more processes," possibly nested, rather than "a process"); flagged System and Process as then-undefined foundational dependencies; refined Protocol vs Standard to distinguish institutionalization attestation (the ISO 9001 model) from maturity attestation (the IETF Internet Standard model, per RFC 6410's criteria). (Claude)

#### What changed
Corrected a property description that could have been read as requiring committee-style production from the first moment of ideation; broadened methodology examples beyond software; corrected process cardinality in the core definition and the Process-bound property; distinguished two genuinely different forms of third-party attestation under Protocol vs Standard.

---

### Terminology document review — Protocol vs API Specification
- Time: 2026-07-10T00:00:00Z
- Type: Added
- Propagates to:
  - terminology.md: Done — the simplified, slightly inconsistent Protocol/API-specification treatment that previously lived in Terminology's worked examples was removed in favor of this document's fuller treatment.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote.

#### What changed
Added a dedicated "Protocol vs API Specification" section, migrating and substantially expanding the treatment that previously lived, in simplified form, inside Terminology's worked examples — keeping Terminology free of dependencies on other documents while giving the API-specification case a treatment grounded in this document's finalized definitions. Replaced the abstract "JSON-only variant" example under Protocol Refinement with the concrete BSON-vs-JSON case, and made explicit that the formal Extension/Refinement boundary remains unresolved rather than implying the given examples settle it.

---

### System document finalized and referenced
- Time: 2026-07-14T00:00:00Z
- Type: Fixed
- Cited:
  - [System](./system.md) — Depends_on: System is now formally defined; this document's Protocol-Process-System ontology depends on System being a defined concept.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote.

#### What changed
Restored a "Foundational Dependency" item under Unresolved Questions, narrowed to Process only. The prior version of this item, which covered both System and Process, had been fully removed when the System document was added to Citations, even though only the System half of that dependency was actually resolved — Process still lacked a dedicated document. This was corrected so the still-open half was not silently dropped. Also trimmed the Abstract's closing sentence, which previewed the full list of concepts this document distinguishes Protocol from (Contract, Standard, Specification, Interface, Policy) — per Terminology's Definition vs. Explanation distinction, a roadmap of Explanation-type subsections does not belong in a Summary/Abstract.

---

### Process content migrated to process.md
- Time: 2026-08-15T00:00:00Z
- Type: refactor
- Cited:
  - [Process](./process.md) — Depends_on: Process now has its own document; this document's Protocol-Process-System ontology depends on it the same way it depends on System.
- Propagates to:
  - process.md: Done — no new content needed there; process.md's existing Process Composition topic already covers the nesting behavior this document previously duplicated.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote

#### What changed
Asked that Process-specific content in this document be migrated to process.md, leaving only a link here. (Omid Hekayati)

Trimmed the process-nesting explanation in "What is a Protocol?" and the "Process-bound" property (both previously repeated the same nesting explanation now covered in full by process.md's Process Composition topic) to a pointer; trimmed "Protocol, Process, and System" to keep only what is Protocol-specific (the reproducibility/verifiability argument, the governance-structure framing), pointing to system.md and process.md for the general System/Process theory previously duplicated here; removed the "Foundational Dependency on Process" Unresolved Questions item, since process.md now exists and the dependency it flagged is resolved. (Claude)

#### What changed
This document no longer independently explains what a Process is or what process nesting means — it links to process.md for that, and keeps only the Protocol-specific half of the Protocol–Process–System relationship, mirroring the same asymmetric-dependency pattern established between system.md and process.md.

---

### Migration to the Explanation-facet document template
- Time: 2026-08-15T00:00:00Z
- Type: refactor
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote

#### What changed
Asked that this document be migrated to the current structure, with a paired changelog file, and that every occurrence of the word "RFC" (referring to Memar's own document type) be replaced with "document." (Omid Hekayati)

Restructured this document from `Summary/Motivation/Guide-level Explanation/Reference-level Explanation/Drawbacks/Rationale and Alternatives/Prior Art/Unresolved Questions/Future Possibilities/Change Rationale` into the current template (`Abstract → Introduction → Explanation → Results → Discussion`); moved front-matter `Citations` and `Contributor(s)` into this changelog's entries; migrated the prior `## Change Rationale` narrative into the changelog entries above; normalized Discussion sub-heading casing to match the template; replaced every occurrence of "RFC" referring to Memar's own documents with "document," while deliberately preserving external IETF RFC numbers (RFC 9110, 9111, 9112, 9113, 9114, RFC 791, RFC 793, RFC 5321, RFC 6410) unchanged, since those are proper external identifiers naming actual IETF standards-track documents, not instances of Memar's own document-type word. (Claude)

#### What changed
This document is now structured per `documentation-explanation.md`. Its Citations, Contributor roster, and full change history now live entirely in this file rather than in front matter and a document-level `## Change Rationale`.

#### Considered and not done
Considered leaving IETF's own "RFC 6410" and similar citations unchanged case-by-case versus a single blanket find-and-replace. A blanket replace was rejected because it would have silently corrupted external, factually-specific identifiers (e.g. turning "RFC 6410" into "document 6410," which refers to nothing). A regex excluding "RFC" followed by a number was used instead, and its output was verified before finalizing this document.

---

### Conceptual consistency check against the now-current system.md, process.md, modularity.md, terminology.md, and framework.md
- Time: 2026-08-16T00:00:00Z
- Type: Fixed
- Propagates to:
  - modularity.md: Done — its "Module, Process, and Protocol" section and its "Module Among Related Concepts" table both described Protocol as governing "interactions within or between Systems," which does not match this document's actual chain (System contains Processes, governed by Protocols); both were corrected to route through Process, with a link back to this document's "What is a Protocol?" topic.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Claude](../CONTRIBUTORS.md#claude) — reviewed, rewrote

#### What changed
Asked for a conceptual (not structural) review of this document against the rest of the now-revised document set, specifically flagging that the "Terminology Governance document" item under Future possibilities was stale now that terminology.md exists. (Omid Hekayati)

Removed the "Terminology Governance document" Future possibility, since terminology.md's "Terminology Authority and Governance" and "Word-Weight Rebalancing" sections now cover exactly what that item proposed creating; added a note to the "Cross-Module and Cross-Organizational Protocols" Unresolved question pointing to modularity.md's now-existing formal definition of Module, without treating that alone as resolving the question; found and fixed the reverse-direction inconsistency in modularity.md, where Protocol's relationship to System had been paraphrased imprecisely. (Claude)

#### What changed
This document's own content needed only two changes: one stale Future possibility (a Terminology Governance document, now that terminology.md exists and covers that ground) and one enrichment to an Unresolved question (Module now has a formal definition, in modularity.md, that didn't exist when the question was first raised). The larger finding was in the opposite direction — modularity.md had been paraphrasing this document's Protocol/Process/System chain imprecisely, describing Protocol as governing System-to-System interaction directly rather than governing Processes within a System. That was corrected in modularity.md, not here, since this document's own ontology was already accurate.

#### Considered and not done
Considered leaving the "Terminology Governance document" Future possibility in place with a note that it had been superseded, rather than removing it outright, to preserve a record of what was originally proposed. Removed instead, following the same pattern already used elsewhere in this project's changelogs for resolved Future possibilities and Unresolved questions: the resolution itself is the record, kept in this changelog entry, so the base document does not accumulate crossed-out proposals.

---

### External-observer consequence made explicit
- Time: 2026-08-25T00:00:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) — argued
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — drafted, reviewed, applied
- Propagates to:
  - agency.md: Done in this same pass — "From Observer to Agent" cross-links this topic.

#### What changed
Proposed recasting Protocol as the boundary facing a System's external observer; accepted the correction recorded below that this is a consequence of the existing definition, not a replacement for it. (Omid Hekayati)

Developed the observation-precedes-action position across discussion, including the hospital-complaint example showing that reading a protocol ordinarily prepares a subsequent act upon the governed system. (ChatGPT)

Wrote the new topic with explicit guards against redefinition drift toward specification/framework territory, and linked the enabling (not constituting) relation to Agency. (Super Z)

#### What changed
Added "Protocols and External Observers". The existing definition — declarative rules governing processes within a System — is unchanged. The new topic states its external consequence: precisely because a Protocol governs processes, it is what makes a System understandable and interactable-from outside its boundary, and understanding a protocol ordinarily precedes becoming a participant. Two guards are explicit: describing a System is not what makes something a Protocol (that is Specification/Framework territory), and understanding a protocol enables but does not constitute action, which belongs to Agency.

#### Considered and not done
- **Redefining Protocol as "the abstractions by which a System is explained to an external observer" (rejected)**: this surfaced during discussion as a candidate reframing. Rejected because it collides with this document's settled ontology — a protocol detached from any governed process is inert — and because "description of a System for observers" duplicates distinctions this document already maintains against Specification and Framework. The adopted text keeps governance as the defining property and presents external observability as its consequence, preserving both the ontology and the insight behind the proposed reframing.

---

### Two open items absorbed from the retired Persian draft
- Time: 2026-08-25T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — reviewed, applied
- Propagates to:
  - protocol.per.md: Pending deletion — fully superseded by this document; no further changes should reference it.

#### What changed
Asked for a final review of the legacy Persian-language draft (`protocol.per.md`) so nothing of value is lost before its deletion. (Omid Hekayati)

Compared the Persian draft against this document item by item; confirmed all substantive content is already present here in evolved form (with its Standard definition explicitly superseded by the attestation framework); transferred the only two genuinely missing items, recorded below. (Super Z)

#### What changed
Added one Unresolved question, "Attestation of Memar's own Protocols" — who plays the attesting role for protocols produced within the Memar ecosystem itself: self-declaration by an implementing contributor versus a dedicated independent body, possibly decided per protocol; until resolved, conformance claims about Memar protocols carry no standard status in this document's precise sense. Added one Future possibilities item, "AI-assisted conformance" — tooling lowering the practical cost of producing and running conformance tests, including possible automatic generation of conformance suites from declared rules. Both were distilled from the legacy Persian draft; everything else in that draft was verified as already covered here.

#### Considered and not done
- **Transferring more content from the Persian draft (rejected)**: the remaining material — the old Rule-Set-style formal definition, the pre-attestation definition of Standard, the five-concept comparison table, and the khayyam-* document-mapping instructions — is either already present here in evolved form, explicitly contradicted by this document's current ontology, or composed of stale references to since-restructured documents. Carrying it forward would reintroduce known-outdated positions rather than preserve knowledge.

---

### Documentation-method migration completed: Discussion, Rationale, Prior art, Unresolved questions, Future possibilities dissolved per the finalized method
- Time: 2026-09-07T00:00:00Z
- Type: refactor
- Propagates to:
  - protocol.handoff.md: Created - open questions and future possibilities moved there.
- Contributors:
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — moved

#### What changed
- The body's fixed top-level sections are now `Abstract`, `Introduction`, `Explanation`, `Results` only (Super Z - applied the finalized documentation method).
- The document-level `Drawbacks`, `Rationale and alternatives`, and `Prior art` content preserved below; `Unresolved questions` and `Future possibilities` moved to the paired handoff (Super Z).

Dissolved the Protocols-and-External-Observers topic's `#### Discussion` and the document-level `## Discussion`; the observer-framing drawback folded into its topic as inline content; all other content relocated below without loss. (Super Z)

#### Considered and not done (topic-level drawbacks relocated per owner ruling)
- **The observer-facing framing invites regression to the familiar software habit of equating "protocol" with an interface document or API specification.** That equation is rejected in the topic itself, but repetition will be needed wherever the Protocol–Specification distinction erodes in everyday usage. (Migrated from the Protocols-and-External-Observers topic)

#### Considered and not done (from the removed document-level Drawbacks section)
- **Abstraction Risk:** Defining Protocol at a high level of generality may feel abstract and removed from the day-to-day concerns of a language designer or developer. The definition is intentionally conceptual, which means it does not immediately yield implementation guidance.
- **Terminology Friction:** Many developers are accustomed to using "protocol" loosely (e.g., "the HTTP protocol" meaning the IETF standard) and "standard" even more loosely. A precise definition may feel pedantic or conflict with established usage in some communities. However, widespread imprecise usage does not invalidate precise definition — any more than widespread belief in a flat earth invalidates the spherical model.
- **Incomplete Finalization:** The ontology question (Rule Set vs. Interaction Model vs. Verifiable Interaction Model) remains open. Deferring this decision means the document's core definition carries inherent ambiguity, though the process and system components apply regardless of which candidate is ultimately chosen.
- **Precision Cost:** Maintaining a precise definition of Protocol — and distinguishing it from Contract, Standard, Specification, Interface, and Policy — imposes a cognitive cost on readers and contributors. Every time these terms are used in subsequent documents, the distinction must be maintained. This cost is accepted as a necessary investment in conceptual clarity.

#### Considered and not done (from the retired Rationale and alternatives section)
- **Why this document is needed**: without a clear, general definition of Protocol, every subsequent Memar document that references protocols risks ambiguity. The distinctions between Protocol, Contract, Standard, Specification, Interface, and Policy are not academic — they drive different design decisions. For example, if Protocol were conflated with Contract, one might incorrectly assume protocols imply bilateral obligations. If Protocol were conflated with Standard, one might incorrectly assume all protocols require third-party certification.
- **Adopt a language-specific definition (rejected)**: define Protocol purely in terms of Khayyam's `ab` (abstraction) construct: "a Protocol is what Khayyam calls an abstraction." Rejected because it ties the concept to one language's implementation. The concept of Protocol existed long before Khayyam and exists in domains outside software. A language-specific definition would prevent Memar from reasoning about protocols in a general way.
- **Treat Protocol and Interface as equivalent (rejected)**: use "Interface" as the primary term, following Java and Go convention. Rejected because "Interface" carries strong associations with programming language type systems, whereas "Protocol" captures the broader reality that interaction rules exist in networking, diplomacy, science, industry, organizational processes, and other domains where "interface" would be an awkward fit.
- **Define Standard as "widely adopted protocol specification" (rejected)**: the common usage where "standard" means widespread adoption (e.g., "HTTP is a web standard") collapses two genuinely distinct concepts into one word. The protocol (the rules governing a process) and the attestation (the certification that those rules are institutionalized) are different things with different properties, different producers, and different consumers. A company can follow a protocol without holding a standard certification. A company can hold a standard certification and still produce poor outcomes. These facts demonstrate that the two concepts are distinct, and precision requires distinct words.
- **Impact of not doing this**: without this document, the term "Protocol" remains undefined in the Memar framework. Discussions about protocol conformance, protocol composition, and protocol relationships would lack a shared foundation, leading to circular debates and inconsistent decisions across documents.

#### Related work
- **Networking Protocols**: HTTP (defined across [RFC 9110](https://datatracker.ietf.org/doc/html/rfc9110), [9111](https://datatracker.ietf.org/doc/html/rfc9111), [9112](https://datatracker.ietf.org/doc/html/rfc9112), [9113](https://datatracker.ietf.org/doc/html/rfc9113), [9114](https://datatracker.ietf.org/doc/html/rfc9114)) is a protocol — a set of rules governing the request-response process between clients and servers; IETF ratification changes the governance status, not the ontological nature of the entity. TCP ([RFC 793](https://datatracker.ietf.org/doc/html/rfc793)) and IP ([RFC 791](https://datatracker.ietf.org/doc/html/rfc791)) are foundational examples of protocols as interaction models with verifiable conformance. SMTP ([RFC 5321](https://datatracker.ietf.org/doc/html/rfc5321)) specifies message formats, command sequences, and response codes without prescribing implementation.
- **Diplomatic and Social Protocols**: the Vienna Convention on Diplomatic Relations (1961) codifies the protocol governing diplomatic missions (accreditation, communication, privileges, immunities); the United Nations Protocol and Liaison Service's existence demonstrates that protocol management is recognized as a distinct, essential function even at the highest levels of international organization; courtroom protocols (various jurisdictions) define who may speak, in what order, under what conditions, and with what consequences for violations.
- **Scientific and Research Protocols**: the scientific method is the foundational meta-protocol of modern science (hypotheses testable and falsifiable, experiments reproducible, conclusions following from evidence); clinical trial protocols (ICH-GCP) define the protocol structure for clinical trials; laboratory protocols specify exact steps, reagents, conditions, and measurements so another researcher following the same protocol obtains comparable results.
- **Industry and Organizational Protocols**: ISO 9001 (quality management) — ISO itself does not issue certifications; it accredits third-party auditors who verify institutionalization, the protocols being the rules and the certification being the attestation; ISO 27001 (information security), same certification model; ISO 20022 (finance) defines messaging protocols for financial transactions; OSHA construction safety standards define protocols governing workplace safety processes.
- **Domain-Specific Protocols**: ACORD (insurance data exchange), HL7/FHIR (healthcare data exchange — HL7 v2 text-based; FHIR a RESTful API protocol with JSON/XML schemas), SWIFT MT/MX (interbank transfer message formats), OPC UA (industrial IoT device interoperability).
- **API and Specification Ecosystems**: OpenAPI is a specification *of* protocols; the GraphQL specification defines a protocol for the data-fetching process.
- **Programming Language Constructs (partial equivalents)**: Swift `protocol` (method requirements without implementations); Go `interface` (method sets, but embedding allows implicit satisfaction, blurring the ownership boundary); Rust traits (default method implementations go beyond pure protocol declaration); Java interfaces (originally pure; Java 8 default methods moved away from protocol purity); CORBA IDL and Protocol Buffers (language-agnostic interface definition languages).
