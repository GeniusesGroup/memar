# Comparison: Memar and Superpowers

After examination by two agents — Composer (via Cursor) and GLM 5.3 Flash — against the Superpowers and Memar's live `docs/` and `.agents/skills/memar`, the results below are the joint finding. Owner positions from that thread are included where they decide the filter.

**Compared project:** [obra/superpowers](https://github.com/obra/superpowers)  
**Question answered:** why use Memar while a polished coding-agent methodology like Superpowers exists?

## Table of contents
- [Comparison: Memar and Superpowers](#comparison-memar-and-superpowers)
  - [Table of contents](#table-of-contents)
  - [1. What each project is](#1-what-each-project-is)
    - [Superpowers (self-definition)](#superpowers-self-definition)
    - [Memar (self-definition)](#memar-self-definition)
    - [Category error](#category-error)
  - [2. What Superpowers has that Memar does not](#2-what-superpowers-has-that-memar-does-not)
  - [3. Adoption filter](#3-adoption-filter)
    - [Absorb by strengthening existing homes](#absorb-by-strengthening-existing-homes)
    - [Reject for Memar](#reject-for-memar)
    - [Already owned](#already-owned)
  - [4. Problems and limits in Superpowers](#4-problems-and-limits-in-superpowers)
  - [5. Why Memar still exists](#5-why-memar-still-exists)
  - [6. What to add to Memar](#6-what-to-add-to-memar)
  - [7. Open for critique](#7-open-for-critique)

## 1. What each project is

### Superpowers (self-definition)
A **software development methodology for coding agents**: composable skills, session-start bootstrap, and a brainstorm → plan → implement → review → finish chain. Domain knowledge of the host product is not the payload; **session process ritual** is. Distribution is a multi-harness plugin/marketplace matrix.

### Memar (self-definition)
A **domain-agnostic system-development framework**: shared definitions and practices for developing systems (software, hardware, organizations, …). One discovery practice loads **live documentation**; cognition and agency norms govern exchange. Contracts are realized in language repositories. Plugin manifests are **delivery tax**, not the mental model.

### Category error
- Superpowers ≈ how a coding agent should behave in a session
- Memar ≈ what shared model of systems and knowledge the work is conducted inside

Both can coexist. Only one is trying to be a long-lived conceptual spine.

## 2. What Superpowers has that Memar does not
Real strengths relative to Memar's surface — observations, not a shopping list:

1. A ready coding-session pipeline (named skills, auto-trigger descriptions).
2. Forced session-start bootstrap toward skill use.
3. Productized subagent-driven development (implementer + two-stage review prompts/scripts).
4. Git worktree and branch-finish menus as first-class skills.
5. Optional visual brainstorm companion.
6. Broad harness install surface and a long porting guide.
7. Eval / plugin tests aimed at whether skills fire.
8. Host-repo plan/spec path convention with checkbox-sized steps.
9. Persuasion engineering against rationalization (Red Flags, Iron Laws, hard gates).

Memar already overlaps some *concerns* (ask / confirm, handoff, TDD as process discipline, thrifty sub-agents) without shipping them as that skill library. Claiming Memar has "almost no codified operations" overstates the gap: Cognition, Handoff, modeling practice, TDD practice, and documentation practices are operational — they are not a Superpowers-shaped pack.

## 3. Adoption filter

### Absorb by strengthening existing homes
- Design sign-off before large enactment → Cognition (already). Clearer routing into modeling/handoff if needed; no mandatory brainstorm skill.
- Inspectable plans for large changes → ordinary documentation results by facet; not a forced `docs/superpowers/` tree; not "junior with no judgment" theater.
- Evidence before claiming done → Process / TDD (expectations before enactment; machine-checkable checks where possible). Not Iron-Law deletion rituals aimed at today's agent weakness.
- Explicit review → Cognition Practice and modeling review; not a separate review-skill pack.
- Spike / bounded / architectural scale → implied by confirm-before-large-scope; name later if useful; never block clarifying questions.

### Reject for Memar
- Marketplace / multi-plugin / multi-skill as how the project *is* — one continuous mental model ([Knowledge](../docs/knowledge.md#a-project-carries-one-continuous-mental-model)); failed Memar trials: separate Khayyam skill, Cognition as peer skill.
- Harness-coverage race as a Memar goal — Agency is not harness theory.
- Heavy persuasion bootstrap — burns context; fights ask-before-assume.
- Prose Practices that belong in executable modules — contracts in docs; generation in language servers / tools agents call ([Knowledge and Code](../docs/knowledge.md#knowledge-and-code)).
- Software-only Iron Laws (worktree, PR menus, toolchain defaults) as core.
- Grid layouts or diagram blocks as carriers of normative logic — including preferring `dot` graphs for models; Memar keeps load-bearing logic linear ([Written surface](../docs/documentation.md#written-surface)).
- ALL-CAPS pressure language and absolute rules without co-located reason.
- Command/recipe catalogs in the Memar skill or growing paste files — scripts document themselves; host helpers are small executables, not prose dumps; no membership indexes of script or comparison folders ([Content Rule](../docs/documentation.md#content-rule-no-fabricated-or-redundant-provenance)).

### Already owned
Documentation-as-truth with discovery scripts; Handoff (agent-general); mid-session tangents; TDD generalized via Process expectations and checks; sub-agent session economy; critique norms.

## 4. Problems and limits in Superpowers
Stated without calling the project worthless — failure modes when it is treated as a development framework:

1. **Normative grids and diagrams** — Thought/Reality tables and control-flow digraphs mislead linear readers (models). Short non-normative lookup is fine; rules must be sentences or numbered steps.
2. **Process without durable domain knowledge** — skills teach behavior, not a living ontology. At scale, even strong process discipline cannot replace an internal knowledge structure; development path satisfaction collapses.
3. **Over-prescription and brittle auto-trigger** — 1% skill rule, stacked mandatories, description-matched triggers; evals exist because compliance is probabilistic; ceremony dominates tiny tasks.
4. **Internal rule tensions** — user override vs "no choice"; autonomous SDD vs checkpoint plans; review-every-task vs nonstop loops; reasons often not co-located with rules.
5. **Harness coupling** — without bootstrap injection, skills are dead weight; N-platform maintenance; compaction can drop bootstrap.
6. **Eval fragility and closed contribution** — baselines drift with model versions; high bar / few new skills → pack stays coherent as process and cannot become *your* knowledge base.
7. **Secondary frictions** — default visual-companion telemetry; single plugin version bump for any skill change (Memar's per-artifact changelogs are structurally stronger here).

Neighboring projects built around **tool-era problems** (early chatbots, then harnesses) often cannot evolve into an agency/knowledge model without rebuild — owner observation from the parallel thread. Superpowers is strong at today's coding-agent ceremony; that is also why it is not Memar's substitute.

## 5. Why Memar still exists
1. **Different job** — session etiquette vs shared system/knowledge model across domains.
2. **Scale** — rituals without internal knowledge structure fail as the system grows.
3. **One model, many projections** — adapters may multiply; the model must not fragment into skill packs.
4. **Text and code each where they belong** — concepts in docs; generative work in callable services.
5. **Write for the subject's structure** — durable concepts, not patches for last year's model limits.
6. **TDD as Process** — expectations of input/output written before enactment; not "unit-test Iron Law." Umbrella words like user-story read as system expectations, not as a separate mythology.

Using Superpowers-like session discipline *while* developing inside Memar can be coherent. Replacing Memar with Superpowers is not — unless the only goal is agent etiquette for small software changes.

## 6. What to add to Memar
Filtered agreement across both agents and owner positions:

**Do / keep doing**
- Hold TDD on Process (expectations and checks) + `tdd` protocol/practice — the Memar answer to "start from the test," without Superpowers packaging.
- Keep written-surface and documentation practice thin; keep discovery scripts as the navigation mechanism (`--help`, no recipe catalog in the skill).
- Keep this `comparisons/` folder as the public fair answer to "why not X?"

**Later, carefully**
- Light practice for verifying Practice effectiveness (pressure scenario + recorded outcome) — evidence culture without a fragile model-version eval farm.
- Conditional sentences with reason co-located where a norm still lacks them — not Red Flag tables.

**Do not add**
- Superpowers skill pack, SDD factory, harness matrix expansion, persuasion bootstrap, `docs/superpowers/` paths, development-as-umbrella Explanation document unless a real concept gap remains after Process/Framework homes are checked.

## 7. Open for critique
- Unfair characterizations of Superpowers
- Adoption-filter flips
- Next comparison subjects for this folder
- Tone that accidentally dismisses useful neighboring work
