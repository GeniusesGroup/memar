---
Title: "Memory Git Store"
Status: Draft
Start Date: 2026-10-26
ID: 498066
---

# Memory Git Store

## Abstract
`git-store` is an adapter of the [store contract](../../../../../modules/computer/memory/store/store.md#the-contract) that keeps a store in a reference of a git object database and nothing else: no worktree, no index, no file in the project's working tree. It knows addresses only. A store is one reference, `refs/memory/<class>` by default; its state is the commit the reference points to, one commit for each committed batch; a batch is written as one pack by a long-lived `fast-import` and made visible by one compare-and-swap of the reference; reads go through one long-lived `cat-file`. When a class names a shared store, every committed batch is published to it soon after it commits, and the adapter knows after a restart how far the shared store lags. It is the first, replaceable medium of the work records: the owner ruled that git is a sink to be left, so the adapter uses plumbing only and builds nothing that would outlive it. The code is [`git-store.py`](git-store.py); the groups it owes are [`cases.py`](cases.py); its tests are [`tests/git-store.py`](tests/git-store.py); what it costs, measured against today's files under git, is [Research 001](git-store.research.001.md), and its procedure [`services/_benchmark.py`](services/_benchmark.py).

## Explanation

### What it declares
The capabilities, the parameters and the limits are code, in `GitStore` of [`git-store.py`](git-store.py), and their meanings are the contract's ([`protocol/store.py`](../../../../../modules/computer/memory/store/protocol/store.py)). In words: a sparse store of addresses and values of any length that can compare and write; atomic, durable, shared between the processes of one machine, asking a fallback for what it does not hold, leaving the working tree untouched; and replicated when, and only when, the class names a shared store. It declares no limit, and it is not `lockable`: the expectation is the control of writers. `stats` counts every git process it starts and every file it opens itself (the index file, the writer's lock); git's own files are git's.

### The first configuration: one reference per class
A class is kept in one reference, named by the key `git-store-reference` (`class=reference` pairs, `refs/memory/<class>` when the class is not named), fetched only by an explicit refspec and never checked out. A batch therefore touches one reference, and its atomicity is one compare-and-swap. With several references, a batch that touched two would not be atomic against a kill, because git's files backend renames each reference's lock on its own; the case `kill-during-batch-is-atomic` decides that, and it is why a split into windows of the address, the later configuration the change plan names, is a migration by address that keeps one reference per batch rather than a batch across two.

Inside the reference's tree, an address is written under a fixed-length prefix of itself: its first three bytes, each a folder of two hexadecimal digits (`__` for a byte the address does not have), then a file named by the whole address in hexadecimal (`_` for the empty address). For an id of version 7 the three bytes are a span of about 35 years, 50 days and 4.7 hours, so no tree is flat and a commit rewrites a few small trees. The rule is private: no answer shows it, and changing it is a migration of one reference.

### The plumbing it uses
Only what the owner's ruling allows ([Memory Store → The contract](../../../../../modules/computer/memory/store/store.md#the-contract), "Adapters state themselves"), and nothing that needs a worktree or an index:
- one long-lived `cat-file --batch-command`, which answers the reference's tip and the bytes of every blob a `get` or an expectation reads, so a `get` of any number of addresses starts no process;
- one long-lived `fast-import`, which writes a batch's blobs, trees and commit, with the previous tip as the commit's parent, into one pack at a `checkpoint`; it writes no reference, since the branch it commits on is reset before the checkpoint, and it answers the commit's id by `get-mark`;
- one long-lived `update-ref --stdin`, which moves the reference from the previous tip to the new commit in one transaction (`start`, `update` with the old value, `commit`): the compare-and-swap;
- `diff-tree`, which answers `changes` and brings the derived index up to date between two tips;
- `repack -d --geometric=2`, run when the store's packs pass a bound, so that one pack per batch does not grow into a pack per batch forever;
- `push` with an explicit refspec and never forced, to publish, and `update-ref` to record what the shared store acknowledged;
- `rev-parse`, once when a store is opened, to find the object database and its hash.

`hash-object`, `mktree` and `commit-tree` are not needed: `fast-import` writes the same objects into one pack instead of one file each, which is the reason the change plan chose it (C7). A commit is still one commit per batch, as [Memory Record Handoff → Decisions](../record/record.handoff.md#decisions) decides ("A reference points to a commit per batch").

### Writers, and a lock a killed writer left
Every writer of a store on a machine goes through the adapter, and the adapter orders them by one lock per store: a file `memar-git-store/<reference>.writer` in git's own directory, held by the operating system's lock on an open file (`LockFileEx` through `msvcrt.locking` on Windows, `flock` elsewhere), which the operating system releases when the process ends, however it ends. A writer holds it from reading the tip to the end of the compare-and-swap; a writer paused at the commit point holds it, and a second writer waits and then decides its expectations on the state the first left.

git's own `<reference>.lock`, which `update-ref` makes for the instant of the swap, carries no owner. A writer that holds the store's lock and finds a `<reference>.lock` knows that no live writer of the adapter made it: it was left by a writer killed during the swap, or is held for an instant by a git process outside the adapter. So a `<reference>.lock` older than two seconds is removed and the swap is tried again; a younger one is waited for. A batch whose swap cannot be decided is answered Unavailable with the reason Failed only once its commit can no longer become the tip: the writer holds the store's lock and the tip is not its commit. A writer killed before the swap leaves at most a pack nothing reaches, which `repack` and git's pruning collect.

### What it keeps outside the store's medium
- **The index**, a derived structure: for each held address, the id of its blob, in byte order. It answers `list` and the addresses of `get`, records the tip it reflects, and is brought up to date before it answers, by `diff-tree` from its tip to the reference's, or from the empty tree when its tip is unknown. It lives in the memory of the process, shared by the handles of one store, and is saved, as a cache another process may start from, in the user's data area: `%LOCALAPPDATA%\Memar\git-store\` on Windows, `$XDG_DATA_HOME/memar/git-store/` or `~/.local/share/memar/git-store/` elsewhere, one file per object database and reference. Its own batches are applied to it in the step that commits them; any other tip invalidates the part since. Dropping it deletes both, and changes no answer. It serves address ranges only: it holds no label and reads no address.
- **Nothing else.** The writer's lock is in git's directory, and the reference that records what the shared store acknowledged is a reference of the same object database (below).

### The fallback
A store holds the ranges of addresses it decides alone; an address outside them is asked of a fallback, through `get` and `list`, as fresh as the asking, and what it answers is never written into the store ([Memory Store → The contract](../../../../../modules/computer/memory/store/store.md#the-contract), "One place orders the writes"). The fallback is an interface, `Fallback` in [`git-store.py`](git-store.py), and its one implementation, `NotFound`, answers that nothing is there. Until a fetch of part of a shared store exists, a store holds every address, so the fallback is reached only through the seam of the `fallback` group, which sets the held ranges and a fallback that holds given addresses or cannot be reached.

### Publishing to the shared store
A class names its shared store by the key `git-store-shared` (`class=remote` pairs, a remote's name or a URL); a class it does not name has none, and its store is not `replicated`. Memar picks no default, so that no store is pushed to a host nobody named. With a shared store:
- After a batch commits at the local compare-and-swap, which is the commit of the batch for its caller, a thread of the process pushes the reference by its explicit refspec, never forced, and on success moves the private reference `refs/memory-published/<class>` to what the shared store acknowledged. So the batches ahead of the shared store are the commits between the two references, known after a restart with no state in memory; a store opened with a lag starts publishing at once.
- An unreachable shared store never fails or delays a batch: the push is retried, at first after half a second and at most every fifteen seconds, for as long as a process has the store open.
- A push the shared store refuses as not a fast-forward means another writer published to the same reference: it is reported, as the refusal in the lag, and never overwritten. This is where the several-writers problem meets this adapter: two machines writing one class each order their own batches, and the shared store keeps the first that reached it. Ordering them is the first of the Anticipated Work of [Memory Record Handoff](../record/record.handoff.md#anticipated-work) and is not solved here.
- The lag (the batches ahead, the age of the oldest, and a refusal) is answered by `lag()` of a store and printed by `python modules-plugable/computer/memory/store/git-store/git-store.py lag --project PATH --class NAME`.
- The key `git-store-publish` (`class=now|soon`, `soon` when unset) says when a batch is answered: `soon` at the local commit, `now` after one push of it has been tried; a batch is Committed either way, and a failed push leaves it in the lag.

### How it meets the suite
- **core and model**: as `volatile` does, answered from the index and the blobs; `many-keys-one-pass` because a `get` starts no process.
- **durable**: a batch is visible only through the swap of one reference, after its pack is complete, so a kill leaves the previous commit or the new one; reopening reads the reference again.
- **shared**: every answer begins by reading the tip, and the index is brought up to date to it, so a batch of another process shows in the next call; `changes` is `diff-tree`.
- **fallback** and **working-tree**: [`cases.py`](cases.py), run on a scratch repository whose working tree has a tracked file.
- **replicated**: [`cases.py`](cases.py), run with a scratch bare repository as the shared store.
- **record**: `record`'s own group, run on `record` laid over this store.

### What it cannot do
- **Remove anything.** Every value stays in history and in packs; erasure waits for the owner's rule ([Memory Handoff](../../../../../modules/computer/memory/memory.handoff.md#what-is-the-retention-and-erasure-rule-for-preserved-history-and-where-do-a-records-versions-live)).
- **Answer a write of the same bytes in `changes`.** `diff-tree` compares trees, so an address rewritten with the value it held is not among the changes; no derived structure keyed by value misses anything by it ([git-store Handoff](git-store.handoff.md#decisions)).
- **Order writers on two machines** (above).
- **Remove a pack another process holds open on Windows.** `repack` then leaves it for the next one.
- **Survive the loss of power** beyond what git's own `core.fsync` gives; the contract does not ask it.
