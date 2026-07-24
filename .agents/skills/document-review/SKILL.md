---
name: document-review
description: defines how documentation improvements are proposed
---

# Documentation Improvement Practice

> **Purpose:** This practice defines how documentation improvements are proposed and handled in the Memar project.  
> **Nature:** This is a *Practice* — a method commonly used for this type of work, not a claim about knowledge, skill, or capability.

---

## When to Apply This Practice
Apply this practice when:
- A discussion reveals ambiguity in existing documentation
- A decision is made that should be recorded
- A new understanding emerges that contradicts or extends docs
- The user requests documentation review
- A conversation reaches stable conclusions worth preserving

---

## Core Principles

### 1. Documentation Serves Understanding, Not Volume
**Goal:** Reduce ambiguity, not increase word count.

Before proposing any addition:
- What ambiguity does this resolve?
- What question does this answer that currently cannot be answered?
- Who will benefit, and when?

If you cannot answer these, the addition may not be needed.

### 2. Propose, Don't Modify (Without Approval)
Never modify project documentation unilaterally.

**Correct flow:**
1. Identify the ambiguity or gap
2. Draft the proposed text
3. Present to user with explanation
4. Wait for approval
5. Then apply (or user applies)

### 3. Definition Before Explanation
In documentation:

| Do | Don't |
|----|-------|
| Define terms before using them | Assume reader knows your terminology |
| State what something IS before explaining how it works | Jump into mechanics without grounding |
| Provide explicit definitions | Rely on intuitive understanding |

Every term that is central to a document should have an explicit definition in that document or a clearly referenced external definition.

### 4. Cross-Reference Relentlessly
Documentation does not exist in isolation.

When writing:
- What related documents exist?
- What terms are defined elsewhere?
- What decisions affect this content?
- What documents, models, or discussions provide context?

Provide explicit references. Do not make the reader search.

---

## Types of Documentation Improvements

### Type 1: Ambiguity Resolution
**Trigger:** Discussion reveals that existing text can be interpreted multiple ways.

**Proposal format:**
```markdown
## Proposed Clarification: [Document Name] - [Section]

### Current Text (ambiguous):
> [Quote the current text]

### Ambiguity Identified:
[Explain what can be misinterpreted and why it matters]

### Proposed Replacement:
> [New text that resolves the ambiguity]

### Rationale:
[Why this resolves it without introducing new problems]
```

---

### Type 2: Gap Filling
**Trigger:** Something is documented incompletely or not at all.

**Proposal format:**
```markdown
## Proposed Addition: [Document Name]

### Gap Identified:
[What's missing and why it matters]

### Context:
[Where this fits in existing documentation structure]

### Proposed Text:
> [The text to be added]

### Placement:
[Exact location - after which section, before which section]
```

---

### Type 3: Decision Recording

**Trigger:** A discussion concludes with a decision not yet captured.

**Proposal format:**
```markdown
## Proposed Decision Record: [Topic]

### Decision:
[What was decided]

### Context / Problem:
[What problem this decision addresses]

### Alternatives Considered:
[What other options were discussed and why they were not chosen]

### Reasoning:
[Why this option was selected]

### Implications:
[What this affects going forward]
```

---

### Type 4: Terminology Alignment

**Trigger:** Inconsistent use of terms across documents.

**Proposal format:**
```markdown
## Proposed Terminology Alignment

### Term: [Term Name]

### Current Usage (inconsistent):
| Document | Usage |
|----------|-------|
| Doc A | Meaning X |
| Doc B | Meaning Y (slightly different) |

### Proposed Standardized Definition:
> [Clear, precise definition]

### Documents Affected:
- [List all docs that should be updated]

### Proposed Changes:
| Document | Current | Proposed |
|----------|---------|----------|
| ... | ... | ... |
```

---

### Type 5: Structural Improvement

**Trigger:** Document organization hinders comprehension.

**Proposal format:**
```markdown
## Proposed Restructuring: [Document Name]

### Current Structure:
[Outline of current organization]

### Problems with Current Structure:
[Why it doesn't serve the reader well]

### Proposed Structure:
[New outline]

### Migration Plan:
[How to move from old to new without losing information]
```

---

## Reviewing Documentation for Issues

When reviewing documentation, systematically check for:

### Content Issues
- [ ] Undefined terms used without explanation
- [ ] Claims made without evidence or reasoning
- [ ] Contradictions within or across documents
- [ ] Outdated information (superseded by newer decisions)
- [ ] Missing context that would aid understanding

### Structural Issues
- [ ] Information buried in wrong section
- [ ] Related concepts scattered across distant sections
- [ ] No clear entry point for new readers
- [ ] Missing table of contents or navigation aids
- [ ] Circular references (A points to B, B points to A, neither defines)

### Terminology Issues
- [ ] Same term used for different meanings
- [ ] Different terms used for same meaning
- [ ] Industry terminology adopted without examination
- [ ] Terms defined differently in different places

---

## Quality Standards for Proposed Text

### Every proposal must be:

1. **Self-contained** — Understandable without reading the surrounding discussion
2. **Precise** — Each word chosen deliberately; no filler
3. **Defined** — All key terms defined or referenced
4. **Actionable** — Reader knows what to do with the information
5. **Referenced** — Connections to related content explicitly stated

### Proposal Anti-Patterns

| Anti-Pattern | Example | Instead |
|-------------|---------|---------|
| Vague improvement | "Make this clearer" | "Change X to Y because Z" |
| Overwriting | Replacing entire file for one fix | Targeted replacement of specific section |
| Assumption preservation | Keeping ambiguous text "just in case" | Resolve the ambiguity |
| Style-only change | Rewording without meaning change | Only change if meaning improves |
| Missing rationale | Proposing text without explanation | Always explain WHY |

---

## Language Conventions

| Artifact | Language | Format |
|----------|----------|--------|
| Proposed documentation text | English | Markdown-ready |
| Rationale/explanation | User's language or English | Plain text |
| Code examples | Per project standard | Code block |
| Comments within proposals | English | Inline |

---

## Output Format

When proposing documentation improvements:

```markdown
## Documentation Improvement Proposal
**Date:** [Date]
**Source Discussion:** [Brief reference to what triggered this]
**Documents Affected:** [List]

---

### Summary
[One paragraph overview of all changes proposed]

---

### Proposals

#### Proposal 1: [Title]
[Using appropriate format from Types above]

#### Proposal 2: [Title]
[etc.]

---

### Priority Assessment
| Proposal | Priority | Effort | Dependency |
|----------|----------|--------|------------|
| 1 | High/Medium/Low | Small/Medium/Large | None / Proposal X |

---

### Questions for Approver
[Any decisions the user needs to make before approval]
```

---

## Relation to Other Practices

| Practice | Connection |
|----------|-----------|
| Architectural Critique | Critique outcomes often require doc updates |
| Domain Modeling Review | Model reviews reveal doc gaps |
| Conversation Handoff | Handoff notes feed into doc improvements |

---

*This Practice is part of the Memar project collaboration framework. It should evolve as the project's documentation needs become clearer.*
