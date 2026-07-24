---
Title: "Protocol"
Status: Proposed
Start Date: 2026-06-21
RFC Number: 495002
Applied to: ["*"]
Related RFCs:
  - Title: "Terminology"
    URI: "./terminology.md"
    Reason: "Foundation Alignment"
    Explanation: "Terminology governs how concepts are understood across protocol"
  - Title: "System"
    URI: "./system.md"
    Reason: "Depends_on"
    Explanation: "System is now formally defined. This RFC's Protocol-Process-System ontology depends on System being a defined concept."
Contributor(s):
  - name: "Omid Hekayati"
    uri: "mailto:omid@geniuses.group"
    contribution: "Core ontological definition of Protocol, Protocol–Process–System relationship, Protocol–Science–Methodology connection, critique of 'standard' as third-party attestation, diplomatic and scientific protocol examples, methodology-based distinction between Protocol and Specification"
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
    effort: "High"
    contribution: "Split original monolithic RFC into three focused RFCs. Restructured Protocol RFC to be purely ontological. Enhanced with Protocol–Process–System relationship (systems theory), Protocol–Science–Methodology connection, diversified domain examples (diplomatic, scientific, medical, legal, aviation, sports), corrected Protocol vs Standard to define standard as third-party attestation, added methodology dimension to Protocol vs Specification, relabeled Formal Definition as language-level illustration, strengthened ontology candidate analysis with process argument."
    task: ["content-split", "restructuring", "enrichment", "ontological-revision"]
  - name: "Claude"
    uri: "https://claude.ai"
    model: "Claude Sonnet 5"
    effort: "medium - thinking"
    contribution: "Critical review pass: distinguished idea/discovery from structured lifecycle development within the Methodologically-produced property; added non-software methodology examples; corrected process cardinality (one-or-more, possibly nested) in the core definition and Process-bound property; flagged System and Process as undefined foundational dependencies; refined Protocol vs Standard to distinguish institutionalization attestation from maturity attestation, grounded in IETF RFC 6410 criteria."
    task: ["critical-review", "clarification", "ontological-revision"]
---

# Protocol

## Summary
This RFC defines the concept of **Protocol** as a general, domain-independent abstraction. **A Protocol is a named set of declarative rules that governs processes within a [system](./system.md)**. It specifies *what* must happen within a process — formats, sequences, behavioral expectations, state transitions — without prescribing *how* those requirements are fulfilled. The definition is intentionally not limited to programming languages or software systems; it must remain valid across networking, diplomacy, science, medicine, industry, law, and organizational processes. This RFC establishes the inseparable relationship between protocols, processes, and systems, and provides an ontological foundation for all subsequent Memar RFCs that reference protocols.

## Motivation

### The Fundamental Question
One of the most important open questions underlying the Memar framework is: **What exactly is a Protocol?** This question is intentionally broader than any single programming language construct. The intention is not to define "What is a Swift Protocol?" or "What is a Go Interface?" or "What is a Rust Trait?" — but rather to arrive at a definition of Protocol as a general concept whose validity extends beyond software engineering, into every domain where rules govern processes.

### Terminology Confusion in Practice
The term "protocol" is widely used but frequently conflated with other terms. The conflation is not limited to software — it is systemic across domains:

- In diplomacy, "protocol" is understood as ceremonial rules, while in networking the same word means message-format specifications. These are not different "types" of protocol — they are the same concept applied to different processes.
- Practitioners loosely call HTTP both "the HTTP protocol" and "the HTTP standard." One refers to the rules; the other misuses a word that actually means something else entirely (see Protocol vs Standard below).
- In object-oriented programming, terms like "interface", "trait", and "protocol" are treated as synonyms, erasing distinctions that matter for design decisions.
- In industry, ISO 9001 is called a "quality management standard" when it is actually a set of protocols whose institutionalization within an organization can then be *certified* by a third party — the certification being the true "standard" in the precise sense.
- In science, "research protocol" is used correctly, but the relationship between this protocol and the broader scientific method (itself a meta-protocol) is rarely made explicit.

This conflation creates real problems: when a team says "implement the protocol," do they mean follow the abstract rules, comply with a certification requirement, or satisfy a contractual obligation? Without precise definitions, these ambiguities propagate into design decisions.

### Why This Matters for Memar
Memar needs a stable, precise definition of Protocol because the concept serves as a foundational building block. If the term remains ambiguous, every subsequent RFC that references protocols inherits that ambiguity. By establishing a clear ontological foundation now — one grounded in the relationship between protocols, processes, and systems — we prevent conceptual leakage between related but distinct concerns such as behavior ownership, inheritance, and conformance, each of which has its own RFC.

## Guide-level Explanation

### What is a Protocol?
A Protocol is a named set of **declarative rules that govern one or more processes within a system**. It specifies *what* must happen — message formats, call sequences, expected behaviors, state transitions — without prescribing *how* those requirements are fulfilled. Think of HTTP: the protocol defines that a client sends a request line, headers, and an optional body, and that a server responds with a status line, headers, and a body. The protocol does not dictate whether the server is written in C, Python, or runs on bare metal.

This definition contains three inseparable components:

- **Rules**: The declarative requirements — what must happen, in what order, under what conditions.
- **Process**: The activity or sequence of activities the rules govern. A protocol without a process is rules on a shelf — a collection of statements with no domain of application. A process may itself be composed of an indeterminate number of nested sub-processes; a Protocol may govern a single process, several independent processes, or a process at any level of this nesting. The definition does not presuppose a single atomic process.
- **System**: The containing context within which the process operates. Protocols exist within systems; processes occur within systems; the system provides the boundary that gives the protocol its scope.

A protocol without a process is inert — it is a collection of statements with no domain of application. A process without protocol-governing rules is unstructured activity — it happens, but not reproducibly or verifiably. A system without protocols governing its internal processes is not a system in the systems-theory sense — it is merely a collection of independent elements with no defined interactions. The three co-arise: you cannot meaningfully discuss one without the others.

### Protocol Across Domains
The breadth of protocol application is not incidental — it is evidence that the concept is genuinely domain-independent. The following examples demonstrate that protocols govern processes across radically different systems:

**Networking and Communications:**
- **HTTP**: Governs the request-response process between clients and servers. The protocol defines methods, status codes, headers, and body formats; implementations vary from Apache to Nginx to a custom embedded server.
- **SMTP**: Governs the process of email transmission between mail agents. It specifies command sequences (HELO, MAIL FROM, RCPT TO, DATA) and response codes without dictating how any particular mail server is implemented.
- **TCP/IP**: Governs the process of reliable data delivery across networks. TCP defines connection establishment (three-way handshake), data transfer, and connection teardown as a protocol governing the data-delivery process.

**Diplomacy and International Relations:**
- **Diplomatic protocol**: Governs the process of official interactions between state representatives. It does not prescribe specific behaviors rigidly — it defines parameters within which culturally appropriate behavior must fit. For example, diplomatic dress protocol requires attire to be "clean and formally appropriate" without specifying that a Western business suit must be worn; an Arab diplomat may wear traditional dress in its finest form and fully satisfy the protocol. The protocol governs the diplomatic-interaction process while leaving room for cultural adaptation within defined boundaries.
- **Vienna Convention on Diplomatic Relations (1961)**: Codifies the protocol governing diplomatic missions — the process of accreditation, communication channels, privileges, and immunities. It is a protocol governing the state-to-state interaction process.

**Science and Research:**
- **Scientific method**: A meta-protocol that governs the process of knowledge production itself. It specifies that hypotheses must be testable and falsifiable, experiments must be reproducible, and conclusions must follow from evidence rather than authority. Without adherence to this protocol, the output is not science — it is speculation, anecdote, or opinion. The scientific method demonstrates that protocols are not merely "technical rules" but can be foundational to entire systems of knowledge.
- **Research protocol**: In clinical trials and laboratory research, a research protocol specifies the exact steps, measurements, controls, inclusion/exclusion criteria, and statistical methods that must be followed. Deviation from the research protocol — even if the results appear valid — invalidates the findings. The protocol governs the experimental process; the scientific method governs the broader knowledge-production process.
- **Peer review protocol**: Governs the process of evaluating research before publication — specifying anonymity requirements, evaluation criteria, revision procedures, and editorial decision-making. The protocol exists to ensure the reliability of the scientific-publication process within the scientific-knowledge system.

**Medicine and Healthcare:**
- **WHO Surgical Safety Checklist**: A protocol governing the process of preparing for and performing surgery. It specifies three phases — before anesthesia, before skin incision, and before the patient leaves the operating room — each with verification steps. The protocol does not tell the surgeon *how* to perform the operation; it governs the safety-verification process.
- **HL7 / FHIR**: Protocols governing the process of medical data exchange between healthcare information systems. They define message structures, terminologies, and workflow patterns without dictating how any particular hospital implements its IT systems.
- **Infection control protocol**: Governs the process of preventing disease transmission in clinical settings — hand hygiene procedures, sterilization sequences, isolation precautions. The protocol specifies what must be done; the hospital's systems determine how it is implemented.

**Industry and Quality Management:**
- **ISO 9001 quality management protocols**: A set of protocols governing quality management processes within an organization — process control requirements, documentation requirements, corrective action procedures, and continuous improvement cycles. These protocols specify what processes must exist and what controls they must have.
- **Construction safety protocol**: Governs the process of ensuring worker safety on construction sites — hard hat requirements, fall protection procedures, hazardous material handling sequences, incident reporting procedures.

**Law and Governance:**
- **Courtroom protocol**: Governs the process of judicial proceedings — how evidence is presented, how witnesses are examined and cross-examined, how objections are raised and ruled upon, how the judge directs proceedings. The protocol defines the trial process without prescribing verdicts.
- **Legislative protocol**: Governs the process of introducing, debating, amending, and passing legislation — bill formatting requirements, reading stages, voting procedures, veto processes.

**Aviation:**
- **Pre-flight protocol**: Governs the process of verifying aircraft readiness before takeoff. Each step must be completed in sequence; skipping a step is a protocol violation regardless of whether an incident occurs. The protocol governs the pre-flight-check process within the aviation safety system.

**Sports:**
- **Competition protocol**: Governs the process of conducting a sporting event. FIFA's Laws of the Game, for example, specify the rules governing the football-match process — field dimensions, player counts, scoring methods, foul definitions, and dispute-resolution procedures. The protocol governs the match process; the players and referees implement it.

**Software and Computing:**
- **POSIX**: Governs the process of OS service access through defined function calls. An OS either conforms or does not; POSIX does not dictate kernel implementation.
- **OpenAPI**: Governs the process of interacting with a RESTful API — endpoint definitions, parameter formats, response schemas, authentication flows.
- **Git workflow protocol**: Governs the process of version control collaboration — branch naming conventions, commit message formats, merge/rebase procedures, code review requirements. Different organizations define different Git protocols; the protocol governs the collaboration process.

**Key observation from these examples**: In every domain, the protocol does not exist in isolation. It governs a specific process within a specific system. The diplomatic protocol governs the diplomatic-interaction process within the international-relations system. The research protocol governs the experimental process within the scientific-knowledge system. The surgical safety protocol governs the surgery process within the healthcare-delivery system. Remove the process, and the protocol loses its meaning — it becomes inert text. Remove the system, and neither the process nor the protocol has a home.

### Protocol, Process, and System

The relationship between protocol, process, and system is not merely categorical — it is foundational, and it connects directly to systems theory and systems thinking.

A **system**, in the systems-theory sense, is a set of interacting components whose interactions produce behavior that no individual component produces alone. A car is not a system because of its parts — it is a system because of how its parts interact: the engine's power transmission process, the braking process, the steering process, each governed by engineering protocols. A cell is not a system because of its molecules — it is a system because of the metabolic processes those molecules participate in, each governed by biochemical protocols.

This reveals a structural chain:

> **System → `contains` → Processes → `governed by` → Protocols**

A system is defined by its processes. A process is defined by the rules that govern it. Those rules are protocols. Therefore, protocols are not merely "rules that happen to exist within systems" — they are part of what *makes a system a system*. Without protocols governing the interactions between components, you do not have a system; you have a pile of parts.

This has practical implications for the Memar framework. When we define a protocol in Memar, we are not just defining a set of method signatures — we are defining a governance structure for a process within a system. The protocol defines *what interactions must occur*; the implementing entities define *how those interactions occur*; the system provides the context within which both the process and its governance make sense.

The connection to systems thinking is also important. Systems thinking emphasizes understanding wholes rather than parts, relationships rather than entities, and patterns rather than isolated events. A protocol is precisely a formalization of a relationship pattern within a system. When we define protocols explicitly, we are practicing systems thinking at the level of interaction design.

### Protocol, Science, and Methodology

The connection between protocol and science runs deeper than the observation that "research has protocols." It touches the nature of knowledge production itself.

**Science is defined by its methodology.** A claim becomes "scientific" not because of its content, but because it was produced through adherence to the scientific method — a meta-protocol governing the knowledge-production process. The methodology is not separate from the science; it *constitutes* the science. An experiment conducted without following the research protocol does not produce scientific results, regardless of how interesting the findings appear. The output is, at best, an anecdote.

This reveals an important property of protocols: **protocols enable reproducibility and verifiability.** The scientific method works because the research protocol specifies exact steps, controls, and criteria. Another researcher can follow the same protocol and verify (or falsify) the results. Without the protocol, there is no basis for verification — and without verification, there is no science.

The same principle applies to software. An API protocol (like HTTP) enables reproducibility: any conforming client can interact with any conforming server and produce predictable results. A quality management protocol (like ISO 9001's process requirements) enables verifiability: an auditor can check whether the specified processes are being followed.

This connection also illuminates why protocols require **methodology for their production**. Science does not accept claims produced by arbitrary methods — it requires adherence to the scientific method as a protocol for knowledge production. Similarly, a protocol that governs a software system's interactions should itself be produced through a defined methodology, not ad hoc text. In Khayyam, the `ab` (abstraction) construct is one such methodological tool — a language-level mechanism for producing protocols that carry structural guarantees (no state, no behavior, pure declarative requirements). The abstraction construct ensures that what it produces is, by construction, a protocol and not merely a description.

The same requirement applies outside software. A diplomatic protocol such as the Vienna Convention did not emerge as a single author's draft; it was produced through structured multilateral negotiation, drafting committees, and formal ratification review — a methodology analogous in function, though different in form, to Khayyam's `ab` construct for code-level protocols. Similarly, a clinical research protocol must pass through structured ethics review (e.g., IRB approval) and methodological critique before it carries the status of a valid research protocol; a proposed experimental procedure that has not undergone this review remains a draft, not a protocol.

### Protocol vs Contract
A Contract implies **parties, obligations, and commitments**. When two organizations sign a contract, there are specific entities with reciprocal duties, and breach carries legal or formal consequences. A Protocol does not inherently require predefined parties. HTTP exists as a protocol regardless of whether any particular client and server are currently interacting. Any conformant participant can engage with the protocol without negotiating with a counterparty.

This distinction is not merely academic. In software design, conflating "protocol" with "contract" leads to assumptions about bilateral obligations that don't exist. A Memar Protocol is a one-sided specification: it declares requirements that govern a process, and any entity that satisfies those requirements conforms to the protocol — no negotiation needed. The contract question (who is obligated to whom, and what happens if obligations are not met) is a separate concern that exists at a different layer.

### Protocol vs Standard

The word "standard" is one of the most consistently misused terms in both technical and non-technical discourse. Clarifying its precise meaning is essential because the misuse is not harmless — it obscures a real distinction.

**Standard (precise definition):** A standard is a **third-party attestation** that an organization has **institutionalized** specific protocols within its processes. A standard is not a document, not a specification, and not a protocol. It is a certification — a statement from a qualified external body that protocols X, Y, and Z have been verified as operational within the certified organization's processes.

Consider ISO 9001. ISO 9001 itself is a document that defines quality management protocols. When a car factory "gets ISO 9001 certified," a third-party auditor (accredited by ISO but not employed by ISO — ISO itself explicitly states it does not issue certificates directly) verifies that the factory has institutionalized the specified protocols within its quality management processes. The certification does not mean the factory produces defect-free cars. It means the factory follows the specified protocols for quality management. The protocol is the rule set; the standard is the attestation that the rule set is operational.

Third-party attestation takes at least two forms, distinguished by what is being attested:

- **Institutionalization attestation** — a third party certifies that a *specific organization* has adopted and operationalized a protocol within its own processes (e.g., ISO 9001 certification of a factory).
- **Maturity attestation** — a third party certifies that a *protocol itself* has reached a defined level of technical maturity, based on objective evidence such as independent interoperable implementations and successful operational deployment (e.g., the IETF's promotion of a Proposed Standard to Internet Standard under RFC 6410, which requires at least two independent interoperating implementations with widespread deployment and no interoperability-blocking errata).

This definition has several important consequences:

1. **A protocol becomes a standard only through a defined attestation process, not through mere publication.** When the IETF publishes an RFC as a Proposed Standard, no attestation has yet occurred — this is closer to a specification being made public. Advancement to Internet Standard, by contrast, is a genuine maturity attestation: the IESG formally confirms, based on documented evidence of independent interoperable implementations and operational experience, that the protocol has met defined criteria (RFC 6410). What colloquially gets called "the HTTP standard" conflates two different moments — HTTP's publication as a specification, and, for the parts of HTTP that have reached that status, its attestation as an Internet Standard. These are not the same event, and the protocol's rules do not change between them; only its attested maturity status does.

2. **An organization can implement a protocol perfectly without ever obtaining a standard certification.** A company can follow all ISO 9001 protocols internally without paying an auditor. Their processes may be excellent. They simply lack the external attestation.

3. **An organization can hold a standard certification and still have poor outcomes.** A factory with ISO 9001 certification can still produce defective cars. The certification attests to protocol institutionalization, not to outcome quality.

4. **Standardization (the activity) is not the same as a standard (the attestation).** Organizations like ISO engage in standardization — the activity of defining protocols, promoting their adoption, and accrediting auditors who verify implementation. This activity is valuable and necessary. But the *word* "standard" should refer to the attestation, not to the protocols being standardized.

**Note on colloquial usage:** This precise definition differs from how "standard" is commonly used. In everyday language, people say "HTTP standard" or "industry standard" to mean "widely adopted protocol." This RFC adopts the precise definition: a standard is a third-party attestation — either of an organization's institutionalization of a protocol, or of a protocol's own technical maturity. This is not pedantry — it is the same kind of precision that distinguishes "the earth is spherical" from "the earth is flat." Widespread usage does not make imprecise usage correct.

### Protocol vs Specification
A specification is *how* something is documented. A protocol is *what* is documented. But this distinction, while correct, misses a deeper difference: **a protocol requires a methodology for its production; a specification does not.**

A specification can be any text. A hardware datasheet is a specification — it describes a component's characteristics in whatever format the manufacturer chooses. A README file is a specification — it describes a software project's setup instructions. A white paper is a specification — it describes a proposed approach. None of these require a specific production methodology. You can write a specification by sitting down and typing prose.

A protocol, by contrast, cannot be produced by arbitrary text generation. A protocol must be the output of a **structured method** that ensures the result actually governs a process verifiably. The methodology constrains what the protocol can say, how it is structured, and what guarantees it carries.

This distinction is visible in practice:
- A research paper *describing* experimental results is a specification of those results. The *research protocol* that governed how those results were produced is a separate, methodologically constrained document.
- An API specification *describing* endpoint behavior (e.g., an OpenAPI document) is a specification. The underlying interaction protocol that the API implements is a separate entity — the protocol is the *conceptual rule set* governing the interaction process; the specification is the *document* describing it.
- In Khayyam, the `ab` (abstraction) construct is a **methodological tool for producing protocols at the code level**. The language enforces that an abstraction declares only signatures — no state, no behavior, no implementations. This methodological constraint guarantees that the output is a protocol (pure declarative requirements) rather than a description or a mixed document. The abstraction is to protocol production what the scientific method is to knowledge production: a structured method that constrains the output to a specific, verifiable form.

Whether a protocol and its specification are identical remains an open philosophical question, but for practical purposes in Memar, they are treated as distinct: the protocol is the conceptual entity (the rules governing a process); the specification is its documentation (the text describing those rules). The methodology produces the protocol; the specification records it.

### Protocol vs API Specification

Within software engineering specifically, "protocol" and "API specification" are used almost interchangeably in casual discussion — "the API spec" and "the protocol" are often treated as two names for the same artifact. The general Protocol vs Specification distinction above applies here directly, but the API case deserves its own treatment, both because the conflation is extremely common in practice and because it is the specific instance the Terminology RFC's Motivation section points to as an example of a broader terminology failure (see the Terminology RFC).

An API specification — an OpenAPI/Swagger document, a gRPC `.proto` file, a GraphQL schema, a WSDL file — is a document, in a particular machine-readable or human-readable format, describing one particular interface's endpoints, message shapes, and invocation conventions. It is a specification in the sense already defined: it can, in principle, be produced simply by writing it down in the required format, and two people working independently could easily produce two different, non-equivalent API specifications while both intending to describe the same underlying interaction rules.

A Protocol, in the sense defined by this RFC, is the underlying, named set of declarative rules that govern the process those endpoints participate in — the ordering constraints, the required message content, the state transitions, the error semantics — independent of which document format is used to write those rules down, and independent of which programming language or framework will eventually implement them.

The relationship becomes concrete with a familiar case. HTTP is a protocol: a named set of rules governing request/response exchange between a client and a server process, defined independently of any particular API. An OpenAPI document describing one specific web service's endpoints is a specification: it documents one particular application of HTTP, plus that service's own conventions, to one particular set of resources. The OpenAPI document did not create HTTP as a protocol, and rewriting that OpenAPI document in a different format — a hand-written Markdown table, for instance — would not change the underlying protocol the API implements, provided the actual rules governing the interaction stayed the same.

This produces consequences that matter for Memar development in practice:

1. **Two API specifications, written in different formats or conventions, can describe the same protocol.** A REST API described in OpenAPI and an equivalent RPC-style API described in a `.proto` file can, in principle, govern the same underlying process with the same rules, expressed through two different specification formats and two different technology-level conventions. Confusing "the protocol" with "the OpenAPI document" makes this equivalence invisible, and can lead a team to treat a migration between API styles as a protocol change when it is only a specification-format change — or the reverse, treating an actual protocol change as a harmless format migration.

2. **A single API specification routinely bundles several distinct protocols.** A typical OpenAPI document usually documents authentication (governed by whatever auth protocol — OAuth2, API keys, mTLS — the service uses), the resource-manipulation interaction itself (governed by HTTP's own protocol rules plus the service's own resource-state-transition rules), and often versioning or pagination conventions that are themselves small protocols in their own right. Treating "the API spec" as one undifferentiated unit obscures the fact that several independent protocols, each with its own conformance rules and its own evolution path, have been bundled into a single document for convenience.

3. **A protocol can exist, and be reasoned about, before any API specification for it has been written.** Because a Protocol is methodologically produced (see "Protocol, Science, and Methodology," above) and is process-bound rather than document-bound, Memar contributors can define and critique a protocol's rules directly — as this RFC does for the general concept of Protocol itself — without first committing to an API specification format. The specification should be derived from an already-validated protocol, not the reverse; a protocol should not be inferred backward from whatever specification format a team happened to reach for first. This is the Concept-First-Thinking discipline the Terminology RFC establishes generally, applied to the specific case of API design.

Confusing these two concepts introduces implementation assumptions into architectural discussions that have no legitimate place there: a debate that is actually about a protocol's rules (should this operation be idempotent? what happens on partial failure?) gets misdiagnosed as a debate about specification format (should we use OpenAPI or a `.proto` file?), and vice versa. Protocols should be understood, designed, and critiqued independently of any particular specification format, framework, language, or vendor ecosystem; the specification is the document that, once the protocol is settled, records it for a particular audience and toolchain.

### Protocol vs Interface
Programming languages introduce constructs named "interface" (Java, Go), "protocol" (Swift), and "trait" (Rust). These are *code-level counterparts* of the broader concept of Protocol. They may represent partial aspects of the general concept — typically the structural requirement that certain methods or operations must exist. However, these language constructs often carry additional baggage: default implementations (Swift protocols, Rust traits), implicit behavior acquisition (Go embedding), or type-system constraints that go beyond pure interaction rules.

A Protocol in the general sense is not limited to method signatures. It can include message formats, state machine transitions, error handling expectations, sequencing rules, and process-level constraints that no single language construct fully captures. The programming language "interface" is a partial implementation of the general protocol concept, adapted to the specific needs of a type system.

### Protocol vs Policy
Policies are high-level directives for behavior or usage, often with discretionary enforcement — for example, "all emails must be encrypted" or "all API responses must include a correlation ID." A Protocol is narrower and more precise: it defines specific data formats, call sequences, and behavioral compatibility requirements that govern a process.

The relationship is often hierarchical: a policy might *mandate* the use of a protocol; the protocol itself specifies *how* the mandated behavior is achieved at the process level. For example, an organizational security policy might mandate that "all data transfers must use TLS." The TLS protocol then specifies exactly how the secure transfer process works — handshake sequences, cipher negotiation, certificate verification. The policy governs organizational behavior; the protocol governs the technical process.

## Reference-level Explanation

### Protocol Ontology Candidates
Several candidate definitions have emerged from discussion. The relationship between protocols, processes, and systems (established above) provides a lens for evaluating each.

**Candidate A — Protocol as Rule Set:**
A Protocol is simply a set of rules. This is the most minimal definition. Its weakness is twofold: first, "rule set" is extremely broad — a style guide is also a rule set, but not a protocol. Second, and more fundamentally, a rule set without a process to govern is inert. A style guide does not govern a process; it provides guidance for individual decisions. A protocol must govern a *process* — a sequence of interactions or activities within a system. The rule-set definition fails because it omits both the process and the system, leaving only the rules.

**Candidate B — Protocol as Interaction Model:**
A Protocol is a specification of how independent entities interact. This adds the constraint of *interaction* between parties, which implicitly introduces process (interaction is a process) and partially introduces system (interactions occur within a system). It captures HTTP (client-server interaction) and ACORD (insurer-agent data exchange). The remaining weakness is that it does not explicitly name the process or the system, making it easy to accidentally treat the protocol as floating free of context.

**Candidate C — Protocol as Verifiable Interaction Model:**
A Protocol is an interaction model whose conformance can be verified. This adds a falsifiability requirement: given an implementation, one can objectively determine whether it conforms to the protocol. This aligns with how protocols are used in practice — conformance testing for HTTP, validation suites for FHIR, audit procedures for ISO 9001 protocols. The verifiability requirement also connects directly to the science connection: just as the scientific method requires reproducibility (a form of verification), a protocol that cannot be verified cannot serve its purpose of governing a process reliably.

No final decision among these candidates has been reached. The RFC adopts Candidate C as the working hypothesis while acknowledging the question remains open. The process and system components established in this RFC apply regardless of which candidate is ultimately chosen.

### Formal Definition (Language-Level Illustration)

The following is an illustration of how the general concept of Protocol manifests at the programming language level. This is not the general definition — it is one specific instance of how a language can give structural form to the protocol concept.

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

This language-level form captures the general protocol properties (declarative, stateless, behavior-free) within the specific context of a programming language's type system. Other domains express protocols differently: diplomatic protocols use procedural text, scientific protocols use structured experimental designs, and aviation protocols use checklists. The underlying concept — declarative rules governing a process — is the same.

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
- **Process-bound:** A Protocol governs one or more processes within a system. A process may itself contain an indeterminate number of nested sub-processes, and a Protocol may bind to a process at any level of this hierarchy, or govern several processes at once. A protocol with no process it governs, at any level, is not a protocol — it is inert text. This is the property that distinguishes protocols from general rule sets like style guides or personal preferences.
- **Methodologically produced:** A Protocol is the product of a structured method applied across its full lifecycle — from initial ideation, through structured proposal and formulation, to critical review and validation. Methodology is not limited to a final verification step; it also governs how the underlying idea is formed and disciplined in the first place, just as reasoning itself depends on learned structures (language, domain training, disciplinary method) rather than occurring in a vacuum. However, an idea or draft, however well-considered, does not by itself carry Protocol status. It must pass through this structured refinement before it earns that status — mirroring, without being identical to, the progression from idea to hypothesis to tested theory in science. A text that has not undergone this progression remains a draft or proposal, not a Protocol.

### Protocol Relationships
Protocols relate to each other in several ways. These relationships are important to name explicitly because many discussions about "inheritance" in software are actually about protocol relationships, and importing inheritance terminology imports assumptions from programming language history that may not apply:

- **Protocol Extension:** One protocol adds requirements on top of another, introducing a new dimension of requirement the base protocol did not address at all. HTTP/2 extends HTTP by defining a new framing layer while preserving the semantic model. This is a *declarative* relationship — the extended protocol inherits *requirements*, not behavior.

- **Protocol Refinement:** A protocol narrows the acceptable value space of a requirement the base protocol already made, without introducing a new dimension of requirement. BSON refines JSON in this sense: BSON does not introduce a kind of requirement JSON entirely lacked — both remain structured, self-describing document formats — it constrains and extends JSON's existing type system, adding explicit binary and date types where JSON only offered generic numbers and strings, while preserving JSON's own document-shape rules.

The formal boundary between Extension and Refinement is not yet fully settled. Because adding any new requirement necessarily also shrinks the set of conforming implementations, every Extension is, in one sense, also a restriction. The working distinction above — Extension adds a new *dimension* of requirement; Refinement narrows the *value space* of a dimension the base protocol already had — is a first approximation, flagged as an open question below rather than treated as settled.

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
- **Terminology Friction:** Many developers are accustomed to using "protocol" loosely (e.g., "the HTTP protocol" meaning the IETF standard) and "standard" even more loosely. A precise definition may feel pedantic or conflict with established usage in some communities. However, widespread imprecise usage does not invalidate precise definition — any more than widespread belief in a flat earth invalidates the spherical model.
- **Incomplete Finalization:** The ontology question (Rule Set vs. Interaction Model vs. Verifiable Interaction Model) remains open. Deferring this decision means the RFC's core definition carries inherent ambiguity, though the process and system components apply regardless of which candidate is ultimately chosen.
- **Precision Cost:** Maintaining a precise definition of Protocol — and distinguishing it from Contract, Standard, Specification, Interface, and Policy — imposes a cognitive cost on readers and contributors. Every time these terms are used in subsequent RFCs, the distinction must be maintained. This cost is accepted as a necessary investment in conceptual clarity.

## Rationale and Alternatives

### Why This RFC Is Needed
Without a clear, general definition of Protocol, every subsequent Memar RFC that references protocols risks ambiguity. The distinctions between Protocol, Contract, Standard, Specification, Interface, and Policy are not academic — they drive different design decisions. For example, if Protocol were conflated with Contract, one might incorrectly assume protocols imply bilateral obligations. If Protocol were conflated with Standard, one might incorrectly assume all protocols require third-party certification.

### Why Not Adopt a Language-Specific Definition?
An alternative would be to define Protocol purely in terms of Khayyam's `ab` (abstraction) construct: "a Protocol is what Khayyam calls an abstraction." This was rejected because it ties the concept to one language's implementation. The concept of Protocol existed long before Khayyam and exists in domains outside software. A language-specific definition would prevent Memar from reasoning about protocols in a general way.

### Why Not Treat Protocol and Interface as Equivalent?
Another alternative is to use "Interface" as the primary term, following Java and Go convention. This was rejected because "Interface" carries strong associations with programming language type systems, whereas "Protocol" captures the broader reality that interaction rules exist in networking, diplomacy, science, industry, organizational processes, and other domains where "interface" would be an awkward fit.

### Why Define Standard as Third-Party Attestation?
An alternative is to accept the common usage where "standard" means "widely adopted protocol specification" (e.g., "HTTP is a web standard"). This was rejected because it collapses two genuinely distinct concepts into one word. The protocol (the rules governing a process) and the attestation (the certification that those rules are institutionalized) are different things with different properties, different producers, and different consumers. A company can follow a protocol without holding a standard certification. A company can hold a standard certification and still produce poor outcomes. These facts demonstrate that the two concepts are distinct, and precision requires distinct words.

### Impact of Not Doing This
Without this RFC, the term "Protocol" remains undefined in the Memar framework. Discussions about protocol conformance, protocol composition, and protocol relationships would lack a shared foundation, leading to circular debates and inconsistent decisions across RFCs.

## Prior Art

### Networking Protocols
- **HTTP:** Defined across multiple IETF RFCs (RFC 9110, 9111, 9112, 9113, 9114). HTTP is a protocol — a set of rules governing the request-response process between clients and servers. IETF has ratified this protocol; this ratification is often colloquially called "making it a standard," but per this RFC's definitions, the protocol's rules are unchanged by ratification. What changes is the governance status, not the ontological nature of the entity.
- **TCP/IP:** TCP (RFC 793) and IP (RFC 791) define the transport and network layers of the Internet protocol suite. These are foundational examples of protocols as interaction models with verifiable conformance.
- **SMTP:** RFC 5321 defines the Simple Mail Transfer Protocol. It specifies message formats, command sequences, and response codes without prescribing implementation — a protocol governing the email-transmission process.

### Diplomatic and Social Protocols
- **Vienna Convention on Diplomatic Relations (1961):** An international treaty codifying the protocol governing diplomatic missions. It defines the process of accreditation, communication, privileges, and immunities. It is a protocol governing the state-to-state interaction process.
- **United Nations Protocol and Liaison Service:** Responsible for the protocol governing the organization's official meetings, ceremonies, and diplomatic interactions. The service's existence demonstrates that even at the highest levels of international organization, protocol management is recognized as a distinct, essential function.
- **Courtroom protocol (various jurisdictions):** Rules governing the process of judicial proceedings. These protocols vary by jurisdiction but share a common structure: they define who may speak, in what order, under what conditions, and with what consequences for violations.

### Scientific and Research Protocols
- **The Scientific Method:** The foundational meta-protocol of all modern science. It governs the process of knowledge production by requiring hypotheses to be testable and falsifiable, experiments to be reproducible, and conclusions to follow from evidence. The methodology is inseparable from the science it produces.
- **Clinical Trial Protocols (ICH-GCP):** The International Council for Harmonisation's Good Clinical Practice guidelines define the protocol structure for clinical trials — objectives, design, methodology, statistical considerations, and organization. A clinical trial without a registered protocol cannot produce valid scientific evidence.
- **Laboratory Protocols:** In chemistry, biology, and physics, laboratory protocols specify the exact steps, reagents, conditions, and measurements required for an experiment. The protocol ensures reproducibility: another researcher following the same protocol in another laboratory should obtain comparable results.

### Industry and Organizational Protocols
- **ISO 9001 (Quality Management):** Defines protocols governing quality management processes — process control, documentation, corrective action, continuous improvement. ISO itself does not issue certifications; it accredits third-party auditors who verify that organizations have institutionalized these protocols. The protocols are the rules; the certification (the "standard" in the precise sense) is the attestation.
- **ISO 27001 (Information Security):** Defines protocols governing information security management processes — risk assessment, access control, incident management. Same certification model as ISO 9001.
- **ISO 20022 (Finance):** A multi-part standard defining messaging protocols for financial transactions (payments, securities). It specifies message schemas and flows — protocols for financial data exchange processes.
- **Construction Safety Protocols (OSHA):** Occupational Safety and Health Administration standards define protocols governing workplace safety processes — hazard identification, protective equipment requirements, incident reporting procedures.

### Domain-Specific Protocols
- **ACORD (Insurance):** Provides data exchange protocols for insurance forms. These define allowed messages between insurers, agents, and regulators — protocols for the insurance-data-exchange process.
- **HL7 / FHIR (Healthcare):** HL7 (v2, v3) and FHIR are protocols for medical data exchange processes. HL7 v2 defines text-based message formats; FHIR defines a RESTful API protocol with JSON/XML schemas.
- **SWIFT (Finance):** The SWIFT MT and MX protocols define rules for interbank transfer message formats, ensuring consistent message structures across banks worldwide — a protocol governing the interbank-transfer process.
- **OPC UA (Industrial IoT):** A protocol for device interoperability in industrial settings — governing the device-communication process within industrial automation systems.

### API and Specification Ecosystems
- **OpenAPI:** A specification format for describing RESTful APIs. It is a specification *of* protocols — it documents the rules for interacting with an API process.
- **GraphQL:** A query language and runtime for APIs. The GraphQL specification defines a protocol for the data-fetching process, including query syntax, type system, and execution semantics.

### Programming Language Constructs (Partial Equivalents)
- **Swift Protocols:** Swift's `protocol` construct is structurally similar to a Protocol in the general sense — it declares method requirements without (necessarily) providing implementations.
- **Go Interfaces:** Go's `interface` describes method sets without default method code. However, Go's embedding mechanism allows implicit interface satisfaction, which blurs the ownership boundary.
- **Rust Traits:** Traits act like interfaces but can include default method implementations, which goes beyond pure protocol declaration.
- **Java Interfaces:** Originally pure (no behavior); Java 8 added default methods, moving away from protocol purity.
- **CORBA IDL, Protocol Buffers:** Interface Definition Languages that define protocols or data schemas in a language-agnostic way.

## Unresolved Questions
- **Foundational Dependency on Process:** This RFC's ontology depends on Process as a prerequisite concept. System is now formally defined (see the System RFC, referenced above), but Process does not yet have a dedicated Memar RFC. Until one exists, Process is treated as an intuitively-understood primitive (drawn from systems theory) rather than a formally defined Memar concept. This RFC's Related RFCs field should be updated to reference a Process RFC once one is drafted.
- **Extension vs. Refinement boundary:** What is the precise, non-example-dependent formal criterion that separates Protocol Extension from Protocol Refinement? The working distinction (a new requirement dimension vs. a narrowed value space within an existing dimension) needs to be tested against more cases — BSON vs. JSON, HTTP/2 vs. HTTP/1.1, and others — before it can be considered settled.
- **Protocol Versioning:** How should protocols evolve while maintaining backward compatibility? This RFC does not prescribe a versioning strategy, but versioning is crucial in practice (HTTP/1.1 to HTTP/2, HL7 v2 to FHIR).
- **Cross-Module and Cross-Organizational Protocols:** Can protocols span modules within a system or organizations? How is conformance coordinated when no single authority governs both sides? We assume an independent protocol definition can be imported as needed, but coordination mechanisms remain undefined.
- **Runtime Conformance Checks:** Protocols are fundamentally static specifications. Should there ever be optional runtime conformance verification? Generally no, but some domains (e.g., security protocols) might benefit. This is a tooling question that interacts with the EBO principle.
- **Multi-Language Protocol Compatibility:** If a protocol is used across language boundaries, how should its specification be encoded? This touches on tooling and specification formats but is beyond this RFC's scope.
- **Protocol vs Specification Identity:** Is a protocol identical to its specification, or does the conceptual protocol exist independently of any written document? The RFC leans toward treating them as distinct (the protocol is the rules governing a process; the specification is the document describing those rules) but acknowledges the question is unresolved.
- **Ontology Finalization:** The choice among Rule Set, Interaction Model, and Verifiable Interaction Model remains open. The addition of process and system as required components may favor Candidate B or C over Candidate A, but formal analysis is needed.
- **Protocol Conformance Measurement:** If Candidate C (Verifiable Interaction Model) is adopted, what constitutes adequate conformance verification? This touches on tooling and is beyond this RFC's scope.

## Future Possibilities
- **Protocol Conformance RFC:** A dedicated RFC defining how conformance to a protocol is verified, including the role of testing, formal verification, and tooling.
- **Protocol Relationships RFC:** A dedicated RFC formalizing the taxonomy of protocol relationships (extension, refinement, composition) and the rules governing each.
- **Protocol Versioning RFC:** A dedicated RFC addressing how protocols evolve, deprecate, and maintain compatibility.
- **Terminology Governance RFC:** A dedicated RFC examining how Memar defines and governs its terminology, including the mechanism by which RFC definitions take precedence over colloquial or ecosystem usage when ambiguity arises. This interacts with the Framework RFC's document-authority principles.

## Change Rationale
This RFC was created by splitting the original monolithic "Protocol" document (which contained Protocol, Explicit Behavior Ownership, and Khayyam Rejection of Inheritance as a single RFC) into three focused RFCs. The original document mixed ontological questions about Protocol with design principles about behavior ownership and language-level decisions about inheritance. This conflation made it difficult to discuss any one topic without being pulled into the others.

The Protocol portion was further refined by removing all Khayyam-specific implementation details, code examples, and entity references (capsule, abstraction, method) to ensure the RFC defines Protocol as a general, domain-independent concept. Content from the working notes — including Protocol Ontology Candidates, Protocol Relationships, and Inheritance Terminology Concerns — was incorporated to enrich the ontological discussion.

In a subsequent review cycle, the Protocol definition was substantially revised to:
- Establish the inseparable relationship between protocols, processes, and systems, drawing on systems theory.
- Establish the connection between protocols and science, demonstrating that protocols are foundational to knowledge production through methodology.
- Diversify domain examples beyond networking and software to include diplomacy, science, medicine, law, aviation, sports, and industry.
- Correct the Protocol vs Standard distinction: "standard" is defined as third-party attestation of protocol institutionalization, not as a synonym for "ratified protocol."
- Enhance the Protocol vs Specification distinction with the methodology dimension: protocols require structured production methods; specifications do not.
- Relabel the Formal Definition as a language-level illustration rather than the general definition.
- Strengthen the ontology candidate analysis by evaluating each against the process and system requirements.
- Add "Process-bound" and "Methodologically produced" to the Protocol Properties list.

In a further review cycle (critical review with Claude), the Protocol definition was refined to:
- Distinguish idea/discovery from structured lifecycle development within the "Methodologically produced" property, so that the property does not read as requiring committee-style production from the first moment of ideation, while still holding that an unrefined idea or draft does not by itself carry Protocol status — analogous to the idea → hypothesis → tested theory progression in science.
- Add non-software examples of protocol-production methodology (diplomatic treaty negotiation, clinical research ethics review) alongside the existing Khayyam `ab` example, so the property is not illustrated by software alone.
- Correct process cardinality: a Protocol governs "one or more processes," not "a process," and processes may themselves be nested into sub-processes, with a Protocol able to bind at any level of that hierarchy.
- Flag System and Process as undefined foundational dependencies in Unresolved Questions, pending dedicated Memar RFCs for each.
- Refine Protocol vs Standard to distinguish two forms of third-party attestation — institutionalization attestation (the ISO 9001 model) and maturity attestation (the IETF Internet Standard model, per RFC 6410's criteria of independent interoperable implementations and operational experience) — correcting the prior framing that treated IETF ratification as mere colloquial misuse rather than a genuine, if differently-scoped, attestation.

In a further review cycle, following the Terminology RFC's own review:
- Added a dedicated "Protocol vs API Specification" section, migrating and substantially expanding the treatment that previously lived, in simplified and slightly inconsistent form, inside the Terminology RFC's worked examples. This keeps Terminology free of dependencies on other RFCs (per that RFC's own foundational-RFC positioning) while giving the API-specification case — the single most common real-world instance of the protocol/specification conflation — a treatment grounded in this RFC's actual finalized definitions, rather than the simplified restatement that previously appeared elsewhere.
- Replaced the abstract "JSON-only variant" example under Protocol Refinement with the concrete BSON-vs-JSON case, and made explicit that the formal boundary between Protocol Extension and Protocol Refinement remains unresolved, rather than implying the two examples given settle the distinction.

In a further review cycle, after the System RFC was finalized and referenced here:
- Restored a "Foundational Dependency" item under Unresolved Questions, narrowed to Process only. The prior version of this item, which covered both System and Process, appears to have been fully removed when the System RFC was added to Related RFCs, even though only the System half of that dependency was actually resolved — Process still lacks a dedicated Memar RFC. This is corrected so the still-open half of the dependency is not silently dropped.
- Trimmed the Summary's closing sentence, which previously previewed the full list of concepts this RFC distinguishes Protocol from (Contract, Standard, Specification, Interface, Policy). Per the Terminology RFC's Definition vs. Explanation distinction, a roadmap of Reference-level subsections is Explanation-type content, not Definition-type content, and does not belong in Summary.
