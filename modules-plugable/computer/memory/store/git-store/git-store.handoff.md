# Memory Git Store Handoff
Open work for `git-store.md`. Entries are mutable current state, revised as each item moves and removed when it resolves or is dropped. See [handoff.md](../../../../knowledge/documentation/handoff/handoff.md) for what a handoff is.

## Topic & Purpose
What the adapter decided where no abstraction gave a name or a rule, and what only the owner can settle.

## Status
Active. Built by task `20261026-T181945Z-16468` (step 3 of `20261023-T074642Z-5420`); measured by task `20261026-T192807Z-36152` (step 4), whose numbers are [Research 001](git-store.research.001.md).

## Decisions
Each is **Tentative**: taken by task `20261026-T181945Z-16468` where the code needed a name or a rule no abstraction gave, open to the owner's ruling, and each says what changing it costs.
- **The adapter's keys are declared by its module, and their form once in the preferences module.** The plan asked for `git-store-reference` read in `modules/process/project/services/preferences.py` with its form declared there; that module's docstring and [Kernel Neutrality](../../../../../modules/knowledge/modularity/rules/kernel-neutrality/kernel-neutrality.md#the-rule) say an adapter's keys are its own. So the form, `class=value` pairs separated by commas, each class once, is declared once there (`class_values_preference`, which `memory` reads too), and the names `git-store-reference`, `git-store-shared` and `git-store-publish` are this module's. The Brief's `git`, `git-reference` and `memory-git` are read as `git-store-reference`. Changing it costs three names and one reader.
- **The shared store is named, never defaulted.** A class without `git-store-shared` has no shared store and is not `replicated`; the project's `origin` is not taken, because for Memar it is a public host and a default would publish work records nobody chose to publish. Changing it costs one default.
- **The lag is answered by `lag()` beside `state()`, and printed by a path-invoked command.** The plan says the lag is visible through `state()` and a verb; `state()` answers a token the contract fixes, so the lag is `Lag` (batches ahead, the age of the oldest, a refusal) from `lag()`, and the command is `git-store.py lag`. Whether it becomes a `memar` verb is the owner's (Open Questions). Changing it costs one method and one command.
- **`changes` is `diff-tree`, so a write of the bytes an address already held is not answered.** The contract says the addresses written; `diff-tree` answers the addresses whose value changed, which is what the plan names and what a derived structure needs. Answering every write exactly would need the addresses in each commit's message and `log`, which is not among the allowed plumbing. Changing it costs the realization of `changes`, or a sentence of the contract.
- **A batch's commit is written by `fast-import`, on a branch reset before its checkpoint.** `commit-tree` would cost a process and a loose object per batch; `fast-import` writes the same commit, with the previous tip as parent, into the batch's one pack, and a branch reset with no `from` makes it write no reference, so the swap of `update-ref` is the only thing that makes a batch visible. `fastimport.unpackLimit` is set to 0, so a small batch is a pack and not loose objects. Changing it costs the writer.
- **A `<reference>.lock` older than two seconds, found while holding the store's writer lock, is removed.** `killed-writer-leaves-no-lock` asks that a new writer not wait for a dead one, and git's lock carries no owner; the store's own lock, held by the operating system, says no live writer of the adapter is inside a swap, and two seconds outlasts any swap a git process outside the adapter makes. Changing it costs the bound.
- **The index is saved in the user's data area, under a folder Memar names here.** No module of Memar names the user's data area; `git-store` uses `%LOCALAPPDATA%\Memar\git-store\` on Windows and the XDG data folder elsewhere, and the tests give it a scratch folder. When a second module needs the place, it moves to the filesystem module. Changing it costs one function.
- **The `fallback`, `working-tree` and `replicated` groups are coded in this module, in `cases.py`.** [Memory Conformance](../../../../../modules/computer/memory/conformance/conformance.md) gives `fallback` and `working-tree` to the adapter that declares them; `replicated` is declared in the kernel's `protocol/store.py`, but its cases need a seam only an adapter with a shared store can offer, and `git-store` is the first. When a second adapter declares `replicated`, the group and its seam move to the conformance module. Changing it costs a move.
- **The seam of the groups is three methods of the adapter: `fall_back(fallback, held)`, `working_tree()`, and `shared_reachable(flag)`, `shared_state()`, `sibling()`.** No abstraction names them; they are declared in `cases.py` with the groups. Changing them costs the cases.
- **Packs are bounded by `repack -d --geometric=2` once a store has more than 32.** Measured by [Research 001](git-store.research.001.md#findings) (task `20261026-T192807Z-36152`): over 10,000 single-write batches the count stayed between 2 and 34 at every sample of 100 and ended at 4, so the bound stands. Changing it costs one number.

## Open Questions

### Which shared store do Memar's own work records publish to?
- State: `memory: work-records=git-store` is in Memar's `manifest.yaml` with no `git-store-shared`, so nothing is published. The owner's decision that every committed batch is published needs a shared store named; the project's `origin` is a public host, and the records branch was never pushed.
- Options: name a private shared store for `work-records` (recommended: records reach a store the owner controls); name `origin`, publishing the work records publicly; keep none until P4.
- Anchor: [Publishing to the shared store](git-store.md#publishing-to-the-shared-store).
- Blocks: publishing Memar's work records; nothing in this step.
- Asked: 2026-10-26, Claude (task `20261026-T181945Z-16468`), for Omid Hekayati.

### Should the lag be a `memar` verb?
- State: the lag is printed by the path-invoked `git-store.py lag`; a `memar` verb needs a route in `bundles/memar` and a name the owner gives.
- Options: `memar memory lag --class NAME` (recommended: the agent's door is `memar`); keep the path-invoked command.
- Anchor: [Publishing to the shared store](git-store.md#publishing-to-the-shared-store).
- Blocks: nothing now.
- Asked: 2026-10-26, Claude (task `20261026-T181945Z-16468`), for Omid Hekayati.

## Anticipated Work
- **The saved index grows with the store and is rewritten whole.** [Research 001](git-store.research.001.md#findings) measured 1.1 GB written to the data area while 99,000 nodes were written in batches of 200 (the packs were 9.9 MB): the index, a JSON file of every address, is saved whole every 256 changed addresses, about 2.2 MB per batch at 100,000 nodes. Options for the task that takes it: save it only on `close` and on a time bound, or save it in parts by the address's fan-out prefix, or append changes and compact; each keeps it a cache that dropping changes no answer of.
