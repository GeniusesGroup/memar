---
name: memar
description: Operating practices for any work conducted the Memar way — not only work inside the GeniusesGroup/memar repository. Use when developing any system (software, hardware, apps, gadgets, buildings, organizations/society) with Memar; when working on a Memar-built project (e.g. `organization`); a Memar sub-project (Khayyam, os, Chapar, Giti/GP, sRPC, GUI, Syllab, Achaemenid); or when applying Memar's principles even if "Memar" is never named — e.g. "write this in Khayyam" or "design this the way Memar does". Also covers reasoning about ideas, architecture, modeling, terminology, critique, or documentation under Memar's approach. This skill holds no project knowledge; it only defines how to discover and use Memar's live documentation to hold the Memar mental model before acting.
---

# Memar
This file holds only what depends on the agent's runtime. Memar's knowledge is in its documents, and how each tool is used and why is in its `--help`; neither is repeated here. Nothing here is complete, so what this file does not say is not therefore absent from Memar: look it up. Where this file and a document or a `--help` disagree, they win, and the disagreement is reported.

## Scope
Memar is the framework the work is conducted within ([Framework](/docs/framework.md)), not a library to consult. The work is usually the person's own project — not necessarily software — and [GeniusesGroup/memar](https://github.com/GeniusesGroup/memar) is its reference; do not assume the project is Memar. "Write this in Khayyam" engages this skill without the word Memar.

## Finding things
- Start at `memar --help`, then `memar <verb> --help`. `memar content` reaches all of Memar's written content, not only `docs/`; prefer it to resolving links by hand or reading whole documents.
- Without the command, in a checkout: `python $MEMAR_ROOT/.agents/scripts/memar-content.py --help`. With no checkout, fetch the bootstrap — [install.sh](https://raw.githubusercontent.com/GeniusesGroup/memar/main/.agents/scripts/install.sh) on POSIX, [install.ps1](https://raw.githubusercontent.com/GeniusesGroup/memar/main/.agents/scripts/install.ps1) on Windows — and run it with `--help` (`-Help` for install.ps1). It installs Python too; a hand-made recipe in place of a script is not the fallback.
- `/docs/...` links here resolve in a checkout or through `memar content`, never beside this copy.

## Each subject through its document
No work on one of these subjects without its document; each leads to its own Practice. This is the foundation, not the whole: [the documentation index](/docs/README.md) has the rest.
- Thinking, reasoning, critique: [Cognition](/docs/cognition.md)
- Terms and definitions: [Terminology](/docs/terminology.md)
- Systems: [System](/docs/system.md)
- Modeling: [Modeling](/docs/modeling.md)
- Types: [Type](/docs/type.md)
- Modules, their boundaries and dependencies: [Modularity](/docs/modularity.md) and [Modules](/docs/modules/README.md)
- What a module promises another: [Protocol](/docs/protocol.md)
- Processes: [Process](/docs/process.md)
- Rules: [Rule](/docs/rule.md)
- Development and testing: [Test](/docs/modules/process/test.md)
- Documentation: [Documentation](/docs/documentation.md)
- Working with other agents: [Agency](/docs/agency.md)

## Runtime rules
- Begin with `memar session new` and keep scratch, the plan included, in the folder it prints; nowhere else, and never the OS temporary directory.
- After any compaction or summary of the context, re-read this file: a summary drops rules that still bind.
- Do not take an act that cannot be undone. Text reaches a file through a file-write tool or `memar content`, never a shell's own text handling. Deleting, moving, restoring, and committing go through [`host/fs.py`](/.agents/scripts/host/fs.py) and [`host/git.py`](/.agents/scripts/host/git.py), never the host's own command or one a runtime may rewrite into it; if they are not at hand, stop and say so.
- Intake binds before work ([Cognition Practice](/docs/cognition.practice.md#norm-application-points)) and ends in a written plan, made before reading the material the work is about, that marks each step local or delegated; a step the plan did not foresee takes the same test before it starts.
- Delegate a step, with its acceptance check, when it would read more than three files, take in any one file, diff, or output over about 20 KB — measure before reading — or rerun a script until it comes out clean; keep only the report. Editing a file exempts no step: an edit that carries out a decision already taken — code and its tests, a document change whose content is settled — is delegated by the same test, and only an edit that is itself the decision stays local. The sections linked here and the passages a report cites, read at the cited lines, do not count. A step that crosses the line midway is delegated from there. Keep local the target's structure — built from reports, not from a survey — the decisions over findings, and the merge; judgment exercised while producing a finding is delegable with its criteria, so calling a step judgment never keeps it local. Do not delegate work whose intermediate context is the deliverable, or work that needs the session's decision between its steps; where such work exceeds the size test, split it at those decisions and delegate the parts between. What a delegation must establish: [Interaction With an Agent](/docs/agency.md#interaction-with-an-agent).
- The session's context is a budget as well as each step's: tool output, reports, and the conversation accumulate across steps that each passed the test. Ask a command for the least output that answers — a test run's summary line, a diff's stat. Once the context is past about half the window, as the runtime reports it or as estimated from what was taken in, take no further step locally: delegate it, or hand the open sections of the plan to a new session.
- Every sub-agent loads this skill first; a read-only step enacts no development step and commits to no module, so it reads only what its step needs. Its brief names this file, the paths and passages to judge, the criteria, the acceptance check, and the report shape, and restates no rule; the sub-agent declares unverified reading and context limits per [What Implementation Asymmetry Obliges](/docs/cognition.md#what-implementation-asymmetry-obliges). Start a new sub-agent rather than resume a long one.
- Each pass, local or delegated, has a finite boundary, the same acceptance check, and a named stop: success, clean no-op, blocked, approval-required, exhausted, no progress. Errors and exhausted budgets are never reported as success ([Acceptance Criteria](/docs/agency.md#acceptance-criteria)).
- A critique or approval is asked per [recording an approval](/docs/documentation-changelog.practice.md#recording-an-approval); in this runtime the reviewer is a new sub-agent, preferably another model ([choosing who reviews](/docs/documentation-changelog.practice.md#choosing-who-reviews)).
- Close by type per [Handoff Practice](/docs/documentation-handoff.practice.md), and keep each delegation's report in the session folder for the [debrief](/docs/cognition.practice.md#debriefing-runs).
