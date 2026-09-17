# Variable in Khayyam Changelog

## Changelog

### Initial creation and consolidation
- Time: 2026-07-15T00:00:00Z
- Type: Added
- Cited:
  - [Khayyam — Programming Language](./khayyam.md) — Reference: defines the canonical `vr` declaration syntax, `in` inclusion syntax, and logical-reference semantics elaborated here.
  - [Khayyam Design Philosophy](./khayyam-design_philosophy.md) — Reference: provides the self-documenting-code, syntactic-atomicity, and domain-modeling principles used to motivate the variable design. *(That document has since been fully retired and deleted; its content was absorbed into khayyam.md and khayyam-abstraction.md — see khayyam.changelog.md. This citation is preserved as historical provenance only.)*
  - [Type](../type.md) — Depends_on: variables name instances of types, and the type model determines which kinds of type may be referenced.
  - [Encapsulation in Khayyam](./encapsulation.md) — Reference: defines the capsule-owned behavioral contract, including the constant model and the rule that mutability is not a variable-level property.
  - [Abstraction in Khayyam](./abstraction.md) — Reference: defines the abstraction category that may be named in a variable declaration.
  - [Polymorphism in Khayyam](./polymorphism.md) — Reference: specifies dispatch for a variable declared against an abstraction.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed
  - [ChatGPT](../../CONTRIBUTORS.md#chatgpt) (GPT-5.5, medium effort) — reviewed
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM 5.2, high effort) — rewrote
  - [Claude](../../CONTRIBUTORS.md#claude) (claude-sonnet-5, extended thinking) — reviewed

#### What changed
- Created the variable document and consolidated the design's declaration syntax, explicit-type rule, assignment prohibition, logical-reference model, scope and inclusion mechanism, arithmetic treatment, constants, and deferred resource-lifecycle concerns.
- Scattered variable content was consolidated and the declaration, initialization, scope, and inclusion explanations expanded (Super Z).

#### Deliberation
- The original variable semantics were claimed — logical references, no assignment operators, and the rejection of privileged primitive types (Omid Hekayati).
- The initial design was critically reviewed (ChatGPT).
- The resulting document was critically reviewed (Claude).

---

### Migration to the current Explanation-facet structure
- Time: 2026-08-19T00:00:00Z
- Type: refactor
- Cited:
  - [Documentation — Explanation](../documentation-explanation.md) — Depends_on: defines the current required front matter, top-level body sections, topic-first organization, and progressive migration rules.
  - [Documentation — Changelog](../documentation-changelog.md) — Depends_on: defines the companion changelog that receives migrated provenance and change rationale.
  - [How to make a new explanation document](../documentation-explanation.practice.md) — Reference: supplies the revision procedure used for this migration.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested
  - [ChatGPT](../../CONTRIBUTORS.md#chatgpt) (GPT-5.6) — rewrote

#### What changed
- Migrated the base document from the retired `Summary` / `Guide-level explanation` / `Reference-level explanation` layout to `Abstract`, `Introduction`, `Explanation`, `Results`, and `Discussion`.
- Removed legacy `Citations`, `Contributor(s)`, and `Applied to` front-matter fields and the obsolete `Change Rationale` section; their historical information is preserved here.
- Existing explanatory topics and their detailed discussion were retained rather than condensed.
- This companion changelog was created.
- The stale `khayyam-type.md` link was corrected to `type.md`.
- The empty executable-documentation subtopic was replaced with its substantive explanation.

#### Deliberation
- Alignment with the latest documentation methodology was requested, without summarizing away existing content (Omid Hekayati — requested).

---

### Clarify aliasing scope and code-level vs. field-level variable
- Time: 2026-08-27T00:00:00Z
- Type: Fixed
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Super Z](../../CONTRIBUTORS.md#super-z) — rewrote

#### What changed
- Narrows the aliasing claim in `No Assignment Operators` from a broad “eliminates aliasing” to the specific sub-class that `b = a` would create; explicit reference sharing through method parameters remains the intended mechanism (e.g., passing the same `conn` to a registry).
- Adds a scope-clarification note to `Variable as Logical Reference` distinguishing a code-level `vr x W32` inside a method body from a field `Timeout Duration` inside a capsule — rebinding questions belong to the capsule level (field rebinding *is* mutation, gated by Sovereign Encapsulation), not to `vr` as such.

#### Deliberation
- The rebinding discussion was noted to belong at capsule level, not `vr` level, and to be a clarifying nudge only (Omid Hekayati — requested).

#### Considered and not done
- Alternatives for aliasing wording: (a) keep broad wording (rejected — misleading), (b) soften to “reduces” (rejected — elimination of `b = a` aliasing is total).
- For the scope note: (a) add a general rebinding rule at `vr` level (rejected per author preference), (b) add only a clarifying nudge distinguishing code-level vs. capsule-level variables (chosen).

---

### Second migration wave: `## Discussion` retired per the finalized method
- Time: 2026-09-08T00:00:00Z
- Type: refactor
- Propagates to:
  - khayyam-variable.handoff.md: Created - open questions and anticipated work moved there.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) - requested
  - [OpenCode](../../CONTRIBUTORS.md#opencode) (qwen3.8-flash) - moved

#### What changed
- The body's fixed top-level sections are now Abstract, Introduction, Explanation, Results only; the document-level `## Discussion` and all eight topic-level `#### Discussion` wrappers are dissolved.
- Drawbacks that are current-state cost claims about the design stand in the body, folded inline at the topics carrying the claims they qualify: Variable Declaration Syntax, Explicit Types, No Assignment Operators, Domain-Driven Arithmetic, Variable as Logical Reference, Variable Scope and Visibility, and Self-Documenting Code and No Magic Numbers.
- The document-level Naming Conventions block is a `Naming Conventions` subsection of the Self-Documenting Code and No Magic Numbers topic.
- The Introduction states that the document specifies the rules and explains their motivation; the record of alternatives considered and rejected lives here.
- Rejected alternatives and recorded decisions relocated to `Considered and not done` below; comparative prior-art surveys to `Related work`; open questions and anticipated work to the paired handoff. "None at this time"/"None recorded yet" placeholders carried no content. No claim was added, dropped, softened, or invented in the relocation.

#### Considered and not done
- **Multi-variable declaration syntax (the conventional approach in Go, C, and JavaScript; rejected; migrated from the Variable-Declaration-Syntax topic's retired Rationale and alternatives)**: compressing multiple distinct pieces of information (each variable's own name, type, and initial state) into a single line works against the language's broader preference for one explicit, visible step per statement. A reader can easily skim past one of several declared variables, especially when their types or initial values differ.
- **Inline initialization (e.g., `vr x W8 = 41`; rejected; migrated from the same topic)**: would reintroduce an assignment operator in a different form, conflicting with the language's decision to eliminate `=` entirely and to make all state changes explicit through capsule methods.
- **Full type inference (as in Haskell, Rust with `let`, Kotlin with `val`; rejected; migrated from the Explicit-Types topic's retired Rationale and alternatives)**: optimizes for the writer at the expense of every future reader, and undermines the self-documenting code principle that every variable's domain meaning should be visible at the declaration site.
- **Partial inference (infer only when "obvious"; considered, not chosen; migrated from the same topic)**: the boundary of "obvious" is subjective and creates inconsistency across a codebase — some variables will have explicit types and others won't, with no principled rule for which is which.
- **Linter-suggested, compiler-enforced (Khayyam's chosen approach; migrated from the same topic as the recorded decision)**: the compiler requires explicit types; the linter assists by suggesting the correct type during development. This gives the writer tooling support while preserving the reader's ability to see every type without inference.
- **Allow `=` for simple reassignment (rejected; migrated from the No-Assignment-Operators topic's retired Rationale and alternatives)**: would create a two-tier system where some state changes use `=` and others use methods, with no principled rule for which is which. It would also reintroduce the aliasing bugs that the elimination of `=` prevents.
- **Allow `=` but only for value types (considered, not chosen; migrated from the same topic)**: Khayyam has no value-type/reference-type distinction at the variable level — all variables are logical references — so this distinction cannot be cleanly drawn.
- **Built-in infix operators (the universal default; rejected; migrated from the Domain-Driven-Arithmetic topic's retired Rationale and alternatives)**: they structurally cannot express a failure path, which conflicts with Khayyam's broader principle that no control flow, including failure handling, should ever be hidden behind syntax (the same principle Khayyam Control Flow applies to branching).
- **Value semantics by default (as in C, Go; rejected; migrated from the Variable-as-Logical-Reference topic's retired Rationale and alternatives)**: would require implicit copies on every assignment or pass, introducing hidden memory allocation overhead and creating a performance model that depends on the compiler's copy-elision decisions.
- **Hybrid value/reference semantics (as in C++ with move semantics; rejected; migrated from the same topic)**: introduces a complex taxonomy (lvalue, rvalue, xvalue, prvalue, glvalue) that adds far more cognitive load than Khayyam's simple reference model.
- **Namespace-based imports (as in Python `from X import *`; rejected; migrated from the Variable-Scope-and-Visibility topic's retired Rationale and alternatives)**: hides which specific variables are used and creates namespace pollution, contradicting the explicitness principle.
- **Package-level imports (as in Java/C#; rejected; migrated from the same topic)**: introduces an abstract naming layer (package names) that is separate from the file system, creating a mapping problem between the import name and the physical file location.
- **Allow magic numbers with mandatory comments (rejected; migrated from the Self-Documenting-Code topic's retired Rationale and alternatives)**: comments can drift out of sync with the code, and a comment does not provide the compiler or linter with a name to enforce consistency across uses.
- **Linter rule rather than language-level constraint (considered, not chosen; migrated from the same topic)**: lint rules can be disabled or ignored at the organizational level, weakening the architectural safeguard.
- **Garbage collection (as in Go, Java; rejected; migrated from the Resource-Lifecycle (Deferred) topic's retired Rationale and alternatives)**: introduces unpredictable pause times and hidden runtime overhead, contradicting Khayyam's principle of making all behavior explicit and predictable.
- **Explicit resource management (Khayyam's intended approach; migrated from the same topic as the recorded decision)**: makes resource lifecycle a visible, predictable, and auditable part of the program's architecture. The precise mechanism is deferred to a future document.
- **GC-experienced developers will eventually need to engage with explicit resource management; the specifics of that engagement are not a variable-level concern (migrated from the Resource-Lifecycle (Deferred) topic's retired Drawbacks)**: kept here rather than folded into the body because it describes the adoption cost of a not-yet-specified future design, not a current-state cost of the variable model.
- **Combine declaration and initialization (rejected; migrated from the retired document-level Rationale and alternatives)**: would require an assignment operator, conflicting with the no-assignment rule and its aliasing-prevention benefits.
- **Allow type inference for "obvious" cases (rejected; migrated from the retired document-level Rationale and alternatives)**: the boundary of "obvious" is subjective and creates inconsistency; see [Explicit Types](./variable.md#explicit-types).
- **Allow multi-declaration for same-type variables (rejected; migrated from the retired document-level Rationale and alternatives)**: would compress distinct variables into a single line, violating the one-visible-step-per-statement principle; see [Variable Declaration Syntax](./variable.md#variable-declaration-syntax).
- **The variable model's insistence on explicit types, no assignment operators, and no multi-declaration syntax creates a measurably more verbose declaration experience than virtually every modern language (migrated from the retired document-level Drawbacks)**: for every variable, the developer must write a separate declaration line with an explicit type, and then a separate initialization line via a method call. This verbosity is the price of guaranteed readability and domain integrity — but it is a real price, and it is felt most acutely during rapid prototyping or when writing boilerplate-heavy code.

#### Related work
- Go, C, and JavaScript all support multi-variable declaration syntax as a convenience. Languages with a stricter "one binding per statement" discipline — idiomatic, non-compressed style in many functional languages — are closer in spirit to Khayyam's choice here. (Migrated from the Variable-Declaration-Syntax topic's retired Prior art)
- Go requires explicit types in `var` declarations but allows `:=` short declarations with inference. Rust allows `let` with optional type annotations. Haskell uses full Hindley-Milner inference. Khayyam's approach is closest to a strict explicit-typing discipline with linter assistance, similar to some enterprise Java style guides that mandate explicit generic type parameters even when they could be inferred. (Migrated from the Explicit-Types topic's retired Prior art)
- Most languages use `=` for assignment. Languages that restrict or eliminate assignment — such as pure functional languages (Haskell, Erlang) where all variables are single-assignment — are closer in spirit, though Khayyam's approach is less restrictive (mutation is possible through capsule methods) while still preventing implicit aliasing. (Migrated from the No-Assignment-Operators topic's retired Prior art)
- Domain-modeling-heavy codebases in many languages already wrap arithmetic in named methods for business types (e.g. `Money.add()` in DDD-style Java/C# code) as a best practice; Khayyam makes this the *only* available path rather than an optional convention. (Migrated from the Domain-Driven-Arithmetic topic's retired Prior art)
- Java's reference semantics for objects are superficially similar, but Java still uses assignment (`=`) and has a separate primitive type system that uses value semantics. Khayyam's model is more uniform: everything is a reference, and there are no primitives at the language level. (Migrated from the Variable-as-Logical-Reference topic's retired Prior art)
- Go's import model is the closest mainstream prior art, importing at the package level but requiring explicit use of the package name to access exported identifiers. Khayyam's model is more granular: each import targets a specific named variable from a specific file. (Migrated from the Variable-Scope-and-Visibility topic's retired Prior art)
- Domain-Driven Design as formulated by Eric Evans advocates for rich domain models and the elimination of "primitive obsession," but leaves enforcement to developer discipline. Khayyam encodes this discipline into the language grammar itself, making it structurally difficult to violate. (Migrated from the Self-Documenting-Code topic's retired Prior art)
- Rust's ownership model is the closest mainstream prior art in terms of explicit resource management. The specific approach Khayyam will take is not yet specified. (Migrated from the Resource-Lifecycle (Deferred) topic's retired Prior art)
- Rust's `let` with optional `mut` is the closest mainstream variable model, though it allows type inference and uses `=` for assignment. Go's `var` declaration with explicit type is syntactically similar to Khayyam's `vr`, but Go allows `:=` short declarations and assignment operators. (Migrated from the retired document-level Prior art)

---

### Resource Lifecycle retargets to the Memory protocol
- Time: 2026-09-15T13:00:00Z
- Type: Changed
- Cited:
  - [Memory](../protocols/memory.md) — Consumed contract: allocation, reclamation, teardown, allocators.
  - [Khayyam](./khayyam.md) — Realization: How Khayyam realizes Memory.
- Propagates to:
  - variable.handoff.md: Done — two resource-management open questions removed; the protocol and Khayyam topic are the homes.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Cursor](../../CONTRIBUTORS.md#cursor) (Composer) — applied

#### What changed
- Body pointers that deferred storage and lifecycle to a "future document on resource management" now point at [Memory](../protocols/memory.md) and [Khayyam → How Khayyam realizes Memory](./khayyam.md#how-khayyam-realizes-memory).
- The `Resource Lifecycle (Deferred)` heading loses the deferral; the topic states the governance/syntax split and links out.

#### Deliberation
- After the Khayyam-shelf memory-model document was retired into the Memory protocol, leaving a "future document" deferral would have been a dangling promise (Omid Hekayati — claimed).

---

### Review-round wording alternatives recorded as considered
- Time: 2026-09-16T00:00:00Z
- Type: Fixed
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided

#### What changed
- Recorded, from the audit of a now-pruned `chats-context` session file, three wording changes proposed for the Abstract/Overview during the vr-ab review round that were not adopted, so they are not silently re-argued: (1) weakening "creates a named reference to an instance of a type" to "establishes a named relationship with a type" pending the Type model's settlement; (2) replacing "reference" altogether — "a variable binds a name to a typed entity" — to avoid importing reference-semantics assumptions from mainstream languages; (3) removing the "provides access to the same instance" sentence as an identity/resource-model claim the variable document should not make.
- The body retains its original wording; the concern behind (3) is defused by the Resource Lifecycle retarget above, which assigns storage and copy semantics to the Memory protocol, while the instance-sharing statement remains a grammar-level fact about pass-by-reference.
