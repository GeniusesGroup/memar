# Label Handoff

## Topic & Purpose

State of converting the label domain's own protocol — `modules/knowledge/label/protocol/` — from Go to Khayyam under the seven governing rules in [`../../../Khayyam.practice.md`](../../../Khayyam.practice.md): the vocabulary-or-contract question this domain raises, what the two converted files declare, which of those declarations were judgment calls, and what is still undecided or blocked on a domain this one does not own.

## Status

Active — `protocol/dt-uuid.kh` and `protocol/model.kh` are converted and return `accept` from the Khayyam frontend against a root where both import roots resolve. Nothing in this domain refuses. One requirement the Go source carried, `edge_p.Model`, could not be composed and is recorded below.

The other nine `.kh` files under `modules/knowledge/label/` are **not** this domain. `edges-loop/label/`, `edges/label-allowed/`, `edges/label-used_by/`, `edges/list/`, `edges/matrix/`, `edges/table/` and `widgets/categories/` each carry their own document (`<name>.md`) and their own `README.md`, which is the shape this repository gives a domain; the migration map's Phase 0 rule ("one folder per edge: `<name>/<name>.md` plus a one-line `README.md`") makes each of them its own domain. They are unconverted, and each of them now has a name to import from this domain.

## Decisions

- **Decided: the label protocol's Go declarations are contracts, not vocabulary, so the domain is converted.** The question was put directly — an edge label is data, not code, and this repository has already decided that registries of what a word means live outside this module — so it had to be settled whether `Field_LabelUUID`, `Field_LabelsUUID` and `Field_Type` were code or dictionary. They are contracts, on three counts. (1) They have consumers outside this domain that require behavior rather than describe meaning: `label_p.Field_LabelUUID` is composed by `label-allowed`, `invoice/edges/item`, `transaction/edges/reference`, `discount`, `good/edges/item-ingredient` and `page-friendship_cycle`; `label_p.Field_LabelsUUID` by `label/edges/table`, `economics/voucher` and two GUI pages; `label_p.Field_Type` by `computer/hardware`'s `ApplicationNode` and `instance_of/edges/address`'s `DataModel`, and written out in full at `instance_of/edges/resource` as `Type() label_p.UUID`. (2) Each names a record identity, so each is a required operation on a data model rather than a fact about a word — the vocabulary of a label is the registry's, and no code here adds to it. (3) The thing this module keeps, the attachment `(thing)-[:label]`, needs an identifier to be stored at all. So the domain is code, and the registries stay documents.
- **Decided: this domain declares no UUID of its own.** `protocol/dt-uuid.kh` includes `ThingUUID` from the thing domain rather than declaring a `LabelUUID`. Reason: the Go `type UUID record_p.UUID` restates the storage record UUID that `thing/protocol/dt-uuid.kh` already owns and states "MUST be unique ID in all domains"; a second value abstraction over the same identifier would be two abstractions claiming one concept, the architecture error rule 3 names. `time`, `uri`, `text` and `calendar` already took this route; `organization` re-imports the user domain's `UserUUID`, which is the same collapse one step along the chain. Every `label_p.UUID` in the tree — about thirty use sites across `storage/graph`, `rights/contract/edges/terms`, `question/edges/rating-labels`, `language-human` and the GUI pages — is this same identifier and now spells it `ThingUUID`.
- **Decided: `Field_LabelUUID` and `Field_LabelsUUID` become `Field_LabelID` and `Field_LabelsID`, with accessors `LabelID` and `LabelsIDs`.** The suffix follows the accessors this repository's converted files already use (`ThingID`, `ThingsIDs`, `UserID`, `TextID`, `CalendarID`, `URIID`); the corpus carries `Field_…UUID` in some files and `Field_…ID` in others, and one spelling had to be chosen. The plural accessor takes the plural on the noun and leaves `ID` last, matching `ThingsIDs`.
- **Decided: the plural surface returns `Array_ThingUUID`, a named type composing memar's `Array_Dynamic`, not `Array_Dynamic ThingUUID`.** Khayyam abstractions carry no type parameters, so a `[]T` has no spelling; the composition is the route the thing pilot took.
- **Decided: `Field_Type` becomes `Field_LabelType` with accessor `LabelType`.** A rename, not a bare name carried over. Bare `Field_Type` is ambiguous in the corpus — `thing/edges/criterion`, `question/edges/rating`, `service/edges/seat`, `matching_system/edges/trade` and `economics/product/edges` each declare a `Field_Type` of their own over a local `Type`, and a sixth domain's `Type` accessor would meet them; qualified-names treats a bare name another module has taken as an architecture error to be qualified at the definition site, never aliased at the import. Qualifying the word rather than the whole name gives `Field_LabelType`, which keeps the `Field_*` prefix rule 2 relies on and states the concept (the label that types this record) without relying on the directory to supply it. The bare accessor `Type` would have collided the same way, and `text_type` is about to declare a `Type` abstraction of its own over this same identifier.
- **Decided: `LabelModel` composes `ThingModel` only; the Go `edge_p.Model` requirement is not composed, because the edge domain declares nothing that could be composed.** In Go, `edge_p.Model` is `interface { thing_p.Model }` — an empty interface — so `label_p.Model` required nothing that `thing_p.Model` did not already require, and the composition carried no requirements. Writing `tp EdgeModel in "modules/knowledge/edge/protocol/model.kh"` was tried and refuses `name-not-declared`: that file declares nothing yet. Declaring `EdgeModel` here instead would be a competing abstraction for a concept the edge domain owns, which the qualified-names rule forbids. So the requirement is dropped from the code and recorded below; the Go source keeps it.
- **Rule 6, recorded rather than papered over:** `LabelModel` composes `ThingModel` and adds nothing of its own, so it is an empty extension point in the sense rule 6 warns about — the pilot `ThingModel` is already incomplete, and this makes it incomplete twice over. What the label domain actually needs and does not yet have: a label is the attachment `(thing)-[:label]`, and nothing declares what the attachment requires beyond the two things it joins — no lifecycle of assigning, changing, or removing a label, no authority over who may do it, and no requirement on the record that holds the attachment. The `list.md` document already asks whether label-update authority is a rights rule, and that question is the same one this `ab` is standing in for.
- **Rule 5 extraction:** the one Go comment in this domain, `// Label text indicate in 'text' domain.`, was carried on `type UUID`, and is now a section of [`label.md`](label.md) instead of a comment above the code. The same edit added the two statements the documents were missing and the code implies: a label's type is itself a label, and a label's text is reached in the text domain.

## Ambiguities Resolved

- Whether a label's type is a label or a kind of its own: it is a label. `edges/table` and `edges/matrix` both model the typed end as `(label)` — `(label)-[:column_of]->(label(table))` and `(label)-[:row_of]->(label(matrix))` — and `text_type`'s `Type` is this domain's `UUID`. So the type of a label is reached through this domain's own identifier, which is why `Field_LabelType` returns a label identity and not a new value type.
- Whether `Field_LabelsID` (a list of labels) belongs in this protocol or in the storage protocol: here. `storage/graph/protocol/data_model.kh` writes `Edge() label_p.UUID` and `Edges() []label_p.UUID` over the same identifier, so the plural surface this domain declares is the one those records are read through, and splitting it would leave two spellings of one requirement.
- **The edge requirement had no home until the edge domain converts** — answered (2026-10-08): the premise is stale; the edge domain has converted. `modules/knowledge/edge/protocol/model.kh` now declares `tp EdgeModel ab { ThingModel; Field_EdgeID }`, so `LabelModel` can compose it — the one-line change this bullet awaited, which is also step 1 of `edge.handoff.md`'s Proposed Next Steps. The three consumers it names (`modules/knowledge/label/edges/table/protocol/model.kh`, `modules/identity/taxon/edges/{gender,sexuality}/protocol/model.kh`) are unaffected.

## Open Questions

- What behavior a label-as-an-edge requires of the record that holds it. Rule 6 says design before conversion; the domain document describes the attachment and the registries and does not answer this, and no implementer exists to say which lifecycle it needs.
- Whether `Field_LabelsID` is a collection of label identities or of labels attached to one thing — the first is what the Go signature says, the second is what every caller seems to want, and the two are the same only when the record holds all of them. `widgets/categories` writes `CategoriesID() []label_p.UUID` and `question/edges/rating-labels` writes `Labels() []label_p.UUID`, which are per-record lists rather than free-standing ones.
- Whether a label's type may be absent. Every use found types the record (`hardware` node type, `instance_of/address` type, `text_type`), and nothing declares an untyped label; if the untyped case is real it needs its own statement rather than an empty identity.

## Assumptions

- **`ThingUUID` is the name the thing domain declares** — stability: Strong. `modules/identity/thing/protocol/dt-uuid.kh` is already converted and declares it.
- **`ThingModel` is the name the thing domain declares** — stability: Strong, same file.
- **`Array_Dynamic` is the name memar declares at `memar/modules/computer/adt/array/protocol/dynamic.kh`** — stability: Strong. Read off the converted thing pilot, and the file exists.
- **The `org/` and `memar/` import roots resolve through a manifest that does not exist in this repository** — stability: Strong, and named as the hard gate by rule 7 of the migration map. Every converted file in the tree refuses `unresolved-import` when the frontend is run against the checkout as it stands; that is the missing-manifest condition, not a defect in these two files.

## Proposed Next Steps

1. Convert `modules/knowledge/edge/protocol/model.kh` to declare `EdgeModel`, then add `EdgeModel` to `LabelModel` here.
2. Design what a label requires as an edge — assignment lifecycle and update authority — and give `LabelModel` a requirement beyond `ThingModel`, which is what rule 6 asks for.
3. Sweep the `Field_*ID` versus `Field_*UUID` suffix across the repository in one pass; this domain picked `…ID`, and the converted files currently carry both.
4. Convert the label domain's edge domains (`edges/label-allowed`, `edges/list`, `edges/table`, `edges/matrix`, `edges/label-used_by`) and its `widgets/categories`, each of which now has `Field_LabelID`, `Field_LabelsID`, `Field_LabelType` and `LabelModel` to import.

## Research 001 questions and next steps (2026-10-18)

### Status
Proposals only, from [label.research.001.md](label.research.001.md) (ten scenarios, a three-element kernel, six rival-model choices, a mapping of every label, status and edge folder, thirty-two test scenarios, a reconciliation with the sibling researches, eighteen contradictions). The research covers label, status and edge as one cluster; [status](../status/status.handoff.md) and [edge](../edge/edge.handoff.md) carry a pointer only. Nothing is ratified; every item is **Tentative**, **Explored** or **Deferred**, none Decided. Settled facts above are not re-argued.

### Open Questions raised by the research
Each carries a recommended default and what it blocks; the full text is in the research's [Open Questions](label.research.001.md#8-open-questions). Ordered by what they change.

1. **Is a label an identity used as the type of a loop-edge, a vertex reached by a generic edge, or a word held in code?** Default: the first; a label may also be a vertex that relations start from. Blocks: the label loop's Model line, every `label_p.UUID` consumer, what `Field_LabelsID` means, the status wording.
2. **Who may attach and withdraw a label, and where is that stated?** Default: in the label's definition, by reference to a rule through `condition_is`, with the vocabulary's default as fallback; withdrawal is a new fact. Blocks: whether the `label` edge exists under "no bare edges", the registries' "registration does not decide who may attach", `list`'s authority question.
3. **Is a status a label of kind `Status` with a transition event and a read guarantee, a separate mechanism, or folded into label?** Default: a label kind. Blocks: the status wording, survey ruling R4, the researches that wait on R4.
4. **Is a label's identity per meaning, per wording, or per wording and kind; who decides two labels mean the same?** Default: per meaning; equivalence is an authorized, dated assertion. Blocks: merge and split, the four `Blocked` meanings.
5. **Is `Field_LabelsID` the free-standing set of label identities or the labels one record carries?** Default: the labels one record carries. Blocks: the table, categories and rating-labels models; the second open question above.
6. **What does `LabelModel` name: the label, or the record that carries an attachment?** Default: the label. Blocks: whether `LabelModel` gains `EdgeModel`, the consumers' `.kh`.
7. **Is a label's kind required and itself a label, with a root kind that takes itself?** Default: yes. Blocks: `Field_LabelType` being total; the third open question above.
8. **Does the ordered, owned list leave the kernel as a `collection` pluggable shared with content?** Default: yes. Blocks: `list`, the content `album`/`serial` reclassification.
9. **Do scope, adoption and standing become a `vocabulary` pluggable that absorbs `label-allowed`, `label-used_by` and the registries?** Default: yes. Blocks: `label-allowed`'s open question, `CNF_DefaultAllowed`, the registries' placement.
10. **Is a private label a label with a one-person scope?** Default: yes, promotable by a succession. Blocks: `list`'s "label own by User(Omid)", the categories widget.
11. **Do table and matrix leave the label domain (stage vocabulary the task domain's, board the GUI's)?** Default: yes. Blocks: the two edge documents.
12. **Where is the line between a shared status and a domain's own?** Default: a flag any record may take is shared; a lifecycle a domain owns is that domain's. Blocks: R4, the three `status/edges/` folders.
13. **Is the shared `block` kept?** Default: kept and defined; the other three `Blocked` are different labels. Blocks: user, group and task contradictions.
14. **Is `deleted` a flag a domain may take, and `edited` derived?** Default: yes and yes. Blocks: the two documents' methods, the content delete question.
15. **Do `request`, `suggest`, `approved` and `approval_needed` become one `approval` capability?** Default: yes. Blocks: the four documents, the task completion rule.
16. **What is an edge for, and are its ends and its type requirements of `EdgeModel`?** Default: yes, a thing joining two ends typed by a label. Blocks: the edge handoff's Rule 6 entry, `EdgeID` against `LabelID`.
17. **Are `loop_edge` and `preference` kept?** Default: `loop_edge` derived and retired; `preference` kept. Blocks: the two documents.
18. **Is attestation a second capability beside `certificate` or the same one?** Default: the same, generalized. Blocks: the certification cases.
19. **May a rule attach a label, and does a person's attachment outrank it?** Default: yes and yes. Blocks: the detectors' contract, degree labels.
20. **Is the subject's right to see, contest and withdraw an ascribed label a kernel rule?** Default: yes, stated once. Blocks: the taxon gender and sexuality edges.
21. **Does hiding a label hide that it was applied, and do counts and facets obey it?** Default: yes. Blocks: search and facet design.
22. **Does a label carry data (weight, score), or is that a second fact about the attachment?** Default: a second fact. Blocks: the probability note in thing labels.
23. **What happens to attachments when their label is merged, split or retired?** Default: they stay readable as of their date and point to the successors. Blocks: vocabulary decay, scheme editions.
24. **Is there a `scheme` pluggable (broader and narrower)?** Default: hold until a hierarchical vocabulary is adopted. Blocks: `taxonomic_rank`.
25. **Are valid time and recorded time both kept for an attachment?** Default: yes. Blocks: late-known labels, backdated certifications.
26. **Is `text-type` defined, and by whom?** Default: a label kind defined in the text domain. Blocks: the Type section above, the text research's question 12.

### Next Steps from the research
1. Answer questions 1 to 3 together with the text (1, 2), content (1, 2, 7, 10) and product (admission statuses) questions: they fix what `LabelModel` names, the meaning of "classification" for every importing domain, and survey ruling R4.
2. Compose `EdgeModel` in `LabelModel` (one import and one composition line); it is no longer blocked, and the first Next Step above is therefore open and doable without an answer. Record that the `Array_ThingUUID` duplicate the edge and estate handoffs name is already gone.
3. Fix the label loop's Model line and the status documents' fragments and Model lines (survey task T1), using the research's mapping as the reading list; none needs an answer.
4. Write Placement and Open questions in the label edge documents that lack them (survey task T5), marked candidate until questions 8, 9 and 11 are answered.
5. After question 2, write the contract section of the label loop and add the attacher kind; after question 3, write the transition section of the status document.
6. Ask the owner about question 8 together with the content research's question 10 before touching `list`: it moves a decided relation's home.
7. Read what the research did not: the bodies of the eight sibling researches outside the passages cited, `certificate`, `detection-toxicity`, `authorization`, `access-control`, `follow` and `delegate`, and `storage/graph` beyond its data model; record anything that changes a Tentative item.

## Related Artifacts

- [`label.research.001.md`](label.research.001.md) — the conceptual development of the label, status and edge cluster whose questions and Next Steps are above.
- [`../../../Khayyam.practice.md`](../../../Khayyam.practice.md) — the seven governing rules.
- [`label.md`](label.md) — the domain document; its Taxonomies paragraph and the two sections added by this conversion.
- `modules/identity/thing/protocol/dt-uuid.kh`, `modules/identity/thing/protocol/model.kh` — the owner of the identifier and the base model this domain includes.
- `modules/knowledge/text/protocol/dt-uuid.kh`, `modules/knowledge/time/protocol/dt-uuid.kh`, `modules/identity/uri/protocol/dt-uuid.kh` — the sibling conversions that answered the UUID question the same way.
- `modules/knowledge/edge/protocol/model.kh` — must declare `EdgeModel`.
- `modules/knowledge/label/edges/list/list.md` — where the label-update authority question this domain's `Model` stands in for is already asked.
- `modules/knowledge/text/edges/text_type/protocol/dt-type.kh` — its `Type` is this domain's identifier; it becomes `ThingUUID` and now resolves.

## Notes

- The frontend was run through `node modules/khayyam/targets/go/frontend_check.ts` against a root built by copying every `.kh` of this repository into `org/` and every `.kh` of the memar repository into `memar/`, preserving relative paths. `protocol/dt-uuid.kh` and `protocol/model.kh` both return `accept`.
- Five consumer files were checked by override against these two files, to confirm the names this domain exports are the ones the tree asks for: `text/edges-loop/query/protocol/model.kh` (`LabelModel`), `text/edges/text_type/protocol/dt-type.kh` (`ThingUUID`), `text/widgets/text/protocol/gui-widget.kh` (`Field_CommentID`, from the comment edge), `label/edges/table/protocol/data_model.kh` (`Field_LabelsID`), and `instance_of/edges/address/protocol/data_model.kh` (`Field_LabelType`). All five accept. These overrides are checks, not edits — none of those files was written by this conversion.
- The `EdgeModel` composition was tried and refused `name-not-declared` against this root, which is the finding recorded under Decisions.
- `abstraction_bridge.py go-to-khayyam` was not used for these two files; the names in them are read off the domain's consumers and the converted files already in the tree, not off tool output.
- The `// TODO(go-migrate):` block is left in place in both files, per the conversion brief and memar's `go-clue-residue` rule.
