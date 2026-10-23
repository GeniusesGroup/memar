---
Title: "Label Rule — A Folder Is a Label"
Status: Draft
Start Date: 2026-10-22
ID: 497843
---

# Label Rule — A Folder Is a Label
Label's rules live one rule per directory under [`modules/knowledge/label/rules/`](../README.md), and this is the rule for what making a folder is, and what a reader may conclude from a path. It is held for every folder of every project built with Memar, and it applies [Label → A name is one label](../../label.md#a-name-is-one-label) to the file system: a folder's name is a label, and a path is a way of labelling.

## The rule
- **Making a folder is labelling.** Every content placed in a folder takes the folder's name as a label, whether or not anyone wrote it down. A folder is therefore made for a label that is worth finding content by, and its name is that label's word, with one identifier, defined once by the module that owns the kind of label it is ([Label → A label has an identifier](../../label.md#a-name-is-one-label)). The same word at two places in the tree is one label at two places, never two labels that happen to be spelled alike.
- **A path is one chain of labels, and each position in it says one kind.** The first position of a path says one kind of thing, the second another, and so on; the kind of each position is stated by the document that owns the position (for example the root of a module says its placement, and the level under it its subject). A path is a namespace for browsing. It is never read as subordination — that what stands below is a part of, a kind of, or owned by what stands above — unless the document that owns the position says the relation is that one.
- **Labels of different kinds are independent, and they combine; they do not nest.** A module that is `kernel` and `computer` is two true statements about it, one of placement and one of subject, and neither is a kind of the other. When both must be known quickly, both are carried, each in the one place that owns it; a kind the path does not carry is carried as a label in the module's manifest ([Label → Labels](../../label.md#a-modules-labels)). A kind is carried in one place only, never by the path and also by the manifest.
- **A path carries as few kinds as it can, and each extra kind is a cost the reader pays.** A tree can show one chain; a second kind in the same path means the same word stands under two roots, and the reader must reason that it is one label there, not two. A kind that only some readers search by is a manifest label, not a folder, until a folder is shown to make finding faster for most.
- **A subject is named where it is owned.** A word that names a subject (the file system, a transport, a database) is the label of the module that owns it, and other modules reach the subject through an abstraction of their own need, not by naming it. A module that names a subject it does not own has depended on it, and the dependence stays after the name is forgotten. The module that owns the file system names it; another module reaches storage through an abstraction of its own need, and takes on no dependence on the file system by naming it.
- **A folder made ahead of its content stays a decision made visible** ([Modules → Why a folder may exist before it holds code](../../../../README.md#why-a-folder-may-exist-before-it-holds-code)), and a folder whose label no longer says anything true of what it holds is renamed or retired like any label ([Label](../../label.md)).

## Why it exists
A path is the first label every reader meets, and the only one an agent sees without opening a file. When a path carries several kinds at once without saying which is which — a placement as a root and a subject beneath it, the same subject under two roots — the reader has to reason to learn that `modules/computer` and `modules-plugable/computer` are one subject in two placements, and that "kernel" and "computer" do not stand in the relation the tree seems to draw. That reasoning is what an agent skips, and the cost is a module put where its name seems to point and a subject named from the places that should not know it. The file system gives one way of labelling, a single chain in which every item has exactly one parent ([Knowledge → Classification Should Not Be Confined to a Single Hierarchy](../../../knowledge.md#classification-should-not-be-confined-to-a-single-hierarchy)); a project that needs several independent kinds of label must say which kind each position holds, and carry the rest elsewhere.

## Keep it or drop it
An organization may keep or drop this rule for its own tree. Dropping it is coherent for a tree one team reads and nobody searches. Memar keeps it because its tree is read by organizations and agents that did not make it.

## What this rule does not claim
- It does not decide what kinds Memar's tree carries. Which kinds the path holds (placement, subject, role) and which the manifest holds is for the documents that own them: [Placements](../../../modularity/placements.md) for the placement labels, and the domain's own documents for the rest ([Label Handoff](../../label.handoff.md)).
- It does not forbid depth. A module may hold facets or parts, and a part below a module is a part of it because that module's document says so.
- It does not make the folder the only label of its content. A content has as many labels as are true of it ([Label](../../label.md#a-name-is-one-label)).
- It does not say how a name is written. That is [Documentation → File Naming](../../../documentation/documentation.md#file-naming).
