# Form relation

## Model

- `(contract)-[:form_relation]->(form)` (note: label, datatype_p.Field_LifeCycle)

## Policies (rules)

- Form with Just can use when in LifeCycle_StableRelease
- MUST NOT any change in LifeCycle_StableRelease, new template MUST born if any changes required.
- datatype_p.Field_LifeCycle
- label can be:
- Template, ContractExpertOpinion, ContractExpertOpinionProgress, ...
