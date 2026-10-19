# Guarantor
Guarantor or endorsement in law indicate that someone who promises to pay a debt if the person who should pay it does not.

## Dictionary

guarantor   
guar·an·tor /ˌgærənˈtɔː US -ˈtɔːr/ n [C]   
- law someone who promises to pay a debt if the person who should pay it does not
- n.  one who provides a warrant or guarantee to another

## Model

- `(transaction)-[:guarantor_is]->(transaction)`
- `(transaction)-[:is_guarantor_for]->(transaction)`

- `(User)-[:GUARANTEES]->(transaction {status: 'Active'})`

## Policies (rules)

- a `transaction` CAN have more than one `guarantor`
- The guarantee is NOT auto-executed: under the legal doctrine examined, collecting from a guarantor requires a separate transaction initiated through a claim/legal process; this edge records the commitment only.
- A guarantor's contingent liability is a rule-side concern (reporting "how much active guarantee does user X have?" is analytics, not stored state).

## Fields

## Discussion

### Drawbacks

- A guarantor's exposure ("how much active guarantee does user X carry?") is not stored anywhere; it is an analytics traversal, which is more expensive and less immediate than the per-account field the legacy model used.

### Rationale and alternatives

- Guarantee modeled as a linked transaction (not a field on the guaranteed transaction): the guarantor's payment is a real, separately-booked effect, so it deserves its own node and lifecycle.
- Auto-execution on default was rejected: the legal doctrine examined requires a claim/legal process to move against a guarantor, so the edge records commitment only and a rule/process decides when it fires.

### Prior art

- Surety/guarantee in law; contingent liability in accounting — the "contingent until claimed" reading matches both.

### Unresolved questions

- How to process more than one `guarantor`? FIFO, pro-rata, or rule-decided? (TODO above)
- Final module home: this edge lives under settlement only because "settlement_system" was a placeholder for "the processing machine behind conditional fulfilment"; endorsement/guarantor may deserve their own module.
- The `(User)-[:GUARANTEES]->(transaction {status: 'Active'})` line is query-flavored, not a model edge — remove or formalize?

### Future possibilities

- Guarantee-coverage analytics (active contingent liability per user) as a pluggable analytical module, mirroring `restriction/analytics/total_blocked`.

