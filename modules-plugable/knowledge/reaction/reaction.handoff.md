# Reaction Handoff

## Topic & Purpose

Conversion state of `modules-plugable/knowledge/reaction` from Go to Khayyam (2026-10-03), and the
three requirements of the reaction record that had no owner.

## Status

The domain's single source file is converted and accepted. One of its six requirements was
deliberately not converted, and two more were bound to memar's names; both decisions are recorded
below.

## Decisions

- **`ReactionTo() [16]byte` became `Field_ReactionTo` returning the imported `ThingUUID`.** The Go
  comment says "any domain", and the thing identity is this repository's one record identity - a
  second reaction UUID would be the architecture error the qualified-names rule names.
- **`Type() rune` became `Field_ReactionType` returning memar's `Character`.** A reaction is "any
  unicode emoji character", and `Character` is memar's abstraction for one code point. The method
  was **renamed from `Type` to `ReactionType`** for two reasons: bare `Type` is the name rule 3
  retires as generic (memar has already had to qualify it once, as `GUI_Element_Type`), and a
  `ReactionType` accessor says whose type it is. Note the limit this exposes - an emoji outside the
  Basic Multilingual Plane is still one code point, but a flag or a ZWJ sequence is several, so
  `Character` covers the Go's stated intent and not every emoji a user can send.
- **`arp.AuditLogging` became memar's `Observer_RequestID`.** `org/modules/app-request/protocol` does
  not exist in this repository - `modules/app-request/` is absent, not unconverted - so the
  composition had no import site. What memar declares is `Observer_RequestID`, whose own comment is
  "Field audit request (logging) is the process of documenting activity within the software systems",
  which is what the Go's name says.
- **`protocol.Storage_SaveTime` became memar's `Observer_Time_Creation`** ("Time of the data is
  created"), and **`protocol.Storage_Versioned` became memar's `Versioned`** with its
  `VersionNumber mt (self Versioned) () (v VersionOffset)`, declared at
  `memar/modules/memory/protocol/version.kh`. That file is where the Go's `protocol.` prefix
  resolves - the Go import was `"memar/protocol"`, a package path this repository has never had,
  while the concepts were migrated into `modules/memory/protocol/`.
- **`UserID() up.UserUUID` imports from `org/modules/identity/user/protocol/dt-uuid.kh`,** not from
  the Go's `org/modules/user/protocol`. That path is stale: the user domain lives under
  `modules/identity/user/`, and it is the one that declares `Field_UserUUID` and its `UserID`
  accessor.
- **`Status() Status` was not converted.** See below.

## The one requirement deliberately dropped

The Go declares `Status() Status` and **no `Status` type exists** - not in this package, not in the
tree, not in memar. The domain's own document asks the question open: "`Status()` - module-local
status vocabulary or the general status domain?" Until that is answered there is nothing for the
accessor to return, and the two available answers point at different owners:

- a module-local `ReactionStatus` would be a new vocabulary invented from a method signature, and
  the repository has no flag-space value form to put it in anyway (see
  [authorization.handoff.md](../../management/authorization/authorization.handoff.md));
- the general status domain ([`modules/knowledge/status`](../../../modules/knowledge/status/status.md))
  holds the shared statuses, and `Terminated` - the only status the sibling form domain records -
  is already claimed there *and* by
  [`modules/knowledge/question/edges/question-status`](../../../modules/knowledge/question/edges/question-status/question-status.md).

Dropping it is a real gap in the record, and it is recorded here rather than papered over with a
width.

## Open Questions

- **`ReactionDataModel` has no `Field_Status`, so the record cannot say a reaction was withdrawn.**
  The document lists "one unified reaction edge vs typed reaction edges (rate, like, emoji as
  distinct relations)" as its first open question, and the answer changes this file: typed edges
  would not need a status on the record, while one unified edge does.
- **One `ReactionType` field carries three different things.** The Go comment is explicit: "any
  unicode emoji character as old fashion rate(5 star) or like||dislike or ...". A five-star score
  saved as a plain number, a like/dislike polarity, and an emoji character are three value shapes in
  one `Character`. The document does not say which a given reaction is, and
  [`edges/reaction-count/reaction-count.md`](edges/reaction-count/reaction-count.md) says the
  count is "by each separate emoji like telegram or linkedin" - which counts only the emoji case.
- **"Query by day??" is still an open comment in the source,** and the record is described as "time
  series data that store user reaction in time if any changes to reaction occurred". With
  `Observer_Time_Creation` converted, the series has a time to hang on, but nothing declares the
  series: no observation of *when the reaction changed*, only when the row was written. Whether the
  series lives here or is mirrored by
  [`economics/analytics`](../../economics/analytics/analytics.md) is the document's own
  open question, and analytics is always pluggable.
- **There is no storage contract.** `edges/reaction/` holds `protocol/data_model.kh` and a document,
  and no `storage.kh` - while [`../form/edges/max-attempt`](../form/edges/max-attempt/) holds both a
  data model and a storage contract for a much thinner record. The time-series requirement and the
  absence of a storage surface are the same gap seen twice in this bundle.
- **`reactionable.md` names a `role` that has no domain.** The edge is recorded as
  `(datatype)-[:reactionable_by]->(role)` and `(role)-[:reactionable_to]->(datatype)`. There is no
  `role` module in this repository - `modules-plugable/management/` holds `access-control`,
  `analytics`, `authorization`, `calendar-reason`, `invite`, `meeting`, `politics`,
  `salary-earth-hourly`, `salary-earth-weekly` and `salary-floating`, and none of them is a role.
  The document is also the only one in this domain with no `## Policies` section and no `## Open
  questions`, and it is a loop-edge-flavoured relation filed under `edges/`.
- **`reaction.md` is a dictionary entry,** not a domain document: it has no Model, no Policies and
  no Open questions, only the module statement and a seven-sense gloss of the English word. The two
  edges that do have documents (`reaction`, `reaction-count`) carry the actual model, and
  `reaction-count.md` has Model and Policies but no Placement and no Open questions.

## Left unconverted

Nothing. `edges/reaction/protocol/data_model.kh` is converted; one of its six requirements
(`Status`) was dropped and is recorded above.

## Related Artifacts

- [`README.md`](README.md)
- [reaction.md](reaction.md) - the module statement and the dictionary gloss
- [`../reaction/edges/reaction/reaction.md`](edges/reaction/reaction.md) - the record's own Model
  and Policies, and the source of the open questions above
- [`../form/form.handoff.md`](../form/form.handoff.md) - the sibling pluggable, and the other side of
  the `Terminated` status claim
- [`../../../modules/knowledge/status/status.md`](../../../modules/knowledge/status/status.md) - where
  `Status` may belong
- `memar/modules/memory/protocol/version.kh` - `Versioned`, the owner of
  `protocol.Storage_Versioned`
- `memar/modules/codec/string/protocol/character.kh` - `Character`, the owner of `Type() rune`
