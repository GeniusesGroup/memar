# Inheritance in Khayyam Changelog

## Changelog

### Created by splitting the Protocol document
- Time: 2026-07-10T00:00:00Z (approximated from Start Date; original drafting time not recorded)
- Type: Added
- Cited:
  - [Protocol](../protocol.md) — Depends_on: Protocol's definition as a pure declarative specification underpins how abstraction inclusion creates requirement-inheritance relationships between abstractions.
  - [Explicit Behavior Ownership](../type.md#explicit-behavior-ownership) — Depends_on: EBO is the principled foundation for rejecting behavior transfer between capsules; this document specifies its language-level consequences.
- Propagates to:
  - khayyam.md: Done — khayyam.md's abstraction/conformance framing reflects this document's placement model of inheritance.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed
  - [ChatGPT](../../CONTRIBUTORS.md#chatgpt) (GPT-5.5) — drafted
  - [Super Z](../../CONTRIBUTORS.md#super-z) — rewrote

#### What changed
- This document was created by splitting the original monolithic "Protocol" document into focused documents; the inheritance-related content was distributed between the Explicit Behavior Ownership document (principled foundation) and this document (language-level specification).
- The initial text of the original monolithic Protocol document was drafted; portions of its behavior-transfer and method-promotion analysis were incorporated here (ChatGPT — drafted).
- The document was retitled from "Rejection of Inheritance" to "Inheritance in Khayyam" and restructured, reframing the topic as placement rather than rejection (Super Z — rewrote).
- The subtyping section was added with Khayyam syntax (Super Z — rewrote).
- Terminology was unified with the EBO document (Super Z — rewrote).
- The Go embedding clarification ("Not All Embedding Is the Same") was extracted from working notes and integrated as a core argument.
- The meta-observation about what "inheritance" debates are really about was initially integrated here but subsequently moved to the Explicit Behavior Ownership document during terminology and content review — it is a general conceptual argument, not a language-specific design decision.
- The "Explicit Delegation Verification" and "Anti-Lazy Inheritance Check" sections of khayyam-linter.md provided the linter enforcement rules.
- The abstraction definition and conformance model of khayyam.md provided the context for how Khayyam handles capsule–abstraction relationships without behavior transfer.

#### Deliberation
- The core language design decisions were claimed (Omid Hekayati — claimed): placement of inheritance in the abstraction layer; rejection of behavior transfer between capsules.
- The document was originally titled "Rejection of Inheritance"; during review that framing proved misleading — Khayyam does not reject inheritance, it places it where it belongs (requirement extension between abstractions) while rejecting behavior transfer between capsules — so it was retitled and restructured accordingly.

### Migrated to Explanation-facet structure
- Time: 2026-08-26T00:00:00Z
- Type: refactor
- Cited:
  - [Documentation](../documentation.md) — Reference: facet meta-layer defining Explanation/Practice/Changelog and the cross-cutting URI and citation rules.
  - [Documentation — Explanation](../documentation-explanation.md) — Depends_on: governing structure the base document was migrated to.
  - [Documentation — Changelog](../documentation-changelog.md) — Depends_on: entry structure used for this companion file.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — migrated

#### What changed
- Structural migration only; no design decision changed.
- The base document was reorganized to the current Explanation-facet specification: fixed top-level sections (`Abstract`, `Introduction`, `Explanation`, `Results`, `Discussion`), topic-first organization under `Explanation`, and Discussion bundles attached to the topics they concern (the per-alternative arguments moved under Capsule Composition Without Method Promotion).
- Provenance previously carried in the base document's front matter (`Citations`, `Contributors`, `Applied to`) was relocated into this file's entries above.
- Two broken Explicit Behavior Ownership links in the old document (`./type.md#explicit-behavior-ownership` in Citations and `./explicit_behavior_ownership.md` in the Summary) were corrected to the actual file, `./type-explicit_behavior_ownership.md`; a duplicated-word typo in Unresolved questions was fixed.
- The former body `Change Rationale`/`Summary` historical narrative now lives in the "Created by splitting the Protocol document" entry above.

#### Deliberation
- Migration of this document to the current documentation method was requested (Omid Hekayati — requested).

### Added the minimal-independent-concepts design goal to Motivation
- Time: 2026-08-26T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Super Z](../../CONTRIBUTORS.md#super-z) — drafted

#### What changed
- "The Design Goal: Minimal Independent Concepts, Not Base Classes" was added at the top of Motivation, making explicit the positive principle behind the document's rules: Khayyam's type model targets the minimal set of independent concepts from which every other concept is derived by composition, not base-class hierarchies.

#### Deliberation
- Stating the compositional design goal explicitly was requested, after prior review had found the principle present only implicitly — framed as costs (No "Base Class" Convenience) and alternatives (Template Method) — never stated as the goal itself (Omid Hekayati — requested).

### Repointed Explicit Behavior Ownership links after EBO absorption into type.md
- Time: 2026-08-30T00:00:00Z
- Type: Fixed
- Contributors:
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — fixed

#### What changed
- The `type-explicit_behavior_ownership.md` file that three links targeted no longer exists: the standalone Explicit Behavior Ownership sub-document was absorbed into [Type](../type.md), where the principle now lives as its `Explicit Behavior Ownership` section.
- The three links (Summary and "Why Not Allow 'Safe' Behavior Transfer?" in the base document, and the Cited entry of the "Created by splitting the Protocol document" entry above) now point to `./type.md#explicit-behavior-ownership`.
- Link-target correction only; no text or design decision changed.

### Second migration wave: `## Discussion` retired per the finalized method
- Time: 2026-09-08T00:00:00Z
- Type: refactor
- Propagates to:
  - khayyam-inheritance.handoff.md: Created - open questions and anticipated work moved there.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) - requested
  - [OpenCode](../../CONTRIBUTORS.md#opencode) (qwen3.8-flash) - moved

#### What changed
- The base document's body now carries only the four fixed top-level sections: Abstract, Introduction, Explanation, Results; the document-level `## Discussion` and the topic-level Discussion wrapper under "Capsule Composition Without Method Promotion" are gone.
- The rejected alternatives from that topic wrapper (restricted "safe" behavior transfer, Go-style embedding, Rust-style default implementations) and the document-level rationale for rejecting behavior transfer between capsules are recorded under `Considered and not done` below.
- Of the document-level Drawbacks, the Template Method cost claim (the sanctioned alternative is more verbose and developers must learn it) was folded inline into the base document's "Template Method and Other OO Patterns" topic; the remaining three drawbacks are recorded under `Considered and not done` below.
- The comparative survey of Go, Rust, Java, C++, Swift, Kotlin, and Zig inheritance mechanisms is preserved under `Related work` below.
- The four unresolved questions moved to the paired handoff's `Open Questions`; the four future possibilities moved to its `Anticipated Work`.

#### Considered and not done
- **Allow restricted "safe" behavior transfer, e.g. single inheritance from abstract base classes only or bases without concrete methods (rejected; migrated from the retired Discussion wrapper under "Capsule Composition Without Method Promotion")**: even restricted behavior transfer creates conceptual dependency on the transfer model that influences how developers think about component relationships, and the "safe" boundaries are subjective and tend to erode over time as exceptions are added. The principled argument is made in the [Explicit Behavior Ownership](../type.md#explicit-behavior-ownership) document.
- **Go-style embedding (rejected; migrated from the same wrapper)**: often cited as a middle ground between behavior transfer and composition, providing method promotion without full class-based inheritance. Rejected because method promotion is still implicit behavior acquisition — the embedding component's source code does not show the promoted methods. The visibility problem remains, just in a milder form.
- **Rust-style traits with default implementations (rejected; migrated from the same wrapper)**: default implementations introduce the same ownership ambiguity the Explicit Behavior Ownership principle prohibits: a method exists in a type but the type's source code does not define it. The default method's implementation lives in the trait, creating dual ownership.
- **Behavior transfer between capsules (rejected; migrated from the retired document-level Rationale and alternatives)**: if Khayyam allowed it, every subsequent design decision would need to account for chains, method resolution order, and hidden behavior paths; the compiler would need to support virtual dispatch tables, the linter would need to trace hierarchies, and developers would mentally simulate chains to understand a capsule's full behavior. By establishing at the foundation that behavior transfer between capsules does not exist, all of this complexity is eliminated. The per-alternative arguments (restricted transfer, Go-style embedding, Rust-style defaults) are recorded directly above.
- **More explicit code (accepted cost, recorded as a drawback; migrated from the retired document-level Drawbacks)**: every behavior must be written explicitly, and for large component structures where many components share similar behavior this results in more source code. In the AI era, this is less a cost and more a structural advantage: AI-generated delegation code is cheap to produce, and the resulting explicit structure makes the codebase more legible to both human and AI participants. The source code is undeniably longer, but length is not the relevant metric — legibility is.
- **Design pattern migration burden on OO teams (drawback of the chosen position; migrated from the retired document-level Drawbacks)**: teams migrating from OO languages (Java, C#, C++) must reformulate behavior-transfer-based designs; this is not just a syntax change — it requires rethinking the architectural relationships between components.
- **No "base class" convenience (drawback of the chosen position; migrated from the retired document-level Drawbacks)**: common patterns like a `BaseService` class that provides shared infrastructure (logging, configuration, error handling) to all service subclasses do not translate directly; each service must explicitly compose its infrastructure.

#### Related work
- **Go Struct Embedding:** Go allows embedding structs and interfaces within other structs. Embedded struct methods are promoted to the outer struct. This is the most well-known "composition with promotion" mechanism. Khayyam rejects the promotion aspect while keeping the composition aspect (capsules can contain other capsules as fields). Go's interface-level embedding (interface inclusion) aligns with Khayyam's abstraction extension. (Migrated from the retired document-level Prior art)
- **Rust Traits:** Rust traits can have default method implementations and blanket implementations. Both introduce behavior without the implementing type's source code defining it. Khayyam rejects both, keeping traits (abstractions) as pure declarations. (Migrated from the retired document-level Prior art)
- **Java Class Inheritance:** Java supports single class inheritance with concrete method bodies and multi-interface implementation. Java 8+ added default interface methods. Khayyam rejects all forms of behavior transfer and default methods. Java's interface extension (without defaults) aligns with Khayyam's abstraction extension. (Migrated from the retired document-level Prior art)
- **C++ Multiple Inheritance:** C++ allows multiple inheritance with concrete method bodies, including the diamond problem. Khayyam's rejection of behavior transfer between capsules eliminates this class of problems entirely. (Migrated from the retired document-level Prior art)
- **Swift Protocols with Extensions:** Swift protocols can be extended with default implementations via protocol extensions. This allows behavior injection that is invisible at the conforming type's definition site. Khayyam rejects this pattern. (Migrated from the retired document-level Prior art)
- **Kotlin Open Classes:** Kotlin marks classes as `open` to allow inheritance, with `final` as the default. This is a more conservative approach than Java's, but still allows behavior transfer when opted in. Khayyam does not provide behavior transfer between capsules at all. (Migrated from the retired document-level Prior art)
- **Zig Comptime and Delegation:** Zig has no inheritance and relies on explicit composition and compile-time code generation. This aligns closely with Khayyam's approach and validates the feasibility of a behavior-transfer-free design in a systems programming language. (Migrated from the retired document-level Prior art)

---

### Abstraction purity restated as behavioral specification
- Time: 2026-09-23T05:38:39Z
- Type: Fixed
- Cited:
  - [Protocol](../protocol.md) — Depends_on: Protocol vs Contract.
  - [Abstraction in Khayyam](./abstraction.md) — Reference: pure-specification wording.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Mimo](../../CONTRIBUTORS.md#mimo) (mimo-v2.6-flash via OpenCode) — applied

#### What changed
- The Abstraction Purity bullet now says Khayyam's abstractions are pure *behavioral specifications* — no logic, no state, no predefined method bodies — rather than pure contracts.
