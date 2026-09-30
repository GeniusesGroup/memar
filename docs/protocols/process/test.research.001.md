# Test Research 001 — How Languages and Their Ecosystems Arrange Tests

## Contents
- [Status](#status)
- [Question and Goals](#question-and-goals)
- [Participants](#participants)
- [Methodology](#methodology)
- [Findings](#findings)
- [Open Questions](#open-questions)
- [Conclusion](#conclusion)
- [Related Artifacts](#related-artifacts)

## Status
Active

The four questions carry final standing, but the inquiry is not closed. The web-search facility was unavailable for the whole session, which left its open questions unresolved rather than answered, and a survey of this kind is never exhausted by one pass. Marking it `Complete` recorded that the questions had been answered, which is not the same as the inquiry being finished; an `Active` record is the mutable instrument this needs.

## Question and Goals

### Questions
1. **Is any test file layout, file naming rule, or discovery scheme mandated by a language specification or by a standards body (ISO, ECMA, W3C, IETF)?** — Answered
2. **Across ecosystems, what mechanism actually finds a test, and what does the distribution of mechanisms imply about what a repository should standardize?** — Answered
3. **Do any ecosystems separate "the file that implements" from "the file that checks" by folder rather than by a marker in the name, and is that arrangement compatible with reading a test as an expectation of a contract rather than as an implementation detail?** — Answered
4. **Does a comparative survey of test arrangement across languages exist in the peer-reviewed literature?** — Withdrawn: the premise was not established and the negative result is not reliable enough to state

### Goals
- Give [Test Placement](../../../modules/process/test/rules/test-placement/test-placement.md) and [Test Naming](../../../modules/process/test/rules/test-naming/test-naming.md) an external basis, or record explicitly that none exists, so that neither Rule is mistakable for a standard and neither claims authority it lacks — Met
- Record what the ecosystems actually do, so that a later session does not re-derive the survey from documentation to answer a question already answered here — Met
- Identify where this repository's arrangement sits among the existing ones, so the Rules' arguments are about a real position rather than an invented alternative — Met

### Scope
Covers how a Test is located, named, and discovered in the mainstream language ecosystems, and what the owning authority is for each. It does not cover how a Test is *written*, what assertion library a Test uses, how a suite is run in CI, or any measurement of testing's effectiveness; the effectiveness literature is the subject of [Test Research 002](./test.research.002.md).

## Participants
- [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — `Questioner`, `Goal-setter`. Asked for a survey of how other languages approach tests, on the reasoning that a rule stating where a Test lives should be answerable to something outside this repository rather than to this repository's own habit.
- Auto (model not recorded) — `Researcher`. Conducted the survey and wrote this record.

No reviewer has examined this record: Not yet reviewed.

## Methodology
Each ecosystem row was assembled from a primary source — the language's own specification, the tool's own documentation, or the tool's source code — and is marked in the findings below as verified against a primary source or not. Where a claim is about a tool's observable behavior (a glob pattern, a default value, a matching predicate in source) it is stated as verified; where it is about a project's stated philosophy, it is marked as self-assessment and is not treated as evidence.

The method was constrained by an environmental limitation that shapes the whole record: the web-search facility returned HTTP 403 for every call in the session. Discovery was therefore restricted to direct retrieval of known documentation URLs, the GitHub and package source trees, and the Crossref bibliographic API. Open-ended discovery — in particular question 4, and any check of what the community believes rather than what a tool does — could not be performed. That limitation is why question 4 is withdrawn rather than answered, and why the Open Questions below are stated as unresolved rather than as negatives.

Two further sources were unreachable: `iso.org` and `webstore.iec.ch` returned 403 and 404, so no ISO/IEC/IEEE software-testing standard was read. Every statement about what such standards contain is inference from their scope, and is marked as such.

## Findings

### No specification and no standards body mandates any test arrangement
The central finding, and the one the Rules depend on. Four specifications were checked individually and none contains a test file layout, a test file naming rule, or a discovery scheme.

The **Go Language Specification** (go1.27) contains no occurrence of `_test.go` and no occurrence of the phrase "test file". The suffix rule lives in `go/build`'s `Context.Import`, which matches `strings.HasSuffix(name, "_test.go")` — a property of the `go` command, documented in `go help test` and in the `testing` package documentation, not of the language.

The **Java Language Specification SE 25** contains no occurrence of `src/test`, `Test.java`, `JUnit`, or "unit test". The JVM specification likewise imposes nothing on a repository's shape. `src/test/java` is Apache Maven's and Gradle's convention, and Maven's own guide states it as a convention to conform to with the settings overridable through the project descriptor.

**ECMA-262** contains no occurrence of `src/test`. Module resolution, grammar, and semantics are silent.

The **Rust Reference** makes the `#[test]` attribute normative — it is a language feature — while the `tests/` directory is Cargo's, which the Cargo Book frames as inference ("Cargo automatically determines the targets to build based on the layout of the files on the filesystem") and documents as disableable with `autotests = false`. rustc has no layout opinion.

There are exactly two cases in the whole survey where a *language specification* constrains anything test-related, and both constrain a syntactic construct rather than a location. **D** makes `unittest` a grammar production (`UnitTest: unittest BlockStatement`), documented at dlang.org/spec/unittest.html, with unit tests run after static initialization and before `main()` — a lifecycle position no other surveyed ecosystem uses, and the reason D's blocks may appear inside `struct`, `class`, and `interface` bodies. The specification is candid about what it declines: it marks the presentation of results, the method of enabling the tests, and whether the program stops at the first failure as implementation-defined, and it states that when unit tests are not enabled the implementation is not required to check the block for semantic correctness. **Zig** documents `test` as a top-level declaration form in the Zig Language Reference, with an implicit return type of `anyerror!void` that cannot be changed.

The structural reason generalizes, and it is the reason a Rule rather than a standard is the right form for such a condition. A language specification defines programs in terms of compilation units and grammar. It has no vocabulary for "folder", because a conforming implementation has no reason to care whether a file is in a directory called `x` or `y`. The moment a specification constrains a filename or a path it is constraining a toolchain, and a toolchain is not a specification.

**Evidence:** Go Language Specification; JLS SE 25; ECMA-262; The Rust Reference; The Cargo Book; D language specification; Zig Language Reference.

### Who actually owns each convention, and in what order of authority
Descending order of authority, as the survey found it:

1. **Language specifications**, only for in-language constructs: D's `unittest`, Zig's `test`. Never for layout or naming.
2. **The reference implementation's build tool**: Go (`cmd/go`), Rust (Cargo), Elixir (Mix), R (`R CMD check`), Perl (MakeMaker), Julia (Pkg). Shipped with the language, so the convention has near-official standing, but it is a tool's choice.
3. **The official standard library**: Python's `unittest` (`test*.py`), Erlang's EUnit (function-name suffixes `_test` / `_test_`), Nim's `std/unittest`, Julia's `Test`, Zig's `std.testing`. Rarer than commonly assumed.
4. **A dominant third-party framework**: Java (Surefire's filename globs), JavaScript (Jest, Vitest, Mocha), Python (pytest), Ruby (RSpec, Minitest), PHP (PHPUnit), C and C++ (GoogleTest, Catch2, doctest), C# (xUnit, NUnit), Haskell (Hspec).
5. **The build tool as enforcing agent**: Maven, Gradle, sbt, CMake, dune — usually where a layout is physically enforced rather than merely advised.
6. **Community convention**: `runtests.jl`, `00compile.t`, `spec/`, `t/`.

That the fourth rung is where most of the ecosystem lives is the reason the placement Rule in this repository can claim no external authority and must therefore argue for its position rather than appeal to one.

### Discovery is not one mechanism, and the common description is wrong for a large share of ecosystems
The claim that "test runners scan directories" is true for Python, JavaScript, Ruby, Elixir, R, Java under Surefire, Node's built-in runner, Mocha, and Vitest. It is **false** for a substantial fraction of the surveyed table, in four distinct ways.

**Link-time synthesis.** `go test` does not scan. It generates a synthetic main package, `_testmain.go`, containing an explicit static list of the discovered functions (`tests = []testing.InternalTest{{"TestFoo", TestFoo}, ...}`). Discovery is therefore a link-time fact, which is why an unused import in a test file is a compile error rather than a silent no-op.

**Compile-time registration.** Rust's `libtest` is linked in by the `--test` flag and collects `#[test]` functions through compiler-generated registration, not reflection; a crate may set `harness = false` and supply its own runner instead. Zig's `test` declarations are compiled into the artifact and executed by the compiler's own runner; `zig test file.zig` needs no build script.

**Static-initialization self-registration.** GoogleTest, Catch2, and doctest expand `TEST(A, B)` into a static object that registers itself at static-init time, and `RUN_ALL_TESTS()` walks the registry. There is no scanning, no naming convention, and no manifest at all. The corollary surprises newcomers: a test in a translation unit that does not link the framework's `main` is silently never run.

**Manifest, in a tree that is not the source tree.** CMake/CTest has no filename convention; tests are declared explicitly with `add_test(NAME … COMMAND …)` and recorded in a generated `CTestTestfile.cmake` in the build tree. PHPUnit is the most explicitly manifest-driven mainstream arrangement, naming its directories and files in `phpunit.xml` with nothing globbed implicitly.

The implication for a repository is narrow but real: *where the mechanism differs, the layout matters differently.* A repository whose ecosystem discovers by suffix scan is made more fragile by a naming convention, because the convention is load-bearing. A repository whose ecosystem discovers by manifest is insulated from naming entirely. A repository whose ecosystem provides no runner at all is not constrained by either.

**Evidence:** `go/build/build.go` and `src/cmd/go/internal/test/test.go`; the `testing` package documentation; the Cargo Book; the Rust Reference; the D and Zig language specifications; Google's GoogleTest source; CMake's `add_test` documentation; PHPUnit's `phpunit.xml` documentation.

### Arrangement by ecosystem
Verified against each project's own documentation or source.

- **Go** — tests beside the code in the same package directory, or a separate `package foo_test`; `testdata/` is ignored by the tool. File suffix `_test.go`, matched case-sensitively; function names `TestXxx` with a capital. `go/build` owns the suffix; the specification does not mention it.
- **Rust** — two kinds with a stated rationale: inline `#[cfg(test)] mod tests` beside the code, which reaches private functions and is compiled only under `cargo test`; and a `tests/` directory, each file compiled as a separate crate so that only the public API is visible, which is how an external consumer sees the library. Files in subdirectories of `tests/` are not compiled as separate crates.
- **Python** — `unittest` discovers by directory walk and `fnmatch` on `test*.py`, then imports and reflects; the pattern is documented as `test*.py` in the standard library's `discover` options. `pytest` is third-party, defaults to `test_*.py` **or** `*_test.py`, and is therefore not interchangeable with `unittest` without silently changing which files are collected.
- **Java** — the chain of custody has three owners: `src/test/java` from Maven or Gradle; the filename globs `**/Test*.java`, `**/*Test.java`, `**/*Tests.java`, `**/*TestCase.java` from Surefire's `getDefaultIncludes()`; the test's identity from JUnit, by annotation and reflection. The `*Test` filter people attribute to JUnit belongs to the build tool.
- **JavaScript and TypeScript** — Node's built-in runner matches a fixed set of filename globs and registers tests imperatively; Jest and Vitest each carry their own default glob and configurable alternates; Mocha defaults to `./test/*.{js,cjs,mjs}` and inspects no names at all.
- **Ruby** — RSpec defaults to a `spec/` path and a `*_spec.rb` glob; Minitest ships with the standard library and its generated rake task globs `test/**/*_test.rb`.
- **C and C++** — no layout convention exists; discovery is self-registration, described above.
- **Erlang** — EUnit runs tests in the same module or in a parallel `<Module>_tests`, matching function-name suffixes, and ships with OTP; Common Test is the separate framework with a directory layout. *(The Common Test details were not verified and are not relied on here.)*
- **Elixir** — `mix test` hard-codes the glob `test/**/*_test.exs` and requires a `test/test_helper.exs`; the task ships in Elixir's core distribution, making this among the most official arrangements surveyed.
- **R** — `R CMD check` runs **every** `.R` file in `tests/`, with no pattern, which is unusually strong for an interpreted language and is documented in *Writing R Extensions*.
- **Perl** — `t/` at the distribution root, `*.t`, run by MakeMaker's `make test` through a harness shipped with the core distribution, emitting TAP — which is the one cross-language de facto standard in this domain.
- **Zig, D, Nim, Julia** — the languages that provide a facility in the language or its standard library: Zig's grammar-level `test` blocks and the compiler's runner, D's grammar-level `unittest` blocks, Nim's `std/unittest` macros, Julia's `Test` standard library invoked through `test/runtests.jl` by `Pkg.test()`.
- **PHP, Haskell, Scala, C#, Swift, Kotlin, Lua, OCaml** — each a build-tool or framework arrangement: an explicit manifest (PHPUnit, dune), a declared test-suite entry (Cabal), a build-tool source set plus reflection (sbt, Gradle), an attribute plus a separate test project (xUnit, XCTest, `kotlin.test` as a facade that deliberately discovers nothing), or a required directory name (busted). *(The OCaml, Scala, Kotlin, C# discovery mechanisms, and Common Test, were not verified against a primary source and are listed in Open Questions.)*

### Where this repository's arrangement sits
The Rules in `modules/process/test/rules/` state that a Test lives in a `tests/` folder inside the module that owns the Process it names, and that its name carries no marker. The survey finds that both halves have precedent, and that the combination has precedent too.

A dedicated test folder beside the module is used by Elixir (`test/`), R (`tests/`), Perl (`t/`), Rust's integration tests (`tests/`), Zeller's own delta-debugging convention, Julia (`test/`), sbt (`src/test/`, which is a role folder rather than a `tests/` one), and PHP's default. Two notable ecosystems pair that folder with a marker in the name (Elixir's `*_test.exs`, Perl's `.t`); this repository's naming Rule removes the marker on the ground that the folder already states it, which makes the name the only place that does not.

What the survey does **not** support is the claim that a `tests/` folder is better than a sibling marker. No ecosystem comparison establishes that; the survey found no such study (question 4). The Rules therefore stand on the argument they state in full — the module's own files stay all production files, so a reader's inference is sound without knowing any convention, and a module's Tests become one addressable thing — and not on an external finding. That is a defensible position, and it is a position rather than a standard.

## Open Questions
- Whether any peer-reviewed comparative study of test-file arrangement across languages exists. Searches under Crossref for six phrasings of the question returned nothing on topic, degrading into unrelated literature; ACM DL, DBLP, and Scopus were unreachable. A targeted search of a subscription database would likely do better than the Crossref queries used here. Until then, the absence of such a survey is not established.
- Whether ISO/IEC/IEEE 29119 or a comparable standard says anything about repository arrangement. The class of standards addresses testing as a process activity, and none of the ones surveyed addresses source-file arrangement; but this is inference from scope, not from reading, because the standards themselves were unreachable.
- How the discovery mechanisms for C#, Kotlin, Scala, OCaml, and Erlang's Common Test actually work. The C# row in particular rests on a project's homepage and a best-practices page rather than on the runners' documentation.
- Whether the Go project has ever considered accepting `_Test.go`; the function-naming rule requires a capital and the file-suffix rule does not, and this pair of opposite conventions is a recurring source of confusion.
- Whether the two singular role folders in this repository's own Khayyam toolchain (`core/test/`, `targets/*/test/`) are the same case as the plural folders the placement Rule governs, or a drift. The plural was argued in the Rule from the count of instances a folder holds; the general convention has no document of its own.

## Conclusion
Question 1 is answered in the negative, specifically and verifiably: no language specification and no standards body mandates any test layout, naming rule, or discovery scheme. The two constructions that appear in specifications — D's `unittest` and Zig's `test` — constrain where tests may be *written within a file*, and neither constrains a filename or a directory. This is the load-bearing finding, because it establishes that a condition about test placement is necessarily an owner's Rule rather than a standard, which is the form `docs/rule.md` already prescribes.

Question 2 is answered: discovery is not one mechanism, and the mechanism determines how much a repository's layout matters. Question 3 is answered in the affirmative and with precedent on both halves, while the survey establishes no external basis for preferring this arrangement over its alternatives — so the Rules' own stated argument is what carries them.

Question 4 is withdrawn. The premise — that a comparative survey exists to be consulted — was not established, and the search that failed to find one is not reliable enough to support a claim that none exists.

No change to [test.md](./test.md) follows from this research: that document states no structural rule, and this research concerns none. The placement and naming Rules were written under the protocol's Rule-then-realization separation, and this record is the external basis a later reader needs in order to judge them — the finding that no external authority exists being itself the reason they must argue rather than appeal. The Rule index at `modules/process/test/rules/README.md` gains no citation from this, because a Rule's subject is the Test protocol and not the state of the ecosystems.

## Related Artifacts
- [test.md](./test.md) — the protocol these Rules check. Needs no revision; it states no structural rule by design.
- [Test Placement](../../../modules/process/test/rules/test-placement/test-placement.md) — the Rule whose "who decides" premise this research establishes. Needs no revision; its argument is unchanged and its handoff already records that no check enforces it.
- [Test Naming](../../../modules/process/test/rules/test-naming/test-naming.md) — the sibling Rule. Its observation that a marker duplicates what the folder states is confirmed by the survey's finding that the pair is widely used together (Elixir, Perl), which makes the Rule's argument about duplication rather than about unfamiliarity.
- [test.research.002.md](./test.research.002.md) — the companion research on the literature, which bears on the protocol rather than on its realization.
