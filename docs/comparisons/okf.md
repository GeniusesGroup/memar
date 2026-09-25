# Comparison: Memar and Open Knowledge Format (OKF)
This comparison evaluates whether [Open Knowledge Format v0.2](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/ad30107c31c06aec8a7d5636e0d1058118604e6f/SPEC.md) contributes a missing idea to Memar's architecture or documentation method. It finds no present reason to replace or extend Memar's governing method with OKF. OKF does expose three concrete seams—portable export, machine-readable freshness, and attested computation—that may justify separate research if a live requirement appears.

The comparison uses OKF v0.2 at commit [`ad30107`](https://github.com/GoogleCloudPlatform/open-knowledge-format/commit/ad30107c31c06aec8a7d5636e0d1058118604e6f), the repository `main` head on 2026-09-25. The older [`okf.md/spec`](https://okf.md/spec/) page identifies itself as an annotated v0.1 draft containing opinions; it is treated as secondary commentary rather than as the governing specification. No performance benchmark, round-trip experiment, or production interoperability test was performed, so claims about relative cost or effectiveness are bounded accordingly.

## Table of contents
- [1. What each project is](#1-what-each-project-is)
  - [OKF](#okf)
  - [Memar](#memar)
  - [Category distinction](#category-distinction)
- [2. Source status and maturity](#2-source-status-and-maturity)
- [3. Where OKF is genuinely more useful](#3-where-okf-is-genuinely-more-useful)
- [4. Where Memar is stronger](#4-where-memar-is-stronger)
- [5. Costs and limits on both sides](#5-costs-and-limits-on-both-sides)
  - [OKF](#okf-1)
  - [Memar](#memar-1)
- [6. `type: BigQuery Table`](#6-type-bigquery-table)
- [7. Technical terms and human language](#7-technical-terms-and-human-language)
- [8. Adoption filter](#8-adoption-filter)
  - [Already governed or better developed in Memar](#already-governed-or-better-developed-in-memar)
  - [Reject as internal Memar rules](#reject-as-internal-memar-rules)
  - [Conditional external profile](#conditional-external-profile)
  - [Separate future research](#separate-future-research)
- [9. Possible future integration](#9-possible-future-integration)
- [10. Decision](#10-decision)
- [11. Open for critique](#11-open-for-critique)

## 1. What each project is
### OKF
OKF is a minimal interchange format for exchanging knowledge as a directory of Markdown documents with YAML frontmatter. Its required structure is deliberately small: non-reserved Markdown files carry a non-empty `type`, unknown type values and keys remain consumable, and a bundle may be distributed as a repository, archive, or repository subdirectory ([OKF v0.2 §§3–4 and 11](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/ad30107c31c06aec8a7d5636e0d1058118604e6f/SPEC.md#3-bundle-structure) — **Evidence**). It is aimed at data catalogs, playbooks, metrics, assets, and agent-readable context that can remain portable without a proprietary store.

### Memar
Memar is a domain-independent system-development framework and shared knowledge model. It governs how concepts, identity, relationships, responsibilities, process, protocol, modeling, terminology, evidence, and change are understood across projects. Its principles deliberately avoid prescribing one storage engine, schema, or workflow; those are realizations in consuming projects ([Knowledge → Principles for Modeling Knowledge](../knowledge.md#principles-for-modeling-knowledge) — **Evidence**). Its live artifact is a connected model and documentation method, not a standard wire format or catalog implementation.

### Category distinction
The two projects do not perform the same job. OKF is primarily an **envelope and exchange format**. Memar is a **modeling and governance framework**. A fair comparison asks whether OKF supplies a missing Memar principle, a useful external projection, or only a different operational concern.

## 2. Source status and maturity
OKF's pinned v0.2 specification is clear, but the separately maintained [`okf.md` site](https://okf.md/) presents an older v0.1 view. That site describes `index.md` as mandatory, advertises validator access on some pages while [`/validator/`](https://okf.md/validator/) says `Coming Soon`, and labels itself MIT while the canonical repository contains an [Apache-2.0 license](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/ad30107c31c06aec8a7d5636e0d1058118604e6f/LICENSE.md). The canonical repository has no separate v0.2 tag or GitHub release at this head, so v0.2 is the version declared by `SPEC.md`, not a separately released artifact.

The repository's [`OKFDocument.validate()`](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/ad30107c31c06aec8a7d5636e0d1058118604e6f/src/reference_agent/bundle/document.py) checks only a non-empty `type`; it does not provide a bundle-level validator for §11's reserved-file rule. The repository also describes its reference agent and viewer as [proof-of-concept components](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/ad30107c31c06aec8a7d5636e0d1058118604e6f/README.md), not a mature production toolchain.

These are source-layer and presentation discrepancies; they do not establish a defect in the pinned core specification. They do make the repository specification preferable to the secondary site when making an architectural judgment.

## 3. Where OKF is genuinely more useful
OKF has real advantages for bounded exchange and catalog work:
1. **Very low adoption cost.** A team can create a bundle with a text editor, Markdown, YAML, and Git. No schema registry, SDK, database, or runtime is required to read the core format ([OKF v0.2 §§1, 4, and 11](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/ad30107c31c06aec8a7d5636e0d1058118604e6f/SPEC.md#1-motivation) — **Evidence**).
2. **Portable distribution.** A bundle can be cloned, archived, embedded in a repository, or handed to another organization without migrating into a proprietary store.
3. **Agent-friendly file access.** An agent that can read Markdown and YAML can navigate the bundle without a format-specific SDK. This is envelope-level interoperability, not guaranteed semantic interoperability.
4. **Extensible vocabulary.** Open `type` values let one corpus cover tables, APIs, metrics, policies, and playbooks without waiting for a central registry.
5. **Machine-readable operational metadata.** `sources`, `generated`, `verified`, `status`, `stale_after`, and claim-level source identifiers make a plain Markdown bundle more useful to an agent-maintained corpus ([OKF v0.2 §5](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/ad30107c31c06aec8a7d5636e0d1058118604e6f/SPEC.md#5-provenance-trust-and-lifecycle) — **Evidence**).
6. **A practical catalog envelope.** The format can carry a schema, business context, source attribution, examples, and a link to external assets in the same portable artifact.
7. **Attested Computation as a candidate pattern.** Its runtime, typed parameters, executor, receipt, and deterministic attester provide a concrete response to agent-authored computation risk, although the full runtime protocol remains deferred.

Where the requirement is limited to portable catalog or agent exchange, OKF can be the lower-ceremony operational choice. This comparison establishes neither a corpus-size threshold nor a measured difference in authoring and maintenance cost.

## 4. Where Memar is stronger
Memar is stronger where the concern is the **meaning and governance of a system**, not merely the transport of documents:
1. **Identity independent of location.** A knowledge artifact's identity must not change when its file moves ([Knowledge → Identity Must Be Independent of Location](../knowledge.md#identity-must-be-independent-of-location) — **Evidence**). OKF's Concept ID is a file path and is therefore suitable for a bundle record but weaker as a long-lived federated identity.
2. **Concept and implementation separation.** Memar requires modeling to discover concepts, responsibilities, and boundaries before implementation structures are chosen ([Modeling → The Model as the Primary Artifact](../modeling.md#the-model-as-the-primary-artifact) — **Evidence**). OKF intentionally leaves the domain model to its producer.
3. **Typed, first-class relationships.** Memar treats reference, dependency, containment, attribution, and opposition as distinct knowledge relations ([Knowledge → Relationships Are First-Class Citizens](../knowledge.md#relationships-are-first-class-citizens) — **Evidence**). OKF's core link syntax leaves the relationship kind in surrounding prose, so a machine consumer must infer it from prose or use a producer-defined extension or mapping layer.
4. **Knowledge beyond a document.** Memar distinguishes a document projection from concepts, claims, rationale, relationships, and context that may be finer than any file ([Knowledge → Definition](../knowledge.md#definition) — **Evidence**). OKF's exchange unit is explicitly one Markdown document per Concept.
5. **Reader-routed documentation.** Explanation, Practice, Changelog, Handoff, and Research have different structures because readers study, follow, audit, resume, or evaluate them ([Documentation → Facets currently defined](../documentation.md#facets-currently-defined) — **Evidence**). OKF's free-form body deliberately leaves this structure to producer convention.
6. **Decision rationale and evolution.** Memar preserves alternatives, deliberation, rationale, and propagation through task-centric knowledge evolution and reader-routed changelogs, handoffs, and researches ([Knowledge → Task-Centric Knowledge Evolution](../knowledge.md#task-centric-knowledge-evolution) — **Evidence**; [Documentation → Facets currently defined](../documentation.md#facets-currently-defined) — **Evidence**). OKF's `log.md` is useful prose history but does not natively carry the same rationale, review, or propagation model.
7. **Concept-first terminology and technology order.** Memar requires problem, concepts, scientific principles, technologies, tools, and products to be considered in that order ([Terminology → Architectural Rule](../terminology.md#architectural-rule) — **Evidence**). OKF's open routing labels are appropriate at an exchange boundary but do not supply that reasoning discipline.
8. **Process and protocol governance.** Process defines expected input, expected output, and checks; Protocol defines conformance; Agency defines authority and accountability ([Process → Expectations and Checks](../process.md#expectations-and-checks) — **Evidence**; [Protocol → Conformance](../protocol.md#conformance) — **Evidence**; [Agency → Authority](../agency.md#authority) — **Evidence**; [Agency → Accountability](../agency.md#accountability) — **Evidence**). OKF can carry prose or producer extensions describing these concerns, but its core three-rule envelope does not instantiate them.

These advantages concern Memar's model and method. They do not imply that Memar currently ships a mature validator, SDK, registry, or interoperability profile.

## 5. Costs and limits on both sides
### OKF
OKF's minimalism creates real costs:
- **Semantic interoperability is shallow by design.** A bundle can conform while producers use incompatible local meanings for the same `type` or body convention.
- **Concept identity is path-based.** Moving or renaming a file can change its Concept ID and break references or merges.
- **Generic relationships are not machine-typed.** A consumer that wants `depends-on`, `supersedes`, or `calculated-from` must parse prose or use a separate profile.
- **Broken links are intentionally tolerated.** This helps incremental authoring but weakens link integrity.
- **Lifecycle is small.** `draft`, `stable`, and `deprecated` do not directly express refutation, deletion, supersession, contested status, or a machine-readable replacement.
- **Freshness is advisory.** `stale_after` is a review signal, not proof that the content is true.
- **Trust is not authorization.** A `human:` prefix or `verified` event does not establish identity, independence, access control, or decision authority.
- **Conformance is shallow.** OKF v0.2 §11 defines three syntactic rules—frontmatter and `type` for concepts, plus reserved-file structure—but says nothing about semantic quality, graph completeness, or provenance correctness.
- **Tooling is early.** The reference agent and viewer are proof-of-concept components, and site claims about validator availability are inconsistent.
- **Discovery and retrieval are outside the core.** OKF v0.2 §1 lists storage, serving, and query infrastructure as non-goals; it does not replace crawling, RAG, search infrastructure, or a system of record.

### Memar
Memar's precision also has costs:
- **Higher authoring and governance overhead.** Facets, companions, explicit methodology, review state, and propagation require more discipline than three structural rules.
- **More files and navigation work.** The richer separation can create file-count and companion-maintenance costs that a single exchange format avoids.
- **No finished external export profile.** The current documents state principles but do not provide a versioned OKF-compatible export/import contract.
- **No packaged documentation validator.** Protocol and model requirements are conceptually checkable, but there is no single end-to-end validator for Memar's documentation set comparable to OKF v0.2's three-rule conformance floor.
- **The typed model is not yet realized in a machine-readable surface.** Memar requires typed relations, while its ordinary Markdown links still commonly carry relation semantics in prose. If that capability becomes a live requirement, possible realizations include a serialization, compiler, or graph projection; the present sources do not select one. Until then, this is an unrealized capability, not a prescribed missing component.
- **External review remains limited.** Several governing documents are Draft or Proposed, and the Terminology document explicitly records that sustained external human review has not yet developed ([Terminology → On Independent Verification, Today](../terminology.md#on-independent-verification-today) — **Evidence**).
- **No measured superiority claim is established.** The present comparison has not measured authoring time, navigation tokens, drift rate, round-trip fidelity, or decision quality on a shared corpus.

The defensible conclusion is category-conditioned: **OKF is a lower-ceremony bounded exchange envelope; Memar offers a broader modeling and governance method. This comparison establishes no relative cost or outcome advantage.**

## 6. `type: BigQuery Table`
`BigQuery Table` appears as an example value for OKF's required descriptive `type` field, not as a registered OKF class ([OKF v0.2 §4.1](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/ad30107c31c06aec8a7d5636e0d1058118604e6f/SPEC.md#41-frontmatter) — **Evidence**; [orders example](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/ad30107c31c06aec8a7d5636e0d1058118604e6f/bundles/acme_retail/tables/orders.md) — **Evidence**). Three layers must remain distinct:
1. **OKF field:** `type` is a descriptive value consumers use for routing, filtering, and presentation; unknown values are tolerated.
2. **External catalog label:** `BigQuery Table` is a producer-defined OKF routing label for a BigQuery table. It is neither a registered OKF class nor a Memar Type.
3. **Memar Type:** the string does not become a modeling Type merely because the field is named `type`. A Memar Type requires an independently justified identity and contract ([Type → Definition of Type](../type.md#definition-of-type) — **Evidence**).

If BigQuery lies outside the modeled domain, copying this label into the core model binds an implementation product to that model. If BigQuery-specific behavior is in scope, the label may remain in a bounded integration model when it has independent identity and contract. Preserve the exact label at the layer where it carries the contract; add a prose gloss only when readers need one. The relevant Memar discipline is to keep technology vocabulary from replacing the concept it implements ([Terminology → Technology Terms](../terminology.md#technology-terms) — **Evidence**).

## 7. Technical terms and human language
Replacing a load-bearing identifier with nearby prose can add ambiguity without adding understanding. Preserve the exact identifier at the layer that defines it: a producer-defined OKF label, a Memar-governed term, or a domain-specific canonical term. Human-language explanation belongs beside that identifier when the audience needs it; it does not replace the identifier's contract-bearing role.

Memar already separates these concerns:
- Technical documentation gives ambiguity a higher cost than precise terminology ([Content → Lexical Token vs. Sense](../content.md#lexical-token-vs-sense--handling-ambiguity) — **Evidence**).
- A Type may retain one functional definition while exposing localized human-facing names, labels, and descriptions in companion artifacts ([Type → Human-facing identity](../type.md#human-facing-identity) — **Evidence**).
- Durable project records remain in English while conversation follows the counterpart's usable language ([Documentation → Documentation Language](../documentation.md#documentation-language) — **Evidence**).

OKF can carry UTF-8 and human prose, but its core v0.2 fields do not define a language or terminology-governance profile. It does not by itself solve the Persian/RTL or canonical-term problem.

## 8. Adoption filter
### Already governed or better developed in Memar
- Separation of model, representation, storage, and projections
- Identity independent of location
- Concept-versus-representation discipline
- Typed relationship semantics at the model layer
- Reader-routed facets and separation of current truth from history
- Evidence, prior-art evaluation, research, and deliberate change governance
- Process expectations, checks, authority, and accountability
- Precise treatment of technology-specific and human-facing terminology

### Reject as internal Memar rules
- One domain concept must equal one Markdown file
- File path is the concept's stable identity
- `type` is a producer-defined descriptive routing label, not a model identity or a Memar Type
- OKF core does not standardize typed relationship semantics; a producer extension may supply them
- A broken cross-link does not make an otherwise valid bundle nonconformant; treating it as valid model state would be a separate modeling choice
- Missing status means `stable`
- A free-form body replaces facet-specific reader contracts
- `log.md` replaces per-artifact Changelog, Handoff, or Research

### Conditional external profile
A future Memar-to-OKF export could be useful if an organization needs portable catalog or agent exchange. It would be a projection over the internal model, never the model's authority.

### Separate future research
- A machine-readable freshness or review-expiry envelope
- A portable Attested Computation profile
- A versioned export/import and conformance contract

None has a current live requirement in the documents reviewed here.

## 9. Possible future integration
The following is a comparison-derived architectural inference, not an existing Memar or OKF integration:
1. Memar remains the internal authority for concepts, identity, typed relationships, lifecycle, rationale, and authority.
2. An export compiler projects selected knowledge into an OKF bundle for exchange.
3. Every exported record receives a stable exported identity independent of its bundle path; the path becomes a locator, not identity.
4. A local profile maps selected Memar relationship types to a machine-readable extension rather than relying only on prose.
5. Lifecycle mappings distinguish maturity from freshness and distinguish supersession, refutation, and deletion from absence.
6. Trust metadata remains evidence, while authorization remains an access-control concern.
7. Round-trip tests verify that exchange does not silently collapse Memar distinctions.

This design is justified only if a real cross-tool or cross-organization requirement appears. Adopting it speculatively would add the very ceremony and machinery this comparison finds unnecessary in OKF's core.

## 10. Decision
OKF should not replace Memar's documentation architecture, modeling method, or governing terminology. For a bounded need—portable data-catalog context, a Git-native knowledge bundle, or low-friction exchange with agents and tools that already read Markdown—OKF is a practical and comparatively simple choice.

Memar remains the better conceptual fit when the goal is to develop a system whose concepts, relationships, responsibilities, decisions, evidence, and evolution must remain coherent over time. Its present limitations include the Draft or Proposed status of many governing documents, limited external review, absent export and validation tooling, an unrealized machine-readable graph, and no comparative operational evidence.

No present change to Memar's governing method is warranted from this comparison; that conclusion should be revisited if a live interoperability requirement appears or comparative evidence changes the fit.

## 11. Open for critique
- Whether the comparison gives sufficient weight to OKF's operational simplicity
- Whether any proposed export profile would duplicate or conflict with Memar's protocol layer
- Whether Attested Computation belongs in Process, Protocol, Knowledge, or a separate protocol document
- Whether the source-status discrepancies on the separately maintained `okf.md` site reflect temporary deployment or a broader documentation-governance problem
- Any benchmark that could replace the bounded qualitative judgments about navigation, authoring, and maintenance cost
