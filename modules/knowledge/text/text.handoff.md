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
  `modules/identity/uri/ui/quiddity-uri/protocol/dt-uri.kh`, which is the
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

### Owner's rulings on the premises of Text, Content and Representation (2026-10-24)

Ruled by the owner in the chat of task 20261023-T164153Z-4608, from the concept map of task 20261018-T095710Z-4380. Each is a premise; the documents named under "Not yet written" do not carry it yet.

- **Content is one concept.** Memar's Content (the model that HTML, Markdown and JSON represent, [content.md](../content/content.md)) and the organization's Content (the unit the knowledge base holds, with a ContentUUID, versions and code as content) are the same concept. What the organization stores and versions is its records of that Content, and the organization does not keep a separate definition. *(decided)*
- **Representation is defined,** as a concept written in some form (text, image, audio, structure), kept apart from the concept it represents. Document is one kind of Representation. *(decided; where it is defined is open)*
- **Text is a kind of Representation,** the written, readable form of a concept. It is not the String (the machine value) and not the record (identity, language). The owner confirms the two were mixed in `edges/language/protocol/data_model.kh` (`Field_Text` against `Field_TextID`) and are to be held apart. *(decided)*
- **Markup is annotation on spans.** The characters of a Text are a plain value; style, structure, links and mentions are separate annotations that point at a span of it. HTML or Markdown is one way to write a text together with its annotations, a representation of it, not the Text. This replaces the lines of [text.md](text.md) that put HTML and CSS inside the value. The owner's reading: as Content may be image, subtitle and audio at once, the Text domain is an umbrella that keeps a text and its style separable, and a text always comes with its structure, never plain only. *(decided)*
- **Names.** Text is the whole (characters with their annotations); the plain value is called Characters for now. This word meets the Character abstraction of task 20261023-T164151Z-21796, which decides it; until then it is a working name. *(decided as direction; name open)*
- **A part is addressed medium by medium.** Text gives (start, end) in a stated unit, image a region, audio a time range. The owner points out that a shared abstraction with a shape per medium and one address per medium are practically the same; a shared abstraction is kept only if it states a requirement common to all (a part is meaningful only against one immutable value, and resolves to the part or fails). *(Tentative; the unit of text offsets is left to the Character task)*
- **Where passages go.** The Position A/B passage of content.md (lines 259-271) goes to the Text domain; the diagram passages (273-304) split: those about representation go with Representation, those about documenting and cognition to those documents. content.md keeps a link at each place. *(decided; the move is not done, removal is gated)*
- **Effect on the read-only view's name** (task 20261023-T164155Z-21032): the view that a quoted form hands to a method is of plain Characters, not of Text, since Text now includes annotations; its name must not contain Text or Content. `CharacterView` and `CharacterRun` stay the candidates and the Character task's decision on the word Character comes first.

Not yet written: the definition of Representation (a document of its own beside Content); rewriting [text.md](text.md) Model and "Text with style" to the rulings above; moving Position A/B and the diagram passages out of content.md; a canonical definition of the organization's Content records (the second reading in [content.handoff.md](../content/content.handoff.md)); the unit of text offsets; the annotation record's shape; whether String needs a length unit. The owner's caution that Text itself may have no view of the structure of a document it holds (below, "How does Text learn that a document has parts?") stands: annotations here are spans of one value, not the parts of a document.

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

### How does Text learn that a document has parts?
- State: the index that ranks sections (`services/index.py`) needs a document's parts, and for a Markdown file it loads the Markdown module's `content_get_section` at run time through `plugable_load`; a `.kh` file is one part. This is not a relationship Text exposes, and the owner (2026-10-24) cautions that Text itself may have no view of the structure of what it holds.
- Options: a part-splitter registry in Text that an authoring-syntax module fills when it attaches; the splitter held by the Markdown module alone, with the index moved beside it; a part as an edge of Content, so Text asks the graph and not a format.
- Anchor: [Markdown](../../../modules-plugable/computer/codec/markdown/markdown.md#open); [Pluggable](../modularity/labels/pluggable.md) (a pluggable module attaches through a relationship the module exposes).
- Blocks: nothing; the index works as it is. Asked 2026-10-24.

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

## Research 001 questions and next steps (2026-10-15)

### Status
Proposals only, from [text.research.001.md](text.research.001.md) (fourteen scenarios, a five-element kernel, five rival models of what a text node is plus language and value-content choices, a mapping of every edge, loop, protocol and widget folder, thirty-two test scenarios, fifteen contradictions). Nothing is ratified; every item is **Tentative**, **Explored** or **Deferred**, none Decided. Settled facts above are not re-argued. The research reads this domain's open questions above as inputs; where it finds an answer in another document it says so (sensitivity, question 17).

### Open Questions raised by the research
Each carries a recommended default and what it blocks; the full text is in the research's [Open Questions](text.research.001.md#8-open-questions). Ordered by what they change.

1. **What is a text node: a slot with persistent identity and immutable content-addressed values, an in-place versioned slot, or an immutable interned value?** Default: the layered slot (`ThingUUID` for the slot, a value address derived from the normalized characters and the language). Blocks: the definition in [text.md](text.md), any requirement on `TextModel` beyond a string, the storage service's shape, the content research's open question 1.
2. **One language per text with languages linked by a pluggable, several languages under one identity, or a neutral anchor?** Default: one language per text, link in a `localization` pluggable. Blocks: the translation folders, `storage.kh`, the content research's open question 6 (answer together).
3. **Is style, structure or reference part of a text's value, or an annotation on a plain value?** Default: a declared format now, plain value plus annotations as the direction. Blocks: Text with style, the character validation, font-weighted tokens.
4. **Who may change a text, and is a text with two referrers read-only?** Default: the referrer's authority; shared means read-only; copy on write. Blocks: template instantiation, username change.
5. **Do `tokens`, `match-*`, `query`, `lowercase`, `typo`, the citation count and `duration` leave for `search-analytic`?** Default: yes; the analyzer choice per language is the pluggable's configuration. Blocks: seven folders, survey task T4's token conversions, the idea backlog's index authorization.
6. **Are `mention`, `hashtag`, `command`, `anchor_text` and citation one capability on text?** Default: yes (`reference-resolution`); content's `mentions` and `topic` become discovered unions. Blocks: the duplicated hashtag and mention folders, survey Q3.
7. **Where do length, character and format requirements come from, and who declares the three validation errors?** Default: the role, format and channel state the requirement; Memar's validators declare all three; this domain declares none. Blocks: `errors/errors.kh`, the `=` rule in `widgets/text-editor/validator.kh`, the memar-side decision this handoff names.
8. **What is the unit of a length?** Default: declared per requirement; user-perceived characters for human limits, bytes for storage and channels. Blocks: Memar's `ValidateTextLength` (counts bytes), SMS limits.
9. **What canonical form is used for equality and the value address, and where does language-specific folding begin?** Default: one canonical form at identity, stored characters untouched, folding in search. Blocks: username uniqueness, Persian matching.
10. **Is "one read-only text per value and classification" (URI, hashtag, token, command) a rule family or a kernel kind?** Default: a rule family. Blocks: the loop docs, `Token`'s `Field_TextID`.
11. **Where is the span address defined once?** Default: in this domain, for text. Blocks: the content research's anchor, token offsets, citations.
12. **Is "Each text MUST have a specific type" a rule, and are the loop folders values of one vocabulary?** Default: type optional until a vocabulary exists; promote `uri`, `hashtag`, `mention`. Blocks: `text_type`, fifteen loop folders.
13. **Are `lowercase` and `typo` relations between two texts, held as discovered data?** Default: yes. Blocks: the two folders.
14. **Is a text derived from an object or a model (transcript, OCR, alt text, AI answer) a text, and how is it kept from reading as authored?** Default: a text with a derived-from relation, a method and a confidence. Blocks: the `ai/text` mapping, the content research's open question 16.
15. **What does erasure do to a stored value, and may a shared word be erased for one requester?** Default: an authority-gated event that keeps the fact; never for one requester on a shared word. Blocks: the change mechanism, the status vocabulary.
16. **Is dynamic data in a text a capability (`template`), and when?** Default: yes, after `localization`. Blocks: the open idea recorded above (dynamic data in a title).
17. **Is sensitivity only the registered label plus a rule, with hide and show one reader's state?** Default: yes; the registered word [Sensitivity](../../../modules-plugable/knowledge/thing-labels/sensitivity/sensitivity.md) already exists in Draft, which answers the question recorded above. Blocks: the widget's three services.
18. **Does this domain hold design-time strings (a Type's localized names and failure descriptions), or only run-time text of the organization's data?** Default: the Type keeps its own, as Memar's Type document says. Blocks: the unconverted `errors/locale.*.kh` here and in `language-human`.
19. **Is a formal notation (code, mathematics, music) a language of a text or a format of its value; is sign language a language of a text?** Default: notations are formats; sign language is a human language. Blocks: deleting `edges/language/labels/`, the `language-human` vocabulary.

### Next Steps
1. Owner reviews research findings 1 to 3 and answers questions 1 to 3 first; they change what the domain is, and 1 and 2 are to be answered together with the content research's questions 1 and 6.
2. If question 1 is accepted, a session writes the definition paragraph and the five-element kernel into [text.md](text.md) (not done: the research did not edit the Model or Policies).
3. A session fills Placement and Open questions on the 27 edge folders that have none, using the research's mapping as a reading list; no folder moves before the owner answers questions 5, 6, 12 and 13 and survey Q3 and Q6.
4. Hold survey task T4 (converting the unblocked text `.kh`) until questions 1, 2 and 5 are answered; the conversions would fix the shape of `tokens`, the storage service and the language data model.
5. Settle the three validation errors together with the memar side (question 7) and record the decision in both repositories' handoffs.
6. Reconcile the contradictions listed in the research in the documents that own each side, notably the language count of a text (contradiction 1), the identity statements (2), the hashtag and mention duplicates (6), and this handoff's waiting list (10, of which only `Field_LanguageUUID` was verified stale).
7. Read what the research did not: the `user`, `object`, `notification` and `group` domains, the label domain beyond its Text paragraph, `internal/matn_____/` file by file, and the localization and information-retrieval literature; record anything that changes a Tentative item.

## Anticipated Work

### The text domain's check
- State: the byte and encoding rules of `memar content check` (byte-order mark, invalid UTF-8, the replacement character, mojibake fingerprints, newlines, final newline) belong here as this domain's check, run when a text is placed and as a query ([Content → Checking text](../content/content.md#checking-text)).
- Next: they move from `modules-plugable/knowledge/documentation/services/content_check.py` when the dispatcher is built; until then they stay where they are.

## Related Artifacts
- [`text.research.001.md`](text.research.001.md) — the conceptual research: scenarios, kernel, models, mapping, tests, owner questions
- [`text.changelog.md`](text.changelog.md)
- [`README.md`](README.md)
- [`../content/content.handoff.md`](../content/content.handoff.md)
- [`../language-human/language-human.md`](../language-human/language-human.md)
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
