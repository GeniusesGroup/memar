# Reevaluating the Filesystem as a Fundamental Modeling Primitive Handoff

Open work for `protocols/filesystem.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../documentation-handoff.md) for what a handoff is.

## Open Questions

### Can repository-wide state be completely eliminated without losing necessary historical context?
- State: if it can, the snapshot paradigm of Git is obsolete. (Migrated from the base document's retired `Unresolved questions`.)

### What minimum primitive replaces the File?
- State: if a file is an artificial boundary, what the correct atomic unit of content is remains open. (Migrated from the base document's retired `Unresolved questions`.)

### What capabilities are lost if the filesystem disappears entirely?
- State: are there critical operations that *only* a filesystem can natively support? (Migrated from the base document's retired `Unresolved questions`.)
- Decomposition from the knowledge-management session: Git's value is the *solutions* it happens to provide, not the *problems* it answers; a successor must re-derive each requirement without assuming file shapes. The requirements Git currently satisfies: stable **Identity** for artifacts; **Change** recording over time; **Provenance** (who, when, based on what); **Consistency** (many actors, one evolving knowledge base); **Synchronization** (offline, online, and distributed continuation); **State Reconstruction** (recover any named past state); and **Conflict Resolution**. Each is a knowledge-system need that survives the filesystem critique; Git's file-centric realization of each does not.

### If Git is internally already graph-like, what does its filesystem surface contribute?
- State: Git's object model is a graph — commits are content-addressed nodes (identity by hash, not path), parents are edges, branches are labels on nodes — so the filesystem-centric shape persists at Git's *surface and workflows*, not in its model. The residual limit is semantic, not structural: Git models the graph of files and changes, not the knowledge graph — it cannot know that two terms are synonyms, that one decision caused seventeen modifications, or that one document invalidates another's assumption. Open: whether a knowledge system can adopt the graph-like internal model while replacing the file-centric surface, or whether Git's repair value is inherently bound to code-centric workflows. (From the knowledge-management session that produced `knowledge.md`.)

### Are there domains where the filesystem as a knowledge model is actually optimal, or is it always a compromise?
- State: unresolved at the time of migration. (Migrated from the base document's retired `Unresolved questions`.)

### How do we handle the cognitive transition for developers who have spent careers thinking in files?
- State: even if the new model is superior, the migration cost (learning, tooling, muscle memory) is non-trivial and may be underestimated. (Migrated from the base document's retired `Unresolved questions`.)

### Is Repository itself a fundamental domain concept, or merely a filesystem-era projection of a richer graph structure?
- State: a repository bundles several distinct concerns — access control, context, grouping, versioning boundary, discovery boundary — into a single physical container. It is not yet established whether these concerns are inherently coupled, or whether "Repository" would simply re-emerge as an *emergent* grouping (e.g., all Content linked to a shared context node) once the underlying model no longer requires a physical container to enforce them. (Migrated from the base document's retired `Possible questions` list, where it was the one question left unanswered.)

## Anticipated Work

- Future documents must explore alternative primitives for Content and Task modeling that are not bound by file boundaries or tree structures. (Migrated from the base document's retired `Future possibilities`.)
- A dedicated document is needed to redefine versioning not as a repository-wide physical snapshot, but as a logical consequence of task and decision evolution. (Migrated from the base document's retired `Future possibilities`.)
- **Content Identity Mechanisms**: how ContentUUID or content-addressable identifiers replace file paths as stable references without sacrificing usability. (Migrated from the base document's retired `Future possibilities`.)
- **Graph-Based Classification Systems**: practical implementations of multi-dimensional classification that exceed the capabilities of tags or hierarchies while remaining performant at scale. (Migrated from the base document's retired `Future possibilities`.)
- **Task-Centric Versioning**: history models where the primary unit is task evolution (question → research → decision → outcome → related changes), not global snapshot. (Migrated from the base document's retired `Future possibilities`; carries the retired `Possible questions` answer's forward half — logical snapshots tied to tasks replacing physical snapshots.)
- **Projection Layer Architecture**: how to maintain file-system-like UI compatibility (for developer familiarity and tool integration) atop a non-file-based knowledge model. (Migrated from the base document's retired `Future possibilities`.)
