# Language

## Model

- `(text)-[:text_language]->(language_human)`

## Policies (rules)

- Translation language text use in `Localization`.
- A `thing` relate to text by e.g. `title` and this `text` relate to each `Localization` text by this label.

## Open questions

- This folder carries a second language vocabulary of its own, under `labels/`,
  and nothing in the tree refers to it. See the handoff: it should be dropped
  rather than converted, and the language table beside it belongs to
  `language-human`.
- The protocol half of this folder cannot be converted yet: it needs the
  language domain's identifier, and no file declares it. See the handoff.
