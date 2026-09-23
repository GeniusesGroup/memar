# Case Changelog

## Changelog

### Particular accusations leave the case type
- Time: 2026-09-23T07:10:00Z
- Type: moved
- Cited:
  - [Claims](../../../modules-plugable/rights/claims/claims.md) - Relation: Evidence: optional kinds of dispute
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — rejected keeping those edges on the case type
  - [Grok](../../../CONTRIBUTORS.md#grok) (Grok 4.7 via Cursor) — moved them

#### What changed
Stolen, kidnap, and illegal moved from this domain's `edges/` to [claims](../../../modules-plugable/rights/claims/claims.md), with annul-for-conflict and annul-for-update. [case.md](case.md) keeps the dispute node. Settlement-for stays here, and whether it is part of the type is open.

#### Deliberation
Owner: putting annul-law-for-conflict on the case type repeated the older mistake. Stolen and the edges like it were already that mistake. Kinds of dispute are optional. The case node is the kernel.
