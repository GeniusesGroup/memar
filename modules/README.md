# Modules (`modules/`)

## What this layer is
Implementation modules: the realizations of what the specifications state — protocol implementations, language-specific toolchains, and the Khayyam library sources (`.kh`). The protocols index already fixes the boundary: "Implementation modules live under `modules/` in this repository" ([protocols → Where implementations live](../docs/protocols/README.md#where-implementations-live)), while the protocol folder itself is "not executable code". Within this layer, placement follows the responsibility a folder names, and each module states its own membership criterion in its own README.

## Why a folder may exist before it holds code
A folder here is a carrier of thinking, not a container waiting for code. Much of this project's design reasoning lived in folder names long before it lived in documents; where the folders were absent, those ideas went unevaluated and the work fell into the ecosystem's general patterns by default — the outcome this project's own principles reject. A folder created ahead of its content keeps a decided direction visible and gives each idea a place to be argued about.

Three rules follow, and they are decisions rather than preferences:
- **An empty folder is a decision made visible.** Do not delete one for being empty; restructure it only with an argument.
- **No folder here is final.** Names may be merged, split, moved, or retired whenever the responsibility they name is better served another way.
- **A folder without a README carries its intent in its name** until one is written; a README is what makes the membership criterion inspectable.

## The kinds of folder here
- **By responsibility** — `computer/`, `process/`, `memory/`, `net/`, `codec/`, `string/`, `math/`, `time/`, `identifier/`, `hardware/`, `crypto/`, `gui/`, `lib/`, `runtime/`. Several of these carry a second level that is itself a set of ideas (for example `process/rule/` and `process/rules-engine/` — a rule, and the general mechanism that executes rules by their stated conditions).
- **By language** — `khayyam/` holds the language's own toolchain: `core/` (the target-independent frontend and semantic representation), `rules/` (Khayyam's rules, each citing the document that states its normative claim), and `targets/<emit>/` for each emit target.
- **By mechanism, language-independent** — `computer/lexer/` and the general rule engine are shared: they must not import a language's knowledge, and a language keeps only its own model beside its toolchain ([khayyam → Membership criterion](./khayyam/README.md)).

## What does not belong here
- **Specifications and general claims** — those live in the repository's [`docs/`](../docs/); this layer realizes them, it does not restate them.
- **Generated output** — compiled artifacts and caches live in git-ignored `build/` folders.
- **A language-specific dependency inside a shared mechanism** — a language-agnostic implementation that acquires Khayyam knowledge stops being language-agnostic.
