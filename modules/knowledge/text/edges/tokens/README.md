# Lexical tokenization 
Lexical tokenization is conversion of a text into (semantically or syntactically) meaningful lexical tokens belonging to categories defined by a "lexer" program. In case of a natural language, those categories include nouns, verbs, adjectives, punctuations etc.

## Articles

- https://en.wikipedia.org/wiki/Lexical_analysis

## Model

- `(text)-[:tokens_by]->(module)`
- `(module)-[:tokenize]->(text)`

## Policies (rules)

- Each analyzer can carry specific data
