# Form relation knowledge unit
## Model
- Candidate (unconfirmed): `(form)-[:relation]->(knowledge_unit)` — a form serving a knowledge unit as its `quiz` (direction unconfirmed).

## Policies (rules)
- Only "quiz" recorded — who may attach, and what attaching triggers (start attempts? grade posting?), are absent from the source (no bare edges).

## Placement
- **Correct here — the quiz attachment is the form capability's own** (placement by entry point: instantiated from the form; [form.md](../../form.md) states form is the optional questionnaire layer while Question/Answer/Text already hold the knowledge graph without it — so the pluggable attaches to knowledge and keeps edge + quiz processing complete in one module).
- **Not core knowledge:** the [knowledge unit](../../../../../modules/knowledge/knowledge_unit/knowledge_unit.md) stays form-free — removing forms must not disturb units (removable capability ⇒ pluggable owns it whole); the unit half needs no new edge (reference by identity).
- **Not a new module:** one label with no recorded processing is not a module candidate (an edge becomes a module only when it carries independent semantics; parameters vs semantics ⇒ one form capability plus configuration).
