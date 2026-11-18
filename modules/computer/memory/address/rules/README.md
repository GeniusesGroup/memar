# Address Rules (`modules/computer/memory/address/rules/`)
Rules for what an address is not asked to name. The general Memar concept of Rule is defined in [`modules/process/rule/rule.md`](../../../../process/rule/rule.md); a Rule is held by the module that owns its subject ([Rule → Which Module a Rule Belongs To](../../../../process/rule/rule.md#which-module-a-rule-belongs-to)).

| Rule | Subject | Tier | What it is |
| --- | --- | --- | --- |
| [An Address Is Not a Domain Identifier](./identifiers-are-memory-addresses/identifiers-are-memory-addresses.md) | What an address does not name | Governance | `MemoryAddress` is a place, not a domain's subject id; the subject is that domain's identifier |

The Rule is governance-tier and is enforced by no check this repository runs today; an organization adopting this repository's Rules may keep, relax, or replace it without forking anything.
