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
  - [Qwen](../../CONTRIBUTORS.md#qwen) (qwen3.8-flash via [OpenCode](../../CONTRIBUTORS.md#opencode)) - moved

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
  - [Mimo](../../CONTRIBUTORS.md#mimo) (mimo-v2.6-flash via [OpenCode](../../CONTRIBUTORS.md#opencode)) — applied

#### What changed
- The Abstraction Purity bullet now says Khayyam's abstractions are pure *behavioral specifications* — no logic, no state, no predefined method bodies — rather than pure contracts.

---

### Abstraction conformance no longer requires identical signatures
- Time: 2026-09-23T08:43:30Z
- Type: Fixed
- Cited:
  - [Abstraction in Khayyam](./abstraction.md) — Depends_on: Abstraction Realization already states exact influencing types, covariant influenced types, and a capsule receiver.
  - [Polymorphism in Khayyam](./polymorphism.md) — Reference: Covariant Return Types is the specification the influenced-type clause points at.
- Contributors:
  - [Grok](../../CONTRIBUTORS.md#grok) (Grok 4.7 via [Cursor](../../CONTRIBUTORS.md#cursor)) — reviewed, applied

#### What changed
- Compiler Rules → Abstraction Conformance Is Structural no longer says a capsule satisfies an abstraction only with identical signatures. Influencing-variable types must match exactly, influenced-variable types must match exactly or by covariant return, and the receiver is the implementing capsule.

---

### Orphan extension rule relocated to rules catalog
- Time: 2026-09-29T16:00:00Z
- Type: Changed
- Propagates to:
  - [orphan extension](../../bundles/khayyam/rules/orphan-extension/orphan-extension.md): Done
- Contributors:
  - Auto (model not recorded) via [Cursor](../../CONTRIBUTORS.md#cursor) - applied

#### What changed
- [What the Linter May Add → orphan extension](./inheritance.md#what-the-linter-may-add): monkey-patching governance text replaced with a link to [orphan extension](../../bundles/khayyam/rules/orphan-extension/orphan-extension.md).

---

### Abstraction scaffolding relocated from Linter Rules
- Time: 2026-09-29T20:30:00Z
- Type: Changed
- Propagates to:
  - [abstraction scaffolding](../../bundles/khayyam/rules/abstraction-scaffolding/abstraction-scaffolding.md): Done
- Contributors:
  - Auto (model not recorded) via [Cursor](../../CONTRIBUTORS.md#cursor) - applied

#### What changed
- [What the Linter May Add](./inheritance.md#what-the-linter-may-add): smart remediation and abstraction-scaffolding bullets replaced with a link to [abstraction scaffolding](../../bundles/khayyam/rules/abstraction-scaffolding/abstraction-scaffolding.md).

---

### Compiler and linter prescriptions removed from the inheritance document
- Time: 2026-10-03T11:16:28Z
- Type: Changed
- Propagates to:
  - [anti-lazy-inheritance rule](../../bundles/khayyam/rules/README.md): Pending - the linter check removed here is a governance rule of this repository; [rule.handoff.md](../rule.handoff.md) already records it as destined for that folder, and no agent owns that folder this session.
  - [abstraction scaffolding](../../bundles/khayyam/rules/abstraction-scaffolding/abstraction-scaffolding.md): Done - the remediation this document used to promise ("suggests the exact explicit delegation needed") is stated there. [see abstraction-scaffolding.md:23]
  - [Computer — Compiler](../modules/computer/compiler.md): Done - the optimization material removed from the document's last section is stated there as rationale, not obligation. [see compiler.md:54]
  - [rule.handoff.md](../rule.handoff.md): Pending - the table quotes this document's delegation rule as "the developer must explicitly define a method on the host capsule and transparently delegate"; that wording changed.
- Contributors:
  - [Space Bunny Alpha](../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../CONTRIBUTORS.md#opencode)) — applied

#### What changed
- The document's opening and Abstract no longer promise enforcement: "and how the compiler and linter enforce the separation" was removed from both, and "This document specifies the language-level consequences of that separation and how the compiler and linter enforce it" became "This document specifies the language-level consequences of that separation."
- [Motivation](./inheritance.md#motivation): the two compiler-analysis arguments were removed — "**Hidden Behavior Paths:** Behavior transfer creates methods in a capsule that are not defined in that capsule's source code. The compiler must traverse external sources to determine the full method set, complicating escape analysis and other static analyses." and "**Linear Escape Analysis:** Khayyam's compiler relies on perfectly linear escape analysis for memory optimization. Methods acquired from external sources that access parent state create non-local references that break this linearity." They were replaced by the model's own requirement: a method a capsule has but did not define is a method a reader of that capsule's source cannot account for.
- [No Method Promotion](./inheritance.md#no-method-promotion): the enforcement sentences became the model's meaning — "The compiler treats any attempt to call an embedded capsule's method directly on the host as an 'Undefined Method' error. The linter detects when a developer appears to be attempting to use method promotion and suggests the exact explicit delegation needed." became "Calling an embedded capsule's method directly on the host names a method the host does not define, and no declaration provides it."
- [Template Method and Other OO Patterns](./inheritance.md#template-method-and-other-oo-patterns): the three-step recipe was replaced by what the model has instead — "The alternative is to use **abstractions** and **explicit delegation**. Instead of a base class with a template method: 1. Define an abstraction that declares the customizable steps. 2. Have the 'template' capsule accept implementations of those steps via its fields. 3. The 'template' capsule explicitly calls the provided implementations." The topic now says no counterpart exists, that composition plus declared methods is the substitute, and that the substitute is more verbose and must be learned.
- [Compiler Rules](./inheritance.md#rules) (retitled from Compiler Rules, and [Linter Rules](./inheritance.md#what-the-linter-may-add) retitled to What the Linter May Add): the enforcement sentences were removed from the rules — "The compiler treats the inner capsule's methods as private to that capsule, even when accessed from the containing capsule's methods", "The compiler verifies that the delegation call exists in the host capsule's source code", "The compiler validates this during assignment or parameter passing where an abstraction type is expected. Missing or mismatched methods result in a strict compile-time error", and "This is enforced at the parser level." The rules remain as statements of what a program may contain. The linter section's check was removed — "**Anti-Lazy Inheritance Check:** The linter blocks any patterns or workarounds that attempt to create implicit method promotion hooks. If a developer writes code that appears to be attempting to use behavior transfer (e.g. embedding a capsule and then calling its methods as if they were native), the linter flags this." — and the section now says only that nothing in the document is a linter rule and points at the catalog.
- [Interaction with Smart Compilation](./inheritance.md): the whole section was removed — "Khayyam's compiler decides whether to handle abstractions at compile time (monomorphization, zero-cost abstraction when exact capsules are known) or at runtime (dynamic dispatch when underlying capsules are hidden). This decision is based on the dependency graph, not on any behavior transfer mechanism. Since there is no behavior transfer between capsules, the compiler never needs to resolve virtual dispatch tables through chains. [...] This simplification enables more aggressive compiler optimizations, including: **Perfectly linear escape analysis** [...] **Devirtualization** [...] **Inlining**". One sentence remains in the rules area: a method a capsule answers to is either defined in it or reached through a method it declares itself, and how each call is carried out is a compiler's business.

---

### Review of the uncommitted changes of 2026-10-12
- Time: 2026-10-12T09:50:00Z
- Type: Changed
- Contributors:
  - [Claude](../../CONTRIBUTORS.md#claude) (Sonnet-5.5) — reviewed, revised

#### What changed
- Restored the changelog entry "Repointed Explicit Behavior Ownership links after EBO absorption into type.md" (2026-08-30), which the working tree had deleted without a record; a changelog is history.
- In the 2026-10-03 entry, the "Propagates to" lines for abstraction scaffolding and Compiler said "Done" while the text said the material was "not yet stated" or had "no home yet"; both targets do state it (abstraction-scaffolding.md:23, compiler.md:54), so the text now says so.
- [Template Method and Other OO Patterns](./inheritance.md#template-method-and-other-oo-patterns): the claim that no construct "lets one type supply steps another assembles" contradicted the substitute stated in the next paragraph (a capsule composes supplied abstractions as fields); that clause was removed.
- Checked and kept: the removal of the compiler and linter prescriptions and the Interaction with Smart Compilation section (each quoted in the 2026-10-03 entry, with the material now in Compiler → What a Language's Discipline Gives and Costs and the rules catalog); the retitling to Rules and What the Linter May Add (the 2026-09-29 entries' anchors were repointed accordingly); the `modules/khayyam` to `bundles/khayyam` repoints.
