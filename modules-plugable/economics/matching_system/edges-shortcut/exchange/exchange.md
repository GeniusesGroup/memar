# Exchange Transaction

## Model

- `(transaction)-[:exchange]->(transaction)`
- `(??Dollar)<-[:currency]-(account)<-[:account__by]-(transaction)-[:deal]->(transaction)-[:account__from]->(account)-[:currency]->(??EURO)`

## Policies (rules)

- Exchange to other currency.
- Transfer money from user account to other banks.
- Transfer failure: must automatically handle checking that every transaction completes, or redo it for the owner.
- Authentication level: user must have a strong authenticate token for some methods.

## Fields

## Placement

- **Correct here — `modules-plugable/economics/matching_system/edges-shortcut/exchange` (already its home).** [matching_system.md](../../matching_system.md) defines this module as owning `trade`, `deal`, `exchange`: cross-unit intent is two same-unit transactions linked by this edge — core [transaction](../../../../../modules/economics/transaction/transaction.md) stays unit-general and never learns conversion.
- The foreign-exchange service notes above (convert, move funds, completion checking, strong-token methods) are the processing semantics of that same capability — pluggable owns complete capability, so they live beside the edge instead of being split away; as a shortcut edge it is owned and maintained by the capability that gives it meaning.
- Not [money](../../../money/money.md): money is representation only (amount types, decimal scaling) and explicitly rejects stored exchange rates as module state — transfer processing is not its semantics.
  - Note (2026-10-10): the owner reads money's rejection of stored exchange rates as concerning the design of the project's own currency, not the evaluation of prices against currencies or baskets ([money → Rationale and alternatives](../../../money/money.md#rationale-and-alternatives)); this placement holds either way.
- Entry point: pairing two unit-differing transactions (give 50$ to get 40€) — filed under matching_system by integration point, not under core transaction/account (parameters vs semantics: rates, retry policy, and which methods demand strong auth are configuration on this capability).

## Open questions

- Source packages were `bank`/`services` under the economics-root `_import/exchange/` — does cross-bank payout ("to other banks") belong to this matching capability, or to a distinct banking/transfer capability? No existing module clearly owns outbound bank rails; nearest neighbor is [settlement](../../../settlement/).
- Transfer-failure redo "to the owner": built into the service, or a rule compensating the transactions (core never knows Rule — [rule.handoff.md](../../../../../modules/computer/rule/rule.handoff.md))?
- Authentication level: which methods require the strong token — per-organization rule configuration rather than fixed edge state?
- `## Fields` remains empty — no ratified fields.

