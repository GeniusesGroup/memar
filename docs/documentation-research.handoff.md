# Documentation — Research Handoff

## Topic & Purpose
The Research facet's specification was drafted and confirmed in one working day (2026-09-08): Omid Hekayati stated the requirements, Super Z drafted [documentation-research.md](./documentation-research.md), the owner's first review confirmed the draft and moved `Method` into the mandatory core as `Methodology`, and the facet was registered as the fifth facet in [documentation.md](./documentation.md). The settled decisions and their reasoning live in [documentation-research.changelog.md](./documentation-research.changelog.md) and [documentation.changelog.md](./documentation.changelog.md); this handoff carries the design edge cases that remain open.

## Status
Active

## Open Questions
- Whether Findings need their own confidence vocabulary, distinct from the Handoff facet's decision confidences — currently a finding's tentativeness lives in its own wording. Suggested path: decide when the first real research shows whether wording suffices.
- The reopen-versus-supersede edge: a frozen research whose question reopens — supersession is the drafted rule, but a finding that graduated into a base document and was later invalidated may deserve its own path. Suggested path: rule when the case first appears.
- A changelog entry citing an Active research as `Evidence`: the research is mutable working state, so the provenance a change relied on can shift after the entry is written. Git history covers the audit trail, but whether an entry may cite only Complete researches — or Active ones with a stated caveat — is undecided. Suggested path: rule when the first citation attempt happens.
- Whether a research may exist without a single governing base artifact (a truly cross-cutting question) — the drafted rule pairs every research to a base, and no counter-case has appeared yet. Suggested path: if a real question resists pairing, decide whether the most central governing document suffices.

## Anticipated Work
- A paired practice document (`documentation-research.practice.md`) once real researches show the producing procedure — deferred, not drafted now, because no research procedure has accumulated yet.
- The first real research, as the specification's test case.

## Proposed Next Steps
- Open a first research against a real subject to exercise the structure.

## Assumptions
- Every researchable question has a governing base artifact to pair with — Weak: a truly cross-cutting inquiry would strain the pairing rule (see Open Questions).
- Researches per base will in practice remain few enough that three-digit ordinals suffice — Strong.

## Related Artifacts
- [documentation-research.md](./documentation-research.md) — the confirmed specification this handoff carries state for.
- [documentation-research.changelog.md](./documentation-research.changelog.md) — the founding entry with the deliberation and the rejected alternatives.
- [documentation.md](./documentation.md) — the meta-layer; the facet is registered there as the fifth.
