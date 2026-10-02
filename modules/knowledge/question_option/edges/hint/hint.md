# Question option to question relation

## Model

- Candidate (unconfirmed): `(question_option)-[:hint]->(question)` — the source carried the relation stem "question_option-relation-question" with the note "use for options not descriptive type." and the label `Hint` (direction per the file name; not ratified).
- The same Hint note also exists on the question-to-question relation (`QuestionQuestionRelation_Type_Hint // use for options not descriptive type.`) in [question-relation-question.kh](../../../_import/question-relation-question.kh) — one concept recorded twice.

## Policies (rules)

- "use for options not descriptive type." — a hint attaches to choice-type options, not to descriptive/free-text answers.
- No creation or trigger semantics recorded.

## Placement

- **Correct here for the option-side relation — home is `question_option/edges` — pending dedup with the question-side Hint type.** Placement by entry point: the option carries its hint when rendered; the question half already has its root home in [question](../../../question/question.md) (questions are owned by the root knowledge question module, as [qa.md](../../../../economics/product/edges/qa/qa.md) also records), so no new module is warranted.
- If the two Hint records converge into a single relation type, the merged relation's owner is the question domain — this doc keeps the option-side provenance until that decision lands, matching the standing "one is a duplicate to resolve" entry in [question.md](../../../question/question.md).
- Not GUI: hint *display* is a pluggable GUI surface; the model only carries the hint data attached to the option.

## Open questions

- Duplicate to resolve: which source owns Hint — this option-side note, or the question-relation type (see the standing entry in [question.md](../../../question/question.md))?
- Edge vs enum value: Hint as a *type* of question-to-question relation, or a dedicated option-to-question edge?
- Where does hint *text* live — same-UUID reference into the Text domain (human-readable text only in Text), not an embedded body?

