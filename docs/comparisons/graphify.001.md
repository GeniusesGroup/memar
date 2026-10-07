# Comparison: Memar and Graphify
**Compared project:** [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify)

**Inspected at:** commit [`35adf43`](https://github.com/Graphify-Labs/graphify/commit/35adf432b9d50f6f3d530ab5d7ec316819ef081c) (2026-10-04), branch `v8`, package `graphifyy` version `0.9.76`.

**Method:** two read-only passes over a shallow single-commit checkout — one on the pipeline and knowledge model, one on distribution, benchmarks, and Memar-side principles — cross-checked against Memar's live `docs/`. Nothing was installed, executed, or benchmarked independently; every claim about Graphify below is a claim about what its files say or what its code contains, with file-and-line citations a reader can check. Where a claim is inference rather than something the repository states, it is labeled.

## Table of contents
- [Comparison: Memar and Graphify](#comparison-memar-and-graphify)
  - [Table of contents](#table-of-contents)
  - [1. What each project is](#1-what-each-project-is)
    - [Graphify (self-definition)](#graphify-self-definition)
    - [Memar (self-definition)](#memar-self-definition)
    - [Category distinction](#category-distinction)
  - [2. Where Graphify is genuinely stronger](#2-where-graphify-is-genuinely-stronger)
  - [3. Where Memar is stronger](#3-where-memar-is-stronger)
  - [4. Limits and failure modes in Graphify](#4-limits-and-failure-modes-in-graphify)
  - [5. What the distribution layer costs a mental model](#5-what-the-distribution-layer-costs-a-mental-model)
  - [6. Costs and limits on both sides](#6-costs-and-limits-on-both-sides)
    - [Graphify](#graphify)
    - [Memar](#memar)
  - [7. Adoption filter](#7-adoption-filter)
    - [Already owned in Memar](#already-owned-in-memar)
    - [Absorb (proposed, not applied)](#absorb-proposed-not-applied)
    - [Adapt (proposed, not applied)](#adapt-proposed-not-applied)
    - [Reject for Memar](#reject-for-memar)
    - [Separate research](#separate-research)
  - [8. Possible relationship](#8-possible-relationship)
  - [9. Decision](#9-decision)
  - [10. Open for critique](#10-open-for-critique)

## 1. What each project is
### Graphify (self-definition)
Type `/graphify` in an AI coding assistant and it maps a project — code, docs, PDFs, images, videos — into a **knowledge graph** to **query instead of grepping** through files ([`README.md:34`](https://github.com/Graphify-Labs/graphify/blob/35adf432b9d50f6f3d530ab5d7ec316819ef081c/README.md)). Its three differentiators are stated on the same page: code parsed locally with tree-sitter AST (deterministic, no LLM, nothing leaves the machine; docs and media take a semantic pass through the assistant's model or a configured key); every edge tagged `EXTRACTED` or `INFERRED`; and a real traversable graph rather than a vector index ([`README.md:36-38`](https://github.com/Graphify-Labs/graphify/blob/35adf432b9d50f6f3d530ab5d7ec316819ef081c/README.md)). Architecturally it calls itself a Claude Code skill backed by a Python library — the skill orchestrates, the library stands alone — with a fixed pipeline `detect() → extract() → build() → cluster() → analyze helpers → report.generate() → export.to_*()` communicating through plain dicts and NetworkX graphs ([`ARCHITECTURE.md:3-11`](https://github.com/Graphify-Labs/graphify/blob/35adf432b9d50f6f3d530ab5d7ec316819ef081c/ARCHITECTURE.md)). The always-on background variant across code, docs, and meetings is the commercial product at `graphify.com` / `app.graphify.com`; the repository is the on-demand skill plus library ([`README.md:40`](https://github.com/Graphify-Labs/graphify/blob/35adf432b9d50f6f3d530ab5d7ec316819ef081c/README.md)).

### Memar (self-definition)
Memar describes itself as a domain-agnostic framework for developing systems, not only software — a framework for constructing, examining, and refining mental models about systems, whose purpose runs knowledge → thinking → intelligence → agency → goals ([Framework → Memar's Purpose Space](../framework.md#memars-purpose-space-from-knowledge-to-agency) — **Evidence**). Its working model is: the model is the primary architectural artifact, contracts live in documents, and generative work lives in callable modules ([Knowledge → Knowledge and Code](../knowledge.md#knowledge-and-code) — **Evidence**). Memar states its limits as part of the framework: finished delivery of a named structure, and subjects no Memar document governs, are answered elsewhere or reported as absent rather than supplied here.

### Category distinction
The two projects answer different questions, and the questions are not adjacent.

- Graphify's question: **given a folder of code and documents, what derived graph lets an agent answer questions without re-reading the files?**
- Memar's question: **what shared model of systems and knowledge is this work conducted inside, and how does that model stay coherent as the system changes?**

A team can query a Graphify projection while developing inside Memar without conflict. Neither replaces the other, because neither addresses the other's question.

The sharper reading, held by the owner, is part–whole rather than peer–peer: Graphify's job — orienting an agent inside already-written sources — is one executable projection of the kind Memar's Knowledge-and-Code principle assigns to code services, built without the framework that would govern it. On the owner's correction, "knowledge graph" here names effective knowledge management, not the graph technique: by that measure `memar content` already manages knowledge — one entry point that resolves references, judges relevance without opening whole files (`meta`), slices (`section`), searches full-text, verifies link integrity, lists undischarged obligations, and writes safely. What is absent is the technique layer beneath that management — typed nodes and edges, multi-hop traversal, clustering, a store, a server — plus the code sources and the organizational discipline, which belong to the Organization project. The owner's evaluation stands on direction and strategic value: management first, technique where it earns its keep.

## 2. Where Graphify is genuinely stronger
Stated as an inventory of genuine strengths; the filter is in section 7.

1. **Deterministic local code extraction at breadth.** Around three dozen tree-sitter grammars plus optional extractors (Terraform, OCaml, Common Lisp, Robot, Pascal, Apex-regex, and others) turn code into nodes and edges with no LLM and no API key; `--code-only` indexes just the code offline ([`README.md:348-362,379,605-606`](https://github.com/Graphify-Labs/graphify/blob/35adf432b9d50f6f3d530ab5d7ec316819ef081c/README.md)). Memar has no comparable code-reading machinery, by scope rather than by oversight.
2. **Read-versus-inferred marking on every edge.** `EXTRACTED` means explicit in the source, `INFERRED` a deduction of the call-graph second pass or co-occurrence, `AMBIGUOUS` a flag for human review in the report ([`ARCHITECTURE.md:67-73`](https://github.com/Graphify-Labs/graphify/blob/35adf432b9d50f6f3d530ab5d7ec316819ef081c/ARCHITECTURE.md)). The semantic path adds a discrete numeric rubric while code defaults to a backstop table — a presentation choice with its own risk, recorded in section 4.
3. **Analyses as code functions, not prose recipes.** God nodes, surprising connections, suggested questions, import-cycle detection, and graph diff are sibling functions with signatures the architecture test imports, so the document describing them cannot drift from the code ([`ARCHITECTURE.md:15-34`](https://github.com/Graphify-Labs/graphify/blob/35adf432b9d50f6f3d530ab5d7ec316819ef081c/ARCHITECTURE.md)). This is Memar's Knowledge-and-Code division practiced well by someone else.
4. **LLM-free community structure.** Leiden (graspologic, Louvain fallback, seed 42, deterministic edge sorting against hash-order effects) splits oversized and low-cohesion communities, with labels derived from hub nodes rather than a model ([`README.md:113`](https://github.com/Graphify-Labs/graphify/blob/35adf432b9d50f6f3d530ab5d7ec316819ef081c/README.md)).
5. **A schema gate before assembly.** `validate.py` enforces required node and edge fields and closed value sets before `build()` consumes anything; a partial run refuses to overwrite a larger graph unless `--allow-partial` is passed. Fail-closed defaults stated as deliberate behavior. Its partial-run refusal is the orientation-side twin of the Revision refuse clause drafted since — two independent arrivals at fail-closed enactment, which is evidence for the shape rather than analogy.
6. **Rationale captured where it already lives.** `# NOTE:` / `# WHY:` / `# HACK:` and sibling comment prefixes plus docstrings become linked rationale nodes on the AST path, and ADR/RFC citations become edges ([`README.md:116`](https://github.com/Graphify-Labs/graphify/blob/35adf432b9d50f6f3d530ab5d7ec316819ef081c/README.md)). Capture is incidental rather than a decision record — section 4 — but as capture it is real. Against this credit stands the owner's position, now verified in Memar's governing rules: documentation lives in comments only where no documentation method exists yet, human-facing text belongs to a type's own methods, and an organization may forbid comments outright ([Comment Policy](../../modules/khayyam/rules/comment-policy/comment-policy.md)). Harvested comment-nodes therefore cannot be a kept representation; at most a transitional migration input — section 7.
7. **Sources across code and the rest.** Docs, PDFs, office files, images, video/audio transcription, URLs, package manifests, MCP configs, and live database introspection map into the same graph, with Markdown links and wikilinks becoming `references` edges.
8. **Queryable products, not just a report.** `graph.json` for queries, `graph.html` for browsing, `GRAPH_REPORT.md` for orientation, plus opt-in wiki, Obsidian vault and canvas, SVG, GraphML, Cypher, and database push — multiple projections of one assembled graph.
9. **Continuity machinery.** Content-hash semantic cache, incremental update, git hooks that rebuild on commit and branch switch, a `graph.json` union merge driver, portable relative-path manifests, and a documented split between machine-local files and shareable products.
10. **Benchmarks with stated method and disclosed agreement.** Same-harness, same-model, same-budget comparisons with a blind-validated second judge (90.6% agreement, Cohen's kappa 0.81) and an admitted embedder confound — stronger reporting hygiene than most neighboring projects manage. The numbers themselves and their bounds are in section 4.

## 3. Where Memar is stronger
1. **Identity independent of location.** Memar requires the stable identifier to derive from content or immutable assignment, never from storage location ([Knowledge → Identity Must Be Independent of Location](../knowledge.md#identity-must-be-independent-of-location) — **Evidence**). Graphify binds identity to location three times over: file stems preserve the full repo-relative path, non-AST ids are re-derived from `source_file`, and the architecture document warns that omitting `root` anchors ids to whatever directory the call happened to pass. Renaming a file mints new identities; ghost-merge heuristics only soften the break. The decided direction on Memar's side is ContentUUID+offset with `path` demoted to one locator among others (rename thread, 2026-10-05) — stated here as the counterpart, not the argument.
2. **Typed relationships, not open verbs.** Memar treats reference, dependency, containment, attribution, opposition, and others as distinct first-class relations ([Knowledge → Relationships Are First-Class Citizens](../knowledge.md#relationships-are-first-class-citizens) — **Evidence**). Graphify's relations are free-form verb phrases (`uses`, `mentions`, `semantically_similar_to`, …) with only `file_type` and `confidence` closed; its own import-cycle detector trusts just two of them. A machine consumer reads prose-flavored labels, not a relation contract.
3. **A model before the representation.** Graphify compiles what sources happen to say into articles, nodes, and hub-ranked communities. Under Memar's model those remain representations whose semantic fidelity must be evaluated: no concept-admission criterion, no responsibility or lifecycle boundary, no assumption-and-contradiction handling, no model-completeness check ([Modeling → The Model as the Primary Artifact](../modeling.md#the-model-as-the-primary-artifact) — **Evidence**). The same gap this folder recorded for wiki compilation applies to graph compilation.
4. **Task-centric evolution, not snapshot diff.** Memar's primary unit of knowledge evolution is the Task or Decision, with history derivable from it ([Knowledge → Task-Centric Knowledge Evolution](../knowledge.md#task-centric-knowledge-evolution) — **Evidence**). Graphify's continuity is hooks plus `graph_diff` over snapshots: what changed between two states, never why, what was considered, or who decided. Valuable for orientation; silent on rationale by construction.
5. **Terminology governance.** Memar's definitions govern over ecosystem usage and say where they diverge. Graphify's `normalize_id` (casefold plus NFKC to fixpoint, non-word runs to underscores) governs collisions, not meaning: two different concepts with similar spellings become neighbors by construction.
6. **Process, protocol, and agency.** Expected inputs and outputs before enactment, checkable conformance, and separated authority, responsibility, capability, and accountability ([Process → Expectations and Checks](../process.md#expectations-and-checks); [Protocol → Conformance](../protocol.md#conformance); [Agency → Authority](../agency.md#authority) — **Evidence**) have no counterpart in Graphify. Its PR triage ranks a review queue; it confers no authority and checks conformance against nothing.
7. **Reader-routed documentation.** Explanation, Practice, Changelog, Handoff, and Research have different structures because their readers study, follow, audit, resume, or evaluate ([Documentation → Facets currently defined](../documentation.md#facets-currently-defined) — **Evidence**). `GRAPH_REPORT.md` is one orientation artifact for one reader posture.
8. **Silence with an owner.** Where Memar does not govern — finished delivery, organizational discipline, sector adoption — it says so and names where the answer is being built. Graphify's silence on the same questions is not a position; it is the edge of an extraction tool — and at the evaluation edge, that silence is deadly rather than neutral, per section 4 item 9.

## 4. Limits and failure modes in Graphify
Stated without calling the project worthless — failure modes when it is treated as a development framework.

1. **Move a file and its history forks.** Path-bound identity (section 3 item 1) means reorganization reads as deletion plus creation. Ghost-merging and legacy-stem maps mitigate; they do not restore stable identity.
2. **Confidence scores without calibration.** The `0.95 / 0.85 / 0.75 / 0.65 / 0.55` INFERRED rubric and the `EXTRACTED 1.0` backstop are asserted per edge with no stated calibration study. A coarse operational label is honest triage; five precise-looking decimals invite a reader to treat resolution heuristics as measured probabilities.
3. **The semantic half is host-model dependent.** Docs, PDFs, and images require the assistant session or a configured backend; quality follows the selected model, context, and keychain. Code-only sources are fully local; mixed sources are not, and the boundary deserves stating plainly in any adoption decision.
4. **Benchmarks are a cost-efficiency win, not a sweep.** On the project's own harness with Kimi K2.6 throughout: LOCOMO recall@10 of 0.497 against a 300-item slice (hybrid RRF 0.493, BM25 0.362); LOCOMO QA accuracy 45.3% against supermemory's 49.7%; LongMemEval-S 76% tied with dense RAG on 50 English items; ingest about $1.40 against supermemory's $15.67; code-intelligence coverage 70.8% to 82.0% on six questions over ERPNext. Small and subset samples, one model family grading its own pipeline's answers, adapters for rivals written by the home team, and an admitted embedder confound on one recall row. The defensible reading is recall-per-dollar with zero build cost — which is a real result — and not general retrieval superiority.
5. **Rationale nodes are not a decision record.** AST comment prefixes capture what someone bothered to write next to the code; the semantic path is forbidden from minting rationale nodes and folds them back into attributes. Nothing carries alternatives, dissent, approval, supersession, or expiry. A `# WHY:` node is evidence that a reason was once stated, not that the decision is held.
6. **Hyperedges and similarity edges carry the model's vaguest semantics.** `participate_in` / `form` groupings and `semantically_similar_to` links are the least checkable relations in the schema, and there is intentionally no embedding layer behind them to inspect. By design, per the repository — which makes it a boundary, not a bug, but a boundary an adopter inherits.
7. **Single-file calls can anchor to the wrong root.** When `root` is omitted, ids derive from the common parent of the passed list, so a one-file extraction carries machine-local path segments. The document warns; the default still permits it.
8. **No vector layer means no graceful degradation outside the graph.** Where the graph is thin — a new domain, mostly-media sources before their semantic pass — there is no dense retrieval to fall back on. Competing harnesses in its own benchmark table supply that baseline; the product itself declines it.
9. **Deadly silence: coherence presented where correctness is owed.** Every analysis is descriptive over the scanned sources — degree, cohesion, cycles, co-occurrence, extraction confidence — with no input for requirements, market reality, competing alternatives, or any ground truth outside the files (verified across `analyze.py`, `report.py`, and the `llm.py` prompts; the strongest evidence-binding only checks that a symbol occurs in the shown chunk). An organization whose documents and code agree with each other gets that agreement back as structure, which can read as validation. The Nokia-style failure — a coherent organization executing the wrong model of the world — is therefore outside what this instrument can falsify; evaluation against independent evidence belongs to the framework's Test, Process, and Research facets, which Graphify does not implement. The owner rules the "deadly silence" verdict apt: an orientation instrument that cannot falsify the model it orients within does not merely leave evaluation undone — it risks certifying the wrong path by returning its coherence as structure. (The mechanism claim is inference from inspected code, labeled as such; the verdict is the owner's.)

## 5. What the distribution layer costs a mental model
This is the part of Graphify with no counterpart in Memar, and the part Memar's model predicts most sharply.

The measured shape: roughly two dozen install rows across assistant platforms, per-platform skill bodies plus a `references/` sidecar, an always-on matrix split between hook platforms (a nudge before search and read tools, with a strict mode that blocks the first raw read) and instruction-file platforms (persistent guidance in `AGENTS.md` and equivalents), an MCP stdio server plus a shared HTTP transport, and auto-refresh of installed skills after upgrades. The hygiene is genuinely good: machine-local files are named and excluded, shareable products are force-added explicitly, manifests are portable relative paths, and the architecture test refuses documentation drift.

Two consequences are visible rather than predicted. First, one model now speaks through a dozen-plus projections maintained per host, and behavioral parity between the canonical skill, generated mirrors, and portable instruction files must be tested rather than assumed — the same lesson this folder recorded for multi-runtime packaging elsewhere. Second, always-on guidance is harness persuasion: nudges and read-blocks patch today's agent habits (skipping orientation, re-reading files instead of querying) and will age into noise as those habits change, while the underlying principle — consult the scoped projection before the raw sources — is the durable sentence underneath.

Memar's position is that a consuming project installs a pointer and receives no copy, and that harness engineering operates a level below the theory of interaction ([Agency → Prompt Engineering and Harness Engineering](../agency.md#prompt-engineering-and-harness-engineering) — **Evidence**). On the evidence above, Graphify's distribution layer is competent engineering and a standing demonstration of what that lower level costs.

## 6. Costs and limits on both sides
### Graphify
- Identity is positional, relations are ungoverned verbs, and history is snapshot diff — a projection that orients well and governs nothing.
- Numeric confidence, similarity edges, and hyperedges present heuristic judgments in calibrated-looking clothes.
- Mixed sources depend on a host model and keychain; the local-first promise covers code, transcription, and caching, not understanding.
- Roughly two dozen platform surfaces to maintain, with parity as a permanent testing obligation.
- Benchmarks establish cost-efficient recall on slices, not general superiority; the strongest table row is dollars, not accuracy.

### Memar
- No code-reading machinery at all: no extractor, no queryable projection, no orientation report. A newcomer to a large codebase gets principles, not a map.
- Higher authoring and governance overhead: facets, companions, explicit definitions, review state, and propagation against a three-rule envelope that ships today.
- Many governing documents remain Draft or Proposed with limited sustained external review; the comparison establishes no measured advantage in authoring time, drift rate, or decision quality.
- The typed model is not yet realized in a machine-readable surface; Memar requires typed relations while its own Markdown links still carry relation semantics in prose.
- The fair conclusion is symmetric: **Graphify has more machinery and less conceptual breadth; Memar has more conceptual breadth and less finished machinery.**

## 7. Adoption filter
### Already owned in Memar
- Executable work in callable services with contracts in documentation ([Knowledge → Knowledge and Code](../knowledge.md#knowledge-and-code) — **Evidence**). Graphify's analyze, export, and serve functions are a conforming instance from outside; nothing needs importing, because the principle already holds and the instance is not Memar's to keep.
- One continuous mental model with multiplying access projections ([Knowledge → A Project Carries One Continuous Mental Model](../knowledge.md#a-project-carries-one-continuous-mental-model) — **Evidence**). Graphify's skill matrix is projections done competently; the parity-testing obligation is the standing consequence, already recorded in this folder for multi-runtime packaging.
- Load-bearing logic kept linear ([Documentation → Written surface](../documentation.md#written-surface) — **Evidence**). Graphify's `GRAPH_REPORT.md` is prose sections and lists; its force-directed `graph.html` is orientation, never the carrier of a norm. No conflict to resolve.

### Absorb (proposed, not applied)
No new governing absorption is proposed in this pass. Two conforming instances are recorded so a later reader does not re-litigate them: schema validation before assembly with fail-closed refusal on partial runs matches the fail-closed posture this folder already asks of Memar's own resolvers; and deterministic structural checks over a documentation set match what Memar's `check` already reports. Both strengthen existing homes by example rather than by edit, and neither is applied here.

### Adapt (proposed, not applied)
- Rationale-comment harvesting is demoted from adaptation to transitional input only. The owner's no-comments hypothesis was steel-checked against the governing rules and survived: comments are the fallback while self-documenting methods do not exist, human-facing text is a value a type's own methods write, and comments carry no lifecycle, identity, or propagation — exactly the orphaned-context failure the Knowledge document diagnoses. The attempted refutation (warnings, contracts, vendor-mirrors as comment-shaped knowledge) fails because each has a proper home already: method-written text, protocol contracts in `docs/`, rationale in changelog, handoff, or research. The narrow remainder a code service may one day perform is harvest-then-delete migration of legacy comment blocks into those homes — never kept rationale nodes. Home if ever built: an executable projection in the Organization project.
- The read-path discipline — consult the scoped projection (`query` / `path` / `explain`) before re-reading raw sources — as one sentence under the asymmetry obligation if it proves durable across model generations. The hook machinery, strict modes, and per-platform nudges stay outside; only the sentence may travel.

### Reject for Memar
- Path-derived identifiers as identity; file stems, re-derived semantic ids, and external stub nodes are collation conveniences, not a counter-model to content-derived identity.
- Open verb phrases as relationship types; no producer-defined edge label becomes a Memar relation without an independent contract.
- Numeric confidence scores as an epistemic model; this folder already declined coarse confidence enums, and finer decimals do not answer that objection.
- Snapshot diff plus hooks as knowledge evolution; `graph_diff` answers what changed between states and must never stand in for task-centric history.
- The harness matrix, skill bodies, marketplace surfaces, and always-on nudges as how Memar is delivered; a consuming project installs a pointer.
- Recall percentages and god-node rankings as completeness evidence; Memar answers coverage by enumerating the obligation's surface.
- The generated report or graph as current truth; a projection is rebuildable input to orientation, never the model's authority.
- Comment-mined rationale as a kept representation; harvesting is migration input at most, and blessing comments as nodes would legitimize the wrong home for rationale.

### Separate research
1. Whether Memar's ecosystem should own a code-graph projection at all — AST extraction, typed-edge mapping, community analysis, and read-only query as an executable service. Status since this comparison: the enactment half is drafted (the Revision contract); what remains is strictly the orientation service, owned by the Organization project's orientation-service slice. The gap inventory is measured, not assumed: the current documentation script builds no nodes, no edges, no store, and no server, so reaching even Graphify's orientation baseline needs parsers with confidence, a persistent index, clustering, path queries, and a serving wrapper. Open sub-questions live with that slice: first-sources scope, extraction-confidence vocabulary, and serving shape. The standing hypothesis is no Memar change: this comparison is input, not a charter.
2. Whether derived projections need a bounded extracted-versus-inferred marking vocabulary, or whether each projection keeps its own. Prior art against standardizing: this folder's rejection of coarse confidence enums and Graphify's uncalibrated decimals above. A research companion, not a change.

## 8. Possible relationship
The architecturally consistent relationship is:

1. **Memar remains the authority** for concepts, terminology, model, identity, typed relationships, process, protocol, agency, evidence, and lifecycle.
2. **Graphify acts as an external orientation instrument** for existing code and document sources: build the graph, query the scoped projection first, read raw sources second. Its output orients; it does not model.
3. **The graph is a projection of whatever model the project holds**, not the model's source of truth. A god node is evidence about coupling; it is not a responsibility assignment.
4. **Compatibility requires an explicit contract before it is claimed**, governing stable exported identity independent of bundle path, typed-relation mapping, provenance and claim verification, lifecycle, privacy of session capture, and conformance. Round-trip tests must prove the integration does not collapse Memar distinctions such as source versus knowledge, node versus concept, similarity versus relation, and snapshot versus task history.
5. **Where Memar is silent, the Organization project answers.** Finished orientation services, creation workflows, and sector adoption are that project's subject under the boundary Memar already states. Silence here is scoping, not a gap awaiting a framework sentence.

## 9. Decision
Graphify is not a substitute for Memar and is not in the same category. It is a well-built, honestly-reported codebase-orientation instrument with a large and largely necessary distribution surface attached; Memar is a domain-agnostic model and discipline that does not read code at all.

This comparison warrants no change to Memar's governing method. It records two conforming instances, one bounded adaptation held for a live requirement that does not currently exist, one demoted harvesting proposal with its failed refutation on record, and two research threads owned elsewhere. The Revision draft and the identity decision cited above arrived through the rename thread, not through this file; they are cited here so the file does not go stale, not claimed as its results. A reader checking Memar's current state should read the governing documents and their changelogs, not this file's section 7 alone.

The strongest argument Memar has here is not any single feature but the direction of dependence. An orientation graph is useful exactly to the extent that someone, somewhere, holds the model it orients within: which concepts deserve identity, which relations are contractual, which decisions stand and why. Graphify extracts the former from what is written; only a framework of the latter makes the extraction worth querying. Since this comparison, the alternative has become nameable rather than gestured at: orientation that cannot falsify, against a Revision that refuses to enact what the analyzer newly rejects, inside task-centric history. That is an argument from a stated principle meeting observed evidence, which is the only kind worth making.

## 10. Open for critique
- Whether the credit in section 2 is sufficient, and whether any of the ten items is stronger than stated.
- Whether the benchmark reading in section 4 item 4 is fair to a team that reports its harness, judge agreement, and confounds openly.
- Whether the management-first framing of section 1 concedes too much: which knowledge-management operations, precisely, does the current script perform, and which named technique is owed next?
- Whether the failed refutation of the no-comments hypothesis missed a live counterexample — a comment-shaped knowledge unit with no proper home in method-written text, protocol contracts, changelog, handoff, or research.
- Whether holding the read-path adaptation for a nonexistent live requirement is correctly scoped restraint or the same deferral pattern this folder criticizes elsewhere.
- Whether section 5 is fair to a distribution surface whose audience is adoption breadth rather than model integrity.
- Any unfair characterization of Graphify. Every claim here is cited to a file and line so it can be checked; the ones to re-read first are the identity mechanics in section 3 item 1 and the benchmark bounds in section 4 item 4.
