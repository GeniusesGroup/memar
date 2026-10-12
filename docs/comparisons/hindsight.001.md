# Comparison: Memar and Hindsight
**Compared project:** [vectorize-io/hindsight](https://github.com/vectorize-io/hindsight)
**Inspected at:** commit [`44ac64e`](https://github.com/vectorize-io/hindsight/commit/44ac64e) ("feat(hermes): let the integration name a retain strategy"), local checkout under `_refs/hindsight`.
**Method:** two independent read-only passes over the checkout — one on the memory method (retain/recall/reflect, consolidation, banks), one on architecture, evals, and distribution — cross-checked against Memar's live `docs/`. Nothing was executed, installed, or benchmarked; every claim about Hindsight below is a claim about what its files say or what its code contains. Where a claim is inference rather than something the repository states, it is labeled.

## Table of contents
- [1. What each project is](#1-what-each-project-is)
  - [Hindsight (self-definition)](#hindsight-self-definition)
  - [Memar (self-definition)](#memar-self-definition)
  - [Category distinction](#category-distinction)
- [2. Source status and maturity](#2-source-status-and-maturity)
- [3. What Hindsight has that Memar does not](#3-what-hindsight-has-that-memar-does-not)
- [4. Where Memar is stronger](#4-where-memar-is-stronger)
- [5. Limits and failure modes in Hindsight](#5-limits-and-failure-modes-in-hindsight)
- [6. Costs and limits on both sides](#6-costs-and-limits-on-both-sides)
- [7. What Memar can learn](#7-what-memar-can-learn)
  - [Absorb](#absorb)
  - [Adapt](#adapt)
  - [Reject](#reject)
  - [Separate research](#separate-research)
- [8. Possible relationship](#8-possible-relationship)
- [9. Decision](#9-decision)
- [10. Open for critique](#10-open-for-critique)

## 1. What each project is
### Hindsight (self-definition)
Hindsight calls itself "an agent memory system built to create smarter agents that learn over time. Most agent memory systems focus on recalling conversation history. Hindsight is focused on making agents that learn, not just remember" (`README.md:22-24`). Its thesis is that alternatives — RAG, knowledge graphs, conversation recall — are insufficient, and that it delivers state-of-the-art performance on long-term memory tasks (`README.md:28`). It reports top LongMemEval scores, independently reproduced by university and press collaborators, and production use at large enterprises (`README.md:44-52`).

What it ships toward that purpose is three operations over isolated memory stores: `retain` (LLM fact extraction into typed facts), `recall` (four-strategy parallel retrieval fused and reranked), and `reflect` (an agentic loop that returns an answer, not memories) — with background consolidation of facts into evidence-bearing observations and standing mental models served as readable pages.

### Memar (self-definition)
Memar is a domain-agnostic framework for developing systems, not only software — "a framework for developing any system, including software, hardware, buildings, and organizations" ([Framework](../framework.md) — **Evidence**). It states its own purpose as a chain, Knowledge → Thinking → Intelligence → Agency → Goals ([Framework → Memar's Purpose Space](../framework.md#memars-purpose-space-from-knowledge-to-agency) — **Evidence**), and its own model of work as: the model is the primary architectural artifact, contracts live in documents, and generative work lives in callable modules ([Knowledge → Knowledge and Code](../knowledge.md#knowledge-and-code) — **Evidence**).

Memar's knowledge principles are "intentionally principle-level; implementation belongs to domain-specific projects" ([Knowledge](../knowledge.md) — **Evidence**, `knowledge.md:12`). Memar ships no extractor, no retriever, no reranker, and no running memory service.

### Category distinction
The two projects answer different questions, and the questions are not adjacent.

- Hindsight's question: **how can an AI agent learn over time — not merely recall — with production-grade accuracy, latency, and operations?**
- Memar's question: **what shared model of systems and knowledge is this work conducted inside, and how does that model stay coherent as the system changes?**

Hindsight is, in Memar's terms, a sub-framework and product: a bounded, valuable slice (agent memory) that leaves modeling, process, terminology governance, and full-system decisions silent. A team can develop an agent system inside Memar and use Hindsight as that system's memory. Neither replaces the other.

## 2. Source status and maturity
The inspected checkout is a large, actively developed monorepo: 18 `hindsight-*` packages (API, slim API, bundles, npm manager, control-plane UI, Rust CLI, four generated SDK clients, docs, integrations, embed, extensions, tools, dev, two eval suites, integration tests), five agent skills, 55 integration directories against a "60+" claim (`README.md:239` — verified count 55 code dirs; the docs site lists 62 integration pages, so the claim is docs-count-true and code-dirs-short), nine quality-eval suites, 71 blackbox system-test stories, and on the order of six hundred mechanism tests in the slim API package.

Two structural facts bound every claim below. First, benchmark and cookbook surfaces partly resolve off-repo: in-repo LongMemEval/LoCoMo runners were removed in favor of an external benchmark monorepo, the cookbook directory is a pointer to an external repository, and continuous performance monitoring lives on an external site. This is stated in the repository, not hidden — but it means the headline accuracy claims cannot be re-derived from the checkout alone. Second, the project's own eval documentation records live failure modes (paraphrase drift, synthesis wiping prior facts, schema-forced fabrication, language drift, reflect extrapolation) with unusual frankness. That frankness is credited in section 3; it also sets the ceiling for what "learn, not just remember" can presently mean.

## 3. What Hindsight has that Memar does not
Stated as genuine strengths, each with the evidence that supports it. This is an inventory, not a shopping list — the filter is in section 7.

1. **Three executable memory operations with a real contract.** `retain`, `recall`, and `reflect` are API endpoints with clients in four languages, an MCP endpoint per bank, and a two-line LLM wrapper — not prose recipes for remembering. Memar names Knowledge as the material thinking operates on and prescribes "generative work belongs in callable services" without shipping any service; Hindsight is what such a service looks like when built.
2. **Retrieval as engineered fusion, not single-query hope.** Four strategies (semantic, keyword BM25, graph, temporal) run in parallel and merge through reciprocal-rank fusion plus cross-encoder reranking under a token budget. Memar's "relationships as first-class citizens" states the need; Hindsight prices it in scorers, fusion weights, and truncation rules.
3. **Consolidation with evidence attached.** Background workers merge related facts into observations carrying exact quotes and proof counts, refined rather than overwritten, and compile standing answers into mental models readable without retrieval or LLM calls. This is the closest running instance in this folder's comparisons to Memar's "explicit context recovery" and "task-centric evolution" — done by workers and schemas rather than by discipline alone.
4. **Isolation and shaping as first-class configuration.** Banks are strictly isolated memory stores; mission, directives, and disposition traits (skepticism, literalism, empathy on 1–5 scales) shape `reflect` without touching `recall`. The recall/reflect split — retrieval stays neutral, shaping happens at answer time — is a clean architectural decision Memar's agency discussion could learn from without importing any of its machinery.
5. **A three-tier eval story with the seams labeled.** Deterministic blackbox system tests on stubs (exact equality, run on forks), quality evals on real models with LLM judges (explicitly *not* on PRs, daily schedule, judge-must-differ-from-test-model rule), and external benchmarks kept in exactly one repo with a pinned ref ("a second copy is how two copies drift"). Memar's Test protocol owns the epistemic half of this (what a passing suite establishes); Hindsight owns the operational half Memar lacks (which tier runs when, against what, judged by whom).
6. **Self-incriminating eval documentation.** The system-evals README records delta-refresh wiping facts, strict schemas fabricating unstated fields, paraphrase breaking exact-match labels, per-language drift, and reflect extrapolating beyond the bank — each with the mechanism that caused it. Of every project compared in this folder, this is the most instructive failure catalog, and the most transferable asset: it shows what "learning" costs when the learner is a probabilistic paraphraser.
7. **Production operations for a stateful service.** Hierarchical configuration (global → tenant → bank), dual-dialect migrations, embedded and external Postgres, memory-defense redaction over 45 secret/PII patterns, webhooks, extension slots, cost tracing per LLM call, fifteen compose variants, a Helm chart, and a managed cloud. Memar's ZeroOps and minimum-dependency goals point the other way; the contrast is honest about what a memory product must carry.

## 4. Where Memar is stronger
1. **Knowledge against paraphrase.** Memar's standing claim is that "a document is a frozen projection of knowledge" and a system storing documents while losing context, relationships, and rationale "has lost knowledge while keeping its artifacts intact" ([Knowledge](../knowledge.md) — **Evidence**, `knowledge.md:12`). Hindsight's own evals demonstrate the failure from inside: extraction paraphrases facts, synthesis from a new batch alone rewrites standing pages, and unstated fields get fabricated to satisfy a schema. A memory that refines beliefs by rewriting them is a memory that can unlearn true things — Memar's append-only changelog, handoff records, and research companions exist precisely because refinement-by-rewrite is lossy.
2. **One continuous mental model against five channels times sixty integrations.** Hindsight teaches its method through commands, skills, agent-context files, MCP, native hooks, five skills, 55+ integration shims, and a plugin matrix — the same five-channel fragmentation the spec-kit comparison documented, with list drift already visible (55 code dirs vs 62 docs pages vs "60+"). Memar's rule — one continuous mental model; adapters may multiply, the model must not ([Documentation — Comparison → Standing principles](../documentation-comparison.md#standing-principles-these-comparisons-assume)) — predicts this drift rather than discovering it.
3. **Design space against retrieval tuning.** Memar's Framework question — *what kinds of solutions are allowed?* ([Framework](../framework.md) — **Evidence**, `framework.md:59`) — has no counterpart: no modeling gate, no terminology authority, no statement of out-of-bounds solutions. `fact`, `observation`, `mental model`, `bank`, and `reflect` mean what the code does with them, and two consuming projects cannot appeal anywhere when their meanings diverge.
4. **Provenance of decisions against provenance of operations.** Hindsight tracks what was computed from what (op lineage, proof counts, freshness). Memar tracks what was *decided, rejected, and why* across sessions. These are different provenances serving different accountabilities, and only the second lets a later reader reconstruct why the system is the way it is.

## 5. Limits and failure modes in Hindsight
Stated without calling the project worthless — these are failure modes when it is treated as a development framework.

1. **Refinement can destroy knowledge.** The delta-refresh episode (a standing page rewritten from one new batch, prior deployed-release facts wiped, customer counts collapsed) is not a bug in one worker; it is the structural risk of consolidation-by-rewrite. Any team treating consolidated pages as the project's memory inherits silent unlearning with no tombstone.
2. **Schemas that compel fabrication.** A strict extraction schema with mandatory when/where/who/why fields produced invented values when the source stated none. A memory system that prefers complete records over honest gaps manufactures the past it claims to preserve — the exact failure Memar's "ask rather than assume" norm exists to prevent.
3. **Marketing ahead of the checkout.** "Eliminates the shortcomings of RAG and knowledge graphs" has no controlled ablation in-repo; "most accurate ever tested" and "Fortune 500 in production" resolve to vendor-run numbers plus external reproduction notes and an off-repo monitor. The numbers may be right; the checkout does not let a reader check, and a framework comparison must price what it can verify.
4. **Count drift as fragmentation symptom.** 55 integration directories, 62 docs pages, "60+" in the README, duplicate rows in the integrations table (Roo Code and Google ADK listed twice), and a cookbook that is a hyperlink. Individually trivial; jointly, the predictable output of one model projected through many channels with nothing reconciling them.
5. **A full-stack dependency surface.** Provider keys or local models, embeddings, rerankers, Postgres or Oracle, background workers that bill through the night on 30–90k-token prompts, fresh-database-per-eval discipline to avoid stale-bank token blowups. Against Memar's minimum-dependency and ZeroOps direction this is not a flaw — a memory product cannot be dependency-free — but it fixes the floor: adopting Hindsight means adopting its stack, its bills, and its ops.
6. **Single bank per request; composition is the client's job.** Multi-bank orchestration, auth/tenancy/storage choices, and the modeling/process/terminology layers are all left to extensions, images, or the consuming project. Correct scoping for a subsystem; disqualifying as a framework.

## 6. Costs and limits on both sides
### Hindsight
- Memory is paraphrase with evidence attached: powerful retrieval and consolidation over a substrate that can silently rewrite, fabricate, drift language, and extrapolate — all documented by the vendor itself.
- Distribution breadth (18 packages, four SDK languages, plugins, Helm, cloud) with the drift breadth brings.
- Headline claims that resolve off-repo; a reader of the checkout alone cannot re-derive them.
- An always-on LLM, vector, reranker, and database stack with real token and ops costs.

### Memar
- **No memory that runs.** Memar prescribes executable memory services and ships none: no extractor, no fusion, no consolidation worker, no redaction, no eval tiers. Every mechanism in section 3 is a standing demonstration of work Memar's principles point at but leave unbuilt — by design, and still unbuilt.
- **No failure catalog.** Hindsight documents six ways its own learning fails, with mechanisms. Memar has no comparable public record of where its own disciplines fail in practice — no maintained statement of where Memar is not applied, attempted and abandoned, or silently unlearned. The project that needs section 3's item 6 most is Memar.
- **No adoption surface.** Nothing to install, no bank to retain into, no dashboard. The correct price of being a framework rather than a product — and still the reason a team reaches for Hindsight first.

## 7. What Memar can learn
### Absorb
1. **The recall/reflect split as an agency norm.** Retrieval stays neutral; shaping (mission, directives, disposition) applies at answer time, never to what is recalled. Stated domain-generally, this is an asymmetry-obligation-grade rule: a participant's standing instructions must not rewrite the shared record they read — they govern what is *concluded*, not what is *retrieved*. Home: the asymmetry obligation in [Cognition](../cognition.md) or [Agency](../agency.md). This is the highest-value item on the list, because Memar currently states nothing that separates reading the record from answering over it. (Since absorbed: [What Implementation Asymmetry Obliges → Keep reading and concluding separate](../cognition.md#what-implementation-asymmetry-obliges).)
2. **Eval tiers with the seams labeled.** Which checks run deterministically on stubs on every change, which run on real models on a schedule with judges that differ from the test model, and which numbers live in exactly one external home with a pinned ref. Memar's Test protocol owns the epistemic rule; it does not own the tiering. Home: [Test Practice](../modules/process/test.practice.md), as a scaling note beside the existing scaling treatment. (Since absorbed: [Test Practice → Scaling → Tiers with labeled seams](../modules/process/test.practice.md#scaling).)
3. **A maintained statement of where Memar is not applied.** The spec-kit comparison already asked for this; Hindsight's frank failure catalog makes the case sharper. A short section on the project README — where Memar was tried and abandoned, which disciplines demonstrably fail under which pressures — is the disclosure instance of a principle Memar already holds (goals achievable by the framework's own processes). The difference from the earlier ask: include *failures*, not just non-application. (Since absorbed as a requirement, not as the report: [Framework → Goal-Oriented Frameworks and Purpose Space](../framework.md#goal-oriented-frameworks-and-purpose-space) states the consistency requirement plus its anticipated public failure statement; the report itself remains anticipated work.)

### Adapt
4. **Evidence-bearing consolidation as a changelog question.** Observations carry quotes and proof counts; pages are standing answers refined rather than overwritten. The adaptation is a review question for Memar's own records, not a mechanism: when a changelog entry supersedes understanding, does it cite the evidence that survived and name what was dropped — or does it rewrite the page from the new batch alone? Candidate home: the changelog practice, as one sentence.
5. **Strict isolation with named scope.** Banks leak nothing across each other; disposition affects reflect only. The adaptation: Memar's bounded delegation and handoff scoping already isolate work, but nothing states the Hindsight-grade rule — scoping constraints must name which operations they touch and which they leave neutral. A scoping note that constrains everything constrains nothing reviewably.

### Reject
- The memory substrate itself: extractors, fusion weights, rerankers, consolidation workers, redaction patterns, and eval judges as Memar doctrine. Generative work belongs in callable services built by domain projects; the principle already says so.
- Typed facts, observations, mental models, banks, and dispositions as knowledge-model content. They answer a product's questions, not the framework's.
- The five-channel distribution (commands, skills, MCP, hooks, plugins), the integration-count race, and the off-repo benchmark/monitor/cookbook shape. Memar's pointer-based consumption stands; the 55-vs-62 drift is the evidence.
- Percentages and vendor-run leaderboards as evidence. Enumeration of the obligation's surface is Memar's answer and the better one.

### Separate research
6. **Refinement without unlearning.** Hindsight refines by rewrite and demonstrably unlearns; Memar appends and never rewrites, at the cost of readers drowning in superseded entries. Is there a named record shape — distinct from both rewrite and raw append — in which a standing answer cites its surviving evidence, names what it dropped, and keeps the dropped material recoverable? The tensorus comparison asked the sibling question about rationale lineage; this one asks about the write mechanics. Research, not a change. (Since investigated, and held open: [Knowledge Handoff → Supersession](../knowledge.handoff.md#supersession-which-home-owns-the-obligation-and-is-it-a-norm-or-a-check).)
7. **Honest gaps under strict schemas.** Hindsight's fabrication episode (mandatory fields filled when the source states nothing) has a Memar counterpart wherever a template or frontmatter *requires* a value the author does not hold. Which of Memar's required fields are fabrication risks, and should any required field admit a named "not held" state? Research, not a change. (Since investigated, and closed: an inventory of the required fields across the six facet specifications and `CONTRIBUTORS.md` found none that forces an invented value — each is mechanically held by its author, already admits a named member meaning not-held, or is a list whose honest gap is its absence. No required field needed a new state; `Propagates to` is the place one would belong if a real case appeared, and no case has been seen.)

## 8. Possible relationship
1. **Memar remains the authority** for concepts, terminology, model, protocol contracts, knowledge discipline, process, and change provenance.
2. **Hindsight is a memory implementation that may run inside a Memar development.** A project whose agents need long-term memory may adopt retain/recall/reflect as its memory service — under an explicit contract — without adopting Hindsight's type vocabulary as Memar doctrine, its benchmark claims as evidence, or its distribution platform as a consumption model.
3. **The memories it stores are retrieval material, not the project's knowledge.** A bank of facts with proof counts is evidence about what was said and seen; what the project holds true, decided, and rejected lives in its model and records. `reflect` returns an answer; Memar's records say whether that answer may be acted on.
4. **Compatibility requires an explicit contract**, and the interesting clauses are the ones Hindsight's own evals expose: which document owns a claim (bank page or project record), whether consolidation may rewrite or only supersede with evidence cited, what makes a retained fact evidence rather than paraphrase, and where shaping is allowed to touch the pipeline (answer time, never retrieval).

## 9. Decision
Hindsight is not a substitute for Memar and is not in the same category. It is a well-built, unusually self-documenting agent-memory product with a real retrieval engine, a real consolidation pipeline, a real eval operation — and documented proof that paraphrase-based learning silently unlearns, fabricates, drifts, and extrapolates. Memar is a domain-agnostic model and discipline that ships no memory at all.

The comparison does not justify changing Memar's governing method. It identifies absorptions that strengthen mechanisms Memar already owns — the recall/reflect split as an agency norm, labeled eval tiers, a failure-inclusive non-application statement — and research threads Memar deferred to itself: refinement without unlearning, and honest gaps under strict schemas.

The strongest argument in this comparison cuts in Memar's favor and against complacency at once. Hindsight's failure catalog is the best evidence in this folder that storing more, fusing better, and consolidating continuously does not produce knowledge — it produces well-indexed paraphrase that can delete true things. That is Memar's founding claim, demonstrated by the other side's own instruments. It is also a standing challenge: until Memar publishes its own catalog of where its disciplines fail, the vendor with the failure log is more honest about its limits than the framework is.

## 10. Open for critique
- Whether the credit in section 3 is sufficient, and whether any of the seven items is stronger than stated.
- Whether the recall/reflect split (item 1) is genuinely an agency norm or only a product configuration dressed as one.
- Whether the failure-inclusive non-application statement (item 3) asks Memar to publish what a single-author project cannot yet produce without performative self-flagellation.
- Whether the refinement-without-unlearning research (item 6) is a real gap or a restatement of what append-only changelogs plus handoffs already solve.
- Whether section 5's treatment of off-repo claims is fair to a product whose benchmarks are too large to live in its own repo.
- Any unfair characterization of Hindsight. Every claim here is pinned to a file and line so it can be checked; the ones that should be re-read first are the "60+" integration count, the eval failure passages, and the off-repo benchmark claims in section 2. Two claims in this essay were not verified against the checkout and are named here rather than left to a reader to discover: the Helm chart version and the size of the generated client surfaces, both carried from the first pass's inventory rather than recounted.
