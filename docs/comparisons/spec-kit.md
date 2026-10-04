# Comparison: Memar and GitHub Spec Kit
**Compared project:** [github/spec-kit](https://github.com/github/spec-kit)
**Inspected at:** commit [`ae5ade72`](https://github.com/github/spec-kit/commit/ae5ade7234be5cb1d975f736c4e06dd46d1326d6) (2026-10-03), `pyproject.toml` version `1.1.1.dev0`.
**Method:** two independent read-only passes over the checkout — one on the method and artifacts, one on the architecture and distribution engineering — cross-checked against Memar's live `docs/`. Neither pass executed Spec Kit's suite, installed it, or ran any of its commands; every claim about Spec Kit below is a claim about what its files say or what its code contains, and file-and-line citations are given so a reader can check them. Where a claim is inference rather than something the repository states, it is labeled.

## Table of contents
- [1. What each project is](#1-what-each-project-is)
  - [Spec Kit (self-definition)](#spec-kit-self-definition)
  - [Memar (self-definition)](#memar-self-definition)
  - [Category distinction](#category-distinction)
- [2. What Spec Kit has that Memar does not](#2-what-spec-kit-has-that-memar-does-not)
- [3. Where Memar is stronger](#3-where-memar-is-stronger)
- [4. Limits and failure modes in Spec Kit](#4-limits-and-failure-modes-in-spec-kit)
- [5. What the distribution layer costs a mental model](#5-what-the-distribution-layer-costs-a-mental-model)
- [6. Direct conflicts if imported into Memar](#6-direct-conflicts-if-imported-into-memar)
- [7. Costs and limits on both sides](#7-costs-and-limits-on-both-sides)
- [8. What Memar can learn](#8-what-memar-can-learn)
  - [Absorb](#absorb)
  - [Adapt](#adapt)
  - [Reject](#reject)
  - [Separate research](#separate-research)
- [9. Possible relationship](#9-possible-relationship)
- [10. Decision](#10-decision)
- [11. Open for critique](#11-open-for-critique)

## 1. What each project is
### Spec Kit (self-definition)
Spec Kit calls itself "an open source toolkit that gives AI coding agents structured processes, reusable templates, and documented outcomes" ([`README.md:20-22`](https://github.com/github/spec-kit/blob/ae5ade7234be5cb1d975f736c4e06dd46d1326d6/README.md)). Its thesis is Spec-Driven Development: "Specifications don't serve code — code serves specifications" ([`spec-driven.md:7`](https://github.com/github/spec-kit/blob/ae5ade7234be5cb1d975f736c4e06dd46d1326d6/spec-driven.md)).

What it actually ships is a software feature pipeline — `specify → clarify → plan → tasks → implement ⇄ converge`, with `analyze`, `checklist`, and `constitution` as quality gates ([`docs/reference/agentic-sdd.md:15`](https://github.com/github/spec-kit/blob/ae5ade7234be5cb1d975f736c4e06dd46d1326d6/docs/reference/agentic-sdd.md)) — plus a distribution platform around it: a PyPI CLI (`specify`), 42 registered agent integrations, an extension system, a preset system, a YAML workflow engine, a bundle layer, community catalogs, and an MCP surface. At the inspected commit: 252 Python files and about 2.54 MiB under `src/`, 334 test files and about 5.19 MiB under `tests/`, 5,636 `def test_` definitions, and a 132 KB `CHANGELOG.md` covering 230 releases.

Its method is software-only. `AGENTS.md:5` says "building software"; the artifact templates hard-code `src/`, `tests/`, `backend/`, `frontend/`, `api/`, `ios/`, `android/`; and `/implement` creates `.gitignore`, `.dockerignore`, `.eslintignore`, `.prettierignore`, `.npmignore`, `.terraformignore`, and `.helmignore` as a required step. The domain-agnostic reach claimed in `docs/index.md:9` ("including processes beyond software development") is supported only by third-party presets and by `assess`, which explicitly disclaims implementation ("Detailed architecture, implementation tasks, and source changes are deliberately outside this process", `docs/guides/assessment.md:66-67`).

### Memar (self-definition)
Memar describes itself as a domain-agnostic framework for developing systems, not only software ([Framework → Memar's Framework: Design Space Over Implementation Layers](../framework.md#memars-framework-design-space-over-implementation-layers) — **Evidence**). It states its own purpose as a chain, Knowledge → Thinking → Intelligence → Agency → Goals ([Framework → Memar's Purpose Space](../framework.md#memars-purpose-space-from-knowledge-to-agency) — **Evidence**), and its own model of work as: the model is the primary architectural artifact, contracts live in documents, and generative work lives in callable modules ([Knowledge → Knowledge and Code](../knowledge.md#knowledge-and-code) — **Evidence**).

Memar has no feature pipeline. It has concept documents, protocol contracts, practices, and per-document changelogs. It has no templates for feature artifacts, no phases, no checklists, and no requirement identifiers — and it says so rather than implying coverage ([Software → The software life cycle, as prior-art taxonomy](../software.md) — **Evidence**: "Full treatment owed" for requirements, "No home yet; owed" for project management and quality assurance).

### Category distinction
The two projects answer different questions, and the questions are not adjacent.

- Spec Kit's question: **given a software feature, what artifacts must exist before implementation, and in what order?**
- Memar's question: **what shared model of systems and knowledge is this work conducted inside, and how does that model stay coherent as the system changes?**

A team can run Spec Kit's pipeline inside Memar without conflict. Neither replaces the other, because neither addresses the other's question.

## 2. What Spec Kit has that Memar does not
Stated as lessons a framework could take, each with the evidence that supports it. This is an inventory of genuine strengths, not a shopping list — the filter is in section 8.

1. **A bounded, ranked budget for the ambiguity you defer.** `/specify` allows at most three `[NEEDS CLARIFICATION]` markers, ordered by impact (`scope > security/privacy > UX > technical details`, `templates/commands/specify.md:128-129`); `/clarify` runs a twelve-category coverage scan marked Clear/Partial/Missing and selects questions by an explicit Impact × Uncertainty heuristic, capped at five questions per session (`templates/commands/clarify.md:73-138`). Memar's `Ask rather than assume` norm ([Cognition → Discourse Norms](../cognition.md#discourse-norms-derived-from-this-model) — **Evidence**) says to prefer a question to an assumption but sets no budget, no ranking, and no record of what was deferred. "Be explicit about uncertainty" is unimplementable advice; "at most three marked gaps, chosen by this ranking, and the rest recorded as open questions" is implementable.

2. **A reply grammar narrow enough for a probabilistic counterpart to parse.** `/clarify` asks exactly one question at a time, each answerable by two-to-five mutually exclusive options or a phrase of five words or fewer, states a recommendation with its reasoning up front, accepts `"yes"` / `"recommended"` / `"suggested"`, and never reveals queued questions in advance (`clarify.md:129-179`). Memar's asymmetry obligation requires returning material "in a form the counterpart can use" ([Cognition → What Implementation Asymmetry Obliges](../cognition.md#what-implementation-asymmetry-obliges) — **Evidence**) — usable content, not a usable reply shape.

3. **Detection separated from repair, with the checker returning a route instead of a patch.** `/analyze` is strictly read-only, offers remediation but never applies it, and its Next Actions block names the *owning* command per finding class, under the doctrine "return to the earlier step that owns them and fix them at the source" (`analyze.md:58, 194-199, 202`). Memar's Test practice requires that a failed check whose *expectation* was wrong revise the expectation first, as a recorded change ([Test Practice → The Cycle](../protocols/process/test.practice.md) — **Evidence**) — the same instinct, without the requirement that the checker's output say where the repair belongs.

4. **Termination as a provable no-op.** `/converge` has two terminal states, and the success state requires that `tasks.md` be left "byte-for-byte unchanged (no empty Convergence header)" and a fixed string reported (`converge.md:82-84, 228-232`); `/analyze` is told to "report zero issues gracefully". Memar owns the epistemic half of this — "A green run establishes exactly one thing: every check the run performed, on the instance it performed them against, matched the expectations that check states" ([Test → What a Passing Suite Establishes](../protocols/process/test.md#what-a-passing-suite-establishes) — **Evidence**) — but not the artifact-level half: that an empty result must leave the shared medium untouched.

5. **A marker that cannot be trusted, because the auditor also writes the marker.** "Include every existing task in the intent inventory, regardless of checkbox state or Convergence phase: completion claims are not evidence" (`converge.md:147-148`). Memar states the principle for expectations ("An expectation held only in the mind of the actor is one person's private model, and a private model is neither reviewable by another participant nor decidable by any check") but has no typed marker discipline where the same party both records progress and verifies it — its changelog `Contributors` field accepts `approved` as an open-vocabulary role tag with nothing saying who may write it.

6. **Gap types named, including the one nobody looks for.** `/converge` classifies divergence as `missing`, `partial`, `contradicts`, or `unrequested` (`converge.md:156-163`) — where `unrequested` means code present that no artifact called for, which it surfaces but refuses to delete. Memar's Content Rule forbids fabricated content ([Documentation → Content Rule](../documentation.md#content-rule-no-fabricated-or-redundant-provenance) — **Evidence**) but has no named category for material that accumulated without any decision producing it.

7. **Escape hatches that cost something.** `## Complexity Tracking` is filled "ONLY if Constitution Check has violations that must be justified", with a mandatory third column "Simpler Alternative Rejected Because" (`templates/plan-template.md:106-113`). Memar's rejected-position discipline requires one `Considered and not done` line "phrased as that alternative and why it was not taken" ([Documentation Practice → Rejected positions](../documentation.practice.md#rejected-positions) — **Evidence**) — the same requirement, stated once, in the right place.

8. **Requirements quality typed separately from implementation completeness.** `/checklist`'s preamble is "CRITICAL CONCEPT: Checklists are UNIT TESTS FOR REQUIREMENTS WRITING", with an explicit block separating "does the implementation work" from "are the requirements well-written" (`checklist.md:11-28`), and the `[x]` semantics restated in five files because one glyph carries two meanings across two artifact families. Memar's `Status` ladder (`Draft`/`Proposed`/`Final`/`Superseded`/`Rejected`) is typed from the start, which is the stronger position, but Memar has no quality gate on a document *before* it is enacted.

9. **The binding constraint named as a first-class cause.** "The underlying cause of context window exhaustion… usually right before or after context compaction is triggered" ([`docs/concepts/complex-features.md:9-13`](https://github.com/github/spec-kit/blob/ae5ade7234be5cb1d975f736c4e06dd46d1326d6/docs/concepts/complex-features.md)). Memar's skill states the same diagnosis and the same response (session economy, bounded delegation).

10. **Candid disclosure of where the method is not used.** `docs/guides/agentic-sdlc.md` names the single feature where SDD was dogfooded, and states "This does not mean every change goes through the full workflow", "Today these project workflows do not consume Spec Kit's bundled `bug` extension", and "There is no automatic handoff between those processes". Memar states the *requirement* — a development framework's goals "should be achievable both by the systems developed within it *and* by the framework's own development processes" ([Framework → Goal-Oriented Frameworks and Purpose Space](../framework.md#goal-oriented-frameworks-and-purpose-space) — **Evidence**) — without a maintained statement of where Memar is not applied.

11. **Deterministic substrate, prose process.** Every command's frontmatter declares `sh` / `ps` / `py` script variants and the scripts emit JSON contracts. Memar holds this position more cleanly: the script declares its own interface and "those declarations, not prose anywhere else, are the authority" ([Scripts → Putting text into a file](../../.agents/scripts/README.md) — **Evidence**).

12. **A hard rule separated from a scoring rubric, and each labeled as which.** `CONTRIBUTING.md:60-87` has one firm evidence gate and a seven-dimension 0–2 rubric that "guides prioritization — it is not a hard pass/fail gate".

13. **Failure over silent fallback, declared as deliberate.** A typo'd `SPECIFY_INIT_DIR` errors rather than resolving elsewhere, "because a typo never writes specs into the wrong project" ([`docs/guides/monorepo.md:66-70`](https://github.com/github/spec-kit/blob/ae5ade7234be5cb1d975f736c4e06dd46d1326d6/docs/guides/monorepo.md)).

14. **"Please remember to bump" turned into a merge requirement.** `.github/scripts/check_extension_version_bump.py` fails any PR that changes an extension without bumping its manifest version, with the rationale recorded as a shipped bug class: content that changes without a bump "go silently stale on every project that already installed the extension". Memar has a parallel obligation — a changelog entry must name every other artifact it should affect, with `Pending` and `Rejected` as closed searchable states ([Documentation Changelog → Propagates to](../documentation-changelog.md#propagates-to) — **Evidence**) — and nothing reports undischarged `Pending` entries.

15. **A required check that is skipped by path filtering blocks every PR; diff against the merge parent, not the base SHA.** Both traps are documented in `extension-version-guard.yml` with observed failure IDs. Engineering hygiene rather than framework doctrine; listed because Memar's `check` obligation has the same shape of problem.

## 3. Where Memar is stronger
1. **One continuous mental model against five parallel discovery surfaces.** Spec Kit teaches its method to a host agent through commands (Markdown/TOML/YAML), skills, agent-context files, MCP, and native hook events — five channels, each a place where the method can be carried partially. Memar states the principle and the failure it predicts: "each introduction may advertise several plugins; each plugin may ship several skills; each skill carries a fragment. The result looks installable and feels modular, but the *model* is no longer continuous" ([Knowledge → A Project Carries One Continuous Mental Model](../knowledge.md#a-project-carries-one-continuous-mental-model) — **Evidence**).

2. **Runtime reading over materialization, and the constitution-sync episode proves it.** Spec Kit propagated its constitution into dependent templates; removed that because it "duplicated the single source of truth and fought the preset/override composition system"; and now ships a bundled preset that reintroduces the removed behavior with a caveat section that includes "A pre-filled Constitution Check can bias `/plan`" ([`presets/constitution-sync/README.md`](https://github.com/github/spec-kit/blob/ae5ade7234be5cb1d975f736c4e06dd46d1326d6/presets/constitution-sync/README.md)). Memar's rule — content lives in one authoritative home and other documents link rather than repeat, because "repetition is where documents go to drift apart" ([Documentation → Content Rule](../documentation.md#content-rule-no-fabricated-or-redundant-provenance) — **Evidence**) — is the resolution of that tension rather than a stage in it.

3. **Version history organized around the task and decision, not the snapshot.** Memar states the principle ([Knowledge → Task-Centric Knowledge Evolution](../knowledge.md#task-centric-knowledge-evolution) — **Evidence**) and backs it with a searchable propagation ledger. Spec Kit claims the git-shaped version of this and does not build it: `spec-driven.md:21` says specs are "expressed and versioned, created in branches, and merged", and `spec-driven.md:59` lists "Branching for Exploration" as a core principle, while `specify.md:110` makes branch and spec directory independent and `converge.md:68-69` disclaims history outright ("no git, no branch comparison, no history").

4. **Checkable form over ritual, and a refusal to adopt the ecosystem's name.** Memar's Test protocol keeps "the ordering and the checkable form; the tools are selected afterward" and explicitly declines the TDD label ([Test → The Ecosystem's Name for This Is TDD, and This Protocol Does Not Adopt It](../protocols/process/test.md) — **Evidence**). Spec Kit holds both extremes at once: `tasks-template.md:12` says "Tests are OPTIONAL - only include them if explicitly requested", while `spec-driven.md:312` says "This is NON-NEGOTIABLE: All implementation MUST follow strict Test-Driven Development".

5. **A green run scoped to what it checked.** Memar's statement of what a passing suite establishes is one sentence and unarguable. Spec Kit's `/analyze` claims "Deterministic results: Rerunning without changes should produce consistent IDs and counts" (`analyze.md:243`) with no test asserting it, and its checklist counting is model-implemented regex with no stated tolerance for a literal `- [ ]` inside a fenced example.

6. **Enumeration instead of percentages.** Coverage under Memar is answered by enumerating the protocol surface the obligation is over, "not a number of Test files, not a percentage of statements" ([Test → A Test Is Part of the System That Owes It](../protocols/process/test.md) — **Evidence**). Spec Kit's `/analyze` reports a coverage percentage.

7. **A canon that is a home, not a truth.** Cognition already refuses the reading Spec Kit's community catalogs invite: "Canonical means: the authoritative *home* of a claim is the governing document, not a participant's memory; it does not mean every sentence in every file is true."

8. **Terminology divergence declared rather than absorbed.** Spec Kit's `agent-context-defaults.json` carries 39 agent keys while the integration registry carries 42, including a `windsurf` key with no corresponding integration at all, and the file's own comment says the mapping is "independent of the Specify CLI by design", so nothing tests the two lists agree. Memar's divergence policy requires acknowledging explicitly that a definition departs from common usage "rather than left for the reader to discover through confusion" ([Framework → Terminology Caveat](../framework.md#terminology-caveat) — **Evidence**).

## 4. Limits and failure modes in Spec Kit
Stated without calling the project worthless — these are failure modes when it is treated as a development framework.

1. **The doctrine has drifted from the shipped artifacts, in the file the README links as the methodology.** `spec-driven.md` quotes a `### Phase -1: Pre-Implementation Gates` block with Simplicity, Anti-Abstraction, and Integration-First gates; a repository-wide search finds `Phase -1`, `Pre-Implementation Gates`, and `implementation-details` only inside `spec-driven.md` itself, and `plan-template.md` has none of them. It describes an `implementation-details/` convention that exists nowhere, quotes a checklist whose items differ from the shipped sixteen, uses the `/speckit.specify` dot-form throughout while README and quickstart use the skills form, and claims the constitution has nine articles when the template ships five slots. It also says "The constitution's power lies in its immutability" and then, eleven lines later, documents constitutional evolution with SemVer bumps (`spec-driven.md:380-401`).

2. **Its central automation claims are unimplemented and stated as fact.** "When a product manager updates acceptance criteria, implementation plans automatically flag affected technical decisions" (`spec-driven.md:23`); "Change a core requirement in the PRD, and affected implementation plans update automatically" (`:45`); "consistency validation continuously improves quality… not as a one-time gate, but as an ongoing refinement" (`:27`). No command, template, or script does any of this.

3. **The constitution's enforcement is prose, and the strongest evidence is that the project opts out of its own artifacts.** `plan.md:164` says "ERROR on gate failures"; nothing in `scripts/` inspects a plan's `## Constitution Check` — the verdict is the model reporting on itself. The repository's `.gitignore` excludes `.specify/` and `specs/` as "meant for dogfooding Spec Kit during its own feature development", so no artifact set is reviewable in a pull request. The ratified constitution is the only committed artifact of the method.

4. **Self-grading, contradicting its own doctrine.** `/specify` generates `checklists/requirements.md` and then validates the spec against it, re-running until all items pass with a maximum of three iterations (`specify.md:144-197`). `/checklist`'s core doctrine is that checklists are reviewer-owned and the agent "MUST NOT mark generated items `[x]`" (`checklist.md:32-37`). The exception is documented and never resolved.

5. **A position stated three incompatible ways.** Whether `/constitution` keeps dependent templates in sync is answered yes (`agentic-sdlc.md:40`), no ("Dependent templates and commands read the constitution at runtime and are not modified here", `constitution.md:23-24`), and "it was dropped" (`presets/constitution-sync/README.md:9-12`).

6. **Software-only assumptions inside the executor.** `implement.md:99-140` embeds a fifteen-language ignore-file matrix and creates seven ignore files as a required step; `plan-template.md:68-101` offers exactly three software layouts and no alternative. The domain-agnostic claim rests on the extensibility substrate, not on the method — nothing in the repository demonstrates SDD applied outside software.

7. **Scaling is handled by capping, not by design.** Three clarification markers, five clarify questions, fifty analyze findings, three self-review iterations. Above those, the answer is hand-maintained roadmap tables with "no special tooling behind it", or a third-party community extension.

8. **Regex-shaped mechanics presented as robust.** Toggling only the checkbox marker "outside of code fences" to avoid noisy diffs, and counting `- [ ]` / `- [X]` / `- [x]` across a directory, are model-implemented pattern matching with no script and no test.

9. **A documented internal contradiction about a security boundary.** Its own constitution's Principle V requires project-relative paths to be confined to the project root; `core.md:55` documents `SPECIFY_FEATURE_DIRECTORY` as joined "without a containment check", and `monorepo.md:84-87` generalizes it — the project root "identifies the Spec Kit project and its command/configuration context, not a containment boundary for feature documents". The rule is enforced in the CLI's code and explicitly declined on the axis the agents actually use. Memar's terminology governance requires a changed definition to state "what changed, why, and what it implies for documents that already depend on the old sense".

10. **Ritual with no observable payoff.** The `### Session YYYY-MM-DD` Q→A changelog inside the spec duplicates information already integrated into the section bodies; `[P]` parallel markers are a human-team artifact that in an agent context licenses concurrency the agent cannot observe; `spec-driven.md:105-163` is a marketing comparison table, not a measurement.

11. **Documentation pointing at files that are not there.** Two contract test modules cite `contracts/bundle-catalog.schema.md` and `contracts/bundle-manifest.schema.md`; there is no `contracts/` directory. `design/workflow-step.md` and `workflows/ARCHITECTURE.md` describe `workflows/steps/` where the tree has `workflows/step/`; `presets/ARCHITECTURE.md` shows `presets.py` and `catalog.py` as single files where the tree has a `presets/` package.

12. **A manifest richer than its installer.** `docs/reference/bundles.md` records that "Pin enforcement is install-time only. Idempotency checks are id-based, not version-aware" and that bundle-local `steps/<id>/` payloads and relative `provides.steps[].source` overrides "are not resolved in this release" — features the manifest can express and the installer silently ignores.

## 5. What the distribution layer costs a mental model
This is the part of Spec Kit with no counterpart in Memar, and the part Memar's model predicts most sharply.

The measured shape: 42 registered agent integrations, a `CommandRegistrar` base of about 75 KB carrying three separator hooks and a dual-layout mode hook purely because some agents differ between commands and skills, an extension system whose manager is a single 276 KB module, a preset stack with a four-level template resolution order and four composition strategies, a workflow engine with twelve step types, and a bundle layer on top. The 178 community extensions, 41 community presets, and 3 bundles in the catalogs are force-included into the published wheel "for offline discovery"; none is marked verified.

Three consequences are visible in the repository rather than predicted:

- **Discovery has become a governance liability before any review infrastructure exists.** A default `search` surface listing 178 unvetted third-party packages is a different kind of default from "install what your team wrote".
- **Fragmentation shows up as list drift.** 39 agent-context keys against 42 integrations, with an orphan key and no test asserting agreement. This is not a maintenance slip; it is what happens when one model is projected into five channels that nothing reconciles.
- **The layering makes provenance unanswerable.** Extension manifests, preset overrides, workflow overlays, and bundle composition are four composable declarative layers over the same Markdown. Spec Kit builds attribution reporting to compensate (`specify workflow resolve` prints which layer won and which are hidden), and still ships a preset whose documented cost is that it biases the reader of the artifact it rewrites.

Memar's position is that a consuming project installs a pointer and receives no copy ([Scripts → A consuming project receives no copy of these files](../../.agents/scripts/README.md) — **Evidence**: "One fetch, one update, every consumer"), and that harness engineering "should not be mistaken for the foundational theory of interaction with Agents. They operate at a lower level" ([Agency → Prompt Engineering and Harness Engineering](../agency.md#prompt-engineering-and-harness-engineering) — **Evidence**). On the evidence above, Spec Kit's distribution layer is competent engineering and a standing demonstration of what the fifth layer costs.

## 6. Direct conflicts if imported into Memar
1. **A pipeline of named phases.** Memar states that "Modeling, Protocol, and Architecture are not sequential phases in a linear pipeline" ([Modeling → Modeling, Protocol, and Architecture](../modeling.md) — **Evidence**). A `specify → plan → tasks → implement` chain is that reading.
2. **Checkbox state as the resume mechanism.** Memar's continuity mechanism is the handoff record carrying decisions, ambiguities, assumptions, and next steps across a session boundary; progress lives in changelog entries, not in a mutable checklist an agent also writes.
3. **A constitution document with a global version.** Memar distributes principles across concept documents, each with its own `Status` and changelog; a single versioned principles file re-centralizes what Memar deliberately distributed, and its SemVer-for-governance policy would collide with per-document supersession.
4. **Copying governing text into artifacts.** This is the constitution-sync lesson; Memar's Content Rule forbids it directly.
5. **Templates per artifact purpose.** Memar prescribes one document skeleton and an optional-section catalog because "a separate independent template per document purpose tends to produce definitional drift over time instead" ([Documentation Explanation → Optional Sections](../documentation-explanation.md) — **Evidence**). A `spec-template` / `plan-template` / `tasks-template` set is that shape.
6. **A host-tool plugin, marketplace card, or harness matrix.** Memar's distribution position is a pointer ([README → Using Memar in another project](../../README.md#using-memar-in-another-project) — **Evidence**).
7. **Normative grids.** Memar's written surface forbids carrying load-bearing logic in grid layouts ([Documentation → Written surface](../documentation.md#written-surface) — **Evidence**); Spec Kit's coverage summary tables, severity tables, and complexity-tracking tables are the form Memar declines.
8. **Percentages as coverage evidence.** Memar answers coverage by enumerating the surface the obligation covers.

## 7. Costs and limits on both sides
### Spec Kit
- The method's claims and the method's artifacts disagree, in the document the README nominates as the methodology.
- Enforcement of the governing principles is a model reporting its own verdict, and the project does not commit its own artifacts for review.
- Roughly half the workflow engine's step-type surface serves capabilities none of the three bundled workflows use; all three use only `command` and `gate`.
- Three script runtimes cost about 193 KB of differential parity tests as the migration toll, and the Python port is not yet the default.
- The `events` subsystem is about 120 KB across two files with no user documentation; `extensions/__init__.py` is a single 276 KB module for a domain split into modules elsewhere in the same codebase.
- About 936 KB of committed generated `.lock.yml` files, and a pre-commit configuration that runs four whitespace hooks while CI runs the linter, the markdown linter, and the shell checker.

### Memar
- **No work decomposition and no delivery state.** Nothing in `docs/` owns how a development is broken into units of work, what a unit of work is, or how progress is recorded against one. `Knowledge → Task-Centric Knowledge Evolution` treats the Task as the unit of knowledge *evolution*, and the changelog's `Tasks` field explicitly declines to require a task system. `Software → The software life cycle` records this as prior art with "No home yet; owed".
- **No requirements artifact.** Requirements concepts are spread across Modeling and its constraints, with "Full treatment owed".
- **No review or approval authority.** Nothing states who approves what, when, or what an approval record is. `Software` names "the review process owed"; `Terminology → On Independent Verification, Today` describes Memar as "largely single-author" and treats structured AI critique as an interim form of scrutiny explicitly not equivalent to peer review.
- **No traceability surface.** The `ID` front matter field "carries no meaning beyond relative creation order"; the only cross-artifact edges are free-text `Propagates to` and `Cited` bullets inside changelog entries. Answering "which documents depend on this one" requires a full-text search.
- **The one machine check covers formatting and links only.** Encoding, newlines, written surface, and links. Not cross-document consistency, not undischarged `Propagates to: Pending`, not rejected-position lines that leaked into a body.
- **No framework-level identity a consumer can name.** `Status` is per document; there are no versions, tags, or releases for the framework itself. This is a defensible trade against a model that is meant to stay live — but a reader six months later cannot tell which state of the model a decision was taken against.
- **Governance of Rules is unfinished by its own account.** `Rule → What This Document Does Not Define` leaves the final notation for linter-checkable Rules, the primary framing, and per-subject catalogs open.

## 8. What Memar can learn
### Absorb
1. **A budget and a ranking for deferred ambiguity, in `Ask rather than assume`.** The norm gains two clauses: ambiguity that is *deferred rather than asked* is recorded where it can be found again, and the deferred set is itself kept visible with a stated ordering. The budget bounds deferral, never asking — a cap on questions would license assumption, which is the failure the norm exists to prevent. Home: [Cognition → Discourse Norms](../cognition.md#discourse-norms-derived-from-this-model) and [Cognition Practice](../cognition.practice.md).
2. **An empty result must leave the medium unchanged.** A report, review, or check whose result is empty produces no artifact: no empty section, no placeholder, no empty changelog entry. This generalizes `Trivial changes` from changelog entries to every artifact a check might write. Home: [Documentation → Written surface](../documentation.md#written-surface).
3. **Teach `check` to report undischarged obligations.** `memar-documentation.py check` already reports encoding, newlines, written-surface problems, and links. It should also report `Propagates to` entries in state `Pending` across the documentation set, and `Considered and not done` lines found in a body rather than a changelog. The obligations already exist in Memar's documents; nothing reports them. This is the highest-value item on the list, because it converts an existing mechanism from a convention into a check. Home: the script and [Scripts → Putting text into a file](../../.agents/scripts/README.md).
4. **A maintained statement of where Memar is not applied.** `Framework → Goal-Oriented Frameworks and Purpose Space` states the consistency requirement; nothing records the current answer. A short section on the project README, kept as the answer changes, is the disclosure instance of a principle Memar already holds.
5. **Separate the hard rule from the rubric, and label which is which, in Memar's own contribution norms.** One sentence, in [Cognition Practice](../cognition.practice.md) or the contributing surface: the evidence gate is firm; any scoring is prioritization and is not a pass/fail gate.

### Adapt
6. **A parseable reply grammar for interactive exchange.** Take from `/clarify` the narrowing of the answer's shape and the practice of stating a recommendation with its reason, and put it under [Agency](../agency.md) or the asymmetry obligation. The adaptation must preserve ask-rather-than-assume: a narrowed grammar may make a question easier to answer, and must never become a forced-choice funnel that manufactures a decision the counterpart did not hold.
7. **The checker returns a route, not a patch.** Extend [Test Practice](../protocols/process/test.practice.md)'s disposition step so that a check reporting a wrong or incomplete expectation also names the artifact that owns the repair.
8. **Type the marker that records an approval.** If a changelog entry may carry `approved`, the schema should say who may write it and that the writer is not the verifier — the discipline `/converge` states for checkboxes ("completion claims are not evidence").

### Reject
- A constitution document, global framework versioning, and SemVer-for-governance. Memar distributes principles and supersedes documents individually; a single versioned file re-centralizes them.
- The phase pipeline, per-artifact templates, and checkbox-as-resume.
- The harness matrix, plugin packaging, marketplace catalogs, and community-extension discovery as a default surface.
- Copying governing text into artifacts — the constitution-sync experiment is the evidence, and it points the other way.
- Coverage percentages as evidence; enumeration of the obligation's surface is Memar's answer and the better one.
- Normative grids, and the `spec-driven.md` habit of an essay that describes machinery the repository does not contain.

### Separate research
9. **Work decomposition — does Memar own it?** The honest gap. Two questions, in order: (a) is *decomposing a development into named sub-processes, each with its own written expectations* a Process concept Memar should own at the concept level, stated domain-independently, with the concrete per-feature artifact set left to consuming projects; (b) if not, is the absence a correct scoping decision that should be stated, rather than an omission. `Software → The software life cycle` already flags the territory as prior art to examine rather than authority to inherit. This should be a `.research.<NNN>.md` companion, not a document drafted from this comparison.
10. **The `unrequested` category.** Whether Memar needs a named home for "material that exists without a decision producing it" — distinct from fabricated content, which the Content Rule already forbids. Candidate homes: the Content Rule, Process, or a concept this comparison has not thought of. Research, not a change.

## 9. Possible relationship
1. **Memar remains the authority** for concepts, terminology, model, protocol contracts, knowledge, process, and change discipline.
2. **Spec Kit is a software-delivery implementation that may run inside Memar.** A team may adopt its pipeline as one project's realization of Process for one class of work — software features — without adopting its distribution platform, its templates as Memar doctrine, or its governance model.
3. **The artifacts it produces are a projection of whatever model the project holds**, not a substitute for it. A `specs/003-user-auth/` directory is evidence about one feature's intent; it is not the project's knowledge.
4. **Compatibility requires an explicit contract**, and the interesting clauses are the ones Spec Kit's own history exposes: which document owns a claim, whether a governing statement is read at runtime or copied into an artifact, and what makes a completion claim evidence.

## 10. Decision
Spec Kit is not a substitute for Memar and is not in the same category. It is a well-built, candidly-limited software feature pipeline with a large and largely unnecessary distribution platform attached; Memar is a domain-agnostic model and discipline that does not cover feature delivery at all.

The comparison does not justify changing Memar's governing method. It identifies three absorptions that strengthen mechanisms Memar already owns — a deferral budget for `Ask rather than assume`, an artifact-level rule that an empty result changes nothing, and a `check` that reports obligations already written down — and one research thread Memar has deferred to itself: whether work decomposition belongs in Memar's concept layer.

The strongest argument Memar has against Spec Kit is not any single feature but the direction of its growth. Nine commands became five distribution subsystems; the essay describing the method stopped matching the artifacts; the propagation behavior was removed, then re-shipped as an opt-in preset with a caveat that it biases the reader; and a 39-versus-42 list mismatch now sits in a shipped JSON file that nothing checks. A model delivered through five channels with four composable override layers has a predictable failure mode, and this repository exhibits it. That is an argument from a stated principle meeting observed evidence, which is the only kind worth making.

## 11. Open for critique
- Whether the credit in section 2 is sufficient, and whether any of the fifteen items is stronger than stated.
- Whether "a budget for deferred ambiguity" is an improvement to `Ask rather than assume` or a constraint that will be read as permission to stop asking.
- Whether the three absorptions are correctly scoped, and whether the `check` extension is too broad for one change.
- Whether the decision to treat work decomposition as research rather than as an omission is right, or whether it is the same pattern Spec Kit demonstrates — deferring the hard part until it is hard.
- Whether section 5's argument is fair to a distribution platform whose target audience is adoption breadth rather than model integrity.
- Any unfair characterization of Spec Kit. Every claim here is cited to a file and line so it can be checked; the ones that should be re-read first are the counts in section 1 and the drift claims in section 4.
