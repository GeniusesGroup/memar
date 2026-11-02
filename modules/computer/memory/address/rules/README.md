# Address Rules (`modules/computer/memory/address/rules/`)
Rules for how a retained thing is named by an address. The general Memar concept of Rule is defined in [`modules/process/rule/rule.md`](../../../../process/rule/rule.md); a Rule is held by the module that owns its subject ([Rule → Which Module a Rule Belongs To](../../../../process/rule/rule.md#which-module-a-rule-belongs-to)).

| Rule | Subject | Tier | What it is |
| --- | --- | --- | --- |
| [Identifiers Are Memory Addresses](./identifiers-are-memory-addresses/identifiers-are-memory-addresses.md) | Minting and sharing ids across domains | Governance | Ids are `MemoryAddress` bytes from one mint abstraction; lenses on one thing share one address; human strings are display only |

The Rule is governance-tier and is enforced by no check this repository runs today; an organization adopting this repository's Rules may keep, relax, or replace it without forking anything.
