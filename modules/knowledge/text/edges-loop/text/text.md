# Text

## Model

- `(thing)-[:text]->(---)`
- Candidate (unconfirmed): text kinds (labels) recorded in the source: Poem, Scientific, Skill.

## Policies (rules)

- Any general lexicon text types got this label

## Placement

- **Correct here — home is this `edges-loop/text` doc, beside the source `edges-loop/text.go`.** The kinds are bare labels for the module's own `text` loop-edge; parameters-vs-semantics: which kinds exist is vocabulary of the text module, not a separate capability and not a rule (core never knows rule — a rules-engine enters only if kinds gate processing).
- Taxonomy reconciliation is an open question below, not a move: the sibling [text_type](../../edges/text_type/text_type.md) edge ("Each text MUST have a specific type") may be the proper owner of Poem/Scientific/Skill as type values — converge onto that existing home if ratified; either way nothing leaves the text module.

## Open questions

- Kinds vs types: are Poem/Scientific/Skill values of [text_type](../../edges/text_type/text_type.md), or labels on the `text` loop-edge itself (the standing "general lexicon text types" wording above)?
- Closed kernel set or organizational-open vocabulary?
- Overlap with [language](../../edges/language/language.md) and other text labels — one vocabulary field or several?

