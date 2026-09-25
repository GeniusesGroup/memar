# Comparison: Memar and LLM Wiki
This comparison evaluates [LLM Wiki](https://llm-wiki.net/) as a possible architecture framework, a Memar substitute, or an operational complement. It finds that LLM Wiki is a substantial and rapidly developed knowledge-work system, but it does not claim or supply a general method for developing arbitrary systems. It is therefore a **specialization and plausible but unvalidated complement**, not a like-for-like architectural competitor to Memar.

This audit inspected the LLM Wiki repository `master` head [`1224fbcdf3827f4ba56d225a9e359f5e8a5594e5`](https://github.com/nvk/llm-wiki/commit/1224fbcdf3827f4ba56d225a9e359f5e8a5594e5) on 2026-09-25. The commit itself was created on 2026-09-15, immediately after the [v0.25.0 release](https://github.com/nvk/llm-wiki/releases/tag/v0.25.0). The comparison separates project instructions, deterministic implementation, tests, benchmarks, issue reports, and marketing claims. The repository's tests and benchmark protocols were inspected but not executed; no LLM Wiki workflow was installed or run locally.

## Table of contents
- [1. What each project is](#1-what-each-project-is)
  - [LLM Wiki](#llm-wiki)
  - [Memar](#memar)
  - [Category distinction](#category-distinction)
- [2. Is LLM Wiki an architecture competitor?](#2-is-llm-wiki-an-architecture-competitor)
  - [The coverage argument](#the-coverage-argument)
  - [Knowledge construction is not document compilation](#knowledge-construction-is-not-document-compilation)
  - [Domain limitation is not framework incompleteness](#domain-limitation-is-not-framework-incompleteness)
  - [Where the projects genuinely overlap](#where-the-projects-genuinely-overlap)
- [3. Where LLM Wiki is stronger](#3-where-llm-wiki-is-stronger)
- [4. Where Memar is stronger](#4-where-memar-is-stronger)
- [5. Direct conflicts if imported into Memar](#5-direct-conflicts-if-imported-into-memar)
- [6. Costs and limits on both sides](#6-costs-and-limits-on-both-sides)
  - [LLM Wiki](#llm-wiki-1)
  - [Memar](#memar-1)
- [7. What Memar can learn](#7-what-memar-can-learn)
  - [Absorb](#absorb)
  - [Adapt](#adapt)
  - [Reject](#reject)
- [8. Possible relationship](#8-possible-relationship)
- [9. Decision](#9-decision)
- [10. Open for critique](#10-open-for-critique)

## 1. What each project is
### LLM Wiki
LLM Wiki describes itself as an “LLM-compiled knowledge base” in which the agent is both compiler and query engine: raw sources are ingested, synthesized into cross-referenced Markdown articles, and queried from the compiled corpus ([portable protocol](https://github.com/nvk/llm-wiki/blob/1224fbcdf3827f4ba56d225a9e359f5e8a5594e5/AGENTS.md#what-this-is) — **Evidence**). The implemented system includes parallel research, thesis mode, source ingestion, compilation, inventories, datasets, Ideas, Projects, output generation, query profiles, session memory, feedback, audit, librarian, lint, adapters, privacy-sealed checkpoints, and packaging for several coding agents ([README](https://github.com/nvk/llm-wiki/blob/1224fbcdf3827f4ba56d225a9e359f5e8a5594e5/README.md) — **Evidence**).

At the inspected snapshot, LLM Wiki is a host-agent protocol suite plus substantial deterministic local tooling. Research, thesis work, semantic compilation, audit, query, planning, and output generation remain agentic workflows. The Python helpers deterministically implement lint and safe index repair, schema management, archiving, session state, specialist management, adapter controls, retraction, and checkpoint sealing and verification; they do not implement a deterministic semantic compiler.

### Memar
Memar describes itself as a domain-independent framework for developing systems. It governs the concepts, model, terminology, responsibilities, processes, protocols, agency, knowledge, evidence, and decisions through which a system is understood and changed across domains ([Framework → Memar's Purpose Space](../framework.md#memars-purpose-space-from-knowledge-to-agency) — **Evidence**; [Modeling → The Model as the Primary Artifact](../modeling.md#the-model-as-the-primary-artifact) — **Evidence**). Its current live surface is still principally a connected set of governing documents and practices, with implementations and executable services at different levels of maturity.

### Category distinction
LLM Wiki primarily governs **knowledge operations**: source acquisition, synthesis, retrieval, maintenance, review, and artifact production. Memar primarily governs **system development**: what a system is, how its concerns and responsibilities are modeled, how development proceeds, and how concepts remain coherent across implementation and evolution.

The LLM Wiki repository has an architecture—the arrangement of its hub, topics, raw sources, articles, inventories, sessions, outputs, and helpers—but that software architecture is not the same thing as a general architecture method for the systems its users are trying to develop.

## 2. Is LLM Wiki an architecture competitor?
### The coverage argument
The strongest form of the argument against LLM Wiki is not that it implements only one command. It implements a wide range of knowledge and delivery operations. The argument is that its governing model remains bounded to wiki-centered knowledge and delivery operations, while Memar attempts to govern the full path from problem and model through architecture, protocol, implementation, verification, operation, and evolution.

LLM Wiki is not silent on process, implementation, lifecycle, authority, or protocol questions within its own domain. It supplies bounded schemas, a `Concept → Idea → Project` lifecycle, explicit approval gates, an executable adapter protocol, and provenance and audit contracts. What it does not supply is a domain-independent method that turns those mechanisms into an architecture for an arbitrary target system.

Under that comparison, LLM Wiki does not provide general answers to questions such as:
- What entities and responsibilities make up the target system?
- Which concepts deserve independent identity, lifecycle, and contract?
- Which behaviors and structural relations must hold before implementation?
- Which agents hold authority, what capabilities may they use, and who is accountable?
- Which process expectations precede implementation, and which checks verify an instance?
- Which protocols govern interaction, and how is conformance established?
- How does the architecture evolve when implementation or evidence changes?

LLM Wiki's `schema.md`, compilation protocol, and lifecycle organize one knowledge system's artifacts well. They do not model an arbitrary system being developed.

### Knowledge construction is not document compilation
The strongest objection to calling LLM Wiki a complete knowledge system appears when its output is intended to be a **handbook or durable reference**. In that use, the wiki must do more than preserve and synthesize what sources happen to say. It must help a reader understand the structure of the subject, distinguish its concepts, relate them, identify what is uncertain, and know which omissions or contradictions matter.

LLM Wiki has real ingredients for this: it extracts concepts and relationships, maintains a topic guide, preserves sources, records disagreements, creates bidirectional links, performs audits, and can require human approval. But the compiler's explicit output is primarily a set of Markdown articles and operational records. Its topic-local `schema.md` can define entity types, relationship verbs, article subtypes, and source boundaries, so the corpus may be coherent and more than a collection ([Wiki Structure → Topic Guide (`schema.md`) Format](https://github.com/nvk/llm-wiki/blob/1224fbcdf3827f4ba56d225a9e359f5e8a5594e5/claude-plugin/skills/wiki-manager/references/wiki-structure.md#topic-guide-schemamd-format) — **Evidence**). What it does not establish or enforce is a separately governed domain model with explicit concept admission, relation semantics independent of prose, lifecycle boundaries, and model-level completeness and evolution rules. The absence of those guarantees limits the strength of the claim; it does not reduce the corpus to a mere collection.

That distinction matters, and two kinds of authority must be separated. If “authoritative” means a trusted, source-grounded reference within a bounded domain, LLM Wiki's provenance, review, audit, freshness, and human-approval mechanisms can provide **evidentiary authority** without a formal model. If it means the governing domain model from which future readers reason, then compilation alone leaves a real gap: the system has organized material without separately establishing and continuously revising the model that gives the material its structure. Under that second, stronger meaning of handbook/reference, the user's criticism is substantive, not merely a complaint about specialization.

To close that second gap, LLM Wiki would need an explicit model-building layer: discovery of concerns and responsibilities; criteria for independent concepts and boundaries; typed or explicitly defined and semantically stable relations; assumption and contradiction handling; model completeness and evolution checks; and a defined relationship between the model and the article projection. None of these needs to make the tool a general architecture framework, but without them its strongest justified claim is “source-grounded compiled handbook with article-level curation,” not “separately governed domain model.”

### Domain limitation is not framework incompleteness
Calling LLM Wiki a “micro-framework” or “fragment” because it specializes in knowledge work is not a valid inference. A focused framework can be complete and coherent within its own domain. The relevant Memar criterion is the **degree of silence within the declared domain**: does a developer repeatedly need to leave the framework for foundational decisions the framework intended to govern? ([Framework → What Makes a Framework Complete?](../framework.md#what-makes-a-framework-complete) — **Evidence**).

So the precise conclusion is narrower than “it is too small”:
- For general development of software, hardware, organizations, or other systems, LLM Wiki is not a sufficient architecture framework.
- For building and operating a research/knowledge corpus with AI agents, it is a serious and substantial bounded system.
- The fact that it does not govern every domain does not make its own domain implementation defective.

### Where the projects genuinely overlap
The projects do compete for part of the practical terrain. LLM Wiki covers projects, plans, outputs, checkpoints, lessons, feedback, research artifacts, and decision-shaped Ideas. A research-heavy team may use it as a practical substitute for parts of Memar's knowledge continuity, documentation support, and inquiry recording. That does not make its checkpoint a Memar Handoff or its research output a Memar Research artifact; a checkpoint may supply input to a Handoff, for example, without being one.

That is a practical overlap in knowledge operations—not evidence that LLM Wiki is a complete substitute for Memar's system-development model.

## 3. Where LLM Wiki is stronger
LLM Wiki is more operationally concrete than Memar in several areas:
1. **A working local knowledge system.** It provides a concrete hub/topic layout, normally immutable raw sources with an explicit retraction path, compiled articles, inventories, dataset manifests, session state, generated indexes, outputs, archive, and logs. The behavior is specified well enough to create, inspect, lint, and maintain a corpus.
2. **A concrete host-agent research workflow.** Standard, deep, and retardmax modes use 5, 8, and 10 agents respectively; planning mode can multiply additional path-level batches. Thesis mode separates supporting, opposing, mechanistic, review, and adjacent evidence, and multi-round research reflects over gaps and prior findings. Memar's Research facet specifies how a deliberate inquiry is recorded, not a competing research method, so this is an operational strength rather than a simple stronger-versus-weaker comparison.
3. **Deterministic structural verification.** The local helper checks frontmatter, placement, indexes, Markdown links, source resolution, orphans, freshness, archive state, and project structure. The test suite includes golden fixtures, one-defect fixtures, packaging sync tests, token budgets, and deterministic CLI checks ([tests/README](https://github.com/nvk/llm-wiki/blob/1224fbcdf3827f4ba56d225a9e359f5e8a5594e5/tests/README.md) — **Evidence**).
4. **Query isolation and lane-specific benchmarks.** Compact query profiles are instruction-level read-only contracts. Claude's command and the Pi launchers narrow the available tool surface, while OpenCode and portable-agent enforcement still depends on host permissions. Static checks measure bytes or characters; the Codex app-server lane measures reported token, cache, TTFT, and latency metrics; the Claude lane additionally measures reported cost; and the DS4 lane measures exact serialized provider bytes and includes exact-citation and abstention cases. All live lanes gate fixture reads and fixture immutability ([Benchmarks](https://github.com/nvk/llm-wiki/blob/1224fbcdf3827f4ba56d225a9e359f5e8a5594e5/benchmarks/README.md) — **Evidence**). The [official site](https://llm-wiki.net/) additionally reports a controlled DS4 AB/BA reduction from 216,640 to 77,338 serialized provider bytes (64.30%), with fixture-read, citation, abstention, and no-mutation checks passing; this is a maintainer-reported result, not independently reproduced here, and it does not establish general synthesis or answer quality.
5. **Human and machine approval boundaries.** Research plans, schema deviations, Idea promotion, checkpoint overrides, remote writes, skill installation, and publication are separated into explicit decisions. Remote adapter writes require an approved plan hash, expected revision, idempotency key, private receipt, and read-back verification ([Adapter Protocol](https://github.com/nvk/llm-wiki/blob/1224fbcdf3827f4ba56d225a9e359f5e8a5594e5/claude-plugin/skills/wiki-manager/references/adapters.md) — **Evidence**).
6. **Privacy-aware session memory.** Session capture is separated from topic evidence; raw transcripts are off by default; redaction, opt-out, explicit promotion, and operational-versus-curated knowledge boundaries are explicit ([Session Context Capture](https://github.com/nvk/llm-wiki/blob/1224fbcdf3827f4ba56d225a9e359f5e8a5594e5/claude-plugin/skills/wiki-manager/references/sessions.md) — **Evidence**).
7. **Privacy-sealed project checkpoints.** The five-file checkpoint records selected inputs, declared section mappings, omissions, hashes, a thin-output floor, deterministic privacy findings, and exact overrides. Semantic coverage and privacy minimization remain agent-performed. The deterministic seal checks structure, integrity, declared coverage consistency, thinness, and scanner findings; it does not prove truth or semantic completeness ([Checkpoint reference](https://github.com/nvk/llm-wiki/blob/1224fbcdf3827f4ba56d225a9e359f5e8a5594e5/claude-plugin/skills/wiki-manager/references/checkpoints.md) — **Evidence**; [checkpoint workflow](https://github.com/nvk/llm-wiki/blob/1224fbcdf3827f4ba56d225a9e359f5e8a5594e5/claude-plugin/commands/checkpoint.md) — **Evidence**). This is a strong bounded export for project knowledge, although it is not the same artifact as Memar Handoff.
8. **Multi-runtime packaging with a canonical Claude skill.** Claude's wiki-manager skill is the behavioral source for generated Codex and OpenCode mirrors and the compact query profiles. Codex copies the references, OpenCode retains a symlink, and Pi query launchers use the generated query profile. The root `AGENTS.md` is a separately maintained portable protocol; synchronization tests do not prove behavioral parity for that file, and the OpenCode remote-reference limitation remains open ([README → Claude-First, Multi-Runtime](https://github.com/nvk/llm-wiki/blob/1224fbcdf3827f4ba56d225a9e359f5e8a5594e5/README.md#claude-first-multi-runtime) — **Evidence**; [Issue #104](https://github.com/nvk/llm-wiki/issues/104) — **Evidence**).

These are substantial strengths. A fair comparison must not minimize them by calling the project “just Markdown” or “just prompts.”

## 4. Where Memar is stronger
Memar is stronger where the target is a coherent model and method rather than a bounded knowledge corpus:
1. **Model before representation.** LLM Wiki treats compiled articles as its default factual layer. Under Memar's model, those articles remain representations whose semantic fidelity must be evaluated rather than assumed; article categories and frontmatter do not by themselves establish that the compiled structure is the natural model of the domain. If the wiki is intended to serve as the governing model for future reasoning, this is a material limitation rather than a minor implementation difference; a trusted, bounded source-grounded reference is a different and supportable claim. Memar makes the model the primary architectural artifact and treats implementation as its projection ([Modeling → The Model as the Primary Artifact](../modeling.md#the-model-as-the-primary-artifact) — **Evidence**).
2. **Independent responsibility and lifecycle as admission criteria.** LLM Wiki's topic guide decides article cardinality and boundaries for corpus organization. Memar asks a different question: whether a domain concern warrants an independent abstraction with its own responsibility, behavioral boundary, identity, or lifecycle. Having an article and having a Memar abstraction are not equivalent admission decisions ([Modeling → Concept Existence vs. Model Existence](../modeling.md#concept-existence-vs-model-existence) — **Evidence**).
3. **Concept-versus-representation discipline.** LLM Wiki already distinguishes global article categories, storage frontmatter types, and topic-local entity types. An integration must not map those local mechanisms automatically to Memar Types; only independently justified domain concerns may become Memar Types. Memar does not allow a convenient representation to become the model's conceptual authority merely because it is useful for navigation ([Content → What “Content” Means Here](../content.md#what-content-means-here-and-what-this-document-is-not) — **Evidence**).
4. **A continuous project model across domains.** One-topic isolation can make shared concept identity harder, but LLM Wiki already provides multi-wiki peek, `--with` context, a hub-wide portfolio, Idea `related_wikis`, and cross-topic checkpoint selection. Memar adds the requirement that an integration preserve one continuous project model across those surfaces; it does not by itself prove that topic directories necessarily partition the model ([Knowledge → A Project Carries One Continuous Mental Model](../knowledge.md#a-project-carries-one-continuous-mental-model) — **Evidence**).
5. **Process before mechanism.** LLM Wiki already encodes bounded processes, participants, ordering, gates, outcomes, failure handling, and authority boundaries. Memar contributes a more general distinction between Process and Mechanism, prior expectations and checks, and a framework for deciding which mechanism realizes a process. The difference is generality and abstraction, not the absence of process engineering ([Process → Expectations and Checks](../process.md#expectations-and-checks) — **Evidence**).
6. **Agency, authority, capability, and accountability.** LLM Wiki encodes concrete participants, approval boundaries, scoped tools, and trust checks. Memar contributes a broader model that distinguishes responsibility, authority, capability, delegation, trust, verification, and accountability ([Agency → Responsibility](../agency.md#responsibility) — **Evidence**; [Agency → Authority](../agency.md#authority) — **Evidence**). The difference is again generality, not the absence of governance mechanics.
7. **Protocol and conformance as architectural concepts.** LLM Wiki's adapter protocol already has manifests, handshakes, scoped effects, approvals, receipts, read-back verification, and tests. Memar contributes a broader ontology in which a Protocol is a named set of declarative rules governing one or more processes. External observability is a claimed consequence, while checkable conformance remains a working hypothesis and open question in the current Proposed document. This broader ontology also distinguishes a Protocol from any one API or implementation contract ([Protocol → What is a Protocol?](../protocol.md#what-is-a-protocol) — **Evidence**).
8. **Reader-routed documentation and durable inquiry.** LLM Wiki's operation log, research output, checkpoint, and session digest are useful artifacts, but they do not carry Memar's full distinctions among current explanation, executable practice, change rationale, resumable discussion state, and a Research record with standing, methodology, findings, and conclusion ([Documentation → Facets currently defined](../documentation.md#facets-currently-defined) — **Evidence**).

## 5. Direct conflicts if imported into Memar
The following LLM Wiki mechanisms should not become Memar rules merely by imitation:
- **One topic, one wiki** may be a useful operational boundary, but it is not a universal knowledge-model rule. LLM Wiki already mitigates isolation through sibling-index peeks, `--with`, a portfolio, related-Idea links, and cross-topic checkpoints. The remaining risk is that shared identity and ownership stay inconsistent across those surfaces; Memar would require an integration to preserve one continuous model.
- **Portable paths are not stable semantic identity.** LLM Wiki already prefers a portable `hub_path` and relative topic paths over machine-specific absolute paths. Issue #102 identifies the remaining gap: registry resolution trusts a valid path as the named wiki and has no opaque `wiki_id` check capable of detecting resolution to the wrong copy ([Issue #102](https://github.com/nvk/llm-wiki/issues/102) — **Evidence**: issue report, not independently reproduced). Memar requires identity independent of location.
- **Article `confidence: high|medium|low` is not a general epistemic model.** It is an article-level operational label based on source credibility and corroboration; source disagreement is collapsed into `low`, while claim-level uncertainty and other epistemic dimensions are not represented. Issue #94 proposes a finer ordinal scale, not a multidimensional epistemic model ([Issue #94](https://github.com/nvk/llm-wiki/issues/94) — **Evidence**). Separately, the [structure contract](https://github.com/nvk/llm-wiki/blob/1224fbcdf3827f4ba56d225a9e359f5e8a5594e5/claude-plugin/skills/wiki-manager/references/wiki-structure.md) describes `verified` as the last human confirmation, while the [compile workflow](https://github.com/nvk/llm-wiki/blob/1224fbcdf3827f4ba56d225a9e359f5e8a5594e5/claude-plugin/commands/compile.md#55-self-validation-pass) instructs the agent to set it to the current date. Freshness therefore cannot be assumed to attest human review unless a human actually performed that review.
- **Source-level provenance is not claim-level verification.** Requiring a compiled article to cite raw sources is valuable, but a source list does not prove that each claim follows from the cited material. Issue #91 reports that footnotes and wikilinks are not validated. Unresolved footnotes leave citation-shaped claim-to-evidence edges without definitions, while unresolved wikilinks leave article-to-article cross-references that appear valid but do not resolve ([Issue #91](https://github.com/nvk/llm-wiki/issues/91) — **Evidence**).
- **A generated wiki article is not automatically validated knowledge.** LLM Wiki treats compiled articles as its default factual layer. Under Memar's model, they remain representations whose semantic fidelity must be evaluated. LLM-mediated synthesis and structural checks do not by themselves establish that every claim is true; human review, source inspection, and later contradiction checking remain necessary.
- **Generated indexes and caches are projections, not authoritative inventories.** They are useful and should remain rebuildable; importing them as governing knowledge would invert the model/storage relation.
- **Local categories and labels must not become Memar Types automatically.** LLM Wiki already distinguishes article categories, storage frontmatter types, and topic-local entity types. An integration must map only independently justified domain concerns to Memar Types; the local mechanisms alone do not establish identity, responsibility, or contract.
- **Automatic repair must not hide unresolved ownership.** Issue #90's concern is not that the catch-all page falsely claims synthesis—it is labeled a low-confidence backlog. The concern is that `--fix` routes all unresolved sources into one reference, does not identify an owning article, and can make lint pass without resolving dependency ownership ([Issue #90](https://github.com/nvk/llm-wiki/issues/90) — **Evidence**).
- **Quotas must not pressure knowledge generation.** An open issue reports that “find at least two lessons” guidance can encourage fabrication and that the lessons workflow lacks an explicit secret/PII redaction rule ([Issue #93](https://github.com/nvk/llm-wiki/issues/93) — **Evidence**). A correct count can be zero.
- **Default-on session capture requires explicit authority and privacy analysis.** Trusted hooks omit raw prompt, tool-output, and transcript bodies and redact selected key/value patterns, but they still persist cwd, Git remote and branch, transcript path, event metadata, and sometimes a redacted feedback preview and text hash. Regex redaction reduces exposure; it does not make the session store private in every environment or eliminate metadata leakage.
- **The adapter boundary is not an operating-system sandbox.** LLM Wiki correctly says its registry, path checks, hashes, and approval receipts are additional controls; the host process permissions remain the real enforcement boundary ([Adapter Protocol → Security properties and limits](https://github.com/nvk/llm-wiki/blob/1224fbcdf3827f4ba56d225a9e359f5e8a5594e5/claude-plugin/skills/wiki-manager/references/adapters.md#security-properties-and-limits) — **Evidence**).

## 6. Costs and limits on both sides
### LLM Wiki
LLM Wiki's operational strength also creates real costs:
- **The semantic engine is host-LLM dependent.** Deterministic helpers implement structural and operational controls, including lint, safe index repair, schema and archive management, session state, specialist management, adapter controls, retraction, and checkpoint sealing. Research, thesis work, semantic compilation, audit, query, planning, and output remain agentic workflows whose quality depends on the selected model, tool access, context, and host permissions.
- **“Any AI agent” is a portability goal, not a uniform guarantee.** A portable `AGENTS.md` needs a host that can follow it and supply the required read, search, edit, shell, and web tools. OpenCode live behavior is explicitly best effort, and an open issue reports broken remote reference loading through the OpenCode symlink path ([Issue #104](https://github.com/nvk/llm-wiki/issues/104) — **Evidence**).
- **The semantic layer is not fully verified.** Lint is strong on structure; audit and librarian are agentic. The project does not claim that mechanical checks prove factual correctness.
- **The corpus model can fragment.** One topic per wiki improves focus, and LLM Wiki supplies multi-wiki peeks, `--with`, a portfolio, related-Idea links, and cross-topic checkpoints. The remaining risk is inconsistent shared-concept identity and ownership across those surfaces.
- **The workflow surface is large and fast-moving.** A 0.x project with many commands, generated runtime packages, adapters, session hooks, and compatibility paths has substantial maintenance and cognitive cost.
- **The benchmark does not prove output quality generally.** Its controlled lanes are useful for context and no-mutation regressions; they do not establish that synthesized knowledge is correct across arbitrary topics.
- **Public assurance is not fully visible in the target tree.** The inspected tree has no active `.github/workflows`; `tests/ci/plugin-tests.yml` is a copy-in template. Even if activated, the template invokes 12 of the 15 deterministic suites named by the project's development contract, omitting the adapter, retract, and Codex runtime suites ([development contract](https://github.com/nvk/llm-wiki/blob/1224fbcdf3827f4ba56d225a9e359f5e8a5594e5/CLAUDE.md#testing) — **Evidence**; [workflow template](https://github.com/nvk/llm-wiki/blob/1224fbcdf3827f4ba56d225a9e359f5e8a5594e5/tests/ci/plugin-tests.yml) — **Evidence**). The v0.25.0 claim that all 15 passed remains maintainer-reported rather than independently reproduced here.
- **The project is young.** Rapid development and visible issue traffic are not defects, but they limit how much maturity can be inferred from adoption or version cadence.

### Memar
Memar's conceptual breadth also creates costs:
- **Less operational machinery.** It lacks an end-to-end compiler, linter, research engine, session store, checkpoint service, and multi-runtime packaging comparable to LLM Wiki.
- **Higher authoring and navigation discipline.** Facets, companions, definitions, review state, and propagation can be cognitively and operationally heavier than a topic-local schema and command set.
- **Many governing documents remain Draft or Proposed.** The comparison does not establish framework completeness; the current document set itself has open questions and limited sustained external review.
- **Concepts are not yet realized as a complete machine-readable model.** Typed relationships and stable identity are governing principles, but the current documentation surface does not provide a comprehensive graph and conformance implementation.
- **No comparative operational evidence exists.** This review has not measured authoring time, research quality, drift, token cost, maintenance, or decision quality on a shared project.

The fair conclusion is symmetric: **LLM Wiki has more machinery and less conceptual breadth; Memar has more conceptual breadth and less finished machinery.**

## 7. What Memar can learn
### Absorb
The following patterns strengthen concerns Memar already owns and can be adopted without importing the whole product:
- Keep raw source material immutable in normal workflows, with a governed retraction path, and distinct from synthesized knowledge and generated outputs.
- Treat indexes and caches as disposable projections.
- Require source paths, revisions, and hashes where external material is compiled into durable claims.
- Use deterministic checks for frontmatter, placement, links, provenance resolution, coverage, and unsafe repair candidates.
- Keep semantic audit separate from structural lint; do not let one substitute for the other.
- Keep full write workflows separate from compact read-only query profiles.
- Make privacy, session capture, promotion into curated knowledge, and opt-out explicit.
- Bind consequential external actions to a declared plan, exact approval, scoped effect, idempotency, receipt, and read-back verification.

### Adapt
- Use the research loop—plan, independent paths, credibility review, counterevidence, gaps, synthesis, and reflection—as a candidate methodology recorded in a Memar Research artifact, and adapt its reusable orchestration, expectations, and gap-handling rules into Process practice.
- Adapt checkpoint sealing, coverage-manifest, and privacy controls into a bounded export artifact. When useful, use a generated checkpoint as input to a Memar Handoff, not as the Handoff itself.
- Adapt `Concept → Idea → Project` as a decision/delivery lifecycle, while keeping a Project linked to Memar model, protocol, implementation, and verification artifacts rather than treating the output folder as the project itself.
- Adapt host-neutral packaging as an implementation of Memar's one-model-many-projections principle, while treating the canonical Claude skill, generated mirrors, and portable `AGENTS.md` as distinct artifacts whose behavioral parity must be tested rather than assumed.
- Adapt personal specialist methods as bounded review protocols with version and content-hash provenance, never as credentials or ambient authority.

### Reject
- Do not replace Memar's model-first method with page-first knowledge compilation.
- Do not make topic directories the universal identity or ownership boundary.
- Do not import a coarse confidence enum as Memar's general uncertainty model.
- Do not use source lists as a substitute for claim-level evidence.
- Do not let prompt quotas pressure fabrication, or let catch-all pages and auto-repair hide unresolved ownership.
- Do not call a Markdown instruction file a deterministic implementation of semantics.
- Do not treat privacy redaction, trust, or an agent prefix as a complete security or authority model.
- Do not replace Memar with LLM Wiki because the latter produces useful artifacts more quickly.

## 8. Possible relationship
The architecturally consistent relationship is:

1. **Memar remains the authority** for concepts, terminology, model, identity, typed relationships, process, protocol, agency, evidence, and lifecycle.
2. **LLM Wiki acts as an external knowledge-operations implementation** for source ingestion, compilation, querying, freshness, review queues, session continuity, and bounded project export. If its output is used as a handbook, that handbook is a source-grounded projection of the model, not a substitute for the model.
3. **The LLM Wiki corpus is a projection of the model**, not the model's source of truth.
4. **An explicit integration contract is required** before compatibility can be claimed. It must govern identity independent of path, typed relation mapping, provenance and claim verification, authority and human review, lifecycle, privacy, and conformance.
5. **Round-trip tests must prove that integration does not collapse Memar distinctions** such as source versus knowledge, article versus concept, inventory versus evidence, project output versus implementation, and session memory versus canonical knowledge.

Without such a contract, “Memar implemented with LLM Wiki” would mean an agent workflow that follows some Memar documents—not that LLM Wiki realizes Memar.

## 9. Decision
LLM Wiki is not a like-for-like architecture competitor to Memar. It is a serious, useful, and rapidly evolving specialization in wiki-centered knowledge and delivery operations. It covers many operational needs and may substitute for parts of a research-heavy knowledge-and-delivery stack, but this audit provides no comparative evidence that it replaces such a stack as a whole. It does not replace Memar's model of general system development.

The user's criticism is correct in the stronger sense when the wiki is intended to be the governing handbook or reference for future reasoning: **without an explicit, separately maintained model-building layer, the output remains source-grounded synthesis and article-level curation rather than a governed domain model.** That is a real gap under that intended use, even though LLM Wiki can provide valuable evidentiary authority as a bounded, reviewable reference. The separate claim that bounded focus automatically makes the project a “fragment” does not follow. The fair classification is **a substantial source-grounded knowledge-work specialization and a plausible but unvalidated operational complement, not a complete governed domain-model construction or general architecture framework**.

On the evidence inspected, this audit does not justify changing Memar's governing method. Individual LLM Wiki patterns remain candidates for separate, bounded inquiry—particularly deterministic documentation checks, privacy-sealed checkpoints, and the research loop—rather than grounds for wholesale adoption.

## 10. Open for critique
- Whether the comparison gives sufficient credit to LLM Wiki's operational completeness within its domain
- Whether Memar should eventually ship comparable deterministic helpers rather than leaving them to consuming projects
- Which LLM Wiki mechanisms are genuinely reusable without importing its topic-silo and file-oriented model
- Whether the proposed integration boundary is useful or merely another speculative profile
- Comparative evidence on a shared corpus remains absent; this document establishes a category and adoption judgment, not measured superiority
- Whether a future LLM Wiki release will add an explicit domain-model layer rather than only improving article compilation and curation
