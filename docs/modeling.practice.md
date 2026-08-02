---
name: domain-modeling-review
description: defines how domain models (particularly graph models) are reviewed
---

# Domain Modeling Review Practice
> **Purpose:** This practice defines how domain models (particularly graph models) are reviewed in the Memar project.  
> **Nature:** This is a *Practice* — a method commonly used for this type of work, not a claim about knowledge, skill, or capability.

---

## When to Apply This Practice
Apply domain modeling review when:
- A new graph model or domain model is proposed
- An existing model is being refined or extended
- Model boundaries are being questioned
- Concept confusion is suspected
- The user requests model validation

---

## Core Modeling Distinctions

### Before reviewing any model, verify these distinctions are maintained:

#### 1. Concept vs. Data

| Concept | Data |
|---------|------|
| Has independent meaning | Derives meaning from context |
| Can be defined in isolation | Requires a concept to attach to |
| Exists in the domain | Is a property or attribute |
| "What something IS" | "What is known ABOUT it" |

**Test:** If you remove all properties/values, does the thing still exist as an understandable concept? If yes → Concept. If no → Data.

**Common error:** Modeling stored data as if it were a concept. Example: treating "email address" as a concept rather than data about a person/identity.

---

#### 2. Rule vs. Code

| Rule | Code |
|------|------|
| What MUST be true | How truth is enforced |
| Declarative statement | Imperative implementation |
| Part of domain understanding | Part of technical realization |
| Stable across implementations | Specific to language/platform |
| "A user cannot have duplicate emails" | `if (exists(email)) throw Error` |

**Test:** Can the constraint be stated clearly in business/domain language without reference to any programming concept? If yes → Rule. If the statement only makes sense in code → Code (and the rule may not have been extracted).

**Common error:** Embedding rules in code without explicit rule statements, making the rule invisible to anyone not reading implementation.

---

#### 3. Relationship vs. Entity

| Relationship | Entity (Concept) |
|-------------|-------------------|
| Exists BETWEEN things | Exists independently |
| Has no meaning without related concepts | Has meaning in isolation |
| Often modeled as edge | Often modeled as node |
| "User HAS orders" | "User", "Order" |

**Test:** Does this thing make sense as a complete sentence subject/object on its own? If it always requires "between X and Y" → Likely a relationship.

**Common error:** Modeling relationships as entities (reification) when they should remain as relationships. Or vice versa: treating genuine concepts as mere attributes.

---

## Review Procedure

### Step 1: Model Reading

Before critiquing:
1. Identify all nodes in the model
2. Identify all edges/relationships
3. Trace the model's "story" — what reality does it describe?
4. Note initial questions or confusions

**Output:** A neutral restatement of what the model appears to say.

### Step 2: Node Classification Audit

For each node, classify it as:

| Type | Indicator |
|------|-----------|
| **Pure Concept** | Independent meaning, definable alone |
| **Relationship masquerading as node** | Only meaningful between other things |
| **Rule masquerading as node** | Actually a constraint/behavior |
| **Data masquerading as node** | Actually a value/attribute |
| **Mixed** | Contains multiple types (warning sign) |

**Flag any node that is:**
- Unclassifiable → May indicate unclear thinking
- Mixed → Should probably be decomposed
- Misclassified → Incorrect modeling

### Step 3: Relationship Audit

For each relationship:
1. Is it genuinely a relationship (connects two concepts)?
2. Or is it actually a rule disguised as a relationship?
3. Is the cardinality correct and justified?
4. Is the direction meaningful?
5. Would the reverse direction also be valid?

**Watch for:**
- Missing relationships that should exist
- Relationships that encode rules (e.g., "validates" hiding a validation rule)
- Symmetric relationships forced into directional form (or vice versa)

### Step 4: Single Responsibility Check

Each concept/node should represent ONE coherent idea.

**Signs of mixed responsibility:**
- The node name uses "and" or "or"
- Different discussions about the node focus on different aspects
- Some relationships relate to one aspect, others to another aspect
- The definition requires multiple unrelated clauses

**Remedy:** Decompose into separate nodes with clear relationships between them.

### Step 5: Implementation Contamination Check

Verify that the model has NOT been contaminated by:

| Source | Contamination Sign |
|--------|------------------|
| Database | Tables become entities; normalization drives boundaries |
| UI | Screens become objects; display needs drive structure |
| API | JSON shapes dictate entity design |
| Framework | Class inheritance constraints appear in model |
| Language | Language features limit concept granularity |

**If contamination is found:** Identify which parts of the model reflect reality vs. which reflect implementation concerns.

### Step 6: Completeness Check

Ask:
- What questions can this model answer?
- What questions CANNOT it answer (but should)?
- Are there orphaned concepts (no relationships)?
- Are there implied but unstated relationships?

---

## Common Modeling Anti-Patterns

| Anti-Pattern | Description | Detection |
|-------------|-------------|-----------|
| **God Concept** | One node that means everything | Node connected to almost everything; vague definition |
| **Data as Concept** | Attributes promoted to entities | Node has no behavior/rules, just holds values |
| **Rule as Entity** | Constraints turned into things | Node that actually represents "must/should/cannot" |
| **Relationship Reification** | Edges turned into nodes unnecessarily | Node whose sole purpose is connecting two other nodes |
| **Implementation Mirror** | Model copies database/API/UI | Structure matches technical artifact too closely |
| **Terminology Drift** | Names don't match definitions | Definition of X actually describes Y |

---

## Output Format

When providing a model review, use this structure:

```markdown
## Model Review: [Model Name]

### 1. Understanding
[Your neutral restatement of the model]

### 2. Node Classification
| Node | Classification | Confidence | Notes |
|------|---------------|------------|-------|
| ... | Concept/Relationship/Rule/Data/Mixed | High/Medium/Low | ... |

### 3. Findings
#### Strengths
[What works well]

#### Concerns
| ID | Concern | Severity | Type |
|----|---------|----------|------|
| C1 | ... | Critical/High/Medium/Low | Classification/Contamination/Missing/etc. |

#### Questions for Clarification
[Things you need understood before proceeding]

### 4. Suggestions (if applicable)
[Only if you have concrete improvements]

### 5. Recommended Next Steps
[What should happen next]
```

---

## Severity Levels

| Severity | Meaning | Action |
|----------|---------|--------|
| **Critical** | Model is fundamentally misstructured | Must redesign before proceeding |
| **High** | Significant issues that will cause problems | Should fix before building on this |
| **Medium** | Notable issues but model is usable | Fix in next iteration |
| **Low** | Minor improvements possible | Address when convenient |
| **Observation** | Not necessarily an issue, worth noting | Keep in mind |

---

## Relation to Other Practices

| Practice | Connection |
|----------|-----------|
| Architectural Critique | Model review often reveals architectural assumptions |
| Documentation Improvement | Review outcomes should update project docs |
| Conversation Handoff | Review conclusions captured for continuity |

---

*This Practice is part of the Memar project collaboration framework. It should evolve as the project's modeling understanding deepens.*
