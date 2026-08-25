# Protocol Changelog

## Changelog

### Original split from the monolithic Protocol document
- Time: 2026-06-21T00:00:00Z
- Type: Added
- Cited:
  - [Terminology](./terminology.md) — Foundation Alignment: terminology governs how concepts are understood across protocol.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued, claimed: core ontological definition of Protocol; the Protocol–Process–System relationship; the Protocol–Science–Methodology connection; the critique of "standard" as third-party attestation; the diplomatic and scientific protocol examples; the methodology-based distinction between Protocol and Specification.
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) (GPT-5.5) — drafted, argued: drafted the initial text; argued for and against alternatives; incorporated revisions.
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM, high effort) — rewrote: split the original monolithic document (Protocol, Explicit Behavior Ownership, and Khayyam Rejection of Inheritance) into three focused documents; restructured this document to be purely ontological; enriched it with the Protocol–Process–System relationship (systems theory) and the Protocol–Science–Methodology connection; diversified domain examples (diplomatic, scientific, medical, legal, aviation, sports); corrected Protocol vs Standard to define standard as third-party attestation; added the methodology dimension to Protocol vs Specification; relabeled Formal Definition as a language-level illustration; strengthened the ontology candidate analysis with the process argument.

#### Summary
Split out of an earlier monolithic document that mixed ontological questions about Protocol with design principles about behavior ownership and language-level decisions about inheritance — a conflation that made it difficult to discuss any one topic without being pulled into the others. The Protocol portion was refined to remove all Khayyam-specific implementation details, code examples, and entity references, so the document defines Protocol as a general, domain-independent concept. Content from working notes — Protocol Ontology Candidates, Protocol Relationships, Inheritance Terminology Concerns — was incorporated to enrich the ontological discussion.

#### Rationale and alternatives
- **Defining Protocol purely in terms of Khayyam's `ab` construct (rejected).** Ties the concept to one language's implementation; Protocol existed long before Khayyam and exists in domains outside software.
- **Using "Interface" as the primary term, following Java/Go convention (rejected).** "Interface" carries strong associations with programming-language type systems; "Protocol" captures the broader reality that interaction rules exist in networking, diplomacy, science, industry, and other non-software domains.

---

### Protocol–Process–System and Protocol–Science connections
- Time: 2026-06-25T00:00:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued.
  - [Super Z](../CONTRIBUTORS.md#super-z) — rewrote.

#### Summary
Established the inseparable relationship between protocols, processes, and systems, drawing on systems theory; established the connection between protocols and science, showing that protocols are foundational to knowledge production through methodology; diversified domain examples beyond networking and software to diplomacy, medicine, law, aviation, sports, and industry; corrected the Protocol vs Standard distinction (standard as third-party attestation, not a synonym for "ratified protocol"); enhanced Protocol vs Specification with the methodology dimension; relabeled Formal Definition as a language-level illustration rather than the general definition; strengthened the ontology candidate analysis by evaluating each candidate against the process and system requirements; added "Process-bound" and "Methodologically produced" to Protocol Properties.

---

### Critical review with Claude
- Time: 2026-07-01T00:00:00Z
- Type: Fixed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Claude](../CONTRIBUTORS.md#claude) (Claude Sonnet 5, medium effort with thinking) — reviewed, rewrote: distinguished idea/discovery from structured lifecycle development within the "Methodologically produced" property, so it does not read as requiring committee-style production from the first moment of ideation, while still holding that an unrefined idea or draft does not by itself carry Protocol status; added non-software methodology examples (diplomatic treaty negotiation, clinical research ethics review) alongside the existing Khayyam `ab` example; corrected process cardinality ("one or more processes," possibly nested, rather than "a process"); flagged System and Process as then-undefined foundational dependencies; refined Protocol vs Standard to distinguish institutionalization attestation (the ISO 9001 model) from maturity attestation (the IETF Internet Standard model, per RFC 6410's criteria).

#### Summary
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

#### Summary
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

#### Summary
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
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: asked that Process-specific content in this document be migrated to process.md, leaving only a link here.
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote: trimmed the process-nesting explanation in "What is a Protocol?" and the "Process-bound" property (both previously repeated the same nesting explanation now covered in full by process.md's Process Composition topic) to a pointer; trimmed "Protocol, Process, and System" to keep only what is Protocol-specific (the reproducibility/verifiability argument, the governance-structure framing), pointing to system.md and process.md for the general System/Process theory previously duplicated here; removed the "Foundational Dependency on Process" Unresolved Questions item, since process.md now exists and the dependency it flagged is resolved.

#### Summary
This document no longer independently explains what a Process is or what process nesting means — it links to process.md for that, and keeps only the Protocol-specific half of the Protocol–Process–System relationship, mirroring the same asymmetric-dependency pattern established between system.md and process.md.

---

### Migration to the Explanation-facet document template
- Time: 2026-08-15T00:00:00Z
- Type: refactor
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: asked that this document be migrated to the current structure, with a paired changelog file, and that every occurrence of the word "RFC" (referring to Memar's own document type) be replaced with "document."
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote: restructured this document from `Summary/Motivation/Guide-level Explanation/Reference-level Explanation/Drawbacks/Rationale and Alternatives/Prior Art/Unresolved Questions/Future Possibilities/Change Rationale` into the current template (`Abstract → Introduction → Explanation → Results → Discussion`); moved front-matter `Citations` and `Contributor(s)` into this changelog's entries; migrated the prior `## Change Rationale` narrative into the changelog entries above; normalized Discussion sub-heading casing to match the template; replaced every occurrence of "RFC" referring to Memar's own documents with "document," while deliberately preserving external IETF RFC numbers (RFC 9110, 9111, 9112, 9113, 9114, RFC 791, RFC 793, RFC 5321, RFC 6410) unchanged, since those are proper external identifiers naming actual IETF standards-track documents, not instances of Memar's own document-type word.

#### Summary
This document is now structured per `documentation-explanation.md`. Its Citations, Contributor roster, and full change history now live entirely in this file rather than in front matter and a document-level `## Change Rationale`.

#### Rationale and alternatives
Considered leaving IETF's own "RFC 6410" and similar citations unchanged case-by-case versus a single blanket find-and-replace. A blanket replace was rejected because it would have silently corrupted external, factually-specific identifiers (e.g. turning "RFC 6410" into "document 6410," which refers to nothing). A regex excluding "RFC" followed by a number was used instead, and its output was verified before finalizing this document.

---

### Conceptual consistency check against the now-current system.md, process.md, modularity.md, terminology.md, and framework.md
- Time: 2026-08-16T00:00:00Z
- Type: Fixed
- Propagates to:
  - modularity.md: Done — its "Module, Process, and Protocol" section and its "Module Among Related Concepts" table both described Protocol as governing "interactions within or between Systems," which does not match this document's actual chain (System contains Processes, governed by Protocols); both were corrected to route through Process, with a link back to this document's "What is a Protocol?" topic.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: asked for a conceptual (not structural) review of this document against the rest of the now-revised document set, specifically flagging that the "Terminology Governance document" item under Future possibilities was stale now that terminology.md exists.
  - [Claude](../CONTRIBUTORS.md#claude) — reviewed, rewrote: removed the "Terminology Governance document" Future possibility, since terminology.md's "Terminology Authority and Governance" and "Word-Weight Rebalancing" sections now cover exactly what that item proposed creating; added a note to the "Cross-Module and Cross-Organizational Protocols" Unresolved question pointing to modularity.md's now-existing formal definition of Module, without treating that alone as resolving the question; found and fixed the reverse-direction inconsistency in modularity.md, where Protocol's relationship to System had been paraphrased imprecisely.

#### Summary
This document's own content needed only two changes: one stale Future possibility (a Terminology Governance document, now that terminology.md exists and covers that ground) and one enrichment to an Unresolved question (Module now has a formal definition, in modularity.md, that didn't exist when the question was first raised). The larger finding was in the opposite direction — modularity.md had been paraphrasing this document's Protocol/Process/System chain imprecisely, describing Protocol as governing System-to-System interaction directly rather than governing Processes within a System. That was corrected in modularity.md, not here, since this document's own ontology was already accurate.

#### Rationale and alternatives
Considered leaving the "Terminology Governance document" Future possibility in place with a note that it had been superseded, rather than removing it outright, to preserve a record of what was originally proposed. Removed instead, following the same pattern already used elsewhere in this project's changelogs for resolved Future possibilities and Unresolved questions: the resolution itself is the record, kept in this changelog entry, so the base document does not accumulate crossed-out proposals.

---

### External-observer consequence made explicit
- Time: 2026-08-25T00:00:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued: proposed recasting Protocol as the boundary facing a System's external observer; accepted the correction recorded below that this is a consequence of the existing definition, not a replacement for it.
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) — argued: developed the observation-precedes-action position across discussion, including the hospital-complaint example showing that reading a protocol ordinarily prepares a subsequent act upon the governed system.
  - [ox-alpha](../CONTRIBUTORS.md#ox-alpha) (opencode) — drafted, reviewed, applied: wrote the new topic with explicit guards against redefinition drift toward specification/framework territory, and linked the enabling (not constituting) relation to Agency.
- Propagates to:
  - agency.md: Done in this same pass — "From Observer to Agent" cross-links this topic.

#### Summary
Added "Protocols and External Observers". The existing definition — declarative rules governing processes within a System — is unchanged. The new topic states its external consequence: precisely because a Protocol governs processes, it is what makes a System understandable and interactable-from outside its boundary, and understanding a protocol ordinarily precedes becoming a participant. Two guards are explicit: describing a System is not what makes something a Protocol (that is Specification/Framework territory), and understanding a protocol enables but does not constitute action, which belongs to Agency.

#### Rationale and alternatives
- **Redefining Protocol as "the abstractions by which a System is explained to an external observer" (rejected)**: this surfaced during discussion as a candidate reframing. Rejected because it collides with this document's settled ontology — a protocol detached from any governed process is inert — and because "description of a System for observers" duplicates distinctions this document already maintains against Specification and Framework. The adopted text keeps governance as the defining property and presents external observability as its consequence, preserving both the ontology and the insight behind the proposed reframing.

---

### Two open items absorbed from the retired Persian draft
- Time: 2026-08-25T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: asked for a final review of the legacy Persian-language draft (`protocol.per.md`) so nothing of value is lost before its deletion.
  - [ox-alpha](../CONTRIBUTORS.md#ox-alpha) (opencode) — reviewed, applied: compared the Persian draft against this document item by item; confirmed all substantive content is already present here in evolved form (with its Standard definition explicitly superseded by the attestation framework); transferred the only two genuinely missing items, recorded below.
- Propagates to:
  - protocol.per.md: Pending deletion — fully superseded by this document; no further changes should reference it.

#### Summary
Added one Unresolved question, "Attestation of Memar's own Protocols" — who plays the attesting role for protocols produced within the Memar ecosystem itself: self-declaration by an implementing contributor versus a dedicated independent body, possibly decided per protocol; until resolved, conformance claims about Memar protocols carry no standard status in this document's precise sense. Added one Future possibilities item, "AI-assisted conformance" — tooling lowering the practical cost of producing and running conformance tests, including possible automatic generation of conformance suites from declared rules. Both were distilled from the legacy Persian draft; everything else in that draft was verified as already covered here.

#### Rationale and alternatives
- **Transferring more content from the Persian draft (rejected)**: the remaining material — the old Rule-Set-style formal definition, the pre-attestation definition of Standard, the five-concept comparison table, and the khayyam-* document-mapping instructions — is either already present here in evolved form, explicitly contradicted by this document's current ontology, or composed of stale references to since-restructured documents. Carrying it forward would reintroduce known-outdated positions rather than preserve knowledge.
