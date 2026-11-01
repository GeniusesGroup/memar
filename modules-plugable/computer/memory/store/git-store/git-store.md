---
Title: "Memory Git Store"
Status: Draft
Start Date: 2026-10-26
ID: 498066
---

# Memory Git Store

## Abstract
`git-store` is an adapter of the [store contract](../../../../../modules/computer/memory/store/store.md#the-contract) that keeps a store in a reference of a git object database and nothing else: no worktree, no index, no file in the project's working tree. It knows addresses only. A store is one reference, `refs/memar/<class>` by default; its state is the commit the reference points to, one commit for each committed batch; a batch is written as one pack and made visible by one compare-and-swap of the reference. When a class names a shared store, every committed batch is published to it soon after it commits, and the adapter knows after a restart how far the shared store lags. It is the first, replaceable medium of the work records: the owner ruled that git is a sink to be left, so the adapter uses plumbing only and builds nothing that would outlive it.

The adapter is Khayyam: [`protocol/git-store.kh`](protocol/git-store.kh) and the `git-store-*.kh` files beside it declare its capabilities, parameters, limits, held ranges, fallback, publisher, lag and the seam; [`git-store.py`](git-store.py) realizes them; the groups it owes are [`cases.py`](cases.py); its tests are [`tests/git-store.py`](tests/git-store.py). What it costs, measured against today's files under git, is Research 001, and its procedure [`services/_benchmark.py`](services/_benchmark.py).

## Explanation

### What it declares
Its capabilities, parameters and limits are [`git-store-capabilities.kh`](protocol/git-store-capabilities.kh), [`git-store-parameters.kh`](protocol/git-store-parameters.kh) and [`git-store-limits.kh`](protocol/git-store-limits.kh), and their meanings are the contract's. Two choices are reasons: it is `replicated` when, and only when, the class names a shared store, and it is not `lockable`, because the expectation is the control of writers.

### The first configuration: one reference per class
A class is kept in one reference, fetched only by an explicit refspec and never checked out. A batch therefore touches one reference, and its atomicity is one compare-and-swap. With several references, a batch that touched two would not be atomic against a kill, because git's files backend renames each reference's lock on its own; the case `kill-during-batch-is-atomic` decides that, and it is why a split into windows of the address, the later configuration the change plan names, is a migration by address that keeps one reference per batch rather than a batch across two. The reference's name and the key that sets it are [`git-store-reference.kh`](protocol/git-store-reference.kh) and [`git-store-reference-namespace.kh`](protocol/git-store-reference-namespace.kh).

**The namespace follows what git hosts already do with namespaces they own** (`refs/pull/<n>/head`, `refs/notes/<name>`, `refs/changes/`), and departs from them where Memar's case differs.
- It is outside the branches and tags, so no listing shows it and a default clone or fetch does not carry it: the fetch is opt-in. A consumer who wants the records fetches them into a private namespace of its own (for example `+refs/memar/*:refs/memar-remote/*`), never into the same name, which would let a fetch overwrite a local store.
- The name is the project's own, because `memory` is generic and another tool may claim it, and never one a host owns. A host may refuse refs outside its customary namespaces, so the first push of the work records tests a real push before anything depends on it.
- Unlike `refs/pull`, which one server writes, this namespace has several writers and no server owns it: it is client-owned, a push is never forced, and a refusal as not a fast-forward is kept and reported, as the section on publishing says.
- Its references are ordinary reachable references, so `git gc` keeps what they reach and no keep-around reference is needed, and a mirror copies them. The bookkeeping references of the adapter are private and outside the public root, so no publish or mirror refspec can push private state.
- A class may not be named so that its reference is a folder of another's (`a` and `a/b`); git cannot hold both.

Inside the reference's tree, an address is written under a fixed-length prefix of itself, so that no tree is flat and a commit rewrites a few small trees; for an id of version 7 the prefix is a window of time of tens of years down to hours, without the adapter reading the id. The rule is private: no answer shows it, and changing it is a migration of one reference.

### The plumbing it uses
The constraint is the owner's ruling that git is a sink to be left ([Memory Store → The contract](../../../../../modules/computer/memory/store/store.md#the-contract), "Adapters state themselves"): only plumbing that any later medium can replace, and nothing that needs a worktree or an index. What follows, as reasons:
- Reads go through one long-lived object reader, so a `get` of any number of addresses starts no process, and `stats` can say so.
- A batch is written as objects by one long-lived `fast-import` into one pack, which is why the change plan chose it (C7) over one file per object (`hash-object`, `mktree`, `commit-tree`); a commit is still one commit per batch, as Memory Record Handoff → Decisions decides.
- The compare-and-swap of the reference is the only act that makes a batch visible, so that a kill leaves the previous commit or the new one.
- `changes` and the derived index are brought up to date by comparing two trees, which is why a write of the same bytes is not a change (below).
- One pack per batch would grow into a pack per batch forever, so the packs are repacked when they pass a bound.
- A push is by explicit refspec and never forced; what the shared store acknowledged is recorded in a private reference.

### Writers, and a lock a killed writer left
Every writer of a store on a machine goes through the adapter, and the adapter orders them by one lock per store, in git's own directory, held by the operating system's lock on an open file, which the operating system releases when the process ends, however it ends. A writer holds it from reading the tip to the end of the compare-and-swap; a writer paused at the commit point holds it, and a second writer waits and then decides its expectations on the state the first left.

git's own lock on the reference, which exists for the instant of the swap, carries no owner. A writer that holds the store's lock and finds one knows that no live writer of the adapter made it: it was left by a writer killed during the swap, or is held for an instant by a git process outside the adapter. So a lock older than a short bound is removed and the swap is tried again; a younger one is waited for. A batch whose swap cannot be decided is answered Unavailable only once its commit can no longer become the tip. A writer killed before the swap leaves at most a pack nothing reaches, which repacking and git's pruning collect.

### What it keeps outside the store's medium
- **The index**, a derived structure: for each held address, the id of its blob, in byte order. It answers `list` and the addresses of `get`, records the tip it reflects, and is brought up to date before it answers by comparing the trees from its tip to the reference's. It lives in the memory of the process and is saved, as a cache another process may start from, in the user's data area, one file per object database and reference. Dropping it deletes both, and changes no answer. It serves address ranges only: it holds no label and reads no address.
- **Nothing else.** The writer's lock is in git's directory, and the reference that records what the shared store acknowledged is a reference of the same object database (below).

### The fallback
A store holds the ranges of addresses it decides alone; an address outside them is asked of a fallback, as fresh as the asking, and what it answers is never written into the store ([Memory Store → The contract](../../../../../modules/computer/memory/store/store.md#the-contract), "Why one place orders the writes"). The fallback is an interface ([`git-store-fallback.kh`](protocol/git-store-fallback.kh)), and its one implementation, [`git-store-not-found.kh`](protocol/git-store-not-found.kh), answers that nothing is there. Until a fetch of part of a shared store exists, a store holds every address, so the fallback is reached only through the seam of the `fallback` group.

### Publishing to the shared store
A class names its shared store by key; a class it does not name has none, and its store is not `replicated`. Memar picks no default, so that no store is pushed to a host nobody named. The publisher, the lag and the publish kinds are [`git-store-publisher.kh`](protocol/git-store-publisher.kh), [`git-store-lag.kh`](protocol/git-store-lag.kh) and [`git-store-publish-kinds.kh`](protocol/git-store-publish-kinds.kh). With a shared store:
- A batch is Committed at the local compare-and-swap and published after, so the batches ahead of the shared store are the commits between the two references, known after a restart with no state in memory.
- An unreachable shared store never fails or delays a batch ([`git-store-publisher.eng.kh`](protocol/git-store-publisher.eng.kh)). The trade-off is that a batch is Committed before it is published, so the shared store lags, and a loss of the machine in that interval loses the batches in the lag; the lag is observable and reported.
- A push the shared store refuses as not a fast-forward means another writer published to the same reference: it is reported, as the refusal in the lag, and never overwritten. This is where the several-writers problem meets this adapter: two machines writing one class each order their own batches, and the shared store keeps the first that reached it. Ordering them is the first of the Anticipated Work of Memory Record Handoff and is not solved here.
- A class may ask that a batch be answered only after one push of it has been tried ([`git-store-publish-kinds.eng.kh`](protocol/git-store-publish-kinds.eng.kh)); a batch is Committed either way, and a failed push leaves it in the lag.

### How it meets the suite
It runs every group its declarations call for; the groups it owes itself are in [`cases.py`](cases.py), on a scratch repository, and the conformance suite's groups in [Memory Conformance](../../../../../modules/computer/memory/conformance/conformance.md#groups). Two reasons are worth keeping: durability holds because a batch is visible only through the swap of one reference after its pack is complete, and a batch of another process shows in the next call because every answer begins by reading the tip. The slow cases and what they cost are an open question in Memory Store Handoff.

### What it cannot do
What it cannot do is stated in [`git-store.eng.kh`](protocol/git-store.eng.kh). The reasons are these.
- **Removal.** Erasure waits for the owner's rule (Memory Handoff).
- **A write of the same bytes in `changes`.** No derived structure keyed by value misses anything by it (git-store Handoff).
- **Ordering writers on two machines** is the several-writers problem of the section on publishing.
- **A pack another process holds open on Windows** is left by repacking for the next one.
