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

## Discussion

### Drawbacks

- A rule watching all of a target's accounts until satisfied costs more than a field check, and must stay active indefinitely if the quantity never materializes.
- "Blocked" is no longer visible as account state; every tool/GUI must query rule satisfaction to explain a refusal.

### Rationale and alternatives

- Per-account block edges carrying the amount were rejected: one judicial order of 1000 copied onto 100 accounts means 100,000 restrained — wrong semantics.
- `AvailableBalance` as an account field was rejected as a mutable derived value (invariant #8); `total_blocked` lives in analytics instead.
- The name `restriction` was chosen over `hold` (banking-colored) and `lien`/`encumbrance` (law-colored): the same mechanism must serve non-legal cases like pending-transfer reservations.

### Prior art

- Wage garnishment regulation (e.g. US 31 CFR 212.7): one order, one protected amount, applied across multiple accounts.
- Bank levy practice: a single debt restraining many accounts.

### Unresolved questions

- (Listed above: final edge set; distinctness from `condition_is`.)
- Destination-less blocks (freeze without naming a beneficiary): which edge expresses "held by no one yet"?
- Should the rule expose `required/satisfied/remaining` as its own fields or derive them from its blocking transactions?

### Future possibilities

- Dishonor/bounce events feeding reputation/social-score analytics (cross-category consumer of this module's events).
