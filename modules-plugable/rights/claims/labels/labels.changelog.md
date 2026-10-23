# Claim Labels Changelog

## Changelog

### Registry of claim-type labels
- Time: 2026-09-27T15:40:00Z
- Type: Added
- Cited:
  - [Label](../../../../modules/knowledge/label/label.md) - Relation: Depends_on: attachment stays that domain's label edge
  - [Case](../../../../modules/rights/case/case.md) - Relation: Depends_on: a label is not a second kind of case
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — required one folder per claim-type label, including complaint
  - [Grok](../../../../CONTRIBUTORS.md#grok) (Grok 4.7 via Cursor) — wrote

#### What changed
The module registers complaint (shekvaieh) as a claim-type label. Civil and criminal are not registered. Attachment uses the existing label edge.

#### Deliberation
Owner: claim-type labels, including a complaint label, each get a folder on the pattern of law labels. Civil versus criminal is a label, and a subtlety about that split stays open, so those two words are not written here.

### Civil versus criminal stays a label
- Time: 2026-09-27T16:20:00Z
- Type: Changed
- Cited:
  - [Claim labels](labels.md) - Relation: Depends_on: the two words stay unregistered
  - [Case](../../../../modules/rights/case/case.md) - Relation: Depends_on: one adjudication model
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — required the label, and required execution as a compelled service whose input is not only a number
  - [Grok](../../../../CONTRIBUTORS.md#grok) (Grok 4.7 via Cursor) — wrote

#### What changed
The open subtlety is closed as a numeric constraint. It is not one. Civil and criminal stay unregistered. Execution stays one compelled service.

#### Deliberation
Owner, evening of 2026-09-27: civil versus criminal stays a label. The subtlety is not numbers. A folder that defined a second procedure is not written. Which labels exist stays pluggable.

### The numeric-constraint close is withdrawn and the question reopened
- Time: 2026-10-07
- Type: Reverted
- Cited:
  - [Case research 005](../../../../modules/rights/case/case.research.005.md) - Relation: Evidence: ICC Article 78(3) merges counts into one sentence, so a total is not the sum of per-count terms
  - [Case research 007](../../../../modules/rights/case/case.research.007.md) - Relation: Evidence: no consulted English source merges the split on computer or agent grounds
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) - said on 2026-10-07 that he is not certain the subtlety was closed, and left it open for a later review

#### What changed
The entry "Civil versus criminal stays a label" recorded the subtlety as closed because it was not a numeric constraint. That close is withdrawn. The label decision stands: civil versus criminal is a label and not a different adjudication model, and execution is one compelled service for either word. What is withdrawn is the claim that the split carries no numeric constraint. The question is open on [claim-labels.handoff.md](labels.handoff.md) as question 1, and the statement that it is not a numeric constraint is out of [claim-labels.md](labels.md), [case.md](../../../../modules/rights/case/case.md), [complaint.md](../../../../modules/rights/case/edges/complaint/complaint.md), and the case handoff.

#### Considered and not done
- **Naming the joint numeric remedy floor as the subtlety** (not done): the candidate is recorded as the only one any consulted source names, not as the answer. Whether it would force a different edge rather than a different label is exactly what is open.
- **Correcting the earlier entry instead of appending this one** (not done): the earlier entry is the record of what was decided that evening, and a changelog entry is not rewritten when its outcome is later withdrawn.

#### Deliberation
Owner, 2026-10-07: not certain the subtlety was ever closed, so it stays open for a later review. The label decision is untouched; nothing about one adjudication model changes. The two words stay unregistered, and registering them was never required for that.

---

### Claim labels fold into claims
- Time: 2026-10-20T07:00:00Z
- Type: Moved
- Cited:
  - [Modules Research 001 → Owner decisions needed](../../../../.agents/tasks/20261019-T191746Z-12632/docs/modules.research.001.md#6-owner-decisions-needed) - Relation: Depends_on: ruling D4 and answer Q17
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — ruled the placement
  - [Claude](../../../../CONTRIBUTORS.md#claude) (Opus-5.5 via Claude Code) — moved and wrote

#### What changed
`modules-plugable/rights/claim-labels` moved to `modules-plugable/rights/claims/labels` with `git mv`, its documents renamed `labels.md`, `labels.handoff.md` and `labels.changelog.md`; [claims](../claims.md) took a manifest.

#### Deliberation
A part never stands as a sibling of its module, and claim labels name the claim types that are the edges of claims.
