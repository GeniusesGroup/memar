# Installing the Memar skill / plugin
Everything in this file serves one question: how does a tool get `skills/memar/` loaded? Read it when installing or when changing distribution; sessions doing Memar work never need it.

## Inside this repository
No installation. Cursor, ZCode, and OpenCode discover `.agents/skills/` as workspace scope; Claude Code sessions get the practice through [AGENTS.md](../AGENTS.md) → [.agents/README.md](README.md) → the skill pointer.

## Directory inventory (distribution-only content)
Nothing below affects a working session; it exists so distribution changes can be made without reverse-engineering the layout.

| Path | Role |
|---|---|
| `skills/memar/` | The plugin's payload — SKILL.md plus the bundled scripts; the only part that matters at session time. |
| `skills/README.md` | Why the directory carries the ecosystem name `skills` and what the project calls it conceptually (`Content → Practice → Skill`). |
| `.claude-plugin/plugin.json` | Claude Code's plugin manifest at the plugin root (`.agents/`). |
| `.cursor-plugin/plugin.json` | Cursor's plugin manifest at the same plugin root. |
| `.codex-plugin/plugin.json` | Codex's plugin manifest at the same plugin root. |
| `plugins/marketplace.json` | Canonical Claude/ZCode marketplace manifest. **Not read by Cursor.** |
| `.claude-plugin/marketplace.json` *(repository root)* | Byte-identical mirror of `plugins/marketplace.json` — Claude Code's only marketplace discovery path (ZCode probes it too). |
| `.cursor-plugin/marketplace.json` *(repository root)* | Cursor's marketplace discovery path. Cursor does not read `plugins/`; this root file is the only Cursor marketplace copy. |

## Outside this repository
- **ZCode** — Settings → Plugin Management → Discover → `+` → add `GeniusesGroup/memar`, then Get on the Memar card. One-time; updates follow the repository.
- **Claude Code** — `/plugin marketplace add GeniusesGroup/memar`, then `/plugin install memar@memar`.
- **Cursor** — Dashboard → Plugins → Team Marketplaces → Add Marketplace → Import from Repo → `GeniusesGroup/memar`, then install the Memar plugin (or Customize → add the marketplace and install). One-time; refresh tracks the repository. Fallback without marketplace: copy `skills/memar/` to `~/.agents/skills/memar/` (or `~/.cursor/skills/memar/` for Cloud Agent sync via Settings → Agents → Sync Skills).
- **OpenCode** — copy `skills/memar/` to `~/.agents/skills/memar/` for global availability.

Documentation still comes from a full Memar checkout via the bundled `memar-root.py`, not from the skill folder alone. Prefer a local clone (workspace, `$MEMAR_ROOT`, or a sibling folder named `memar`) over a temp clone when developing Memar alongside another project.

## Why the manifests sit where they sit
The manifests are positional requirements of the tools that read them — not a claim that this layout is right.

**Claude Code / ZCode** (verified against their docs):

- `.claude-plugin/marketplace.json` **at the repository root** — their only marketplace probe; and
- `.claude-plugin/plugin.json` **at the plugin root** — here `.agents/` itself.

Edit `plugins/marketplace.json` and copy it over `../../.claude-plugin/marketplace.json` unchanged.

**Cursor** (verified against Cursor's plugin reference):

- `.cursor-plugin/marketplace.json` **at the repository root** — Cursor's only marketplace probe; Cursor does **not** read `.agents/plugins/`; and
- `.cursor-plugin/plugin.json` **at the plugin root** (`.agents/.cursor-plugin/plugin.json`).

There is no second Cursor marketplace under `plugins/` — that path is Claude/ZCode-only. The root `.cursor-plugin/marketplace.json` is edited in place.

Codex's manifest sits at `.codex-plugin/plugin.json` for Codex compatibility.

## What being a plugin actually buys
Be clear-eyed about this, because the plugin wrapper earns less than it appears to. A Memar session needs the Memar repository regardless — the skill holds no documentation; the docs live in `docs/` of a full clone. The plugin's real benefits:

1. **Distribution and updates** — marketplace install clones once and marketplace refresh tracks the repository; without it, every tool needs a manual copy.
2. **Skill discovery** — without the plugin, a session in *another* project only sees the skill if a human points at the path (AGENTS.md does this inside this repository; marketplace install does it elsewhere).
3. **Namespaced invocation / clean uninstall** — where the host tool supports it.

What it does **not** do: carry the documentation. The bundled `scripts/` resolve that gap at session time (`memar-root.py` clones or reuses), which is why the plugin remains worthwhile even though the clone still happens — the alternative, shipping doc copies inside the skill, violates the project's one-authoritative-source rule and would go stale.

## What marketplace and plugin are not
Host tools invent **marketplace** and **plugin** as their install vocabulary. Memar pays that tax so a session outside this repository can *discover* the single Memar practice. That is not how Memar models its own knowledge.

- A marketplace card is not a mental model.
- A plugin is not a partition of Memar into optional products.
- Multiple plugins each shipping multiple skills is not how Memar is structured — and must not become the aspiration. Memar carries **one continuous mental model** in `docs/` (plus language implementations of its contracts). The skill folder is a **navigation practice** into that model, not a second copy of it and not a menu of peer frameworks ([Knowledge → A project carries one continuous mental model](../docs/knowledge.md#a-project-carries-one-continuous-mental-model)).
- Failed shape: shipping Khayyam or Cognition as separate skills beside Memar. A fragment without the rest has no coherent practice; those concerns live as documents inside the shared medium.

If a future host tool required a different adapter filename, that would be another distribution detail — not a reason to redesign Memar as a plugin catalog.
