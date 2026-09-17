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
- Before reasoning about ideas, architecture, modeling, terminology, or critique, read [**Cognition**](/docs/cognition.md) and follow its discourse norms.
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
- When a request is ambiguous in intent, scope, or acceptance criteria, ask immediately — do not guess or over-derive to resolve it. Apply Cognition's *Ask rather than assume* norm at intake, not only during reasoning.
- When a change is large-scope — a definition other documents reference, a restructure of a document or the document set, or edits spanning several files — present the plan (the proposed text and the list of touched files) and obtain the user's explicit approval before applying; after applying, hold the result open for the user's review and apply their feedback. Apply Cognition's *Confirm before large-scope changes* norm at intake, not only during reasoning.
- When a request opens a development thread unrelated to the current session's purpose, do not execute it in this session's context — follow [Handoff Practice → Mid-session tangents](/docs/documentation-handoff.practice.md#mid-session-tangents).
- Canonical repository: https://github.com/GeniusesGroup/memar
- Do not embed copies of project documents inside this skill.

## Session economy with sub-agents
This section is agent-specific (tool-dependent), so it lives here rather than in a repository Practice. When the runtime supports sub-agents:

- Do not spend the main session's context on bounded exploration whose raw material you will not need after integration.
- Keep local what requires the session's held model — target structure, judgment, final merge. Delegate bounded, self-contained discovery (e.g. "extract document X's concepts against this brief and report where they map") to a sub-agent; receive a report sized to what that delegated work needs; apply the merge yourself mechanically.
- The brief must tell the sub-agent to discover documentation per this skill, not receive a content dump, and to return a structured report with acceptance criteria stated.
- Do not delegate work whose intermediate context is itself the deliverable, or work needing continuous back-and-forth judgment; delegation is lossy and has coordination cost.
- Prefer a **new** sub-agent with a short brief (paths + the passages it must judge) over **resuming** a long prior sub-agent thread: resume replays that thread's history into the bill again. Prefer a smaller model when the job is a second opinion, not primary drafting. Do not open whole base documents when the needed sections can be named by path and anchor.

## Documentation navigation
Two standard-library Python scripts ship beside this file ([`scripts/`](scripts/)); they are the navigation mechanism. Invoke them; do not re-derive their logic or read them for usage — each documents itself via `--help`. Every path in Memar documentation is relative to the **Memar repository root**, never to the user's workspace, this skill's directory, or the filesystem root.

1. Root: if the workspace *is* `GeniusesGroup/memar`, that is the root. Otherwise `memar-root.py` resolves it (shallow-clones if missing) and prints the path — use that as `$MEMAR_ROOT` for the session; do not re-resolve after the first run.
2. Relevance: `memar-doc.py meta FILE` prints a document's front matter + Abstract — judge from that before opening anything whole.
3. Reading: `memar-doc.py section FILE HEADING` extracts exactly the needed section; follow documents' own hyperlinks (resolve via `memar-doc.py path REF --from FILE`) when Memar rules require related reading.
4. Finding: `memar-doc.py search PATTERN...` searches full-text across the doc set — filenames are slugs, not a taxonomy, so never guess by filename. A `Status` earlier than `Final` means unsettled; section structure is uniformly Abstract → Introduction → Explanation.

```bash
MEMAR_ROOT="$(python "$SKILL_DIR/scripts/memar-root.py")"     # once per session ($SKILL_DIR = this file's directory)
python "$SKILL_DIR/scripts/memar-doc.py" meta docs/framework.md   # judge relevance cheaply
python "$SKILL_DIR/scripts/memar-doc.py" section docs/framework.md "Goal-Oriented Frameworks and Purpose Space"
python "$SKILL_DIR/scripts/memar-doc.py" search "polymorphism"    # full-text, not filename
```

On Git Bash/MSYS shells, pass bare names (`docs/cognition.md`), not leading-`/` paths — MSYS rewrites the latter into Windows paths before the script sees them.

Only if the runtime has no Python: read the scripts' source (short, dependency-free, self-documenting) and reproduce the needed step with the tools available — first execution by Python's own agency, then source-reading, and only then a bare `git clone --depth 1` of https://github.com/GeniusesGroup/memar.git into a temp dir, reusing any existing checkout. A referenced file missing from the root is reported, not guessed at — it may be an unpublished draft.
