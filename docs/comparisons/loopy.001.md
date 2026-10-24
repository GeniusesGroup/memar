# Comparison: Memar and Loopy
This comparison evaluates [Forward-Future/loopy](https://github.com/Forward-Future/loopy) against Memar. It finds that Loopy is a careful, well-bounded session-workflow pack for repeatable agent work, and that its discipline overlaps a real gap Memar left at the session surface — which this session narrows without importing the pack.

This audit inspected Loopy at commit `75966cb` (the checkout under review), reading `README.md`, `AGENTS.md`, `skills/loopy/SKILL.md` with its `references/` workflows, and `CHANGELOG.md`. No loop was installed or run; the live catalog was not queried. Memar is read from this repository's live `docs/` and `.agents/skills/memar`.

## Table of contents
- [Comparison: Memar and Loopy](#comparison-memar-and-loopy)
  - [Table of contents](#table-of-contents)
  - [1. What each project is](#1-what-each-project-is)
  - [2. What Loopy has that Memar does not](#2-what-loopy-has-that-memar-does-not)
  - [3. Adoption filter](#3-adoption-filter)
  - [4. Problems and limits in Loopy](#4-problems-and-limits-in-loopy)
  - [5. Why Memar still exists](#5-why-memar-still-exists)
  - [6. What to add to Memar](#6-what-to-add-to-memar)
  - [7. Open for critique](#7-open-for-critique)

## 1. What each project is
### Loopy (self-definition)
A **loop library plus an installable agent skill** for repeatable work. A loop is a playbook with feedback built in: what the agent tries, how it checks the latest attempt, what it does with what it learned, when it finishes or asks for help. The website is the catalog; the Loopy skill is the guided workflow (discover, find, audit, adapt, craft, run, debrief, save, publish). Bounded passes, one acceptance check applied each pass, an evidence receipt per run, and a debrief that separates loop-design issues from execution, tool, environment, or goal problems.

### Memar (self-definition)
A **domain-agnostic system-development framework**: shared definitions and practices for developing systems (software, hardware, organizations, …). One discovery practice loads **live documentation**; cognition and agency norms govern exchange. Contracts are realized by the implementation modules in this repository. Plugin manifests are **delivery tax**, not the mental model.

### Category distinction and direction
- Loopy ≈ how an agent should run a bounded, repeatable task in a session
- Memar ≈ what shared model of systems and knowledge the work is conducted inside

The session-workflow discipline is a small part of what Memar must govern, so the direction here is absorption, not coexistence. Where Loopy's pack carries durable workflow knowledge, Memar takes it into its own homes until the pack becomes unnecessary inside a Memar session; what remains outside is product surface (hosted catalog, installer mechanics), not knowledge.

## 2. What Loopy has that Memar does not
Real strengths relative to Memar's surface — observations, not a shopping list:

1. A named bounded-execution discipline (finite run boundary, same acceptance check each pass, named terminal states: success, clean no-op, blocked, approval-required, exhausted, no progress; errors never reported as success).
2. Receipt and debrief as separate artifacts with separate verdicts (run explanation versus design judgment; one run is one result, not a pattern).
3. A plain-language craft interview (one question at a time, no jargon, neutral wording, no invented defaults, early catalog scaffold, abort to one-shot when fresh feedback cannot change the next action).
4. Find-then-craft with a catalog-overlap gate (search live catalog first, prefer adaptation, never invent titles, numbers, or URLs).
5. A silent preflight trace of one full cycle before delivery, with grounding rules (no invented stack, metric, schedule, owner, or permission).
6. Local reuse with staleness awareness (`LOOPS.md` project file, source URL plus source modified date, one-sentence change notice, secrets refused, file treated as untrusted reference).
7. Draft-by-default publication with exact preview, separate attestation confirmation, and read-back verification.

Memar already overlaps some *concerns* (ask and confirm at intake, handoff across sessions, changelog approval by a reviewer that did not do the work, thrifty sub-agents, Agency acceptance criteria, Test expectations before enactment) without shipping them as that session pack. Claiming Memar has "almost no session workflow" overstates the gap: Cognition, Handoff, Changelog, Agency delegation, and Test practice are operational — they were thin at exactly two points this comparison addresses, in-session critique shape and the bounded-pass stop vocabulary.

## 3. Adoption filter
### Absorb by strengthening existing homes
- Finite boundary plus same check plus named stops → Agency acceptance criteria and Test expectations, surfaced in the skill's agent workflow; not a loop Iron Law.
- Four-part critique request (claim quoted, evidence as command or passages, boundaries, verdict asked for) → Cognition Practice second-opinion shape and Changelog Practice approval procedure; one shape, two landing places (handoff reasoning versus `approved` tag).
- One question at a time, short options, preferred first, no funnel → Cognition Practice norm-application-points (already); no new interview skill.
- Search-before-invent and overlap check → report-absence discipline (read owning documents before calling a gap); not a catalog dependency.
- Run evidence preserved with loop definition, check, boundary, and stopping reason → session-folder material and handoff evidence, graduated through changelog; not a standalone receipt mythology.

### Reject for Memar
- Nine-path skill pack as how the project *is* — one continuous mental model ([Knowledge](../../modules/knowledge/knowledge.md#a-project-carries-one-continuous-mental-model)); failed Memar trials: separate Khayyam skill, Cognition as peer skill.
- Marketplace and multi-harness install matrix as a Memar goal — Agency is not harness theory; prompt and harness sit under Communication ([Agency → Prompt Engineering and Harness Engineering](../agency.md#prompt-engineering-and-harness-engineering)).
- `LOOPS.md` as persistent memory — thinking is a process, not a store ([Cognition → What Thinking Is](../cognition.md#what-thinking-is)); handoffs retire on graduation; reusable patterns graduate into governing documents, they do not accumulate as local prompt files.
- Live external catalog as source of truth — Memar's source of truth is the live documentation in the repository; an outside database cannot hold that position.
- Prompt-compression norms (fewer than 80 words) and loop-versus-one-shot heuristics as framework rules — durable concepts, not patches for today's model limits.
- Grid layouts or diagram blocks as carriers of normative logic — Memar keeps load-bearing logic linear ([Written surface](../../modules-plugable/knowledge/documentation/documentation.md#written-surface)).

### Already owned
Intake ask and confirm, report-absence, handoff produce and consume with mid-session tangents, changelog approval with an independent reviewer (a sub-agent without session context, usually a smaller model), sub-agent session economy, Agency delegation with responsibility, authority, capability, context, knowledge, acceptance criteria, and escalation as a designed boundary.

## 4. Problems and limits in Loopy
Stated without calling the project worthless — failure modes when it is treated as a development framework:

1. **Process without durable domain knowledge** — loops carry behavior plus checks, not a living ontology. Strong pass discipline cannot replace an internal knowledge structure at system scale.
2. **Catalog dependence** — the live catalog is the source of truth; when it is unreachable, discovery is declared unavailable. Honest, and a single external point of failure for find, craft-scaffold, and publish gates.
3. **Harness coupling** — the skill assumes web access, thread-history tools, and per-agent installation. Without those, the nine paths are dead weight; per-agent maintenance follows.
4. **Ceremony pressure on tiny tasks** — six interview questions, preflight, receipt, debrief offer, save offer. The abort-to-one-shot rule and stop-asking-early rule mitigate this; the mitigations are agent-judged.
5. **Receipt without graduation** — a receipt preserves what ran, but nothing in the loop model decides what becomes durable knowledge, where it lands, or what retires. Memar's handoff graduation and changelog provenance answer exactly that.
6. **`LOOPS.md` as silo** — correctly labeled untrusted and correctly staleness-checked by date, but still a project-local prompt accumulation with no concept-admission rule, no identity independent of path, and no propagation tracking. Date comparison detects change; it does not judge semantic drift.
7. **Overlap search is registry matching, not modeling** — outcome, trigger, verification, and keyword similarity prevent near-duplicate publication; they do not establish whether two loops name the same concept.
8. **Authority model is prompt-scoped** — selecting never runs, running never schedules or publishes, destructive acts pause for approval. Sound inside the skill; outside it there is no contract, accountability, or trust model beyond the prompt.

## 5. Why Memar still exists
1. **Different job** — repeatable-task discipline versus shared system and knowledge model across domains.
2. **Scale** — pass rituals without internal knowledge structure fail as the system grows.
3. **One model, many projections** — adapters may multiply; the model must not fragment into loop packs or memory files.
4. **Text and code each where they belong** — concepts in docs; generative work in callable services.
5. **Write for the subject's structure** — durable concepts, not patches for last year's model limits.
6. **Test as Process discipline** — expectations of input and output written before enactment; not a loop check bolted onto prose.

A Memar session must not need the Loopy skill: the durable discipline (bounded passes, receipt and debrief separation, four-part critique) now lives in Memar's own homes, and this session is the evidence. What stays outside is the hosted catalog product and installer mechanics, which are not Memar's job — and a Memar-shaped replacement for even those remains possible, never required.

## 6. What to add to Memar
Filtered agreement from this session; applied where the home already exists:

**Done in this session**
- Generalized the skill's `Session economy with sub-agents` into `Agent workflow in sessions` (session container, intake, delegate versus tangent, brief shape, bounded execution with named stops, four-part critique and review, close by type); norms stay in Cognition, Agency, and facet Practices.
- Extended [Cognition Practice](../cognition.practice.md#norm-application-points) so an in-session second opinion uses the same four-part request shape an approval requires.
- Extended [Documentation Changelog Practice](../../modules-plugable/knowledge/documentation/changelog/changelog.practice.md#choosing-who-reviews) so the same request serves critique without an `approved` tag.
- Clarified [Handoff Practice](../../modules-plugable/knowledge/documentation/handoff/handoff.practice.md#mid-task-tangents) that bounded work needing integration is delegation inside the session, not a tangent.
- Required the human-last-resort order (skill workflow; [Cognition Practice](../cognition.practice.md#norm-application-points)): re-read, delegate, seek machine critique before asking the human; bring only what survives, with what was tried.
- Defined the run report and its debrief (skill close rule; [Debriefing Runs](../cognition.practice.md#debriefing-runs)): preserve what ran, the check, the boundary, the stopping reason beside the session; attribute across plan-design, execution, tool and environment, and goal causes; one run is one result.
- Pointed delegation intake at [Interaction With an Agent](../agency.md#interaction-with-an-agent): the ten dimensions a delegation must establish, which is Memar's standing answer to the craft interview.

**Later, carefully**
- Light practice for verifying Practice effectiveness (pressure scenario plus recorded outcome) — evidence culture without a fragile model-version eval farm.
- A bounded-export artifact (checkpoint-style coverage manifest with privacy controls) used as input to a handoff, never as the handoff.

**Do not add**
- Loop skill pack, `LOOPS.md` memory file, harness install matrix, catalog dependency, prompt-compression norms, or development-as-umbrella Explanation document unless a real concept gap remains after Process, Agency, and facet homes are checked. Refusing the packaging is how the replacement works: the discipline is absorbed, the distribution shape is not.

**Intentionally silent**
- Finished delivery of a structure Memar names, including the live-corpus knowledge service (orientation, extraction, retrieval), is Enterprise and Organization work, per [Where Memar Stops](https://github.com/GeniusesGroup/memar/blob/dc3d1433/README.md#where-memar-stops-and-where-work-continues) — the framework shows the shape, it does not hand over the built system.
- Subjects no Memar document governs stay reported absence per [Cognition](../cognition.md#report-absence-rather-than-supplying-it); silence there is neither availability nor unavailability, and becomes a question with an owner.

## 7. Open for critique
- Unfair characterizations of Loopy
- Adoption-filter flips
- Whether the bounded-pass stop vocabulary belongs deeper (Process or Test practice) rather than only in the skill workflow
- Whether a session-folder receipt deserves its own facet companion or stays as handoff evidence
- Tone that accidentally dismisses useful neighboring work
