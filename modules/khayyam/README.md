# Khayyam (`modules/khayyam/`)
This directory is the Khayyam toolchain module of this repository — the language's own tooling: the target-independent frontend and semantic representation, one folder per emit target, the Khayyam realization of any language-independent tool, and the documents that govern that work. It answers "how is Khayyam compiled, checked, and shipped?" — not "what is Khayyam?" ([Khayyam design](../../docs/khayyam/README.md)) and not "what is Memar's protocol for X?" ([protocols](../../docs/protocols/README.md)).

The governing plan lives at the root because it governs the core and the first target together: [execution.md](./execution.md) is the JavaScript-first execution roadmap (M0–M5); unfinished state and open questions live in its paired [handoff](./execution.handoff.md), and the readiness review record in [execution.research.001.md](./execution.research.001.md).

## Membership criterion
A document or module belongs here when it is specific to Khayyam: the language's own compiler core, a target realization of the language, or the Khayyam-specific part of a language-independent tool.

What does **not** belong here:
- **Language-independent mechanisms** — the generic Lexer and the general rule engine belong in the shared implementation modules under [`modules/`](../), without importing Khayyam knowledge, following the placement the plan already records for the Lexer ([execution.md → Pipeline](./execution.md#pipeline)). A shared mechanism must not acquire a language-specific dependency.
- **Khayyam language specification** — grammar and construct design live in [`docs/khayyam/`](../../docs/khayyam/), while language-wide library source (`.kh`) lives in the other module folders under [`modules/`](../).
- **General concepts** (Type, Modeling, Process, …) — the repository's [`docs/` root](../../docs/).

## Local placement
The module organizes by kind — language-specific work at the root, every emit target under `targets/`, and language-independent protocol implementations shared with the rest of the repository:

| Content | Placement | Rule |
| --- | --- | --- |
| Governing plan, handoff, and research records | `modules/khayyam/execution.*` | The plan governs the core and its first target together, so it sits above both |
| Frontend + semantic representation (every target consumes this one head) | `modules/khayyam/core/` | Target-independent code never lives inside a target folder |
| Emit target: backend, runtime glue, compile cache, demo, and that target's own plan | `modules/khayyam/targets/<emit>/` — `js` first, then `wasm`, and `c`/`asm` as taken up (per-arch subfolders under `asm/` when real) | The folder names the emit output, never the implementation language; targets never sit beside language-level work at the root |
| Khayyam's rules — each citing the subject document that states its normative claim, with its condition, what it consumes, what it produces, and whether it gates compilation, reports governance, or rewrites source | `modules/khayyam/rules/` | There is no `linter/` folder: "linter" and "formatter" are labels on rules, not places — a formatter is a rule that rewrites source |
| Language-independent mechanisms (generic Lexer, the general rule engine) | `modules/<category>/<name>/` — `modules/computer/lexer/`; the rule engine's home is the open question in the handoff | No Khayyam knowledge leaks into a shared mechanism |
| Khayyam language-wide design and `.kh` library | `docs/khayyam/`, `modules/` | Language-owned material is not part of the toolchain |
| Cross-cutting protocol and readiness design that is host-independent | `docs/` (protocols under `docs/protocols/`) | General claims live at the repository level |

A folder that names a responsibility the project has already accepted may be created before it holds code; nothing here is final, and any grouping may be restructured when a good argument calls for it (see the handoff's Decisions).

The compile cache and any generated JavaScript are build products of the JS target; they are git-ignored and never committed (see [execution.md → Compile cache](./execution.md#compile-cache)).
