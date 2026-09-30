# Skills
This folder holds agent practices. The name `skills/` and the `SKILL.md` filename are kept for interoperability with the current AI ecosystem rather than as Memar's own terms: a **skill** is a capability an agent possesses, acquired through learning or experience, and a document cannot literally be one. What these files contain are **practices** — explicit descriptions of how a kind of reasoning or task is to be performed — from which the corresponding skill may gradually emerge:
```
Content → Practice → Skill
```

The word *practice* is closer to the intended meaning than *skill*, but it is not perfect: a practice describes an established way of approaching a task without implying its reader already has the ability, where a manual teaches and an experienced practitioner performs. These words overlap in everyday use and differ across communities and industries, so where the label is ambiguous the definition decides ([Terminology → The Default Meaning of an Unreferenced Term](../../docs/terminology.md#the-default-meaning-of-an-unreferenced-term)).

Memar exposes a single practice in this folder, [`memar/`](./memar/). Splitting it into peer skill packs has been tried and rejected: a project's knowledge is one continuous mental model, and a Skill file is a projection of access into a host tool rather than a partition of that model ([Knowledge → A Project Carries One Continuous Mental Model](../../docs/knowledge.md#a-project-carries-one-continuous-mental-model)). What a Skill file may contain — its front matter, progressive disclosure, bundled resources, writing style — is specified in [Documentation → Practice](../../docs/documentation-practice.md) and is not restated here; the format that specification was adopted from is documented at [agentskills.io](https://agentskills.io/specification).

The scripts that install this configuration into a project or into an agent app are described in [Scripts](../scripts/README.md).
