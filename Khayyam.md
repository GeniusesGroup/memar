# Khayyam - Programming Language
This language is ideal for developers that want a clean spoken code that can write most performance library and application with it.

## File extension
We choose .kh for files that have Khayyam language codes.

## Keywords

### Language Keyword in a glance
| Top level | types |
| :-------: | :---: |
|    tp     |  in   |
|    vr     |  cp   |
|           |  mt   |
|           |  ab   |
|           |  lb   |

### Top Level Keywords
Khayyam fundamentally relies on only three primary top-level concepts for declaration and importing: Types (`tp`), Variables (`vr`) and Labels(`lb`).

### Import Mechanism (`in`)
Khayyam treats the file system as the ultimate source of truth, avoiding abstract concepts like `namespace` or `package`. The `in` keyword is used as a routing operator to include entities from other files. 
Since capsules (`cp`), abstractions (`ab`), and methods (`mt`) are all fundamentally types, the import syntax remains strictly orthogonal:

In this manner devs force to write very short codes in each file to respect single responsible codes.

- **Type Inclusion:** `tp {name} in "{path}"`
  - *Example:* `tp TcpConn in "net/tcp"` (Imports a capsule, abstraction, or method type)
  - *Example:* `tp ErrServiceNotFound in "memar/process/services/errors/service-not-found.kh"` without need indicate a name to call them e.g. `fn example () () (err error) { err = ErrServiceNotFound }`
- **Variable Inclusion:** `vr {name} in "{path}"`
  - *Example:* `vr MaxTimeout in "net/config"` (Imports a specific variable, constant, or singleton)

### type
Type or data type is a subdivision of a particular kind of things. All things MUST define in below shape to understand by Khayyam compiler.
```khayyam
tp {name} [Type] [subtype defined value]
```

#### Capsule
Khayyam allow developers to indicate first level encapsulation-pattern by use `cp`.
  - `tp {name} cp { ___ }`
  - Capsule structure CAN include some other data types inside itself.
  - Each field in a capsule write by `fieldName fieldType` in each line.
  - Khayyam only allow access to inner data types via methods(functions). there is no data fields to expose.

#### Method
In Khayyam, functions and methods are not separate concepts; a method is fundamentally a callable capsule. By using the `mt` subtype, developers define an executable behavior and attach it to a receiver. The receiver is not limited to capsules (`cp`); a method can be attached to *any* type (`tp`), including an abstraction (`ab`) or even another method (`mt`).
- `tp {name} mt ({ReceiverType}) ({args}...) ({returns}...) { ___ }`
- Devs MUST separate `capsule`, `args` and `returns` by use `()` to indicate all of them even it is empty. We know that all of them is same in underlying layers and this rule is just to improve code readability.
- Devs CAN write pure standalone function in this way, there is no limitation.
- Dev can use any naming for capsule naming, BUT suggest use `self` as base point to other members in the capsule.
  - `tp Set mt (self Key) (key String) (err Error) {}`
- **Body-less Methods (FFI & Contracts):** A method can be defined without a body ({}). This is legally used in two scenarios:
  - Contract Definition: Defining the required signature for an abstraction (ab).
  - Foreign Function Interface (FFI): When the receiver is a concrete capsule (cp), a body-less method signals to the compiler that the implementation will be provided externally during the linking phase (e.g., from an Assembly .s or C .o file).

#### Abstraction
Abstractions in Khayyam are pure contracts. They do not contain logic, state, or even predefined method bodies. Unlike traditional interfaces, an abstraction is simply a named tag. The methods that fulfill this contract are defined entirely outside the abstraction.
- `tp {name} ab`
- Abstractions MUST use other abstractions as arguments or returns, not other `capsule`s.
- **No Generic Syntax:** We do not introduce syntax complexity for Polymorphism or Generics (like `<T>` in C# or `[T]` in Go). Khayyam inherently supports **Covariant Return Types**. If an abstraction dictates a method must return Abstraction `A`, a capsule can implement this method by returning Capsule `B` (as long as `B` implements `A`).
- **Smart Compilation:** The compiler decides smartly whether to handle these abstractions at compile-time (Monomorphization, zero-cost abstraction when exact capsules are known) or at runtime (via dynamic dispatch/interfaces when underlying capsules are hidden), entirely freeing the developer from generic syntax management.
- Khayyam treats abstraction as a pure contractual agreement, entirely avoiding generic syntax (e.g., `<T>`, `[T]`). We believe that explicitly defining type parameters in the syntax forces developers to expose implementation details, violating the core principle of Information Hiding.
  - **Contract-First Approach:** Abstractions in Khayyam represent behavior. If an abstraction requires an `Element`, it simply accepts `Element`. Any capsule that satisfies this interface is valid. 
  - **The Intelligence of the Compiler:** Instead of forcing developers to choose between compile-time and runtime polymorphism via syntax, the Khayyam compiler analyzes the codebase graph. It intelligently optimizes the implementation—applying monomorphization (compile-time) where specific types are known, or dynamic dispatch (runtime) where flexibility is required.
  - **Why this works:** Polymorphism is about **code reuse**, not about teaching the compiler how to do its job. By keeping syntax minimal, we allow the compiler to innovate in how it resolves these abstractions, keeping the source code clean and focused on domain logic rather than type-system boilerplate.
- Example:
  ```khayyam
    // Defining a pure abstraction
    tp Reader ab

    // The methods belonging to this abstraction are defined independently
    tp Read mt (self Reader) (data Element) (err Error)
    tp Close mt (self Reader) () (err Error)
  ```

#### Label
- `tp {name} lb { ___ }`
- Labels use in many logic methods like `IF`, `LOOP`, `GOTO`, ... that will develop in compiler library.
- labels MUST used just inside a method body.

### Variable
- `vr {name} {type}`
- Like other programming languages, `vr` keyword uses to store data in any mutable device. 
- Variables CAN declare in any encapsulation level as files and methods bodies.
- Compiler MUST inline variables as much as possible like immutable variables(constant in other language like Go).
