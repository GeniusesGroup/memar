# Text

## Model

- `(thing)-[:text]->(---)`
- Candidate (unconfirmed): text kinds (labels) recorded in the source: Poem, Scientific, Skill.

## Policies (rules)

- Any general lexicon text types got this label

## Placement

- **Correct here — home is this `edges-loop/text` doc, beside the source `edges-loop/text.go` (no such file yet).** The kinds are bare labels for the module's own `text` loop-edge; parameters-vs-semantics: which kinds exist is vocabulary of the text module, not a separate capability and not a rule (core never knows rule — a rules-engine enters only if kinds gate processing).
- The sibling [text_type](../../edges/text_type/text_type.md) edge ("Each text MUST have a specific type") may be the proper owner of Poem/Scientific/Skill as type values — nothing leaves the text module.
