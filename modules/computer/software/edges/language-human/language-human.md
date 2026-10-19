# Language human (software)

## Model

- `(software)-[:language_human]->(language_human)` — `SoftwareLanguageDataModel` composes `Field_SoftwareID` and `Field_LanguageUUID`, referenced by UUID across domains, plus the request/audit pair (`Observer_RequestID`, `Observer_Time_Request`).
- The Go additionally declared `Status()` with an empty result; no Khayyam form exists for it, which is the open `Status()` question in `software.handoff.md`.

## Policies (rules)

- The source states none: what the status means, and what changes when a software's language is set, are recorded nowhere.

## Placement

- Two distinct nodes (software, language-human), so an ordinary `edges/` relation of the software domain. The far end is the knowledge domain's `language-human`, reached by UUID only. Not a module: the relation carries no processing of its own beyond the record and its audit pair.

## Open questions

- `edges/language-human-ability/` next door already states `(software)-[:language_human_ability]->(language_human)` too; whether "speaks a language" and "is able in a language" are one relation seen twice or two requirements belongs to the Phase 0 wrong-kind-folder pass, not settled here.
- `Status()`'s vocabulary is undecided; see `software.handoff.md`.

## Source

> Source: `modules/computer/software/edges/language-human/protocol/data_model.kh` (in code).
