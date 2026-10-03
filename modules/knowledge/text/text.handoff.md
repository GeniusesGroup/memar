# Text Handoff

## Topic & Purpose
Identity & Text ownership: human-readable text lives only in the Text domain; other domains relate to it. Migrated from the Organization ideas backlog (2026-09-16).

## Status

Active — the ownership decision below is unchanged, and the protocol layer of
this domain is now written in Khayyam. The edges that depend on a vocabulary
another domain owns are still waiting on that domain; see Open questions.

## Decisions

### From Organization ideas backlog — Identity & Text ownership

- Human-readable text may be stored only in the Text domain; every other domain holds a relation to it (username, email, titles, comment bodies); identity attributes like email are entities linked to User, not owned fields. *(decided)*
- Identity is independent of location: content-derived or immutable-at-creation stable reference — the org's conclusion from the Git analysis; Content Addressability is the one Git property worth keeping. *(decided)*

### From the Go → Khayyam conversion of this domain (2026-10-02)

- **A text's identity is a `ThingUUID`, not a new identifier.** `protocol/dt-uuid.kh`
  imports `ThingUUID` from the thing domain and declares only `Field_TextID` /
  `TextID` over it. A text is a thing, and the thing domain's identifier is the
  base identifier for every other domain, so declaring `TextUUID` beside it
  would be the second owner of one concept. The `time` and `uri` protocols
  already converted this way; this follows them. The Go comment on the field
  calls the value `TextID` even though the method was named `TextUUID`, so the
  `TextID` spelling is the author's own as well as the corpus's.
- **`Text` is a `String` the text domain owns.** `protocol/dt-text.kh` composes
  memar's `String` abstraction, following `QuiddityURI` in
  `modules/identity/uri/widgets/quiddity-uri/protocol/dt-uri.kh`, which is the
  same case: a Go `string`/`[]byte` value given a name of its own. **This has a
  cost worth a decision later:** satisfaction is structural, so *any* `String`
  capsule satisfies `Text`, and the domain loses the distinction between "text a
  human reads in a locale" and "a string". That is acceptable while the only
  values in the domain are written by this domain's own capsules, and wrong the
  moment a foreign string is passed where a `Text` is meant. See Open questions.
- **`TextModel` is not an empty abstraction.** The Go `Model` interface carried
  no requirement of its own — it only embedded the thing domain's model — so a
  faithful conversion would have been `tp TextModel ab` with nothing in it, which
  the governing rules call a design smell. What the domain actually needs is
  stated instead: a thing, an identity, and text.
  ```
  tp TextModel ab {
      ThingModel
      Field_TextID
      Field_Text
  }
  ```
  The `uri` domain already composed `text_p.Model`, so this unblocks it: a URI
  is a thing that reads as text.
- **`Field_Text`'s accessor is `GetText`, not `Text`.** Two rules collide on the
  name `Text`: the receiver-method-names rule keeps a method bare, but where a
  bare method name is also a declaration the *declaration* takes the module's
  path — which would have made the domain's own value type `Text_Text`. The
  corpus already writes `GetURI` for exactly this case, so the accessor is
  `GetText` and `Text` stays bare.
- **`Get…` on service contracts and token accessors.** The method-verb-phrases
  rule lists a noun-only method name as the bad form and leaves `Get…` open.
  Where the corpus already settles it — `GetURI`, `GetRequestID`,
  `GetRequestTime`, `GetSelectUUID` — the accessors here follow: `GetTextID`,
  `GetBackLinksNumbers`, `GetTokenOffsetInSentence`, and the rest. The `<Domain>ID`
  accessors (`TimeID`, `URIID`, `ThingID`) were left alone; they are the
  identifier of the receiver itself, where the receiver does not say which
  identifier is meant.
- **`uint64` became `U64`, and pagination became `Container_Offset` /
  `Container_Limit`.** The scores, weights and offsets in `dt-token.kh` are
  magnitudes, not container lengths, so `NumberOfElement` would have been a
  false claim; `U64` is memar's unsigned 64-bit abstraction. The `offset, limit`
  pairs in storage contracts are pagination and use the pagination abstractions,
  as the `quiddity-uri` storage contract already does.
- **The three validation errors are declared as capsules in this domain, under
  qualified names.** `errors/errors.kh` declares `Text_Error_OverFlow`,
  `Text_Error_Lack`, `Text_Error_IllegalCharacter`, each composing `Error`. They
  are qualified rather than bare because memar's `modules/process/validators`
  already claims the bare names `TextOverFlow` and `TextLack` — see Open
  questions, where the duplication itself is recorded.
- **`errors/locale.eng.kh` and `errors/locale.per.kh` were left unconverted.**
  Both hold only build-tag-gated Go `init` functions that call `SetDetail`.
  Human-facing text in Khayyam is a value one of the type's own methods writes,
  not a table beside the type, and no such method exists yet; writing English
  prose into a declaration would have been the middle state the comment-policy
  rule forbids. The prose is preserved in `text.md` under Validation.

## Open questions

### Waiting on a name another domain owns

No file outside this domain declares these, so the files that need them were
left unconverted rather than converted against a name invented here.

- `Field_LanguageUUID`, owned by
  `modules/knowledge/language-human/protocol/dt-uuid.kh`. It blocks
  `edges/language/protocol/data_model.kh`,
  `edges/tokens/protocol/data_model.kh`, and `widgets/text/protocol/storage.kh`.
- `label_p.UUID`, owned by `modules/knowledge/label/protocol/dt-uuid.kh`. It
  blocks `edges/text_type/protocol/dt-type.kh` and, through it,
  `edges/text_type/protocol/data_model.kh`.
- `label_p.Model`, owned by `modules/knowledge/label/protocol/model.kh`. It
  blocks `edges-loop/query/protocol/model.kh`.
- `module_p.UUID`, owned by `modules/computer/module/protocol/dt-uuid.kh`. It
  blocks `edges/tokens/protocol/dt-analyzer.kh`.
- `comment_p.Field_CommentID`, owned by
  `modules/knowledge/content/edges-loop/comment/protocol/dt-uuid.kh`. It blocks
  `widgets/text/protocol/gui-widget.kh`, whose one condition is that field.

### Questions this domain could not settle

- **Does `Text` composing `String` cost more than it buys?** See Decisions above.
  The question to answer before a foreign string reaches a `Text` position: is a
  text distinguished from a string by behaviour, or only by which domain wrote
  it? If the answer is "only by who wrote it", `Text` needs a requirement of its
  own that `String` does not carry — a length, a locale, a validity check.
- **The `Text` source carried an open idea and it is still open:** dynamic data
  in a title, text substitution, text piping. A `Text` is currently a value with
  nothing in it that says what it refers to.
- **`edges/language/labels/` should be dropped, not converted.** `dt-language.kh`
  declares a `LanguageID` enum and a `Field_LanguageID` accessor in a package
  called `language_p`; the file beside it, `internal/languages.kh`, does not use
  that declaration — it imports `memar/language/protocol` instead. Nothing
  anywhere in the tree refers to `edges/language/labels`, and memar has no
  `language` module at all. So this is unreferenced code duplicating a
  vocabulary that has no owner. It should be deleted; the language table
  (`internal/languages.kh`: native names, scripts) belongs to
  `modules/knowledge/language-human/`, and `internal/unsafe.kh` — three
  `reflect.SliceHeader`/`unsafe.Pointer` reinterpretations of a slice as a byte
  slice — should be deleted with it.
- **The three validation errors exist twice, in two repositories.**
  `modules/knowledge/text/errors/errors.kh` and memar's
  `modules/process/validators/errors.kh` declare the same three conditions with
  the same media types (`text-over-flow`, `text-lack`,
  `text-illegal-character`) and the same domain string `Validation`, and memar
  holds the validator that raises two of them. Only `text-illegal-character`
  exists on this side alone. The duplication is not settled: memar's
  `validators` is the natural owner of length and overflow, while the illegal
  character is a text-domain concern — but that split is a decision for the
  memar side as much as this one, and neither domain's error set is convertible
  to a shared declaration until it is taken.
- **Sensitive content is a widget behaviour with no domain model.**
  `GUI_Widget_Service` offers `MakeSensitiveContent`, `HideSensitiveContent` and
  `ShowSensitiveContent`, and nothing in this domain's documents says what a
  sensitive text is. Marking a text sensitive is a fact about the text; hiding
  and showing it are states of one reader's view. Only the second half looks
  like a widget concern.
- **`Precision` has no vocabulary.** `edges-loop/query/protocol/dt-precision.kh`
  declares the value and nothing else — which is the corpus's normal shape for a
  value abstraction (`U64`, `NumberOfVersion`, `VersionOffset` are all the same),
  but a precision nothing can name is not yet usable, and nothing carries it in
  the query's `DataModel` either.
- **The widget conditions file had a signature that carried no information.**
  The Go `Overflow()` returned nothing, so a condition could not report its own
  value. It was left with the Go's shape rather than given an invented result;
  the value is documented in `text.md` under Widgets and the shape is a Phase 3
  question.
- **Where the text storage service belongs.**
  `widgets/text/protocol/storage.kh` is declared in package `text_p` and its
  `DataModel` is the *language* edge's data model, unqualified. It is the text
  record's storage service sitting in a widget folder. Its home is
  `edges/language/protocol/`, and the folder it is in has no document of its own.

## Not converted, and why

| Path | Disposition |
|---|---|
| `edges/language/protocol/data_model.kh` | Blocked on `Field_LanguageUUID`. |
| `edges/language/labels/dt-language.kh` | Recommend deletion — see Open questions. |
| `edges/language/labels/internal/languages.kh` | Real logic, and its home is `language-human`. Phase 3. |
| `edges/language/labels/internal/unsafe.kh` | Recommend deletion — unsafe reinterpretation, no caller. |
| `edges/text_type/protocol/dt-type.kh` | Blocked on the label domain's identifier. |
| `edges/text_type/protocol/data_model.kh` | Blocked on `Field_Type` from the file above. |
| `edges/tokens/protocol/dt-analyzer.kh` | Blocked on the module domain's identifier. |
| `edges/tokens/protocol/data_model.kh` | Blocked on `Field_LanguageUUID` and `Field_Analyzer`. |
| `edges-loop/query/protocol/model.kh` | Blocked on the label domain's model. |
| `widgets/text/protocol/gui-widget.kh` | Blocked on `Field_CommentID`. The services half is convertible on its own and is worth doing once the comment domain declares its identifier. |
| `widgets/text/protocol/storage.kh` | Blocked on `Field_LanguageUUID`. |
| `widgets/text-editor/validator.kh` | Real logic, no declarations of its own. Its two claims are recorded in `text.md` under Validation; the length check is memar's, so nothing here needs to be written. |
| `errors/locale.eng.kh`, `errors/locale.per.kh` | See Decisions. |
| `internal/matn_____/` | **Recommend deletion, not conversion.** See below. |

### On `internal/matn_____/`

It was read and left alone. It is the old text engine: a hand-rolled inverted
index over `ganjine` records, with hand-written `Syllab` encoders and decoders,
SHA3-derived index keys, hard-coded structure IDs, and `reflect`-based pointer
arithmetic. Its own words mark it as superseded — `// TODO::: now just one word
work!!!`, an `IndexTextGet` whose response it never fills, a `PhraseTokenization`
that returns nothing, and a `WordSuggestion` struct of unexported fields with no
behaviour at all.

The operations it performs are the operations memar now provides:
`pehrest.HashSetValueReq` and `pehrest.HashGetValuesReq` in
`word.kh` and `phrase.kh` are `HashSetValue` and `HashGetValues` in
`memar/modules/memory/index-one_one/services____/`, and its syllab codecs are
`memar/modules/codec/syllab/`. The modern statement of the same intent is
already in this domain: `edges/tokens/` and `edges-loop/query/`. Converting it
would preserve a second index engine in Khayyam for the sake of a record format
nothing reads any more. Deleting it — not converting it — is the recommendation;
the decision belongs to whoever owns the migration, and the files are untouched.

## Related Artifacts
- [`README.md`](README.md)
- [`../content/content.handoff.md`](../content/content.handoff.md)
- [`../../language-human/language-human.md`](../../language-human/language-human.md)
- [`../../../bundles/knowledge-management/knowledge-management.handoff.md`](../../../bundles/knowledge-management/knowledge-management.handoff.md)

## Notes
- Provenance: Organization ideas backlog → Knowledge / Content / Task → Identity & Text ownership (2026-09-16 migration).
- Token-as-smallest-knowledge-unit and Text-only human-text arguments expanded in Content handoff + [`../../../bundles/knowledge-management/knowledge-management.handoff.md`](../../../bundles/knowledge-management/knowledge-management.handoff.md) (Discussion — Modeling method, entry points, and documentation facets).
- Converted 2026-10-02 (Go → Khayyam, protocol layer): `protocol/model.kh`,
  `protocol/dt-text.kh`, `protocol/dt-uuid.kh`, `errors/errors.kh`,
  `edges/citations_number/protocol/bs-citation_numbers.kh`,
  `edges/duration/protocol/data_model.kh`,
  `edges/duration/protocol/storage.kh`,
  `edges/tokens/protocol/dt-token.kh`,
  `edges-loop/query/protocol/data_model.kh`,
  `edges-loop/query/protocol/dt-precision.kh`. All accept under the Khayyam
  frontend. Every Go clue block is left in place.