# Memar Changelog

## Changelog
### A session reaches the Memar skill from AGENTS.md alone; Memar's preferences move to the project's manifest
- Time: 2026-10-19T20:00:00Z
- Type: Changed, removed
- Cited:
  - Owner (2026-10-19, in chat) - Relation: Evidence: AGENTS.md is sent with the prompt, yet it only pointed at `.agents/memar/README.md`, which cost every session a tool call and said nothing more; AGENTS.md says itself what a session loads, and what else is needed is added there, not to a file in between. The preferences file is read by the `memar` command, not by models, so it is not among the files agents are pointed at, and Markdown is the wrong form for it. The projects that use Memar are changed the same way.
  - Task 20261014-T113227Z-24288 - Relation: Evidence: the owner's request of 2026-10-14 that a project's preferences live once in its `manifest.yaml`, Memar's own keys under a key of Memar's.
  - Owner (2026-10-22, in chat) - Relation: Evidence: the note Not every idea belongs in Memar, which stood in the removed preferences file, has lost its meaning and is not kept anywhere.
- Propagates to:
  - `bundles/memar/services/install/services/project.py`: Done — writes only the `## Memar` section of AGENTS.md; the Memar repository's section links its own skill file; an earlier install's `.agents/memar/README.md` goes to the trash, and a `.agents/memar/preferences.md` is named as no longer read and left
  - `bundles/memar/services/install/services/apps.py`: Done — the skill pointer in each agent app names the checkout's `SKILL.md` by its path on the machine, so the skill is one read away
  - `modules/process/project/services/preferences.py`: Done — reads the `memar:` block of the project's `manifest.yaml`; install writes no preferences file and no manifest
  - The `memar` and `organization` repositories: Done — `memar install` rewrote their AGENTS.md and trashed their `.agents/memar/README.md`; Memar's `.agents/memar/preferences.md`, whose keys were all empty, was trashed
  - `modules/knowledge/content/rules/normative_references/normative_references.md`, `modules/knowledge/documentation/handoff/handoff.handoff.md`, `docs/comparisons/context-mode.001.md`, `docs/framework.handoff.md`: Done — they name the manifest block, or the removed file's last version where an essay cites it
  - Task 20261017-T162520Z-13368: Done — closed without work by the owner's ruling of 2026-10-22
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [Claude](../../CONTRIBUTORS.md#claude) (Opus 5.5) — carried, recorded

#### What changed
A session in a project that uses Memar read AGENTS.md (sent with the prompt), then `.agents/memar/README.md` (a tool call), then ran `memar content path` (another), then read the skill. AGENTS.md now says what the README said; in the Memar repository it links the skill file. The bootstrap commands are not copied into AGENTS.md: it is paid on every prompt, and only a machine without `memar` needs them.

What a project tells Memar's tools (`sessions`, `records`, `most-characters`, `normative_references`) is a `memar:` block of indented `key: value` lines in the project's `manifest.yaml`, read without a YAML library; the manifest's other keys are not read. Absent, every key is Memar's default.

#### Considered and not done
- A `.agents/memar/preferences.json` or `.toml`: not done, because the owner had already named the project's manifest as the one place for its preferences.
- Writing an empty `memar:` block into a project's manifest on install: not done, because the manifest is the project's and an absent block already means the defaults.
