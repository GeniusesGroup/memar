# Agents
An **agent** is any entity that acts on behalf of another system (person, organization, ...) to carry out a defined set of responsibilities. The concept is much older than artificial intelligence, and is not specific to it: a company's CEO is an agent of its shareholders and board, carrying out duties delegated to them; a lawyer is an agent of their client; a purchasing manager is an agent of their employer. An AI system acting on someone's behalf is one instance of this general relationship, not the definition of it.

Do not assume "agent" in this repository means "AI agent." A human role, an organizational function, or an AI system can all be agents, and content in this directory should be written so it applies to whichever kind of agent is actually reading or carrying out the work, not phrased as if an AI is always the one on the other end.

## Loading the skill
Whether a session loads [`skills/memar/SKILL.md`](skills/memar/SKILL.md) is decided by that skill's own description, not by this file: when the session's work falls within it — developing a system the Memar way, working on Memar or a Memar-built project, or applying Memar's principles — load the skill at session start and keep it active. For work outside that scope, do not load it.

## Distribution as an agent plugin
This directory is also the root of the Memar plugin, so agent tools can carry Memar's practices into any project — not only sessions that open this repository. The layout:

| Path | Role | Who reads it |
|---|---|---|
| `skills/memar/SKILL.md` | The Memar practice; when a session loads it is decided by its own description — [Loading the skill](#loading-the-skill) | ZCode and OpenCode natively (workspace scope); Claude Code only through the plugin |
| `.claude-plugin/plugin.json` | Plugin manifest | Claude Code; ZCode (second probe path) |
| `.codex-plugin/plugin.json` | Plugin manifest, Codex compatibility | Codex |
| `plugins/marketplace.json` | Marketplace manifest in the generic `.agents` location — the proposed standard | No tool yet; the canonical copy |
| `../.claude-plugin/marketplace.json` | Marketplace manifest at the repository root — the only path Claude Code accepts, and one of the two paths ZCode probes | Claude Code, ZCode |

The two marketplace manifests are byte-identical mirrors. Edit `plugins/marketplace.json` (the canonical copy) and copy it over `../../.claude-plugin/marketplace.json` unchanged. The root mirror exists only because current tools discover marketplaces there; it is retired the moment a tool reads the generic location.

### Installing the Memar plugin
Inside this repository no installation is needed: ZCode and OpenCode discover `.agents/skills/` as workspace scope. Outside it:

- **ZCode** — Settings → Plugin Management → Discover → `+` → add `GeniusesGroup/memar`, then Get on the Memar card. One-time; updates follow the repository.
- **Claude Code** — `/plugin marketplace add GeniusesGroup/memar`, then `/plugin install memar@memar`.
- **OpenCode** — copy `skills/memar/` to `~/.agents/skills/memar/` for global availability.
- **Cursor** — ships Skills and Plugins; verify the current directory layout in Cursor's documentation before relying on it.
