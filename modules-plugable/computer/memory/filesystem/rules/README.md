# Filesystem Rules (`modules-plugable/computer/memory/filesystem/rules/`)
Rules for the conditions the concepts of the filesystem are held to. The general Memar concept of Rule is defined in [`modules/process/rule/rule.md`](../../../../../modules/process/rule/rule.md); a Rule is held by the module that owns its subject ([Rule → Which Module a Rule Belongs To](../../../../../modules/process/rule/rule.md#which-module-a-rule-belongs-to)).

| Rule | Subject | Tier | What it is |
| --- | --- | --- | --- |
| [No File Concept Outside the Filesystem](./no-file-concept/no-file-concept.md) | Where a file, a directory or a path may be named | Governance | Only the filesystem module names a file, a directory or a path; every other module names what the thing is and reaches it through the memory port |

The Rule is governance-tier and is enforced by no check this repository runs today; an organization adopting this repository's Rules may keep, relax, or replace it without forking anything.
