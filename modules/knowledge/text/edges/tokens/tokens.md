# Lexical tokenization 
Lexical tokenization is conversion of a text into (semantically or syntactically) meaningful lexical tokens belonging to categories defined by a "lexer" program. In case of a natural language, those categories include nouns, verbs, adjectives, punctuations etc.

## Articles

- https://en.wikipedia.org/wiki/Lexical_analysis

## Model

- `(text)-[:tokens_by]->(module)`
- `(module)-[:tokenize]->(text)`

## Policies (rules)

- Each analyzer can carry specific data
- A token is a hit: one token stored in one place, pointing at every text it
  was found in, rather than a copy of the word in each text. Google names the
  same thing a *hit list*.
- A token carries where it sits in the text it was found in — its offset in the
  sentence and in the text, and the offset of its first character in each — and
  it carries weight and scores: the weight of the occurrence, a score within
  its sentence, a score within its text, and the ranking score that orders it.
- Weight is not only frequency. A token shown in a larger or bolder font is
  weighted higher than other tokens, which is the reading that makes a heading
  count for more than the word it happens to spell.

## Open questions

- is stop-word removal an analyzer concern (dt-analyzer) rather than storage? Do weights/scores belong to analytics (pluggable)?
- The citation count of the text a token came from was reachable from the
  token's own surface in the source, commented out. It is the
  [`citations_number`](../citations_number/citations_number.md) edge's number;
  should a token carry it?
- `Token` was declared bare in [`protocol/dt-token.kh`](protocol/dt-token.kh)
  because nothing else in the corpus claims that name. If a second domain grows
  its own tokens, that name has to become qualified on both sides at once.

## Source

> Source: `modules/knowledge/text/edges/tokens/protocol/dt-token.kh` (in code).
