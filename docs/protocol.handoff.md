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
- State: can protocols span modules within a system or organizations? How is conformance coordinated when no single authority governs both sides? An independent protocol definition is assumed importable as needed, but coordination mechanisms remain undefined. [Modularity](./modularity.md) now gives Module a formal definition that did not exist when this question was first raised; the question itself is not resolved by that alone, since Modularity does not address protocol conformance coordination, but a revisit of this item should start from Modularity's definition rather than an informal sense of "module."
- Next: revisit starting from Modularity's formal definition.

### Runtime Conformance Checks
- State: protocols are fundamentally static specifications. Should there ever be optional runtime conformance verification? Generally no, but some domains (e.g., security protocols) might benefit. This is a tooling question that interacts with the [EBO principle](./type.md#explicit-behavior-ownership).
- Next: revisit with the conformance document (see Anticipated Work).

### Multi-Language Protocol Compatibility
- State: if a protocol is used across language boundaries, how should its specification be encoded? This touches on tooling and specification formats but is beyond protocol.md's scope.
- Next: revisit when the first cross-language protocol realization ships.

### Protocol vs Specification Identity
- State: is a protocol identical to its specification, or does the conceptual protocol exist independently of any written document? protocol.md leans toward treating them as distinct (the protocol is the rules governing a process; the specification is the document describing those rules) but acknowledges the question is unresolved.
- Next: settle during the next ontology review.

### Ontology Finalization
- State: the choice among Rule Set, Interaction Model, and Verifiable Interaction Model remains open. The addition of process and system as required components may favor Candidate B or C over Candidate A, but formal analysis is needed.
- Next: formal analysis of the three candidates under the process-and-system requirement.

### Protocol Conformance Measurement
- State: if Candidate C (Verifiable Interaction Model) is adopted, what constitutes adequate conformance verification? This touches on tooling and is beyond protocol.md's scope.
- Next: fold into the Protocol Conformance document (see Anticipated Work).

### Attestation of Memar's own Protocols
- State: protocol.md defines Standard as third-party attestation of institutionalization or maturity, but does not settle who plays the attesting role for protocols produced within the Memar ecosystem itself. Whether self-declaration by an implementing contributor is sufficient, whether a dedicated independent body is eventually required, and whether the answer may differ per protocol (a core ecosystem protocol versus a single organization's internal one) are all open. Until resolved, no conformance claim about a Memar protocol should be read as carrying standard status in the precise sense defined in protocol.md.
- Next: decide when the first external conformance claim is made about a Memar protocol.

## Anticipated Work

- **Protocol Conformance document:** a dedicated document defining how conformance to a protocol is verified, including the role of testing, formal verification, and tooling.
- **Protocol Relationships document:** a dedicated document formalizing the taxonomy of protocol relationships (extension, refinement, composition) and the rules governing each.
- **Protocol Versioning document:** a dedicated document addressing how protocols evolve, deprecate, and maintain compatibility.
- **AI-assisted conformance:** linters, generators, and increasingly AI-based tooling lower the cost of producing and running conformance tests for protocol implementations. A future treatment could examine how such tooling changes the practical economics of protocol adoption — including whether conformance test suites can be generated automatically from a protocol's declared rules — without changing what conformance itself means.
