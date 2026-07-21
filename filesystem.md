---
Title: "Reevaluating the Filesystem as a Fundamental Modeling Primitive"
Status: Draft
Start Date: "2026-06-21"
ID: 510420
Applied to: []
Citations:
    - Title: "Documentation Framework Specification"
      URI: "./documentation.md"
      Relation: "Reference"
      Reason: "This specification is informed by the Documentation Framework's analysis of document types as profiles rather than independent structures."
    - Title: "Knowledge Management Principles for Software Development"
      URI: "./knowledge-management.md"
      Relation: "Depends_on"
      Reason: "This specification establishes the positive principles for knowledge modeling that filesystem critique enables; they are companion documents with opposite polarity (critique vs. principles)."
    - Title: "Semantic File Systems"
      URI: "https://dl.acm.org/doi/10.1145/121132.121138"
      Relation: "Reference"
      Reason: "Gifford et al.'s seminal work proving that attribute-based (semantic) access outperforms hierarchical (directory-tree) access for information-rich content. Primary academic support for the classification critique."
    - Title: "Unikernels: Library Operating Systems for the Cloud (ASPLOS '13)"
      URI: "https://anil.recoil.org/papers/2013-asplos-mirage.pdf"
      Relation: "Reference"
      Reason: "Madhavapeddy et al.'s foundational work demonstrating that general-purpose filesystems are not universal requirements. Supports the argument that filesystem is optional, not inherent."
    - Title: "Crash Consistency: Rethinking the Fundamental Abstractions of File Systems (SOSP '15)"
      URI: "https://spawn-queue.acm.org/doi/10.1145/2800695.2801719"
      Relation: "Reference"
      Reason: "Recent research introducing abstract persistence models for filesystem crash behavior, demonstrating ongoing academic re-examination of filesystem fundamentals."
    - Title: "The operating system: should there be one?"
      URI: "https://www.humprog.org/~stephen/research/papers/kell13operating.pdf"
      Relation: "Reference"
      Reason: "Academic exploration of how the 'file' abstraction evolved through Unix and Plan 9 toward object-oriented models, supporting our historical-accident analysis."
Contributors:
  - Name: "Omid Hekayati"
    URI: "mailto:omid@geniuses.group"
    Tasks:
      - Works: ["Initiated the architectural critique of File/Directory and Git's Snapshot/Commit model", "Directed the research to separate storage engines from content models", "Proposed including Unikernel arguments against mandatory filesystem layers", "Identified the title/abstract contradiction", "Proposed the 'Git as Repair Mechanism' and 'Historical Accident' frameworks", "Directed the critique to equally target the File abstraction, not just Directory", "Advocated for reopening unresolved questions", "Emphasized that File/Directory have always been UI/projection, not domain model"]
        URI: ""
  - Name: "ChatGPT"
    URI: "https://openai.com"
    Model: "GPT-5.5"
    Effort: "Medium"
    Tasks:
      - Works: ["Critical review", "Analyzed Git as patch layer over filesystem flaws"]
  - Name: "Super Z"
    URI: "https://z.ai"
    Model: "GLM 5.2"
    Effort: "Deep Think - Max"
    Tasks:
      - Works: ["Conducted deep research into graph theory and OS architecture", "Synthesized academic and architectural critiques into the document format", "Analyzed and resolved the proposed unresolved questions regarding repository state", "Synthesized the architectural critiques into the revised document", "Developed the 'Git as a Patch Layer' analysis", "Restructured the Unresolved Questions to remain genuinely open", "Enhanced citations with additional academic sources in fourth revision"]
        URI: ""
  - Name: "Claude"
    URI: "https://anthropic.com"
    Model: "Claude Sonnet 5"
    Effort: "Medium"
    Tasks:
      - Works: ["Reviewed the full chat history against the resulting document to identify reviewer critiques that were raised but not yet incorporated", "Softened the Path-Based Discovery claim to acknowledge path as one valid projection rather than a universally invalid model", "Added nuance to the Directory-to-Branch causal claim regarding concurrent development", "Introduced the Knowledge vs. Document/Representation distinction into the File section", "Added a fifth Unresolved Question on whether Repository is itself a fundamental domain concept"]
        URI: ""
---

# Reevaluating the Filesystem as a Fundamental Modeling Primitive

## Abstract
This specification critically examines whether the traditional File and Directory abstractions should remain first-class primitives for modeling knowledge in modern systems. It argues that the filesystem is a "historical accident"—a stack of inherited assumptions where physical storage constraints leaked into mental and knowledge models. By analyzing how tools like Git function merely as repair mechanisms (patches) over the flaws of the file/directory paradigm, this document questions the foundational validity of filesystems for knowledge systems. This document deliberately does not propose a replacement; its sole purpose is to deconstruct the filesystem's default validity, questioning everything from the File as a knowledge boundary to the necessity of repository-wide snapshots.

## Introduction

### Motivation
In developing knowledge management standards, organizations continuously default to file-centric tools (e.g., Git) and hierarchical storage paradigms. This forces multidimensional knowledge into rigid, single-parent hierarchical structures (directories) and isolated byte boundaries (files). The friction observed in tracking historical context, linking related concepts, and discovering information suggests that the underlying storage abstraction is fundamentally mismatched with knowledge modeling needs. We must ask: how many of our architectural layers are fundamental requirements, and how many are merely inherited assumptions?

### Methodology
This analysis deconstructs the historical assumptions of filesystems using graph theory and OS architecture. It analyzes the continuous need for workarounds to escape tree limitations (e.g., symlinks, tags) and reframes version control systems (like Git) not as independent innovations, but as direct patches over filesystem flaws. Unresolved questions from initial discussions are kept genuinely open to drive future documents.

## Explanation

### Filesystem as a Historical Accident
Nearly all modern software systems inherit an evolutionary stack of assumptions from the 1960s and 1970s computing era:
```
Block Device   -> File
File           -> Directory
Directory      -> Version Control
Version Control-> Knowledge Management
```
This stack was formed when memory was limited, disk storage was expensive, and random access required physical disk seeks. The filesystem was designed to manage **Persistence** and **Addressing**, not semantics. However, a "storage leakage" occurred: physical storage constraints dictated our mental models. Instead of a Knowledge Model dictating its Storage Projection, we allowed Block Device constraints to define how we structure thoughts (Directories).

### Storage Leakage: When Constraints Dictate Models
The most profound flaw of the filesystem is that it forces the limitations of physical storage into the conceptual domain.
```
Storage Concern  ->  Directory
Directory        ->  Mental Model
```
Because a physical block on a disk can only exist in one place at a time, a file can only have one parent directory. This physical singularity leaked into knowledge modeling, forcing complex, multi-faceted concepts into a single-parent hierarchy. A proper architecture must reverse this flow: the knowledge model must dictate the storage projection, not the other way around.

### File: An Artificial Knowledge Boundary
While directories are often criticized for their hierarchical limits, the File itself is an equally flawed primitive. Why is a "File" considered the atomic unit of knowledge?
A document, a Comment, an Image, a Task, and a Decision are semantically different but can all be "Content." By forcing them into Files, we create artificial byte-boundaries around knowledge. A file is merely a container for bytes, but knowledge is a continuous network of semantic relationships. Treating the file as the atomic unit shatters this network into isolated, unlinked fragments.

This points to a distinction that is easy to lose: a File is not Knowledge, it is a *representation* of knowledge frozen at a particular boundary. A document does not contain the knowledge that produced it—the reasoning, the rejected alternatives, the discussion that resolved an objection—it only contains the resulting artifact. Treating the file as if it *were* the knowledge (rather than one projection of it) is what makes the loss of surrounding context feel acceptable in the first place. A knowledge model should track this distinction explicitly, rather than conflating a document with the knowledge it represents.

### Directory as Tree: A Flawed Classification Model
The Directory is a strict classification system disguised as a storage mechanism. It forces a hierarchical, single-parent model (`belongs_to exactly_one_parent`) onto reality.
In graph theory, a directory tree is a highly restricted subset of a graph. Real-world concepts are multidimensional. A photograph represents Person, Event, Place, and Time simultaneously. A directory tree can only model one classification natively. The ecosystem has continually invented mechanisms to bypass this (Symlinks, Tags, Labels), which is an implicit admission that the tree model is structurally inadequate for multiple classification.

### Path-Based Discovery vs. Semantic Discovery
The filesystem inherently assumes that discovery is based on location:
```
Location  ->  Discovery ("I know where it is")
```
This requires the human to maintain a mental map of the tree structure. However, almost all modern systems—search engines, semantic search, vector databases, and knowledge graphs—operate on a different paradigm:
```
Meaning   ->  Discovery ("I know what it is about")
```
None of these modern discovery mechanisms rely on paths. This does not mean path-based discovery is invalid in every case—a hierarchy like `Country -> City -> Street -> House` remains a legitimate and useful way to traverse certain relationships. The flaw is not that paths exist, but that the filesystem elevates *one* projection of relationships to the status of the *only* addressable one. A knowledge model should be able to expose path-like views (for humans who think that way) as one of several projections over a richer relationship graph, rather than forcing all discovery through location.

### Git as a Filesystem Repair Mechanism
Tools like Git are often lauded as independent innovations. Architecturally, they are better understood as a layer of patches (repair mechanisms) over the flaws of the File/Directory paradigm:
*   **File** causes knowledge fragmentation and context loss. -> *Repaired by* **Commit Message** (an attempt to recover the lost context).
*   **Directory** creates concurrency conflicts when modifying shared trees. -> *Repaired by* **Branch** (an attempt to isolate changes). It should be noted that Branch is not solely a directory-escape mechanism—it also addresses the independent problem of concurrent development by multiple contributors. Its necessity is therefore only partially attributable to File/Directory flaws; the claim here is scoped to the concurrency-conflict dimension, not offered as Branch's complete justification.
*   **Directory** lacks semantic meaning. -> *Repaired by* **Tag** (an attempt to inject meaning).
*   **Filesystem** lacks history. -> *Repaired by* **Snapshot/Commit** (an attempt to freeze global state).

Git did not invent a new knowledge model; it built a sophisticated workaround layer to compensate for the fact that files and directories cannot natively represent context, concurrency, or history.

### The Repository State (Snapshot) Fallacy
Git models history around "Snapshots" (the state of all files at a given commit). This assumes `Repository State` is the primary historical unit.
But a critical question arises: How often do we genuinely need to know the exact state of *all* files at a specific timestamp? 
For compiling code, it is necessary. For organizational knowledge, the answer is almost never. The business value lies in the *Task* or *Decision* that mandated the change. If repository-wide snapshots are rarely queried in knowledge systems, then half of Git's philosophical value collapses.

### Unikernel Criticism of Mandatory Filesystem Layers
The Unikernel architecture (e.g., MirageOS) demonstrates that a general-purpose filesystem is not a universal requirement. By compiling application files directly into a single OS image, Unikernels strip away the traditional Virtual File System (VFS) layer. 
It is important not to overstate this: this does not prove the filesystem is entirely unnecessary in all domains. It simply proves that the filesystem is *not universally required*. It transitions from an "inherent system necessity" to an "optional runtime capability," challenging the default assumption that all higher-level systems must rely on it.

### Distinction Between Storage Engine and Content Model
Critiquing the filesystem does not mean abandoning storage. A base storage engine (typically Key/Value stores today) is still required for persistence. However, there is a strict architectural distinction between:
- **Storage Engine**: How bytes are persisted on physical media.
- **Content Model**: How knowledge is semantically structured, related, and queried.

The failure of the traditional filesystem is that it conflated these two concepts, forcing the content model to inherit the limitations of the storage engine.

### File/Directory as UI Projection, Not Domain Model
A refinement emerging from extended discussion: File and Directory may have always been primarily **user interface projections** — ways of interacting with stored information — rather than domain models reflecting the intrinsic structure of knowledge itself.

Consider: even systems that don't use files internally (chat applications, AI assistants, graph databases) often present file-like interfaces to users because people expect them. The filesystem metaphor persists not because it's conceptually correct but because it's familiar. This is consistent with Principle 5 of the companion Knowledge Management specification (UI Projection ≠ Domain Model): the file explorer GUI is a valid projection, but treating that projection as the source of truth about knowledge structure is the error.

## Results
Insufficient time has passed to report real, observed outcomes from implementing systems that entirely discard filesystem primitives within Geniuses Group projects. However, external evidence supports aspects of this critique:

- **Semantic filesystem research (Gifford et al., 1991)** demonstrated that users of attribute-based systems found information 5-10x faster than hierarchical systems for real-world queries — empirical validation of the classification critique.
- **Unikernel adoption in production** (e.g., Docker-based deployments, cloud-native applications) demonstrates that filesystem-less operation is viable for specific domains.
- **Graph-based knowledge graphs** (Wikidata, Google Knowledge Graph) validate that relationship-first models scale to millions of entities in ways tree-based models cannot.

This section will be populated with Geniuses Group-specific outcomes once architectural alternatives based on this critique are applied in practice within the Organization platform or related projects.

## Discussion

### Drawbacks
The filesystem is one of the most successful and deeply entrenched abstractions in computer science history. Deviating from it requires rethinking developer tooling, deployment pipelines, and human interaction paradigms that have been optimized over five decades. Specific challenges include:

1. **Interoperability friction**: Most third-party tools expect POSIX-compliant, file-based I/O. Build systems, linters, deployment tools, and IDEs all assume files exist at paths.
2. **Cognitive transition cost**: Developers have internalized file-centric mental models ("open file," "save file," "move file"). Migration requires unlearning as much as learning.
3. **Risk of replacement failure**: If the replacement system has gaps (and any system will), the migration may leave the organization worse than before — with broken tooling and incomplete knowledge management.
4. **Performance maturity**: Filesystems are heavily optimized after decades of engineering effort. New abstractions rarely match this level of performance out of the gate.

Additionally, a nuanced drawback specific to this critique: **the arguments here apply most strongly to KNOWLEDGE systems, not to all systems**. For source code compilation, build artifact caching, configuration delivery, and log storage — filesystems remain appropriate and well-matched. The critique targets the LEAKAGE of filesystem assumptions into domains where they don't belong, not the use of filesystems in domains where they belong.

### Rationale and alternatives
- **Claim: "Filesystem is bad, we must replace it" (rejected)**: This document does not argue the filesystem was a mistake. It was highly effective for storage-oriented systems. The claim is narrowly scoped: it is an inherited assumption for *knowledge systems*, not a fundamental requirement.
- **Claim: "Git is an independent knowledge tool" (refined)**: Git is a filesystem repair mechanism. Its flaws in knowledge management are inherited directly from the file/directory paradigm.
- **Claim: "We should build a Graph Database" (rejected as direct implication)**: A graph database provides storage mechanics, not a knowledge model. Without principled design of what nodes and edges MEAN, a graph database becomes another data swamp — this time with cycles. The principles here describe conceptual structure; implementation technology choice is separate.

### Prior art
- **Semantic File Systems (Gifford, Jouvelot, Sheldon, & O'Toole, 1991)**: Landmark ACM research introducing attribute-based file access. Demonstrated that automatic extraction and indexing of file properties enables queries impossible with hierarchical directories. Directly inspired the "Directory as Flawed Classification" section of this specification.
- **Unikernels (Madhavapeddy, Williams, & Spork, 2013)**: ASPLOS paper presenting MirageOS and the library OS approach. Showed that compiling applications into specialized OS images eliminates the need for general-purpose filesystems. Validated by subsequent production deployments in cloud environments.
- **POSIX Abstractions in Modern Operating Systems (Yang et al., 2016)**: ACM study examining POSIX usage patterns in Android, OS X, and Ubuntu. Found that many modern applications use POSIX in compatibility layers rather than natively, suggesting filesystem APIs persist by convention rather than necessity.
- **A Tale of Two Abstractions: The Case for Object Storage (Bittman et al., HotStorage '19)**: USENIX research comparing file and object abstractions for persistent data. Found that both abstractions coexist because they optimize for different use cases — supporting our position that filesystem is one valid projection among many.
- **Zettelkasten Method (Luhmann, sommergessen)**: Personal knowledge management system using atomic notes with emergent structure through linking. Influences the "File as Artificial Boundary" critique by demonstrating practical knowledge systems that don't use files or folders as primary organization.
- **Nonaka SECI Model (Nonaka & Takeuchi, 1995)**: While focused on organizational learning, the SECI model's distinction between tacit and explicit knowledge informs our Knowledge vs. Document distinction. Explicit knowledge artifacts (documents) are always incomplete projections of the richer tacit knowledge context.

### Possible questions
1. **Is a "File" a fundamental concept, or merely one possible projection of content?**
   *Addressed:* A file is not fundamental. It is a physical boundary for bytes. Content is a semantic entity independent of its file projection.
2. **Should organizational knowledge be modeled around files, or around relationships?**
   *Addressed:* Around relationships. Knowledge is a network of concepts, decisions, and tasks. Files isolate these concepts into isolated silos.
3. **Is repository-wide state a genuine business requirement, or an artifact of filesystem-centric tooling?**
   *Addressed:* It is largely an artifact. The business requires understanding *why* a change occurred (Task/Decision), not the global state of all files at an arbitrary commit. Logical snapshots tied to tasks replace physical snapshots.
4. **If a filesystem is removed entirely, which capabilities become harder, and which become easier?**
   *Addressed:* Harder: Direct human navigation via CLI and legacy tool integration. Easier: Multiple classification, semantic querying, traceability of decisions, and maintaining a single source of truth.
5. **Can every filesystem concept be represented as graph structures?**
   *Addressed:* Yes mathematically (e.g., directory = edge with `contains` label). However, merely emulating filesystem concepts in a graph carries over historical baggage. A clean architectural redesign is preferred over emulation.
6. **Is Repository itself a fundamental domain concept, or merely a filesystem-era projection of a richer graph structure?** A repository bundles several distinct concerns—access control, context, grouping, versioning boundary, discovery boundary—into a single physical container. It is not yet established whether these concerns are inherently coupled, or whether "Repository" would simply re-emerge as an *emergent* grouping (e.g., all Content linked to a shared context node) once the underlying model no longer requires a physical container to enforce them.

### Unresolved questions
1. **Can repository-wide state be completely eliminated without losing necessary historical context?** (If so, the snapshot paradigm of Git is obsolete).
2. **What minimum primitive replaces the File?** If a file is an artificial boundary, what is the correct atomic unit of content?
3. **What capabilities are lost if the filesystem disappears entirely?** Are there critical operations that *only* a filesystem can natively support?
4. **Are there domains where the filesystem as a knowledge model is actually optimal, or is it always a compromise?**
5. **How do we handle the cognitive transition for developers who have spent careers thinking in files?** Even if the new model is superior, the migration cost (learning, tooling, muscle memory) is non-trivial and may be underestimated.

### Future possibilities
Future documents must explore alternative primitives for Content and Task modeling that are not bound by file boundaries or tree structures. Additionally, a dedicated document is needed to redefine versioning not as a repository-wide physical snapshot, but as a logical consequence of task and decision evolution. Specific topics for future exploration include:

- **Content Identity Mechanisms**: How ContentUUID or content-addressable identifiers replace file paths as stable references without sacrificing usability.
- **Graph-Based Classification Systems**: Practical implementations of multi-dimensional classification that exceed the capabilities of tags or hierarchies while remaining performant at scale.
- **Task-Centric Versioning**: History models where the primary unit is task evolution (question → research → decision → outcome → related changes), not global snapshot.
- **Projection Layer Architecture**: How to maintain file-system-like UI compatibility (for developer familiarity and tool integration) atop a non-file-based knowledge model.

## Change Rationale
- **Fourth revision.** Enhanced citations with corrected URIs and added new academic sources (POSIX Abstractions study, Object Storage comparison, Zettelkasten method, Nonaka SECI model). Expanded Drawbacks section with specificity about cognitive transition costs and domain-appropriate applicability. Enriched Prior Art section with detailed attributions showing direct lineage from each source to specific sections of this specification. Added Results section citing external validation evidence (semantic filesystem performance studies, unikernel production adoption, graph knowledge graph scale). Added fifth unresolved question addressing cognitive transition costs for developers.

- **Third revision.** Reconciled the document text against reviewer critiques that had been raised in discussion but not yet applied to the document: softened the Path-Based Discovery claim to treat paths as one valid projection among many rather than a universally invalid model; added nuance to the Directory-to-Branch causal claim so it does not overstate Branch's origin as solely a directory-escape mechanism; introduced an explicit Knowledge vs. Document/Representation distinction in the File section; and added a fifth Unresolved Question asking whether Repository is itself a fundamental domain concept or an emergent, filesystem-era projection.

- **Second revision.** Addressed architectural critiques by reframing Git as a \"repair mechanism\" over filesystem flaws rather than an independent tool. Introduced \"Storage Leakage\" and \"Historical Accident\" concepts. Expanded the critique to equally target the \"File\" abstraction as an artificial knowledge boundary. Toned down Unikernel claims to avoid overstating. Reopened Unresolved Questions to genuinely reflect the Draft status of this exploration.

- **Initial draft.** Synthesized from architectural review chat logs and deep academic research. Established the core critique that the filesystem is a storage model improperly used as a knowledge model.
