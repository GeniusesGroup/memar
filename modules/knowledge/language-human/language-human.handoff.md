# Language Human Handoff

## Topic & Purpose
State of converting `modules/knowledge/language-human/` from Go to Khayyam under
the seven governing rules in [`../../../Khayyam.practice.md`](../../../Khayyam.practice.md):
what each converted file declares, which of those declarations were judgment
calls, and what is still undecided or owned by another domain.

## Status
Active — `protocol/dt-uuid.kh` and `errors/errors.kh` are converted and both
return `accept` from the Khayyam frontend once the roots they import resolve
through a manifest. The two locale files hold human-facing prose with no method
to write it into yet and stay unconverted, as the text domain's do.

## Decisions
- **Decided: this domain declares no UUID of its own.** `protocol/dt-uuid.kh`
  imports `ThingUUID` from the thing domain rather than declaring a
  `LanguageUUID`. The Go source's `type UUID label_p.UUID` is the same chain as
  every other one in the tree — `label_p.UUID` is `record_p.UUID`, and
  `thing_p.UUID` is `record_p.UUID` — and `thing/protocol/dt-uuid.kh` states
  the identifier "MUST be unique ID in all domains". Importing rather than
  declaring is what `modules/identity/time/`, `modules/identity/uri/` and
  `modules/knowledge/text/` already did. The label domain's own
  `dt-uuid.kh` is itself unconverted, so nothing here is blocked on it.
- **Decided: `Field_LanguageUUID` is kept under exactly that name, and its
  accessor is `LanguageID`.** The name is fixed by four files in other domains
  that compose it, so it was not a choice to make. The accessor spelling was: the
  five already-converted `Field_*` files (`ThingID`, `TimeID`, `URIID`,
  `TextID`, `CalendarID`) all use the bare `<Domain>ID` form for an identifier
  of the receiver, and `OrganizationID` beside them, so `LanguageID` follows the
  majority. The minority form — `GetURI` in `quiddity-uri`, `GetText` in the
  text domain — is for a *value*, not an identity.
- **Decided: `Field_LanguageUUID` is an empty `ab`, and that is not rule 6's
  design smell.** Rule 2 makes a `Field_*` surface an abstraction whose method
  bodies are generated from an `abstraction.Implements` intent, so the block is
  empty by construction for every `Field_*` in the corpus. The accessor is
  therefore declared beside it as a separate `mt` on `Field_LanguageUUID`, which
  is the shape `thing`, `user`, `time`, `uri`, `text` and `organization` all
  use. What *would* be a rule-6 smell is a `Model` here: this domain has no
  model abstraction in the Go and none was invented.
- **Decided: the one error is a capsule composing `Error`, qualified.**
  `errors/errors.kh` declares `Language_Error_BadLanguage cp { Error }`. This
  follows the text domain's `errors/errors.kh`, which converted the same Go shape
  (`var ErrTextOverFlow er.Error`) the same way, so that the repository has one
  error model in it and not two. The Go held an interface *value*, so the
  Khayyam declaration is a type that **is** an Error rather than one that holds
  one. The media type string the Go `Init` call carried is now in
  [`language-human.md`](language-human.md) rather than in a declaration.
- **Decided: `errors/locale.eng.kh` and `errors/locale.per.kh` are left
  unconverted.** Both hold only a build-tag-gated Go `init` that calls
  `SetDetail` with prose. Human-facing text in Khayyam is a value one of the
  type's own methods writes into an influenced variable, and no such method
  exists on `Error` yet; writing the English and Persian strings into a
  declaration would be exactly the middle state the comment-policy rule
  forbids. The prose is preserved in [`language-human.md`](language-human.md)
  under Errors.

## Ambiguities Resolved
- **Whether this domain's UUID is a competing abstraction of `label_p.UUID` or
  of `ThingUUID`.** It is neither. All ~90 `dt-uuid.kh` files in the tree declare
  `type UUID <other>_p.UUID`, every chain terminates at
  `memar/storage/record/protocol`'s `record_p.UUID`, and the thing domain owns
  the single name for it. `user` declares its own `UserUUID` and `organization`
  imports it — that fork is a naming inconsistency in the repository, not a
  second concept, and it does not reach this domain.
- **Whether `LanguageID` collides with anything.** The only other declaration by
  that plain name is `type LanguageID uint32` in
  `modules/knowledge/text/edges/language/labels/dt-language.kh`, which the text
  agent recommended for deletion and which is not converted. The two are
  different concepts — see Open questions — so the name meeting is a report, not
  a redesign of this domain.

## Open Questions
- **The language *vocabulary* has no owner at all.** This domain declares the
  identifier of a language; nothing in the tree declares a language *as a
  value*. `modules/knowledge/text/edges/language/labels/dt-language.kh` held a
  `LanguageID uint32` enum with `LanguageUnset`, `LanguageMachine`,
  `LanguageMathematics`, `LanguageMusical`, `LanguageSign`, `LanguagePersian`,
  `LanguageEnglish`, `LanguageRussian`, `LanguageArabic`, and its neighbour
  `internal/languages.kh` held the matching native names and scripts — but that
  file imports `memar/language/protocol`, **a module the memar repository does
  not have**, and nothing in either repository refers to it. memar keeps the
  same enum only as archived `memar-js` JavaScript inside comments at
  `modules/computer/datatype/protocol/detail.kh`. So the enum is a vocabulary
  with no home, and this domain is the natural home for it. That is not this
  conversion's job — it is real logic, Phase 3 — but the text agent's deletion
  recommendation should be weighed against it: deleting the enum and the table
  together removes the only statement of which languages the system knows.
- **`modules/knowledge/text/ui/text/protocol/storage.kh` needs more from
  this domain than a field.** Its Go signatures read
  `Count(textID UUID, language language_p.UUID)` and
  `ListLanguages(textID UUID, ...) (languages []language_p.UUID, ...)`. The
  `language_p.UUID` positions want the *value*, not the field surface. Under the
  decision above they become `ThingUUID`, which is the same value type the text
  domain's own identifier uses; but a `ListLanguages` result of `[]ThingUUID`
  reads as "any things", and `Array_LanguageUUID ab { Array_Dynamic }` over
  `ThingUUID` would say what it means. That array was not declared here because
  this domain's own Go needs no list of languages — the call is the text
  domain's. Whoever converts that storage file should raise it.
- **Should the label on the `language_human` node be part of this domain's
  contract?** The model's only edge is `(label(language))-[:---]->(language_human)`,
  and the label domain (`modules/knowledge/label/`) is unconverted, so nothing
  could be stated here even if it were decided. Recorded so the dependency is not
  discovered twice.
- **Qualifier spelling: `Language_` or `LanguageHuman_`.** The module is
  `language-human`, and the qualified-names rule wants a declaration to carry
  its module's path — but an identifier cannot hold a `-`. `Language_Error_*`
  was chosen because the domain's own Go package is `language_p`, the graph node
  is `language_human`, and the required `Field_LanguageUUID` already says
  "Language" with no "Human". If the repository decides hyphenated modules are
  spelled by joining the segments, `LanguageHuman_Error_BadLanguage` follows and
  this one line changes. Worth settling once, for every hyphenated module.
- **`Field_LanguageUUID` composes nothing, so it cannot be told apart from any
  other field surface.** That is true of every `Field_*` in the corpus and is
  rule 2's consequence, but it means nothing yet rejects a record whose
  `LanguageID` returns a thing that is not a language. Whether a language record
  needs requirements of its own — or whether the text domain's `data_model`
  should compose a language *model* that has some — is unanswered by any document
  in this domain.

### The language registry of the retired memar-js repository
- State (2026-10-30): `modules/computer/type/protocol/detail.kh` held, as comments, two files of the retired memar-js repository (archive commit 27e013d, `language/language.js` and `language/languages.js`). They were not a type's text and were removed from there at the owner's word; the sources stay in the archive. What they carried, as data, is the closed set of human languages the owner's rule on language files needs.
- The data: language codes used by the old code were Unset 0, Machine 1, Mathematics 2, Musical 3, Sign 4, Persian 5, English 6, Russian 7, Arabic 8. Eight languages carried ISO 639-1, 639-2 and 639-3 codes and a direction: Arabic (ar, ara, rtl), Chinese (zh, zho, ltr), English (en, eng, ltr), French (fr, fra, ltr), German (de, deu, ltr), Hindi (hi, hin, ltr), Persian (fa, fas, rtl), Russian (ru, rus, ltr).
- Blocks continuation: no.
- Next: decide the closed set and its code form (`eng`, `per` or `fas`) with the language-file rule, then declare it in this domain as code.

## Not converted, and why
| Path | Disposition |
|---|---|
| `errors/locale.eng.kh`, `errors/locale.per.kh` | Prose with no method to write it into. See Decisions. |

## Files changed by this conversion
- `protocol/dt-uuid.kh` — `ThingUUID` imported, `Field_LanguageUUID` and
  `LanguageID` declared above the untouched Go block.
- `errors/errors.kh` — `Error` imported, `Language_Error_BadLanguage` declared
  above the untouched Go block.
- `language-human.md` — Model kept; Identity and Errors sections added from the
  Go comments; the locale prose moved here out of the unconverted locale files.
- `language-human.handoff.md` — this file.

## Related Artifacts
- [`README.md`](README.md)
- [`../text/text.handoff.md`](../text/text.handoff.md) — the domain waiting on
  `Field_LanguageUUID`, and the recommendation that
  `text/edges/language/labels/` be deleted.
- [`../../identity/thing/protocol/dt-uuid.kh`](../../identity/thing/protocol/dt-uuid.kh)
  — the owner of `ThingUUID`.
- [`../../../Khayyam.practice.md`](../../../Khayyam.practice.md) — the seven governing rules.

## Notes
- Converted 2026-10-03 (Go → Khayyam, protocol and errors layer). Both converted
  files return `accept` under the Khayyam frontend. Every Go clue block is left
  in place.
- The frontend was run against a copy of both repositories laid out as
  `…/khroot_copy/org/…` and `…/khroot_copy/memar/…`, because `in "org/…"` and
  `in "memar/…"` resolve through a manifest that does not exist in this
  repository; a plain run reports `unresolved-import` for every converted file in
  the tree for that reason alone. The harness was confirmed to resolve imports
  (a probe file importing `Field_LanguageUUID` from here accepts, and one naming
  a non-existent path refuses `unresolved-import`).
- `abstraction_bridge.py go-to-khayyam` produced no output for either path, so
  nothing here is tool-suggested; every declaration was written by hand against
  the rules.
- `memar-documentation.py write`/`edit` with `--newline` writes the literal words
  `lf`/`crlf` into the file. These files were written with the file-write and
  `edit` tools, and `memar-documentation.py edit` without that flag.
