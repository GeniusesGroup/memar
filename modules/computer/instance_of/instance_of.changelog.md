# Node Changelog

## Changelog

### Five edge documents written where the Phase 0 rule found none
- Time: 2026-10-09T09:30:00Z
- Type: added
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided

#### What changed
- `edges/{address,health,resource,language-human,node-metric}` each gained their `<name>.md` and a one-line `README.md`, in the Edge folder shape (Model, Policies, Placement, Open questions), extracted from the protocol sources and the domain document's settled sections.
- The handoff's "no domain document" item moved to Ambiguities Resolved; the wrong-kind-folder pass stays open and is now cited from [`node-metric.md`](edges/node-metric/node-metric.md).
- A repo-wide survey the same pass counted 48 edge folders without a `<name>.md`; eight were the ones the handoffs had already scored — these five and the three in [Software Changelog](../software/software.changelog.md) — and the rest belong to the per-category edge-bucket sessions in [Modules Handoff → Anticipated Work](../../modules.handoff.md#anticipated-work).

#### Considered and not done
- Answering the bucket doubts the sources raised (`address`/`resource`'s far end, `node-metric`'s `edges/` membership) — not taken: the sources state no relation, and inventing one would fail the no-bare-edges rule; each is recorded in its document's Open questions.
- Writing the remaining 40 documents in the same pass — not taken: they belong to the category sweeps that score each bucket move, not to a bulk write.

### Request Research 001: pointer section for the node end of the request chain
- Time: 2026-10-19T00:00:00Z
- Type: added
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — requested the work (2026-10-14)
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — researched and drafted

#### What changed
- [instance_of.handoff.md](instance_of.handoff.md) gains a pointer section to [Request Research 001](../request/request.research.001.md); the document, the edges and every `.kh` file are unchanged.
