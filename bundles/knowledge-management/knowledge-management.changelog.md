# Knowledge Management Changelog

## Changelog

### Bundle layer may own nested modules
- Time: 2026-09-21T12:40:00Z
- Type: Clarified
- Cited:
  - [bundles.md](../bundles.md) - Relation: Evidence: `modules/` is the base rules of its container; a bundle may introduce `bundles/<name>/modules/`
- Propagates to:
  - [bundles.md](../bundles.md): Done — governing statement
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Grok](../../CONTRIBUTORS.md#grok) (Grok 4.6 via Cursor) — recorded

#### What changed
The three-layer table no longer says the umbrella word lives in a bundle and the semantics always live elsewhere. This bundle remains composition-only; that is a fact about knowledge-management, not a rule for every bundle.
