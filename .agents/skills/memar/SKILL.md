---
name: memar
description: Operating practices for any work conducted the Memar way — not only work inside the GeniusesGroup/memar repository. Use when developing any system (software, hardware, apps, gadgets, buildings, organizations/society) with Memar; when working on a Memar-built project (e.g. `organization`); a Memar sub-project (Khayyam, os, Chapar, Giti/GP, sRPC, GUI, Syllab, Achaemenid); or when applying Memar's principles even if "Memar" is never named — e.g. "write this in Khayyam" or "design this the way Memar does". Also covers reasoning about ideas, architecture, modeling, terminology, critique, or documentation under Memar's approach. This skill holds no project knowledge; it only defines how to discover and use Memar's live documentation to hold the Memar mental model before acting.
---
# Memar
This file holds only what is the agent's own: how an agent's runtime — its context window, its sub-agents, its tools — carries out work the Memar way. Memar's knowledge is in its documents; how tools are used is declared by `memar` and the tools it leads to; Memar's rules are delivered by a service. None of those are listed or cached here. This file is not complete: what it does not say may still be in Memar, so look it up. Where this file disagrees with a document or with `memar`, the document or `memar` wins, and the disagreement is reported.

## Scope
Memar is the framework the work is conducted within ([Framework](/modules/knowledge/framework/framework.md)), not a library to consult. The work is usually the person's own project — not necessarily software — and [GeniusesGroup/memar](https://github.com/GeniusesGroup/memar) is its reference; do not assume the project is Memar. "Write this in Khayyam" engages this skill without the word Memar.

## Reaching Memar
Memar is reached by one of two routes.

- **The `memar` command, or its MCP tool.** Where the runtime lists Memar's MCP tools, call the tool of a command and do not run that command in a shell: a tool's description is the command's `--help`, and a call through the tools is not given the command card again. A chat that needs a command and has not yet seen the list runs `memar commands` once (or the tools catalog). Take each named thing's interface from that command's `--help` or its tool description **each time it is used**, not from memory and not from this file. Find and read content the ways those commands offer. Resolve a link in this file that begins with `/` the way they offer, never into the folder this copy sits in nor into the project being worked on.
- Before deleting, moving, restoring, or committing files, call the tool of the verb that does it and read its help; the same for `memar fs`, whose bundle is [`bundles/memar_fs/`](/bundles/memar_fs/memar_fs.md); for putting text in a file, use a file-write tool or `memar content write`/`edit` (never shell text handling).
- **Where `memar` is absent**, read those same files' opening comments and `--help` ([GitHub: paths under GeniusesGroup/memar](https://github.com/GeniusesGroup/memar)). If they cannot supply what the work needs, stop and say so.

## Fetch before each step
Do not cache in this file — or in the chat as lasting instruction — the argv, kinds, or answer text of Memar's delivery commands. Their live help and output are the source.

- **Take up a task** with `memar ai get-task-init-context` (with `--without-skill` when this file is already loaded). Run it first, once; read every part it prints before acting on the plan. It composes what the plan's act needs, including the passages Normative References name for that act.
- **Before every step**, call `memar ai get-rules-for-subject` with a **precise subject**: the act of this moment in words (what is about to be done), not a vague topic. Open the hits that govern the step and follow them; a listing is not following. When the step changes, call it again with the new subject.
- **When the act's kind changes** mid-work (or after compaction — below), fetch the passages that kind requires through the command that prints them for an act kind — the same family init-context already used. Take its words from `--help` or the tool description; do not replay a recipe from this file. A question answered in chat with no task still fetches that way for the act it is. Thinking runs in every step and is not named as a separate act: every kind's lists still print their passages.
- **A subject is not a kind.** Find its governing documents by searching (`memar content search`, `memar content find` — find is informative only and binds nobody). Read the governing section the search surfaces for the step; follow its links where the act depends on them. A subject that enters midway is consulted when it enters. Where search matches nothing, proceed as Cognition Practice says for a lookup that matches nothing — find that passage by search, do not cache its path here.
- Read each as [Reading documentation](/modules-plugable/knowledge/documentation/documentation.md#reading-documentation) says, and act from the section that governs the act — not from memory, from training, or from this file. Where a passage links a Practice for the act, do the act as that Practice says. A proposal that departs from a passage cites it.

## Task and plan
Work is conducted as a task on Memar's records; the task is the unit that outlives the chat. How a task is opened, planned, handed on and ended is in the rules the service delivers and in what `memar task ensure` prints.

## Context window and compaction
- After any compaction or summary of the context — announced or not; a context that opens with a summary has been compacted — re-read this file and the task's plan, and fetch again the current act's passages **without** treating earlier prints as still verified: a summary drops rules and decisions that still bind. What was read before a compaction and not since is unverified reading ([What Implementation Asymmetry Obliges](/modules/knowledge/cognition/cognition.md#what-implementation-asymmetry-obliges)).
- The chat's context is a budget as well as each step's: ask a command for the least output that answers.
- A prompt cache reuses only an unchanged prefix, and it lasts about an hour. So this skill, the context a kind printed, and the plan stay unchanged within a chat; a new chat, or a changed prefix, pays the whole context again.
