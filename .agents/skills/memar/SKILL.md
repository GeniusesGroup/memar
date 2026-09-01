---
name: memar
description: Memar is a system development framework — a design space that any development can be conducted within, not a project that is itself being built. Use this skill for ANY work conducted the Memar way, not only work on the Memar repository: developing any system (software, hardware, apps, gadgets, buildings, organizations/society) such as a project built with Memar (e.g. the `organization` project), a sub-project of Memar (Khayyam, os, Chapar, Giti/GP, sRPC, GUI, Syllab, Achaemenid), or work applying Memar's principles to something else entirely — even if "Memar" is never mentioned: a request like "write this in Khayyam" or "design this the way Memar does" is enough. It also covers conversations that reason about ideas, architecture, modeling, terminology, critique, or documentation under Memar's approach. This skill holds no project knowledge itself — it only defines how to reliably discover and use Memar's live documentation to have the `Memar` mental model before doing anything.
---

# Memar

## Purpose
This skill defines the operating practices for working with Memar and its sub-projects (Khayyam among them). It intentionally does **not** duplicate project documentation or specifications. Project knowledge always lives in the repository documentation (`/docs/`). This skill only explains how to discover, navigate, and use that knowledge to have the `Memar` mental model.

## Scope: not limited to the Memar repository, and not limited to software
Memar and Khayyam are meant to be *used*, not just maintained. Most people who trigger this skill will be working on **their own, separate thing they're designing or building** — a codebase, a product, a piece of hardware, an organization — and want to apply Memar's approach. They are not editing the `GeniusesGroup/memar` repo itself. Treat `GeniusesGroup/memar` purely as the **reference documentation** to consult (specs, practices, design rationale), while the actual work happens in the person's own project, whatever form it takes. Don't assume the person's project *is* Memar, don't assume it's software, and don't wait for them to mention "Memar" by name — a request like "write this in Khayyam" or "design this the way Memar does" is enough to trigger full use of this skill.

Memar is not a passive reference library, however — it is the **framework the development is conducted within**. When a project is developed the Memar way, Memar's principles, definitions, and practices participate in every stage of that development, not only where Memar is explicitly invoked: development of a project such as `organization` is not meaningfully possible without Memar's involvement, because its modeling, terminology, documentation, and critique practices *are* Memar's. This skill therefore stays active for the whole life of such a project — architecture, modeling, implementation, review, and documentation conversations alike — rather than being consulted once at the start.

## Three-layer separation
When working with Memar, keep these responsibilities separate:

1. **Documentation** — the source of truth. Defines concepts, specifications, architecture, and decisions. Lives in the repository, not in any skill.
2. **Practices** — recommended ways of working with the documentation. Organizational knowledge, not agent-specific; may be followed by humans, IDEs, automation tools, AI systems, or any other agent. Also lives in the repository (e.g. `docs/*.practice.md`), not in this skill.
3. **Agent configuration** — how *this* agent, with *its* specific tools, discovers and applies the above. This skill belongs to this layer, and only this layer.

## Working rules
- Before reasoning about ideas, architecture, modeling, terminology, or critique — in this repository or in any project using Memar's approach — read [Thinking](../../../docs/thinking.md) and follow its discourse norms.
- Never answer from training-data memory when project documentation exists.
- Never invent Memar-specific rules, conventions, or terminology by analogy to mainstream standards of whatever domain is involved — mainstream programming languages/frameworks if the work is software, but equally typical building codes, organizational structures, or social conventions if it isn't. Memar frequently departs from mainstream conventions on purpose. (General background knowledge of the relevant domain is fine for context; what's off-limits is inventing Memar-specific behavior from it.)
- Treat the repository documentation as canonical source of truth.
- Discover relevant documents from the repository instead of relying on embedded copies or a hardcoded file list — the file set changes independently of this skill.
- Read only the documentation required for the current task.
- Do not enumerate, rediscover, or inspect unrelated Memar documentation merely because it exists.
- Do not restart Memar documentation discovery on every interaction when the relevant knowledge is already available in the current context or persistent project context.
- If a task is unrelated to Memar-specific knowledge, do not perform additional Memar documentation discovery merely because this skill is active.
- If required documentation cannot be found, state that clearly instead of fabricating an answer.
- Canonical repository is https://github.com/GeniusesGroup/memar
- Use the current repository contents whenever precision matters. Do not embed copies of project documents inside this skill. Documentation evolves independently and should remain the single source of truth.

## How to discover documentation
This part is inherently agent-specific — it depends on which tools are actually available — so it lives here rather than in a repository-level Practice document.

Shallow-clone the repo rather than hitting the GitHub REST API: the API is unauthenticated and shared across many users, so it rate-limits quickly, while `git clone` does not.

```bash
[ -d /tmp/memar-repo/.git ] || git clone --depth 1 https://github.com/GeniusesGroup/memar.git /tmp/memar-repo
```

Then read only the specific file(s) needed with `view`/`grep` — don't dump the whole repo into context. If already cloned earlier in this session, reuse it; don't reclone.

If a referenced file isn't found in the clone, say so plainly and ask for it directly (it may be an unpublished draft) rather than fabricating its content.

## How to navigate between documents
Don't guess filenames or rely on a memorized list of what exists — instead:
1. Start from `README.md` (or the relevant `docs/` entry point) for orientation.
2. Follow each document's hyperlink to move through related documents if it is necessary by memar rules.

This convention doesn't go stale as new documents are added, unlike a hardcoded index, so it's safe to rely on permanently.
