# Question types

## Model

- Candidate (unconfirmed): question type flags — `Type_StandAlone` (not part of a form), `Type_Quiz`, `Type_Anonymous`, `Type_Duration`, `Type_ForceToAnswer`, `Type_AllowToEdit`, `Type_MaxAttempt`, `Type_Analytical`.
- Candidate (unconfirmed): answer-shape flags (multiple can be on) — `YesNo` (True/False), `SingleChoice`, `MultipleChoice`, `Ordering`, `Matching` (with the explanatory comment: match stems/premises to responses; a variation of multiple choice), `FillInTheBlank`, `Descriptive`, `Rating`, `Object`.
- Additional notes: question data (text/videos/images) saved in Comment domains; TODO dynamic data in questions (text substitution, text piping); significance as `Significance_Positive`/`Significance_Negative` uint64 scores.

## Policies (rules)

- Several answer-shape flags may be on at once.
- Question data (text, video, image) is stored in the comment domains, not on this flag set.
- No who-may-set rule is recorded.

## Placement

- Stays on the question record in this module: the names are flags of a question, not a separate capability.
- Whether the set is closed or organizational-open, and where Significance lives, are open below.

## Open questions

- closed kernel set or organizational-open? Does Significance belong to the endorsement/score edges?

