# Skills
This directory exists to organize reusable reasoning practices for agents. The name **`skills`** is kept for compatibility with the current AI ecosystem, where many tools expect a `skills/` directory containing `SKILL.md` files. However, from the perspective of the Memar project, this terminology is not considered conceptually precise. A **skill** is an ability possessed by an agent. It is a property of the agent itself, acquired through learning or experience. A document cannot literally be a skill.

What these files actually contain are **practices**: explicit descriptions of how a particular kind of reasoning or task should be performed. When an agent reads, understands, and consistently applies such a practice, it may gradually develop or improve the corresponding skill. For this reason, the conceptual model adopted by Memar is:
```
Content → Practice → Skill
```

rather than:

```
Content → Skill
```

The distinction matters because it separates the description of a capability from the capability itself. This repository continues to use the `skills/` directory and `SKILL.md` filenames only for interoperability with existing AI tooling. These names should be understood as implementation constraints rather than conceptual definitions.

## Why "Practice"?
The word **practice** is not perfect, but it is significantly closer to the intended meaning than *skill*. A practice describes an established way of approaching a task, a reasoning pattern, or a repeatable method. It does not imply that the reader already possesses the corresponding ability. This distinction is similar to the difference between a training manual and an experienced practitioner. Reading the manual does not immediately create the skill, but it provides the practice through which the skill can eventually emerge.

The Memar project therefore treats these files as **reasoning practices**, independent of any particular AI platform or vendor terminology.

## About Terminology
Human language is inherently ambiguous. Words such as *practice*, *skill*, *procedure*, *method*, and *instruction* often overlap in everyday usage and may carry different meanings across communities, industries, or even dictionaries. Memar does not assume that commonly accepted terminology is conceptually correct. Whenever possible, definitions take precedence over labels. Terminology is chosen pragmatically, while the underlying concepts remain the primary source of truth.
