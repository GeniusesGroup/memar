# Text types

## Model

- Candidate (unconfirmed): `Type_Localization` — a proposed text type with query-time behavior: "When this word||phrase be in query it must answer with user location." e.g. "Near Pizza Store" (source marked `TODO::: right or wrong?`).
- Entity annotation notes recorded beside it: **PERSON** — People; **GPE** — geographical/political Entities (GPE).
- POS (part-of-speech) tag list recorded in the source comment block — candidate annotation vocabulary for tokens:

```text
CC	conjunction, coordinating
CD	cardinal number
DT	determiner
EX	existential there
FW	foreign word
IN	conjunction, subordinating or preposition
JJ	adjective
JJR	adjective, comparative
JJS	adjective, superlative
LS	list item marker
MD	verb, modal auxiliary
NN	noun, singular or mass
NNP	noun, proper singular
NNPS	noun, proper plural
NNS	noun, plural
PDT	predeterminer
POS	possessive ending
PRP	pronoun, personal
PRP$	pronoun, possessive
RB	adverb
RBR	adverb, comparative
RBS	adverb, superlative
RP	adverb, particle
SYM	symbol
TO	infinitival to
UH	interjection
VB	verb, base form
VBD	verb, past tense
VBG	verb, gerund or present participle
VBN	verb, past participle
VBP	verb, non-3rd person singular present
VBZ	verb, 3rd person singular present
WDT	wh-determiner
WP	wh-pronoun, personal
WP$	wh-pronoun, possessive
WRB	wh-adverb
```

## Policies (rules)

- Localization proposal as recorded: when the word/phrase appears in a query, the answer must incorporate the user's location ("Near Pizza Store") — status `TODO::: right or wrong?`, explicitly unverified.
- No other rules recorded; the entity and POS notes are vocabulary, not behavior.

## Placement

- **Not an edge — nothing here enters the graph schema; the vocabulary stays in the text module (this doc beside the source home `edges-loop/`).** The declarations are candidate *values* consumed by the existing [text_type](../../edges/text_type/text_type.md) edge ("Each text MUST have a specific type") — parameters-vs-semantics: which types exist is configuration of that edge, not a new capability and not a module.
- The `Type_Localization` half may split off: if it turns out to be query-time behavior rather than a type value, it moves to the query/search capability ([query](../query/query.md); cross-domain search analytics is always pluggable). Until that question is answered the type flag stays here — this answers the standing review in [text.md](../../text.md) ("is Localization a text type or a query-time behavior?") as **open, defaulting to this home**.
- PERSON / GPE / POS: candidate [label](../../../label/label.md) vocabulary (names are labels; UUIDs are identity) — if ratified, they become label or token-analyzer configuration, still not an edge.

## Open questions

- Is Localization a text type or a query-time behavior? Does the POS tag list become a uri/label vocabulary? (the standing questions from [text.md](../../text.md), carried here with the source)
- `TODO::: right or wrong?` — who signs off location-aware answers (user-privacy of location in query responses)?
- Are PERSON/GPE annotation vocabulary stored on tokens ([tokens](../../edges/tokens/tokens.md)) or produced by the analyzer — derived output ⇒ pluggable analytics?

