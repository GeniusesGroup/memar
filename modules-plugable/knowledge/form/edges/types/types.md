# Form types

## Model

- Candidate (unconfirmed): one type/kind flag-space on the form record — type flags `Type_Anonymous`, `Type_Duration`, `Type_StartPoint`, `Type_AllowToEdit`, `Type_MaxAttempt`; kind flags `Type_Criterion`, `Type_Quiz`, `Type_Survey`, `Type_Questionnaire`, `Type_Poll` (bit-shifted constants in one `const` block — one iota set, not distinct edges).

## Policies (rules)

- `Type_Criterion`: "No one can made direct answer to this form." — a direct-answer prohibition carried by the form's kind.
- Domain TODO in source: "product, Marketing, law, invoice, education, department, content, estate," — form use-cases sketched across domains.
- GUI TODO in source: "GUI template for forms?"

## Placement

- **Correct here — the form module owns its own type vocabulary** (a flag-space is parameters, not processing — parameters vs semantics ⇒ one form capability plus per-organization kind configuration; no new module).
- **Not core knowledge:** form is the optional questionnaire layer; Question/Answer/Text hold the knowledge graph without it (stated in [form.md](../../form.md)) — the flags travel with the pluggable.
- Kind flags like `Type_Quiz` connect to relation edges in the same module ([knowledge-unit](../knowledge-unit/knowledge-unit.md)) — one capability keeping flag and edge together, never "flag here, edge there".

## Open questions

- Is `Type_Criterion` the same concept as thing/criterion (task evaluation), or a form-only kind?
- Are the kind flags (Criterion, Quiz, Survey, Questionnaire, Poll) one flag-space or separate identities?
- Do the domain TODOs become per-domain form profiles (parameters per organization) rather than new kinds?
- What does the GUI-template TODO imply — template as page under `computer/page`, or a form-owned template list?

