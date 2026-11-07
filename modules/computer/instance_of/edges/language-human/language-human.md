# Language human (instance)

## Model

- `(instance)-[:language_human]->(language_human)` — `NodeLanguageDataModel` composes `Field_InstanceUUID` and `Field_LanguageUUID`, referenced by UUID across domains, plus the request/audit pair.
- The Go additionally declared `Status()` with an empty result; no Khayyam form exists for it.

## Policies (rules)

- The source states none: what the status means, and what changes when a running instance's language is set, are recorded nowhere.

## Placement

- Two distinct nodes (instance, language-human), so an ordinary `edges/` relation of `instance_of`. The far end is the knowledge domain's `language-human`, reached by UUID only.

## Source

> Source: `modules/computer/instance_of/edges/language-human/protocol/data_model.kh` (in code).
