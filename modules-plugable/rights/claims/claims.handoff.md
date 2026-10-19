# Claims Handoff

## Topic & Purpose
Open state for the optional dispute kinds: [claims.md](claims.md) and the edges under `edges/`. The case node itself lives in the [case](../../../modules/rights/case/case.md) domain; this module holds only the kinds an organization may include.

## Status
Active. The kinds are drafted and none is ratified as an edge.

## Open Questions

1. **Do the kind edges end at a case?** [claims.md](claims.md) states that every document under `edges/` is `(case)-[:.]->(.)`, and [case.md](../../../modules/rights/case/case.md) states that "Kidnap is an edge from this case to the kidnapped user". Neither edge file says so. [kidnap.md](edges/kidnap/kidnap.md) reads "Use to relate a `person` to a `person`" and [stolen.md](edges/stolen/stolen.md) reads "Use to relate a `product` to a `user` or `group`". The umbrella rule and the two edge files do not agree on the starting end. He has said the case and the claim are the same node here, so the one-line glosses are the narrower statement and the umbrella rule is the wider one; which one an implementer writes from is not settled. Matters because an implementer reading only the edge file would draw no case end at all. Blocks the endpoints of both edges.

## Assumptions
- **Weak.** That the two one-line glosses are drafts to be widened rather than the settled statement. Nothing in this module records who wrote them or when.

## Related Artifacts
- [claims.md](claims.md) — Review. Its Definition states the umbrella rule that question 1 turns on.
- [case.md](../../../modules/rights/case/case.md) — Review. It names the case end for kidnap and for stolen.
- [case.handoff.md](../../../modules/rights/case/case.handoff.md) — None. Question 25 there asks who owns liability, not this.

## Notes
- Question 7 of the pilot model draft asked "Does either edge have a case as an end?" and it was not answered then. It is the same question as number 1 here.
