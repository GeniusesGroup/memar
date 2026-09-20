# Form
It can be use in many ways like exams, questionnaire, poll, ...

Form is an optional questionnaire capability. Question, Answer, and Text already hold the knowledge graph without it, so this folder lives under `modules-plugable/knowledge/form` rather than kernel `modules/knowledge/`.

## Idea backlog from edge code comments

Raw proposals from comment notes inside edge .go files (comments remain in code as source). Review discipline per modules/management/vocabulary-discipline.handoff.md. Nothing below is ratified.

### Form types - edges/form.go
- **Idea**: type flags Type_Anonymous, Type_Duration, Type_StartPoint, Type_AllowToEdit, Type_MaxAttempt; kind flags: Criterion (no one can make a direct answer to this form), Quiz, Survey, Questionnaire, Poll. TODOs: form use-cases across domains (product, marketing, law, invoice, education, department, content, estate); GUI templates for forms?
- **Review questions**: is Criterion-form the same concept as thing/criterion (task evaluation)? Are form kinds one flag-space or separate identities? Do the domain TODOs become per-domain form profiles?

### Status and relations - edges/form-status.go, form-relation-question.go, form-relation-task.go
- **Idea**: status Terminated; question-in-form labels Optional/Mandatory; form-task labels Creator/Pending.
- **Review questions**: statuses vs the general status domain; are Creator/Pending task-role labels?