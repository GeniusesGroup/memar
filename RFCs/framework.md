---
Title: "The Relationship Between Framework, Language, and Operating System"
Status: Proposed
Start Date: 2026-06-30
RFC Number: 000001
Applied to: ["*"]
Related RFCs: []
Author(s):
  - name: "Omid Hekayati"
    uri: "mailto:omid@geniuses.group"
    contribution: "Core architectural stance, document authority principle, terminology governance concept, word-weight rebalancing vision"
    task: []
  - name: "Gemini"
    URI: "https://gemini.google.com/"
    Model: "3.1 pro"
    Effort: "Extended thinking enabled"
    Contribution: "Drafted initial text, argued for and against alternatives, incorporated revisions"
    Task: []
  - name: "Claude"
    URI: "https://claude.ai"
    Model: "claude-sonnet-5"
    Effort: "Medium - extended thinking enabled"
    Contribution: "Drafted initial text, argued for and against alternatives, incorporated revisions"
    Task: []
  - name: "Super Z"
    uri: "https://z.ai"
    model: "GLM"
    effort: "Medium"
    contribution: "Added Document Authority and Terminology Governance section, formalized the Word-Weight Rebalancing concept for AI model integration with Memar RFCs"
    task: ["terminology-governance", "document-authority"]
---

## Summary
The conventional hierarchy in software development places the framework as a guest living inside a language and operating system — the language defines what is expressible, the OS defines what is executable, and the framework merely organizes how developers use both. Memar inverts this: the **framework** is the primary architectural authority. The language and the operating system are components whose design assumptions are themselves defined by the framework, not the other way around.

## Motivation
When a framework is subordinate to a language and an OS, it inherits every assumption those layers baked in — often assumptions made decades ago for very different hardware, scale, and application models. A framework built inside Go must accept Go's concurrency model, Go's memory model, and Go's standard library conventions. A framework built on Linux must accept POSIX's process/thread model, its I/O abstractions, and its general-purpose kernel interface. These inherited assumptions are invisible until they become constraints, at which point they are very expensive to remove.

The deeper problem is that these layers were never designed with each other in mind at the architectural level. A language is typically designed to be OS-agnostic and framework-agnostic. An OS is typically designed to be language-agnostic. A framework, arriving last, is left to patch the gaps between whatever assumptions the first two happened to make independently. The result is a stack of layers that each hide complexity from the layer above — and where each layer's hidden complexity eventually leaks upward as surprising constraints, performance cliffs, or security surfaces.

Memar's position is that this ordering is historical accident, not architectural necessity. A framework that defines its own assumptions first — and then specifies what language and OS behavior it needs to support those assumptions — can maintain coherence across all three layers rather than inheriting incoherence from two independent prior decisions.

## Guide-level explanation
In Memar's model, a developer working on a business feature does not think about "which OS API to call" or "which language runtime to trust." They think about the domain model and the framework's contracts. The OS and the language are implementation details of those contracts — present, but not surfaced. This is the same thinking behind Unikernel architectures, where the application and the OS are compiled together into a single artifact with no general-purpose kernel in between: the application does not "call the OS," it is co-designed with the minimal substrate it actually needs.

Concretely, this means:
- The Khayyam language is not "Memar's language" in the sense that Memar is a framework for Khayyam. Khayyam is a language whose design assumptions are specified by Memar, so that code written in Khayyam already expresses the architectural constraints Memar cares about — explicit state, explicit error paths, no hidden control flow, no invisible allocations.
- An OS running Memar applications is not a general-purpose OS that Memar happens to run on. It is a substrate whose interface is defined by what Memar actually needs — no more. In a fully realized deployment, this means a Unikernel or Exokernel model, not a POSIX kernel offering thousands of syscalls that the application will never use.
- Memar is implemented as libraries across multiple languages and runtimes, at different levels of completeness: a Go implementation (`memar-go`) that has been production-tested in a real business deployment; a JavaScript implementation covering select subsystems only (error handling, services) with no current timeline for further completion; a Rust implementation not yet started, with its repository reserved for future work contingent on additional contributor capacity; and Khayyam itself, still under active design. "Framework as architectural authority" does not require every language binding to be complete or even started — it means Memar's design principles are the starting point that any such binding must conform to, whenever and to whatever extent it is undertaken.

## Reference-level explanation
This RFC has no syntax or grammar implications — it is an architectural stance that shapes the design decisions made in every subsequent RFC. Specifically:
- It is the reason why control flow keywords, memory management, concurrency primitives, and standard library shapes are not baked into the Khayyam language itself but instead live in the Memar framework (RFC 000003, RFC 000008, RFC 000011).
- It is the reason why the framework's recommended toolchain (compiler, linter, scaffolding) is designed as a coherent unit rather than as independent tools that happen to be compatible.
- It is the reason why architectural constraints (e.g. "no hidden state," "every error path must be visible") are expressed as framework-level contracts rather than as optional conventions.

## Drawbacks
Inverting the conventional hierarchy does not make Memar incompatible with existing languages and operating systems — a Go implementation has been built and production-tested in a real business context, and partial implementations exist in other languages. However, this cost is not merely a one-time adaptation friction: a concrete instance already occurred in `memar-go`, where introducing Go generics into an already-working, production-tested implementation produced widespread breakage that, after being deferred for roughly two years, was determined to be unresolvable within Go's generics model rather than merely time-consuming to fix (see [memar-go generics elimination RFC]). This is cited as direct evidence for the RFC's core claim — that friction from implementing framework principles atop a language with different assumptions compounds over time rather than being paid once — rather than a hypothetical risk.

## Rationale and alternatives
The conventional model (framework lives inside language and OS) was rejected because it guarantees that the framework will eventually be constrained by assumptions it did not make and cannot change. The cost of that constraint compounds over time — each new capability the framework needs must be negotiated against what the language and OS already decided, rather than being specified from first principles. Memar's inversion accepts a higher initial cost (no incremental adoption, no reuse of existing language/OS tooling without design review) in exchange for eliminating that compounding constraint cost.

## Prior art
- **Unikernel projects** (MirageOS, IncludeOS, Nanos): the closest architectural parallel, specifically in their treatment of the OS as a consequence of the application's requirements rather than a given substrate.
- **Singularity (Microsoft Research)**: an OS research project that co-designed the language (Sing#) and the OS from shared first principles, rather than fitting a language onto an existing OS.
- **Erlang/BEAM**: a language+runtime that is, in practice, its own OS-like substrate — the BEAM VM defines process scheduling, memory isolation, and fault tolerance in ways that make the underlying OS largely irrelevant to application code.
- **General-purpose OS + framework combinations** (Spring Boot on JVM on Linux, Rails on Ruby on Linux): the conventional prior art being explicitly rejected, not because they are bad engineering for their context, but because their inherited-assumption problem is well-documented and the cost of navigating it is visible in every large codebase that has lived long enough.

## Document Authority and Terminology Governance

### The Authority Principle
Memar RFCs are the authoritative source for all terminology used within the framework. When ambiguity exists between common or colloquial usage of a term and the definition established in a Memar RFC, the RFC definition takes precedence within the Memar ecosystem. This is not an assertion that the rest of the world is wrong — it is the same principle that governs any specialized domain. In law, statutory definitions differ from colloquial ones and courts follow the statutory meaning. In medicine, clinical terminology differs from everyday language and practitioners follow the clinical meaning. In physics, "force" has a precise definition that differs from how the word is used in everyday speech, and no physicist apologizes for this precision.

The purpose of this principle is not to change how the world uses words. The purpose is to ensure that within the Memar ecosystem, every participant — human or AI — can rely on stable, precise definitions rather than guessing which of several colloquial meanings is intended. A framework whose foundational terms are ambiguous is a framework whose every subsequent decision inherits that ambiguity.

### How Authority Is Established
Authority over a term is established when an RFC explicitly defines that term and provides a rationale for the definition. The definition must include:

1. **The precise definition itself** — what the term means within Memar.
2. **Distinctions from related terms** — what the term is not, and why the distinction matters.
3. **Acknowledgment of colloquial usage** — a brief note on how the term is commonly used differently, so readers understand the gap between Memar's usage and the world's.
4. **Rationale for the choice** — why this specific definition serves the framework better than alternatives.

The Protocol RFC (RFC 495465) is the first concrete application of this principle: it defines "Protocol" precisely, distinguishes it from Contract, Standard, Specification, Interface, and Policy, acknowledges that colloquial usage conflates these terms, and provides rationale for each distinction.

### How Authority Is Maintained
Once a term is defined in an RFC:

- **Subsequent RFCs must use the term according to its RFC-established definition.** If an RFC author needs to use a term in a way that differs from the established definition, they must either (a) use a different term, or (b) write a new RFC that revises the definition with explicit rationale.
- **Revision is possible but costly.** An RFC that revises an established definition must explain what changed, why, and what the implications are for all existing RFCs that use the term. This cost is intentional — it discourages casual redefinition while preserving the ability to correct genuine errors.
- **Ambiguity is resolved by reference, not by popularity.** When a term is ambiguous (e.g., 99% of developers use "standard" to mean "widely adopted protocol"), the RFC definition wins. The fact that the colloquial usage is more popular is irrelevant — popularity does not determine precision. This is the same principle by which scientific terminology is governed: the fact that most people call all reptiles "lizards" does not make the colloquial usage correct for zoological taxonomy.

### Terminology Governance and AI Models

A specific challenge that Memar must address — one that is increasingly important as AI-assisted development becomes standard — is that AI models are trained on the same ambiguous, conflated usage that this RFC seeks to correct. When an AI assistant encounters the word "standard" in a Memar context, its training data biases it toward the colloquial meaning ("widely adopted specification") rather than Memar's precise meaning ("third-party attestation of protocol institutionalization").

This is not a defect of AI models — it is a consequence of training on human-generated text, which contains the same ambiguities. The solution is not to fix the training data (impossible at the framework's scale) but to establish a mechanism by which the framework's precise definitions carry higher weight than the training data's ambient usage.

**Word-Weight Rebalancing** is the concept for this mechanism. In a fully realized implementation, an AI model operating within the Memar ecosystem would:

1. **Load Memar RFC definitions as a high-weight context layer.** The definitions in RFCs are treated as authoritative references that override the model's default weights for those terms.
2. **Resolve ambiguities by reference.** When the model encounters a term that has both a colloquial meaning and an RFC-established meaning, the RFC meaning takes precedence in any Memar-related context.
3. **Flag conflicts explicitly.** If the model detects that a user's usage of a term conflicts with the RFC definition, it should note the conflict rather than silently adopting the colloquial meaning. The model does not correct the user — it informs them of the framework's definition.
4. **Propagate definitions consistently.** When one RFC references a term defined in another, the model should use the referenced definition, not its training-data understanding of the term.

This concept is not limited to AI models. Human participants in the Memar ecosystem benefit from the same principle: when an RFC has defined a term, that definition is the reference. The difference is that humans can choose to ignore the reference; the word-weight rebalancing mechanism makes it easier for AI assistants to respect it by default.

### Scope of This Governance
Terminology governance applies to terms that are explicitly defined in Memar RFCs. It does not apply to general English (or Persian, or any other natural language) usage of words that have not been defined by an RFC. The framework does not seek to govern the entire language — only the specific terms that it has taken the responsibility to define precisely.

## Unresolved questions
None at this time. This RFC is intentionally a statement of architectural stance, not a specification of a concrete mechanism — the concrete mechanisms flow from it in subsequent RFCs.

## Future possibilities
- **Minimal OS Interface Specification:** A formal specification of the minimal OS interface Memar applications actually require (the boundary between "what the framework needs from a substrate" and "what a substrate provides") would be the natural follow-up to this RFC at the OS-design layer.
- **Terminology Governance RFC:** A dedicated RFC formalizing the word-weight rebalancing mechanism for AI model integration — specifying how RFC definitions are loaded as high-weight context, how ambiguities are detected and resolved, and how the mechanism is tested for consistency.
- **Memar Glossary:** A living glossary document that extracts all RFC-defined terms into a single reference, making it easier for both humans and AI models to access precise definitions without reading every RFC. The glossary would be auto-generated from RFC frontmatter and definition sections.
