# Language human (software)

## Model

- `(software)-[:language_human]->(language_human)` — `SoftwareLanguageDataModel` composes `Field_SoftwareID` and `Field_LanguageUUID`, referenced by UUID across domains, plus the request/audit pair (`Observer_RequestID`, `Observer_Time_Request`).
- The Go additionally declared `Status()` with an empty result; no Khayyam form exists for it.

## Policies (rules)

- The source states none: what the status means, and what changes when a software's language is set, are recorded nowhere.

## Placement

- Two distinct nodes (software, language-human), so an ordinary `edges/` relation of the software domain. The far end is the knowledge domain's `language-human`, reached by UUID only. Not a module: the relation carries no processing of its own beyond the record and its audit pair.

## Source

> Source: `modules/computer/software/edges/language-human/protocol/data_model.kh` (in code).
