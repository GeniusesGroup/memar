---
name: memar
description: Operating practices for any work conducted the Memar way — not only work inside the GeniusesGroup/memar repository. Use when developing any system (software, hardware, apps, gadgets, buildings, organizations/society) with Memar; when working on a Memar-built project (e.g. `organization`); a Memar sub-project (Khayyam, os, Chapar, Giti/GP, sRPC, GUI, Syllab, Achaemenid); or when applying Memar's principles even if "Memar" is never named — e.g. "write this in Khayyam" or "design this the way Memar does". Also covers reasoning about ideas, architecture, modeling, terminology, critique, or documentation under Memar's approach. This skill holds no project knowledge; it only defines how to discover and use Memar's live documentation to hold the Memar mental model before acting.
---

# Memar

## Purpose
This skill defines how an agent discovers and applies Memar (and its sub-projects, including Khayyam). It does **not** duplicate project documentation. Project knowledge lives in the repository (`docs/`). This skill only explains how to find, navigate, and use that knowledge.

## Scope
Memar and Khayyam are meant to be *used*, not only maintained. Most people who trigger this skill are working on **their own** project — code, hardware, an organization, etc. — and want Memar's approach. Treat `GeniusesGroup/memar` as **reference documentation**; do the actual work in the person's project. Do not assume that project *is* Memar, do not assume it is software, and do not wait for the word "Memar" — phrases like "write this in Khayyam" are enough.

Memar is the **framework the development is conducted within**, not a passive library. When a project is developed the Memar way, Memar's principles participate in every stage. Keep this skill active for the life of such a project — architecture, modeling, implementation, review, and documentation — not only at the start.

## Separation of knowledge
1. **Repository documentation** — the source of truth: the facet system of [documentation.md](/docs/documentation.md) and the protocol contracts of [protocol.md](/docs/protocol.md), living in [`docs/protocols/`](/docs/protocols/). That system names its own kinds and grows; this skill does not enumerate them. Never invent ad-hoc note formats: when work produces state worth persisting, discover the governing facet and follow its practice.
2. **Agent configuration** — how *this* agent, with *its* tools, discovers and applies the above. Organizational ways of working belong in the repository's Practice-facet documents, never here; only tool-dependent content lives in this skill.

## Working rules
- Before reasoning about ideas, architecture, modeling, terminology, or critique, read [**Cognition**](/docs/cognition.md) and follow its discourse norms.
- Before enacting any development step, read [**Test**](/docs/protocols/process/test.md) and follow [Test Practice](/docs/protocols/process/test.practice.md) for the procedure.
- Before writing or editing a document under Memar's own `docs/`, follow [Documentation Practice](/docs/documentation.practice.md); the facets it presupposes are defined in [Documentation](/docs/documentation.md).
- Text reaches a file through a file-write tool or through [`memar-documentation.py`](/.agents/scripts/memar-documentation.py), never through a shell's own text handling; run that tool's `check` on what you wrote. Why a shell damages the files it reads is in [Scripts → Putting text into a file](/.agents/scripts/README.md#putting-text-into-a-file).
- Never answer from training-data memory when project documentation exists, and never derive a Memar rule, convention, or term from the domain's mainstream standard — general domain background is fine, Memar behavior invented from it is not. Where the two disagree, the Memar definition governs ([Terminology → Terminology Authority and Governance](/docs/terminology.md#terminology-authority-and-governance)).
- Treat repository documentation as the canonical source of truth.
- Discover relevant documents from the repository; do not rely on embedded copies or a hardcoded file list.
- Read only the documentation required for the current task.
- Do not read [`docs/protocols/`](/docs/protocols/) wholesale. If a subject there seems needed (e.g. Error), read that folder's [`README.md`](/docs/protocols/README.md) first; list the folder for filenames as the index. When the task only needs to *use* a library that implements a protocol, skip those docs and go to the implementing code in this repository (`modules/`). Open a protocol document only when the contract itself is the subject.
- Do not enumerate unrelated Memar documentation merely because it exists.
- Do not restart discovery on every turn when the relevant knowledge is already in context.
- If the task is unrelated to Memar-specific knowledge, do not discover Memar docs merely because this skill is active.
- If required documentation cannot be found, say so clearly instead of fabricating an answer.
- When a request is ambiguous in intent, scope, or acceptance criteria, ask immediately — do not guess or over-derive to resolve it. Apply Cognition's *Ask rather than assume* norm at intake, not only during reasoning.
- When a change is large-scope — a definition other documents reference, a restructure of a document or the document set, or edits spanning several files — present the plan (the proposed text and the list of touched files) and obtain the user's explicit approval before applying; after applying, hold the result open for the user's review and apply their feedback. Apply Cognition's *Confirm before large-scope changes* norm at intake, not only during reasoning.
- When a request opens a development thread unrelated to the current session's purpose, do not execute it in this session's context — follow [Handoff Practice → Mid-session tangents](/docs/documentation-handoff.practice.md#mid-session-tangents).
- Canonical repository: https://github.com/GeniusesGroup/memar
- Do not embed copies of project documents inside this skill.

## Session economy with sub-agents
This section is agent-specific (tool-dependent), so it lives here rather than in a repository Practice. When the runtime supports sub-agents:
- Do not spend the main session's context on bounded exploration whose raw material you will not need after integration.
- Keep local what requires the session's held model — target structure, judgment, final merge. Delegate bounded, self-contained discovery (e.g. "extract document X's concepts against this brief and report where they map") to a sub-agent; receive a report sized to what that delegated work needs; apply the merge yourself mechanically.
- The brief must tell the sub-agent to load this skill and discover documentation per it — a sub-agent does not load it on its own, and one that works without it works from training-data memory — rather than carrying a content dump, and must ask for a structured report with acceptance criteria stated.
- Do not delegate work whose intermediate context is itself the deliverable, or work needing continuous back-and-forth judgment; delegation is lossy and has coordination cost.
- Prefer a **new** sub-agent with a short brief (paths + the passages it must judge) over **resuming** a long prior sub-agent thread: resume replays that thread's history into the bill again. Prefer a smaller model when the job is a second opinion, not primary drafting. Do not open whole base documents when the needed sections can be named by path and anchor.

## Documentation navigation
Paths here resolve against `MEMAR_ROOT`, the environment variable naming the one Memar checkout on this machine: this skill is copied into other repositories, so that variable — not the user's workspace, this folder, or the filesystem root — is what a path in it is relative to. What the variable holds and what to run when it is unset: [Scripts → Where Memar lives](/.agents/scripts/README.md#where-memar-lives).

One tool answers questions about Memar's documentation: [`memar-documentation.py`](/.agents/scripts/memar-documentation.py), reached at `$MEMAR_ROOT/.agents/scripts/memar-documentation.py`. It resolves, reads, and searches the doc set. Prefer it to hand-resolving document links or reading whole documents; on shells that rewrite leading-`/` paths (Git Bash/MSYS), pass bare names (`docs/cognition.md`). It declares its own interface through `--help` — ask the tool what it does rather than expecting this document to say. Do **not** maintain a command catalog or pasteable recipe list in this skill — catalogs grow, go stale, and invite every later session to add "one more example."

If Python is absent: read the script source and reproduce only the needed step — prefer the language runtime's own agency when it is available; inventing a parallel recipe catalog here is not the fallback.
