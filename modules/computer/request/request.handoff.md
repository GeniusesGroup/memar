# Request Handoff

## Topic & Purpose
Org service-surface addressing policy inherited from the sRPC / URL critique sessions: four-identity decomposition, address carries only destination, and Official ≠ standard. Migrated from the Organization ideas backlog second pass (2026-09-16).

## Status
Active — direction/decided principles recorded; org-side operationalization of Official≠standard still open.

## Decisions

### From Organization ideas backlog — sRPC / URL critique (`sRPC - chatgpt.md`)

- **Four-identity decomposition for any org service surface:** routing identity, service identity,
  operation identity, and request identity are distinct concepts; HTTP collapsed them into one string
  and the ecosystem pays in cache-key ambiguity, authorization variance, and non-canonical resources.
  Org-internal service addressing should keep them separate (ServiceID fields, per-request stream
  identity) and never build user-facing URLs that double as internal service addresses. *(direction;
  recorded in memar as an sRPC design-rationale open item — the org should inherit it as policy)*
- **An address carries only destination information; request data never rides in the routing address.**
  The org's API design rule for every exposed surface (internal sRPC or external HTTP): the path/route
  names the destination; parameters are request data; "two optional places for one concept" is the
  smell to forbid — one concept, one representation, decided once per resource class. *(decided
  direction in the session; candidate org engineering rule)*
- **"Official" ≠ "standard": conformance is never inferred from a label.** When the org evaluates a
  vendor library, framework, or protocol, the check is against the rules themselves, not the
  implementation's origin, market share, or the fact that it ships by default — Memar already records
  the principle (protocol.md); the org's procurement/evaluation practice should operationalize it.
  *(decided principle; org-side operationalization open)*

## Open Questions
- Org-side operationalization of Official ≠ standard (procurement/evaluation practice). *(decided principle; org-side operationalization open)*

## Related Artifacts
- [`README.md`](README.md)
- Memar `protocol.md` / sRPC design-rationale open item

## Notes
- Provenance: Organization ideas backlog → second-pass From `sRPC - chatgpt.md` (2026-09-16 migration).
