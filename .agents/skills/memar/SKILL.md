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
1. **Repository documentation** — the source of truth, organized by Memar's documentation system: reader-relationship facets governed by [documentation.md](/docs/documentation.md) (each with a governing specification and paired practice), and protocol contracts — one layer above the per-language implementations — governed by [protocol.md](/docs/protocol.md) and living in [`docs/protocols/`](/docs/protocols/). The system names its own kinds and grows; this skill does not enumerate them. Never invent ad-hoc note formats: when work produces state worth persisting (decisions, resolutions, open questions, change history), discover the governing facet and follow its practice.
2. **Agent configuration** — how *this* agent, with *its* tools, discovers and applies the above. Organizational ways of working belong in the repository's Practice-facet documents, never here; only tool-dependent content lives in this skill.

## Working rules
- Before reasoning about ideas, architecture, modeling, terminology, or critique, read [**Thinking**](/docs/thinking.md) and follow its discourse norms.
- Never answer from training-data memory when project documentation exists.
- Never invent Memar-specific rules, conventions, or terminology by analogy to mainstream standards of the domain involved (programming frameworks, building codes, organizational norms, etc.). Memar often departs from mainstream on purpose. General domain background is fine; inventing Memar-specific behavior from it is not.
- Treat repository documentation as the canonical source of truth.
- Discover relevant documents from the repository; do not rely on embedded copies or a hardcoded file list.
- Read only the documentation required for the current task.
- Do not read [`docs/protocols/`](/docs/protocols/) wholesale. If a subject there seems needed (e.g. Error), read that folder's [`README.md`](/docs/protocols/README.md) first; list the folder for filenames as the index. When the task only needs to *use* a library that implements a protocol, skip those docs and go to the implementing `memar-{language}` repository (e.g. https://github.com/GeniusesGroup/memar-khayyam/). Open a protocol document only when the contract itself is the subject.
- Do not enumerate unrelated Memar documentation merely because it exists.
- Do not restart discovery on every turn when the relevant knowledge is already in context.
- If the task is unrelated to Memar-specific knowledge, do not discover Memar docs merely because this skill is active.
- If required documentation cannot be found, say so clearly instead of fabricating an answer.
- When a request is ambiguous in intent, scope, or acceptance criteria, ask immediately — do not guess or over-derive to resolve it. Apply Thinking's *Ask rather than assume* norm at intake, not only during reasoning.
- When a change is large-scope — a definition other documents reference, a restructure of a document or the document set, or edits spanning several files — present the plan (the proposed text and the list of touched files) and obtain the user's explicit approval before applying; after applying, hold the result open for the user's review and apply their feedback. Apply Thinking's *Confirm before large-scope changes* norm at intake, not only during reasoning.
- When a request opens a development thread unrelated to the current session's purpose, do not execute it in this session's context — follow [Handoff Practice → Mid-session tangents](/docs/documentation-handoff.practice.md#mid-session-tangents).
- Canonical repository: https://github.com/GeniusesGroup/memar
- Do not embed copies of project documents inside this skill.

## Session economy with sub-agents
This section is agent-specific (tool-dependent), so it lives here rather than in a repository Practice. When the runtime supports sub-agents:

- Do not spend the main session's context on bounded exploration whose raw material you will not need after integration.
- Keep local what requires the session's held model — target structure, judgment, final merge. Delegate bounded, self-contained discovery (e.g. "extract document X's concepts against this brief and report where they map") to a sub-agent; receive a compact report; apply the merge yourself mechanically.
- The brief must tell the sub-agent to discover documentation per this skill, not receive a content dump, and to return a structured report with acceptance criteria stated.
- Do not delegate work whose intermediate context is itself the deliverable, or work needing continuous back-and-forth judgment; delegation is lossy and has coordination cost.

## How to discover documentation
This section is agent-specific (tool-dependent), so it lives here rather than in a repository Practice.

**Prefer, in order:**
1. If the current workspace *is* the `GeniusesGroup/memar` repository, use it as the Memar root.
2. Otherwise shallow-clone (or reuse) into the system temporary directory, folder name **`memar`** — same as the repository name. Do not append suffixes like `-repo`.

```bash
# Unix / Git Bash / WSL — MEMAR_ROOT is e.g. /tmp/memar
MEMAR_ROOT="${TMPDIR:-/tmp}/memar"
[ -d "$MEMAR_ROOT/.git" ] || git clone --depth 1 https://github.com/GeniusesGroup/memar.git "$MEMAR_ROOT"
```

```powershell
# Windows PowerShell — MEMAR_ROOT is e.g. C:\Users\...\AppData\Local\Temp\memar
$MEMAR_ROOT = Join-Path $env:TEMP "memar"
if (-not (Test-Path (Join-Path $MEMAR_ROOT ".git"))) {
  git clone --depth 1 https://github.com/GeniusesGroup/memar.git $MEMAR_ROOT
}
```

Prefer `git clone` over the GitHub REST API (unauthenticated API rate-limits quickly; clone does not).

Then read only the needed file(s) with the agent's normal read/search tools — do not dump the whole repo into context. If already cloned earlier in the session, reuse it; do not reclone.

If a referenced file is missing from the clone, say so and ask for it (it may be an unpublished draft) rather than fabricating content.

### Path resolution (agents)
Links in this skill and across Memar documentation use ordinary Markdown / Git path forms (`/docs/...`, `./foo.md`, `../bar.md`, etc.). For an agent, **every such path is relative to the Memar repository root** established above — not to the user's project workspace, not to this skill's directory, and not to the machine filesystem root.

- A root-style path such as `/docs/thinking.md` means `{Memar root}/docs/thinking.md`.
- A relative link inside a document (e.g. `./modeling.md` from `docs/system.md`) resolves against that document's directory **under the Memar root**, as Markdown/Git already imply — still never against the user's other project.

When following hyperlinks between documents, keep resolving under that same Memar tree.

## How to navigate between documents
Do not guess filenames or rely on a memorized list:
1. Start from `README.md` (or the relevant `docs/` entry point) for orientation.
2. Follow each document's hyperlinks when Memar rules require related reading.

This stays valid as new documents are added, unlike a hardcoded index.

You do not need to read every document end-to-end. Use front matter (Title, Status, ID) and the Abstract to judge relevance, then jump to the needed section. Documents share one section structure (Abstract → Introduction → Explanation). Treat nothing before `Status: Final` as settled; detailed semantics live in the project's documentation specification.
