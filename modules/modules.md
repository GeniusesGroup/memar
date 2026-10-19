# Modules
A module is the base rule of the container it sits in: a kernel type at the repository root, an optional capability under `modules-plugable/`, a standing rule of a bundle inside `bundles/<name>/modules/`. The three scopes are defined in [Bundles](../bundles/bundles.md#the-word-modules).

This document and its companions, [modules.changelog.md](modules.changelog.md) and [modules.handoff.md](modules.handoff.md), hold only how a module is placed and added. A change inside a module — a new module, an edge, a decision — is recorded in that module's own changelog and handoff, never here.

## Placement
Where a module is placed — [Kernel](./knowledge/classification/primitive/kernel.md), [Pluggable](./knowledge/classification/primitive/pluggable.md), [Bundle](./knowledge/classification/primitive/bundle.md) — which [category](./knowledge/classification/primitive/category.md) it is browsed under, and which [labels](./knowledge/classification/classification.md#labels) (`guest`, first) it carries is decided by Memar's [Classification](./knowledge/classification/classification.md), with its [Placement](./knowledge/classification/rules/placement/placement.md) and [Category Depth](./knowledge/classification/rules/category-depth/category-depth.md) rules. That module is the authority; this repository's placements were first worked out here and now cite it, and where this repository places a module differently it owes the reason in that module's own handoff. What a label is, and that a name is one, is Memar's [Label](./knowledge/label/label.md). The bundle test is in [Bundles](../bundles/bundles.md).

This repository's categories (`computer`, `economics`, `identity`, `knowledge`, `management`, `rights`, `storage`) are not final; their re-reading is in [Modules Handoff](modules.handoff.md#re-reading-this-repositorys-categories).

These rules are this repository's own, over its graph of vertices and edges:

- An edge becomes its own module only when it carries independent domain semantics — identity, lifecycle, authorization, rules, processing. A purely structural or classifying relation does not.
- No bare edges. An edge with no stated who-may-create-or-remove and what it triggers does not exist. An apparently simple `member_of` or `related_to` is either a real capability with rules or a shortcut over a deeper path.
- Kernel does not reference the [rule](computer/rule/rule.md) domain directly: a generic `condition_is` edge connects a subject to a rule node, and the rules engine decides the semantics.
- Cross-domain analytics sit under the category's `analytics` namespace in `modules-plugable/`, named by the knowledge produced; domain analytics sit inside the pluggable that produces them. A query crossing categories has no home yet.
- Behavior binds to a module's UUID, never to a name, so two organizations may ship the same term with different identity and different rules.

## Edge buckets
Every relationship folder under a domain is one of three kinds, decided in this order. Ground: Memar `docs/modeling.md` → *Edge Types and Their Traditional Counterparts*.

- `edges/` — two distinct nodes: an acquired relation.
- `edges-loop/` — a classification on one node, the node related to itself, spelled as a single `Type_*` or `Status_*` marker on that node.
- `edges-shortcut/` — a derived cache of a walk already in the graph. It is never the source of truth, and its document names the source edges it recomputes from. A fact the user sets (mute, pin, invite) is acquired and is not a shortcut.

## Edge folder
Every edge is one folder under the owning `edges/`, `edges-loop/`, or `edges-shortcut/`: `<name>/<name>.md` plus a one-line `README.md`, with the sections Model, Policies, Placement, and Open questions. There is no aggregate `edges.md`, and a domain document does not list its folders or point at that directory as a substitute for the list — membership is the directory. A sentence may name an edge that lives in another domain when that placement is the judgment. Uncertain edge notes stay in that edge's Open questions; non-edge sketches go to the domain backlog as `**Idea**` / `**Review questions**`. Ground: Memar `docs/documentation.md` → *No derivative inventories*.

The path is the owner; the folder name is the relation. Name it for the relation (`depend-on`, `citizen`, `site`) or, when several labels share one document, for the other end (`module`, `group`). Do not repeat the owning domain in the folder name unless that word is the classification itself (`budget/edges/budget`). A deleted path is not archived: once the claim is in the document, `Migrated from`, `Verbatim`, and `(deleted …)` are not part of the model, and a `Source` line names only a file that is still in the tree.

## Module skeleton
A module's folders are one project-defined skeleton — `manifest`, `edges`, `edges-loop`, `edges-shortcut`, `protocol`, `services`, `status` — and a module does not invent a private taxonomy. The skeleton's exact names are under revision; the open item is in [Modules Handoff](modules.handoff.md).

## Model

### Graph vertex
Base on [DDD] We MUST choose some limited thing to be top level modules labels.

### Graph Edges
Graph Edges use as labels to relate two vertices or as a graph loop.

### Graph loop
In graph theory, a [loop](https://en.wikipedia.org/wiki/Loop_(graph_theory)) (also called a self-loop or a buckle) is an edge that connects a vertex to itself. A simple graph contains no loops.

#### Examples
- `Commodity` is an edge for any `product` vertex but not link the `product` to any other `thing` in the system.

### Pitfalls
- Labels for bad relation. 
  - `user1` is `creator` of `comment1` with `email` label and `user2` is `creator` of `comment2` with `email` label that `comment2` is `reply` for `comment1` so we can use `REPLIED_TO` label as `user2` `REPLIED_TO` `comment1`, But it is better to use as `comment2` `REPLY_TO` `comment1`

### Fields
- Some edges CAN carry some data such as `time` or `status` or ...
- They will be introduces in each package or in `memar`

## Top or thing Levels labels

Just some limited labels can be top or quiddity Levels labels. We MUST think very deeply to add any label here e.g. `project` is just a label for `task` and MUST NOT add as thing level label.

`TODO:::` Each UUID can use in more than one vertex category.
e.g. `product` UUID is as `text` UUID for a product.
e.g. `product` UUID use as `group` for a product as default chat timeline (comments)
If above is true, we can assume that default text as `loop edge` is title for each vertex.

## Idea backlog

Nothing below is ratified.

### Module manifest
- **Idea**: a published module carries a manifest: name, description, documentation URL, git repository, files to include and exclude, compilers (name and version), install and uninstall scripts, and requirements split into direct, indirect, and test-only.
- **Review questions**: is that manifest a document of this repository's module layout, or a package format of its own? The sketch nested a full module descriptor inside each direct requirement. Does a requirement name an existing module, or copy that module's manifest?
