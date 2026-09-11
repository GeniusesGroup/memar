---
Title: "Reevaluating the Filesystem as a Fundamental Modeling Primitive"
Status: Draft
Start Date: 2026-06-21
ID: 510420
---

# Reevaluating the Filesystem as a Fundamental Modeling Primitive
This document deconstructs the default validity of File and Directory as primitives for modeling knowledge; the positive principles this critique motivates are stated in its companion, [Knowledge](../knowledge.md).

## Abstract
This specification critically examines whether the traditional File and Directory abstractions should remain first-class primitives for modeling knowledge in modern systems. It argues that the filesystem is a "historical accident"—a stack of inherited assumptions where physical storage constraints leaked into mental and knowledge models. By analyzing how tools like Git function merely as repair mechanisms (patches) over the flaws of the file/directory paradigm, this document questions the foundational validity of filesystems for knowledge systems. This document deliberately does not propose a replacement; its sole purpose is to deconstruct the filesystem's default validity, questioning everything from the File as a knowledge boundary to the necessity of repository-wide snapshots. The deconstruction serves a practical check: the companion [Filesystem Practice](./filesystem.practice.md) turns it into criteria for deciding, concern by concern, whether a system actually needs the filesystem protocol surface.

## Introduction

### Motivation
In developing knowledge management standards, organizations continuously default to file-centric tools (e.g., Git) and hierarchical storage paradigms. This forces multidimensional knowledge into rigid, single-parent hierarchical structures (directories) and isolated byte boundaries (files). The friction observed in tracking historical context, linking related concepts, and discovering information suggests that the underlying storage abstraction is fundamentally mismatched with knowledge modeling needs. We must ask: how many of our architectural layers are fundamental requirements, and how many are merely inherited assumptions?

### Methodology
This analysis deconstructs the historical assumptions of filesystems using graph theory and OS architecture. It analyzes the continuous need for workarounds to escape tree limitations (e.g., symlinks, tags) and reframes version control systems (like Git) not as independent innovations, but as direct patches over filesystem flaws. Unresolved questions from initial discussions are kept genuinely open in the paired handoff to drive future documents.

## Explanation

### Memar's Stance on the Filesystem Protocol Surface
The filesystem is not a concept Memar defines: it is a protocol surface owned outside Memar — the POSIX file interface, the VFS contract, and their kin — with stable, externally specified rules. Memar's own stack is expected to implement that surface rather than inherit it from a host: [memar-khayyam](https://github.com/GeniusesGroup/memar-khayyam/), for example, will likely provide filesystem access as a component it realizes itself. This is why this document lives in [`protocols/`](./README.md): it does not answer "what is a filesystem?" (the general meaning governs — see [Terminology → The Default Meaning of an Unreferenced Term](../terminology.md#the-default-meaning-of-an-unreferenced-term)); it answers "what is Memar's position on depending on the filesystem?"

That stance has one content: **in Memar's stack, the filesystem is a high-level library — a component whose inclusion is a decision — not an OS-given foundation.** The prevailing OS view inverts this: because every conventional operating system presents files as unavoidable, developers design systems as if the filesystem were a fundamental requirement, and that inherited assumption leaks into domain models, knowledge structures, and architectures. This document is a deep critique of that inheritance; the topics below supply the evidence. Its function toward the builder is a warning with an action attached: **set aside the old default that you necessarily need a filesystem, and actually check whether you want the need** — for compilation, artifact caching, configuration delivery, and log storage, a filesystem may well be the right answer. What is not acceptable is choosing it by default, without the check. If the check says the filesystem goes, expect the trade-off: direct human navigation via CLI and legacy tool integration become harder; multiple classification, semantic querying, traceability of decisions, and maintaining a single source of truth become easier. The check itself — the criteria that replace the strong past default — is operationalized in the companion [Filesystem Practice](./filesystem.practice.md).

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
In graph theory, a directory tree is a highly restricted subset of a graph. Real-world concepts are multidimensional. A photograph represents Person, Event, Place, and Time simultaneously. A directory tree can only model one classification natively. The ecosystem has continually invented mechanisms to bypass this (Symlinks, Tags, Labels), which is an implicit admission that the tree model is structurally inadequate for multiple classification. The classification critique has empirical support: semantic filesystem research demonstrated that users of attribute-based systems found information 5-10x faster than hierarchical systems for real-world queries (Gifford et al., 1991).

### Path-Based Discovery vs. Semantic Discovery
The filesystem inherently assumes that discovery is based on location:
```
Location  ->  Discovery ("I know where it is")
```
This requires the human to maintain a mental map of the tree structure. However, almost all modern systems—search engines, semantic search, vector databases, and knowledge graphs—operate on a different paradigm:
```
Meaning   ->  Discovery ("I know what it is about")
```
None of these modern discovery mechanisms rely on paths. This does not mean path-based discovery is invalid in every case—a hierarchy like `Country -> City -> Street -> House` remains a legitimate and useful way to traverse certain relationships. The flaw is not that paths exist, but that the filesystem elevates *one* projection of relationships to the status of the *only* addressable one. A knowledge model should be able to expose path-like views (for humans who think that way) as one of several projections over a richer relationship graph, rather than forcing all discovery through location. Wikidata and the Google Knowledge Graph validate in practice that relationship-first models scale to millions of entities in ways tree-based models cannot.

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
It is important not to overstate this: this does not prove the filesystem is entirely unnecessary in all domains. It simply proves that the filesystem is *not universally required*. It transitions from an "inherent system necessity" to an "optional runtime capability," challenging the default assumption that all higher-level systems must rely on it. This optionality is borne out in practice: production adoption (e.g., Docker-based deployments, cloud-native applications) demonstrates that filesystem-less operation is viable for specific domains.

### Distinction Between Storage Engine and Content Model
Critiquing the filesystem does not mean abandoning storage. A base storage engine (typically Key/Value stores today) is still required for persistence. However, there is a strict architectural distinction between:
- **Storage Engine**: How bytes are persisted on physical media.
- **Content Model**: How knowledge is semantically structured, related, and queried.

The failure of the traditional filesystem is that it conflated these two concepts, forcing the content model to inherit the limitations of the storage engine.

### File/Directory as UI Projection, Not Domain Model
A refinement emerging from extended discussion: File and Directory may have always been primarily **user interface projections** — ways of interacting with stored information — rather than domain models reflecting the intrinsic structure of knowledge itself.

Consider: even systems that don't use files internally (chat applications, AI assistants, graph databases) often present file-like interfaces to users because people expect them. The filesystem metaphor persists not because it's conceptually correct but because it's familiar. This is consistent with the UI Projection ≠ Domain Model principle of the companion [Knowledge](../knowledge.md) specification: the file explorer GUI is a valid projection, but treating that projection as the source of truth about knowledge structure is the error.
