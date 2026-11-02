---
Title: "Protocol Rule — A Protocol Is Written in a `protocol/` Folder"
Labels: Draft
Start Date: 2026-10-31
ID: 497844
---
# Protocol Rule — A Protocol Is Written in a `protocol/` Folder
The owner's ruling of 2026-10-31, while designing the title module. It is the rule for where an abstraction is written, held for every module of every project built with Memar, and it applies [Protocol](../../protocol.md) to the file system: an abstraction is the code-level form of a protocol, and a protocol has one place to be read.

## The rule
- **Every abstraction is written in a `protocol/` folder.** No abstraction stands in a module's root, in `primitive/`, in `errors/`, or in a service's folder beside its realization. What realizes an abstraction stands elsewhere in the module; what states it stands in `protocol/`.
- **The module's main `protocol/` holds what the module as a whole states.** It is the one folder a reader opens to learn what the module requires, and it stays small: it holds the concepts of the module and nothing that belongs to a single service or widget.
- **Each service and each widget has a `protocol/` folder of its own** (`services/<name>/protocol/`, `widgets/<name>/protocol/`), holding the abstractions of that service or widget: what it takes and what it gives back. The main `protocol/` does not repeat them. [Title](../../../../../modules-plugable/uri/title/title.md) is the applied example.
- **A `protocol/` folder is one protocol surface of its owner, however many files it holds.** A service's `protocol/` is its owner's, not a second protocol of the module, and no `protocol/` stands inside another `protocol/`.
- **A `.kh` file in `protocol/` is named for the concept it states, with no `dt-` prefix.** The kind of a thing is a label it takes, never a prefix of its file name ([Label Rule → A Folder Is a Label](../../../label/rules/folder-label/folder-label.md)).
- **The label `protocol` is independent of the other kinds a content has.** One content may carry the label `protocol`, be a widget, and be a member of a module at once: the kinds combine and do not nest ([Label Rule → A Folder Is a Label](../../../label/rules/folder-label/folder-label.md#the-rule)).

## Why it exists
A module's contract is read first, and by an agent often only. When every service's types stand in one folder, the folder grows with the module and a reader must open all of it to learn about one service; when an abstraction stands in the root beside its realization, a reader cannot tell what a party is held to from what happens to be implemented. One `protocol/` per owner keeps each surface small and tells the reader at the path whose surface it is.

## What this rule does not claim
- It does not decide what a protocol is, or when a text is one: that is [Protocol](../../protocol.md).
- It does not forbid a service from using the main `protocol/`'s concepts; it forbids writing them again.
- It does not say how a file is named beyond the `dt-` prefix: that is [Documentation → File Naming](../../../../../modules-plugable/knowledge/documentation/documentation.md#file-naming).
