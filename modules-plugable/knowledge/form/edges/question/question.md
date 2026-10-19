# Form relation question

## Model

- Candidate (unconfirmed): `(form)-[:relation_question]->(question)` carrying requirement labels `Optional` / `Mandatory` (direction unconfirmed).

## Policies (rules)

- `Optional` / `Mandatory` recorded without semantics — what Mandatory enforces (must answer before submit? before next question?), absent from the source (no bare edges).

## Placement

- **Correct here — the form-question link stays with the form capability** (placement by entry point: the relation is instantiated from a form; pluggable owns complete capability — edge and the answering/grading rules that read it live together, never "edge here, behavior there").
- **Not core knowledge:** Question is already held by the knowledge graph without forms; a form-specific requirement flag must not force itself on bare questions (removable capability ⇒ pluggable owns it whole; the question half needs no new edge — reference by identity, reference-not-embed).
- **Not a new module:** two labels on one relation are parameters, not independent processing semantics (parameters vs semantics; prefer existing homes over inventing new modules).

## Open questions

- Are `Optional`/`Mandatory` labels on one generic form-question edge, or two distinct edge types? (Same labels-on-edge-vs-distinct-edges question as [form](../form/form.md) — one review, two relations.)
- What does Mandatory trigger — validation on submit, scoring, or ordering? Who may flip it (no bare edges)?
- Relation to the general status domain's `optional` loop-edge ([status](../../../../../modules/knowledge/status/status.md) `edges-loop/optional/`) — same vocabulary word, same mechanism or a form-local flag?
- Direction/naming unconfirmed — nothing ratified.

