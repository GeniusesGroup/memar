---
name: cognition
description: defines how the thinking modes and their elementary operations are exercised in Memar's work — chiefly critical evaluation of a proposal, model, or design
---

# Cognition Practice

> **Purpose:** This practice defines how the thinking modes of [Cognition](./cognition.md) are exercised in Memar's actual work, starting with the one whose procedure is most developed: critical evaluation. The concept, the modes, the elementary operations and awareness disciplines beneath them, and the discourse norms live in [cognition.md](./cognition.md) — that document is assumed reading, and its rules are not restated here.

---

## Where Critique Sits

Thinking is a family of modes, and critical thinking is one of them — not all of it ([cognition.md → Modes of Thinking](./cognition.md#modes-of-thinking)). Two consequences govern this practice's scope:

1. **Critique is a component of writing, not a separate phase for evaluating finished things.** Documentation work exercises all the modes together: producing a document from scratch is creative, abstract, and structural work — and critical examination of one's own claims is one component of that writing, applied while drafting, not a ritual bolted on afterward. The same holds for modeling ([modeling.practice.md](./modeling.practice.md) owns that exercise). This practice covers critique when it is the *dominant* activity — an explicit evaluation of a proposal, model, or design.
2. **Do not let critique dominate an exchange.** An engagement that is all critique is as unhealthy as one with none: generative and structural work must keep producing the material critique evaluates. The discourse norms in [cognition.md → Discourse Norms](./cognition.md#discourse-norms-derived-from-this-model) govern the balance; this practice only sharpens the critical end of it.

---

## Norm Application Points

The discourse norms in [cognition.md → Discourse Norms](./cognition.md#discourse-norms-derived-from-this-model) bind at intake, not only mid-reasoning. Checkpoints:

- **Before assuming intent or scope:** ask ([Ask rather than assume](./cognition.md#discourse-norms-derived-from-this-model)).
- **When the medium language differs from the system's strongest working representation:** transform for thinking; ask on translation ambiguity; return in counterpart-usable form ([Operate in the system's strongest working representation](./cognition.md#what-implementation-asymmetry-obliges)).
- **Before a change that reaches beyond the instance:** propose the content and the file list; obtain confirmation ([Confirm before large-scope changes](./cognition.md#discourse-norms-derived-from-this-model)).
- **Before building on a load-bearing term:** verify its governing definition, or report that it is unverified ([Definitions outrank terminology](./cognition.md#discourse-norms-derived-from-this-model)).
- **When required material is missing:** report absence; do not fabricate ([Report absence rather than supplying it](./cognition.md#discourse-norms-derived-from-this-model)).
- **When a shared artifact conflicts with stronger evidence:** report the conflict; do not silently propagate or silently override ([Treat shared artifacts as claims](./cognition.md#discourse-norms-derived-from-this-model)).
- **When conceptual depth is high and other cognitive systems are available:** consult them before settling ([Consult other cognitive systems](./cognition.md#discourse-norms-derived-from-this-model)).
- **When generalizing a received criticism:** keep reported / inferred / confirmed distinct; label the inferred root as the receiver's extension until the giver confirms ([conceptual-root with provenance](./cognition.md#discourse-norms-derived-from-this-model)).

Procedure detail for confirm-before-large-scope and for conceptual-root questioning lives here as practice; the norms themselves stay in the base document.

---

## Working With the Operations Layer

A mode's Runs-on clause ([cognition.md → Elementary Operations and Awareness Disciplines](./cognition.md#elementary-operations-and-awareness-disciplines)) tells you which operations the mode exercises — use it when the mode's *name* is not enough to decide what to actually do. Per the base document's use threshold: begin from the material's lack, not from mode-label matching.

- **When you cannot tell which mode a task needs, work at the operation level.** Ask what the material lacks — a whole un-examined (decompose), alternatives un-weighed (compare and apply criteria), a field never closed (commit), a model no one has tested against instances (instantiate) — and run the operation the lack names. The mode follows.
- **When a critique must name its strongest move, name the operation.** "I compared the two framings and X persists across both" is a stronger critique statement than "this feels critical" — the operation makes the critique checkable.
- **When drifting, switch to the discipline level.** Awareness of goal is the standing remedy for exploration that has become wandering; awareness of assumptions is the standing remedy for reasoning that has silently committed to its premises. Disciplines do not produce material — they re-govern the operations that do.

---

## Named-Error Checks

Knowing that an argument has slipped is part of doing the work, not an optional refinement ([cognition.md → Named Errors](./cognition.md#named-errors-biases-and-fallacies)). The body document owns the two error classes; this practice carries the checks an exercise runs against them:

- **Sender-side, before issuing material:** re-read the claim for the bias signatures the operations layer names — discrepancy noticing that only confirms (confirmation bias), ordering pinned to the first input (anchoring), comparison over a surviving-only sample (survivorship bias), criterion application that substitutes the counterpart's framing for independent evaluation (source-deference / agreement pressure). One named check per issued claim is the minimum; the discipline that carries it is awareness of assumptions.
- **Receiver-side, on receiving material:** check for defective inferential support — support that comes from the source rather than the claim (ad hominem, appeal to authority), a position replaced by a weaker one (straw man), popularity standing in for evidence (industry convention; the practice's insufficient-critique list below is this check in Memar vocabulary). Fallacies are structural: the support offered does not support, whether the pattern arose in solitary reasoning or in transit.
- **Both sides, on both paths:** the Persian phrase that names the shared property is به غلط — both classes derail the path of thinking and of dialogue alike, so a check that passes sender-side can still fail transit, and material that arrives clean can still corrupt the receiver's own operations. Run the check on both paths, not only the one you occupy.
- The checklists are deliberately short. Enumerating individual biases and fallacies is catalog work — grow the list per project, from named errors actually observed in that project's material, not from a generic catalog imported wholesale.

---

## When to Critique

Apply this practice when:

- a new proposal, model, or design is presented
- an existing architecture is being evaluated
- a decision between alternatives must be made
- a participant explicitly requests critique
- hidden assumptions need to be uncovered

---

## The Conceptual Stack

Every proposal has layers, and the value of a critique depends on how deep it operates:

```
Layer 1: Terminology    — what words are being used?
Layer 2: Definitions    — what do those words actually mean?
Layer 3: Assumptions    — what must be true for this to hold?
Layer 4: Consequences   — what follows if this is adopted?
Layer 5: Alternatives   — what else explains the same phenomena?
```

Most surface-level critiques operate only on Layer 1. Valuable critique operates on Layers 3–5 — consistent with the discourse norm that terminology and definitions are evaluated differently: when terminology and definition conflict, the definition governs ([cognition.md → Discourse Norms](./cognition.md#discourse-norms-derived-from-this-model)).

---

## Procedure

1. **Understand before critiquing.** Restate the proposal in your own words; identify the problem it attempts to solve and the definitions it relies on; ask clarifying questions where ambiguous. **Do not critique what you have not understood** — and per the discourse norms, prefer a question to an assumption at exactly this step. When the subject arrived as a criticism of something else, keep three statuses distinct before you act: what was *reported*, what root you *inferred* (your extension until confirmed), and what generalization the giver *confirmed*.
2. **Identify explicit and implicit assumptions.** For each: mark whether it is stated or unstated, assess its stability from inspectable material (strong evidence / weak / unexamined), and evaluate what follows if it is false. Common hidden assumptions worth checking: that industry terminology is correct; that the current implementation reflects the true domain structure; that the proposal's prerequisites exist; that existing boundaries are natural rather than accidental.
3. **Check internal consistency.** Definitions used consistently throughout; no term carrying two meanings in different contexts; no circular dependencies among proposed relationships; no contradiction of the model's own stated principles.
4. **Evaluate explanatory power.** Compare against the phenomenon it models, alternative explanations, and the existing model it would replace: does it explain more? With fewer contradictions? Does it predict anything verifiable?
5. **Assess long-term implications.** Evolvability (how easily can it change as understanding grows), maintainability (how costly to reason about later), composability (does it combine with the rest of the model), communicability (can it be understood without the original author).

---

## Quality Standards

**A critique must include at least one of:**

- a stronger explanation for the same observations
- identification of a meaningful internal contradiction
- demonstration that an assumption is false or unstable
- an alternative with clearly superior properties

**A critique relying solely on the following is insufficient:**

- terminology preference ("this isn't standard wording")
- industry convention ("nobody does this")
- authority appeal ("expert X says otherwise")
- taste ("I don't like this structure")
- implementation difficulty without architectural justification

**Proportional strength rule:** the strength of required critique is proportional to the strength of the model being challenged. Judge model strength from inspectable material — stated assumptions, evidence, alternatives considered, tests, consequences — not from author status or presumed hidden reasoning. Proportionality raises required critique *quality*; it never licenses withholding a critique that meets that quality.

| Model strength (inspectable) | Required critique strength |
|---------------------------|---------------------------|
| Casual suggestion | Observation of a potential issue |
| Well-reasoned proposal | Identified contradiction OR stronger alternative |
| Deeply-developed model | Fundamental flaw in assumptions OR significantly better explanatory power |
| Battle-tested architecture | Multiple lines of evidence + comprehensive alternative |

A superficial objection to a deeply-reasoned model is not merely unhelpful — it is noise that obscures genuine issues. Silence before mature-looking prose, when a quality critique exists, is the opposite failure. (The norm's home is [cognition.md](./cognition.md#discourse-norms-derived-from-this-model); this table operationalizes it.)

---

## Output Format

When critique is the session's deliverable, structure it as:

```markdown
## Critique: [Subject]

### Understanding
[Restate what you understand the proposal to be — the reader must be able to
verify you critiqued the actual proposal, not a misreading of it]

### Assumptions Identified
| Assumption | Type | Stability | If false... |
|------------|------|-----------|-------------|

### Observations
[What you found that merits attention]

### Questions / Concerns
[Genuine uncertainties or issues]

### Suggestions (if any)
[Only if you have a stronger alternative to offer]
```

---

## Anti-Patterns

| Anti-Pattern | Description | Instead |
|-------------|-------------|---------|
| Terminology policing | Objecting to word choice while agreeing on meaning | Focus on definitions, not labels |
| Industry appeals | "Industry does X" | Explain *why* X is better, if it is |
| Yes-but agreement | Stating agreement then undermining it | Either agree or critique, honestly |
| Shotgun objection | Listing many weak objections | Find one strong one, or none |
| Critique for show | Critiquing because it is expected | Critique only when you have value to add |

---

## Relation to Other Artifacts

| Artifact | Connection |
|----------|-----------|
| [cognition.md](./cognition.md) | Governing concept — the cognition frame, the thinking modes, the elementary operations and awareness disciplines, the named-error classes, and the discourse norms this practice operationalizes |
| [modeling.practice.md](./modeling.practice.md) | Model discovery and review — critique of a model belongs to its review procedure; this practice covers proposals and designs generally |
| [documentation-handoff.practice.md](./documentation-handoff.practice.md) | Critique conclusions that outlive the session are captured in a handoff record |

---

*This Practice is part of the Memar project collaboration framework. It should evolve as the project's collaboration patterns become clearer.*
