# Khayyam Rationale & Design Decisions
This document explores the foundational philosophy of Khayyam. It outlines the rationale behind the language's unique architecture, explains why many common features from other languages were explicitly rejected, and addresses edge-case scenarios for compiler developers and software architects.

## Not Implemented Features! (Rejected Designs)
In this part, we say why not choose something that be real in some other programming languages.
*Note: This section describes a design that was explicitly REJECTED in Khayyam to maintain language orthogonality and prevent syntax clutter. It remains here to answer common architectural design questions.*

### Framework
Khayyam is designed purely as a core programming language, but it acts as a tool within a broader development philosophy. 

We strictly avoid terms like "Standard Library" or "Official Library," as they imply a rigid, unchangeable set of forced tools. Instead, Khayyam is introduced alongside a **Recommended Framework**.
- **Separation of Concerns:** Architectural concepts, such as memory allocators or logical object lifecycles (e.g., `Init` and `Deinit` contracts), belong to the framework, not the language syntax. The language itself remains entirely independent and agnostic of these implementations.
- **Flexibility with Caution:** Developers are free to swap, modify, or rewrite parts of the recommended framework to suit highly specialized needs. However, this is highly discouraged for general use cases. Replacing framework components requires a profound understanding of Khayyam's core design principles, as the recommended framework is heavily optimized to work seamlessly with the language's zero-magic, explicit nature.

### Library-Driven Control Flow (Why Conditional Keywords Were Rejected)

In traditional languages, conditional statements like `if`, `else if`, and `else` are hardcoded into the compiler's core syntax and Abstract Syntax Tree (AST). Khayyam explicitly rejects this design to maintain strict language orthogonality and prevent syntax bloating.

#### The Problem with Built-in Conditionals
1. **Semantic Contradiction with Multi-Return Methods:** In Khayyam, methods return values through explicit output variables on separate lines. Forcing a method invocation inside a traditional conditional block (e.g., `if (method())`) creates immense parsing ambiguity and forces the compiler to establish complex, arbitrary evaluation rules.
2. **AST Complexity:** Built-in conditionals complicate the compiler's syntax analyzer, turning control flow into a magical entity distinct from standard type evaluations.

#### The Khayyam Architectural Solution
In Khayyam, control flow is entirely decoupled from the language syntax. There are no built-in logical keywords except the bare-metal `goto` instruction. Conditionals are implemented as standard, framework-level abstraction types (`tp`) that interact with the compiler to conditionally execute a specific code scope.

To use conditional structures, a developer simply includes them directly from the framework's logic layer, treating them exactly like any other component:

```khayyam
tp IF in "khayyam/compiler/logic/if.kh"
tp ELSE in "khayyam/compiler/logic/else.kh"

vr isValid Status
validator.Check(data)(isValid)

IF(isValid) {
    // Code scope to execute if true
}
ELSE(isValid) {
    // Code scope to execute if false
}
```

### Package (Packaging)
Khayyam explicitly removes the concept of package-level encapsulation or global namespaces. We believe that relying on packages often leads to lazy naming conventions (e.g., naming a method `Parent()` simply because it resides in an `ast` package) and eventually causes naming collisions.

Instead, Khayyam enforces **Domain-Driven Naming** and **Consumer-Driven Inclusion**:
- **Explicit Naming:** Developers must write clear, self-explanatory names for capsules and methods. For example, `Parent() T` is an ambiguous name; Khayyam encourages explicit names like `ParentCommand() Command` or `ParentElement() Element`. This makes the code highly readable without needing a package prefix.
- **Consumer-Driven Inclusion:** Producers (library authors) do not define package names. Instead, the consumer includes the file and assigns it a local capsule name using the `in` keyword. 
  - Example: `tp JsonEncoder in "memar/codec/data_exchange/json/encode.kh"`.
  - By doing this, the consumer fully controls the local scope. This fundamentally eliminates global naming collisions, as there is no central package registry to conflict with.

So Khayyam don't allow developers to *imports* other files as top level encapsulation-pattern. Anyway if khayyam want to provide import:
  - Consumers will set name for the `file` that import, IN this style, producers don't need to indicate or naming in producing side.
  - Khayyam use `tp {name} im {addr}` keyword e.g. `tp jsonEncode im "memar/codec/data_exchange/json/encode.kh"` to import other code file to local one. import desire file and use needed logic by this way e.g. `jsonEncode.Encoder`

### Function
Function can't imagine as independent blocks of code. It is a capsule and need to provide more methods about its behavior. Many languages need to provide their other usages such as authorization to access the function as top level keyword such as `private`, `public`,... But Khayyam don't introduce many top level keyword for this type of requirements, Due to we believe this requirements CAN change in near future and this abstraction CAN easily implement by methods for any capsule. So a function is a capsule with many methods to introduce itself.   
Khayyam don't allow developers to indicate functions by use any keywords like `fn` or `func`, ... as `tp {name} fn (args) (returns)`. Khayyam still support pure standalone function and MUST not assume in wrong way. It can be assumed that functions are methods for the file level encapsulation and Khayyam not support this style.
We suggest use `Do` method name for a capsule to doing its logic like a simple function call 
```khayyam
// when is a helper function for setting the 'when' field of a Timer.
// It returns what the time will be, in nanoseconds, Duration d in the future.
tp Do mt (wh WhenHelper) (d duration.NanoSecond) (t monotonic.Time) {}

// use in this manner:::
vr t1 monotonic.Time
WhenHelper.Do (d) (t1)
```

### Constant
- [Constant](https://en.wikipedia.org/wiki/Constant_(computer_programming)) is a `variable` that return by a `capsule` `method` that can't change after first initialization. So it is an organization rule not compiler one. e.g. a `config` capsule for a module that expose module variables, this config capsule may provide some method to change some of its variables.
- We have 2 types of constant:
  - Static constants as compile time declaration and initialization that usually inline in compile time
  - Dynamically-valued constants as compile time declaration and runtime initialization that can't inline in compile time and need memory service call to get its value.
- Constants can assume as functions that run in compile time! so write functions that return desire variable that live in that function body!
- Dev can change variables in runtime. `compiler` CAN force `Runtime` to change binary codes and don't need to get it by memory call. Compiler and runtime just let to change the value with the same memory size. (Really decide to provide this??)

### Operators
Khayyam intentionally does not provide mathematical or logical operators (like `+`, `-`, `==`, `*`). 

In computer science, operations are physical processes bound by hardware limitations, not abstract infallible mathematical concepts. A simple addition or division can fail (e.g., integer overflow, division by zero). Traditional mathematical syntax (`c = a + b`) leaves no room to return an error, forcing languages to invent dangerous workarounds like hidden `panic`s, exceptions, or silent overflows.

Since Khayyam has no primitive types, all operations are explicit methods on a capsule. This forces the developer to acknowledge and handle potential runtime errors transparently.
- Example: Instead of `c = a + b`, developers use explicit methods like `a.Add(b)(c, err)`, ensuring no error is ever hidden behind syntactic sugar.

### Complex Expressions and Formulas
Without built-in operators, developers might wonder how to implement complex mathematical or scientific formulas. Khayyam resolves this by keeping the core language minimal and delegating domain-specific logic to libraries. 

Instead of writing verbose nested method calls for complex math, developers can pass mathematical expressions as strings to specialized capsules (e.g., passing "x = (-b + sqrt(b^2 - 4ac)) / 2a" to a `MathEval.FromString()` method). The capsule's internal logic, potentially aided by AI-driven code generation or runtime AST evaluation, handles the parsing and execution. This fluid approach ensures the language remains free of strict syntactic assumptions while offering limitless flexibility for domain-specific needs.

### Decorators
As describe [decorators in TS](https://www.typescriptlang.org/docs/handbook/decorators.html) or [python decorators](https://www.w3schools.com/python/python_decorators.asp) or [Java decorators](https://docs.oracle.com/javaee/7/api/javax/decorator/package-summary.html), It is just a `initialize` process that we don't want to have magic and not support this feature.

### Abstraction and Polymorphism
Khayyam promotes simplicity by avoiding syntactic overhead for polymorphism. We believe that generic syntax (e.g., `[T]`, `<T>`) introduces unnecessary complexity that hinders readability and limits compiler creativity.

- **Unified Abstraction (No Overloading/Generics):** - Khayyam does not support method overloading. A method name must represent a single, clear, and unambiguous intent.
  - We do not use dedicated generic syntax. Instead, we rely on **Interface-based Polymorphism**. If a method requires an abstraction, developers must refer to that abstraction directly (e.g., `Index(el Element)` rather than `Index[T](el T)`).

- **Compiler-Driven Implementation:**
  - Developers define "what" the requirement is through abstractions. The "how" (implementation strategy) is the sole responsibility of the Khayyam compiler.
  - Whether a piece of code is handled at **Compile-Time** (e.g., through monomorphization/inlining for performance) or at **Run-Time** (e.g., through dynamic dispatch/vtable for flexibility) is determined automatically by the compiler based on the code context. This maintains the clean, "spoken-like" syntax while ensuring maximum performance without burdening the developer.

### Containers and Type Safety (Without Generics)
Developers coming from other languages might wonder how Khayyam ensures Type Safety in data structures (like Lists or Maps) without generic syntax like `List<T>`. The answer lies in Khayyam's lack of primitive types and its strict reliance on encapsulation.

- **Domain-Specific Containers:** In Khayyam, raw Abstract Data Types (ADTs) are not meant to be exposed directly to high-level application logic. Instead, developers (or code generators/AI) create intermediate domain-specific capsules. For example, instead of a generic `List<Connection>`, you define a `ConnectionList` capsule.
- **Method-Level Safety:** The `ConnectionList` capsule internally manages the raw ADT but its public methods strictly accept and return only `Connection` capsules.
- **Linter and Explicit Typing:** Because Khayyam does not support automatic type inference (variables must be explicitly typed) and relies heavily on strict Linters, passing the wrong capsule type to `ConnectionList.Add()` will immediately trigger a linting error during development. 

This architectural choice completely eliminates the need for generic collections at the syntax level, shifting the responsibility to highly readable, domain-specific intermediate layers.

### Rich Domain Models vs. Generic Containers
By eliminating generic syntax (like `List<T>`), Khayyam intentionally prevents the creation of "Anemic Domain Models"—dumb data structures stripped of business rules.

When developers use generic collections in other languages, they often place critical domain logic (e.g., "do not allow duplicate Service IDs in this list") in disconnected layers like controllers or random services, leading to unmaintainable spaghetti code. 
In Khayyam, because you must create an intermediate domain-specific capsule (e.g., `ServiceRegistry` instead of `Map<ID, Service>`), you are naturally guided to place that specific business logic exactly where it belongs: inside the capsule's methods (e.g., `ServiceRegistry.Register()`). The "cost" of writing this intermediate capsule is actually a fundamental investment in Clean Architecture and robust domain modeling.

Furthermore, the base Abstract Data Types (like a raw Hash Map) act merely as "Hosts". They do not need generic syntax to know the exact identity of their "Guests" (`Elements`). The guest capsule maintains its own identity and memory management rules (e.g., acting as a pointer), and the host simply accommodates it without needing syntax-level type awareness.

### Methods Overloading
It seems we need this feature if we want to have very simple [generic](https://en.wikipedia.org/wiki/Generic_programming) and polymorphism.   
Due to Khayyam not support primitive types, All disadvantages disappear and JUST advantages will shine.

### Method overriding
Method overloading is a compile-time polymorphism. Method overriding is a run-time polymorphism. CAN provide runtime feature when not provide rich runtime??

### Memory management - GC (Garbage Collection)
Libraries must provide memory management and data types (almost always ADT's decide) decide to choose and use desire memory management for its usage.

### Memory Management and Allocation
The term "Garbage Collection" (GC) has been incorrectly monopolized by heavy runtime tracing algorithms (like in Go or Java). In reality, any system that requests chunks of memory from the OS and distributes them to objects is performing memory management.

- **Pluggable Allocators:** Khayyam does not force a universal, monolithic memory runtime. Memory allocation is treated simply as an independent library. Developers choose or write their own memory allocators (e.g., Arena, Object Pools) based on their specific application profile.
- **Linters as the Guardian (The true place of Borrow Checking):** Concepts like memory safety, preventing data races, and use-after-free are fundamentally static analysis concerns, not syntax elements. Instead of polluting the language syntax with complex lifetime annotations (as seen in languages with strict borrow checkers), Khayyam relies on powerful, strict Linters. The Linter enforces correct variable usage and safe memory access patterns during development, ensuring safety without adding cognitive load to the code's visual structure.
- **Explicit over Magic:** If a specific memory management model requires particular methods to track memory (e.g., incrementing/decrementing reference counts), Khayyam encourages using explicit code generation (e.g., generating `file_name.generated_by_gc1.kh` files) rather than hiding the logic behind syntax-level magic or borrow checkers.

### Tuples
Tuples are implemented by two dynamic and static type languages.
- In a dynamic language, tuples implement unsafe structures that allocate by the runtime and have a performance penalty for the app because we use runtime for developing or compiling phase.
- In a static language, tuples implement safe structures that just don't have internal names. But it is duplicate work, more learning curve and adds more confusing situation just lazy developer to not indicate names.

### Iteration - Loop
We think loop can implement easily by `goto` instead of `while`, `for`, `do`, ... if and just if `Iterator` interface not implement by desire type. But strongly suggest iteration MUST implement by just `Container` ADT.

### Dependency Management
We don't offer any version control for your codes, So we must not offer any dependency management too.

### Multiple declarations
- Devs can't declare multiple variables in one line using a comma-separated list
- Devs can't declare multiple types in one block by using a `{}` list
- Devs can't declare multiple in one line using a `;` as say in `Commands Break` part

## Inspired of
### Languages
These languages inspirations don't mean just about get good idea but mean drop bad idea from these and not implement them.
- [C](https://en.wikipedia.org/wiki/C_(programming_language))
- [D](https://dlang.org)
- [Go](https://golang.org/)
- [Rust](https://www.rust-lang.org/)
- [Spiral](https://github.com/mrakgr/The-Spiral-Language)

### Articles
- https://pingcap.com/blog/early-impressions-of-go-from-a-rust-programmer/
- http://www.linux-kongress.org/2009/slides/compiler_survey_felix_von_leitner.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.143.4688

## Khayyam word meaning
[Omar Khayyam](https://en.wikipedia.org/wiki/Omar_Khayyam) was a Persian mathematician, astronomer, philosopher, and poet.
