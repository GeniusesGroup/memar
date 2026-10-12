# Protocol Handoff
Open work for `protocol.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](./documentation-handoff.md) for what a handoff is.

## Open Questions

### Extension vs. Refinement boundary
- State: what is the precise, non-example-dependent formal criterion that separates Protocol Extension from Protocol Refinement? The working distinction (a new requirement dimension vs. a narrowed value space within an existing dimension) needs to be tested against more cases — BSON vs. JSON, HTTP/2 vs. HTTP/1.1, and others — before it can be considered settled.
- Next: test the working distinction against additional concrete protocol pairs.

### Protocol Versioning
- State: how should protocols evolve while maintaining backward compatibility? protocol.md does not prescribe a versioning strategy, but versioning is crucial in practice (HTTP/1.1 to HTTP/2, HL7 v2 to FHIR).
- Next: dedicated versioning treatment (see Anticipated Work).

### Cross-Module and Cross-Organizational Protocols
- Answered: a Protocol's boundary is the process it governs, not the Module it passes through ([Protocol → Protocol, Process, and System](./protocol.md#protocol-process-and-system)); and a Protocol is meaningful at the level of the system that offers it, so one organization's protocol is never the measure of another's ([Protocol → Who Defines a Protocol](./protocol.md#who-defines-a-protocol)). Both answers are the body's; this entry no longer asks them.
- Residue: where two participants belong to authorities that govern neither of them together, conformance is measured separately for each and never jointly, and what is owed between them is a Contract ([Protocol → Conformance](./protocol.md#conformance)). The mechanisms by which one organization takes on another's protocol — an attestation, a mapping, a declared profile — are undesigned, and whether Memar should offer one is not this document's question.
- Next: examine an actual cross-organization case, a Memar protocol taken up outside Memar, before proposing any coordination mechanism.

### Runtime Conformance Checks
- State: protocols are fundamentally static specifications. Should there ever be optional runtime conformance verification? Generally no, but some domains (e.g., security protocols) might benefit. This is a tooling question that interacts with the [EBO principle](./type.md#explicit-behavior-ownership).
- Next: revisit with the conformance document (see Anticipated Work).

### Protocol vs Standard boundary
- State: the Protocol/Standard split and the rule that conformance is never inferred from a label are carried in the body ([Standard as third-party attestation](./protocol.md#protocol-vs-standard), [conformance is never inferred from a label](./protocol.md#protocols-and-external-observers)), and the same section now states how Memar's own vocabulary follows that definition. Two residues remain: whether [Terminology](./terminology.md) should carry that consequence as a statement of its own, and whether a dedicated document for it is wanted.
- Next: settle in a terminology session ([Terminology](./terminology.md)).

### Attestation of Memar's own Protocols
- State: protocol.md defines Standard as third-party attestation of institutionalization or maturity, but does not settle who plays the attesting role for protocols produced within the Memar ecosystem itself. Whether self-declaration by an implementing contributor is sufficient, whether a dedicated independent body is eventually required, and whether the answer may differ per protocol (a core ecosystem protocol versus a single organization's internal one) are all open. Until resolved, no conformance claim about a Memar protocol should be read as carrying standard status in the precise sense defined in protocol.md.
- Next: decide when the first external conformance claim is made about a Memar protocol.

## Anticipated Work
- **Protocol Conformance document:** a dedicated document defining how conformance to a protocol is verified, including the role of testing, formal verification, and tooling.
- **Protocol Relationships document:** a dedicated document formalizing the taxonomy of protocol relationships (extension, refinement, composition) and the rules governing each.
- **Protocol Versioning document:** a dedicated document addressing how protocols evolve, deprecate, and maintain compatibility.
- **AI-assisted conformance:** linters, generators, and increasingly AI-based tooling lower the cost of producing and running conformance tests for protocol implementations. A future treatment could examine how such tooling changes the practical economics of protocol adoption — including whether conformance test suites can be generated automatically from a protocol's declared rules — without changing what conformance itself means.
