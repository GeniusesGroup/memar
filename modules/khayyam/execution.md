---
Title: "Khayyam JS Execution"
Status: Draft
Start Date: 2026-09-23
ID: 497283
---

# Khayyam JS Execution
## Abstract
This document is the executable plan for running Khayyam source on any JavaScript host (browser, V8, Node): a language frontend → one semantic representation → a JavaScript backend → a JS runtime, with an incremental compile cache so unchanged files are not recompiled. It is the working realization of the first-prototype path recorded in the repository's [Compiler Handoff](../../docs/protocols/computer/compiler.handoff.md): quick feedback without treating speed as a license to skip modeling or the Implementation Readiness Review. Two disciplines bind every milestone: the JavaScript backend never becomes the hidden specification of Khayyam's semantics; no library name is ever an intrinsic of the frontend. The order *within* a milestone is fixed as well, and is stated under [How work in this toolchain proceeds](#how-work-in-this-toolchain-proceeds): a goal becomes an abstraction or a protocol in the language first, the output shape is fixed by a test written before the code, and the code comes last. Open questions live in the paired [handoff](./execution.handoff.md).

## Introduction
### Motivation
Khayyam is specified but not executable: no lexer, frontend, or backend exists in this repository yet, and the `.kh` library sources under `modules/` cannot run until a toolchain exists to compile them. Without a written plan that fixes placement, scope, order, and cache behavior before code, each session would re-derive those choices — and the fast path would risk becoming an unprincipled one.

### Methodology
The plan follows memar's ordering discipline: modeling output and readiness review precede implementation code ([Modeling Before Implementation](../../docs/modeling.md)); the pipeline shape comes from the Compiler and Runtime protocols rather than from ad-hoc design; scope was chosen among explicit alternatives (core-then-bootstrap vs. demo-with-simulated-control-flow vs. full-language) with the rejected alternatives recorded in the [handoff](./execution.handoff.md). Milestones are ordered so each ends in inspectable running feedback.

## Explanation
### Goal
A `.kh` source compiles to JavaScript and runs on a JS host with correct observable behavior, without recompiling unchanged inputs, and without any layer outside the semantic representation defining what the program means.

### The goals, in the order they come
Each goal is owed by the milestones named beside it, and each is finished when the check written beside it passes. They are stated in the order the work reaches them, because each one's check is written against the shape the one before it fixed.

1. **The plan, the open state, and the folder's own placement exist before any compiler code does.** Owed by M0. A session that starts cold must be able to read this document and its handoff and know what is decided, what is open, and where each open question is anchored, without a conversation. Done when every open question in the handoff names a file and a line, when [execution.research.001.md](./execution.research.001.md) records the specification state the plan was rated against, and when the cache ignore rules are in [`.gitignore`](../../.gitignore) — checked by reading those three artifacts, not by running anything.
2. **The frontend accepts and refuses the core grammar against an inspectable semantic representation.** Owed by M1. Done when [core/test/form.test.ts](./core/test/form.test.ts) passes with every accepted form naming the document section its form comes from, [core/test/refusal.test.ts](./core/test/refusal.test.ts) pins the one label each refused form must carry, [core/test/gate.test.ts](./core/test/gate.test.ts) and [core/test/reader.test.ts](./core/test/reader.test.ts) hold the gate and the reader, and [core/test/matrix.test.ts](./core/test/matrix.test.ts) is green over the archive — every refusal reason being one label in [core/src/sr.ts](./core/src/sr.ts), `tsc --noEmit` clean, and the inspector printing a unit's declarations from a representation no other layer has to interpret.
3. **A `.kh` source runs on a JavaScript host.** Owed by M2. Done when one `.kh` program that needs no library control flow compiles to an ES module that runs under Node, and the same artifact loads in a browser with no bundler — checked by running the artifact, and by loading it, not by reading the backend.
4. **The `.kh` library under `modules/` is reachable, link-first.** Owed by M3. Done when every entry of the URI→JS-module map resolves and records the protocol document it was checked against, every unit with no conformant equivalent compiles from its `.kh` source, and a compiled program that uses library control flow runs.
5. **A reader runs a `.kh` file without a bundler.** Owed by M4. Done when a page opens with no build step, takes a pasted or loaded `.kh` file, resolves and compiles it through the cache, runs it, and shows its output.
6. **Unchanged work is not repeated.** Owed by M5. Done when a second build over unchanged inputs compiles nothing, a change to one file compiles that file and its dependents and no other, and a change to the frontend, the backend, or the compiler version invalidates every entry.
7. **A `.kh` file reads the same wherever it is shown.** Owed by every realization and by no milestone in the table below, because it is the standing form of what the [display contract](./display/display.json) claims and this repository ships one realization of it. Done when a realization that is not the editor — built on the contract alone, with none of the editor's own shapes in it — colours a Khayyam file inside a document that embeds it, and agrees with the contract's value for every role it shows.

### Pipeline
```text
Source (.kh)
  → Frontend (Khayyam-specific; may read source directly in the first prototype)
  → Semantic representation (single source of truth for meaning)
  → JS backend (translation only)
  → Artifact (ES module JS)
  → Runtime (browser / V8 / Node — host, not language)
```
Layer responsibilities:
- **Frontend** accepts or refuses source against the Khayyam grammar (`tp`, `vr`, `in`, `cp`, `mt`, `ab`, `sc` and their forms). It recognizes language primitives only, never library names ([Compiler protocol](../../docs/protocols/computer/compiler.md)). The name `Parser` is not assumed.
- **Semantic representation** is the only carrier of meaning. Both the JS backend (today) and a future WebAssembly backend must sit behind it.
- **JS backend** translates representation to JavaScript. It must not invent semantics the representation does not state.
- **Runtime** is configuration plus the host JS engine. Entry and lifecycle are not grammar.
- **Lexer** (optional, deferred): if a separate lexical layer is introduced later, its language-agnostic implementation belongs under `modules/computer/lexer/`, consuming a Khayyam lexical model that lives with the Khayyam toolchain — not inside the generic lexer. The first prototype may front the source directly while this stays deferred.

The toolchain implementation itself is TypeScript developed on Node during M1–M5; only the artifact — plain ES-module JavaScript — is part of the host contract.

### The language server answers in its own abstractions
The language server is reached by clients that speak protocols this repository did not write, and it answers in its own terms under every one of them. Its own abstractions are five, and none of them is a protocol's:

- **The roles** — what every name *is*: the display contract's twenty-one, in the contract's own order ([`display.json`](./display/display.json)), read through the identity vocabulary in [`core/src/sr.ts`](./core/src/sr.ts). A role names an identity and never a position. One of them names no TextMate scope and says why in the contract, because no grammar can answer it: a role a consumer cannot reach is part of what the server answers in, and a consumer has to be able to read that off the contract rather than discover it.
- **The refusals** — one label per fault this toolchain reports, one list in [`core/src/sr.ts`](./core/src/sr.ts): `unresolved-import`, `name-not-declared`, `kind-mismatch`, `unbound-type-name`, `scope-placement`, each realized as a rule under [`rules/`](./rules/README.md).
- **The document it holds** — one open `.kh` file's whole text, replaced whole on every change, and measured against the synchronization the server declared for itself.
- **The reader** — [`readUnit`](./core/src/reader.ts), which recovers per declaration and returns every fault beside the declarations it did read, so one unreadable declaration costs the file that declaration and nothing else.
- **The gate** — [`analyze`](./core/src/frontend.ts), which resolves an `in` and refuses a unit whose closure it cannot account for, so no target is invoked over a unit this toolchain could not read.

A protocol spoken outward is realized by an adapter in whatever client needs it, never by reshaping the server's own vocabulary. Where an external protocol's structure is incomplete or awkward for what this toolchain answers, that cost is the client's to carry, in the client's own files.

The rule is stated here because reshaping is not a local cost. A name is not one string in one advertisement: it is what the server's answers, its tests, its diagnostic codes, and every later reader of them must match — and a name chosen to fit a client's constraint is then a fact about the server that each later session reads as though that constraint had always required it, because the constraint is invisible and the name is not. The Language Server Protocol is where this toolchain paid that price: the editor's rule that a semantic token type may not carry a separator was answered in the legend rather than in the adapter, and the twenty role names are the shape that answer left. What the roles are then called is a claim about the language, so it is settled where a claim about the language is settled, and it is not settled here: the naming and the work an adapter does instead are carried as open state in the [handoff](./execution.handoff.md).

### Scope decision (bootstrap path)
The working scope is **core grammar first, then library bootstrap**:
1. Implement the frontend and semantic representation for the grammar constructs whose meaning `docs/khayyam/khayyam.md` already states.
2. Lower to JS and run programs that need no library control flow.
3. Bootstrap the `.kh` library under `modules/` link-first: resolve each `in` import through a URI→JS-module map to implementations already conformant to the protocol documents, and compile only the units for which no conformant equivalent exists — library-driven control flow is the expected compile set.
4. Only then treat library-driven control flow (`CF.IF`, `while`, …) as available to user programs.

Rejected alternatives and their reasons are in the handoff; the demo-with-JS-simulated-control-flow path is rejected because it would make the backend a hidden specification.

### Readiness review (Gate)
Before substantial implementation code: for each open item this plan depends on — settle concept definition, boundary, semantic rule, language-vs-implementation ownership, foundational-law vs. pluggable policy, multi-realization realizability, and cross-realization invariants. Findings that concern only this host stay in this folder; findings that are host-independent protocol design belong in the repository's `docs/protocols/`; findings that are Khayyam language design belong in `docs/khayyam/` or the `modules/` tree. The M1 review is recorded in [execution.research.001.md](./execution.research.001.md); its gap list lives in the paired handoff, and its `.kh` inventory resolved the FFI question. Later milestones record their own review passes the same way.

### Milestones
The checkable form of each milestone's completion is [The goals, in the order they come](#the-goals-in-the-order-they-come); the table names what each stage delivers.

| ID | Deliverable | Done when |
| --- | --- | --- |
| M0 | This plan, handoff, folder README, cache ignore rules | Every open question in the handoff names a file and a line, and no compiler code exists |
| M1 | Frontend → semantic representation for the core grammar | The matrix is green with each accepted form naming its document section, and the representation is inspectable |
| M2 | JS backend + first runnable programs (no library control flow) | The artifact runs under Node and loads in a browser |
| M3 | Link-first bootstrap: URI→JS-module map for conformant equivalents, compile the rest | Every map entry records the protocol document it was checked against, and a program using library control flow runs |
| M4 | Browser demo page: paste/load `.kh` → resolve and compile (cached) → run → show output | The end-to-end path runs with no bundler and no build step |
| M5 | Incremental cache hardened (content-hash keys, invalidation on frontend/backend/compiler-version change) | Unchanged files never recompile; changed inputs recompile transitively |

M2 and M3 may interleave if a library construct blocks an earlier runnable sample; the order is default, not a constraint on experimentation.

### How work in this toolchain proceeds
Every piece of work in this toolchain is taken in the same three steps, and the order is part of what the work is, not a preference about how to start it.

1. **A goal becomes an abstraction or a protocol in the language first.** A goal that says what a program may mean is settled where that claim belongs: as an abstraction, a category, a construct, or a boundary in [`docs/khayyam/`](../../docs/khayyam/) and [`docs/type.md`](../../docs/type.md), or as a protocol in [`docs/protocols/`](../../docs/protocols/) when it is host-independent. Nothing is written into a folder of code first and described afterwards, because a term that appears in code before it appears in a document has an owner that never gets to state it, and the document written to catch up states what the code happened to do rather than what a program may mean.
2. **The output shape of a module or a function is fixed by a test written before the code.** The test states what comes out — the rows, the roles, the token stream, the refusal — while nothing yet states how it comes out, so the shape is a decision somebody made and wrote down rather than the first thing that happened to work. A shape discovered while writing is a shape nobody chose, it has no owner to be changed by, and a second caller has to match the code instead of a stated contract.
3. **The code comes last**, written to the shape the test fixed and to the rule the owning document states. The code is the shortest of the three steps because the two before it have already answered what the code is for.

The order is what keeps the disciplines above holdable rather than aspirational. The JS backend cannot become the hidden specification of Khayyam's semantics if the semantics are a document that predates it and the representation behind it; a rule's condition cannot drift from the claim it cites if a test froze the condition's output before the engine that evaluates it existed; and a client cannot be answering about a document no editor holds if the wire's shape was pinned by a test driving the real process rather than settled by whichever shape the code had on the day.

The display realization in [`display/`](./display/) is the worked case of all three: the twenty-one roles and their attributes are [the contract](./display/display.json) and nothing states a value; the output shape is [lsp/test/semantic.test.ts](./lsp/test/semantic.test.ts) and [lsp/test/sync.test.ts](./lsp/test/sync.test.ts), which drive the real server over its own stdio because a statement about the wire is only checkable on the wire, and [display/test/](./display/test/), whose files fix what the realization's own check says — the contract, a test, then the check, in that order, which is also how the twenty-first role arrived; and [`lsp/src/`](./lsp/src/) is written to them.

### Compile cache
Compiled JavaScript is a build product, never a source of truth:
- **Location:** `modules/khayyam/targets/js/build/` (artifact output) with intermediate cache under `modules/khayyam/targets/js/build/.cache/` — both git-ignored in this repository's `.gitignore`.
- **Key:** hash of (source content, link-map revision, frontend version, semantic-representation version, backend version, target host profile). Any change to those inputs invalidates the entry.
- **Transitive invalidation:** Khayyam `in` imports form a dependency graph; a source change recompiles that unit and its dependents, not the whole tree.
- **Portability:** hosts that ship only prebuilt artifacts consume `build/` output from CI or a local build step; the cache itself is never committed.
- **Rule:** no layer may read `build/` output as if it were the semantic representation; only the backend writes it and only the runtime executes it.

### Disciplines binding every milestone
1. The JS backend is never the hidden specification of semantics; the semantic representation is.
2. The frontend recognizes language primitives only — never library names as intrinsics.
3. Entry and lifecycle come from compiler configuration plus the Runtime host, not from grammar.
4. Each milestone's code starts only after the modeling/readiness output it depends on exists (this document + handoff updates).
5. Protocol implementations stay language-agnostic in the shared `modules/` placement; Khayyam-specific knowledge stays under `modules/khayyam/`.
6. Designs take the archived `memar-go` code as their first reference: its deliberately built abstractions and categorizations — production-tested, not yet fully critiqued into documents — guide toolchain and `.kh` library design. Ecosystem idioms (Go standard-library patterns, LLVM-shaped structure, and their kin) are consulted only after recording why the memar-go abstraction does not fit; a rejection is a recorded critique, never a silent substitution.
7. A file transferred from the reference is not finished when it analyzes. Before it is committed, its abstractions are reviewed against [Abstraction in Khayyam](../../docs/khayyam/abstraction.md) and [Polymorphism in Khayyam](../../docs/khayyam/polymorphism.md) — each contract stated once in the file that owns it, a refinement written as abstraction composition rather than as a second interface, a declaration that exists only because the reference instantiated a generic removed, and a name that repeats its owner dropped — and each change recorded as a before/after with the document that justifies it. The bridge's own output is a mechanical transfer, not a reviewed library: discipline 6 says which reference to reach for, this one says the reaching is not the end of the step.
8. No implementation step is begun on a shape that no test fixes first, and no shape is reached from a goal that no document owns. [How work in this toolchain proceeds](#how-work-in-this-toolchain-proceeds) is the order; this discipline is the reason it is not a matter of preference.
9. The language server's own vocabulary is never shaped by an outside protocol. A protocol spoken outward is realized by an adapter in the client that speaks it, and the cost of an external structure that is incomplete or awkward is that client's. [The language server answers in its own abstractions](#the-language-server-answers-in-its-own-abstractions) names the five abstractions the server answers in and states what reshaping costs; the display realization is where the rule was first needed, and what is still open about the naming and the adapter is in the [handoff](./execution.handoff.md).

### Non-goals (this plan)
- Implementing the generic Lexer protocol (`modules/computer/lexer/`) — deferred, not required for M0–M5.
- WebAssembly backend — second target behind the same semantic representation, after JS is proven.
- Changing the repository's root `docs/` for host-specific decisions — placement rules above apply first.
- A conformance suite for the Compiler protocol — anticipated in the repository's compiler handoff, not started here.

## Implications
- Until M3, user programs cannot rely on library control flow; samples must stay within core grammar.
- Any future `modules/computer/lexer/` work in this repository must not import from `modules/khayyam/`.
- Cache layout changes are breaking for local builds only (safe to clear `build/`); they are not protocol changes.
- Taking the order in [How work in this toolchain proceeds](#how-work-in-this-toolchain-proceeds) costs one thing and buys another: every new shape is preceded by a test that has to be argued for, and in exchange no shape in this toolchain exists without a document that owns the claim behind it and a test that owns its output.
