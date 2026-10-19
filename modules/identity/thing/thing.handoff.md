# Thing Handoff

## Topic & Purpose

Conversion of the `modules/identity/thing` domain from Go to Khayyam (Phase 2 of the Go -> Khayyam migration map), and — because this is the domain every other domain's identity and model chain hangs from — the state of the thing domain's own unanswered questions. Nothing here changes what a thing is; it records what the conversion could not settle.

## Status

Active — protocol-layer surfaces converted 2026-10-03; `ThingModel` still states no behavior of its own, and the domain's storage and service contracts are still unexpressed.

## Decisions

- **`ThingModel` left exactly as it was: `tp ThingModel ab` (Decided — to leave it).** Its Go interface was empty, and rule 6 forbids translating an empty Go interface into an empty `ab` *and* inventing requirements in its place. The file was not reconverted; the only edit was removing the two English comment lines that sat above the declaration, which rule 5 sends to a document (their content is the migration map's governing rule 3: there is no bare `Model`, each domain states its type in full). - reason: eleven converted domains already import this file by name; changing its shape is a change every one of them would have to re-read, and the missing behavior is a design question, not a conversion task.
- **`dt-uuid.kh`, `model.kh` not touched (Decided).** They were already converted; `ThingUUID`, `Field_ThingUUID`, `ThingID`, `Array_ThingUUID`, `Field_ThingsUUID`, `ThingsIDs` and `ThingModel` keep their names and stay the single owner of the thing's identity.
- **`QuiddityID` was not declared; the service request composes `Field_ThingUUID` instead (Decided).** `service-get.kh` asked for `QuiddityID() [16]byte`. That `[16]byte` is the thing's own base identifier, so a second accessor name for it would be one concept under two names in one domain. The quiddity vocabulary itself is already carried by `thing.md`'s Quiddity section. - reason: qualified-names rule; a name another file brings in by name must not collide, and `ThingID` is already that name here.
- **`Service_Get_Request` composes `Field_ThingUUID`; `Service_Get_Response` composes `ThingModel` (Decided).** The Go wrote `Service_Get_Response = QuiddityDomain`, an alias for this domain's own record, so the response of "get quiddity" is a thing.
- **`Field_CountUnitID`, `Field_FinancialCurrencyID`, `Field_TemplateID`, `Field_SubjectID` + `Field_SubjectsID` (Decided).** Four loop/edge folders carried a `Field_*UUID` surface over their own copy of `UUID`; each now returns `ThingUUID` under the `Field_X` + `X` suffix convention.
- **`edges/template`'s `Field_UUID` became `Field_TemplateID` (Decided).** The Go declared `type Field_UUID interface { TemplateID() UUID }` — a field named for the type while its method named the concept. Every other domain follows `Field_X` + `X`; keeping `Field_UUID` here would be the one file that does not.
- **`criterion/protocol/dt-type.kh` and `dt-point.kh` converted to `Criterion_Type` / `Criterion_Point` (Decided).** `Type` is claimed by thirteen other modules' `dt-type.kh` and `Point` by none but reads as a generic quantity; the qualified-names rule keeps a module prefix where the bare name is ambiguous, and the identifier-naming rule requires a name to state its own domain meaning. - reason: the module path segment is `criterion`, which is also the concept.
- **The `Criterion_Type` and `Criterion_Point` value lists went to `criterion.md`, not to `vr` (Decided).** Both are abstractions, so no constant can be a value of them at the protocol layer; the closed lists are vocabulary the implementation layer realizes. Rule 5 sends them to the domain document, which is where they now are.
- **`criterion/protocol/data_model.kh` and `storage.kh` left unconverted (Decided).** Both need `Field_TaskID`, which the unconverted `modules/management/task` domain has not declared; naming a task identifier here would be this domain claiming a concept another domain owns. - reason: qualified-names rule; an import of a name the target does not declare refuses with `name-not-declared`, and inventing the name would be worse.
- **`protocol/storage.kh` and `protocol/service-register.kh` left unconverted (Decided).** Between them they need three things that no file in the repository declares: a media-type *identity* abstraction (Go: `libgo/protocol.MediaTypeID`, for the criterion "Domain MediaTypeID e.g. product, content, ... domain"), the request identity accessor `Field_RequestID` (`modules/computer/request/protocol/dt-uuid.kh` is unconverted), and `Time` from a libgo path. `Field_QuiddityID`'s one convertible member was not extracted on its own, because a data model with one of four fields says less than the clue block it replaces.
- **`internal/storage/`, `services/`, `_import/` left unconverted (Decided).** These are the implementation layer (migration map Phase 3, blocked by rule 7) and, in `services/*/req.kh`, generated `//libgo:impl protocol.Syllab` / `protocol.JSON` serializers (Phase 4: migrate the generator, regenerate last). Converting them now would fossilize a pattern, which is exactly what rule 7 exists to prevent.

## Ambiguities Resolved

- **Should `ThingModel` have been given requirements from the Go's `Storage_Fields` / `Service_Get_Response`?** — resolved: no. Those are storage and service contracts, not the identity of a thing; attaching them to the model would make every domain that embeds `ThingModel` inherit a storage surface. The Go's empty interface is the record; the requirement is the open question below.

## Open Questions

- **What must a thing offer? (Explored-but-unresolved — the keystone question.)** `ThingModel` is `ab` with no composition and no methods, so it is satisfied by any capsule that declares nothing at all — eleven domains compose it and every one of them is, today, extending nothing. The Go interface it came from was empty. What a thing actually has to offer is undecided, and at least four candidates are live in this repository, none of them stated as the answer:
  - **Text.** `knowledge/text/protocol/model.kh` composes `ThingModel` and then adds `Field_TextID` + `Field_Text`. If every thing has a name, that name is a text and `TextModel` belongs *inside* `ThingModel` — which would make `TextModel` a specialization rather than a sibling.
  - **A media type.** Every libgo-based service in `services/` calls `s.MediaType.Init(...)` and `SetDetail(...)` — the thing is addressed by a media type before anything else happens to it. `computer/module/protocol/bs.kh` already gives a module `Identifier_MediaType`, so the concept exists in memar as a *value*, but nothing states that a thing must have one.
  - **Request/time audit.** `protocol/storage.kh` gave the record `QuiddityID`, `DomainID`, `Time`, `RequestID`, and the converted `DelegateDataModel` / `TextDurationDataModel` both compose `Observer_RequestID` + `Observer_Time_Request`. If those are attributes of every stored record, they are attributes of a thing — but they may equally belong to the *record* rather than to the thing, and this repository distinguishes those two nowhere.
  - **Naming.** Nothing in Khayyam yet carries the `name`/`title`/`summary` surface that `thing.md`'s "Quiddity ... what it is" implies, and no `Field_Name` exists anywhere in the corpus.

  This is a question for the owner of the thing domain, not for a converter. Whatever is chosen lands in `thing/protocol/model.kh` and every importing domain re-reads it.
- **Is "quiddity" a second name for "thing", or a third concept? (Explored-but-unresolved.)** `thing.md` treats Quiddity as the essence of a thing, but the Go source names the same `[16]byte` identifier `quiddityID` in the storage and service code while `dt-uuid.kh` calls it the thing's `UUID`. The domain document's whole vocabulary is "thing"; the code's is "quiddity". If they are one concept, one of the two names should retire; if quiddity is the essence and thing the whole, nothing currently says so.
- **Does a thing's identity need to be a concept at all, or is `ThingUUID` enough? (Deferred.)** `ThingUUID` is `ab` with no requirements too, for the same reason — its Go type was `record_p.UUID`, an opaque record identity. An identifier's behavior (uniqueness across domains, ordering, parse/format) is unstated.
- **What happens to `_import/`? (Deferred.)** `modules/identity/thing/_import/` holds 19 files of retired quiddity code (`quiddity-status`, `quiddity-substitute`, `quiddity-complement`, `asset/data-credit`, plus two `_import` copies of `user-request*` under `modules/computer/request/_import/`). Whether it is kept as a record or deleted is a Phase 0 content decision, not a conversion.
- **`Field_XUUID` -> `Field_XID` sweep (Deferred).** The suffix convention is applied file by file as domains convert; a repository-wide pass is pending and was deliberately not started.

## Anticipated Work

- An owner ruling on what `ThingModel` requires, then the edit to `modules/identity/thing/protocol/model.kh`.
- A media-type *identity* abstraction in memar or in `modules/identifier/mediatype` — without it `protocol/storage.kh` and `protocol/service-register.kh` cannot be expressed.
- Conversion of `modules/computer/request` and `modules/management/task`, which unblock the thing domain's storage and criterion contracts.
- Phase 3/4 work on `internal/storage/` and the service generators, once rule 7 is lifted.

## Assumptions

- **`QuiddityDomain` (the Go alias for the get-service response) is this domain's own model (Weak).** The Go package for `modules/identity/thing/protocol` was `thing_p` while the services imported `modules/quiddity-domain/protocol`, so the two are the same module under two names from the repository's rename history. If `QuiddityDomain` was in fact a separate record type, `Service_Get_Response` is wrong and should be re-derived.
- **`[16]byte` in the quiddity service and storage code is `ThingUUID` (Strong).** It is the same fixed 16-byte identity `dt-uuid.kh` describes, and no other domain claims it.
- **Every `.kh` file in `services/` is generated (Strong).** Each declares `//libgo:impl protocol.Syllab` or `protocol.JSON` with hand-edited field offsets; the migration map's triage table assigns such files to "migrate the generator first, regenerate last".

## Key Definitions Established

- `ThingModel` — what every domain's model composes. Requirements: none stated. See Open Questions.
- `Criterion_Type` — the classification a criterion record carries; values in `edges/criterion/criterion.md`.
- `Criterion_Point` — the measurement a criterion records; unit deliberately undecided.
- `Field_CountUnitID`, `Field_FinancialCurrencyID`, `Field_TemplateID`, `Field_SubjectID`, `Field_SubjectsID` — the identity surfaces of this domain's four edge/loop-edge folders.

## Proposed Next Steps

1. Rule on what a thing must offer, and write it into `ThingModel` — the question above, with its four candidates.
2. Decide "thing" vs "quiddity" as the domain's one name for its own identity.
3. Convert `modules/computer/request/protocol/dt-uuid.kh`, then return to `protocol/storage.kh`.
4. Decide whether criterion belongs to `thing` at all (its own review question), which would retire `edges/criterion/protocol/{data_model,storage}.kh`.

## Research 001 questions and next steps (2026-10-18)

### Status
Proposals only, from [thing.research.001.md](thing.research.001.md) (eleven scenarios, a five-element kernel, five rival-model choices, a mapping of every edge, loop, protocol and residue folder, twenty test scenarios, a reconciliation with the four sibling researches, thirteen contradictions). Nothing is ratified; every item is **Tentative**, **Explored** or **Deferred**, none Decided. Settled facts above are not re-argued. The research reads the Open Questions above as inputs: it proposes an answer to the keystone question (the identity accessor alone), a reason for the quiddity question (under [thing.md](thing.md#quiddity) the identifier names the individual, not the kind), and leaves "does identity need to be a concept" and the `_import/` question to questions 7 and 21.

### Open Questions raised by the research
Each carries a recommended default and what it blocks; the full text is in the research's [Open Questions](thing.research.001.md#8-open-questions). Ordered by what they change.

1. **What must a thing offer: nothing, the identity accessor, or also a name, a kind or an audit?** Default: the identity accessor only; name, kind and audit are relations and events. Blocks: `protocol/model.kh`, Khayyam rule 6 for fifteen importing domains, `service-get`, survey R3(b) (default "stays empty", which contradicts rule 6's pilot note).
2. **Must every thing have a name?** Default: no; a name is a relation to a text with a role. Blocks: text TM5, the modules.md default-title TODO, any find-by-title service.
3. **One identity for several kinds, or one identity per kind linked to the thing?** Default: one identity, many kinds; exclusivity is an edge rule. Blocks: survey A1 and the `UserUUID` fork, product question 2, the estate positions.
4. **When does a change keep an identity and when does it end it?** Default: both mechanisms (events on one identity; `supersedes` between two) exist, the owning domain picks per relation, test: every reference would still be true after the change. Blocks: the `supersedes` policy text, estate, content and text identity statements.
5. **Is a sameness assertion (`same_as` / `distinct_from`) a kernel fact, and who may make one?** Default: yes, by an identity with authority over both ends; duplicate detection is a pluggable. Blocks: follow across organizations, outside-platform things, mergers.
6. **May succession be many-to-one and one-to-many?** Default: yes, as dated facts. Blocks: the `supersedes` document, law amendments, estate subdivision.
7. **Identity scope across organizations: one global opaque value, organization-scoped, or an external identifier?** Default: one global opaque value; equivalence across organizations is an assertion. Blocks: `dt-uuid.kh` behaviour (order, format), follow's identity-proof question.
8. **What decides who may state which relation of a thing, given that ownership arises from rights?** Default: per relation kind and organization by a rule through `condition_is`; the creating organization is authoritative for what it states; follow's "owner" reads as that organization. Blocks: follow's authorization, the tombstone, correction, ownership's bare-edge-or-node question.
9. **What does retiring an identity do, and how does erasure differ?** Default: a tombstone is a dated, reversible fact by an authority; erasure is an authority-gated event that removes readability and keeps the identity and the fact. Blocks: the tombstone, an `erasure` capability, survey R4.
10. **Is the registry (identity to the domains that hold it) authoritative or a derived shortcut?** Default: a shortcut; uniqueness comes from minting. Blocks: `services/register` and `get`, `protocol/storage.kh`, `service-register.kh`, the media-type identity abstraction (survey A7).
11. **Is `follow` a pluggable attached to thing, or a relation on thing with separate processing?** Default: one pluggable. Blocks: the follow placement and its open question 2, price-index, replacement-cost. Changes a placement the owner decided on 2026-10-10, so it needs his ruling.
12. **Is the count unit a relation of the counting context, and is "one unit per thing" dropped?** Default: yes; compound units in a `measurement` capability. Blocks: count_unit, the currency label, pricing's display basis.
13. **Are `complement` and `substitute` each one directed relation with an asserter and a scope, with recommendations as discovered data?** Default: yes. Blocks: the nine lines in each document, survey Q5.
14. **What does `subjective` mean (agency, standing, social construction), is it exclusive, and does it end?** Default: standing to be a party to relations, rule-governed and dated; animate/inanimate leaves the kernel document. Blocks: the subject loop, thing.md's two sections, survey P9.
15. **Is "quiddity" retired as an identifier name, is it the kind, or the browsing level?** Default: the kind (derived); retired as an identifier name. Blocks: service vocabulary, `_import`, modules.md.
16. **Do icon, picture and the user's object labels become one `depicted_by` relation in the object domain?** Default: yes; the rating is a thing-labels word; access is a rule. Blocks: three edge documents.
17. **Does `criterion` leave thing as an `evaluation` capability, and does `Progress` leave it?** Default: yes and yes. Blocks: the criterion `data_model.kh` and `storage.kh` conversion (`Field_TaskID` now exists), Next Step 4 below, task question 13.
18. **Is `derived_from` defined once on thing, with which kinds?** Default: yes, with a small closed `kind` reviewed after use. Blocks: the template instance side, estate lineage candidates.
19. **How is a recurring or intermittent thing modeled?** Default: an occurrence per interval, a series related by `derived_from`, existence interval in the time domain. Blocks: parity with task recurrence.
20. **Are valid time and recorded time both kept for identity events?** Default: yes. Blocks: late-known deaths, backdated mergers.
21. **What happens to `_import/`, `internal/storage/mysql.sql` (an `InvoiceVoucher` table) and `widgets/ai_generated`?** Default: retire what is not about thing after the research's findings are kept; reclassify the AI label as a discovered thing-labels word. Blocks: survey A8.

### Next Steps from the research
1. Answer questions 1 to 4 together with the text (1, 2), content (1, 2) and product (2) questions: they fix `ThingModel`, the identity statements of every importing domain, and the meaning of "classification" for the four base models.
2. Ask the owner about question 11 before touching [follow](edges/follow/follow.md): it moves a decided relation's home.
3. Do survey task T3 (thing folder shapes: the nested `edges-loop/subject/edges/`, the missing `supersedes` README, the stray files) independently; it needs no answer.
4. After question 17, convert `edges/criterion/protocol/data_model.kh` and `storage.kh` or retire them; the blocker named in the Decisions above has been removed.
5. Write Placement and Open questions in the edge documents that lack them (survey T12), using the research's mapping as the reading list.
6. Record in [Khayyam handoff](../../../temp/Khayyam.handoff.md) the contradiction between survey R3(b) and rule 6 once question 1 is answered.
7. Read what the research did not: `internal/storage/*` and `_import/quiddity-status/*` file by file, `task.research.002`, the `user`, `person`, `object`, `group`, `timeline` and `status` domains, and the identity pluggables; record anything that changes a Tentative item.

## Related Artifacts

- [`thing.research.001.md`](thing.research.001.md) — the conceptual research: scenarios, kernel, rival models, folder mapping, tests and the 21 owner questions above.
- [`thing.md`](thing.md) — the domain document, including the Criterion idea backlog that this conversion's criterion files answer to.
- [`edges/criterion/criterion.md`](edges/criterion/criterion.md) — where the criterion value lists now live.
- [`protocol/dt-uuid.kh`](protocol/dt-uuid.kh), [`protocol/model.kh`](protocol/model.kh) — the owners eleven converted domains import.
- [`../user/protocol/model.kh`](../user/protocol/model.kh) — the one domain that already composes `ThingModel` for a narrower identity.
- [`../../knowledge/text/protocol/model.kh`](../../knowledge/text/protocol/model.kh) — the strongest candidate for what belongs inside `ThingModel`.
- [`../../computer/module/protocol/bs.kh`](../../computer/module/protocol/bs.kh) — where a media type already appears as a required attribute.
- [`../../rights/delegate/protocol/data_model.kh`](../../rights/delegate/protocol/data_model.kh) — the shape a converted record data model takes here.
- [`../../../Khayyam.practice.md`](../../../Khayyam.practice.md) — the seven governing rules. The pilot findings that recorded the empty-`ThingModel` question are in [`../../../Khayyam.handoff.md`](../../../Khayyam.handoff.md).

## Notes

- Eight `.kh` files written (`edges/count_unit/protocol/dt-uuid.kh`, `edges/count_unit/labels/currency/protocol/dt-uuid.kh`, `edges/template/protocol/dt-uuid.kh`, `edges-loop/subject/protocol/dt-uuid.kh`, `edges/criterion/protocol/dt-type.kh`, `edges/criterion/protocol/dt-point.kh`, `protocol/service-get.kh`) plus one edited (`protocol/model.kh`, comment removal only). All nine `accept` from the Khayyam frontend (`frontend_check.ts`) against a resolved root.
- No Go clue block was touched anywhere. Nothing outside `modules/identity/thing` was edited. `git` was not run.
- Verification note: a plain frontend run against the organization repository reports `unresolved-import` for every `in "org/..."` and `in "memar/..."` path, because the manifest that resolves those two roots is not in this repository. The nine accepts above come from a run against a root where every `.kh` of both repositories was copied in under `org/` and `memar/`, which is the missing-manifest condition worked around rather than a defect in these files.
