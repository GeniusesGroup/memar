---
name: thinking
description: defines how the thinking modes are exercised in Memar's work — chiefly critical evaluation of a proposal, model, or design
---

# Thinking Practice

> **Purpose:** This practice defines how the [Thinking](./thinking.md) modes are exercised in Memar's actual work, starting with the one whose procedure is most developed: critical evaluation. The concept, the modes, and the discourse norms live in [thinking.md](./thinking.md) — that document is assumed reading, and its rules are not restated here.

---

## Where Critique Sits

Thinking is a family of modes, and critical thinking is one of them — not all of it ([thinking.md → Modes of Thinking](./thinking.md#modes-of-thinking)). Two consequences govern this practice's scope:

1. **Critique is a component of writing, not a separate phase for evaluating finished things.** Documentation work exercises all the modes together: producing a document from scratch is creative, abstract, and structural work — and critical examination of one's own claims is one component of that writing, applied while drafting, not a ritual bolted on afterward. The same holds for modeling ([modeling.practice.md](./modeling.practice.md) owns that exercise). This practice covers critique when it is the *dominant* activity — an explicit evaluation of a proposal, model, or design.
2. **Do not let critique dominate an exchange.** An engagement that is all critique is as unhealthy as one with none: generative and structural work must keep producing the material critique evaluates. The discourse norms in [thinking.md → Discourse Norms](./thinking.md#discourse-norms-derived-from-this-model) govern the balance; this practice only sharpens the critical end of it.

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

Most surface-level critiques operate only on Layer 1. Valuable critique operates on Layers 3–5 — consistent with the discourse norm that terminology and definitions are evaluated differently: when terminology and definition conflict, the definition governs ([thinking.md → Discourse Norms](./thinking.md#discourse-norms-derived-from-this-model)).

---

## Procedure

1. **Understand before critiquing.** Restate the proposal in your own words; identify the problem it attempts to solve and the definitions it relies on; ask clarifying questions where ambiguous. **Do not critique what you have not understood** — and per the discourse norms, prefer a question to an assumption at exactly this step.
2. **Identify explicit and implicit assumptions.** For each: mark whether it is stated or unstated, assess its stability (strong evidence / weak / unexamined), and evaluate what follows if it is false. Common hidden assumptions worth checking: that industry terminology is correct; that the current implementation reflects the true domain structure; that the proposal's prerequisites exist; that existing boundaries are natural rather than accidental.
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

**Proportional strength rule:** the strength of required critique is proportional to the strength of the model being challenged.

| Model strength | Required critique strength |
|----------------|---------------------------|
| Casual suggestion | Observation of a potential issue |
| Well-reasoned proposal | Identified contradiction OR stronger alternative |
| Deeply-developed model | Fundamental flaw in assumptions OR significantly better explanatory power |
| Battle-tested architecture | Multiple lines of evidence + comprehensive alternative |

A superficial objection to a deeply-reasoned model is not merely unhelpful — it is noise that obscures genuine issues. (The norm's home is [thinking.md](./thinking.md#discourse-norms-derived-from-this-model); this table operationalizes it.)

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
| [thinking.md](./thinking.md) | Governing concept — the modes, the discourse norms, and the model this practice operationalizes |
| [modeling.practice.md](./modeling.practice.md) | Model discovery and review — critique of a model belongs to its review procedure; this practice covers proposals and designs generally |
| [documentation-handoff.practice.md](./documentation-handoff.practice.md) | Critique conclusions that outlive the session are captured in a handoff record |

---

*This Practice is part of the Memar project collaboration framework. It should evolve as the project's collaboration patterns become clearer.*
