---
Title: "Label"
Status: Draft
Start Date: 2026-10-17
ID: 497843
---

# Label
## Abstract
A **label** is a word or phrase attached to a piece of content to identify or describe it. This module states what a label is for every project built with Memar, and it is the one place the rules for naming point to: a file name, a module name, a record's `Topic`, a session's task kind, a manifest's `labels` are all labels, and each rule that governs one of them cites this module for what a label is and does not restate it. Names are labels; identity is not. A content's identity is its [identifier](../../computer/identifier/), and a label is one of the ways a reader or a tool finds it.

## Dictionary
The senses of the word that this module uses, from a general dictionary (label, `['leɪbl]`):
- noun: a brief description given for purposes of identification; an identifying or descriptive marker that is attached to an object.
- verb: assign a label to, designate with a label; attach a tag or label to.

The other senses — a recording company's trade name, a radioactive isotope used to trace a reaction, to pronounce judgment on, to distinguish a molecule or element by a labeled atom — are not this module's.

## A name is one label
The name of a file or a module is a label that someone attached to content, and it has no special standing over other labels. Seeing a name as a label has three consequences:
- **More than one label may attach to one content.** A photograph can be labelled by what it shows — an animal in it — and by the state it evokes in a viewer, and neither label is the photograph's name or replaces the other. The same holds for a module: its name, its [placement](../modularity/placements.md), and the labels in its manifest each say something true of it.
- **A label describes; it does not identify.** Two contents may carry one label, and one content may lose a label without ceasing to be itself. Behaviour that must survive a rename is bound to identity and never to a label.
- **A label has an identifier, and its definition takes labels.** A word alone is no label: `design` as a topic and `design` as a task kind are two labels. So a label is written with its identifier, `design(01a14a04-6531-73d5-8eeb-6e37ddce016d)`, a UUID version 7 that sorts by the time it was made, and that identifier is what a search finds every record that took the label by. A label is defined once, in one place, and the definition takes labels of its own: `design` takes the label `TaskKind`, which is what makes it a task kind and is written in that definition, never beside the label in every record. A kind is therefore itself a label that other labels take, declared with the rule that makes a word of it valid; a closed kind lists its words in code, a free kind (`Topic`) defines a word when it is first used, in the project's own registry. A value of a field of its own is a label too: the values of Status are labels that take the label `Status`. A document that uses a label cites its definition ([A Fact in Code Is Written Once](../documentation/documentation.md#a-fact-in-code-is-written-once)).

## What belongs in a label
A label is chosen by the criteria of the term it encodes: it communicates meaning, keeps the concept's boundaries, avoids implementation vocabulary, and stays stable over time. A label that tells only where its content is stored, or which tool produced it, says nothing true about the content and goes stale when either changes.

## Taxonomy
[Taxonomy](https://en.wikipedia.org/wiki/Taxonomy) is a practice and science concerned with classification or categorization. Typically, there are two parts to it: the development of an underlying scheme of classes (a taxonomy) and the allocation of things to the classes (classification). Originally, taxonomy referred only to the classification of organisms on the basis of shared characteristics; today it also has a more general sense, the classification of things or concepts and the principles underlying such work, so a taxonomy can organize species, documents, videos or anything else.

Registries of what a particular word means live outside this module. This module keeps the attachment `(thing)-[:label]`. The registries are [law labels](../../../modules-plugable/rights/law/labels/labels.md), [thing labels](../../../modules-plugable/knowledge/thing-labels/thing-labels.md), and [account labels](../../../modules-plugable/economics/account/labels/labels.md). How a module's own labels classify it is classification's ([Label → Labels](./label.md#a-modules-labels)).

## Type
A label's type is itself a label: a record says what kind of thing it is by carrying the label that types it, and the words of that label live in the same registries as any other. `Scrum Board` is a label whose type is the `table` label; `text-type` types the labels that classify a text. This is the same statement as a kind being a label that other labels take ([A name is one label](#a-name-is-one-label)).

## Text
The text of a label is indicated in the [text](../text/text.md) domain. Nothing here carries the words of a label, so a label record here and its readable text are reached through two domains.

## A module's labels
A module is classified by its placement and by labels, and a module carries as many labels as are true of it: a label is attached to a module the way a name is attached to content, and no label replaces the placement. A module's labels are written in its manifest, `<module>.manifest.yaml` beside its main document, in a `labels` field:

```yaml
labels:
  - guest
```

A label is defined once, by the module that owns the claim it makes. The placement labels `kernel`, `pluggable` and `bundle`, and `guest`, are [Modularity's](../modularity/placements.md); a domain's own labels are the domain's, in its own registry. A label is added when a recurring claim about modules needs to be searched for, and a claim that is true of one module only is stated in that module's document. The manifest's other fields are not yet decided ([Open Questions](../modularity/placements.handoff.md#the-module-manifest-fields-beyond-labels)); `labels` is the one this module relies on.

## Where the rules for names live
- **A name in the file system** — the separators that divide category from topic, the words of a term and a companion record's facet — are the documentation module's rule, [File Naming](../documentation/documentation.md#file-naming), which applies this module's definition to documents.
- **A record's labels** — the `Labels` field of a documentation record and its kinds — are declared by [`primitive/label.py`](../documentation/primitive/label.py) and the types it serves.
- **A module's labels** — the `labels` field of its manifest — are classification's ([Label → Labels](./label.md#a-modules-labels)).

A rule for naming that stands anywhere else in the documents cites this module for what a label is, and the owner of that rule cites it back, so a reader of any of them reaches the same definition.

## Related artifacts
| Artifact | Relation | Action |
| --- | --- | --- |
| [Placements](../modularity/placements.md) | Reference — the labels a module carries | None (read) |
| [Documentation → File Naming](../documentation/documentation.md#file-naming) | Reference — the naming rule for documents | Cite this module for the definition of a label |
| [Text](../text/text.md) | Reference — where the words of a label are | None (read) |
| [Law labels](../../../modules-plugable/rights/law/labels/labels.md), [thing labels](../../../modules-plugable/knowledge/thing-labels/thing-labels.md), [account labels](../../../modules-plugable/economics/account/labels/labels.md) | Reference — the registries of what a word means | None (read) |
| [Knowledge](../knowledge.md) | Depends_on — the concept of knowledge this category belongs to | None (read) |
