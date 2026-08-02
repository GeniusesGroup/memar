---
name: conversation-handoff
description: defines how context is preserved between conversations
---

# Conversation Handoff Practice

> **Purpose:** This practice defines how context is preserved between conversations in the Memar project.  
> **Nature:** This is a *Practice* — a method commonly used for this type of work, not a claim about knowledge, skill, or capability.

---

## Why This Practice Exists

Conversations in the Memar project often span multiple sessions. A topic may be introduced, partially explored, set aside, and resumed days or weeks later.

**Without handoff notes:**
- Context is lost or misremembered
- Previous decisions are revisited unnecessarily
- Resolved ambiguities resurface
- The user must re-explain background

**With handoff notes:**
- Each new conversation can begin from stable ground
- Progress is cumulative, not cyclical
- Both parties share understanding of current state

---

## When to Create Handoff Notes

Create a Conversation Note when:
- A substantive discussion reaches a natural pause point
- The user indicates they will continue in a new conversation
- Significant decisions or resolutions have been reached
- Complex topics with many nuances have been explored
- The user explicitly requests a summary note

**Do NOT create handoff notes when:**
- The exchange was trivial (simple Q&A, quick factual answer)
- Nothing was decided or resolved
- No continuation is anticipated

---

## Anatomy of a Conversation Note

### Required Sections

```markdown
# Conversation Note: [Topic]

**Created:** [Date]  
**Source Chat:** [Brief identifier or description]  
**Status:** [Active / Paused / Complete / Blocked]

---

## 1. Topic & Purpose
[What was being discussed and why]

---

## 2. Decisions Made
| Decision | Reasoning | Confidence |
|----------|-----------|------------|
| [What was decided] | [Why] | High / Medium / Low / Tentative |

---

## 3. Ambiguities Resolved
| Issue | Previous Confusion | Resolution | How Resolved |
|-------|-------------------|------------|--------------|
| [What was unclear] | [What the confusion was] | [What's now clear] | [What evidence/argument clarified it] |

---

## 4. Open Questions
| Question | Why It Matters | Blocking? | Suggested Path |
|----------|---------------|-----------|----------------|
| [What remains unknown] | [Why it matters] | Yes / No | [How to find out] |

---

## 5. Assumptions Identified
| Assumption | Stability | If Wrong, Then... |
|------------|-----------|------------------|
| [What we're assuming] | Strong / Weak / Unexamined | [What would change] |

---

## 6. Key Definitions Established
| Term | Definition Agreed | Status |
|------|-------------------|--------|
| [Term] | [Definition] | New / Refined / Confirmed |

---

## 7. Proposed Next Steps
| Step | Dependency | Priority |
|------|-----------|----------|
| [What to do next] | [What depends on what] | High / Medium / Low |

---

## 8. Related Artifacts
| Artifact | Relation | Action Needed |
|----------|----------|---------------|
| [Doc/Model/RFC name] | [How it relates] | [None / Update / Review / Create] |

---

## 9. Notes & Observations
[Anything that doesn't fit above but may be useful later]
```

### Optional Sections (add when relevant)

```markdown
## 10. Terminology Notes
[Industry terms that were discussed, rejected, or redefined]

## 11. Rejected Alternatives
| Alternative | Why Rejected |
|-------------|-------------|
| [Option not chosen] | [Reason] |

## 12. User Preferences Observed
[Style, terminology, or approach preferences that emerged]
```

---

## Quality Standards

### A Good Conversation Note Is:

1. **Complete** — Captures all decisions, resolutions, and open items
2. **Precise** — Specific enough to be useful without re-reading the chat
3. **Self-contained** — Understandable by someone who didn't participate
4. **Actionable** — Clear next steps with dependencies
5. **Honest about uncertainty** — Distinguishes firm conclusions from tentative ones

### A Poor Conversation Note:

1. **Too brief** — "We discussed X" (but no outcomes recorded)
2. **Too verbose** — Full transcript rather than distilled essence
3. **Opinionated** — Reflects one side's view rather than shared understanding
4. **Vague** — "Some concerns were raised" (which concerns? by whom?)
5. **Overconfident** — Presents tentative conclusions as final decisions

---

## Writing Guidelines

### Be Specific

❌ "We talked about modeling approaches"
✅ "Decided: Graph-oriented modeling will be primary method; reason: better reveals relationships than table-based approaches"

### Distinguish Confidence Levels

Use explicit confidence markers:
- **Decided:** Firm conclusion, unlikely to revisit unless new evidence
- **Tentative:** Current direction, open to revision
- **Explored but unresolved:** No conclusion reached yet
- **Deferred:** Deliberately postponed, not forgotten

### Preserve Nuance

If a decision had dissenting considerations, record them:

> **Decision:** Use graph modeling as primary method.
> 
> **Considered alternative:** Table/entity modeling. Rejected because: conceals relationships behind foreign keys. However, this alternative may still be useful for implementation-level documentation.

This prevents future re-litigation of settled issues while preserving the reasoning.

### Record the "Why"

A decision without reasoning cannot be evaluated or revised later.

For each decision, capture:
- What options existed
- What criteria were used
- What tipped the balance

---

## Using Handoff Notes

### For the User (Starting a New Conversation)

When beginning a related conversation:
1. Identify the relevant previous Conversation Note(s)
2. Provide it at the start of the new chat
3. Specify what aspect you want to continue
4. Note any new information since the last conversation

Example opening:
> "Here's the conversation note from our discussion about [topic]. I want to continue exploring [specific aspect]. Since then, I've been thinking about [new thought]..."

### For the AI (Receiving a Handoff Note)

When receiving a Conversation Note:
1. Read completely before responding
2. Acknowledge key decisions and current state
3. Do not re-argue settled points unless asked
4. Pick up from where the previous conversation left off
5. Update the note if the new conversation changes anything

---

## File Naming & Storage

### Convention

```
conversation-notes/
├── 2024-01-15-topic-name.md
├── 2024-01-22-another-topic.md
└── 2024-02-10-third-topic.md
```

- Date in ISO format (YYYY-MM-DD)
- Topic name in kebab-case
- One topic per file (split multi-topic conversations)

### Metadata Header

Each file should begin with:

```markdown
---
topic: [Topic Name]
created: [YYYY-MM-DD]
status: [active/paused/complete/blocked]
related-topics: [list of related note files if any]
---
```

---

## Example

```markdown
---
topic: aggregate-boundary-definition
created: 2024-01-15
status: active
related-topics: []
---

# Conversation Note: Aggregate Boundary Definition

## 1. Topic & Purpose
Defining what constitutes an aggregate boundary in Memar's domain model, specifically whether boundaries are intrinsic properties or emergent from rules.

## 2. Decisions Made
| Decision | Reasoning | Confidence |
|----------|-----------|------------|
| Aggregate boundaries are NOT intrinsic types | Boundaries emerge from consistency rules, not from classification | Tentative - needs RFC |
| Term "Aggregate Root" should be avoided | Carries DDD baggage that doesn't match our definition | Decided |

## 3. Ambiguities Resolved
| Issue | Resolution |
|-------|-----------|
| Whether boundary = type | No, boundary is a constraint relationship, not a classification |

## 4. Open Questions
| Question | Priority |
|----------|----------|
| How do we formally specify consistency rules? | High |
| Should boundaries be mutable over time? | Medium |

## 5. Next Steps
1. Draft RFC for boundary-as-constraint model
2. Review existing DDD literature for useful concepts (without adopting terminology)
3. Create concrete examples testing the model
```

---

## Relation to Other Practices

| Practice | Connection |
|----------|-----------|
| Documentation Improvement | Handoff notes often reveal doc gaps needing updates |
| Architectural Critique | Critique outcomes should be captured in handoff notes |
| Domain Modeling Review | Model review conclusions feed into handoff records |

---

*This Practice is part of the Memar project collaboration framework. It should evolve as the project's collaboration patterns become clearer.*
