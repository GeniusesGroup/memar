---
name: memar
description: Operating practices for any work conducted the Memar way — not only work inside the GeniusesGroup/memar repository. Use when developing any system (software, hardware, apps, gadgets, buildings, organizations/society) with Memar; when working on a Memar-built project (e.g. `organization`); a Memar sub-project (Khayyam, os, Chapar, Giti/GP, sRPC, GUI, Syllab, Achaemenid); or when applying Memar's principles even if "Memar" is never named — e.g. "write this in Khayyam" or "design this the way Memar does". Also covers reasoning about ideas, architecture, modeling, terminology, critique, or documentation under Memar's approach. This skill holds no project knowledge; it only defines how to discover and use Memar's live documentation to hold the Memar mental model before acting.
---

# Memar
This file holds only what is the agent's own: how an agent's runtime — its context window, its sub-agents, its tools — carries out work the Memar way. Memar's knowledge is in its documents, and how its tools are used is declared by `memar` and the tools it leads to; neither is repeated here. Nothing here is complete, so what this file does not say is not therefore absent from Memar: look it up. Where this file disagrees with a document or with `memar`, the document or `memar` wins, and the disagreement is reported.

## Scope
Memar is the framework the work is conducted within ([Framework](/docs/framework.md)), not a library to consult. The work is usually the person's own project — not necessarily software — and [GeniusesGroup/memar](https://github.com/GeniusesGroup/memar) is its reference; do not assume the project is Memar. "Write this in Khayyam" engages this skill without the word Memar.

## Reaching Memar Server
Memar is reached by one of two routes.

- **The `memar` command.** Start at `memar --help` and follow what it says: it leads to opening the session, to finding, reading, and writing Memar's content, and to resolving a reference. Take the interface of each thing it names from that thing each time it is used, rather than recalling it from this file, from training, or from an earlier session. Find and read content the ways it offers, in preference to resolving links by hand or reading whole documents. Resolve a link in this file that begins with `/` the way it offers, never into the folder this copy sits in nor into the project being worked on.
- **Where `memar` is absent**, read [Scripts](https://github.com/GeniusesGroup/memar/blob/main/.agents/scripts/README.md) and decide from it. If it cannot supply what the work needs, stop and say so.

## Consult the governing document before each act
- Before a step names, defines, models, divides, specifies, implements, tests, documents, critiques, or delegates anything, find the document that governs the subject of that step and the one that governs the act itself — implementing, testing, modeling, documenting — and read the part of each that governs the step; the act's own document says what has to come before it. The trigger is the step, not the session: a subject that enters the work midway is consulted when it enters, and a document read for one act is read again at the section that governs the next.
- Find each by searching Memar's content for the subject's term and for the act's; follow their links to the documents they rest on where the act depends on them.
- Read each as [Reading guidance](/docs/README.md#reading-guidance) says, and act from the section that governs the act — not from memory, from training, or from this file. Where it links a Practice for the act, do the act as that Practice says.
- Where the search finds nothing, proceed as [Cognition Practice → Norm Application Points](/docs/cognition.practice.md#norm-application-points) says for a lookup that matches nothing.

## Session and plan
- Before any other work, open a session through Memar ([Reaching Memar Server](#reaching-memar-server)) — or, when your brief hands you one, take that one up and open none — and keep all scratch in its folder; nowhere else — not the OS temporary directory, and not a scratch place the runtime offers.
- One session holds one task, and its plan holds that task's own acceptance check; a further task — another request, or one delegated — gets a session of its own, linked to the session it came from.
- A runtime's own to-do list or plan mode may track steps inside this context, but it is not the session's plan: it ends with the context, and the plan has to outlive it.
- Thinking runs in every step, and no step names it as its act: once the session is open or taken up — a sub-agent's too — and before acting on or adding to its plan, read [Cognition](/docs/cognition.md)'s [Abstract](/docs/cognition.md#abstract), [What Implementation Asymmetry Obliges](/docs/cognition.md#what-implementation-asymmetry-obliges), and [Discourse Norms](/docs/cognition.md#discourse-norms-derived-from-this-model) — about 19 KB — in this context, not as a delegate's summary, and hold them for the session, as [Status and Use](/docs/cognition.md#status-and-use) says.
- Intake binds before work ([Cognition Practice → Norm Application Points](/docs/cognition.practice.md#norm-application-points)) and ends in the written plan, made before reading the material the work is about. Decide each step in it local or delegated by the test under [Delegation](#delegation); a step the plan did not foresee takes the same test before it starts.

## Context window and compaction
- After any compaction or summary of the context — announced or not; a context that opens with a summary has been compacted — re-read this file, the session's plan, and Cognition's sections named under [Session and plan](#session-and-plan): a summary drops rules and decisions that still bind. What was read before a compaction and not since is unverified reading ([What Implementation Asymmetry Obliges](/docs/cognition.md#what-implementation-asymmetry-obliges)).
- The session's context is a budget as well as each step's: tool output, reports, and the conversation accumulate across steps that each passed the test. Ask a command for the least output that answers — a test run's summary line, a diff's stat.
- Once the context is past about half the window, as the runtime reports it or as estimated from what was taken in, take no further step locally: delegate it, or hand what remains of this session's task to a new session linked to this one.

## Delegation
- Delegate a step, with its acceptance check, when it would read more than three files, take in any one file, diff, or output over about 20 KB — measure before reading — or rerun a script until it comes out clean; keep only the report. The sections this file links and the passages a report cites, read at the cited lines, do not count. A step that crosses the line midway is delegated from there.
- A sub-agent is used when that test calls for one, or when tasks run in parallel; a delegated task's sub-agent works in a session of its own, linked to the delegating one.
- Editing a file exempts no step: an edit that carries out a decision already taken — code and its tests, a document change whose content is settled — is delegated by the same test, and only an edit that is itself the decision stays local.
- Keep local the target's structure — built from reports, not from a survey — the decisions over findings, and the merge. Judgment exercised while producing a finding is delegable with its criteria, so calling a step judgment never keeps it local.
- Do not delegate work whose intermediate context is the deliverable, or work that needs the session's decision between its steps; where such work exceeds the size test, split it at those decisions and delegate the parts between.
- A tangent the session will not otherwise need is not a step to delegate; it is handled per [Mid-session tangents](/docs/documentation-handoff.practice.md#mid-session-tangents).
- What a delegation must establish: [Interaction With an Agent](/docs/agency.md#interaction-with-an-agent).

## Sub-agents, briefs, and reports
- Every sub-agent loads this skill first. A read-only step enacts no development step and commits to no module, so it looks up no document for an act it does not take, and beyond Cognition's sections named under [Session and plan](#session-and-plan) reads only what its step needs.
- A sub-agent starts with none of the session's context: what its session's plan does not carry, it does not know. The delegating session opens the sub-agent's session itself, linked to its own, and writes the whole task into that session's plan.md — the paths and passages to judge, the criteria, the acceptance check, and the report shape, restating no rule — then hands the sub-agent only the brief that opening the session prints, the same text for every sub-agent. The task is stated once, in the delegator's words; the sub-agent does not rewrite the plan's Request, and its report.md is read against the plan's check. The sub-agent declares unverified reading and context limits per [What Implementation Asymmetry Obliges](/docs/cognition.md#what-implementation-asymmetry-obliges).
- Start a new sub-agent rather than resume a long one.
- Sub-agents running at the same time write disjoint files, or write a shared one only through Memar's writing tool.
- A report is a claim: read the passages it cites at the cited lines before building on it ([Treat shared artifacts as claims](/docs/cognition.md#treat-shared-artifacts-as-claims-under-the-same-evaluation-not-as-absolute-authority)). Keep each report in the session folder for the [debrief](/docs/cognition.practice.md#debriefing-runs).
- Each pass, local or delegated, has a finite boundary, the same acceptance check, and a named stop: success, clean no-op, blocked, approval-required, exhausted, no progress. Errors and exhausted budgets are never reported as success ([Acceptance Criteria](/docs/agency.md#acceptance-criteria)).

## Reviewers
- Ask for a critique or approval as [recording an approval](/docs/documentation-changelog.practice.md#recording-an-approval) says. In this runtime the reviewer is a newly started sub-agent that has not seen the work — never the session itself, nor a sub-agent resumed from the work — preferably on a different model from the session's where the runtime offers one ([choosing who reviews](/docs/documentation-changelog.practice.md#choosing-who-reviews)).

## Asking the human
- Ask as [Cognition Practice → Norm Application Points](/docs/cognition.practice.md#norm-application-points) says — what to settle first, and the shape of the question; an act beyond the instance is confirmed first ([Confirm before large-scope changes](/docs/cognition.md#confirm-before-large-scope-changes)).
- When the runtime's sandbox or permissions refuse a command, report the refusal or ask for the permission; do not reach the same act by another route.
- A sub-agent has no human to ask: what it would ask, it ends on as blocked or approval-required, with the question stated, and the session that delegated it asks.

## Closing
- Before ending work on a task — finished or not — write its session's report and set its plan's Status to agree, as `memar session --help` says: a session left `open` after its check passed reads to every later session as work still owed.
- Close by type per [Handoff Practice](/docs/documentation-handoff.practice.md), each durable result in the home [Results routing](/docs/documentation.md#results-routing) gives it.
