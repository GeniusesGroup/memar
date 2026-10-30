# Type Rules (`modules/computer/type/rules/`)
Rules for the conditions a type and the code that declares it are held to. The general Memar concept of Rule is defined in [`modules/process/rule/rule.md`](../../../process/rule/rule.md); a Rule is held by the module that owns its subject ([Rule → Which Module a Rule Belongs To](../../../process/rule/rule.md#which-module-a-rule-belongs-to)).

| Rule | Subject | Tier | What it is |
| --- | --- | --- | --- |
| [No Comments in Code](./no-comments-in-code/no-comments-in-code.md) | Where a type says what it is | Governance | A type's text is written by its own methods, never by a comment, in every language |

The Rule is governance-tier and is enforced by no check this repository runs today; an organization adopting this repository's Rules may keep, relax, or replace it without forking anything.
