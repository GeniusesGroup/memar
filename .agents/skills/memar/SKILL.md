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

## Three-layer separation
1. **Documentation** — source of truth (concepts, specs, architecture, decisions). Lives in the repository, not in any skill.
2. **Practices** — recommended ways of working with that documentation. Organizational, not agent-specific (`docs/*.practice.md`), not in this skill.
3. **Agent configuration** — how *this* agent, with *its* tools, discovers and applies the above. This skill belongs only here.

## Working rules
- Before reasoning about ideas, architecture, modeling, terminology, or critique, read [**Thinking**](/docs/thinking.md) and follow its discourse norms.
- Never answer from training-data memory when project documentation exists.
- Never invent Memar-specific rules, conventions, or terminology by analogy to mainstream standards of the domain involved (programming frameworks, building codes, organizational norms, etc.). Memar often departs from mainstream on purpose. General domain background is fine; inventing Memar-specific behavior from it is not.
- Treat repository documentation as the canonical source of truth.
- Discover relevant documents from the repository; do not rely on embedded copies or a hardcoded file list.
- Read only the documentation required for the current task.
- Do not read [`docs/protocols/`](/docs/protocols/) wholesale. If a subject there seems needed (e.g. Error), read that folder's [`README.md`](/docs/protocols/README.md) first; list the folder for filenames as the index. When the task only needs to *use* a library that implements a protocol, skip those docs and go to the implementing `memar-{language}` repository (e.g. https://github.com/GeniusesGroup/memar-go/). Open a protocol document only when the contract itself is the subject.
- Do not enumerate unrelated Memar documentation merely because it exists.
- Do not restart discovery on every turn when the relevant knowledge is already in context.
- If the task is unrelated to Memar-specific knowledge, do not discover Memar docs merely because this skill is active.
- If required documentation cannot be found, say so clearly instead of fabricating an answer.
- Canonical repository: https://github.com/GeniusesGroup/memar
- Do not embed copies of project documents inside this skill.

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

You do not need to read every document end-to-end. Use front matter (Title, Status, ID) and the Abstract to judge relevance, then jump to the needed section. Documents share one section structure (Abstract → Introduction → Explanation → Results → Discussion). Treat nothing before `Status: Final` as settled; detailed semantics live in the project's documentation specification.
