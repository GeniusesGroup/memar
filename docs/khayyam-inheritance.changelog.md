# Inheritance in Khayyam Changelog

## Changelog

### Created by splitting the Protocol document
- Time: 2026-07-10T00:00:00Z (approximated from Start Date; original drafting time not recorded)
- Type: Added
- Cited:
  - [Protocol](./protocol.md) — Depends_on: Protocol's definition as a pure declarative specification underpins how abstraction inclusion creates requirement-inheritance relationships between abstractions.
  - [Explicit Behavior Ownership](./type.md#explicit-behavior-ownership) — Depends_on: EBO is the principled foundation for rejecting behavior transfer between capsules; this document specifies its language-level consequences.
- Propagates to:
  - khayyam.md: Done — khayyam.md's abstraction/conformance framing reflects this document's placement model of inheritance.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed: core language design decisions, placement of inheritance in the abstraction layer, rejection of behavior transfer between capsules
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) (GPT-5.5) — drafted: initial text of the original monolithic Protocol document; portions of the behavior-transfer and method-promotion analysis incorporated here
  - [Super Z](../CONTRIBUTORS.md#super-z) — rewrote: restructured the document from "Rejection of Inheritance" to "Inheritance in Khayyam," reframing the topic as placement rather than rejection; added the subtyping section with Khayyam syntax; unified terminology with the EBO document

#### Summary
This document was created by splitting the original monolithic "Protocol" document into focused documents. The inheritance-related content was distributed between the Explicit Behavior Ownership document (principled foundation) and this document (language-level specification). It was originally titled "Rejection of Inheritance"; during review that framing proved misleading — Khayyam does not reject inheritance, it places it where it belongs (requirement extension between abstractions) while rejecting behavior transfer between capsules — so it was retitled and restructured accordingly.

Additional incorporated sources:
- **Working notes:** the Go embedding clarification ("Not All Embedding Is the Same") was extracted from working notes and integrated as a core argument. The meta-observation about what "inheritance" debates are really about was initially integrated here but subsequently moved to the Explicit Behavior Ownership document during terminology and content review — it is a general conceptual argument, not a language-specific design decision.
- **khayyam-linter.md:** the "Explicit Delegation Verification" and "Anti-Lazy Inheritance Check" sections provided the linter enforcement rules.
- **khayyam.md:** the abstraction definition and conformance model provided the context for how Khayyam handles capsule–abstraction relationships without behavior transfer.

### Migrated to Explanation-facet structure
- Time: 2026-08-26T00:00:00Z
- Type: refactor
- Cited:
  - [Documentation](./documentation.md) — Reference: facet meta-layer defining Explanation/Practice/Changelog and the cross-cutting URI and citation rules.
  - [Documentation — Explanation](./documentation-explanation.md) — Depends_on: governing structure the base document was migrated to.
  - [Documentation — Changelog](./documentation-changelog.md) — Depends_on: entry structure used for this companion file.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: migration of this document to the current documentation method
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — migrated: structural migration and provenance relocation per the Explanation-facet specification

#### Summary
Structural migration only; no design decision changed. The base document was reorganized to the current Explanation-facet specification: fixed top-level sections (`Abstract`, `Introduction`, `Explanation`, `Results`, `Discussion`), topic-first organization under `Explanation`, and Discussion bundles attached to the topics they concern (the per-alternative arguments moved under Capsule Composition Without Method Promotion). Provenance previously carried in the base document's front matter (`Citations`, `Contributors`, `Applied to`) was relocated into this file's entries above. Two broken Explicit Behavior Ownership links in the old document (`./type.md#explicit-behavior-ownership` in Citations and `./explicit_behavior_ownership.md` in the Summary) were corrected to the actual file, `./type-explicit_behavior_ownership.md`; a duplicated-word typo in Unresolved questions was fixed. The former body `Change Rationale`/`Summary` historical narrative now lives in the "Created by splitting the Protocol document" entry above.

### Added the minimal-independent-concepts design goal to Motivation
- Time: 2026-08-26T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: stating the compositional design goal explicitly after review found it only implied
  - [Super Z](../CONTRIBUTORS.md#super-z) — drafted

#### Summary
Added "The Design Goal: Minimal Independent Concepts, Not Base Classes" at the top of Motivation, making explicit the positive principle behind the document's rules: Khayyam's type model targets the minimal set of independent concepts from which every other concept is derived by composition, not base-class hierarchies. Prior review had found this principle present only implicitly — framed as costs (No "Base Class" Convenience) and alternatives (Template Method) — never stated as the goal itself.

### Repointed Explicit Behavior Ownership links after EBO absorption into type.md
- Time: 2026-08-30T00:00:00Z
- Type: Fixed
- Contributors:
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — fixed: repointed the three Explicit Behavior Ownership links that broke when the standalone EBO sub-document was absorbed into the Type document

#### Summary
The `type-explicit_behavior_ownership.md` file that three links targeted no longer exists: the standalone Explicit Behavior Ownership sub-document was absorbed into [Type](./type.md), where the principle now lives as its `Explicit Behavior Ownership` section. The three links (Summary and "Why Not Allow 'Safe' Behavior Transfer?" in the base document, and the Cited entry of the "Created by splitting the Protocol document" entry above) now point to `./type.md#explicit-behavior-ownership`. Link-target correction only; no text or design decision changed.
