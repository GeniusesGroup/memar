---
Title: "Memory Record"
Status: Draft
Start Date: 2026-10-23
ID: 497992
---

# Memory Record

## Abstract
The record capsule is the one way through which a domain, a service or an agent's verb reaches the nodes a project keeps in non-volatile memory. A node is named by an id and holds one value per domain, its parts; a node may carry labels, and a label is an id attached to it so that nodes can be found by it. It is laid over any store that realizes the [store contract](../../../../../modules/computer/memory/store/store.md#the-contract) and knows ids and batches and nothing about how a medium keeps them: windows, branches, folders, packs and paths belong to the adapter that serves a class of nodes, an adapter is a pluggable module, and which adapter serves which class is the project's choice, made once in the `memar:` block of its manifest and never in a service. Whether an adapter conforms is decided by one contract suite, run against every adapter.

The capsule is Khayyam: [`protocol/record.kh`](protocol/record.kh) and the `record-*.kh` files beside it declare the operations, the id, the domain key, the part, the labels, the class, the answers and the needs, each type's human-facing text in its `*.eng.kh`; its refusals are in [`errors/errors.kh`](errors/errors.kh). [`record.py`](record.py) realizes them. This document holds what they cannot.

Correction of 2026-10-24, from the owner's rulings: this document was first written as if the record were the one abstraction of retention. It is not. The contract (an address, `get`, `list`, the atomic `batch` under expectations, `state` and `changes`, the guarantees, the capabilities and the suite) belongs to the memory module and is realized by every capsule; `record` is one such capsule, pluggable, whose address is a 16-byte id followed by the bytes of a domain key, and which adds the node, the part and the label. The token (the SHA-256 of a value) stays in the contract, so an adapter that knows addresses only can serve it. Those statements moved to [Memory Store](../../../../../modules/computer/memory/store/store.md) and [Memory Conformance](../../../../../modules/computer/memory/conformance/conformance.md) on 2026-10-26; what stays here is what `record` adds, and it is Tentative where it conflicts with them. On 2026-10-26 the first design's `list` of ids became `nodes`.

## Introduction

### Motivation
A service that reaches its records through a folder, a version-control command or a database call carries what that medium costs and what it can lose. Work records kept as files in the working tree are scanned by antivirus software at every create and edit, are lost by a stash or a branch switch, and can be edited by any tool; a second store would repeat each of those with its own exceptions in the services. One port with the adapter chosen outside the services removes the exceptions, lets the medium change without a service changing, and makes a claim about the medium (atomic, durable, not in the working tree) a claim a test can decide.

## Explanation

### Definition
The types are Khayyam ([`record-id.kh`](protocol/record-id.kh), [`record-domain-key.kh`](protocol/record-domain-key.kh), [`record-part.kh`](protocol/record-part.kh), [`record-labels.kh`](protocol/record-labels.kh), [`record-class.kh`](protocol/record-class.kh)); what they are for is this.
- **Node.** A thing a project keeps, named by an id; it is a record in the sense of the memory module's Record model, and this document says node for a record together with its parts and labels. A node exists once it has a part, and it is not a file, a row or a record: how an adapter shows it is the adapter's.
- **Id.** A UUID version 7, the form [Label](../../../../../modules/knowledge/label/label.md#a-name-is-one-label) already gives its identifiers; what the capsule requires of it is [`record-id.eng.kh`](protocol/record-id.eng.kh). Its order is what lets an adapter's shards follow time without reading the id. Whoever names a node mints its id, and a collision is caught by writing the first part with an expectation that the part is absent. An id names no class: a caller that holds an id knows its class from where it got it, and a reference from a node of one class to a node of another carries the class name beside the id.
- **Domain key.** The name under which a domain keeps its part on a node ([`record-domain-key.eng.kh`](protocol/record-domain-key.eng.kh)), issued by the domain's own module in code, so that the capsule knows no domain.
- **Part.** The value that one domain keeps on one node ([`record-part.eng.kh`](protocol/record-part.eng.kh)). Its encoding is its domain's, and canonical because the token is taken over the bytes.
- **Token.** The contract's ([Memory Store](../../../../../modules/computer/memory/store/store.md#the-contract)). It is not an order: a value that returns to an earlier value returns to its token.
- **Label.** An id attached to a node ([`record-labels.eng.kh`](protocol/record-labels.eng.kh)). What a label means is its own domain's ([Label](../../../../../modules/knowledge/label/label.md)): the capsule treats it as an id, so any id a writer attaches, such as the id of another node, serves to find the nodes that carry it, and the choice of what to attach is the writer's.
- **Class.** A name a composition gives to the nodes one group of services reads and writes, so that one adapter serves them all. A node belongs to exactly one class, hence to one store, and a batch never spans two.

### The operations
The operations and their answers are [`protocol/record.kh`](protocol/record.kh) and the files it names (`record-parts.kh`, `record-nodes.kh`, `record-nodes-query.kh`, `record-scan-query.kh`, `record-unmet.kh`), and what is refused is [`errors/errors.kh`](errors/errors.kh). `record` is itself a store of the contract whose address is a key ([`record-key.eng.kh`](protocol/record-key.eng.kh)), so the contract's operations are its operations over keys, and what it adds is [`record.eng.kh`](protocol/record.eng.kh). `put` is a batch of one write and adds no semantics of its own. The first design called `nodes` `list`; the contract's `list` answers keys and keeps the name. Paging ([`record-scan-query.eng.kh`](protocol/record-scan-query.eng.kh)) is why a consumer can poll `scan` instead of subscribing.

### What every adapter guarantees
The guarantees are the contract's ([Memory Store → The contract](../../../../../modules/computer/memory/store/store.md#the-contract)); `record` reads them for nodes, and adds the reason for two.
- **Atomic and isolated.** A node's parts and labels written by one batch are seen together by every read.
- **One place orders the writes.** A held range is a range of existence instants; because the writer mints the id, an adapter with a shared store also holds every instant after the last range a fetch gave it, where new ids are minted, and decides an `absent` expectation there alone.
- **Nothing is removed.** No operation removes a part, a label or a node, though a medium others can change, such as files, may lose one; what a domain shows is its own matter, and no service offers erasure until the owner rules.
- **Derived structures are rebuildable and never stale.** The index that answers `nodes` and `scan` ([`record-index.eng.kh`](protocol/record-index.eng.kh)) is kept in the memory of the process and never in the store's medium, so a batch committed by another handle or process shows in the next `scan` and dropping it costs one rebuild and changes no answer.

### Capabilities and limits
They are the contract's. A record of state changes spans keys, so a class that keeps one needs an atomic batch when it is opened ([`record-needs.eng.kh`](protocol/record-needs.eng.kh)).

### What the port does not know
It does not know how a medium keeps nodes: no window, branch, reference, folder, pack, object, path, file name or fan-out is part of its contract, and the rule that places a node in a window is the git adapter's private detail: since 2026-10-24 the adapter knows addresses only and shards by a fixed-length prefix of the address, which for this capsule's ids is a window of time, so the adapter reads no id. It does not know what a value encodes, what a domain key or a label means, which class a node belongs to, who wrote, or what a node's history was. It enforces no access: whoever can run an adapter on a store can read and write it, and who may do what is the authorization above it, so `nodes` and `scan` hide nothing. It stamps no time on a write and mints no id, and it accepts a node whose id has any existence instant, so a node named long before it is first written lands where its id says. History is the Request chain ([Request → Recording a change of state](../../../../../modules/computer/request/request.md#recording-a-change-of-state)), and a domain that wants an old value reads it there.

### Placement
[Kernel Neutrality](../../../../../modules/knowledge/modularity/rules/kernel-neutrality/kernel-neutrality.md#the-rule) puts to each part of this design the question whether a second organization could choose it otherwise without the subject meaning something else.
- The atomic batch under expectations, the difference between Absent and Unavailable, and the guarantees are the subject of the memory module, and stay in it as its contract (`modules/computer/memory/store/`). The nodes, ids, parts, labels and tokens are this capsule's: they are a form of address and of value, and a second organization could take another form (an id of another kind, no labels) without a store meaning something else. Other kernel modules that refer to a node (Task, timeline, Request) refer to an address through the memory contract and depend on nothing here, so the capsule is pluggable and stands at `modules-plugable/computer/memory/store/record/` (owner's rulings of 2026-10-24).
- The contract suite is the decision procedure of the contract and stays with it in the memory module; the cases that name ids, parts or labels are this capsule's.
- The media and their mechanics, git branches, the shard rule, packs, folders, a reference in memory, are choices. Each adapter is a pluggable module attached to this contract ([Pluggable → Operational rules](../../../../../modules/knowledge/modularity/labels/pluggable.md#operational-rules)), and carries its capability's name. `git` and `files` are modules of their own at `modules-plugable/computer/memory/`, they realize the memory contract and know nothing of this capsule, and this capsule is laid over whichever store a class is bound to (2026-10-24). Neither redoes the existing `git` and `filesystem` modules: each realizes the contract over a medium those modules already serve. `git` keeps work records and uses git plumbing only; `files` stands for a project's source tree until the editing surfaces that replace it exist. Because `files` and `git` know no label, a path is a thing this capsule's caller attaches (a label of a node), not something `files` keeps. The reference adapter that keeps nodes in the process, `volatile`, is the model the suite compares others with, so it is part of the decision procedure and sits in the memory module beside the suite, address-generic. The view is a consumer of this capsule and a pluggable module of its own, [Memory View](../view/view.md).
- Which adapter serves which class is a choice of the project and sits in its preferences, below. The name of a class is its services' own, and a project binds the name it finds.
- The limits and the capabilities are values the subject requires, so they are parameters and a class states what it needs of them; no adapter and no port document fixes a floor.
- Every dependence runs toward the foundation: the capsule depends on the identifier it reads and on nothing under `modules-plugable/` or `bundles/`, and each adapter's tests run the suite on `record` laid over it, so the adapter depends on the foundation and never the reverse; the module-graph test fails any import that runs the other way ([Kernel Neutrality → How a check runs](../../../../../modules/knowledge/modularity/rules/kernel-neutrality/kernel-neutrality.md#how-a-check-runs)).

### The Go-era Record model this contract replaces
The record folder holds a draft written for a database node: `Records` (named `Record_Model` before 2026-10-25) with `Get`, `Save`, `Read`, `Write`, `Append`, `Prepend`, `Extend`, `Lock`, `Unlock`, `Delete`, `Erase` and a count, a 16-byte `RecordUUID`, and versions. This contract is that model made decidable, and it stands where the draft stood so that the memory module has one record abstraction and no second. Each operation of the draft has a place in it, or a stated absence:
- `Get`, `Save` and `Read` are `get` and `batch`; the count and the listing are `nodes` and `scan`.
- `Lock` and `Unlock`, which reach strict consistency by holding a record, are the expectations of a batch: a writer reads a token and writes under it, and no lock outlives a process. The owner ruled on 2026-10-25 that they are an optional capability `lockable` of a store, outside the core operations.
- `Write` at an offset, `Append`, `Prepend` and `Extend` are not offered. The draft itself advises saving a large record in several small ones, and a part is replaced whole; a larger value is several parts or several nodes.
- `Delete` and `Erase` are the erasure question the contract leaves open: the draft distinguishes making a record invisible from zeroing its place, and the owner's ruling on retention and erasure chooses between them.
- The versions of one record are not a property of this contract: the history of a value is the chain of its Requests ([Request → Recording a change of state](../../../../../modules/computer/request/request.md#recording-a-change-of-state)).
- The draft's id was a 16-byte hash of the data, so that a collision is improbable; this contract's id is a UUID version 7 so that `nodes` can order by time, and a content hash may fill the random bits of one when a node is content-addressed.
- Ranged `Read` and `Length` are not offered: a part is read whole, and a size is the domain's field when it needs one. The subscriptions are not offered: a consumer polls `scan`, and a change feed is a later capability recorded in the handoff. The draft's per-object metadata is not kept: the media type is in the `content` part. The record's own request identity and time are the Request's. Broadcast replication on save is outside, since one writer location orders the writes.

The draft's Go-era declarations in `protocol/` (`model.kh`, `save-options.kh`, `data_model.kh`) and `services/` still stand beside the Khayyam of this contract and are the owner's to replace or delete; the open question is recorded in [Memory Store Handoff](../../../../../modules/computer/memory/store/store.handoff.md). A declaration other modules import (`uuid.kh`, `uuid.observers.kh`, `data.kh`) stays and is repointed, so that the folder holds one record abstraction.

### Binding adapters to classes
A project says which adapter serves which class in the `memar:` block of its `manifest.yaml`, the block the tools read and no agent loads, in the key `memory`, whose form is [`record-binding.eng.kh`](protocol/record-binding.eng.kh), declared once in [project preferences](../../../../../modules/computer/software/edges/manifest/services/preferences.py). The example is illustrative; the class names are the composition's, and Memar's own choice is written in its manifest and nowhere else.

```
memar:
  memory: work-records=git-store, sources=files
```

- **A service asks for a class, never for an adapter.** The one function that opens it is [`memory-open.eng.kh`](../../../../../bundles/memar/services/memory/memory-open.eng.kh), in the entry point of Memar's tooling, [`bundles/memar/memar`](../../../../../bundles/memar/memar), because a bundle may import pluggable modules and a kernel module may not. So a kernel module imports no adapter and no bundle, and no service holds a branch for a class or an adapter. The binder, the bindings and the needs are [`record-binder.eng.kh`](protocol/record-binder.eng.kh), [`record-binding.eng.kh`](protocol/record-binding.eng.kh) and [`record-needs.eng.kh`](protocol/record-needs.eng.kh).
- **A group of services names its class.** The task verbs name the class of the work records they keep, in their own module, and the capsule fixes no name. A class the key does not name is refused when it is opened; the capsule has no default adapter, because a default would be a choice the kernel makes.
- **A class states what it needs.** The service that opens a class says whether it records state changes, which needs an atomic batch, and the limits it uses; opening it on an adapter that declares less is refused when the class is opened.
- **An adapter's own parameters** are keys of the same block named after the adapter and declared by the adapter's module; the capsule declares none.
- **Two adapters never write one store.** A node's class decides its store, and a class has one adapter.

### The contract suite
The cases that name no id, part or label are the contract's, in [Memory Conformance](../../../../../modules/computer/memory/conformance/conformance.md), which says which moved and why. `record`'s own cases, those that name an id, a part or a label, are code too, in [`tests/record.py`](tests/record.py), with the halves of the contract's cases that stayed here under the contract case's name; each holds for `record` over any store, and an adapter's own tests run them on `record` laid over it.

The contract's suite makes its addresses from the store's parameters alone, and an address it makes is not a key, so it reaches `record` through a translation in the tests that keeps equality and the byte order; every call still goes through `record` and its checks. The cross-process cases run only on a store declaring that it is shared between processes, and run on `record` laid over [`git-store`](../git-store/git-store.md) in that adapter's tests.

### The view
A read-only folder built from a class's committed state, for a person's editor, is a consumer of the capsule and is specified in [Memory View](../view/view.md). The capsule offers it nothing beyond `get`, `parts`, `nodes` and `scan`.

### Adapters state themselves
What an adapter's document states is the contract's ([Memory Store → The contract](../../../../../modules/computer/memory/store/store.md#the-contract)). For `record`, the 30-day window of the first design is a parameter of `git-store` for a class of ids of version 7, a prefix of the address, not a rule of the contract.
