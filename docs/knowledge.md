---
Title: "Knowledge"
Status: Draft
Start Date: 2026-07-20
ID: 510421
---

# Knowledge
This document defines what knowledge is, how it differs from its representations, and what a system must do to preserve, retrieve, and evolve it. The organizational discipline of managing knowledge as a practice — creation workflows, tacit-to-explicit conversion, sector adoption, and change management — belongs to the Organization project; this document owns the concept and its modeling consequences.

## Abstract
Knowledge is not its documents: a document is a frozen projection of knowledge for a purpose, and a system that stores documents while losing the context, relationships, and rationale that made them meaningful has lost knowledge while keeping its artifacts intact. This document establishes a precise vocabulary (Data → Information → Knowledge → Document), positions knowledge in Memar's purpose chain — knowledge is the material thinking operates on, and a reliable model built from it is what intelligent agency acts through — and derives nine principles for modeling knowledge in any system: storage model is not content model; identity independent of location; relationships as first-class citizens; UI projection is not the domain model; task-centric evolution; explicit context recovery; classification beyond a single hierarchy; communication channels as producers, not repositories, of knowledge; and knowledge units finer than documents. The principles are domain-independent and intentionally principle-level; implementation belongs to domain-specific projects.

## Introduction

### Motivation
Organizations across every domain continuously default to document-centric tools and hierarchical storage paradigms, forcing multidimensional knowledge into rigid structures. The friction observed in tracking historical context, linking related concepts, discovering information, and recovering decision rationale suggests that the underlying storage abstraction is fundamentally mismatched with knowledge modeling needs.

The pattern recurs regardless of domain:

| Software Development | Healthcare | Education | Manufacturing | Legal |
|---------------------|------------|-----------|---------------|-------|
| Why was this architecture chosen? | Why was this treatment selected? | Why was this curriculum designed? | Why does this process parameter exist? | Why was this legal strategy pursued? |
| Who has expertise in module X? | Who has experience with condition Y? | Who teaches subject Z effectively? | Who knows how to fix machine M? | Which attorney handled a similar matter? |
| Where is the decision documented? | Where is the protocol archived? | Where are the learning outcomes defined? | Where is the SOP stored? | Where is the precedent recorded? |

A hospital losing a care protocol because a retiring nurse "took the procedure in her head" is structurally identical to a software company losing architectural rationale because the lead developer left and only the code remains. These are not domain-specific problems; they are manifestations of a single failure — treating the representation as the thing represented.

Within Memar specifically, the immediate trigger was a series of architectural discussions about whether File and Directory should remain first-class primitives for modeling knowledge in modern systems (see [Reevaluating the Filesystem](./protocols/filesystem.md)). Those discussions revealed deeper questions:

- Why do organizations produce vast amounts of data but cannot retrieve knowledge when needed?
- Why does every team eventually build its own wiki structure, only to abandon it?
- Why do decisions made six months ago become irrecoverable, even though the decision was "documented"?
- Why does Git — designed for source code version control — become the de facto knowledge repository for things that have nothing to do with code?

### Problem
Stated from the perspective of the people and systems that depend on knowledge, systems that claim to "manage knowledge" universally suffer from:

1. **Knowledge loss through personnel transition**: when experts leave, their tacit knowledge leaves with them.
2. **Knowledge fragmentation across silos**: information exists in isolated repositories — departmental drives, email threads, chat histories, paper files — without unified discoverability or relational context.
3. **Document-knowledge conflation**: stored documents are mistaken for managed knowledge. A policy manual is not the same as understanding why the policy exists, what alternatives were considered, and under what conditions it should change.
4. **Context decay over time**: artifacts created with rich context (decisions, designs, protocols) become orphaned from the discussions, rationales, and assumptions that gave them meaning.
5. **Classification rigidity**: hierarchical storage models force artificial single-category membership on inherently multi-dimensional knowledge.
6. **Communication-knowledge confusion**: transient communication channels (email, chat, meetings, handoffs) produce knowledge but fail to preserve it structurally.

### Methodology
This analysis synthesizes four sources: academic research on knowledge organization and retrieval (semantic filesystems, documentation usefulness, organizational knowledge creation); multi-session architectural dialogues examining File, Directory, Git, Repository, Content, Task, and their relationships; historical analysis of how computing abstractions evolved from physical constraints (block devices, limited memory, single-user systems) into assumed truths about knowledge organization; and cross-domain observation — healthcare, education, manufacturing, legal, and small enterprises — which supplies the evidence that the underlying failures, and therefore the principles addressing them, are domain-independent. Unresolved questions are kept genuinely open to drive future specifications.

## Explanation

### Definition

**Data**: raw symbols, bytes, characters without interpreted meaning.
```
42
"customer"
0x1a2b3c
98.6°F
```

**Information**: data with context, structure, and interpretive meaning.
```
Customer ID: 42 refers to Omid Hekayati, registered 2024-01-15
Patient temperature: 98.6°F recorded at 14:30 by Nurse Sarah
```

**Knowledge**: information integrated with experience, context, relationships, and actionable understanding.
```
Customer #42 (Omid) prefers email communication on Tuesday mornings because his team
stands up on Wednesdays and he prepares talking points overnight. This preference
emerged from a pattern observed across 17 interactions and was confirmed in Q3 planning.

Patient Mrs. Rodriguez consistently reports lower pain scores when assessed by Nurse
Sarah — likely due to Sarah's longer assessment conversations. This observation should
inform care assignment decisions.
```

**Document**: a frozen representation of knowledge at a specific boundary, for specific purposes.
```
document-510420: "Communication Preferences Specification"
Hospital Protocol #114: "Pain Assessment Guidelines"
Legal Precedent Brief: Smith v. Jones (2024)
```

**Critical implication**: a document is a **projection** of knowledge, not knowledge itself. When we store documents, we store representations. When we lose the surrounding context — why this was written, what alternatives were rejected, who disagreed — we lose knowledge even if the document remains intact. Most organizational "knowledge management" systems actually manage documents and mistake the map for the territory.

This hierarchy holds whether the domain is software development, healthcare, education, law, or manufacturing. The examples differ; the structural relationships do not.

The foundational one-line definition used across Memar is given in [System → Knowledge and Science](./system.md#knowledge-and-science): knowledge is a justified, structured understanding of a domain, acquired through observation, reasoning, experimentation, or critical discourse, that enables reliable prediction, explanation, or action within that domain. This document is the detailed treatment of that concept — what the understanding is made of, how it relates to its representations, and what systems must do to preserve it.

#### Discussion

##### Rationale and alternatives
- **Define knowledge as a static asset (rejected)**: the research literature on organizational knowledge creation (Nonaka & Takeuchi's SECI model) established knowledge as a dynamic, social process rather than a stock of artifacts. The modeling principles below follow that reading — knowledge exists in the living relationships between assertions, evidence, tasks, and participants, not in the files that freeze them. The organizational application of that process view is developed in the Organization project.
- **Leave "knowledge" undefined and regulate only storage behavior (rejected)**: management rules stated over an undefined central term import the reader's colloquial sense. Memar's terminology governance ([Terminology → Terminology Authority and Governance](./terminology.md#terminology-authority-and-governance)) requires defining a load-bearing term once, here, and letting other documents reference that definition.

### Knowledge in Memar's Concept Web
Knowledge is one link in the chain Memar exists to serve:

```text
Knowledge ──material──► Thinking ──quality──► Intelligence ──exercised──► Agency ──directed──► Goals
(this document)         (thinking.md)          (framework.md)             (agency.md)
```

- **Knowledge** is what understanding is made of and how it survives — the subject of this document.
- **Thinking** is the activity that manipulates representations toward some end ([Thinking](./thinking.md)); knowledge is both its material and its product.
- **Intelligence** is the quality of that activity: building a reliable model of reality from partial and ambiguous evidence, and revising it with new evidence. Memar states it as a goal in [Framework → Memar's Purpose Space](./framework.md#memars-purpose-space-from-knowledge-to-agency), not as an independent concept with its own document, because it is an output relation of knowledge, thinking, and agency — defining it separately would restate them.
- **Agency** is acting on the model toward objectives ([Agency](./agency.md)); an Agent's effective agency depends on the knowledge available to it, and knowledge that exists only inside individual Agents is a failure of collective agency, not merely of filing.
- **Goals** — ultimately the quality of life of the systems and people involved — are what the whole chain serves.

**Scope boundary.** This document owns the concept of knowledge and the modeling principles below. It does not own: the activity of thinking ([Thinking](./thinking.md)); the structure of acting systems ([Agency](./agency.md)); the domain model of Content, Relation, and Timeline ([Content](./content.md), [Modeling](./modeling.md)); or knowledge management as an organizational discipline — creation workflows, tacit-to-explicit conversion practice, sector adoption patterns, and change management — which belongs to the Organization project.

### Principles for Modeling Knowledge
The principles below describe what a system must do if it is to treat knowledge as what it is. They are principle-level and domain-independent: they prescribe no storage technology, no schema, and no workflow, all of which belong to implementing projects.

#### Storage Model ≠ Content Model
One of the most pervasive errors in system design is conflating *how* something is stored with *what* it means:

```text
Storage Engine Concerns:                  Content Model Concerns:
├── Persistence (bytes survive power loss)    ├── Semantics (what does this mean?)
├── Addressing (find the bytes later)         ├── Relationships (how does it connect?)
├── Allocation (fit N bytes on media)         ├── Provenance (who, why, based on what?)
├── Access Control (who may read/write)       ├── Evolution (how has this changed?)
└── Integrity (detect corruption)             └── Context (what assumptions does it depend on?)
```

The filesystem was designed to address the left column in an era of scarce resources. It was never designed for the right column. A **storage leakage** then occurred: physical storage constraints dictated mental models. Instead of a knowledge model dictating its storage projection, block-device constraints defined how we structure thought (Directories). The same leakage recurs in every domain where a filing convention becomes a thinking convention: patient folders, course files, case files, and part-number hierarchies all answer storage-engine questions and are then mistaken for answers to content-model questions.

**Principle statement**: Any system where the content model inherits structure from the storage engine will eventually fail at knowledge management. The two models must be independently designable, with storage as one possible projection of content.

#### Identity Must Be Independent of Location
The stable identifier of a knowledge artifact must be derived from its content (or assigned immutably at creation), never from its storage location. Location may change; identity must not.

Git's most important contribution to software development was not Branch, Merge, or distributed development. It was **Content Addressability**:

```text
Location-based identity (problematic):        Content-based identity (stable):
"The file at /src/customer/model.go"          "The object whose SHA is a3f2b1c..."
"The patient record in Cabinet 3, Folder 7"   "Patient Record #PR-2024-08921"
"The contract in Room 402, Drawer B"          "Matter #M-4521 (Smith v. Jones)"
```

The knowledge-management consequences are profound:

- **Location-based identity**: moving a file changes its identity. Renaming a directory breaks all references. Reorganizing a project destroys provenance.
- **Content-based identity**: content is what it is regardless of where it is stored. References survive reorganization. Provenance is inherent.

A legal citation references the decision itself, not the database holding it; a curriculum standard should keep its identity as it migrates between repositories; a manufacturing process step's identity is intrinsic to the process definition, not its position in a documentation hierarchy.

**Principle statement**: In any knowledge system, the stable identifier of a knowledge artifact must be derived from its content (or assigned immutably at creation), never from its storage location. Location may change; identity must not.

#### Relationships Are First-Class Citizens
Traditional hierarchical systems model exactly one relationship — **containment** (`parent → child`) — and force that single relationship type to represent all semantic connections:

```text
"document-A is inside /architecture/"   → containment (physical)
"Task-B is related to document-A"       → ??? (must use tags, symlinks, or conventions)
"Decision-C informed both"              → ??? (no native representation)
"Symptom-C contraindicates Protocol-A"  → ??? (no native representation)
```

The ecosystem's response reveals the inadequacy: symlinks, tags, labels, bookmarks, cross-references, search indexes — each an attempt to escape the single-relationship prison.

Relationship types that should be natively supported (at minimum):

| Relationship Type | Definition | Example (Software) | Example (Healthcare) | Example (Legal) |
|-------------------|------------|---------------------|----------------------|-----------------|
| **Containment** | A is physically/compositionally part of B | File in directory | Lab result in patient record | Document in matter file |
| **Reference** | A cites or points to B | Code imports library | Guideline cites research study | Brief cites precedent |
| **Dependency** | A requires B to exist/be valid | Module depends on API | Prescription requires diagnosis | Claim requires standing |
| **Sequence** | A precedes B temporally or logically | Build step before deploy | Diagnosis before treatment | Filing before discovery |
| **Specialization** | A is a more specific form of B | Subclass extends class | Pediatric cardiology ⊂ Cardiology | Criminal law ⊂ Law |
| **Association** | A is related to B (general-purpose) | Related issue link | Symptom associated with condition | Witness associated with testimony |
| **Attribution** | A was created/modified/approved by B | Commit authorship | Protocol approved by Medical Board | Brief authored by Partner X |
| **Opposition** | A contrasts with or negates B | Deprecated alternative | Treatment contraindicated for condition | Argument counters precedent |

**Principle statement**: A knowledge model must support multiple, explicit, typed relationships as first-class citizens. Containment is one useful relationship among many, not the privileged default.

#### UI Projection ≠ Domain Model
What users see varies by domain — files and folders, patient charts, student portfolios, case dockets, work orders — but what those views represent is universal: content nodes with types, context/grouping nodes, task nodes with state transitions, content-plus-relation structures. These are not the same. Conflating them leads to systems where the UI becomes the domain model — and when the UI needs to change (which it always does), the domain model must change too, breaking all existing data and integrations.

- You can build a GitHub-like interface on top of a graph-based knowledge model.
- You can build a wiki-like interface on the same model.
- You can build a conversation-like interface on the same model.
- You should be able to add a new interface without changing the model.
- If adding a feature requires changing your data schema, your UI has leaked into your model.

The clinician's rapid-entry screen and the researcher's cohort-analysis tool project the same patient-data model differently; the student's gradebook and the instructor's curriculum map project the same course-content model differently. The file explorer is a valid projection; treating that projection as the source of truth about knowledge structure is the error.

**Principle statement**: The user-visible interface (GUI, CLI, API surface, physical form) is a **projection** of the domain model, optimized for specific interaction patterns. Multiple projections can coexist on the same model. No projection should constrain the model's expressive power.

#### Task-Centric Knowledge Evolution
Most version control and document systems model history around **snapshots**: `Commit = state of all files at time T`; `Document Version = state of document at save point T`. But organizational knowledge rarely evolves around snapshots. It evolves around **tasks and decisions**:

```text
Task / Decision Unit
├── Question / Problem Statement
├── Discussion (multi-participant, temporal)
├── Research / Evidence Gathered
├── Alternatives Considered
├── Decision (with rationale)
├── Outcomes (what changed as a result)
└── Related Content (what documents were affected)
```

When someone asks "Why does this code look like this?" six months later, the answer is almost never in the commit snapshot. It is in the task discussion, the decision rationale, the rejected alternatives. The same holds for the treatment chosen after a tumor board, the curriculum revised after a failed term, the legal strategy recorded in a memo, and the root-cause analysis closed after a quality incident.

This does not mean snapshots are useless. They remain valuable for reproducible builds, deployment state, forensics, regulatory audits, and legal holds. But for **knowledge** — understanding why things are the way they are, what was considered, what was rejected — task-centric history is strictly more informative.

**Principle statement**: The primary unit of knowledge evolution is the Task (or its equivalent: Decision, Investigation, Experiment, Case Review), not the Snapshot or Commit. Version history should be derivable from task evolution, not the reverse.

#### Knowledge Requires Explicit Context Recovery
Every representation of knowledge loses context. The question is not whether context is lost, but whether the system provides mechanisms to **recover** it:

```text
What the document contains:               What was lost:
├── Final decision: Use PostgreSQL        ├── Why PostgreSQL was chosen over MySQL (Task #142)
├── Configuration parameters              ├── Who objected and why (operational familiarity)
└── Migration script                      ├── What benchmark was run (Task #140)
                                          ├── What assumption proved wrong later
                                          └── What alternatives exist now that didn't then
```

The same loss recurs everywhere: a treatment order without the differential diagnosis behind it, a filed brief without the rejected arguments, an SOP parameter without the accident that motivated it.

Git attempts to recover some context through commit messages — but commit messages are notoriously poor knowledge vessels: often written in haste, structurally free-form, disconnected from the actual reasoning process, and unable to capture dissenting opinions or rejected alternatives. A task-centric model naturally captures richer context because tasks exist specifically to host discussion, research, and decision-making.

**Principle statement**: A knowledge system must treat the document/artifact as ONE component of a knowledge unit, alongside its provenance, discussion history, decision rationale, evolutionary context, and relational connections. Storing only the artifact is storing only the conclusion, not the knowledge.

#### Classification Should Not Be Confined to a Single Hierarchy
Directory trees enforce a strict rule: **every item has exactly one parent**. This works for `Country → City → Street → House`. It fails for multi-dimensional knowledge:

```text
Medical Research Paper-123
├── belongs_to: Cardiology (specialty)
├── authored_by: Dr. Sarah Chen (author)
├── studies: Heart Failure (condition)
├── uses_method: Randomized Trial (methodology)
├── funded_by: NIH Grant (funding source)
└── tagged: High-Impact, Peer-Reviewed (quality markers)
```

In graph terms, a directory tree is a highly restricted graph (a rooted tree where each node has exactly one parent). Real-world concepts form general graphs: multi-parent, cyclic references, cross-cutting categories. Implementation approaches applicable across domains:

- **Tagging/Labeling**: simple, but tags become a flat namespace without governance.
- **Faceted Classification**: items described by multiple independent facet values (Specialty × Condition × Treatment × Evidence Level; Jurisdiction × Practice Area × Court × Outcome).
- **Graph-Based Classification**: categories are nodes; membership is an edge; categories themselves relate to each other.
- **Attribute-Based Retrieval** (Gifford et al., 1991): extract attributes from content; query by attribute combinations rather than location.

**Principle statement**: Knowledge classification must support multiple concurrent taxonomies. An item may belong to many categories simultaneously, and category membership should be independent of storage location.

#### Communication Channels Produce Knowledge but Are Not Knowledge Repositories
A common organizational error is conflating communication channels with knowledge repositories:

```text
Email threads contain knowledge → but are terrible at retrieving it
Slack conversations contain knowledge → but disappear into scrollback
Meeting recordings contain knowledge → but are virtually unsearchable
Bedside handoffs contain knowledge → but are never recorded
Courtroom arguments contain knowledge → but exist only in transcripts (if available)
```

These channels **produce** knowledge during communication, but they are not structured to **preserve or retrieve** it. The knowledge exists transiently and degrades rapidly afterward. The practical implication: do not ban the channels (people will use them anyway); build systems that make it easy to promote a conversation thread into a structured Task, extract a Decision into a recorded artifact, or link a casual discussion to a formal Concept Definition.

**Principle statement**: Communication channels generate knowledge artifacts; a knowledge system must provide mechanisms to extract, structure, and preserve those artifacts from communication flows — without disrupting the communication itself.

#### The Smallest Knowledge Unit Is Smaller Than You Think
When designing knowledge systems, there is a tendency to assume the atomic unit is something large: Document, File, Page, Record, Patient Chart, Case File, Syllabus. But knowledge granularity goes finer:

```text
Better candidates:                 Even finer:
├── Concept (any term)             ├── Distinction (between two concepts)
├── Assertion (a stated claim)     ├── Pattern (recurring structure)
├── Argument (a reasoning step)    ├── Rule (if X then Y)
├── Decision (a resolved choice)   └── Question (no settled answer yet)
└── Observation (a recorded datum)
```

Every domain has its own atomic units — function signatures and business rules in software; diagnostic criteria and drug interactions in healthcare; learning objectives and misconception patterns in education; elements of claim and legal standards in law; process parameters and failure modes in manufacturing.

Two modeling disciplines from Memar apply directly: a Comment is not an independent entity — it is Content + a `reply_to` relation; and a concept is not always a node — sometimes it is a shortcut edge (see [Modeling → the attribute-or-edge question](./modeling.md)). Reducing assumed entities to their minimal representation reduces model complexity and increases flexibility.

**Principle statement**: Knowledge systems should be able to represent and manipulate units at the granularity of individual concepts, assertions, and distinctions — not just documents or files. The choice of granularity should be driven by the use case, not by storage convenience.

### Knowledge and Code
Code has a dual nature unique to software: it is both a human-readable knowledge artifact and a machine-executable artifact. As knowledge, code benefits from every principle above — explicit relationships between modules, task-centric change history, concept definitions for domain types. As an executable artifact, code currently requires file-system projection: compilers expect files, build tools expect paths, deployment packages files. The resolution: **code's identity is content-derived; the file path is one projection among others.** The machine-consumable form may be file-based; the knowledge-managed form need not be.

Software-specific relationship types are particularly prone to remaining implicit, and implicit relationships are lost knowledge: module dependencies live only in import statements, API contracts only in stale documentation, feature gating only in scattered configuration, architectural layers only in directory conventions, security boundaries only in comments. Making these relationships explicit is the software instance of [Relationships Are First-Class Citizens](#relationships-are-first-class-citizens).

For AI-assisted development, knowledge structure directly determines capability: fragmented knowledge yields generic, context-free suggestions; well-structured knowledge — explicit relationships, task-centric history, concept-level granularity — lets an AI system reason about *why* things exist and propagate changes correctly. This is the practical face of the chain in [Knowledge in Memar's Concept Web](#knowledge-in-memars-concept-web): the quality of the shared medium is a quality of the thinking that runs on it ([Thinking → Grounding: Cognition and the 4E Framing](./thinking.md#grounding-cognition-and-the-4e-framing)).

## Results
Insufficient time has passed to report real, observed outcomes from implementing systems based on these principles. This section will be populated once principle-aligned implementations are applied in practice within Geniuses Group projects.

## Discussion

### Drawbacks
These principles are demanding. Implementing them fully requires:

1. **Infrastructure investment**: graph-based storage, content-addressable identifiers, and rich relationship modeling do not come free with traditional stacks. The investment does scale, however: small teams can start with stable identifiers and structured decision logging alone.
2. **Behavioral change**: professionals are deeply habituated to existing mental models ("where is the file?", "which folder does this go in?"). Migration requires unlearning regardless of domain.
3. **Tooling gap**: most organizations lack principle-aligned knowledge systems; custom or niche tooling is often required.
4. **Risk of over-engineering**: it is possible to build an elaborate knowledge graph nobody uses because it is too complex for everyday tasks. The principles should be applied incrementally, not all-at-once.

Most dangerously, adopting these principles can lead to **analysis paralysis** — endless modeling without shipping. The counterweight principle is: **imperfect knowledge management now beats perfect knowledge management never**.

### Rationale and alternatives
- **"Just use Confluence/Notion/Wiki" (rejected)**: these tools improve over raw files but still inherit the document-as-knowledge fallacy. They add layers (search, linking, collaboration) on top of fundamentally document-centric storage. Useful, but not addressing the root issue.
- **"Just use a Knowledge Graph database" (rejected as complete solution)**: a graph database provides storage mechanics, not a knowledge model. Without principled design of what the nodes and edges MEAN, a knowledge graph becomes another data swamp — this time with cycles.
- **"Keep current tools but be more disciplined" (partial acceptance)**: commit-message conventions, structured clinical notes, standardized syllabi. These mitigate symptoms but do not cure the disease. For organizations already invested in existing tooling, this is a reasonable transitional strategy while building toward principle-aligned systems.
- **"These principles only apply to large organizations" (rejected)**: small teams suffer knowledge loss more acutely, because they lack institutional memory and redundant personnel. The principles scale down: a solo practitioner benefits from task-centric history and explicit relationships.

### Prior art
- **Gifford et al., Semantic File Systems (1991)**: demonstrated that attribute-based (semantic) access outperforms hierarchical (directory-tree) access for information-rich content. Directly supports [Storage Model ≠ Content Model](#storage-model--content-model), [Relationships Are First-Class Citizens](#relationships-are-first-class-citizens), and [Classification Should Not Be Confined to a Single Hierarchy](#classification-should-not-be-confined-to-a-single-hierarchy).
- **Madhavapeddy et al., Unikernels (2013)**: showed that general-purpose filesystems are not universal requirements, supporting the argument that filesystem is an optional capability, not a knowledge primitive.
- **Nonaka & Takeuchi, The Knowledge-Creating Company (1991)**: the SECI model established knowledge as a dynamic, social process rather than a static asset. This document adopts the process view; the organizational machinery (socialization, externalization, combination, internalization) is developed in the Organization project.
- **Nygard, Architecture Decision Records**: a pattern for capturing decisions with context — the software instantiation of [Task-Centric Knowledge Evolution](#task-centric-knowledge-evolution) and [Knowledge Requires Explicit Context Recovery](#knowledge-requires-explicit-context-recovery).
- **Diátaxis Framework (Rock)**: documentation structured by audience need (tutorials, how-to, reference, explanation). Complements this framework by addressing document PURPOSE.
- **Zettelkasten Method (Luhmann)**: personal knowledge management based on atomic notes, links, and emergent structure. Influences [The Smallest Knowledge Unit Is Smaller Than You Think](#the-smallest-knowledge-unit-is-smaller-than-you-think) and [Relationships Are First-Class Citizens](#relationships-are-first-class-citizens).
- **Solid (Berners-Lee)**: web decentralization emphasizing personal data pods, content addressability, and granular permissions — a technical implementation of several principles here.
- **Communities of Practice (Wenger-Trayner)**: how groups learn together through shared practice — evidence for the process view of knowledge and for [Communication Channels Produce Knowledge but Are Not Knowledge Repositories](#communication-channels-produce-knowledge-but-are-not-knowledge-repositories).

### Unresolved questions
1. **What IS the minimum viable knowledge unit?** The granularity principle argues for fine units, but practical experience is needed to identify the optimal balance between expressiveness and complexity. Is the unit a Concept? An Assertion? A property change? Does the answer vary by domain?
2. **Can snapshot-style state ever be completely eliminated?** For legal holds, regulatory compliance, financial audits, and clinical trials, point-in-time global state is a genuine requirement. Is there a hybrid model where logical snapshots coexist with task-centric evolution?
3. **How do we handle concurrent knowledge modification without locking semantics?** If two people simultaneously edit the definition of a protocol or a standard, how do we reconcile? (This is the same fundamental problem as database concurrency, not unique to knowledge graphs.)
4. **Are there domains where hierarchical classification IS actually optimal?** The classification principle argues against single hierarchies universally, but configuration management, biological taxonomy, and library classification may be sufficiently hierarchical that tree projection IS the natural knowledge model. Where is the crossover point?
5. **Does the Task concept itself decompose further?** If Task is not primitive, what is? How far down does decomposition go before reaching truly atomic knowledge primitives?
6. **How do cultural factors affect principle adoption?** Research indicates that national culture, professional norms, and organizational climate significantly impact knowledge-sharing behavior. Do the principles need cultural localization, or are they genuinely universal? (The localization question, as a practice, belongs to the Organization project; it is recorded here because it tests the domain-independence claim.)

### Future possibilities
- **Content Domain Model**: [Content](./content.md) now defines Content, Semantic, Reference, and composition; the knowledge-side integration (how Knowledge units, Assertions, and Distinctions map onto Content and Relation) should be worked out against it.
- **Task Domain Model**: defining Task, Decision, Discussion, Outcome and their relationships — possibly as compositions of more primitive concepts.
- **Versioning Strategy**: how versioning works in a non-file-centric system (content versions vs. snapshot versions vs. logical timestamps).
- **Migration Path**: how organizations transition from current tooling to principle-aligned systems incrementally (the organizational-side program belongs to the Organization project).
- **AI Integration Patterns**: how AI systems consume knowledge structured by these principles, and how AI can assist in maintaining it (relationship inference, context extraction, duplicate detection).
- **Knowledge Practices**: the companion [Knowledge Practice](./knowledge.practice.md) develops the followable procedures this document's principles presuppose — questioning, researching, and evaluating knowledge.
