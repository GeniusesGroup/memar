# Person Handoff

## Topic & Purpose
Where the person domain stands: what it is for, what it should hold, and the questions only the owner can answer. The domain document is one encyclopedia sentence; the folders (kinship, the social graph, a Go life-log) have never had a handoff.

## Status
Active - a pointer section only, from a research on 2026-10-18. Nothing is ratified.

## Research 001 pointer (2026-10-18)
[estate.research.001.md](../estate/estate.research.001.md) analyses person with estate and taxon as the identity world around the user (scenarios H1 to H7; findings 2B, 3 and 5). Every item is Tentative, Explored or Deferred. In one paragraph: person is proposed as a classification of a thing (not of a user), with life facts (birth, death, declared absence, reversible by a later fact) and parentage as a record with a kind as its kernel; the social graph becomes a pluggable; gender and sexuality leave taxon.

### Open Questions raised by the research
Each has a default and what it blocks in the research's [Open Questions](../estate/estate.research.001.md#8-open-questions), under Person.
1. **PS.1** - Is a person a classification of a thing, so that a person need not be a user? Default: yes. Blocks: the `person` loop, the kinship endpoints, `PersonModel`.
2. **PS.2** - Does "person" mean the natural human individual only? Default: yes; legal persons are organizations. Blocks: person.md against organization.md.
3. **PS.3** - Is kinship one `parentage` record with a kind rather than four edges? Default: yes; siblings discovered.
4. **PS.4** - Are life facts events with effective and recorded time and reversibility? Default: yes. Blocks: `protocol/life-log.kh`.
5. **PS.5** - Is the social graph a pluggable? Default: yes. Blocks: ten edge folders.
6. **PS.6** and **PS.7** - Where do gender identity, the legal marker and sexuality live, and is sexuality modeled at all? Default: person-side pluggables; sexuality not in any kernel, off by default.

### Contradictions found (reported, not resolved)
person.md's "legal responsibility" against organization.md's "non-person" (PS-C1); social-connection endpoints that mix `person`, `user`, `group` and `connection_user` (PS-C2); `life-log.kh` in package `org` inside the person folder (PS-C3).

## Proposed Next Steps
1. Owner rules on PS.1 and PS.2; they decide the loop, the kinship endpoints and `PersonModel`.
2. Replace the kinship edges with `parentage` and reclassify the social-connection family as one pluggable, after PS.3 and PS.5.
3. Resolve `life-log.kh` (its `Type` values, its package) before any conversion, after PS.4.

## Related Artifacts
- [`person.md`](person.md) - the domain document.
- [`../estate/estate.research.001.md`](../estate/estate.research.001.md) - the research.
- [`../user/user.research.001.md`](../user/user.research.001.md) - kind is a classification, not part of identity.
- [`../organization/organization.research.001.md`](../organization/organization.research.001.md) - the non-person collective.
