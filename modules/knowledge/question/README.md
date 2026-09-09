## Question

A [question](https://en.wikipedia.org/wiki/Question) is an utterance which serves as a request for information. Questions are sometimes distinguished from interrogatives, which are the grammatical forms, typically used to express them. Rhetorical questions, for instance, are interrogative in form but may not be considered bona fide questions, as they are not expected to be answered.

## Interrogative

An [interrogative](https://en.wikipedia.org/wiki/Interrogative) clause is a clause whose form is typically associated with question-like meanings. For instance, the English sentence "Is Hannah sick?" has interrogative syntax which distinguishes it from its declarative counterpart "Hannah is sick". Also, the additional question mark closing the statement assures that the reader is informed of the interrogative mood. Interrogative clauses may sometimes be embedded within a phrase, for example: "Paul knows who is sick", where the interrogative clause "who is sick" serves as complement of the embedding verb "know".

Languages vary in how they form interrogatives. When a language has a dedicated interrogative inflectional form, it is often referred to as interrogative grammatical mood. Interrogative mood or other interrogative forms may be denoted by the glossing abbreviation INT.

## Idea backlog from edge code comments

Raw proposals from comment notes inside edge .go files (comments remain in code as source). Review discipline per modules/management/vocabulary-discipline.handoff.md. Nothing below is ratified.

### Question types - edges/question.go
- **Idea**: type flags Type_StandAlone (not part of a form), Type_Quiz, Type_Anonymous, Type_Duration, Type_ForceToAnswer, Type_AllowToEdit, Type_MaxAttempt, Type_Analytical; answer-shape flags (multiple can be on): YesNo (True/False), SingleChoice, MultipleChoice, Ordering, Matching (with the explanatory comment: match stems/premises to responses; a variation of multiple choice), FillInTheBlank, Descriptive, Rating, Object. Additional notes: question data (text/videos/images) saved in Comment domains; TODO dynamic data in questions (text substitution, text piping); significance as Significance_Positive/Negative uint64 scores.
- **Review questions**: closed kernel set or organizational-open? Does Significance belong to the endorsement/score edges?

### Question status and relations - edges/question-status.go, question-relation-question.go, question_option-relation-form.go
- **Idea**: status proposals: waiting-for-approval, Terminated, Deprecate. Relations: SubQuestion, Translated; Hint (for options, not descriptive type - appears in both files, one is a duplicate to resolve).
- **Review questions**: reconcile the duplicate Hint comment; are statuses the general status domain?