# Documentation — Research Handoff
## Topic & Purpose
The Research facet's specification was drafted and confirmed in one working day (2026-09-08): Omid Hekayati stated the requirements, Super Z drafted [documentation-research.md](./research.md), the owner's first review confirmed the draft and moved `Method` into the mandatory core as `Methodology`, and the facet was registered as the fifth facet in [documentation.md](../documentation.md). The settled decisions and their reasoning live in [documentation-research.changelog.md](./research.changelog.md) and [documentation.changelog.md](../documentation.changelog.md); this handoff carries the design edge cases that remain open.

## Status
Active

## Open Questions
- **Whether the criterion needs a further test for a record whose sources are external but whose method is a survey of this project's own documents.** [documentation-research.md -> What Qualifies as an Inquiry Worth This Facet](./research.md#what-qualifies-as-an-inquiry-worth-this-facet) requires material from outside this project *and* a method this project's vocabulary does not supply, and three records that failed the second half were re-surveyed into their artifacts' changelogs and removed: the Go-group claim corpus in [Framework Changelog](../../../../docs/framework.changelog.md#the-go-group-claim-corpus-audited-against-the-documents-and-its-residue-recorded-here), the placement survey in [Knowledge Changelog](../../knowledge.changelog.md#material-with-no-producing-decision-a-placement-survey-and-what-knowledge-already-holds), and the four-discipline survey in [Process Changelog](../../../process/process.changelog.md#four-disciplines-surveyed-against-process-modeling-and-their-practices). Whether a two-part test is the right cut, or whether the second part should be dropped and the criterion left to the first, is unsettled - and now that such a survey is recorded in the changelog, the question is sharper, because a session that runs one now has to decide whether it was a research or an entry.
- What is **not** open: [rule.research.001.md](../../../process/rule/rule.research.001.md) meets the criterion and is untouched. An earlier note in this file named it as failing, on the strength of a count of URLs; its sources are the SBVR and Business Rules Group vocabularies and the production-rule literature, cited by name, and the criterion is about what was read rather than about whether a link was pasted. The three renames were made only after re-reading each record's own Methodology section.
- The reopen-versus-supersede edge: a frozen research whose question reopens — supersession is the drafted rule, but a finding that graduated into a base document and was later invalidated may deserve its own path. Suggested path: rule when the case first appears.
- Promotion and withdrawal criteria for researches: when an Active inquiry graduates, when it is Withdrawn, and who decides — so open researches do not accumulate as a parking lot.
- A changelog entry citing an Active research as `Evidence`: the research is mutable working state, so the provenance a change relied on can shift after the entry is written. Git history covers the audit trail, but whether an entry may cite only Complete researches — or Active ones with a stated caveat — is undecided. Suggested path: rule when the first citation attempt happens.
- Whether a research may exist without a single governing base artifact (a truly cross-cutting question) — the drafted rule pairs every research to a base, and no counter-case has appeared yet. Suggested path: if a real question resists pairing, decide whether the most central governing document suffices.

## Anticipated Work
- A paired practice document (`documentation-research.practice.md`) once real researches show the producing procedure — deferred until at least one real Research has been reviewed and further use reveals whether a repeatable procedure has accumulated.
- Execution Research 001 — M1 readiness of the Khayyam specification (`bundles/khayyam/khayyam.research.001.md`) is the current real Research in the working tree. It is Active and has not yet closed the facet-level questions tracked here.

## Proposed Next Steps
- Review `bundles/khayyam/khayyam.research.001.md` and record its outcome on that research artifact.
- Use the reviewed outcome to decide whether Findings need a confidence vocabulary and whether enough accumulated practice exists to begin this facet's paired Practice document.

## Assumptions
- Every researchable question has a governing base artifact to pair with — Weak: a truly cross-cutting inquiry would strain the pairing rule (see Open Questions).
- Researches per base will in practice remain few enough that three-digit ordinals suffice — Strong.

## Related Artifacts
- [documentation-research.md](./research.md) — the confirmed specification this handoff carries state for.
- [documentation-research.changelog.md](./research.changelog.md) — the founding entry with the deliberation and the rejected alternatives.
- `bundles/khayyam/khayyam.research.001.md` — the current real Research test case; it is Active and awaiting owner review, so it has not yet closed the questions in this handoff.
- [documentation.md](../documentation.md) — the meta-layer; the facet is registered there as the fifth.
