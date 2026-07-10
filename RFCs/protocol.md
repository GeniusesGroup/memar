---
RFC Number: 495465
Title: "Protocol"
Status: Proposed
Start Date: 2026-07-10
Applied to: ["*"]
Supersedes: ""
Superseded by: ""
Related:
  Depends_on: []
  Extends: []
  Conflicts with: []
Contributor(s):
  - name: "Omid Hekayati"
    uri: "mailto:omid@geniuses.group"
    contribution: ""
    task: []
  - name: "ChatGPT"
    uri: "https://openai.com"
    model: "GPT-5.5"
    effort: ""
    contribution: "Drafted initial text, argued for and against alternatives, incorporated revisions"
    task: []
  - name: "Super Z"
    uri: "https://z.ai"
    model: "GLM"
    effort: "Medium"
    contribution: "Split original monolithic RFC into three focused RFCs (Protocol, Explicit Behavior Ownership, Khayyam Rejection of Inheritance). Restructured Protocol RFC to be purely ontological — removed all Khayyam-specific implementation details, capsule references, and code examples. Enriched with Protocol Ontology Candidates, Protocol Relationships, Inheritance Terminology Concerns, and Standard Library Criticism from working notes."
    task: ["content-split", "restructuring", "enrichment"]
---

# Protocol

## Summary
This RFC defines the concept of **Protocol** as a general, domain-independent abstraction. A Protocol is an abstract specification of interaction rules — formats, procedures, and message exchange sequences — that governs how independent components communicate. The definition is intentionally not limited to programming languages or software systems; it must remain valid across networking, industry standards, healthcare, finance, and organizational processes. This RFC distinguishes Protocol from related but distinct concepts — Contract, Standard, Specification, Interface, and Policy — and establishes an ontological foundation for all subsequent Memar RFCs that reference protocols.

## Motivation

### The Fundamental Question
One of the most important open questions underlying the Memar framework is: **What exactly is a Protocol?** This question is intentionally broader than any single programming language construct. The intention is not to define "What is a Swift Protocol?" or "What is a Go Interface?" or "What is a Rust Trait?" — but rather to arrive at a definition of Protocol as a general concept whose validity extends beyond software engineering.

### Terminology Confusion in Practice
The term "protocol" is widely used but frequently conflated with other terms. Practitioners loosely call HTTP both "the HTTP protocol" and "the HTTP standard" interchangeably. In object-oriented programming, terms like "interface", "trait", and "protocol" are treated as synonyms. Even within standards bodies, the boundary between a protocol (the rules) and a standard (the ratification) is often blurred. This conflation creates real problems: when a team says "implement the protocol," do they mean follow the abstract rules, comply with a ratified standard, or satisfy a contractual obligation? Without precise definitions, these ambiguities propagate into design decisions.

### Why This Matters for Memar
Memar needs a stable, precise definition of Protocol because the concept serves as a foundational building block. If the term remains ambiguous, every subsequent RFC that references protocols inherits that ambiguity. By establishing a clear ontological foundation now, we prevent conceptual leakage between related but distinct concerns — such as behavior ownership, inheritance, and conformance — each of which has its own RFC.

## Guide-level Explanation

### What is a Protocol?
A Protocol is a named set of **declarative requirements** for interaction. It specifies *what* must happen — message formats, call sequences, expected behaviors — without prescribing *how* those requirements are fulfilled. Think of HTTP: the protocol defines that a client sends a request line, headers, and an optional body, and that a server responds with a status line, headers, and a body. The protocol does not dictate whether the server is written in C, Python, or runs on bare metal.

Protocols appear in many domains beyond software:

- **Networking:** HTTP, SMTP, TCP/IP
- **Industry:** ISO 9001 (quality management), ISO 27001 (information security)
- **Insurance:** ACORD (data exchange standards for insurance forms)
- **Healthcare:** HL7, FHIR (medical data exchange)
- **Operating Systems:** POSIX (standard interface for OS services)
- **API Ecosystems:** OpenAPI, GraphQL

This breadth is intentional. The concept of Protocol must be defined independently from any language syntax or implementation technology, because a definition tied to one domain will fail to capture the essence of what makes all of these examples "protocols."

### Protocol vs Contract
A Contract implies **parties, obligations, and commitments**. When two organizations sign a contract, there are specific entities with reciprocal duties, and breach carries legal or formal consequences. A Protocol does not inherently require predefined parties. HTTP exists as a protocol regardless of whether any particular client and server are currently interacting. Any conformant participant can engage with the protocol without negotiating with a counterparty.

This distinction is not merely academic. In software design, conflating "protocol" with "contract" leads to assumptions about bilateral obligations that don't exist. A Memar Protocol is a one-sided specification: it declares requirements, and any entity that satisfies those requirements conforms — no negotiation needed.

### Protocol vs Standard
A Standard carries the weight of **formal approval, governance, and recognized adoption**. A protocol *can* become a standard through ratification by a governing body (IETF, ISO, IEEE), but the two concepts are not equivalent. HTTP's rules are defined in RFC 7540 (the protocol). The IETF's formal approval process makes it an Internet Standard. The protocol exists independently of its standardization status.

This distinction has practical implications. A team can define a protocol for internal use without any standards body involvement. Conversely, implementing a protocol specification exactly does not automatically grant "standard" status unless ratified. Many software projects ship libraries they call "standard libraries" without any independent validation of correctness, completeness, or conformance — the word "standard" is used merely because the library ships with the language.

### Protocol vs Specification
A specification is *how* a protocol is documented. A protocol is *what* is documented. The protocol exists conceptually as a set of interaction rules; the specification is the authoritative text — the RFC, the ISO document, the markdown file — that describes those rules for implementers. The two are related but distinct: you can have a protocol without a written specification (implicit organizational protocols), and you can have a specification that describes something other than a protocol (a hardware datasheet, for example).

Whether a protocol and its specification are identical remains an open philosophical question, but for practical purposes in Memar, they are treated as distinct: the protocol is the conceptual entity; the specification is its documentation.

### Protocol vs Interface
Programming languages introduce constructs named "interface" (Java, Go), "protocol" (Swift), and "trait" (Rust). These are *code-level counterparts* of the broader concept of Protocol. They may represent partial aspects of the general concept — typically the structural requirement that certain methods or operations must exist. However, these language constructs often carry additional baggage: default implementations (Swift protocols, Rust traits), implicit behavior acquisition (Go embedding), or type-system constraints that go beyond pure interaction rules.

A Protocol in the general sense is not limited to method signatures. It can include message formats, state machine transitions, error handling expectations, and sequencing rules that no single language construct fully captures.

### Protocol vs Policy
Policies are high-level directives for behavior or usage, often with discretionary enforcement — for example, "all emails must be encrypted" or "all API responses must include a correlation ID." A Protocol is narrower and more precise: it defines specific data formats, call sequences, and behavioral compatibility requirements. A policy might *mandate* the use of a protocol; the protocol itself is the technical specification of *how* the mandated behavior is achieved.

## Reference-level Explanation

### Protocol Ontology Candidates
Several candidate definitions have emerged from discussion. None has been finalized; the purpose of listing them is to make the space of options explicit:

**Candidate A — Protocol as Rule Set:**
A Protocol is simply a set of rules. This is the most minimal definition. It covers HTTP (rules for request/response), ISO 9001 (rules for quality processes), and organizational protocols equally. The weakness is that "rule set" is extremely broad — a style guide is also a rule set, but not necessarily a protocol.

**Candidate B — Protocol as Interaction Model:**
A Protocol is a specification of how independent entities interact. This adds the constraint of *interaction* between parties, excluding non-interactive rule sets. It captures HTTP (client-server interaction) and ACORD (insurer-agent data exchange) but may exclude single-entity protocols (if such things exist).

**Candidate C — Protocol as Verifiable Interaction Model:**
A Protocol is an interaction model whose conformance can be verified. This adds a falsifiability requirement: given an implementation, one can objectively determine whether it conforms to the protocol. This is the strongest candidate and aligns with how protocols are used in practice — conformance testing for HTTP, validation suites for FHIR, etc.

No final decision among these candidates has been reached. The RFC adopts Candidate C as the working hypothesis while acknowledging the question remains open.

### Formal Definition
A Protocol `P` is defined as a named set of declarations `{ sig1, sig2, ..., sigN }`, where each signature `sig` specifies a requirement — a method name, its parameters, and its expected return. These declarations specify *requirements* that any implementing entity must provide. A Protocol has no bodies, implementations, or data fields.

A Protocol Declaration takes the general form:
```
Protocol P : (extends other protocols)
    sig1(params) -> returnType
    sig2(params) -> returnType
    ...
```
- `P` inherits requirements from its extended protocols transitively.
- No signature may have a body. No state is allowed.

### Conformance
An entity conforms to a Protocol if and only if it provides implementations for *all* signatures declared by the Protocol (and its ancestors) with matching forms. Conformance can in principle be verified statically. The concept of conformance is separate from the concept of implementation: a Protocol declares requirements, and conformance is the measure of whether those requirements are satisfied, regardless of how they are satisfied.

### Protocol Identity
Protocols do not define identity. When multiple entities implement the same Protocol, each implements the required signatures separately; the Protocol does not create a shared parent identity or shared state between them. The Protocol is a specification, not an entity. It can be extended by other Protocols or fulfilled by implementers, but it is not itself a container of state or behavior.

### Protocol Ownership
A Protocol **owns nothing** beyond its name and declared signatures. It cannot own state or behavior — if a Protocol declaration would imply state (e.g., a default field) or behavior (e.g., a default method body), that violates Protocol properties. A Protocol "owns itself" in the sense that it exists as an independent conceptual entity, but this self-ownership does not extend to controlling the implementations that fulfill it.

### Protocol Properties
Regardless of which ontology candidate is ultimately adopted, the following properties are generally agreed upon:

- **Declarative:** A Protocol declares requirements; it does not provide implementations.
- **Stateless:** A Protocol itself holds no state. State resides in the entities that implement or participate in the protocol.
- **Behavior-free:** A Protocol specifies behavioral *expectations* (what should happen) but does not contain behavioral *implementations* (how to make it happen).
- **Composable:** Protocols can reference, extend, or compose other protocols. A secure messaging protocol might extend a base messaging protocol by adding encryption requirements.
- **Identity-free:** A Protocol does not define or confer identity on its implementers. Multiple implementers of the same Protocol are independent entities.

### Protocol Relationships
Protocols relate to each other in several ways. These relationships are important to name explicitly because many discussions about "inheritance" in software are actually about protocol relationships, and importing inheritance terminology imports assumptions from programming language history that may not apply:

- **Protocol Extension:** One protocol adds requirements on top of another. HTTP/2 extends HTTP by defining a new framing layer while preserving the semantic model. This is a *declarative* relationship — the extended protocol inherits *requirements*, not behavior.

- **Protocol Refinement:** A protocol narrows or constrains another. A "JSON-only" variant of a protocol refines the original by restricting the acceptable content types.

- **Protocol Composition:** Multiple protocols are combined. A "secure file transfer" protocol might compose a file transfer protocol with a security protocol. Each constituent protocol retains its identity; the composition creates a new, compound set of requirements.

None of these relationships involve the transfer of *implementation* or *behavior*. They are purely structural relationships between declarative specifications. This distinction is critical: protocol extension is not the same as class inheritance, and using inheritance terminology to describe protocol relationships obscures this fact.

### Inheritance Terminology Concerns
A major concern that emerged during these discussions is that many software conversations start from the assumption that "inheritance exists" and then split it into categories: "good inheritance" vs. "bad inheritance," "type inheritance" vs. "implementation inheritance," "interface inheritance" vs. "behavioral inheritance." This framing already assumes that inheritance is the correct conceptual model for the relationships being discussed.

In the protocol domain, terms like "protocol inheritance" or "sub-protocol" are often used when what is actually meant is protocol extension or protocol composition. These are fundamentally different from the inheritance mechanisms found in object-oriented languages, which transfer both structure and behavior. By being precise about terminology, we avoid importing flawed conceptual models from existing language ecosystems.

### Protocol-Specific Allowed and Rejected Patterns

| **Pattern** | **Status** | **Comment** |
|---------|----------|----------|
| Protocol with no method bodies | **Allowed** | Pure protocol declaration. |
| Protocol extends other protocols | **Allowed** | Protocol composition (declarative). |
| Protocol defining state (fields) | **Rejected** | Protocol must remain stateless. |
| Protocol with default method bodies | **Rejected** | Introduces behavior; violates protocol purity. |

Note: Patterns involving *implementing entities* (e.g., how an entity satisfies a protocol, whether delegation is explicit or implicit) are governed by the Explicit Behavior Ownership RFC, not this one.

## Drawbacks
- **Abstraction Risk:** Defining Protocol at a high level of generality may feel abstract and removed from the day-to-day concerns of a language designer or developer. The definition is intentionally conceptual, which means it does not immediately yield implementation guidance.
- **Terminology Friction:** Many developers are accustomed to using "protocol" loosely (e.g., "the HTTP protocol" meaning the IETF standard). A precise definition may feel pedantic or conflict with established usage in some communities.
- **Incomplete Finalization:** The ontology question (Rule Set vs. Interaction Model vs. Verifiable Interaction Model) remains open. Deferring this decision means the RFC's core definition carries inherent ambiguity.

## Rationale and Alternatives

### Why This RFC Is Needed
Without a clear, general definition of Protocol, every subsequent Memar RFC that references protocols risks ambiguity. The distinctions between Protocol, Contract, Standard, Specification, Interface, and Policy are not academic — they drive different design decisions. For example, if Protocol were conflated with Contract, one might incorrectly assume protocols imply bilateral obligations. If Protocol were conflated with Standard, one might incorrectly assume all protocols require ratification.

### Why Not Adopt a Language-Specific Definition?
An alternative would be to define Protocol purely in terms of Khayyam's `ab` (abstraction) construct: "a Protocol is what Khayyam calls an abstraction." This was rejected because it ties the concept to one language's implementation. The concept of Protocol existed long before Khayyam and exists in domains outside software. A language-specific definition would prevent Memar from reasoning about protocols in a general way.

### Why Not Treat Protocol and Interface as Equivalent?
Another alternative is to use "Interface" as the primary term, following Java and Go convention. This was rejected because "Interface" carries strong associations with programming language type systems, whereas "Protocol" captures the broader reality that interaction rules exist in networking, industry standards, organizational processes, and other domains where "interface" would be an awkward fit.

### Impact of Not Doing This
Without this RFC, the term "Protocol" remains undefined in the Memar framework. Discussions about protocol conformance, protocol composition, and protocol relationships would lack a shared foundation, leading to circular debates and inconsistent decisions across RFCs.

## Prior Art

### Networking Protocols
- **HTTP:** Defined across multiple IETF RFCs (RFC 9110, 9111, 9112, 9113, 9114). HTTP is a protocol — a set of rules for request/response exchange — that became an Internet Standard through IETF ratification. The protocol defines methods, status codes, headers, and body formats; the standard is the IETF's formal approval.
- **TCP/IP:** TCP (RFC 793) and IP (RFC 791) define the transport and network layers of the Internet protocol suite. These are foundational examples of protocols as interaction models with verifiable conformance.
- **SMTP:** RFC 5321 defines the Simple Mail Transfer Protocol. Like HTTP, it specifies message formats, command sequences, and response codes without prescribing implementation.

### Industry Standards
- **ISO 20022 (Finance):** A multi-part ISO standard defining messaging for financial transactions (payments, securities). It specifies message schemas and flows — a protocol for financial data exchange.
- **ISO 11783 / ISOBUS (Agriculture):** A protocol for tractor-machine communication, demonstrating that protocols exist in physical and mechanical domains, not just software.
- **IEC 62379 / AES70 (Audio):** Protocol for AV device control.
- **OPC UA (Industrial IoT):** A protocol standard for device interoperability in industrial settings.

### Domain-Specific Protocols
- **ACORD (Insurance):** Provides data exchange standards (XML schemas for insurance forms). These define allowed messages between insurers, agents, and regulators — protocol-like in that they specify message structure without dictating implementation.
- **HL7 / FHIR (Healthcare):** HL7 (v2, v3) and FHIR are standards for medical data exchange. HL7 v2 defines text-based message formats (segments and fields); FHIR defines a RESTful API protocol with JSON/XML schemas. Both are mature examples of high-level data protocols.
- **SWIFT (Finance):** The SWIFT MT and MX standards define protocols for interbank transfer message formats, ensuring consistent message structures across banks worldwide.
- **POSIX (Operating Systems):** IEEE 1003.1 is a Standard Interface Protocol for operating systems. It defines function calls (APIs) that an OS must provide. Although not a "protocol" in the networking sense, POSIX demonstrates that "protocol" can meaningfully describe an interface definition.

### API and Specification Ecosystems
- **OpenAPI:** A specification format for describing RESTful APIs. It is a specification *of* protocols — it documents the rules for interacting with an API.
- **GraphQL:** A query language and runtime for APIs. The GraphQL specification defines a protocol for data fetching, including query syntax, type system, and execution semantics.

### Programming Language Constructs (Partial Equivalents)
- **Swift Protocols:** Swift's `protocol` construct is structurally similar to a Protocol in the general sense — it declares method requirements without (necessarily) providing implementations.
- **Go Interfaces:** Go's `interface` describes method sets without default method code. However, Go's embedding mechanism allows implicit interface satisfaction, which blurs the ownership boundary.
- **Rust Traits:** Traits act like interfaces but can include default method implementations, which goes beyond pure protocol declaration.
- **Java Interfaces:** Originally pure (no behavior); Java 8 added default methods, moving away from protocol purity.
- **CORBA IDL, Protocol Buffers:** Interface Definition Languages that define protocols or data schemas in a language-agnostic way.

## Unresolved Questions
- **Protocol Versioning:** How should protocols evolve while maintaining backward compatibility? This RFC does not prescribe a versioning strategy, but versioning is crucial in practice (HTTP/1.1 to HTTP/2, HL7 v2 to FHIR).
- **Cross-Module and Cross-Organizational Protocols:** Can protocols span modules within a system or organizations? How is conformance coordinated when no single authority governs both sides? We assume an independent protocol definition can be imported as needed, but coordination mechanisms remain undefined.
- **Runtime Conformance Checks:** Protocols are fundamentally static specifications. Should there ever be optional runtime conformance verification? Generally no, but some domains (e.g., security protocols) might benefit. This is a tooling question that interacts with the EBO principle.
- **Multi-Language Protocol Compatibility:** If a protocol is used across language boundaries, how should its specification be encoded? This touches on tooling and specification formats but is beyond this RFC's scope.
- **Protocol vs Specification Identity:** Is a protocol identical to its specification, or does the conceptual protocol exist independently of any written document? The RFC leans toward treating them as distinct but acknowledges the question is unresolved.
- **Ontology Finalization:** The choice among Rule Set, Interaction Model, and Verifiable Interaction Model remains open. Future discussion and use-case analysis may favor one candidate.
- **Protocol Conformance Measurement:** If Candidate C (Verifiable Interaction Model) is adopted, what constitutes adequate conformance verification? This touches on tooling and is beyond this RFC's scope.

## Future Possibilities
- **Protocol Conformance RFC:** A dedicated RFC defining how conformance to a protocol is verified, including the role of testing, formal verification, and tooling.
- **Protocol Relationships RFC:** A dedicated RFC formalizing the taxonomy of protocol relationships (extension, refinement, composition) and the rules governing each.
- **Protocol Versioning RFC:** A dedicated RFC addressing how protocols evolve, deprecate, and maintain compatibility.
- **Standards and Terminology RFC:** A dedicated RFC examining the misuse of "standard" in software (e.g., "standard library" without independent validation), as touched upon in the Motivation section.

## Change Rationale
This RFC was created by splitting the original monolithic "Protocol" document (which contained Protocol, Explicit Behavior Ownership, and Khayyam Rejection of Inheritance as a single RFC) into three focused RFCs. The original document mixed ontological questions about Protocol with design principles about behavior ownership and language-level decisions about inheritance. This conflation made it difficult to discuss any one topic without being pulled into the others.

The Protocol portion was further refined by removing all Khayyam-specific implementation details, code examples, and entity references (capsule, abstraction, method) to ensure the RFC defines Protocol as a general, domain-independent concept. Content from the working notes — including Protocol Ontology Candidates, Protocol Relationships, Inheritance Terminology Concerns, and the Standard Library Criticism — was incorporated to enrich the ontological discussion.

## Related RFCs

| **RFC** | **Relationship** |
|---------|-----------------|
| explicit_behavior_ownership.md | **Extends.** Defines the design principle that governs how protocols are implemented (no default behavior, no implicit acquisition). |
| khayyam-rejection_of_inheritance.md | **Independent.** Addresses language-level decisions about inheritance; references Protocol definition from this RFC. |
| khayyam-protocols_vs_contracts.md | **See also.** Related concept; this RFC refines the Protocol side of that distinction. |
| khayyam-error_abstraction.md | **References.** Uses Protocols to define abstract error interfaces. |
| khayyam-rejection_of_default_implementations.md | **Superseded by** explicit_behavior_ownership.md. Default implementations violate protocol purity. |
| khayyam-rejection_of_method_promotion.md | **Superseded by** khayyam-rejection_of_inheritance.md. Method promotion is a form of implicit behavior inheritance. |