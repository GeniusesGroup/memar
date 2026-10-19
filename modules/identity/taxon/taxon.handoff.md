# Taxon Handoff

## Topic & Purpose

Conversion of the `modules/identity/taxon` domain from Go to Khayyam (Phase 2 of the Go -> Khayyam migration map), plus the state of its two classification edges. The domain's own definition is thin; what this handoff carries is what the conversion could not settle.

## Status

Active - protocol layer converted 2026-10-03; the edge vocabulary and the two loop-edge placement questions remain open.

## Decisions

- **`TaxonModel` composes `ThingModel` only (Decided).** The Go `taxon_p.Model` embedded `thing_p.Model` and `object_p.Model`, but `object_p.Model` is itself only `thing_p.Model`, so the second embedding adds no requirement. `modules/identity/object/protocol/model.kh` has not been converted, so no `ObjectModel` exists to import; writing `tp ObjectModel ab` here would be this domain claiming a concept another domain owns. - reason: an abstraction states requirements, and a requirement already implied by a composed requirement is not restated.
- **`Field_TaxonID` / `TaxonID` (Decided).** Go wrote `Field_TaxonID interface { TaxonID() UUID }` with a local `type UUID record_p.UUID`. The ~90 per-domain `UUID` declarations are one concept owned by the thing domain as `ThingUUID`, so the accessor returns `ThingUUID` and the local `UUID` is gone. - reason: qualified-names rule; one concept, one owner, never a second declaration at the import site.
- **`GenderModel` and `SexualityModel` compose `LabelModel` alone (Decided).** Go embedded `thing_p.Model` and `label_p.Model`; `LabelModel` already composes `ThingModel`, so `ThingModel` inside the block would restate a requirement the composition already carries. - reason: same as above; the requirement set is identical either way.
- **`Field_GenderID` / `GenderID` and `Field_SexualityID` / `SexualityID` (Decided).** The Go spelled them `Field_GenderUUID` / `GenderUUID()` and `Field_SexualityUUID` / `SexualityUUID()`; the repository's suffix convention is `Field_X` + `X` where the Go said `Field_XUUID`. Both return `ThingUUID`. - reason: the convention the converted domains already established; the repository-wide sweep that would make every domain consistent is still pending and was not started here.
- **`gender/validator.kh` left unconverted (Decided).** It is a Go `regexp.MustCompile` over a closed string list plus a matcher function. `gender.md` rules that the `Male`/`Female` pair is "a value list, not processing semantics ... never grounds a new module on its own", and Memar declares no pattern-matching abstraction for a validator to import. - reason: the domain document is the newer intent; the source is the older record.
- **`edges/sexuality/data/user-sexuality.kh` left unconverted (Decided).** The file holds nothing but 35 `Type_*` label constants - vocabulary as data, the same disposition as `identity/organization/edges/` and the rights label folders.

## Ambiguities Resolved

- **Does the taxon edge set need its own models, or is `ThingModel` enough?** - resolved: the two edges carry `Model` interfaces in Go, so they get `GenderModel` / `SexualityModel`; the taxon's own `Model` does not compose them, because the Go does not say a taxon *is* a gender or a sexuality - it says a taxon is *classified by* them, which is an edge, not an identity.

## Open Questions

- **`validator.kh`'s vocabulary contradicts `gender.md` (Explored-but-unresolved).** The regex accepts `Male|Female|Gay|Lesbian|Bisexual|Asexual|Other`; `gender.md` records only `Male` and `Female` as candidate values and the rest as belonging to the sibling `sexuality` edge. Either the validator was wrong when written, or `gender.md` understates the vocabulary. Nothing states which.
- **Should `taxon` compose `ObjectModel` once the object domain is converted (Deferred).** Decided above that it adds no requirement today; if the object domain's model grows one, taxon's is a one-line edit.
- **The `edges/` classification folders vs `edges-loop/` (Deferred).** The migration map's open questions list "tax labels" among the high-confidence kind errors - classifications filed under `edges/` that should be `edges-loop/`. `gender` and `sexuality` are classifications of one node, which is the loop-edge shape. The folder move is a Phase 0 review edit, not a Khayyam conversion, and was not made here.
- **Whether `Field_GenderID` should return a taxon-side identifier at all (Explored-but-unresolved).** `gender.md` asks whether gender attaches to `(taxon)` or to the organism/person instance. If the latter, the accessor belongs on the person domain and this one should go.

## Anticipated Work

- A repository-wide `Field_XUUID` -> `Field_XID` sweep, not started here.
- Conversion of `modules/identity/object/protocol/model.kh` and of the remaining unconverted domains, which several of the open questions above wait on.

## Assumptions

- **`record_p.UUID` and `thing_p.UUID` are the same value (Strong).** Every converted domain in the repository reads them as one identifier type.
- **`LabelModel` is the right requirement for a stored classification (Weak).** It rests on the Go embedding `label_p.Model`; if a classification turns out to be a plain thing with a type field, both edge models change.

## Key Definitions Established

- `TaxonModel` - what a taxon is, required: `ThingModel`.
- `GenderModel`, `SexualityModel` - what a stored gender/sexuality classification is, required: `LabelModel`.
- `Field_TaxonID`, `Field_GenderID`, `Field_SexualityID` - the surfaces that expose each concept's identity.

## Proposed Next Steps

1. Settle whether gender attaches to the taxon or to the person instance (`gender.md`).
2. Decide whether the classification folders move to `edges-loop/`, then apply the Phase 0 review move.
3. Delete `validator.kh` or replace it with a label-vocabulary check, once the vocabulary disagreement above is settled.

## Research 001 pointer (2026-10-18)
[estate.research.001.md](../estate/estate.research.001.md) analyses taxon with estate and person (scenarios T1 to T6; findings 1C, 2C, 3 and 5). Every item is Tentative, Explored or Deferred, none Decided; the Decided items above are untouched. Proposals: a taxon is a group asserted by an authority under a scheme, and an individual living thing is an organism related to it; a rank is a relation to a scheme with a label vocabulary (one relation, not ten loops); taxonomy is a pluggable rather than a kernel; gender and sexuality are not taxon attributes.

Questions for the owner, each with a default and what it blocks in the research's [Open Questions](../estate/estate.research.001.md#8-open-questions), under Taxon:
- **TN.1** - Is a taxon a kind (a group asserted by an authority) or an individual? Default: a kind; the individual is an organism. This also answers the open question above about where gender attaches.
- **TN.2** - Is a rank a relation to a scheme rather than ten loops? Default: yes.
- **TN.3** - Does a taxon revision use many-to-many `supersedes` with `same_as`/`distinct_from`, the name never being identity? Default: yes.
- **TN.4** to **TN.5** - Functional kinds as an organization's classification; published schemes adopted by `follow`.
- **TN.6** - Does taxon stay kernel (the survey's Q1) or become an identity pluggable? Default: a pluggable; `PersonModel` stops composing `TaxonModel`.

Contradictions found, reported and not resolved: taxon.md's first sentence ("any living things") against its quoted definition (a group); `eukaryote/eukaryote.md` headed "Plant"; gender and sexuality attached to a group.

## Related Artifacts
- [`estate.research.001.md`](../estate/estate.research.001.md) - the research behind the pointer above.


- [`taxon.md`](taxon.md) - the domain document.
- [`edges/gender/gender.md`](edges/gender/gender.md), [`edges/sexuality/sexuality.md`](edges/sexuality/sexuality.md) - the two classification edges.
- [`../thing/protocol/dt-uuid.kh`](../thing/protocol/dt-uuid.kh), [`../thing/protocol/model.kh`](../thing/protocol/model.kh) - the owners of `ThingUUID` and `ThingModel`.
- [`../../knowledge/label/protocol/model.kh`](../../knowledge/label/protocol/model.kh) - the owner of `LabelModel`.
- [`../../../Khayyam.practice.md`](../../../Khayyam.practice.md) - the seven governing rules this conversion followed.

## Notes

- Six files converted; all six `accept` from the Khayyam frontend (`frontend_check.ts`) against a resolved root.
- Nothing outside `modules/identity/taxon` was edited. `git` was not run.
