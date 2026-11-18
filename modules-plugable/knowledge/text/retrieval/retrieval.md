# Text Retrieval
## In one sentence
Given a query text (and optional typed filters), return **holders** that have matching indexed texts — without reading every text.

## Ask / answer
| You give | You get |
| --- | --- |
| Scope (which population of texts), query `Text`, optional field predicates, bound score service, holders to exclude, limit | Ordered `Text_Index_Hits` (each hit: holder + matched text id + opaque score) |

Pipeline: upsert services write derived **label postings** and **field values** for each `(scope, holder, text)`; `Text_Index_Store` reads them and retires entries; `Text_Index_Score_Service.Do` scores; widget `Text_Find_Holders.Find` builds that score call. Likeness is **not** part of this module.

Research task `20261103-T100549Z-14796`.

## Placement
- **Pluggable capability** under the Text mirror: `modules-plugable/knowledge/text/retrieval/`.
- **Not likeness.** Signature ranking is [Likeness](../likeness/likeness.md).
- **Not kernel Text.** Omitting this module does not change what Text means ([Kernel neutrality](/modules/knowledge/modularity/rules/kernel-neutrality/kernel-neutrality.md)).

## Where things live
| Place | Holds |
| --- | --- |
| Kernel [`modules/knowledge/text/protocol/`](/modules/knowledge/text/protocol/) | `Field_Text_Scope`, `Field_Text_Holder`, `Text_Holders`, `Field_TextID` |
| [`protocol/`](protocol/) | Shared field preds and the index store port (several services import them). Hit/Hits, score, and upsert write ports live under their services ([Protocol folder → Placement test](/modules/knowledge/protocol/rules/protocol-folder/protocol-folder.md#placement-test-refuse-the-main-folder)) |
| [`services/score-text-index/protocol/`](services/score-text-index/protocol/) | Score service + score / hit / hits |
| [`services/upsert-text-index-*/protocol/`](services/) | Upsert + `Replace` write ports |
| [`widgets/text-find-holders/protocol/`](widgets/text-find-holders/protocol/) | Find widget |
| [`edges/`](edges/) | Label-posting and field-value Data Models |

## Lifecycle
- **Replace** posting content: upsert ports only.
- **Retire** an entry: `Text_Index_Store.Retire*` only.

## Edges
- [Label posting](edges/label-posting/label-posting.md) — derived `(scope, holder, text, label)`
- [Field value](edges/field-value/field-value.md) — same entry key + Type_Identifier membership (v1)

## Model (Tentative)
- Index keys are [Label](/modules/knowledge/label/label.md).
- Score is opaque (`Before`). Counts/limits: `NumberOfElement`; positions: `Container_ElementIndex`.
- Context weighting = which score/analyzer/scope bind.
- Likeness floor: [Likeness_Ranker](../likeness/widgets/likeness-ranker/protocol/likeness-ranker.kh), not Find.
- Upsert takes **Labels**; widget `Text_To_Labels` (kernel Text: Fold → Lex → Label_Intern) turns text into labels before upsert. Keeper uses `Text_Holders_Of_Text`, not likeness types.

## For intelligent agents
Hits carry holder + text id for citation. Scorer is swappable without changing Find. Named ranking families stay out of Khayyam. Thresholds that need a 0–1 floor use likeness’s `FromUnitParts`, not retrieval’s opaque score. Index keys are Labels (word/phrase IR terms); a dense/subword path is another bind of the score/analyzer surface, not a redefinition of Label. Span offsets inside a text are kernel Token debt, not this hit shape. See research on task `20261103-T100549Z-14796`.
