# Knowledge unit to knowledge unit relation

## Model

- Candidate (unconfirmed): unit-to-unit relations — `(knowledge_unit)-[:OtherHumanLanguage]->(knowledge_unit)` / `->[:Substitute]->` / `->[:Harder]->` / `->[:Easier]->` — four bare labels; direction unconfirmed.

## Policies (rules)

- No rules recorded beyond the labels themselves.

## Placement

- **Correct here — home is `knowledge_unit/edges`.** Placement by entry point: the knowledge unit relates to another knowledge unit; the module already holds its sibling edges ([duration](../duration/), [endorse](../endorse/), [score](../score/)), so unit-to-unit semantics belong together with them, not in a new module.
- Parameters-vs-semantics: Harder / Easier / Substitute read like a difficulty-and-alternatives *vocabulary* (configuration over one comparison relation) rather than three processing semantics — if they differ only in parameters they collapse into one relation plus label configuration; only a genuine processing difference would justify separate edges.
- OtherHumanLanguage overlaps the text module's [translation](../../../text/edges/translation/translation.md) / [language](../../../text/edges/language/language.md) edges — if it only means "this unit's text is in language X", it converges onto that existing home rather than becoming a new label here.
- Rules stay out until needed: nothing here references the rules-engine; when approval or impact rules attach, they attach as generic rule edges (core never knows rule).

## Open questions

- One edge with four labels, or four distinct relations? Dedupe before any migration.
- Harder / Easier: store both directions, or one comparison edge with a derived direction?
- Substitute: prerequisite / alternative-of semantics — does it belong to the education hierarchy proposal in [knowledge_unit.md](../../knowledge_unit.md)?
- OtherHumanLanguage vs [translation](../../../text/edges/translation/translation.md): whose capability?
- All four are bare labels (no bare edges) — who creates them, and what do they trigger?

