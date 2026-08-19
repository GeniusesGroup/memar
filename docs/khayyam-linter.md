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

## Boilerplate Generation
- **Getters & Setters:** To strictly enforce Information Hiding, capsules expose no data fields. The Linter MUST assist developers by automatically generating global `get` and `set` methods for internal fields when requested.


## Linters
- Linters MUST suggest naming e.g. in importing other packages, ...
- Linter MUST provide `Type` suggestion in developing of codes.
- Linter MUST help to generate some useful methods like getter and setter methods. For each structure field developer must define global get & set methods, otherwise compiler throw compile error if any read||write directly to fields be in codes.
