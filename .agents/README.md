# Agents
An **agent** is any entity that acts on behalf of another system (person, organization, ...) to carry out a defined set of responsibilities. The concept is much older than artificial intelligence, and is not specific to it: a company's CEO is an agent of its shareholders and board, carrying out duties delegated to them; a lawyer is an agent of their client; a purchasing manager is an agent of their employer. An AI system acting on someone's behalf is one instance of this general relationship, not the definition of it.

Do not assume "agent" in this repository means "AI agent." A human role, an organizational function, or an AI system can all be agents, and content in this directory should be written so it applies to whichever kind of agent is actually reading or carrying out the work, not phrased as if an AI is always the one on the other end.

This file is loaded by [AGENTS.md](../AGENTS.md) at the start of every session in this workspace, so it is a pointer table only — everything operational lives one pointer away.

## What lives here
| Path | Role |
|---|---|
| [`skills/memar/SKILL.md`](skills/memar/SKILL.md) | The Memar practice — how to discover and apply Memar's live documentation, including its bundled scripts. Load it whenever the session's work falls within its description; its description decides, not this file. |
| [`commands.md`](commands.md) | Ready-to-paste commands with their one-line "why" — git history rules and the documentation script invocations. |
| [`installing.md`](installing.md) | Distribution: the plugin manifests, per-tool installation steps, and what the plugin wrapper does and does not buy. Read only when installing or changing distribution. |

For work on this repository's documents, the skill's rules govern; this file adds none of its own.
