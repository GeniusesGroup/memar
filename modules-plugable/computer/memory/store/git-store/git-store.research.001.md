# Memory Git Store Research 001 — The benchmark

## Table of Contents
- [Status](#status)
- [Question and Goals](#question-and-goals)
- [Participants](#participants)
- [Methodology](#methodology)
- [Findings](#findings)
- [Conclusion](#conclusion)
- [Related Artifacts](#related-artifacts)

## Status
Complete

## Question and Goals
- **Questions**
  - Q1: What does writing nodes through `git-store` cost on the owner's machine (files created, write operations, process starts, wall and CPU time), against the baseline of today's files under git (task `20261020-T131910Z-22300`), like for like? — Answered (scan events and Defender's CPU not measured; see Methodology).
  - Q2: Does the number of packs stay bounded by `repack` over at least 10,000 single-write batches? — Answered.
  - Q3: What do a push and a fetch send after 1,000 and 100,000 nodes, for a reference that points to a commit per batch and for one that points at a bare tree? — Answered.
- **Goals**
  - Evidence whether the store is worth leaving files in the working tree for (the Why of the build programme, task `20261023-T074642Z-5420`). — Partially met: the store's own cost is measured, the scanner's is not.
  - The decision "A reference points to a commit per batch" of [Memory Record Handoff](../record/record.handoff.md#decisions) tested by numbers, not only argued. — Met.
- **Scope**: the adapter as built by task `20261026-T181945Z-16468`, on one Windows machine, unelevated. Leaves out Defender's CPU and Process Monitor's event counts (they need elevation), a shared store over a network (the shared stores here are local bare repositories), and reads.

## Participants
- An AI agent (Claude, model claude-opus-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — Researcher, in task `20261026-T192807Z-36152`.
- [Omid Hekayati](../../../../../CONTRIBUTORS.md#omid-hekayati) — Questioner and Goal-setter (the build programme's Request and the owner's question of 2026-10-26 on a bare tree). Reviewer: Not yet reviewed.

## Methodology
- **The procedure** is [`services/_benchmark.py`](services/_benchmark.py); its docstring says what each case does. Each measured write is a worker process (Python, `record` laid over `git-store` on a fresh scratch repository) inside a Windows Job Object, so a number counts the worker and every git process it starts, as the baseline counts a command. Files created are the files present in the repository's `.git` and the data area after the run and not before (a file created and removed within the run is not seen). Nodes are the baseline's small files (`# file i`, `small record i`) as one part each, with ids of version 7 five minutes apart, so they spread over the tree's folders as a year of records would.
- **Bytes on the wire** are what a `--receive-pack` wrapper reads from the pushing client, and what an `--upload-pack` wrapper sends the fetching client (protocol lines and pack together), with a local bare repository as the shared store and another as the fetcher. "full" is the first transfer into an empty store; "one more" is the next transfer after one batch of one node. The bare-tree variant is the same object database with a second reference set to the tree of the same commit, pushed and fetched by its own refspec; it is a variant of the reference, not a second adapter.
- **The baseline** was run again, unelevated, with its own procedure (`bench_baseline.py --repeat 5 --files 200`, copied into task `20261026-T192807Z-36152`'s `services/`); its elevated numbers of 2026-10-23 are quoted from its `docs/options.md`.
- **With and without the exclusion.** Reading or setting Defender's exclusions needs elevation, which this run did not have, so no setting was changed. Instead every case ran twice: in a folder under `C:\Sync\Persons\Geniuses.Group\github.com`, which the owner excluded on 2026-10-23 per the baseline's record, and in a folder under `%LOCALAPPDATA%\Temp`, which is not excluded. That the exclusion still stands was not verifiable unelevated. Defender's CPU reads as null unelevated, so the scanner's cost is not measured; the command that measures it, run as administrator from the checkout, is:
  `python modules-plugable\computer\memory\store\git-store\services\_benchmark.py like-for-like --where <folder> --label elevated --out <file>` (and `nodes`, `single`), once with `--where` inside the excluded folder and once outside it.
- **Limits.** One machine, one run of the 100,000-node and 10,000-batch cases per location (median of 5 only for the like-for-like cases); the raw lines are kept in that task's `temp/git-store-bench.jsonl`, which is not archived.

## Findings
Numbers are measured, unelevated, on 2026-10-26; "inside" is the excluded folder, "outside" the other.

**Q1, like for like (median of 5).** 200 small items created and committed, then edited and committed:

| case | wall s | own CPU s | processes | write ops | files created |
| --- | --- | --- | --- | --- | --- |
| baseline, elevated 2026-10-23, create+add+commit 200 files | 1.310 | 0.422 | 5 | n/a | 200 files and their loose objects |
| baseline rerun, inside, create+add+commit | 1.367 | 0.359 | 5 | 412 | (as above) |
| baseline rerun, outside, create+add+commit | 1.337 | 0.390 | 5 | 412 | (as above) |
| git-store, inside, 200 nodes in one batch | 0.294 | 0.219 | 9 | 19 | 5 |
| git-store, outside, 200 nodes in one batch | 0.326 | 0.250 | 9 | 19 | 5 |
| baseline, elevated 2026-10-23, edit+add+commit 200 | 1.471 | 0.609 | 5 | n/a | |
| baseline rerun, inside, edit | 1.465 | 0.390 | 5 | 412 | |
| git-store, inside, 200 nodes edited in one batch | 0.317 | 0.234 | 9 | 19 | 2 |
| git-store, outside, edit | 0.324 | 0.203 | 9 | 19 | 2 |

The baseline's job holds `git add` and `git commit` only; its 200 files are written by the script outside the job, so the baseline is the cheaper side of the comparison. `git-store`'s job holds the whole write, a Python start and its imports included (0.15 to 0.18 s of it is the write inside the process). The baseline's other cases, rerun unelevated: `git status` 0.097 s, `memar task list` 0.790 s, `memar content check docs/` 1.321 s (outside: 0.095, 0.790, 1.296), against 0.07, 0.99 and 1.63 s quoted from 2026-10-23.

**Q1, 100,000 nodes in batches of 200** (1,000 written first, then one batch of one node, then the rest to 100,000; the 100,000 row is the second segment, 99,000 nodes in 495 batches):

| location | segment | wall s | own CPU s | processes | write ops | bytes written | files created / removed | packs at end |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| inside | 1,000 | 0.643 | 0.484 | 9 | 85 | 0.4 MB | 13 / 0 | 5 |
| inside | to 100,000 | 26.631 | 23.719 | 114 | 8,561 | 1,106.5 MB | 38 / 15 | 17 |
| outside | 1,000 | 0.393 | 0.281 | 9 | 85 | 0.4 MB | 13 / 0 | 5 |
| outside | to 100,000 | 26.056 | 23.250 | 114 | 8,561 | 1,106.5 MB | 38 / 15 | 17 |

At the end the store holds 104,300 objects in 18 packs, 9.9 MB of packs, for 100,001 nodes. Files in the working tree: none. The 1.1 GB written is not the packs: it is the index the adapter saves in the data area, a JSON file of every address, rewritten whole every 256 changed addresses, so its cost grows with the store (about 2.2 MB per batch at 100,000 nodes).

**Q2, 10,000 single-write batches:**

| location | wall s | own CPU s | processes | write ops | bytes written | packs, most sampled (every 100) | packs at end |
| --- | --- | --- | --- | --- | --- | --- | --- |
| inside | 190.8 | 133.4 | 2,189 | 163,350 | 95.4 MB | 34 | 4 |
| outside | 185.5 | 129.6 | 2,189 | 163,350 | 95.3 MB | 34 | 4 |

About 19 ms and 13 ms of CPU per batch. The packs stay bounded: `repack -d --geometric=2`, asked every 16 batches past 32 packs, kept them between 2 and 34 at every sample, and 4 remained (60,003 objects, 5.1 MB). The adapter itself started 938 processes (its own count); the job counted 2,189, the rest being the processes `repack` starts.

**Q3, bytes on the wire** (the same in both locations to within 500 bytes; inside shown):

| nodes | transfer | commit per batch: push | fetch | bare tree: push | fetch |
| --- | --- | --- | --- | --- | --- |
| 1,000 | full | 69,546 | 69,595 | 68,303 | 68,352 |
| 1,000 | one more batch | 647 | 774 | 979 | 68,423 |
| 100,000 | full | 7,148,780 | 7,149,369 | 6,991,493 | 6,992,072 |
| 100,000 | one more batch | 669 | 796 | 1,833 | 6,992,144 |

- A first transfer of a bare tree is about 2 % smaller (no commits).
- After one more batch, a fetch of the bare tree resends the whole store (68 KB at 1,000 nodes, 7.0 MB at 100,000), where the commit chain sends under 0.8 KB at both sizes: fetch negotiates by commits, and a tree gives it none.
- A push of the bare tree sends a little more than the commit chain's (1.8 KB against 0.7 KB at 100,000), and git refuses it unless forced: "You cannot update a remote ref that points at a non-commit object ... without using the '--force' option". A forced push cannot be refused as not a fast-forward, so the shared store's refusal of a lost update, which `replicated` reports, is lost with it.

## Conclusion
- Q1: like for like, `git-store` writes 200 small items in about a quarter of the wall time and three fifths of the own CPU of today's add and commit, with 5 files created instead of 200 and their loose objects, 19 write operations instead of 412, and nothing in the working tree; the Python start is inside its number and not inside the baseline's. Wall and CPU were the same inside and outside the excluded folder, for the store and for the baseline. What the scanner spends is not measured (elevation); the owner's command is in Methodology. At 100,000 nodes the cost that grows is the saved index (1.1 GB written for 99,000 nodes), not the packs. Recorded in [git-store Handoff](git-store.handoff.md#anticipated-work).
- Q2: the number of packs stays bounded (at most 34 sampled, 4 at the end of 10,000 single-write batches). The bound of 32 in `git-store.py` stands as measured.
- Q3: the numbers support the decision that a reference points to a commit per batch: one more batch costs under 0.8 KB to push or fetch with commits, while a bare tree's fetch resends the store and its push must be forced. Recorded, Tentative and not reversed, in [Memory Record Handoff](../record/record.handoff.md#decisions).

## Related Artifacts
- [Memory Git Store](git-store.md) — the adapter measured; it points here for its numbers.
- [git-store Handoff](git-store.handoff.md) — the pack bound, revised by Q2; the index's write cost, anticipated work from Q1.
- [Memory Record Handoff](../record/record.handoff.md#decisions) — "A reference points to a commit per batch", revised by Q3.
- Task `20261020-T131910Z-22300`, `docs/options.md` and `services/bench_baseline.py` (on the records branch) — the baseline.
