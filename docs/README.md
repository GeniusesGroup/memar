# Documentation (`/docs/`)
This directory contains the project's descriptive and explanatory documents. The primary purpose of these documents is to define, explain, clarify, and evolve knowledge about concepts, terminology, relationships, principles, rules, and architectural decisions.

These documents answer questions such as:
- What is this?
- What does it mean?
- Why is it modeled this way?
- How is it related to other concepts?
- What assumptions, constraints, or open questions exist?

---

## Why `docs`?
Several alternative names were considered, including:
- `concepts/`
- `knowledge/`
- `specifications/` (`specs/`)
- `references/`
- `descriptions/`
- `explanations/`
- `expositions/`

Each of them captures part of the intended purpose, but none captures it completely. For example:
- **knowledge** often refers to knowledge possessed by an individual rather than its documented representation.
- **concepts** focuses on concepts, while many documents describe relationships, principles, historical context, or architectural reasoning that extend beyond a single concept.
- **specifications** typically imply normative requirements ("what the system must do"), while many documents here are descriptive, analytical, or exploratory rather than prescriptive.
- **references** usually imply lookup material rather than conceptual explanation.
- **descriptions**, **explanations**, and **expositions** each emphasize a particular aspect of documentation but unnecessarily narrow the perceived scope.

Instead of selecting a more restrictive term, this project intentionally uses the familiar and broader name **`docs`**.

---

## Scope
Documents in this directory are primarily intended to explain and evolve understanding. The exact structure depends on the purpose of the document rather than a fixed document category. A document may contain:
- definitions
- explanations
- terminology
- rationale
- architectural reasoning
- principles
- relationships
- examples
- comparisons
- misconceptions
- references
- open questions
- migration notes
- normative specifications (when appropriate)

Design documents are not limited to any single component. A given design document may affect the language, the recommended framework library, linter/compiler behavior, OS-layer assumptions, or several of these at once; its scope is stated explicitly in its own content.

## Subdirectories

### Module specifications
The specifications of **Memar's modules** are not in this directory. A module is a bounded responsibility of the systems Memar builds, specified chiefly by its protocol, and each module's documents sit beside its code, in the layer above this one ([`modules/README.md`](../modules/README.md) gives the membership criterion, the shared layout, and where implementations live); this directory holds the conceptual foundation (System, Type, Process, Protocol, ...), which models general concepts: a concept document answers "what is X?", a module's document answers "what does *Memar's* module for X require?". A base document that needs only a concept's general meaning does not cite a module for it — an unreferenced term carries its general meaning per [Terminology → The Default Meaning of an Unreferenced Term](./terminology.md#the-default-meaning-of-an-unreferenced-term).

### `khayyam/`
The design and specification documents of the **Khayyam programming language** — the language designed within Memar's design space, whose local realization is hosted in this repository — the toolchain under `bundles/khayyam/` (`bundles/khayyam/khayyam.md`), the language's library sources, which sit with the modules they belong to ([`modules/` → Where implementations live](../modules/README.md#where-implementations-live)). These are base documents, beside the concept documents at this root: a document here answers "how does Khayyam realize X?", and its citations run down the layers of the written content as [Documentation → Citation Direction](../modules-plugable/knowledge/documentation/documentation.md#citation-direction) states. See [`khayyam/README.md`](./khayyam/README.md) for the membership criterion.

---

## Relationship to Practices
This project distinguishes between two fundamentally different kinds of documentation.

### `docs/`
Focuses on understanding. Its goal is to explain **what something is**, **why it exists**, and **how it fits into the overall model**.

### `agents/practices/`
Focuses on execution. Its goal is to describe **how to perform a task**, **how to apply knowledge**, or **how an agent should operate in practice**. Although both are documentation, they serve different purposes and should remain conceptually separate.

We just name `/practices/` to `skills/` to respect ecosystem word but in near future we will rename it to original name.

---

## Philosophy
Document categories such as [RFC — Request for Comments](https://en.wikipedia.org/wiki/Request_for_Comments), [ADR — Architecture decision record](https://en.wikipedia.org/wiki/Architectural_decision), PRD, MRD, design documents, research papers, or concept documents are viewed as documentation profiles rather than fundamentally different documentation systems. Memar prefers a shared documentation foundation where the nature of the knowledge being documented determines the structure of the document, while specialized document profiles may impose additional conventions when needed. The goal is to maximize consistency, reduce fragmentation, and allow knowledge to evolve without unnecessary structural duplication.

## Reading guidance
You do not need to read every document in full to answer a question. Start from a document's front matter (Title, Status, ID) and its Abstract to find what is relevant, then jump directly to the specific section you need inside that file. Every document follows the same section structure (Abstract → Introduction → Explanation), so you can navigate directly to the section that answers your question rather than reading end-to-end. A document's `Status` value tells you how far its content can be trusted as settled — the detailed status semantics are defined in [Explanation → Status](../modules-plugable/knowledge/documentation/explanation/explanation.md#status).
