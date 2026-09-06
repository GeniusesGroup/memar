# Endorsement
Endorsement refers to transfer transaction ownership to another entity, serving as a legal verification. In old financial system it MUST be done by signing the back of a check.

## Dictionary

## Model

- `(transaction)-[:endorsement_in_favor_of]->(transaction)`
- `(transaction)-[:is_endorsement_for]->(transaction)`

## Policies (rules)

- a `transaction` CAN have more than one `endorsement` to split first transaction quantity.
- Endorsement SUSPENDS the original transaction in favor of the new one; it never voids it (append-only history, invariant #6).
- Only the owner of the receiving account may invoke the endorsement process.

## Fields

## Discussion

### Drawbacks

- Endorsement-as-transaction-chain means a single negotiable instrument's history spans several transaction nodes; "who holds this now?" is a traversal, not a field.

### Rationale and alternatives

- Modeling endorsement as editing the original transaction's destination was rejected: it breaks append-only audit (invariant #6) and misrepresents business truth.
- A separate `Payment Instrument` domain (the conventional finance answer) was rejected earlier in modeling: under the graph model, endorsement is just an edge + process over transactions, not a new core concept.

### Prior art

- Negotiable-instrument endorsement (signing the back of a check); matches the "transfer of a commitment-bearing document, not of a transaction" reading.

### Unresolved questions

- Is it a shortcut edge?? `SUSPENDED_BY` (TODO above) — if suspension is a separate relation, endorsement owns the new-transaction creation and `SUSPENDED_BY` belongs to a status/suspension mechanism.
- Final module home (settlement placeholder vs dedicated conditional-fulfilment module; shared with guarantor).
- Endorsement of a guaranteed transaction: which fires first at maturity — guarantor payment or suspension?

### Future possibilities

- Endorsement chains as a first-class navigable view (who transferred to whom) for dispute/case tooling.
