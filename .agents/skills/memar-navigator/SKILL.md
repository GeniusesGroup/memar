---
name: memar-navigator
description: Use whenever Memar, or any component/sub-project of it, comes up — Khayyam (programming language), PersiaOS, Chapar (data-link protocol), Giti/GP (network layer), GUI, sRPC, Syllab, Achaemenid, or any file belonging to the GeniusesGroup/memar repo. Trigger this for writing/reading/reviewing code or specs in these systems, or any architectural question about them. This is a young, low-adoption, fast-evolving project — do NOT answer from training-data memory or by analogy to mainstream languages/frameworks. Always pull the live docs from the canonical repo via this skill instead of guessing or relying on possibly-stale content pasted earlier in the conversation. Other domain-specific skills (e.g. a Khayyam syntax skill) should defer to this skill for actual document content rather than embedding their own copies.
---

# Memar Navigator
**Memar** ("architect" in Persian) is a software-development structure/framework by Omid Hekayati (GeniusesGroup), expressed as a set of markdown documents. It defines its own programming language (**Khayyam**), OS (**PersiaOS**), network protocols (**Chapar**, **Giti/GP**, **sRPC**), and supporting concepts (encoding, type system, terminology).

**Canonical source of truth (single repo, no forks/mirrors to worry about):**
`https://github.com/GeniusesGroup/memar` — branch `main`

## Why this skill exists
Earlier attempts at this bundled static copies of one or two document files directly inside topic-specific skills (e.g. a Khayyam skill embedding a copy of `Khayyam.md`). That doesn't scale: the repo has 50+ interlinked document files that cite each other and evolve independently, so copies go stale and duplicate maintenance across every skill that needs them. **Don't copy documents content into skill folders.** Instead, fetch it live from the repo every time it's needed, through this skill.

## How to get the docs
The repo is small (~2 MB, almost entirely markdown) and public — a shallow clone is cheap and avoids GitHub API rate limits (the REST API is unauthenticated and shared across many users, so it gets rate-limited quickly; plain `git clone` does not hit that limit).

```bash
# Reuse an existing clone in this session if present; otherwise clone fresh.
[ -d /tmp/memar-repo/.git ] || git clone --depth 1 https://github.com/GeniusesGroup/memar.git /tmp/memar-repo
```

Then read only the specific file(s) relevant to the question with `view` or `grep` — don't `cat` the whole repo into context. If you already cloned it earlier in this same conversation/session, don't reclone; just re-`view` the file (it may have been read once and be enough, or you may need a different file this time).

If a cited file isn't found in the clone, say so plainly and ask the user to provide it directly — it may be an unpublished draft — rather than fabricating its content.

## Cross-reference convention (how to navigate, not guess)
Every document file has YAML frontmatter with a `Citations` list, e.g.:
```yaml
Citations:
    - Title: "Terminology"
      URI: "./terminology.md"
      Kind: Depends_on
      Explanation: "..."
```
- `Kind: Depends_on` → read that file first if the current one assumes it.
- `Kind: Extends` → the current file builds on / narrows that one; check it for the broader picture.
Use these links to follow a topic across files instead of guessing filenames. `grep -A3 "Citations:" <file>` is a fast way to see a file's dependencies before reading further.

## Topic index (orientation only — always confirm against the live clone, since new documents get added)
**Meta / cross-cutting concepts**
`README.md`, `terminology.md`, `protocol.md` (+ `protocol.per.md`, Persian version), `framework.md`, `modeling.md`, `system.md`, `type.md`, `documentation.md`, `knowledge-management.md`, `conditional_naming_convention.md`, `immutable_infrastructure.md`, `error-vs-log-boundary.md`, `filesystem.md`

**Khayyam — language core** (start with `Khayyam.md` for canonical syntax, `khayyam-design_philosophy.md` for rationale)
`Khayyam.md`, `khayyam-design_philosophy.md`, `khayyam-abstraction.md`, `khayyam-encapsulation.md`, `khayyam-inheritance.md`, `khayyam-polymorphism.md`, `khayyam-variable.md`, `khayyam-memory_model.md`, `khayyam-concurrency.md`, `khayyam-error_handling.md`, `khayyam-function_as_capsule.md`, `khayyam-library_driven_control_flow.md`, `khayyam-naming_driven_package_elimination.md`, `khayyam-dependency_resolution.md`, `khayyam-composition_depth_as_decomposition_signal.md`, `khayyam-absence_of_closures.md`, `khayyam-decorators_rejection.md`, `khayyam-rejection_of_macros.md`, `khayyam-domain_driven_arithmetic.md`

**Khayyam — tooling**
`Khayyam-compiler.md`, `Khayyam-linter.md`, `Khayyam-runtime.md`, `Khayyam-migration_guide.md`

**Type system extras**
`type-explicit_behavior_ownership.md`, `type-metadata.md`, `type-static_concepts_must_be_types.md`

**OS / platform**
`PersiaOS.md`

**Networking / protocols**
`networking.md`, `networking-osi_1-Asb.md`, `networking-osi_3-Giti-Network.md`, `networking-frame-signature.md`, `chapar.md`, `chapar-introduction-goals-and-topology.md`, `chapar-discovery-and-path-establishment.md`, `chapar-broadcast-scope-and-known-risks.md`, `chapar-vs-ethernet-rationale.md`, `sRPC.md`

**Interfaces**
`GUI.md`, `Giti.md`

**Encoding**
`Syllab.md`, `characters-codec.md`, `media-type.md`

## Guidance for other skills in this family
A topic-specific skill (e.g. one about writing Khayyam code) should:
1. Say up front that it defers to this skill for actual document content.
2. List which filenames from the index above are most relevant to its topic, so the model doesn't have to rediscover that mapping each time.
3. Not embed quoted document text as a "cheat sheet" that could drift from the live spec — a short *mechanically-derived* syntax summary is fine if clearly labeled as a convenience summary to be verified against the live file when precision matters, but the live file is always the source of truth.
