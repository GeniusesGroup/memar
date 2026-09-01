# AI Agents Skills
A standardized way to give AI agents new capabilities and expertise. [Read more here](https://agentskills.io/).

Memar don't have any plan to write this skill yet, We use AI providers like [Anthropics - Claude](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md), [OpenAI - Codex](https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md), [Microsoft](https://github.com/microsoft/skills/blob/main/.github/skills/skill-creator/SKILL.md), ...

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

## What are Agent Skills?
Agent Skills are a lightweight, open format for extending AI agent capabilities with specialized knowledge and workflows.

At its core, a skill is a folder containing a `SKILL.md` file. This file includes metadata (name and description, at minimum) and instructions that tell an agent how to perform a specific task. Skills can also bundle scripts, reference materials, templates, and other resources.

## How do Agent Skills work?
Agents load skills through progressive disclosure, in three stages:

- Discovery: At startup, agents load only the name and description of each available skill, just enough to know when it might be relevant.
- Activation: When a task matches a skill’s description, the agent reads the full SKILL.md instructions into context.
- Execution: The agent follows the instructions, optionally executing bundled code or loading referenced files as needed.

Full instructions load only when a task calls for them, so agents can keep many skills on hand with only a small context footprint.

## Specification
The complete format specification for Agent Skills [document here](https://agentskills.io/specification).

### Template
```markdown
---
name: my-skill-name
description: A clear description of what this skill does and when to use it
license: Proprietary. LEGAL has complete terms
metadata:
  author: geniuses.group
  version: "0.1"
compatibility: Designed for Claude Code (or similar products), Requires access to the internet
allowed-tools: Bash(git:*) Bash(jq:*) Read
---

# My Skill Name
[Add your instructions here that Claude will follow when this skill is active]

## Workflow
[An explicit checklist helps the agent track progress and avoid skipping steps, especially when steps have dependencies or validation gates.]
[Validation loops, Instruct the agent to validate its own work before moving on.]

## Guidelines
- Guideline 1
- Guideline 2

## Gotchas
[The highest-value content in many skills is a list of gotchas — environment-specific facts that defy reasonable assumptions. These aren’t general advice (“handle errors appropriately”) but concrete corrections to mistakes the agent will make without being told otherwise.]

## Examples
- Example usage 1
- Example usage 2

## Available scripts
- **`scripts/validate.sh`** — Validates configuration files
- **`scripts/process.py`** — Processes input data

```

### Optional directories
- **scripts/**: Contains executable code that agents can run. Supported languages depend on the agent implementation. Common options include Python, Bash, and JavaScript. Scripts should:
  - Be self-contained or clearly document dependencies
  - Include helpful error messages
  - Handle edge cases gracefully    
​
- **references/**: Contains additional documentation that agents can read when needed. Keep individual reference files focused. Agents load these on demand, so smaller files mean less use of context.
  - REFERENCE.md - Detailed technical reference
  - FORMS.md - Form templates or structured data formats
  - Domain-specific files (finance.md, legal.md, etc.)
​
- **assets/**: Contains static resources:
  - Templates (document templates, configuration templates)
  - Images (diagrams, examples)
  - Data files (lookup tables, schemas)

- **evals/**: 
  - `evals.json`: Store test cases to [evaluating skills](https://agentskills.io/skill-creation/evaluating-skills). A test case has these parts:
    - **Prompt**: a realistic user message — the kind of thing someone would actually type.
    - **Expected output**: a human-readable description of what success looks like.
    - **Files (optional)**: files the skill needs to work with.
    - **Assertions**: Assertions are verifiable statements about what the output should contain or achieve.
  - `feedback.json`: Reviewing results with a human
