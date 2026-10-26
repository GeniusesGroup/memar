---
Title: "Key-Value"
Status: Draft
Start Date: 2026-10-24
ID: 498037
---

# Key-Value

## Abstract
A key-value store is a capsule that realizes the memory contract ([Memory Store → The contract](../../../../../modules/computer/memory/store/store.md#the-contract)) for one kind of address: a byte string of variable length, listed in byte order. It adds no abstraction to the contract and no operation: it reads with `get` and `list`, writes only by the atomic `batch` under expectations, and states what a key, its limits and its engine are. It is not a record store: its key is not a fixed-length id, it lists keys, and keeping it in records would cost a hash of the key and the whole pair in a record's data; so its engine is its own and rests on `page`, a store of fixed-size positions that the contract describes as dense. The engine is a copy-on-write B+tree whose commit is the write of one meta page after the pages it points to are flushed; a root is a committed state, the snapshot a reader holds and the token that `state` answers. Uniqueness is a committed key written under an `absent` expectation. The Go-era `Model` is carried onto the contract: `Get` is `get`, `ListKeys` is `list`, `Set` is a write of a batch, `Lock` and `Unlock` are expectations of a batch, `Delete` and `Erase` wait for the erasure rule, and the key count and the value length are not offered.

## Introduction

### Motivation
Every kind of store that a project needs ordered, sparse, variable-length keys for (a name table, a set of unique values, the adjacency of a graph) would otherwise write its own engine or borrow a foreign one with its own durability story. One capsule that answers the contract's questions for such keys once, and that is decided by the same suite as every other capsule, removes that repetition and keeps the concern's data in one location ([Memory → The memory/storage dichotomy rejected](../../../../../modules/computer/memory/memory.md#the-memorystorage-dichotomy-rejected)).

### Methodology
The design is derived from the contract's guarantees and from the Go-era `Model` the module held; the engines named under [Prior art](#prior-art) are consulted for the cost of each structure and are not authorities. Where this document and [Memory](../../../../../modules/computer/memory/memory.md) differ on the contract, the memory module governs, and this document states only what the capsule adds to it.

## Explanation

### Definition
- **Key.** A byte string of 0 to `max_key_bytes` bytes, compared as unsigned bytes with the shorter of two strings that share a prefix first. The empty string is a key, the lowest. A key is the address of the contract, and a key outside the length range is Refused in every operation that takes one, `get`, `list` bounds and expectations included.
- **Value.** A byte string of any length including none, up to `max_value_bytes`. An empty value is a value and differs from an absent one. Its encoding is its writer's.
- **Instantiation of the contract.** Sparse, any value length, and an atomic compare-and-write of one address; every read of a key it does not hold answers Absent, since the store has one writer location and holds every key.
- **Sizes.** A leaf holds at least four entries, an entry being a key with its inline value or with the position of the first overflow page of its value. The key plus the inline value, or the key plus the overflow position, is at most a quarter of a leaf, so a value is inline only while it fits in what a quarter of a leaf leaves after its key. `max_key_bytes` is therefore at most a quarter of a leaf less the overflow position, and an instance whose page size leaves it under 255 bytes is refused at its opening.

### What the Go-era Model becomes
The commented `Model` of `protocol/` is replaced by the contract; each operation has a place or a stated absence.
- `Get` is `get`. `Set` is a write in a `batch`; `put` is a batch of one write and adds no semantics.
- `ListKeys(offset, limit)` is `list`, paged by `after` and not by offset, since an offset moves when a key is written between two pages. A prefix is listed by `from` the prefix and `to` its successor: strip the trailing 0xFF bytes of the prefix and raise the last byte left, with no `to` when none is left.
- `Lock(key)` and `Unlock(key, value)` are expectations. A writer reads a value and its token and writes under an expectation on the token; no lock outlives a process, and a holder that dies leaves nothing to release.
- `Batch` is `batch`, which the draft left commented.
- `KeyNumbers` is not offered. A count that costs less than a listing needs a tree whose every node carries a count, which makes every write pay for it; a consumer that needs one counts a listing or keeps its own count as a key written in the same batch.
- `Length(key)` is not offered, as a choice: the leaf could answer it, but a value is read whole through the contract and a size a consumer needs is that consumer's field, so the contract carries one read less.
- `Delete` and `Erase` are the erasure question the contract leaves open ([Memory Handoff](../../../../../modules/computer/memory/memory.handoff.md#what-is-the-retention-and-erasure-rule-for-preserved-history-and-where-do-a-records-versions-live)): the draft distinguishes making a key invisible by removing it from the primary index from zeroing the place of its value, and the owner's ruling on erasure chooses between them or neither. No verb removes a key until then, and the pages the engine reclaims below are not erasure.
- The draft's comment that encryption is implemented at the level of the block store is kept as the rule it states: the capsule encrypts nothing, and a project that needs it chooses a page store beneath that does.
- No read of this capsule's own is added to the contract's. A range of keys with their values from one state is the state-checked `list` followed by `get`; whether the contract offers that as a derived read is asked in [Key-Value Handoff](key_value.handoff.md).

### The engine on `page`
The engine is a copy-on-write B+tree over a store of fixed-size positions, which is what `page` is read as an instance of the contract: dense, a fixed value size, and an order. It depends on that instance and on nothing of `block`; which of the two is the foundation changes the size of the unit and not the engine, provided the store beneath declares what the engine needs.
- **What it needs of the store beneath, checked when it opens.** `Flush` as a barrier: every write made before it is on the medium before any write made after it; whether a write of one page can tear, which the engine assumes it can; and growth, a write at the position after the last one, which extends the store. A store that declares less is refused when it is opened, as record.md states for a class. Survival of the loss of power is claimed by this capsule only where the store beneath declares the three; the contract's `durable` covers the end of the process alone.
- **What it allocates.** Pages of six kinds: two meta pages at the first two positions, interior pages, leaf pages, overflow pages, free-list pages, and log pages. A page carries a checksum of its own bytes, which a read verifies. Positions come from the free list, and when it is empty from the end.
- **The tree.** An interior page holds keys that divide its children and the positions of the children; a leaf holds entries in key order. A page is split when full and merged or rebalanced when it falls under a third. The height is the same for every leaf.
- **What it reads.** A read starts at the root that a meta page names and follows positions down; nothing the read reaches changes while the reader holds that root. `list` is an ordered walk in either direction and a point read is one path. A reader holds a root for the length of one call, or of one walk that the engine's own API keeps open and ends.
- **What it writes.** A batch is applied by copying each page on the path from a leaf to the root, writing the copies at positions taken from the free list or from the end, and never writing a position that the latest root or a reader reaches. Expectations are decided by the engine, which holds every key, so the medium is asked to compare nothing. One process opens the store for writing: opening takes an exclusion that the medium releases with the process, so a killed writer leaves nothing a new one waits for.
- **The commit.** The new tree pages, the free list as copied for this batch, and the page of the log that records the keys this batch wrote are written and flushed; then one meta page is written with the root, the head of the free list, the head of the log, a transaction number counted up by one and a checksum, and flushed. There are two meta pages, written in turn; on opening, the engine takes the valid one with the higher number, and a meta page torn by a failure is invalid by its checksum and the other stands. A batch is therefore all there or all absent, and the tree, the free list and the log are always at one transaction.
- **The free list.** It is copy-on-write like the tree: a commit never writes a free-list page that the latest meta reaches. A page the batch supersedes is recorded in the new free list as pending under the batch's transaction number, and becomes free for reuse only when no reader holds a state older than that number. A position is taken only if it is free, not superseded by the batch in progress, and not reachable from the latest root or any reader's root.
- **Recovery.** Positions taken by a batch that did not commit belong to no meta page, so on opening the engine rebuilds the free list by one walk from the root: a position that is neither reachable nor in the surviving free list is added to it. No page is lost to a crash.
- **A failed commit.** A write or a flush of the meta page that errors leaves its durability unknown. The engine does not answer the batch until it has made the outcome known: it writes a valid meta page with a higher number that names the previous root, over the other slot, and flushes it; if it cannot, it refuses further writes until it is opened again, and the batch is answered Unavailable with the reason Failed only then. The next opening reads whichever meta stands.
- **Changes.** Each commit adds, in the log, the keys the batch wrote under its transaction number. `changes(since)` reads the log and does not depend on whether superseded tree pages exist. The log is trimmed to a horizon the instance declares, a count of transactions. What the contract answers for a token beyond the horizon, and whether `changes` returns the token it answers up to, is asked in [Key-Value Handoff](key_value.handoff.md), since every adapter with a bounded history meets it.
- **Limits that follow.** The copy of a whole path for each batch is paid by every batch; a reader that holds a root for long keeps the pages it reaches from reuse, so the store grows while it holds; one process writes at a time; and a key is bounded as the sizes above say.

#### Why a tree and not a log-structured merge tree
- The contract asks for a batch atomic and isolated, reads that are linear, an ordered `list` with `after` in both directions, and a token of the committed state. An immutable root is each of those without a mechanism beside it: it is the snapshot, the order and the token.
- A log-structured tree answers an `absent` expectation, which uniqueness needs, by a lookup across its levels guarded by filters, and it keeps a compaction running behind the writes, whose cost in space and time is paid at moments no batch names and which a reader of a state must be held clear of. The tree pays the same kind of cost in reclaiming pages, but at the commit and bounded by the batch.
- Both structures write out of place, which suits a medium that cannot rewrite a page without reading it first ([Page](../page/protocol/page.kh)), so the medium does not decide.
- Considered and not taken, a log-structured design for a write-heavy class: a class whose writes outrun the tree's path copying is a capsule of its own over the same contract, chosen by the project, and does not change this one.

### Uniqueness
A key is unique in the store by being the address. A value that must be unique across keys, a name or an external id, is a key of its own that the consumer names, with a prefix the consumer owns, written in the same batch as the pair it protects: `batch(expect: absent(<unique key>), absent(<key>) or the token read for <key>, write: put(<unique key>, owner), put(<key>, <value>))`. The batch commits for the first writer and conflicts for the second, which names the expectation; the expectation on `<key>` keeps a concurrent change of that key from leaving a claim behind. The constraint is a key of this store that the contract's atomic batch checks, and no index that is never committed ([Memory Handoff → Is `services/batch.kh` superseded by the contract's batch?](../../../../../modules/computer/memory/memory.handoff.md#is-servicesbatchkh-superseded-by-the-contracts-batch)).
- A value longer than `max_key_bytes` less the prefix is hashed by the consumer, which accepts the collision a hash carries or keeps the value itself as an overflow check.
- A claim is released only by a write, since nothing is removed: the consumer writes a tombstone value under the unique key and the next claimant expects its token and not absent. What a tombstone means is the consumer's, and the capsule does not know it.

### Capabilities and limits
The instance declares: `atomic_batch` true, since the commit is one meta page; `durable` and the survival of the loss of power as the store beneath declares what the engine needs of it; `shared_between_processes` false; `fallback` false; `leaves_working_tree_untouched` as the store beneath declares it. The limits: `max_key_bytes`, `max_value_bytes`, writes per batch and bytes per batch, the last two bounded by the pages the store can take at the commit, and the horizon of the log. `stats` as the contract names them.

### The contract suite for keys
The core cases of the contract run against this capsule in their sparse, any-length form. The cases below are the capsule's own: they name keys or the engine, are specified here and written as tests by the build task, each carrying `owed:memory.key-value.suite` until then. The engine's cases need a page store with a seam that tears a write and discards or reorders the writes made since the last flush at a simulated crash, and that pauses a read between two page reads; the build task writes it beside the engine.

Owed: memory.key-value.suite

Core, for every instance:
- `key-order-bytewise`: keys that share prefixes, hold 0x00 and 0xFF bytes, differ in length and include the empty key come back in unsigned byte order, the shorter prefix first.
- `key-length-limits`: keys of 0 bytes and of `max_key_bytes` are accepted; one byte over is Refused in `get`, a bound, an expectation and a write.
- `value-any-length`: values of 0, 1, what a quarter of a leaf leaves after the key, one byte more, a page, many pages and `max_value_bytes` come back identical; one byte over is Refused as TooLarge.
- `prefix-successor`: a prefix is listed by its successor, including prefixes that end in one or more 0xFF bytes and one that is all 0xFF.
- `unique-key-by-absent`: two writers each write the same unique key and a pair under an `absent` expectation; exactly one commits and the other conflicts naming it; a writer that changes the pair's key between a reader's read and its batch leaves no claim behind; a tombstoned claim is taken by a writer that expects its token.
- `batch-across-many-leaves`: a batch whose keys split and merge many pages commits whole, and a batch whose last expectation fails leaves every key and the tree as they were.
- `no-page-lost`: after random batches every page is on the free list or reachable from the latest root, and none is both.
- `reader-snapshot-survives`: a reader paused between two page reads sees its state unchanged over 10,000 later commits, none of its pages is reused before it ends, and the store grows while it is held.
- `reclaim-bounds-the-store`: with no reader held, overwriting the same keys 100,000 times keeps the store's size within a stated multiple of the live data.
- `log-trims-at-the-horizon`: the log holds the declared count of transactions and no more, and what `changes` answers inside it is exactly the keys written.
- `second-writer-refused`: a second process that opens the store for writing is refused, and after the first is killed a new one opens without waiting.
- `store-needs-checked`: a page store that does not declare `Flush` as a barrier, or growth, is refused when it is opened.

Durable, for an instance whose store declares what the engine needs:
- `torn-meta-takes-the-other`: a newer meta page torn by the seam is not taken, the engine opens the previous state, and every batch reported committed before it is present.
- `flush-order-holds`: a crash between the flush of the pages and the write of the meta page, and one that discards the unflushed writes, leave the previous state whole.
- `crash-loses-no-page-and-no-log`: after a killed writer, opening rebuilds the free list so that `no-page-lost` holds, and the tree, the free list and the log are at one transaction.
- `failed-meta-flush-settles`: a meta write or flush made to error is not answered until the previous root is named by a valid meta page or writes are refused; the next opening reads a state that is whole and equals the one answered.

The durable group of the contract runs as well. The model case runs with the reference adapter `volatile` as a sparse store.

### Where it stands
It is pluggable: a second organization could take no ordered store, or another structure, without a store meaning something else. It stands at `modules-plugable/computer/memory/store/key_value/`, a path parallel to the memory module's, once the moves of the memory module are done, and its document, its handoff and its changelog move with it ([Memory Store → What stands where](../../../../../modules/computer/memory/store/store.md#what-stands-where)). It rests on the contract, and through `page` on a store of fixed-size positions; it knows nothing of `record`. Its protocol declares the key and value types and the limits; the operations of the contract are not restated there.

### Prior art
- [Pebble](https://github.com/cockroachdb/pebble) -- Go, log-structured
- [redb](https://github.com/cberner/redb) -- Rust, copy-on-write B-tree
- [lmdb](https://github.com/LMDB/lmdb) -- C, copy-on-write B+tree with two meta pages and a reader table
- [sled](https://github.com/spacejam/sled) -- Rust
- [fjall](https://github.com/fjall-rs/fjall) -- Rust, log-structured
- [LevelDB](https://github.com/google/leveldb) -- C++, log-structured
- [RocksDB](https://github.com/facebook/rocksdb) -- C++, log-structured
- [Berkeley DB (BDB)](https://en.wikipedia.org/wiki/Berkeley_DB) -- C

A [key-value database](https://en.wikipedia.org/wiki/Key%E2%80%93value_database) is a data storage paradigm for storing, retrieving and managing associative arrays, dictionaries or hash tables, whose records are stored and retrieved by a key that identifies them. Here the paradigm is a capsule of the contract and not a paradigm of its own.
