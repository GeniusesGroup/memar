# Question option to question option relation

## Model

- Candidate (unconfirmed): `(question_option)-[:relation]->(question_option)` — a relation between options (presumably of the same question); the source recorded only the relation stem plus one gating note. Label name and direction unrecorded.
- Gating flag documented beside it: `Type_Criterion` — "It will effect on other option analytical." ([protocol/dt-type.go](../../protocol/dt-type.go)).

## Policies (rules)

- "In most cases just when `Type_Criterion` flag is on." — the relation is expected mainly among criterion-type options.

## Placement

- **Correct here — home is `question_option/edges`.** Placement by entry point: option-to-option semantics are instantiated from the option; question_option already owns [target](../target/) and its own protocol, and a capability keeps its complete behavior together — never "edge here, behavior there".
- The `Type_Criterion` flag is *parameters*, not semantics: which options are criteria is option-type configuration inside this module; no rule-domain involvement unless a rule must decide eligibility (core never knows rule — then a generic rule attachment).
- If the relation's real purpose is analytical weighting, the discovered outputs are analytics and always pluggable; the stored relation stays with the option capability.

## Open questions

- What do related options *mean* — criterion weighting, dependency, exclusion? Semantics unrecorded (no bare edges: who creates, what triggers?).
- Does the relation carry its own label, or reuse a generic option-relation type?
- Is "in most cases just when `Type_Criterion` is on" a rule (eligibility) or an observation about prevalence?

