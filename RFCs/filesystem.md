---
Title: "Reevaluating the Filesystem as a Fundamental Modeling Primitive"
Status: Draft
Start Date: "2026-06-21"
RFC Number: 510420
Applied to: []
Citations:
    - Title: "RFC Template Specification"
      URI: "./rfc-template.md"
      Relation: "Reference"
      Reason: "Adheres to the structural and formatting rules defined by the Geniuses Group RFC template."
    - Title: "Semantic File Systems"
      URI: "https://dl.acm.org/doi/10.1145/121132.121137"
      Relation: "Reference"
      Reason: "Provides academic basis for the distinction between physical storage paths and semantic content attributes."
    - Title: "Unikernels: The Rise of the Virtual Library Operating System"
      URI: "https://dl.acm.org/doi/book/10.1145/3442482"
      Relation: "Reference"
      Reason: "Demonstrates that general-purpose filesystems are not universally required, though not necessarily obsolete everywhere."
Contributors:
  - Name: "Omid Hekayati"
    URI: "mailto:omid@geniuses.group"
    Tasks:
      - Works: ["Initiated the architectural critique of File/Directory and Git's Snapshot/Commit model", "Directed the research to separate storage engines from content models", "Proposed including Unikernel arguments against mandatory filesystem layers", "Identified the title/abstract contradiction", "Proposed the 'Git as Repair Mechanism' and 'Historical Accident' frameworks", "Directed the critique to equally target the File abstraction, not just Directory", "Advocated for reopening unresolved questions"]
        URI: ""
  - Name: "ChatGPT"
    URI: "https://openai.com"
    Model: "GPT-5.5"
    Effort: "Medium"
    Tasks:
      - Titles: ["Critical review"]
  - Name: "Super Z"
    URI: "https://z.ai"
    Model: "GLM 5.2"
    Effort: "Deep Think - Max"
    Tasks:
      - Works: ["Conducted deep research into graph theory and OS architecture", "Synthesized academic and architectural critiques into the RFC format", "Analyzed and resolved the proposed unresolved questions regarding repository state", "Synthesized the architectural critiques into the revised RFC", "Developed the 'Git as a Patch Layer' analysis", "Restructured the Unresolved Questions to remain genuinely open"]
        URI: ""
  - Name: "Claude"
    URI: "https://anthropic.com"
    Model: "Claude Sonnet 5"
    Effort: "Medium"
    Tasks:
      - Works: ["Reviewed the full chat history against the resulting RFC to identify reviewer critiques that were raised but not yet incorporated", "Softened the Path-Based Discovery claim to acknowledge path as one valid projection rather than a universally invalid model", "Added nuance to the Directory-to-Branch causal claim regarding concurrent development", "Introduced the Knowledge vs. Document/Representation distinction into the File section", "Added a fifth Unresolved Question on whether Repository is itself a fundamental domain concept"]
        URI: ""
---

# Reevaluating the Filesystem as a Fundamental Modeling Primitive

## Abstract
This specification critically examines whether the traditional File and Directory abstractions should remain first-class primitives for modeling knowledge in modern systems. It argues that the filesystem is a "historical accident"—a stack of inherited assumptions where physical storage constraints leaked into mental and knowledge models. By analyzing how tools like Git function merely as repair mechanisms (patches) over the flaws of the file/directory paradigm, this document questions the foundational validity of filesystems for knowledge systems. This RFC deliberately does not propose a replacement; its sole purpose is to deconstruct the filesystem's default validity, questioning everything from the File as a knowledge boundary to the necessity of repository-wide snapshots.

## Introduction

### Motivation
In developing knowledge management standards, organizations continuously default to file-centric tools (e.g., Git) and hierarchical storage paradigms. This forces multidimensional knowledge into rigid, single-parent hierarchical structures (directories) and isolated byte boundaries (files). The friction observed in tracking historical context, linking related concepts, and discovering information suggests that the underlying storage abstraction is fundamentally mismatched with knowledge modeling needs. We must ask: how many of our architectural layers are fundamental requirements, and how many are merely inherited assumptions?

### Methodology
This analysis deconstructs the historical assumptions of filesystems using graph theory and OS architecture. It analyzes the continuous need for workarounds to escape tree limitations (e.g., symlinks, tags) and reframes version control systems (like Git) not as independent innovations, but as direct patches over filesystem flaws. Unresolved questions from initial discussions are kept genuinely open to drive future RFCs.

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
An RFC, a Comment, an Image, a Task, and a Decision are semantically different but can all be "Content." By forcing them into Files, we create artificial byte-boundaries around knowledge. A file is merely a container for bytes, but knowledge is a continuous network of semantic relationships. Treating the file as the atomic unit shatters this network into isolated, unlinked fragments.

This points to a distinction that is easy to lose: a File is not Knowledge, it is a *representation* of knowledge frozen at a particular boundary. An RFC document does not contain the knowledge that produced it—the reasoning, the rejected alternatives, the discussion that resolved an objection—it only contains the resulting artifact. Treating the file as if it *were* the knowledge (rather than one projection of it) is what makes the loss of surrounding context feel acceptable in the first place. A knowledge model should track this distinction explicitly, rather than conflating a document with the knowledge it represents.

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

## Results
Insufficient time has passed to report real, observed outcomes from implementing systems that entirely discard filesystem primitives. This section will be populated once architectural alternatives based on this critique are applied in practice.

## Discussion

### Drawbacks
The filesystem is one of the most successful and deeply entrenched abstractions in computer science. Deviating from it requires rethinking developer tooling, deployment, and human interaction paradigms. Dismissing it entirely may introduce friction in interoperability with existing third-party tools that expect POSIX-compliant, file-based I/O.

### Rationale and alternatives
- **Claim: "Filesystem is bad, we must replace it" (rejected)**: This RFC does not argue the filesystem was a mistake. It was highly effective for storage-oriented systems. The claim is narrowly scoped: it is an inherited assumption for *knowledge systems*, not a fundamental requirement.
- **Claim: "Git is an independent knowledge tool" (refined)**: Git is a filesystem repair mechanism. Its flaws in knowledge management are inherited directly from the file/directory paradigm.

### Prior art
- **Semantic File Systems (Gifford et al., 1991)**: Explored non-hierarchical file access through attributes, proving the inadequacy of directory trees.
- **Unikernels (Madhavapeddy et al.)**: Demonstrated library operating systems that function without a traditional filesystem layer.
- **Graph Databases / Knowledge Graphs**: Acknowledge that relationships, not trees or files, model reality.

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

### Future possibilities
Future RFCs must explore alternative primitives for Content and Task modeling that are not bound by file boundaries or tree structures. Additionally, a dedicated RFC is needed to redefine versioning not as a repository-wide physical snapshot, but as a logical consequence of task and decision evolution.

## Change Rationale
- **Third revision.** Reconciled the RFC text against reviewer critiques that had been raised in discussion but not yet applied to the document: softened the Path-Based Discovery claim to treat paths as one valid projection among many rather than a universally invalid model; added nuance to the Directory-to-Branch causal claim so it does not overstate Branch's origin as solely a directory-escape mechanism; introduced an explicit Knowledge vs. Document/Representation distinction in the File section; and added a fifth Unresolved Question asking whether Repository is itself a fundamental domain concept or an emergent, filesystem-era projection.
- **Second revision.** Addressed architectural critiques by reframing Git as a "repair mechanism" over filesystem flaws rather than an independent tool. Introduced "Storage Leakage" and "Historical Accident" concepts. Expanded the critique to equally target the "File" abstraction as an artificial knowledge boundary. Toned down Unikernel claims to avoid overstating. Reopened Unresolved Questions to genuinely reflect the Draft status of this exploration.
- **Initial draft.** Synthesized from architectural review chat logs and deep academic research. Established the core critique that the filesystem is a storage model improperly used as a knowledge model.
