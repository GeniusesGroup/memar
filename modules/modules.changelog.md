# Modules Changelog

## Changelog

### Placement text reduced to a reference to Memar's Classification
- Time: 2026-10-17T12:00:00Z
- Type: changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided

#### What changed
- `modules.md` → Placement no longer states the Kernel, Pluggable and Bundle tests or the operational rules of Memar's Pluggable; it cites Memar's [Placements](./knowledge/modularity/placements.md) (with its Placement and Category Depth rules, the Label module and the `guest` label) as the authority. The heading and anchor `#placement` are kept because many documents link to it.
- Kept as this repository's own: an edge becomes a module only with independent semantics; no bare edges; kernel does not reference the rule domain; the category-level `analytics` namespace for cross-domain analytics; behavior binds to UUID. Edge buckets, Edge folder and Module skeleton are unchanged.
- `modules.handoff.md` gained "Re-reading this repository's categories": a proposal for `storage` under `computer` and for `management/organization` against `identity/organization`, and the categories not yet read.

#### Considered and not done
- Moving `modules/storage/` or `modules/management/organization/` — not taken: the owner has ruled the direction for `storage` only, not its shape, and has not ruled on the organization pair; both are asked in the handoff.
- Restating Memar's tests here — not taken, as in the 2026-10-08 entry: a second copy of what Memar owns.
- Rewriting the documents that link `modules.md#placement` — not needed: the anchor stays, and "no bare edges" still lives under it.

#### Notes
- The links to Memar point at its `main` branch on GitHub; Classification and Label are uncommitted in Memar at this writing, so they resolve only after Memar commits them.

### Placement rules and edge buckets recorded; audit open state made durable
- Time: 2026-10-08T09:05:00Z
- Type: added
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided

#### What changed
- `modules.md` gained a `Placement` section, an `Edge buckets` section, and a `Module skeleton` section; its empty H1 became `# Modules`.
- `modules.handoff.md` was created, carrying the audit's open state and owner-gated leftovers.
- The three-layer model, the core-by-necessity test, the capability-completeness rule, and the `edges/` / `edges-loop/` / `edges-shortcut/` buckets are the durable outcome of the 2026-08 to 2026-09 core-vs-pluggable sessions, previously held only in gitignored briefs under `____Chats/`.

#### Considered and not done
- A new category-level doctrine file for the audit — not taken: the criteria land in the existing `modules.md`, and the working state in `modules.handoff.md`. The framework tests stay in Memar's own documents and are linked, not restated.
- Porting the per-domain rationale of the applied moves back out of their destinations — not taken: that rationale already lives in each destination document.
- Copying the framework tests themselves into `modules.md` — not taken: [Content Rule](../modules-plugable/knowledge/documentation/documentation.md#content-rule-no-fabricated-or-redundant-provenance) forbids a second copy of what Memar already owns.

### Go → Khayyam migration map graduated out of `____Chats`
- Time: 2026-10-08T09:56:07Z
- Type: created, moved
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided

#### What changed
- The Go → Khayyam migration map, held only as a gitignored brief under `____Chats/`, graduated by facet: its governing rules, disposition triage, and review criteria are now `Khayyam.practice.md`, and its phase record, corpus conventions, pilot findings, and open questions are `Khayyam.handoff.md` (both at the top of the `organization` repository as it stood then; the links were turned into plain names on 2026-10-20 because neither path exists in this repository).
- `modules.md` gained the edge-folder shape the Phase 0 pass produced: one folder per edge with Model, Policies, Placement, and Open questions; no aggregate `edges.md`; no archived deleted path; and the folder named for the relation rather than for the owning domain.
- The twelve module handoffs that cited the brief by its scratch path now link the practice document, and `thing` and `comment` also link the handoff for the pilot findings and the Phase 0 review. `AGENTS.md` declares the practice before source work.
- The brief itself went to the platform trash through `host/fs.py`.

#### Considered and not done
- Keeping the brief in `____Chats/` as the rules' standing home — not taken: a gitignored workspace is not a durable home, and its citations were the only record of rules the rest of the tree follows.
- Restating the rules inside `Contribution.md` — not taken: ways of working belong in a Practice document, and `Contribution.md` stays a contributor's entry point.
- Moving `____Chats/____main/` with it — not taken: Phase 4 reads it, and its entry-point text exists in no commit of this repository, so it stays scratch until that phase converts it.

### Scope of the modules records stated
- Time: 2026-10-10T13:45:00Z
- Type: changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided

#### What changed
- `modules.md` now states that it and its companions hold only how a module is placed and added; a change inside a module is recorded in that module's own changelog and handoff.
- An entry recording the `replacement-cost` module and the pricing decision, written here the same day, moved to [replacement-cost.changelog.md](../modules-plugable/economics/replacement-cost/replacement-cost.changelog.md) and [pricing.changelog.md](../modules-plugable/economics/pricing/pricing.changelog.md).
- The entry recording the eight edge documents written for `computer/software` and `computer/instance_of` (2026-10-09) moved to [software.changelog.md](computer/software/software.changelog.md) and [instance_of.changelog.md](computer/instance_of/instance_of.changelog.md), each carrying the part about its own edges.

---

### organization's modules README carried after the merge
- Time: 2026-10-19T12:00:00Z
- Type: changed
- Cited:
  - [Modules](./modules.md) - Relation: Evidence: the document organization's `modules/README.md` pointed at
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Claude](../CONTRIBUTORS.md#claude) (Sonnet-5.5) — carried, recorded

#### What changed
In organization (commit `19834121`) `modules/README.md` was a git symlink to `modules.md`, so it held no text of its own; memar's `README.md` here is a separate document describing the layer. `README.md` gained the section *Placement and the edge rules*, which names `modules.md` as the main document for placement, edge buckets, the edge folder and the module skeleton, so the entry point organization's README gave is kept without a second statement of it. `modules.md` itself is the content session's file and was not touched here. Nothing else from organization's side existed to carry or to drop.

---

### `status/` is a main folder beside `edges/` and `protocol/`
- Time: 2026-10-20T07:00:00Z
- Type: Changed
- Cited:
  - [Modules Research 001 → 6](../.agents/tasks/20261019-T191746Z-12632/docs/modules.research.001.md#6-owner-decisions-needed) - Depends_on: the owner's rulings D5 and D6 of 2026-10-20.
  - [Modules Categories Research 001 → 7](../.agents/tasks/20261019-T191746Z-16420/docs/modules.categories.research.001.md#7-owner-decisions-needed) - Depends_on: the owner's ruling C3 of 2026-10-20, one profile with two layers.
- Tasks:
  - 20261020-T060221Z-19268: Closed - the session that applied the rulings.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - decided
  - [Claude](../CONTRIBUTORS.md#claude) (Opus 5.5 via Claude Code) - applied

#### What changed
- [Edge buckets](./modules.md#edge-buckets) names four kinds: `status/` holds the loop-edges whose kind is Status and sits beside `edges/` and `protocol/`; `edges-loop/` no longer spells `Status_*` and keeps every other one-node classification, the status module's shared statuses excepted. The edge folder sentence names `status/` with the other three.
- [Module skeleton](./modules.md#module-skeleton) states the two layers, the structural kinds and the kinds of work, and that a need only one domain has is a part of it, not a role.
- [README](./README.md#the-kinds-of-folder-here) gains the bullet *By structure inside a module*, which lists `protocol/`, the edge folders and `status/`, and says that `status/` is neither a role folder nor a Role.

---

### `labels/` joins the structural layer of the module skeleton
- Time: 2026-10-23T10:20:00Z
- Type: Changed
- Cited:
  - [Modules Handoff → Decisions](./modules.handoff.md#decisions) - Depends_on: the decision of 2026-10-23, taken by the coordinator from the owner's rulings of 2026-10-20 and 2026-10-23.
- Tasks:
  - 20261023-T100229Z-17920: Closed - the task that wrote it.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - ruled
  - [Claude](../CONTRIBUTORS.md#claude) (Opus 5.5 via Claude Code) - applied

#### What changed
- [Module skeleton](./modules.md#module-skeleton) lists `labels` among the structural kinds: the folder in which every module, kernel or pluggable, declares its own labels as code.
