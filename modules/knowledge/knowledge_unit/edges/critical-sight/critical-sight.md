# Knowledge unit to content relation

## Model

- Candidate (unconfirmed): `(knowledge_unit)-[:CriticalSight]->(content)` — a single bare relation label, "CriticalSight", from knowledge unit to content (direction unconfirmed).

## Policies (rules)

- No rules recorded: who may create/remove the relation, and what it triggers, are absent from the source.

## Placement

- **Correct here — home is `knowledge_unit/edges`.** Placement by entry point: the relation is instantiated from the knowledge unit, whose siblings already live in this folder — [duration](../duration/), [endorse](../endorse/), [score](../score/).
- The content half needs no new content-side edge: [content](../../../content/content.md) stays the holding domain and the unit may reference it by identity (reference-not-embed / content multi-typing — a node takes both identities simultaneously), so no parallel edge is required on content.
- Not a new module and not a rule: a single label with no processing semantics is not a module candidate (an edge becomes a module only when it carries independent semantics); if "CriticalSight" later triggers workflow, that processing joins this capability or a pluggable — never a bare edge shipped as-is (no bare edges).

## Open questions

- What does "CriticalSight" mean — critical insight, critical viewpoint on the content, or critical citation? Semantics must be authored before the edge may exist (no bare edges).
- Edge type or [label](../../../label/label.md) name? The source sits in `package label`, which suggests a label attached to a generic unit-to-content relation.
- Does it interact with [endorse](../endorse/) / [score](../score/) — a critical sight sounds evaluative.

