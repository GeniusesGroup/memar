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
Document categories such as RFC, ADR, PRD, MRD, design documents, research papers, or concept documents are viewed as documentation profiles rather than fundamentally different documentation systems. Memar prefers a shared documentation foundation where the nature of the knowledge being documented determines the structure of the document, while specialized document profiles may impose additional conventions when needed. The goal is to maximize consistency, reduce fragmentation, and allow knowledge to evolve without unnecessary structural duplication.
