# Topic: Reference by UUID, Not Aggregates

Status: extracted from the Account & Transaction modeling session (2026-08). Although discovered here, this is a general modeling principle and a candidate for promotion to the Memar framework docs.

## Rule

Domain models MUST NOT embed or return each other's types. A cross-domain link is held as a UUID reference only; a separate service resolves UUID → record when the full object is needed.

- The [bookkeeping](account/edges/bookkeeping/README.md) edge holds `Field_AccountID` and `Field_FinancialTransactionUUID` — UUIDs, nothing more.
- Account does not carry Transaction objects; Transaction does not carry Account objects.

## Why

- Account ↔ Transaction is a genuinely mutual conceptual dependency (a transaction names accounts; a ledger entry names its transaction). Fighting it with shared abstraction packages or interfaces only hides the cycle or throws away type information.
- With UUID-only fields there is no bidirectional *type* dependency at all — the "cycle" was never a domain problem; it is an artifact of aggregate-style modeling (DDD) that embeds child records inside one owner.
- Caching: the consumer of a UUID decides whether/how to resolve and cache; an embedded aggregate forces the producer's freshness semantics onto every consumer.
- Embedded/edge deployment: a module compiled as a library at the edge can hold references without co-locating the other domain's storage.

## Language note

Go forbids import cycles at package level, which pressures developers into string-typed IDs or artificial abstractions. Khayyam measures dependencies at type level, so this rule is naturally enforceable there. The Go constraint is a representation limit, not a domain principle.

## Related identity principle

Human-readable identifiers (username, cheque number, sayyad code) are also not fields on a node: they are edges from the node to a `uri` domain record — the same "reference, not embed" logic applied to naming.

## Discussion

### Drawbacks

- Reading a transaction with its accounts costs several fetches instead of one aggregate load; the cost moves to the read path.
- Without discipline, "just UUIDs" degenerates into primitive string typing that throws away all type information (the very trick Go developers use to dodge cycles).

### Rationale and alternatives

Alternatives considered: a shared abstraction package holding both interfaces (only good if the relationship itself is a real domain concept, not a cycle-breaking device); dependency inversion via interfaces (hides, does not resolve); DDD aggregate root owning bookkeeping entries (rejected: forces one domain to own another domain's records).

### Prior art

- Graph databases natively store edge endpoints as references.
- Normalized relational modeling (foreign keys) is the same idea with weaker typing.

### Unresolved questions

- Does a bidirectional edge (e.g. bookkeeping traversed from both sides) share one edge UUID or exist as two records? Deferred to the storage-engine session.
- Should UUID→record resolution be a generated per-domain service or one generic graph resolver?

### Future possibilities

- Formalize as a Memar-wide modeling rule with lint/codegen support.
