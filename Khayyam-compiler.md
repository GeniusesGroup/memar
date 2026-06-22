# Khayyam Compiler Directives

This document outlines the strict behavioral rules and responsibilities of the Khayyam Compiler. The compiler's primary job is to translate explicit, domain-driven code into highly optimized machine instructions without relying on hidden runtime magic.

## Control Flow via Framework Intrinsics
Khayyam's AST does not natively recognize high-level conditional logic like `if`, `else if`, or `else`. 
- **The `goto` Core:** The only native branching keyword in Khayyam is `goto`.
- **Lowering Logic:** The compiler treats conditionals (imported from the framework) as compiler intrinsics. It evaluates the boolean state of the explicitly provided variable and translates the framework's `IF` method directly into optimized `goto` jumps at compile time.

### GOTO
- `goto(LocationLabel)` is a compiler method.
- **GOTO**: GOTO use to fly to desire location in a process. Some known labels:
  - loop: find loop by `{}`
  - end: find by `{}`
  - next: it is like `continue` in `switch` in other languages.
  - return
      - Just use to indicate return in body of a function.
      - Not need to indicate on end of any functions.
      - It is pure keyword and must end with [commands break](#Commands_Break) style so dev can't use like "return 0".
      - 
- **Commands Break**: each command must end with new line

## Smart Compilation of Abstractions
Khayyam avoids explicit generic syntax (like `<T>`). Abstractions are pure contracts.
- **Graph Analysis:** The compiler MUST analyze the dependency graph to determine the implementation strategy for an abstraction.
- **Compile-Time (Monomorphization):** If the exact underlying capsule satisfying the abstraction is known at compile time, the compiler MUST inline the code, resulting in zero-cost abstraction.
- **Run-Time (Dynamic Dispatch):** If the capsule is hidden or determined dynamically, the compiler automatically implements a VTable/Interface mechanism for runtime resolution.

## Environment-Agnostic Entry Points
Khayyam does not enforce any syntax-level entry point or lifecycle functions such as `main`, `init`, or `deinit`.

Hardcoding an execution model into the language syntax restricts its adaptability for different environments (e.g., event-driven architectures, serverless, or WASM) and forces future breaking changes if the execution paradigm evolves. 
Instead, defining how a program boots or tears down is the strict responsibility of the `compiler` and `runtime` libraries. These libraries can introduce their own conventions, ensuring the core Khayyam language remains completely environment-agnostic and future-proof.

- **Delegation:** The compiler and the selected runtime framework are entirely responsible for defining how a program boots. 
- **Adaptability:** This allows the compiler to easily target different environments (e.g., WASM, Serverless, embedded systems) by simply changing the compiler configuration, without breaking language compatibility.

## Compile-Time Functions
- Methods that calculate configurations, constants, or pure logic that do not depend on runtime state MUST be evaluated by the compiler during the compilation phase. The compiler replaces these method calls with constant capsules in the final binary.
- Below function MUST compute in compile time not runtime. Any use of CNF_KeepAlive_Idle return variable is just a simple constant capsule.
```Khayyam
tp CNF_KeepAlive_Idle mt (self Config) () (dur duration.NanoSecond) {
    dur.FromASCII("7200")
    dur.Multiplication(duration.NanoSecondInSecond)
}

tp closeIdleSocket mt (tcpSock TCPSock) (st NetSocket) (err Error) {
    // some logic ...
    // vr passIdle bool
    tcpSock.checkIdlePass (Config.CNF_KeepAlive_Idle()) (passIdle)
    // some logic ...
}
```

## FFI & External Linking
- **Body-less Concrete Methods:** If the compiler encounters a method without a body (`{}`) attached to a concrete capsule (`cp`), it MUST NOT throw a syntax error. Instead, it must treat this as a Foreign Function Interface (FFI) declaration and expect the implementation to be provided during the linking phase (e.g., via `.s` or `.o` files).

## Compiler library
- Compiler provide `compiler` library that developers can use in coding and let compiler know that must decide.
```khayyam
tp Set mt (self Key) (key STR) () {
	if key.CharacterEncoding().IsEqual(asciiCharacterEncoding) {
		compiler.Log.Fatal("Linter MUST notify developers not call this method with string other than ASCII")
	}
	self.CopyFrom(key)
}
```
- The function body can omit in write code and add by compiler plugins as know code generation.
- Public of the first-class keyword indicates by a capital letter of identifier word and vice versa. Khayyam doesn't offer any specific keyword for this purpose like Go language.

## Inline Function
- Inline function return const as declare const globally. Below codes are same when compile them.

## Runtime
- We need to offer very simple but with some unique logic

### Change logic in runtime
You can write code to change(add or remove) modules binary code in runtime. It is like `WASM` idea. It can be very dangerous feature and MUST tag as `unsafe`. It is useful to add or remove modules in microservice way but as describe by [this paper from google expert software developers](https://dl.acm.org/doi/pdf/10.1145/3593856.3595909)
