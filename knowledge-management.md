---
Title: "Knowledge Management Principles for Software Development"
Status: Draft
Start Date: 2026-07-20
RFC Number: 510421
Applied to: []
Citations:
    - Title: "Reevaluating the Filesystem as a Fundamental Modeling Primitive"
      URI: "./filesystem.md"
      Relation: "Depends_on"
      Reason: "This specification builds upon the filesystem critique to establish positive principles for knowledge modeling."
    - Title: "The Knowledge-Creating Company: How Japanese Companies Create the Dynamics of Innovation"
      URI: "https://hbr.org/1991/07/the-knowledge-creating-company"
      Relation: "Reference"
      Reason: "Nonaka & Takeuchi's foundational work on organizational knowledge creation, introducing the SECI model (Socialization, Externalization, Combination, Internalization) that remains influential in KM research."
    - Title: "Key success factors of knowledge management systems for optimizing organizational performance"
      URI: "https://www.sciencedirect.com/science/article/pii/S2405844025024983"
      Relation: "Reference"
      Reason: "Recent empirical study identifying critical success factors for KMS adoption and effectiveness in organizations."
    - Title: "Organizational Knowledge and Knowledge Management - A New Framework"
      URI: "https://www.researchgate.net/publication/384774643_Organizational_Knowledge_and_Knowledge_Management_-_A_New_Framework"
      Relation: "Reference"
      Reason: "Proposes a new framework for understanding knowledge flow within firms, relevant to our discussion of knowledge evolution and traceability."
    - Title: "Managing Knowledge in Organizations: A Nonaka's SECI Model Operationalization"
      URI: "https://pmc.ncbi.nlm.nih.gov/articles/PMC6914727"
      Relation: "Reference"
      Reason: "Practical operationalization of Nonaka's SECI model with measurable dimensions for knowledge management assessment."
    - Title: "Semantic File Systems"
      URI: "https://dl.acm.org/doi/10.1145/121132.121138"
      Relation: "Reference"
      Reason: "Gifford et al.'s seminal work demonstrating that attribute-based (semantic) access to content is more effective than hierarchical (directory-tree) access for information-rich systems."
    - Title: "Unikernels: Library Operating Systems for the Cloud"
      URI: "https://anil.recoil.org/papers/2013-asplos-mirage.pdf"
      Relation: "Reference"
      Reason: "Madhavapeddy et al.'s work demonstrating that general-purpose filesystems are not universal requirements, supporting our argument that filesystem is an optional capability."
    - Title: "Usage and usefulness of technical software documentation"
      URI: "https://www.sciencedirect.com/science/article/abs/pii/S095058491400192X"
      Relation: "Reference"
      Reason: "Industrial case study showing that documentation value depends on discoverability, relevance, and accessibility — all knowledge management concerns."
Contributors:
  - Name: "Omid Hekayati"
    URI: "mailto:omid@geniuses.group"
    Tasks:
      - Works: ["Initiated the architectural critique of File/Directory and Git's Snapshot/Commit model", "Directed the research toward separating storage engines from content models", "Advocated for treating Repository as emergent projection rather than fundamental concept", "Emphasized that GUI must not determine domain model", "Identified that organizations produce data but fail to produce retrievable knowledge", "Directed the insight that Comment=Content+Relation, not independent entity"]
        URI: ""
  - Name: "ChatGPT"
    URI: "https://openai.com"
    Model: "GPT-5.5"
    Effort: "Medium"
    Tasks:
      - Works: ["Analyzed Git as repair mechanism over filesystem flaws", "Developed Task-centric knowledge evolution model", "Proposed Decision as outcome of Task, not root concept", "Identified Commit Message as compensation for missing Task entity"]
  - Name: "Claude"
    URI: "https://anthropic.com"
    Model: "Claude Sonnet 5"
    Effort: "Medium"
    Tasks:
      - Works: ["Reviewed chat history against resulting documents", "Softened Path-Based Discovery claim to acknowledge path as valid projection", "Added nuance to Directory-to-Branch causal claim", "Introduced Knowledge vs Document/Representation distinction", "Analyzed GUI Projection vs Domain Model separation"]
  - Name: "Super Z"
    URI: "https://z.ai"
    Model: "GLM 5.2"
    Effort: "Deep Think - Max"
    Tasks:
      - Works: ["Conducted deep research into SECI model, semantic filesystems, and KMS success factors", "Synthesized multi-chat insights into unified framework", "Established connection between filesystem critique and KM principles", "Developed Content Addressability and Explicit Relations principles", "Restructured architectural critiques into principle-based format"]
        URI: ""
---

# Knowledge Management Principles for Software Development

## Abstract
This specification establishes foundational principles for managing knowledge within software development organizations, particularly those building domain-specific languages, frameworks, or platforms. It argues that **knowledge management failure is the root cause of most organizational dysfunction in software teams** — not process inadequacy, not tooling gaps, not communication problems per se. By analyzing how traditional abstractions (File, Directory, Repository, Commit) leak storage-oriented assumptions into knowledge models, this document proposes a set of principles for designing systems where **knowledge, not files, is the primary modeling primitive**. These principles are intentionally停留在 principle-level; they do not prescribe implementation details which belong to the Organization project's domain modeling work.

## Introduction

### Motivation
In developing software systems — particularly those intended for broad use like frameworks, languages, or platforms — organizations continuously default to file-centric tools (Git, wikis, document management systems) and hierarchical storage paradigms. This forces multidimensional knowledge into rigid structures. The friction observed in tracking historical context, linking related concepts, discovering information, and recovering decision rationale suggests that the underlying storage abstraction is fundamentally mismatched with knowledge modeling needs. This is not a new observation: researchers have documented "knowledge fragmentation" in organizations since the 1990s (Nonaka & Takeuchi, 1991; Wiig, 1993). What this specification adds is a **software-development-specific analysis** of why these failures persist and what architectural principles might address them.

The immediate trigger for this specification was a series of architectural discussions about whether File and Directory should remain first-class primitives for modeling knowledge in modern systems (`filesystem.md`). Those discussions revealed deeper questions:

- Why do organizations produce vast amounts of data but cannot retrieve knowledge when needed?
- Why does every team eventually build its own wiki/confluence/notion structure, only to abandon it?
- Why do decisions made six months ago become irrecoverable, even though the decision was "documented"?
- Why does Git — designed for source code version control — become the de facto knowledge repository for things that have nothing to do with code?

This specification attempts to answer these questions at the principle level, leaving domain-specific design to the Organization project.

### Methodology
This analysis synthesizes insights from multiple sources:

1. **Academic research**: Nonaka's SECI model of knowledge creation, studies on KMS success factors, research on semantic filesystems and information retrieval.
2. **Architectural discussions**: Extensive multi-session dialogues between human architects and AI assistants examining File, Directory, Git, Repository, Content, Task, and their relationships.
3. **Historical analysis**: Tracing how computing abstractions evolved from physical constraints (block devices, limited memory, single-user systems) into assumed truths about knowledge organization.
4. **Industry observation**: Examining patterns of tool adoption, abandonment, and fragmentation in real software organizations.

Unresolved questions from earlier discussions are kept genuinely open to drive future specifications.

## Explanation

### Principle 1: Knowledge ≠ Data ≠ Information ≠ Document
Before discussing tools or structures, we must establish what we are actually trying to manage. Drawing on the Data-Information-Knowledge-Wisdom (DIKW) hierarchy and Nonaka's distinction between tacit and explicit knowledge:

**Data**: Raw symbols, bytes, characters without interpreted meaning.
```
42
"customer"
0x1a2b3c
```

**Information**: Data with context, structure, and interpretive meaning.
```
Customer ID: 42 refers to Omid Hekayati, registered 2024-01-15
```

**Knowledge**: Information integrated with experience, context, relationships, and actionable understanding.
```
Customer #42 (Omid) prefers email communication on Tuesday mornings because his team stands up on Wednesdays and he prepares talking points overnight. This preference emerged from a pattern observed across 17 interactions and was confirmed in Q3 planning.
```

**Document**: A frozen representation of knowledge at a specific boundary, for specific purposes.
```
RFC-510420: "Communication Preferences Specification" — contains the above knowledge in structured form, but is NOT the knowledge itself.
```

**Critical implication**: A document is a **projection** of knowledge, not knowledge itself. When we store documents, we store representations. When we lose the surrounding context (why was this written? what alternatives were rejected? who disagreed?), we lose knowledge even if the document remains intact. Most organizational "knowledge management" systems actually manage documents and mistake the map for the territory.

### Principle 2: Storage Model ≠ Content Model
One of the most pervasive errors in system design is conflating *how* something is stored with *what* it means. The filesystem is the canonical example:

```text
Storage Engine Concerns:
├── Persistence (bytes survive power loss)
├── Addressing (find the bytes later)
├── Allocation (fit N bytes on physical media)
├── Access Control (who may read/write)
└── Integrity (detect corruption)

Content Model Concerns:
├── Semantics (what does this mean?)
├── Relationships (how does it connect to other knowledge?)
├── Provenance (who created this, why, based on what?)
├── Evolution (how has this changed over time?)
└── Context (what assumptions does this depend on?)
```

The filesystem was designed to address Storage Engine concerns in an era of scarce resources (limited memory, expensive disks, single-user systems). It was never designed to address Content Model concerns. However, a **storage leakage** occurred: physical storage constraints dictated mental models. Instead of a Knowledge Model dictating its Storage Projection, Block Device constraints defined how we structure thoughts (Directories).

**Principle statement**: Any system where the content model inherits structure from the storage engine will eventually fail at knowledge management. The two models must be independently designable, with storage as one possible projection of content.

### Principle 3: Identity Must Be Independent of Location
Git's most important contribution to software development was not Branch, Merge, or Distributed development. It was **Content Addressability**:

```text
Before Git:
Identity = Location
"The file at /src/customer/model.go"

After Git:
Identity = Content Hash
"The object whose SHA is a3f2b1c..."
```

This seems technical but has profound knowledge-management implications:

- **Location-based identity**: Moving a file changes its identity. Renaming a directory breaks all references. Reorganizing a project destroys provenance.
- **Content-based identity**: Content is what it is regardless of where it's stored. References survive reorganization. Provenance is inherent.

**Principle statement**: In any knowledge system, the stable identifier of a knowledge artifact must be derived from its content (or assigned immutablely at creation), never from its storage location. Location may change; identity must not.

Application: If `RFC-495000` is identified by its number (content-derived or assigned), it remains the same RFC whether stored in `/docs/rfc/`, `/knowledge/architecture/`, or a graph database node. Its relationships, version history, and metadata travel with it — they are not properties of its containing directory.

### Principle 4: Relationships Are First-Class Citizens
Traditional filesystems model exactly one relationship: **containment** (`parent → child`). This single relationship type is forced to represent all semantic connections:

```text
"RFC-A is inside /architecture/"     → containment (physical)
"Task-B is related to RFC-A"         → ??? (must use tags, symlinks, or conventions)
"Decision-C informed both"          → ??? (no native representation)
"Concept-D is a special case of E"   → ??? (no native representation)
```

The ecosystem's response reveals the inadequacy: Symlinks, Tags, Labels, Bookmarks, References, Cross-references, Search Indexes — each an attempt to escape the single-relationship prison.

**Principle statement**: A knowledge model must support multiple, explicit, typed relationships as first-class citizens. Containment is one useful relationship among many, not the privileged default.

Relationship types that should be natively supported (at minimum):
- **Containment**: A is physically/compositionally part of B
- **Reference**: A cites or points to B
- **Dependency**: A requires B to exist/be valid
- **Sequence**: A precedes B temporally or logically
- **Specialization**: A is a more specific form of B
- **Association**: A is related to B (general-purpose)
- **Attribution**: A was created/modified/approved by B
- **Opposition**: A contrasts with or negates B

### Principle 5: UI Projection ≠ Domain Model
Perhaps the most important principle for practical system design:

```text
What users SEE:
├── Files and Folders
├── Repositories
├── Issues and Pull Requests
├── Comments and Threads
└── Wikis and Pages

What those things REPRESENT:
├── Content nodes with various types
├── Context/grouping nodes (possibly emergent)
├── Task nodes with state transitions
├── Content + reply_to relation
└── Content with Definition profile
```

These are NOT the same. Conflating them leads to systems where the UI becomes the domain model — and when the UI needs to change (which it always does), the domain model must change too, breaking all existing data and integrations.

**Principle statement**: The user-visible interface (GUI, CLI, API surface) is a **projection** of the domain model, optimized for specific interaction patterns. Multiple projections can coexist on the same model. No projection should constrain the model's expressive power.

Practical implications:
- You CAN build a GitHub-like interface on top of a graph-based knowledge model.
- You CAN build a Wiki-like interface on the same model.
- You CAN build a Reddit/Twitter-like interface on the same model.
- You SHOULD be able to add a new interface without changing the model.
- If adding a feature requires changing your data schema, your UI has leaked into your model.

### Principle 6: Task-Centric Knowledge Evolution
Most version control systems (Git being the primary example) model history around **snapshots**:

```text
Commit = State of all files at time T
```

But organizational knowledge rarely evolves around snapshots. It evolves around **tasks and decisions**:

```text
Task
├── Question / Problem Statement
├── Discussion (multi-participant, temporal)
├── Research / Evidence Gathered
├── Alternatives Considered
├── Decision (with rationale)
├── Outcomes (what changed as a result)
└── Related Content (what documents were affected)
```

When someone asks "Why does this code look like this?" six months later, the answer is almost never in the commit snapshot. It's in the task discussion, the decision rationale, the rejected alternatives.

**Principle statement**: The primary unit of knowledge evolution is the Task (or its equivalent: Decision, Investigation, Experiment), not the Snapshot or Commit. Version history should be derivable from task evolution, not the reverse.

This does not mean snapshots are useless. They are extremely valuable for:
- Reproducible builds ("compile exactly this state")
- Deployment ("what's running in production?")
- Forensics ("what did the world look like when bug X appeared?")

But for **knowledge management** — understanding why things are the way they are, what was considered, what was rejected — task-centric history is strictly more informative.

### Principle 7: Knowledge Requires Explicit Context Recovery Mechanisms
Every representation of knowledge loses context. The question is not WHETHER context is lost, but whether the system provides mechanisms to RECOVER it:

```text
What the document contains:
├── Final decision: Use PostgreSQL
├── Configuration parameters
└── Migration script

What was lost:
├── Why PostgreSQL was chosen over MySQL (discussed in Task #142)
├── Who objected and why (Sarah: operational familiarity)
├── What benchmark was run (link to Task #140)
├── What assumption proved wrong later (connection pooling behavior)
└── What alternatives exist now that didn't then (TiDB, CockroachDB)
```

**Principle statement**: A knowledge management system must treat the document/artifact as ONE component of a knowledge unit, alongside its provenance, discussion history, decision rationale, evolutionary context, and relational connections. Storing only the artifact is storing only the conclusion, not the knowledge.

Git attempts to recover some context through Commit Messages — but commit messages are notoriously poor knowledge vessels:
- Often written in haste ("fix", "update", "refactor")
- Lack structure (free text, no standard fields)
- Disconnect from the actual reasoning process
- Cannot capture dissenting opinions or rejected alternatives

A Task-centric model naturally captures richer context because tasks exist specifically to host discussion, research, and decision-making.

### Principle 8: Classification Should Not Be Confined to Single Hierarchy
Directory trees enforce a strict classification rule: **every item has exactly one parent**. This works adequately for:

```text
Country → City → Street → House
```

It fails catastrophically for:

```text
Photo-123
├── belongs_to: Birthday Party (event)
├── features: Ali (person)
├── taken_in: Tehran (location)
├── dated: 2026-01-15 (time)
└── tagged: Family, Celebration (topics)
```

In graph theory terms, a directory tree is a highly restricted graph (specifically, a rooted tree where each node has exactly one parent). Real-world concepts form general graphs (multi-parent, cyclic references, cross-cutting categories).

**Principle statement**: Knowledge classification must support multiple concurrent taxonomies. An item may belong to many categories simultaneously, and category membership should be independent of storage location.

Implementation approaches:
- **Tagging/Labeling**: Simple but often unstructured; tags become a flat namespace without hierarchy.
- **Faceted Classification**: Items described by multiple independent facet values (like e-commerce: Brand × Price Range × Category × Color).
- **Graph-Based Classification**: Categories are nodes; membership is an edge; categories themselves can have relationships.
- **Attribute-Based Retrieval** (Gifford et al., 1991): Extract attributes from content automatically; query by attribute combinations rather than location.

### Principle 9: Communication ≠ Knowledge (But Can Produce It)
A common organizational error is conflating communication channels with knowledge repositories:

```text
Email threads contain knowledge → but are terrible at retrieving it
Slack conversations contain knowledge → but disappear into scrollback
Meeting recordings contain knowledge → but are virtually unsearchable
Chat bot histories contain knowledge → but are locked in proprietary formats
```

These channels PRODUCE knowledge during communication, but they are not structured to PRESERVE or RETRIEVE it. The knowledge exists transiently during the conversation and degrades rapidly afterward.

**Principle statement**: Communication channels generate knowledge artifacts; a knowledge management system must provide mechanisms to extract, structure, and preserve those artifacts from communication flows — without disrupting the communication itself.

Practical implication: Don't ban Slack/Email/Discord (people will just use them anyway). Build systems that make it easy to promote a conversation thread into a structured Task, extract a Decision into a recorded artifact, or link a casual discussion to a formal Concept Definition.

### Principle 10: The Smallest Knowledge Unit Is Smaller Than You Think
When designing knowledge systems, there's a tendency to assume the atomic unit is something large:

```text
Common assumptions (too large):
├── Document
├── File
├── Page
├── Article
└── Record
```

But knowledge granularity goes finer:

```text
Better candidates:
├── Concept (any token: word, phrase, term)
├── Assertion (a stated fact or claim)
├── Argument (reasoning step supporting a conclusion)
├── Decision (a resolved choice among alternatives)
└── Observation (a recorded datum or measurement)
```

Even finer:

```text
Atomic level:
├── Distinction (differentiation between two concepts)
├── Pattern (recognizable recurring structure)
├── Rule (conditional relationship: if X then Y)
└── Question (an inquiry with no settled answer yet)
```

**Principle statement**: Knowledge systems should be able to represent and manipulate units at the granularity of individual concepts, assertions, and distinctions — not just documents or files. The choice of granularity should be driven by the use case, not by storage convenience.

This connects directly to the observation from the architectural discussions: **Comment is not an independent entity; it is Content + reply_to relation**. Customer is not always a Node; sometimes it is a shortcut edge representing "User who has completed a purchase." Reducing assumed entities to their minimal representation reduces model complexity and increases flexibility.

## Results
Insufficient time has passed to report real, observed outcomes from implementing systems based on these principles. This section will be populated once architectural alternatives following these principles are applied in practice within Geniuses Group projects or the Organization platform.

## Discussion

### Drawbacks
These principles are demanding. Implementing them fully requires:

1. **Infrastructure investment**: Graph-based storage, content-addressable identifiers, rich relationship modeling — none of these come free with traditional stacks.
2. **Behavioral change**: Developers and organizations are deeply habituated to file-centric thinking ("where is the file?", "which folder does this go in?"). Migration requires unlearning.
3. **Tooling gap**: While Git integrates with everything, graph-based knowledge systems require custom or niche tooling. IDE integration, CI/CD integration, code review workflows all assume file-centricity.
4. **Risk of over-engineering**: It's possible to build an elaborate knowledge graph that nobody uses because it's too complex for everyday tasks. The principles should be applied incrementally, not all-at-once.

Most dangerously, adopting these principles can lead to **analysis paralysis** — endless modeling without shipping. The counterweight principle is: **imperfect knowledge management now beats perfect knowledge management never**.

### Rationale and alternatives
- **"Just use Confluence/Notion/Wiki" (rejected)**: These tools improve over raw files but still inherit the document-as-knowledge fallacy. They add layers (search, linking, collaboration) on top of fundamentally document-centric storage. Useful, but not addressing the root issue.
- **"Just use a Knowledge Graph database (Neo4j, etc.)" (rejected as complete solution)**: A graph database provides storage mechanics, not a knowledge model. Without principled design of what the nodes and edges MEAN, a knowledge graph becomes another data swamp — this time with cycles.
- **"Keep using Git but be more disciplined" (partial acceptance)**: Git discipline (commit messages, conventional commits, PR templates) mitigates symptoms but does not cure the disease. For organizations already invested in Git, this is a reasonable transitional strategy while building toward principle-aligned systems.
- **"These principles only apply to large organizations" (rejected)**: Small teams suffer knowledge loss too — arguably more, because they lack institutional memory, documentation staff, and redundant personnel. The principles scale down; a solo developer benefits from task-centric history and explicit relationships.

### Prior art
- **Nonaka & Takeuchi SECI Model (1991)**: Foundational framework for understanding how tacit knowledge converts to explicit knowledge through Socialization, Externalization, Combination, and Internalization. Our principles align with SECI's emphasis on knowledge as a dynamic, social process — not a static asset.
- **Gifford et al., Semantic File Systems (1991)**: Demonstrated that attribute-based (semantic) access outperforms hierarchical (directory-tree) access for information-rich content. Directly supports Principles 2, 4, and 8.
- **Madhavapeddy et al., Unikernels (2013)**: Showed that general-purpose filesystems are not universal requirements. Supports Principle 2 (Storage ≠ Content).
- **Nygard, Architecture Decision Records**: Influential pattern for capturing decisions with context. Aligns with Principle 6 (Task-centric evolution).
- **Diátaxis Framework (Rock)**: Documentation structured by audience need (Tutorials, How-to Guides, Reference, Explanation). Complements our framework by addressing document PURPOSE.
- **Zettelkasten Method (Luhmann)**: Personal knowledge management system based on atomic notes, links, and emergent structure. Influences Principle 10 (small knowledge units) and Principle 4 (relationships as first-class).
- **Solid (Berners-Lee)**: Web decentralization protocol emphasizing personal data pods, content addressability, and granular permissions. Technical implementation of several principles here.

### Possible questions
1. **Do these principles mean we should abandon Git entirely?**
   *Addressed:* No. Git solves real problems (identity via SHA, distributed synchronization, merge algorithms, binary diffing). The critique is that Git's knowledge-management features (commit messages as context, repository as organization unit, snapshot as history) are inadequate for organizational knowledge. Git remains excellent for source-code-specific concerns. The question is whether source code IS the primary knowledge artifact in your organization — for many modern organizations, it increasingly isn't.

2. **Is a graph database required to implement these principles?**
   *Addressed:* Not necessarily. A graph DATABASE is one implementation option. A graph MODEL is what's required. You can implement graph relationships in relational databases (junction tables), document stores (embedded references), or even key-value stores (with index tables). The principle is about conceptual structure, not storage technology. That said, native graph databases reduce impedance mismatch if your model is inherently graph-like.

3. **How does this relate to AI-assisted development (like the Memar/Architect project)?**
   *Addressed:* Directly and critically. AI assistants consume knowledge to generate outputs. If the knowledge is fragmented across emails, Slack, Git commits, Confluence pages, and people's heads, the AI cannot reason effectively. These principles describe the kind of knowledge structure that would make AI assistance maximally effective: explicit relationships, task-centric history, concept-level granularity, separated concerns. The Architect project's modeling.md already moves in this direction; these principles provide the philosophical foundation.

4. **What about code specifically? Isn't code inherently file-based?**
   *Addressed:* Code has dual nature: it is both a human-readable knowledge artifact AND a machine-executable artifact. As knowledge, code benefits from these principles (explicit relationships between modules, task-centric change history, concept definitions for domain types). As executable artifact, code currently requires file-system projection (compilers expect files, build tools expect paths, deployment packages files). The resolution suggested in architectural discussions: **Code's identity is ContentUUID (or similar); file path is one projection among others.** The machine-consumable form may be file-based; the knowledge-managed form need not be.

5. **Isn't "knowledge management" just consultant-speak for "using a wiki"?**
   *Addressed:* Common perception, but missing the point. Wikis are DOCUMENT management systems (Principle 1: they manage representations, not knowledge). Knowledge management, properly understood, addresses: How do decisions get made? How is context preserved? How is expertise discovered? How does learning propagate? A wiki can be PART of a knowledge management ecosystem (as a document projection layer) but is not synonymous with it.

6. **Who has time for this? We have software to ship.**
   *Addressed:* Valid concern, and the reason Principle selection emphasizes incremental adoption. Start with Principle 3 (independent identity) — use UUIDs or content hashes instead of paths. Add Principle 4 (explicit relationships) — tag dependencies explicitly, not implicitly through directory structure. Adopt Principle 6 (task-centric history) — write decision rationales in task trackers, not commit messages. None of these requires rebuilding your infrastructure. Each adds knowledge resilience with modest effort.

### Unresolved questions
1. **What IS the minimum viable knowledge unit?** Principle 10 argues for fine granularity, but practical experience is needed to identify the optimal balance between expressiveness and complexity. Is the unit a Concept? An Assertion? A Property change? Different domains may require different granularities.
2. **Can repository-wide state (Git snapshot) ever be completely eliminated?** For certain domains (legal, financial, regulatory), point-in-time global state is a genuine requirement. Is there a hybrid model where logical snapshots (state of all items related to Decision-42) coexist with task-centric evolution?
3. **How do we handle concurrent knowledge modification without file-locking semantics?** Git solves this for files via branches/merges. What is the equivalent operation for graph nodes? If two people simultaneously edit the definition of "Customer," how do we reconcile? (Note: this is the same fundamental problem as database concurrency, not unique to knowledge graphs.)
4. **Are there domains where filesystem-as-knowledge-model is actually optimal?** Principle 8 argues against single-hierarchy classification universally, but perhaps some domains (configuration management, build pipelines) are sufficiently hierarchical that filesystem projection IS the natural knowledge model. Where is the crossover point?
5. **Does the Task concept itself decompose further?** Architectural discussions suggest Task = Group + Content + State + Permission composition. If Task is not primitive, what is? How far down does decomposition go before reaching truly atomic knowledge primitives?

### Future possibilities
Future specifications must explore concrete implementations of these principles:
- **Content Domain Model**: Defining Content, Timeline, Relation, and associated types with enough precision for implementation.
- **Task Domain Model**: Defining Task, Decision, Discussion, Outcome and their relationships — possibly as compositions of more primitive concepts.
- **Versioning Strategy**: Defining how versioning works in a non-file-centric system (content versions vs. snapshot versions vs. logical timestamps).
- **Migration Path**: How organizations transition from file-centric tooling to principle-aligned systems incrementally.
- **AI Integration Patterns**: How AI assistants (like the Architect project's agents) consume knowledge structured according to these principles.

## Change Rationale
- **Initial draft.** Synthesized from extensive multi-party architectural discussions spanning filesystem critique, Git analysis, content modeling explorations, and knowledge management theory. Draws on academic sources (Nonaka SECI model, Gifford semantic filesystems, Madhavapeddy unikernels) and industrial studies (KMS success factors, documentation usefulness research). Intentionally principle-focused rather than implementation-focused, deferring domain-specific design to the Organization project while establishing philosophical foundations for Geniuses Group's approach to knowledge in software development.
