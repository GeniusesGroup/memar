# organization — repository instructions

## Memar is the foundation of this repository
This repository is built the Memar way: its cornerstones are Memar's concepts and live documentation. No development work here — design, modeling, implementation, review, or
documentation — may proceed without the Memar skill active. This is not optional guidance; a change made without the Memar mental model is a defect regardless of whether it works.

## Activating the Memar skill
The Memar skill is **not copied into this repository** — a copy would silently rot against upstream. Each session, locate the live Memar repository instead. Its root directory is called **`MEMAR_ROOT`** throughout this document: a documentation placeholder for one resolved path, *not* an OS environment variable.

Resolve `MEMAR_ROOT` to the first of the following that applies. Rules 1–2 find a **developer-owned checkout: use it read-only** — never run git commands inside it; its owner keeps it fresh. Only rule 3's clone belongs to the agent.

1. **Recorded path.** If agent/project memory records a `MEMAR_ROOT` for this machine (typically a working copy ahead of GitHub, because the developer also develops Memar) and the directory exists, use it.
2. **Ask once, then record.** If nothing is recorded, ask the developer whether a local working copy of `GeniusesGroup/memar` exists and where. Record the outcome in this repository's project memory — the path, or the fact that there is none — so later sessions resolve at rule 1 without re-asking.
3. **Agent-owned clone.** If the developer has no local copy, `MEMAR_ROOT` is a persistent shallow clone (`--depth 1`) of `https://github.com/GeniusesGroup/memar` in the system-temporary directory, folder name `memar`. Create it on first use only; if it already exists, refresh it in place with `git pull --depth 1` instead of re-cloning — this is the only checkout where the agent may run git. No timer gates freshness: per-session verification is by design and an incremental fetch of an unchanged repo costs almost nothing, while re-downloading a ~100 MB working tree every session is waste. If offline, use whatever the clone already holds and state that the Memar model may be stale; do not fabricate.

Once resolved, read `{MEMAR_ROOT}/.agents/skills/memar/SKILL.md` and follow it for the rest of the session. Paths written as `/docs/...` inside Memar documents resolve against `{MEMAR_ROOT}`, never against this workspace. If a referenced file is missing there, say so instead of fabricating content.

## No machine-specific paths in committed files
- This file is shared by every developer and agent working on this repository.
- Machine-specific locations (a local Memar working copy path, personal tool settings) belong in agent/project memory or user-scope instruction files — never here.
