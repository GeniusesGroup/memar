# Tax relation rule

## Model

- Candidate (unconfirmed): `(tax)-[:relation_rule]->(rule)` carrying a `Value` capability for tax logic beyond a flat percentage (direction unconfirmed).

## Policies (rules)

- "When value of a tax want to be more complex logic than a `per.Myriad` calculation." — ordinary tax value is a `per.Myriad` percentage ([value.go](../../protocol/protocol/value.go): `Value per.Myriad`); this relation exists for the cases that exceed it.
- "e.g. Made some discount to specific user type like charities institution." — the worked example: a charity-institution tax discount keyed to user type.

## Placement

- **Correct here — the tax-rule attachment is instantiated from the tax capability**.
- **Not core rule (and it does not duplicate it):** core's rule mechanism already exists — "Fees and charges are rules producing transactions" ([rule.handoff.md](../../../../../modules/computer/rule/rule.handoff.md) §9), "Core never knows Rule" — this relation is the *structural attachment* a tax evaluation reads; the complex-value decision itself is rule material the tax capability configures, not a second rule engine (one rule domain, many consumers; prefer existing homes over inventing new modules).
- **Not a new module:** attaching a rule reference to a tax is parameters of tax evaluation, not independent processing (parameters vs semantics).

## Open questions

- Receiving [vat.md](../../vat.md) backlog question: does tax-rule duplicate the core rule mechanism ([rule.handoff.md](../../../../../modules/computer/rule/rule.handoff.md) §9 — fees are rules producing transactions)? Verdict above says no (attachment vs engine) — confirm against how discount/rule modules attach.
- Charity discount keyed to *user type* — user-type/segment vocabulary lives where (group? law-labels? rights)? The example implies a population predicate the rule reads.
- Does `Value` here replace `per.Myriad` for that tax, or override per matched population (both coexist)?
- Direction/naming unconfirmed — nothing ratified.

