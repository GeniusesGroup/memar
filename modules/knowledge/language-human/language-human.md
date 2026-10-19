# Language human
A human language — the language people speak and read, as opposed to the
languages computers speak. The domain names one and identifies it; it does not
store text in it. Human-readable text belongs to the
[Text domain](../text/text.md), and a record in another domain that carries a
language carries a relation to a language here.

## Model
- `(label(language))-[:---]->(language_human)`

A language is classified by a label and is a language-human. A text held in a
given language is a relation from the text to that language; the storage
contract that reads and writes such records lives with the text domain, at
`modules/knowledge/text/edges/language/protocol/`.

## Identity
A language's identifier is the base identifier every domain uses — the thing
domain's `ThingUUID` — so a language record is a thing and this domain mints no
identifier of its own. The field surface `Field_LanguageUUID`, with the accessor
`LanguageID`, is what a record composed of a language offers; the bodies come
from the generator that the abstraction's `Implements` intent drives.

## Errors
`ErrBadLanguage` — a language that is not supported, or not the one that was
selected. Its media type is
`domain/memar.scm.geniuses.group; package=language; type=error; name=bad-language`,
and its domain string in each locale is the word for "language" itself (`Language`
in English, `زبان` in Persian).

| Locale | Summary | Overview |
|---|---|---|
| English | Bad Language | Not supported or bad language selected! |
| Persian | زبان بد | زبان انتخاب شده صحیح نمی باشد یا توسط نرم افزار پشتیبانی نمی شود |

This prose is content, not source. It is written by a method on the error type
itself, and no such method exists yet, which is why
`errors/locale.eng.kh` and `errors/locale.per.kh` are unconverted — see the
handoff.

## Open questions
What this conversion left undecided, and what belongs to another domain, is in
[`language-human.handoff.md`](language-human.handoff.md).
