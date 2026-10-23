# Law — optional parts Changelog

## Changelog

---

### The law type's optional parts become one module
- Time: 2026-10-20T07:00:00Z
- Type: Added, moved
- Cited:
  - [Modules Research 001 → Owner decisions needed](../../../.agents/tasks/20261019-T191746Z-12632/docs/modules.research.001.md#6-owner-decisions-needed) - Relation: Depends_on: rulings D1 to D3
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — ruled the placement
  - [Claude](../../../CONTRIBUTORS.md#claude) (Opus-5.5 via Claude Code) — moved and wrote

#### What changed
`modules-plugable/rights/law-labels` moved to `labels/`, `law-validity` to `edges/validity/`, and `laws` to `laws/`, each with `git mv`; each part's main document took its folder's name. The module took [law.md](law.md) and [law.manifest.yaml](law.manifest.yaml). No `rules/` part was made, because no rule of the rule domain runs under law yet.

#### Deliberation
Owner: the parts are one capability of one kernel type, removed as one unit; validity is a relation of a law, so an edge, not a rule; a rule and a law are different subjects.
