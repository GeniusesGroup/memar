# Form Handoff

## Topic & Purpose

Conversion state of `modules-plugable/knowledge/form` from Go to Khayyam (2026-10-03), and what the
domain's own edge documents name that no longer has a source.

## Status

All six source files converted, all accepted. Nothing was left unconverted - this is the one assigned
domain with no blocked file - but the *documents* are in worse shape than the code, and that is the
substance of this handoff.

## Decisions

- **`MaxAttempt() uint16` became `Field_MaxAttempt` / `MaxAttempt` returning `U16`.** The
  `Field_*` + accessor shape is the one the whole converted corpus uses for a stored value;
  `U16` rather than memar's `W16` because a capsule cannot appear in an abstraction's signature.
- **`AnswerBy()` and `FillBy()` became `Field_AnswerBy` and `Field_FillBy`,** both returning
  `UserUUID`. They are the only requirement the respondent record places on a person that is not
  `Field_UserUUID`, so the naming deliberately does not say "user": *who the form answers on behalf
  of* and *who filled it in* are different people, and a field named `Field_UserID` for either would
  have hidden that.
- **`FormMaxAttemptDataModel` and `FormRespondentDataModel` name their records,** following
  `<Owner><Concept>DataModel` as `BookkeepingDataModel`, `DelegateDataModel` and
  `GroupDataModel` already do. Bare `DataModel` is not available - it is the generic name rule 3
  retires.
- **Both `UUID` types resolved to the imported `ThingUUID`.** The Go said `type UUID thing_p.UUID`
  in both `form_p` and `fr_p`; a second form UUID and a second form-respondent UUID would be the
  architecture error the qualified-names rule names. The record identity is the thing identity.
- **The form type vocabulary was not declared.** See below.

## What the documents name that has no source

The brief for this domain asked for exactly this, and the answer is larger than `form.go`:

- **`form.go` does not exist anywhere in this repository.** Three documents (`edges/form/form.md`,
  `edges/knowledge-unit/knowledge-unit.md`, `edges/types/types.md`) pointed at it with a "(no such
  file yet)" marker; the pointer is removed from each, and the claim underneath - that a `form.go`
  holds the type flags and the form skeleton - has no source.
- **The whole form type-flag space has no source left.** `edges/types/types.md` records ten flags -
  `Type_Anonymous`, `Type_Duration`, `Type_StartPoint`, `Type_AllowToEdit`, `Type_MaxAttempt` and
  the kinds `Type_Criterion`, `Type_Quiz`, `Type_Survey`, `Type_Questionnaire`, `Type_Poll` - as "one
  `const` block, one iota set". A repository-wide search finds `Type_Anonymous`, `Type_Quiz` and
  `Type_Criterion` **only inside `.md` files**. These documents were written in Phase 0 from
  comment-only Go that has since been deleted, so the vocabulary survives only as prose. Nothing was
  declared for it: a flag space has no value form in this repository yet (the same gap
  [authorization.handoff.md](../../management/authorization/authorization.handoff.md) records), and
  inventing one from a document would be converting a document into code.
- **The six form-to-form kind labels have no source left either.** `Alternative`, `EasierAlternative`,
  `HarderAlternative`, `SameForm_DifferentOrder`, `Basic`, `SamePurpose_MoreQuestion` appear in
  exactly one place in the tree: `edges/form/form.md`. The document notes the source sat in
  `package label`, so these were label names on one generic form-to-form edge; that package is gone
  too.
- **`Terminated` is the form's only recorded status** (`edges/form-status/form-status.md`) and has no
  source. It also appears in
  [`modules/knowledge/question/edges/question-status/question-status.md`](../../../modules/knowledge/question/edges/question-status/question-status.md)
  as a *question* status, so the same word is claimed by two domains for two records.
- **One document pointer was stale rather than absent, and is repointed.**
  `edges/respondent-task/respondent-task.md` named `respondent/protocol/data_model.go (no such file
  yet)`; that file is `respondent/protocol/data_model.kh`, and the document now links it.

## Open Questions

- **The form type flags are duplicated by the question domain's flags.**
  `Type_Quiz`, `Type_Anonymous`, `Type_Duration`, `Type_AllowToEdit` and `Type_MaxAttempt` all appear
  in *both* `form/edges/types/types.md` and
  [`modules/knowledge/question/edges/question/question.md`](../../../modules/knowledge/question/edges/question/question.md)
  (which adds `Type_StandAlone`, `Type_ForceToAnswer`, `Type_Analytical` and drops the form's five
  kinds). Both documents say "one iota set". A form made of questions plausibly inherits the
  question's flags rather than repeating them - which would make `form/edges/types/` a shortcut
  rather than an owner - or the form's are genuinely its own. **Two vocabularies, one set of names,
  neither with a source.** This is the form taxonomy question the migration record lists, and it
  cannot be settled from the tree as it stands.
- **The max-attempt edge is the only edge in this domain with code, and it is the only one whose
  document is missing.** `edges/max-attempt/` holds `protocol/data_model.kh` and
  `protocol/storage.kh` and **no `max-attempt.md` and no `README.md`**. The Phase 0 rule is one
  folder per edge with its own document, and `edges/knowledge-unit/knowledge-unit.md` already links
  to it as "`max-attempt/`" - a link to a directory holding no document.
- **Every other edge here is documentation-only with no protocol file at all:** `form-status`,
  `form`, `group`, `knowledge-unit`, `question`, `respondent-task`, `task`, `types`. Each is marked
  "Candidate (unconfirmed)" and each closes with "Direction/naming unconfirmed - nothing ratified",
  so none of them may become an edge record yet. That is a consistent state, not a gap - but it means
  **the form capability is one identity, one respondent identity, one attempt counter, and eight
  ratified nothing.**
- **`MaxAttempt`'s zero is undefined.** The Go declares `MaxAttempt() uint16` with no statement of
  what zero means - unlimited attempts, or no attempts. `knowledge/username`'s Go carries the same
  kind of note elsewhere ("0 means unset"), and `form/edges/types/types.md` lists `Type_MaxAttempt` as
  a *flag* as well, so a form both carries the flag and a count.
- **`AnswerBy` and `FillBy` have no stated relationship.** The Go declares both and nothing more: is
  an anonymous form one where the two differ, is `AnswerBy` always the form's owner, and what happens
  when they are equal? `Type_Anonymous` in the type flags is presumably the case where they differ,
  but that link is nowhere written down.

## Left unconverted

Nothing. All six files - `protocol/dt-uuid.kh`, `respondent/protocol/{dt-uuid,data_model,storage}.kh`
and `edges/max-attempt/protocol/{data_model,storage}.kh` - are converted.

## Related Artifacts

- [`README.md`](README.md)
- [form.md](form.md) - the capability's own statement that a form is the optional questionnaire
  layer over Question / Answer / Text
- [`../reaction/reaction.handoff.md`](../reaction/reaction.handoff.md) - the sibling pluggable
  knowledge capability
- [`../../management/authorization/authorization.handoff.md`](../../management/authorization/authorization.handoff.md)
  - why no flag space was declared here either
- [`../../../modules/knowledge/question/edges/question/question.md`](../../../modules/knowledge/question/edges/question/question.md)
  - the duplicated type-flag vocabulary
- [`../../../modules/knowledge/question/edges/question-status/question-status.md`](../../../modules/knowledge/question/edges/question-status/question-status.md)
  - the other claim on `Terminated`
