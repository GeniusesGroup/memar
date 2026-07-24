---
name: architectural-critique
description: defines how architectural critique is performed
---

# Architectural Critique Practice
> **Purpose:** This practice defines how architectural critique is performed in the Memar project.  
> **Nature:** This is a *Practice* — a method commonly used for this type of work, not a claim about knowledge, skill, or capability.

---

## When to Apply This Practice
Apply architectural critique when:
- A new proposal, model, or design is presented
- An existing architecture is being evaluated
- A decision between alternatives must be made
- The user explicitly requests critique
- Hidden assumptions need to be uncovered

---

## Core Principles of Critique

### 1. Critique Targets Assumptions, Not Surfaces
**Ineffective critique:**
- "This terminology is non-standard"
- "Nobody does it this way"
- "The industry uses pattern X instead"

**Effective critique:**
- "This proposal assumes Y. Has that assumption been examined?"
- "If assumption Z were false, how would this model change?"
- "What definitions justify this classification?"

### 2. Examine the Conceptual Stack
When critiquing any proposal, examine each layer:

```
Layer 1: Terminology
    ↓ What words are being used?
Layer 2: Definitions  
    ↓ What do those words actually mean?
Layer 3: Assumptions
    ↓ What must be true for this to hold?
Layer 4: Consequences
    ↓ What follows if this is adopted?
Layer 5: Alternatives
    ↓ What other models explain the same phenomena?
```

Most surface-level critiques operate only on Layer 1 (terminology). Valuable critique operates on Layers 3-5.

---

## Critique Procedure

### Step 1: Understand Before Critiquing
Before offering any critique:
1. Restate the proposal in your own words
2. Identify what problem it attempts to solve
3. Identify what definitions it relies on
4. Ask clarifying questions if anything is ambiguous

**Do not critique what you have not understood.**

### Step 2: Identify Explicit and Implicit Assumptions
For each assumption found:
- Mark whether it is explicit (stated) or implicit (unstated)
- Assess its stability (strong evidence? weak? unexamined?)
- Evaluate consequences if it were false

**Common hidden assumptions to check:**
- That industry terminology is correct
- That current implementation reflects true domain structure
- That the proposed solution's prerequisites exist
- that "how" questions don't affect "what" answers
- That existing boundaries are natural rather than accidental

### Step 3: Check Internal Consistency
Verify:
- Definitions are used consistently throughout
- No term means two different things in different contexts
- Proposed relationships don't create circular dependencies
- The model doesn't contradict its own stated principles

### Step 4: Evaluate Explanatory Power
Compare the proposal against:
- The phenomenon it aims to explain/model
- Alternative explanations (if any)
- The existing model (if replacing)

Ask:
- Does this explain more than the alternative?
- Does it explain with fewer contradictions?
- Does it predict things that can be verified?

### Step 5: Assess Long-Term Implications
Consider:
- Evolvability: How easily can this change as understanding grows?
- Maintainability: How costly is it to reason about this later?
- Composability: Does this combine well with other parts of the model?
- Communicability: Can this be understood without the original author?

---

## Critique Quality Standards

### Minimum Viable Critique
A critique MUST include at least ONE of:
- ✅ A stronger explanation for the same observations
- ✅ Identification of a meaningful internal contradiction
- ✅ Demonstration that an assumption is false or unstable
- ✅ An alternative with clearly superior properties

### Insufficient Critique
A critique is INSUFFICIENT if it relies solely on:
- ❌ Terminology preference ("this isn't standard wording")
- ❌ Industry convention ("nobody does this")
- ❌ Authority appeal ("expert X says otherwise")
- ❌ Taste ("I don't like this structure")
- ❌ Implementation difficulty without architectural justification

### Proportional Strength Rule
> **The strength of required critique is proportional to the strength of the model being challenged.**

| Model Strength | Required Critique Strength |
|---------------|--------------------------|
| Casual suggestion | Observation of potential issue |
| Well-reasoned proposal | Identified contradiction OR stronger alternative |
| Deeply-developed model | Fundamental flaw in assumptions OR significantly better explanatory power |
| Battle-tested architecture | Multiple lines of evidence + comprehensive alternative |

A superficial objection to a deeply-reasoned model is not just unhelpful—it is actively harmful because it creates noise that obscures genuine issues.

---

## Output Format
When providing critique, structure it as:

```markdown
## Critique: [Subject]

### Understanding
[Restate what you understand the proposal to be]

### Assumptions Identified
| Assumption | Type | Stability | If False... |
|------------|------|-----------|-------------|
| ... | explicit/implicit | strong/weak/unexamined | ... |

### Observations
[What you found that merits attention]

### Questions / Concerns
[Genuine uncertainties or issues]

### Suggestions (if any)
[Only if you have a stronger alternative to offer]
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Description | Instead |
|-------------|-------------|---------|
| Terminology policing | Objecting to word choice while agreeing on meaning | Focus on definitions, not labels |
| Industry appeals | "Industry does X" | Explain WHY X is better, if it is |
| Yes-but agreement | Stating agreement then undermining | Either agree or critique honestly |
| Shotgun objection | Listing many weak objections | Find one strong one or none |
| Critique for show | Critiquing because it's expected | Critique only when you have value to add |

---

## Relation to Other Practices

| Practice | Connection |
|----------|-----------|
| Domain Modeling Review | Critique often reveals modeling issues |
| Documentation Improvement | Critique outcomes often require doc updates |
| Conversation Handoff | Critique conclusions should be captured in handoff notes |

---

*This Practice is part of the Memar project collaboration framework. It should evolve as the project's understanding deepens.*
