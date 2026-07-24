# Khayyam Linter & Tooling Rules

In Khayyam, the Linter is not just an optional code-quality tool; it is a fundamental pillar of the language's architecture. Khayyam intentionally keeps its core syntax minimal and shifts the burden of enforcing safety, memory rules, and clean architecture directly onto the Linter and IDE tooling.

## IDE Behavior & Visual Formatting
- **Auto-Folding:** To manage inclusion bloat and improve readability, IDEs MUST automatically fold continuous blocks of `tp ... in ...` and `vr ... in ...` declarations at the top of files.
- **Structural Overview:** By default, IDEs SHOULD fold all capsule and method bodies (`{}`) when a file is first opened. This forces the reader to see the high-level architecture and contracts before diving into the implementation details.

## Cross-file Methods - The Orphan Rule (Monkey Patching Prevention)
Since Khayyam does not use explicit `package` boundaries, large capsules or logic blocks can be naturally split across multiple files within a directory. To achieve this, a type can be imported (`in`) into a new file, and new methods (`mt`) can be attached to it there.

Since Khayyam relies entirely on the file system for modularity (without `package` keywords), capsules can be legally split across multiple files in the same directory. Syntactically, Khayyam allows you to attach a method to any imported type. This provides the freedom to split implementations across multiple files cleanly. However, to prevent unintended mutations of third-party libraries (Monkey Patching), Khayyam relies on its strict Linter. 

The Linter differentiates between extending a *local directory type* (which is fully permitted for file-splitting) and mutating a *distant/external library type* (which will trigger a strict warning or error by default). This design keeps the core syntax simple while allowing organizations to customize strictness via Linter rules.

- **The Rule:** The Linter MUST strongly warn or throw an error if a developer attempts to attach a new method (`mt`) to a type (`tp`) that was imported from an external library or a different domain directory.
- **Why:** This prevents unpredictable "Monkey Patching" and mutation of third-party behavior. If external extension is needed, the developer must use Composition (wrapping the external capsule in a local one).

## Memory Safety Guardian
Khayyam does not use a built-in heavy Garbage Collector or complex Borrow Checking syntax.
- **Execution Path Analysis:** If a capsule acquires memory via an allocator or requires explicit teardown, the Linter MUST perform static analysis to ensure that the `Deinit()` or `Free()` method is called in all possible execution exit paths before the capsule logically dies.
- **Zero Syntax Cost:** This guarantees memory safety at development time without polluting the language syntax with lifetime annotations.

## Type Strictness & Inference
- **No Type Inference:** The compiler does not infer types. The Linter MUST assist the developer during the coding phase by suggesting the correct types based on the assigned capsules, ensuring the final written code is explicit and readable.
- **Immutable by Default:** Variables MUST be treated as immutable by default after initialization. The Linter should warn against direct mutations unless explicit cloning or copying methods are used.

- Khayyam explicitly does NOT support automatic type inference at the compiler level. 
- While implementing type inference is technically trivial, it introduces "magic" into the codebase. It slightly speeds up the writing process for the author but significantly increases the cognitive load for the reader. 
- In Khayyam, code readability is paramount. Developers must declare explicit types. Linters will heavily assist developers during the writing phase, ensuring the final code is crystal clear, explicitly typed, and requires minimal mental processing for future maintainers.
- 
- Taken from other rules of language, it is clear that developers can't assign to var before decare it.
- e.g.
```go
// Other languages
var x = 41
var y = 3.14
```
```khayyam
// Khayyam way
vr x W8 // whole 8 bit
x.FromString ("41")

vr y R32 // rational 32bit
y.FromString ("3.14")
```

## Boilerplate Generation
- **Getters & Setters:** To strictly enforce Information Hiding, capsules expose no data fields. The Linter MUST assist developers by automatically generating global `get` and `set` methods for internal fields when requested.


## Linters
- Linters MUST suggest naming e.g. in importing other packages, ...
- Linter MUST provide `Type` suggestion in developing of codes.
- Variables MUST treat immutable by default after initialization, unless Developer indicate it by some specific method. If need to change the capsule data, need to copy desire data to new variables.
- Linter MUST help to generate some useful methods like getter and setter methods. For each structure field developer must define global get & set methods, otherwise compiler throw compile error if any read||write directly to fields be in codes.

## Abstraction Validation and DX Scaffolding
Since the language syntax avoids explicit implementation keywords, the Linter is responsible for assisting the developer and ensuring architectural compliance:
- **Scaffolding**: When a developer intends to implement an abstraction (detected via context or explicit linter hints), the Linter provides automated code generation to scaffold all missing method signatures with empty bodies.
- **Proactive Warnings**: The Linter analyzes the codebase and issues warnings if a capsule partially implements an abstraction's method set in a context where it is clearly expected to satisfy that abstraction, preventing unexpected compilation failures.

## Explicit Delegation Verification
Khayyam enforces explicit delegation to eliminate lazy programming patterns and ensure 100% human readability. The Linter blocks implicit or magical method promotion hooks and provides smart remediation when a developer attempts to call an embedded capsule's method on the host.

> For the full specification — including anti-lazy inheritance checks, smart remediation behavior, scaffolding details, and the orphan rule — see **[RFC 495467 — Khayyam Rejection of Inheritance](./khayyam-rejection_of_inheritance.md)**.