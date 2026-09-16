---
name: tdd
description: turns the TDD protocol into the procedure a development step follows — write the developed process's input and output expectations before the work, in checkable form, and check the enacted instance against them; use whenever developing anything the Memar way, software or not, at any scale from a function to a system. Carries the steps only; the reasons, the scope, and the mechanism separation live in [tdd.md](./tdd.md) and [process.md](../process.md) and are not restated here.
---

# TDD Practice

> **Purpose:** This practice operationalizes [tdd.md](./tdd.md): it turns the discipline that document adopts — the expected input and output of a developed process stated before enactment, the enacted instance checked against them ([Process → Expectations and Checks](../process.md#expectations-and-checks)) — into the followable procedure for one development step. The reasons live in the base document and are not restated here; each step below links to the topic that argues it.

---

## What One Cycle Covers

The unit of this procedure is **one development step** — a piece of work whose expectations can be stated in one pass and whose enactment can then be checked: a function, a defect fix, a document section, a feature, a protocol contract, a piece of store equipment being designed. A larger development is decomposed into steps; each step runs the full cycle below. Scale changes how much the expectation states, never whether it is stated first ([tdd.md → Scope](./tdd.md#scope)).

## The Procedure

For each development step:

1. **Name the process being developed and its intent.** What entity or behavior is being advanced, for what end — who or what brings what in, what must come out, under which conditions, with which outcomes ([tdd.md → Whose Expectations Are Written](./tdd.md#whose-expectations-are-written); [tdd.md → A User Story Is a Developed Process's Expectations](./tdd.md#a-user-story-is-a-developed-processs-expectations)). A step whose developed process cannot be named is not ready for its expectations; discover that process first.

2. **Write the expectations, in checkable form, before the work.** Expected input, expected output, the conditions each applies under, and which outcomes count as which — of the *developed* process, not of the developers' procedure ([tdd.md → Whose Expectations Are Written](./tdd.md#whose-expectations-are-written)). Record them in the project's artifacts, not in conversation memory — tacit holding has exactly the two failures the concept document names: invisible to every participant other than its holder, and checkable by nothing ([Process → Expectations and Checks](../process.md#expectations-and-checks)). The artifact must pass the another-agent test ([tdd.md → Test Is Not Its Implementation](./tdd.md#test-is-not-its-implementation)).

3. **Choose the check's form by what the domain applies.** Where the developed process is software and the expectation can be executed by a machine, write the test code first — that is the ordinary realization, not an optional extra. Establish two facts before the work: that the expectation is genuinely checkable, and that it is not already satisfied — running the check before the work is the usual way to establish both; the obligation is the two facts, not the run ([tdd.md → What Memar Adopts](./tdd.md#what-memar-adopts)). Where it cannot be executed as code (a checkout counter's ergonomics, an organization's process, a document's acceptance), state the observation procedure that will check it: what is observed, by whom, against which stated condition ([tdd.md → Test Is Not Its Implementation](./tdd.md#test-is-not-its-implementation)).

4. **Enact the smallest increment that could satisfy the expectation.** The work is judged against the written expectation only. Enlarging the step's intent mid-flight is not enactment; it is a new expectation — return to step 2 and record it.

5. **Run the check and record the disposition.**
   - **Satisfied** — the step is done; the expectation artifact stays as the step's record.
   - **Not satisfied, expectation sound** — fix the work; re-run the check.
   - **Expectation itself wrong or incomplete** — revise the expectation *first*, as a recorded change, then continue. An expectation revised after the instance to match what was built, without the revision recorded, has silently converted the discipline into description ([Process → Expectations and Checks](../process.md#expectations-and-checks)).

## Where the Expectation Lives

Record the expectation wherever the owning project holds its artifacts — an executable test beside the code when the check is mechanical, a stated acceptance condition in the governing document when it is not, the user story where feature-scale requirements live. Whatever the placement, the artifact must pass the another-agent test stated in [tdd.md → Test Is Not Its Implementation](./tdd.md#test-is-not-its-implementation).

## Failure Modes

| Failure | Why it fails | Correction |
|---|---|---|
| Test written after the code, then called TDD | Post-hoc verification, not the discipline — the ordering cannot be recovered afterward | State the expectations first for the *next* step; retrofitting a check onto enacted work is verification, a different activity ([Process → Expectations and Checks](../process.md#expectations-and-checks)) |
| Red-green-refactor performed without written expectations | The cycle is one realization mechanism; without stated expectations there is nothing to check against | Return to step 2; the ritual is not the discipline ([tdd.md → What Memar Adopts](./tdd.md#what-memar-adopts)) |
| A narrated desire ("it should feel fast") standing as the expectation | Not checkable — no input, output, or condition stated | Force it into checkable form, or treat the work as inquiry (below), not development |
| Expectation silently edited to match the built instance | Converts the discipline into description; the check loses its subject | Expectation revisions are recorded changes, made before the next enactment |
| Test code treated as the source of truth over the model | A test contradicting the model tests the wrong process ([tdd.md → Relationship to Other Concepts](./tdd.md#relationship-to-other-concepts)) | Fix the model or the test at the concept layer; the written expectation follows the model |
| Non-executable expectations treated as exempt | The form of the check varies by domain; whether the ordering binds does not ([tdd.md → Scope](./tdd.md#scope)) | State the observation procedure (step 3) |
| Expectations stated for the developers' procedure instead of the developed process | Checks the wrong subject ([tdd.md → Whose Expectations Are Written](./tdd.md#whose-expectations-are-written)) | Return to step 1; name the process being developed |

## Boundary: When the Cycle Does Not Apply

The discipline binds planned processes whose expectations are decidable before enactment. Three boundary cases are named by the concept document; this practice carries them as routing, not re-argument:

- **The step is itself an inquiry** — a spike, an exploration, an investigation whose enactment is the means of discovery. State expectations *for the inquiry* (what evidence it must produce, what decision it must return, what record it must leave) and run the cycle on that; do not state expectations for answers nobody yet has. When the inquiry graduates into development, step 1 begins there. An inquiry whose course and outcome deserve a surviving record is recorded per the project's Research facet. The recurring instance is the reported defect: resolving one is an inquiry conducted per [Process → Defect Resolution as an Inquiry](../process.md#defect-resolution-as-an-inquiry), and only the fix it concludes with is a development step under this practice.
- **The work is already enacted** — checking it against newly written expectations is verification, valuable and legitimate, and a different activity. Do not present it as development conducted under the discipline.
- **The enactment is one-shot** — expectations are still written first; if the check cannot be re-run afterward, that limits the check's availability, not the ordering ([Process → Expectations and Checks](../process.md#expectations-and-checks)).

## Scaling

- **Function scale** — the expected input, output, and failure behavior stated as the test, written before the function.
- **Feature scale** — the user story read as the feature's written expectations ([tdd.md → A User Story Is a Developed Process's Expectations](./tdd.md#a-user-story-is-a-developed-processs-expectations)); its mechanically checkable subset is the executable realization of those expectations; the cycle runs per development step within the feature.
- **System scale** — the expected interfaces and contracts stated before the system is built ([tdd.md → What Memar Adopts](./tdd.md#what-memar-adopts)); in Memar's own production these are the protocol documents, and the framework's development is checked against them under the same rule it states.
