# Restriction

Restriction is a pluggable module for global quantity constraints — e.g. a judicial order freezing 1000 units of a person's assets. The constraint targets a person/thing, NOT individual accounts: copying the amount onto every account of the target would multiply the constraint (100 accounts × 1000 ≠ 1000). This is why the legacy `AvailableBalance`-as-account-state model was rejected (invariant #8 in [topic-accounting-invariants.md](../../../modules/economics/topic-accounting-invariants.md)).

## Model

Current edges (under review; naming/shape not final):

- `(rule)-[:restricted]->(user)` / `(user)-[:restricted_by]->(rule)` — the constraint itself ([restricted_rule](edges/restricted_rule/README.md)).
- `(account)-[:released_by]->(transaction)` — release of a blocked amount ([released_by](edges/released_by/README.md)).
- Shortcuts: [restricted_account](edges-shortcut/restricted_account/README.md), [restricted_user](edges-shortcut/restricted_user/README.md), [restriction_cause](edges-shortcut/restriction_cause/README.md).
- Analytics: [total_blocked](analytics/total_blocked/README.md) — a derived sum, deliberately an analytics output, not stored state.

## Policies (rules)

- Applies to any count unit: money, shares, goods. The constraint is on a quantity, not on "funds".
- Incoming transactions are processed normally; the restriction rule reacts by creating its own blocking transactions until satisfied. It never modifies or rolls back the triggering transaction (invariants #6, #9).
- A rule stays active until its target amount is satisfied; it must not assume the quantity already exists (e.g. it can wait for future deposits).
- Release/unblock is a new compensating transaction, never a deletion.
- A judge may block an amount without naming a destination account; destination-less constraints are valid.

## Open questions

- Final edge set/labels for the module (work in progress by owner).
- Interaction with `condition_is` on transactions: a restriction is a rule reacting to events, not a per-transaction condition; keep the two usages distinct.
