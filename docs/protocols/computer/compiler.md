---
Title: "Compiler"
Status: Draft
Start Date: 2026-06-22
ID: 495024
---

# Compiler

## Abstract
A **compiler** is a system that consumes a language's specification and produces a target representation of a well-formed program. It is not identified with any one language, and it is not identified with any one target — native machine code, JavaScript, WebAssembly, and further backends are equally legitimate products of the same concept. The compiler is a separate system from the language it consumes: it is not part of what that language *is*. This document is Memar's protocol for that system: what a compiler may recognize (the language's own primitives, never a library's names as intrinsics), that it emits analysis events rather than special-casing libraries, that entry and lifecycle are configuration plus [Runtime](./runtime.md) libraries rather than grammar, that designated pure operations may be evaluated at compile time without privileging types, and that it consumes the [Lexer](./lexer.md) under that protocol's contract. A Khayyam-to-JavaScript compiler and a C compiler that honors the same rules are two realizations, not two concepts.

## Introduction

### Motivation
Once a language project owns compiler implementation, every convenience request becomes pressure to add syntax, special cases, or built-in magic — because the team that controls the language spec is the same team that feels the pain of not having the convenience. The failure is documented across language projects; [Khayyam Is Not Its Own Compiler or Runtime](../khayyam/khayyam.md#khayyam-is-not-its-own-compiler-or-runtime) records it for one language. This protocol states the same boundary as a contract any compiler realization must satisfy, so the safeguard does not have to be re-derived per language.

The second failure is identifying "compiler" with "Khayyam to machine code." A compiler that lowers Khayyam to JavaScript, or that lowers C to an intermediate representation, is still a compiler. If the protocol is shaped by one language and one target, every later backend has to fight the definition.

The third failure is the compiler quietly adopting protocol semantics by recognizing a library by name — treating a framework's `IF` as an intrinsic, a numeric type as a builtin, a `main` as grammar. Each shortcut reintroduces magic the language's specification refused.

### Methodology
The positions below were first exercised as directives to a Khayyam compiler, then lifted: what survives without naming that language's constructs is the protocol; what names those constructs is a realization fact and lives in [Khayyam](../khayyam/khayyam.md). The Lexer was split out of the same discussion into its own protocol because a lexer serves many consumers, of which a compiler is only one. Compile-time evaluation is stated as a designation-and-purity rule, not as a catalogue of privileged types; C's `const` folding and similar toolchain features are evidence the requirement is not language-unique. Directives are currently enforced by review against this document — there is no conformance suite yet.

## Explanation

### What a compiler is
A compiler is a system whose process is compilation: given a source and a language specification, it accepts or refuses the source as a program of that language, and, on acceptance, produces a target representation. The language specification is an input, not a component of the compiler. The target is an output chosen by configuration — it is not part of the compiler's definition. Multiple compilers may consume one language; one compiler may produce several targets behind one semantic representation. The semantic representation, not any one backend, is the source of truth both targets realize.

A compiler is not the language. Folding compiler implementation into the language's own scope is the failure mode the Motivation names.

### The compiler recognizes language primitives, not library names
The compiler's front end accepts the constructs the language specification actually defines. It does not treat library-provided operations as intrinsics because they are common, useful, or imported from a privileged package. Framework control-flow methods, numeric helpers, and lifecycle hooks are ordinary library code. Special-casing any of them by name couples the compiler to one library and forces every other library through that one library's shape.

What a given language's primitives *are* is stated in that language's documents. For Khayyam, the grammar's control-flow primitive is the inert code scope `sc`, and the compiler of a Khayyam realization lowers scope-driven branches to internal jumps without a `goto` keyword in source — see [Khayyam](../khayyam/khayyam.md). That lowering is a realization of this topic, not this topic's definition.

### The compiler emits analysis events
The compiler, as an independent application, emits events that analysis tools subscribe to — entering and leaving a scope, taking or skipping a branch — rather than requiring those tools to recognize a library's constructs by name. The [Linter](./linter.md) and definite-assignment / path-coverage analyses consume this surface. Once tools depend on it, changing event shape or ordering is a breaking change for consumers the compiler does not control. The versioned event schema is not yet specified; see the paired handoff.

### Entry and lifecycle are not grammar
A compiler does not hardcode a syntax-level entry point or lifecycle (`main`, `init`, `deinit`, or equivalents) into the language it consumes. How a program boots and tears down is compiler configuration plus the selected [Runtime](./runtime.md). Changing target environment — a Unix process, a unikernel, WebAssembly, a serverless handler, a JavaScript host — is a configuration change, not a language change.

The cost of the rule is real: a newcomer cannot discover where execution starts from the language alone. That cost is accepted so the language does not have to grow a new entry-point syntax each time the execution environment changes.

### Designated pure operations may run at compile time
An operation that does not depend on runtime state, and that is *explicitly designated* as pure, may be evaluated during compilation and replaced in the target by its result. Qualification is designation plus purity, never a privileged type the compiler "knows." Languages that fold constants implicitly still owe an equivalent honesty about *which* operations ran at compile time; this protocol's default is explicit designation so a reader can see the boundary.

Compile-time evaluation is a second interpreter that must stay semantically identical to runtime evaluation of the same operation. Divergence is a real bug class. Designation adds an authoring obligation that implicit const-evaluation does not have; the protocol accepts that cost for visibility.

### The compiler consumes the Lexer; it is not the Lexer
Lexical processing is owned by the [Lexer](./lexer.md). A compiler is one consumer of that protocol. Tokenization strategy, token shape, and whether a lexer exists at all for a given source are not compiler-definitional. A compiler that parses characters directly remains a valid architecture under the Lexer protocol's own terms.

### Runtime mutation of the artifact is `unsafe`
A compiler may support emitting or linking code that patches a running module's binary — adding or removing modules the way a WASM host replaces a module. The capability is dangerous and MUST be tagged `unsafe`. It is an opt-in escape hatch from [Structure Is Fixed by Definition](../type.md#structure-is-fixed-by-definition), not the normal path. The [Runtime](./runtime.md) states the same hatch on the execution side; [immutable infrastructure](./immutable_infrastructure.md) owns the deployment-side working-out. The two sides do not contradict: default is the base principle; the hatch is explicit, audited, and never used for normal capability evolution.
