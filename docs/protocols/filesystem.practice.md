---
name: filesystem
description: replaces the default assumption that a system needs a filesystem with an explicit, per-concern need-check and recorded decision
---

# Filesystem Practice

> **Purpose:** This practice operationalizes [filesystem.md](./filesystem.md): it turns that document's warning — set aside the default that you necessarily need a filesystem — into a followable check with explicit criteria. The critique and its arguments live in the base document and are not restated here; each criterion below links to the topic that argues it.

---

## The Default to Suspend

*"Every software system has a filesystem; architecture questions start inside it."*

Under Memar's stance ([filesystem.md → Memar's Stance on the Filesystem Protocol Surface](./filesystem.md#memars-stance-on-the-filesystem-protocol-surface)), the filesystem is a high-level library whose inclusion is a decision. This practice is that decision procedure.

---

## When to Run the Check

Run it when any of these appears in the work:

- a new system (software, hardware, organization) is being designed and files, paths, or folders show up in the draft model;
- an OS or substrate dependency is being chosen for a component;
- a domain model's structure mirrors a directory layout (folders as categories, filenames as metadata);
- a tool's requirement ("the compiler expects files") is about to become an architectural premise;
- a storage decision is being inherited from an existing project without examination.

---

## The Need Check

Answer each question about **one concern at a time** — the answer may differ per concern within the same system. Do not answer for "the system" as a whole.

1. **What kind of thing is being stored?**
   Opaque bytes with no internal semantics (build artifacts, caches, logs, media blobs) → the filesystem fits; the critique targets leakage, not use ([Drawbacks](./filesystem.md#drawbacks)). Semantic, multi-relational knowledge → the file imposes an artificial boundary around it ([File: An Artificial Knowledge Boundary](./filesystem.md#file-an-artificial-knowledge-boundary)).

2. **How must it be discovered?**
   By known location → path-based access is a legitimate projection. By meaning, attribute, or relationship → the tree is the wrong primitive ([Path-Based Discovery vs. Semantic Discovery](./filesystem.md#path-based-discovery-vs-semantic-discovery)).

3. **What history is needed?**
   Point-in-time global state (reproducible builds, audits, legal holds) → snapshots are justified. Decision rationale, rejected alternatives, discussion → snapshots cannot carry it; task-centric evolution must ([The Repository State (Snapshot) Fallacy](./filesystem.md#the-repository-state-snapshot-fallacy)).

4. **Is the classification genuinely single-parent?**
   True hierarchies (`Country → City → Street → House`) → tree is native and fine. Multi-dimensional membership (one item in many categories at once) → single-parent containment is a constraint, not a model ([Directory as Tree: A Flawed Classification Model](./filesystem.md#directory-as-tree-a-flawed-classification-model)).

5. **What external surfaces must be satisfied?**
   External tools, other operating systems, or boot processes that expect POSIX paths → expose files as a **projection layer** over the real model, not as the model itself ([File/Directory as UI Projection, Not Domain Model](./filesystem.md#filedirectory-as-ui-projection-not-domain-model), [Future possibilities → Projection Layer Architecture](./filesystem.md#future-possibilities)).

6. **Could the substrate be smaller?**
   The unikernel result shows the filesystem is an optional runtime capability, not an inherent necessity ([Unikernel Criticism of Mandatory Filesystem Layers](./filesystem.md#unikernel-criticism-of-mandatory-filesystem-layers)). If the answers above find no need for a given concern, do not include it for that concern.

---

## Recording the Decision

The outcome — full dependency, projection-only, or none — must be an explicit, recorded decision, not a silent default: Memar's framework standard is that no aspect of the design space may be assumed by default; every assumption must be the outcome of an explicit decision ([Framework → Goal-Oriented Frameworks and Purpose Space](../framework.md#goal-oriented-frameworks-and-purpose-space)). Record it where the project's decisions live (a Task or Decision artifact), with the answers above as its rationale.

---

## Anti-patterns

- Designing the domain model to fit a directory layout.
- Encoding metadata in filenames or paths.
- Treating "the compiler needs files at the build boundary" as "the system needs a filesystem at the model boundary."
- Adopting a graph database and then reproducing single-parent folders inside it.
- Banning the filesystem — the check may well conclude *yes, use it*. The error is the default, not the outcome.
