# Task Research 002 — Task and content for readers with a bounded context: what outside work says, and where the organization's model agrees or does not

## Table of Contents
- [Status](#status)
- [Question and Goals](#question-and-goals)
- [Participants](#participants)
- [Methodology](#methodology)
- [Findings](#findings)
  - [1. What the source-control article says, and what it does not](#1-what-the-source-control-article-says-and-what-it-does-not)
  - [2. What the context-engineering sources say](#2-what-the-context-engineering-sources-say)
  - [3. Many participants, one task: share or partition](#3-many-participants-one-task-share-or-partition)
  - [4. How a context cache constrains the model](#4-how-a-context-cache-constrains-the-model)
  - [5. Where the organization's model agrees](#5-where-the-organizations-model-agrees)
  - [6. Where it does not, or says nothing](#6-where-it-does-not-or-says-nothing)
  - [7. Proposals](#7-proposals)
- [Open Questions](#open-questions)
- [Addendum — independent review by a stronger model (2026-10-18)](#addendum--independent-review-by-a-stronger-model-2026-10-18)
- [Second opinion — a fresh agent, positions formed before reading the addendum (2026-10-18)](#second-opinion--a-fresh-agent-positions-formed-before-reading-the-addendum-2026-10-18)
- [Related Artifacts](#related-artifacts)

## Status
Active

**Superseded in part by the owner's rulings of 2026-10-18, second round** ([handoff](task.handoff.md#owners-rulings-the-second-round-2026-10-18)): one timeline per Task used by every participant; no structured inheritance and retrieval by search instead of rings; a Task related by an edge to a content it intends to change; the cache not tied to today's models. Where a finding, proposal or position below says otherwise, the ruling governs.

Nothing here is ratified, and nothing in [task.md](task.md) changed because of it. Claims from outside sources are claims, read through a page summary and not in full; figures are the sources' own and unverified here. Where a statement is the agent's own it says "(agent, ...)". Marks follow [Research 001](task.research.001.md#status): Tentative, Explored, Deferred.

## Question and Goals
- **Questions:**
  - A Task and the content around it are read by agents whose context is bounded, and a Task may have many participants, human and not. What must the model say so that this works? — Findings 3 to 5.
  - Does recent outside work contradict the organization's choices on content and task management (git as a sink, Task as the commit message)? — Findings 1, 5, 6.
  - How can a cached context be reused across the readers of one Task? — Finding 4.
- **Goals:** state what the outside sources show, separate it from what they do not; list the points of agreement and of gap; give the owner proposals and questions only the owner can settle.
- **Scope:** the task domain and its neighbours at the places they touch a reader's context. Out of scope: how a model is served, any change to a `.kh` file or folder, and the design of the `agent run` concept (Task, User, AI model and how agents run are the organization's concepts, and the last is not designed here).

## Participants
- [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — Questioner; pointed to the source-control article and asked for the context, cache and many-participants question (2026-10-18). Reviewer: Not yet reviewed.
- An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — Researcher. Reviewer: Not yet reviewed.

## Methodology
One reasoning pass by one agent, with web retrieval. Pages were fetched and summarized by a small model, so a summary may drop detail; they were not read in full. Read: Anthropic Engineering, [Redesigning source control at Anthropic](https://www.anthropic.com/engineering/redesigning-source-control); [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents); [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system); the [prompt caching](https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching) page (first 100,000 of 160,000 characters); and, only as search excerpts, Cognition's [Don't Build Multi-Agents](https://cognition.ai/blog/dont-build-multi-agents) (the page itself did not load). Memar read at the passages cited: [Cognition → What Implementation Asymmetry Obliges](https://github.com/GeniusesGroup/memar/blob/main/docs/cognition.md#what-implementation-asymmetry-obliges), [Agency → Multi-Agent Systems](https://github.com/GeniusesGroup/memar/blob/main/docs/agency.md#multi-agent-systems), [Agency → Agency and Ownership of Process State](https://github.com/GeniusesGroup/memar/blob/main/docs/agency.md#agency-and-ownership-of-process-state). Not read: the full prompt caching page, Cognition's own post and its 2026 follow-up, content.md in full, the Scion systems beyond the article.

## Findings

### 1. What the source-control article says, and what it does not
(agent, from the page summary.) The article reports a monorepo whose merge rate grew from about 2,500 to over 30,000 changes a day between May and September 2026, with source control becoming the bottleneck. It names git's design as the mismatch: every clone is a full, offline-capable repository, while nearly all clients are always-online agents and jobs. Its replacement, Scion, rests on these points:

- clients are always online; the server holds history and does commit, merge and blame; a client keeps a bounded cache;
- every query is an API, so many jobs need no local copy at all;
- a commit is created on the server as an immutable **changeset**, content-addressed, with no push; refs are discouraged except main and release, because global state does not scale;
- everything beyond the changeset (blame, path history) is **derived data**, one generic mechanism, each type defined from its parents' values, computable eagerly or deferred, and changeable without clients noticing;
- fetches request immutable objects by address, so any cache tier can answer; the article reports cache hit rates above 99% and about 200 times less CPU and memory than the mirrors;
- a global merge lock does not fit agent-scale work; post-merge testing replaces it and conflicts are usually fixed by a model faster than people notice them;
- review shifts to the intent of a change; approval rules can be semantic (a comment-only change differs from a change to sensitive logic); permissions exist at repository and directory level;
- it is not offered publicly and is not a general git replacement.

**What it does not say.** The summary found no task abstraction and no account of bounded context or many collaborators. The article is about the storage and serving of changes at scale; the claim that task management is criticised in it is not supported by it. What it does support is narrower: that a design built on an always-online server, immutable addressed changes and derived views beats a design built on local full copies when most readers are agents. It also says a bounded local cache is the right client, which is the same shape as a bounded context.

### 2. What the context-engineering sources say
(agent, from page summaries.)

- Recall degrades as the window fills, gradually and not at a cliff; the guiding rule is the smallest set of high-signal tokens that makes the result likely ([Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).
- Agents hold **lightweight references** and load content just in time; metadata such as names and structure carries signal; progressive disclosure builds understanding step by step.
- For work longer than a window: **compaction** (summarize and restart; tune for recall, then precision; clearing old tool results is the lightest form); **notes kept outside the window** and reloaded; **sub-agents in clean windows** that return condensed summaries, often 1,000 to 2,000 tokens.
- In the research system, a lead agent saves its plan to memory because the window is truncated past 200,000 tokens; sub-agents write outputs to external artifacts and pass **references**, not copies, back; the cost is about 4 times a chat for an agent and about 15 times for several, so multi-agent work suits high-value work that parallelizes; vague delegation caused duplicated and misread work; the lead cannot steer a running sub-agent and sub-agents cannot coordinate with each other ([multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)).
- Cognition's argument, from excerpts: agents should **share full traces, not messages**, and every action carries implicit decisions, so parallel writers that cannot see each other's decisions produce conflicting results; their later note says it holds for parallel-writer swarms while setups where several agents contribute intelligence and **writes stay single-threaded** work.

(agent) The two vendors differ on parallelism and agree on three things: state lives outside the window, readers get references and condensed hand-backs, and a worker must see the decisions already taken.

### 3. Many participants, one task: share or partition
A Task may have humans, software agents, machines and organizations on it. Memar's [Agency](https://github.com/GeniusesGroup/memar/blob/main/docs/agency.md#multi-agent-systems) already says such a system is a network of relationships, not a list of identical agents, and that for state under one invariant the model should first ask whether **responsibility can be partitioned so that one Agent is responsible for that state at a time** ([ownership of process state](https://github.com/GeniusesGroup/memar/blob/main/docs/agency.md#agency-and-ownership-of-process-state)). Read together with the sources:

- Cognition's single-writer finding and Agency's partitioning say the same thing in two vocabularies. In the Task model the partition is the holder of a Task, and the children of a Task are the partition of its work.
- The "implicit decisions" a worker must see are, in this model, the **decisions recorded as labels on the ancestors and siblings** of its Task (Decided: Decision is a label on a Task, [handoff](task.handoff.md#from-organization-ideas-backlog--task)). A child that does not read its parent's decisions repeats the failure Cognition describes.
- A hand-back is the bridge both vendors describe: the result a parent receives is a bounded outcome and a reference to the content, and not the child's whole trace. Whether a parent may also read the trace is a permission question.
- Communication on a Task is to the Task, not to a person: a message lands on the Task's discussion, and each participant reads a view cut by role and authority. This is what lets a human, an agent and an organization sit on one Task without the model assuming one human reader.

### 4. How a context cache constrains the model
(agent, from the caching page.) A prompt cache reuses an **exact prefix** in the order tools, system, messages; any change at or before the cached point misses. Writes cost more than ordinary input (about 1.25 times for five minutes, 2 times for an hour) and reads far less (about a tenth or less); the default lifetime is five minutes, refreshed by each read; one hour is optional; caches are isolated per organization or workspace; a cached entry is usable only after the first response begins, so parallel readers need the first to have started; changing tool definitions, effort or thinking settings invalidates parts of it. Prices and thresholds are the page's and change.

What this requires of the Task and content model, whatever serves the model (agent, from the above):

1. **Append-only and addressed.** A prefix is reusable only if what came before never changes. The model's rule that a correction is a new fact and never a rewrite, and that a revision is a new addressed content, is not only cleanliness; it is what makes a history a stable prefix. Scion's immutable addressed changeset is the same property.
2. **A stable order.** The context for a reader of a Task is a walk of the graph, and the walk must serialize identically each time: the same order of ancestors, decisions, content, and events.
3. **Stable first, volatile last.** What changes rarely goes first (the organization's constants and rules, then the Task chain from its root: intents, checks, decisions), then the Task's own content, then recent events, and last what changes every time (status, time, the reader's role). Putting a timestamp or status early costs the whole cache.
4. **Share across readers by sharing the prefix.** Readers on one Task with the same model and organization share a cache only for the part that is identical for them; each reader's role belongs after it. Isolation per organization agrees with the proposed rule that a Task is not created in another organization's space (Research 001, question 16).
5. **The cache is not the Task's.** Which model, window, lifetime or price applies belongs to how agents run, an organization concept this domain only feeds. The Task supplies the **view**; it does not know the budget.

### 5. Where the organization's model agrees
- **Git as a sink; Task as the commit message.** Decided in the domain ([handoff](task.handoff.md#from-organization-ideas-backlog--task)); Scion's changeset with a message-free, server-made, addressed record and derived blame is the same direction from the other side.
- **Derived data is not stored as source.** The model's `edges-shortcut` bucket is a derived cache whose document names the edges it recomputes from, and Research 001 already puts a parent's progress in discovered data. Scion's generic derived-data mechanism is that rule at scale.
- **No global state entity.** The handoff doubts a global "state of the graph at time T" entity; Scion discourages refs for the same reason.
- **Intent first.** Defining the node as intent ([task.md](task.md#task)) matches review that moves to the intent of a change.
- **Events, not rewrites.** The same as item 1 of finding 4.
- **Delegation and single responsibility.** [Delegate](../../rights/delegate/delegate.md) and the Assign rules (assignment is a delegation, a thing may be the holder) match the partitioning of finding 3.

### 6. Where it does not, or says nothing
- **Scion is still file-and-tree shaped.** A changeset lists files changed against a parent; fetches walk trees and blobs; checkouts are sparse working copies. The organization has put file-system thinking aside for content. The adoptable part is the properties (online, addressed, immutable, derived), not the shape. Whether `changes` points at paths or at content revisions is Research 001's K5 and is restated below.
- **No task, no context, no hand-back in the article.** The model has to carry these itself. Nothing outside this research found says how to model a Task graph for a bounded reader; the organization is ahead of the sources on the question, or has missed them, and cannot tell which.
- **Context assembly has no owner.** Neither [task.md](task.md), [content](../../knowledge/content/content.md), nor the other neighbours says who builds the view a reader gets from a Task, what it includes, or in what order. This is the largest gap.
- **Compaction has no model.** A summary of a stretch of discussion is content derived from other content, with a risk of losing what mattered; the sources say deciding what survives is the hard part. The model has `changes` and no `summarizes`.
- **Inheritance has no rule.** What a child sees of its ancestors is unstated.
- **Concurrent change.** Scion replaces a merge lock with post-merge tests and quick repair; the model has `blocks` and no stated policy for two Tasks that change the same content at once.
- **Approval by kind of change.** Semantic approval rules and directory-level permission have no counterpart besides the shared `approval_needed` and `approved` loops and the authorization overlap Research 001 reports.
- **Evidence is thin on cost.** The sources' multipliers (4 and 15 times) are from one vendor's secondary report; whether a Task graph pays for itself in a bounded context is untested here.

### 7. Proposals
All Tentative.

1. **The reader's context is a derived view of the Task graph and is never stored as source.** A pluggable capability assembles it by a stated, deterministic walk and places the stable parts first. It reads the graph and writes nothing, like an `edges-shortcut`.
2. **A summary is a content that `summarizes` a span of a Task's content or discussion, with the span kept**, labeled with who made it and that it is a summary. It is the compaction and the condensed hand-back in one mechanism. It is never the record, and it is replaceable.
3. **A child reads from its ancestors by walk: decisions, checks and constraints (labels and rules) and references to content; not their text unless asked.** This is just-in-time retrieval and progressive disclosure expressed as graph walking.
4. **A content has one holder with write responsibility at a time; others propose through child Tasks.** Reading is open by authority; writing is partitioned.
5. **Order is canonical.** The events and revisions of a Task have a stable, addressed order, so the prefix of any reader's view is identical across readers.
6. **`changes` points at content revisions, not at paths.** A file layout is a projection a consumer may ask for.
7. **Two Tasks changing one content at once is allowed; the second to arrive creates a child conflict Task for the holder.** Optimistic, with a repair Task, in place of a lock; `blocks` stays for declared dependence.
8. **The Task never knows a window, a model or a price.** Those belong to how agents run.

## Open Questions
Only the owner can decide these. Each has a recommended default and what it blocks. They are also entered in the [handoff](task.handoff.md#research-002-questions-2026-10-18). Numbering continues Research 001's.

17. **Is a reader's context a derived view of the Task graph, assembled by a pluggable capability, and where does that capability live?** Default: derived, pluggable, home undecided. Blocks: finding 4 items 2 and 3, the hand-back, the agent-run concept.
18. **Is a summary a content that `summarizes` a kept span, never the record?** Default: yes. Blocks: compaction, the condensed hand-back, a `summarizes` edge.
19. **What does a child Task inherit by walk from its ancestors?** Default: decisions, checks and constraints and references; not text. Blocks: the context view, the decision-as-label shape (question 15).
20. **Does a content have one write holder at a time?** Default: yes; others propose through child Tasks. Blocks: the holder model, the claim, the conflict policy.
21. **Do events and content revisions have a canonical, addressed, append-only order?** Default: yes. Blocks: cache-friendly views, audit, K5.
22. **Does `changes` point at content revisions or at paths?** Default: revisions. Blocks: K5, the bridge to Memar's adapter, any file projection.
23. **Concurrent change to one content: a lock through `blocks`, or optimistic with a child conflict Task?** Default: optimistic. Blocks: the conflict policy, test scenarios for two writers.
24. **Is review attached to the intent of a Task rather than to its changes, and are approval rules conditioned on the kind of change (comment, structure, sensitive)?** Default: yes to both. Blocks: the approval consequence on closure, authorization overlap.
25. **Does a parent read a child's trace, or only its hand-back?** Default: hand-back; the trace by permission. Blocks: the visibility model (question 11).
26. **Where does the concept of how agents run, with its window, cache and model tier, live, and what does the Task give it?** Default: its own concept; the Task gives the view. Blocks: questions 17 and 21.

## Addendum — independent review by a stronger model (2026-10-18)
Written by an AI agent (Claude, model claude-opus-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) in a session opened for the review, at the owner's request after the owner found Findings 1 to 7 unclear. Nothing here is ratified; every proposal is Tentative. It corrects two items above, both against decided material: **Proposal 7 and question 23** (optimistic concurrency) contradict the owner's decided direction of 2026-10-05 in [content.handoff.md](../../knowledge/content/content.handoff.md) (one changer per entity, not time-stamp reconciliation); **Proposal 2 and question 18** conflict with content's question 16 ("a summary is discovered data"). Where the addendum's revised default differs from the one above, the addendum's governs until the owner decides. Its own Proposals and Open Questions continue the numbering (Proposals from 9; questions 27 to 34).

### Findings 8 and following

#### 8. The owner's reading of the source-control article, checked
- **Where the owner is right.** The article does say that git's model no longer fits when most clients are agents: "Git assumes that clients work offline and need a complete copy of the repository", while "nearly all of our clients were agents and jobs that are online by definition" ([Redesigning source control at Anthropic](https://www.anthropic.com/engineering/redesigning-source-control), read). It also says something Finding 1 left out and that bears directly on the owner's question about attention: people "still review every change request" but "examine the _intent_ of the change as opposed to reading every line of code", and the review tool "can express complex semantic constraints on approvals" so that "human reviewers focus on the most consequential changes" (same page, read). That is a statement about a person's attention under agent volume, and its answer is the one this addendum proposes: show the person the intent and route only the consequential kinds of change to them.
- **Where the owner is not right.** The article has no task or issue concept, no discussion of an agent's context window, and no account of coordination among many participants beyond the lack of a global merge lock (same page, read; asked for each and answered absent). It does not say that task management in the git style fails; it says source control in the git style fails. Finding 1's narrower reading stands, with the addition above.
- **What follows.** The article is evidence for properties (always-online server, immutable addressed changes, derived data, no global refs, review of intent, approvals by kind of change), not for a task model. The task model has to be argued on its own, which Findings 9 to 14 do.

#### 9. A `#12345` is two different things, and only one of them is the Task's
(agent) On GitHub one syntax carries every kind of link. A `#123` in a comment is a mention; it renders as a link, and in a list it "will unfurl to show the title and state"; "by default, references generate a backlink" ([Autolinked references](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/autolinked-references-and-urls), read). Typed relations were added later and apart: sub-issues ("up to 100 sub-issues per parent issue", "up to eight levels", [Adding sub-issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-sub-issues), read) and dependencies, shown as "Blocked by: octo-org/octo-repo#200 Database schema migration", that is, with the target's title ([Creating issue dependencies](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-issue-dependencies), read). Linear has blocked, blocking, related and duplicate, and "referencing issues in a description or comment automatically creates a related issue" ([Issue relations](https://linear.app/docs/issue-relations), search summary; the page returned 404 to the tool). Jira has named link types with an outward and an inward description, configured by administrators ([Configure work item linking](https://support.atlassian.com/jira-cloud-administration/docs/configure-issue-linking/), search summary).

What they get wrong at scale (agent):
1. **A mention is promoted to a relation.** Linear turns a mention into "related"; GitHub turns it into a backlink in the target's timeline. A word in someone's comment then changes what every reader of the target sees. With thousands of Tasks citing a common one, the target's history fills with references that say nothing about it.
2. **The preview is too thin to act on and the target too large to read.** Title and state tell a reader whether a link is open, not whether it binds the reader's work. What binds is the target's decisions and outcome, which no tracker shows in the preview.
3. **Relation types are vocabulary, not behaviour.** Jira's configurable types have no stated trigger; only "blocks" changes anything. This is the same failure Research 001 found in the domain's edge folders.

The model's answer (agent, Tentative): a reference written in text is **content's** relation (a mention from a content to a thing), not a Task relation; Task keeps only `part_of`, `blocks`, `changes`, and thing's `supersedes`, each with a trigger. A backlink is derived, never an event on the target's timeline. Following any reference gives the reader a **card**, not the target (Proposal 9).

#### 10. One bound for the agent and for the person
(agent) A reader of a Task, human or AI, has a bounded working set: an agent's window, a person's attention for the day. Outside work agrees that the bound is real and soft. Recall falls as the window fills ([Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), read: "context rot", an "attention budget"); across 18 models "performance consistently degrades with increasing input length" and topically related distractors reduce accuracy further ([Context Rot, Chroma](https://www.trychroma.com/research/context-rot), read); material in the middle of a long input is used worst ([Lost in the Middle, arXiv 2307.03172](https://arxiv.org/abs/2307.03172), read, abstract only). For people, interruption research reports that interrupted work takes a long time to resume ([Interruption science](https://en.wikipedia.org/wiki/Interruption_science), search summary; Mark, Gonzalez and Harris, CHI 2005, not read, its figures not repeated here). Kanban limits work in progress, and by Little's Law fewer items in progress means shorter cycle time at the same throughput (search summary only, several secondary pages; Anderson's own text not read).

The consequence for the model is the central claim of this addendum: **the bound is a property of the reader, but whether a Task fits it is a property of the Task.** What binds a Task (its intent, its check, the decisions and constraints it inherits, the questions open on it, the Tasks that block it) must reach every reader of it whole. If that set does not fit a reader's bound, ranking it or truncating it hides a binding item, which is the Cognition failure ("implicit decisions" not seen). The right answer is to decompose the Task, so that each child's binding set fits. A large graph is then not read; it is walked, one bounded neighbourhood at a time, and each neighbourhood is small because the Tasks were sized for it. This is the same rule as a WIP limit, applied to what one reader holds at once rather than to what a team holds.

#### 11. Many participants: partition writes, share decisions, keep traces as content
(agent) Cognition's position, as far as it could be checked, is that parallel agents make implicit choices others cannot see, and that multi-agent systems "work best today when writes stay single-threaded and the additional agents contribute intelligence rather than actions" (Cognition, "Multi-Agents: What's Actually Working", 2026, seen only as a quotation in a third-party guide, [13labs](https://www.13labs.au/guides/multi-agent-orchestration-what-works), search summary; Cognition's site refused the connection). Anthropic's research system has sub-agents "store their work in external systems, then pass lightweight references back", with each needing "an objective, an output format, guidance on the tools and sources to use, and clear task boundaries"; it notes the lead "can't steer subagents" and sub-agents "can't coordinate" ([Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system), read). Its sub-agents explore, the lead writes: that is Cognition's single-threaded writes. The two agree once the question is split:

- **Writes** to one content are partitioned: one changer per content at a time. This is not new; it is the owner's decided direction of 2026-10-05 in `content.handoff.md` (single changer per entity, routing by identity, time-stamp reconciliation rejected as the default) and Memar's [Agency and Ownership of Process State](https://github.com/GeniusesGroup/memar/blob/main/docs/agency.md#agency-and-ownership-of-process-state). Research 002's question 23 default ("optimistic") contradicts it (see the revised defaults).
- **Decisions** are shared, not traces. What a sibling must not miss is what another sibling decided, not how it got there. A holder records each decision it took as a Decision label on its own Task before it hands back; a reader's view includes the decisions of its ancestors and of its siblings under the same parent.
- **Traces** are content on the Task's timeline, readable by permission, never sent by default.
- **Discussion** has many writers safely, because each entry is its own content placed on a timeline; appending distinct contents does not contend for one changer.

#### 12. A chat is a run on a Task, not the Task
(agent) Today an agent session is a chat opened and closed; what it decided lives in its scrollback unless written elsewhere. Claude Code carries knowledge across sessions only through files loaded at start ("Each Claude Code session begins with a fresh context window"; auto memory loads its "first 200 lines or 25KB"; nested instruction files "load on demand", [Claude Code memory](https://code.claude.com/docs/en/memory), read). Devin's knowledge is "retrieved when relevant, not all at once" by a trigger description ([Devin knowledge](https://docs.devin.ai/Onboard_Devin/knowledge), search summary). MemGPT treats the window as main memory paged from external storage ([arXiv 2310.08560](https://arxiv.org/abs/2310.08560), search summary). All three keep the durable part outside the chat; none ties it to a unit of agreed work. Memar's session does: its plan outlives its context, which is why this session can be handed to a sub-agent at all.

In the model: the Task owns intent, check, status, outcome, relations and claim; the conversation is a timeline of content the Task refers to; each message is a content; text owns the words; the agent's run is an event span on the Task by its holder, owned by the organization's concept of how agents run. Closing the chat ends a run, not the Task. What is lost is only the run's working state (its cache, its unwritten reasoning); what is gained is that every later reader, of any kind, starts from the Task's view and not from a transcript.

#### 13. What makes a view reusable as a cached prefix
(agent, from [Prompt caching](https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching), read to 100,000 of about 160,000 characters.) The page states: prefixes are built in the order "tools, system, then messages"; changing tool definitions "invalidates the entire cache"; changing the thinking configuration "always invalidates message blocks"; the default lifetime is five minutes, refreshed on use, with a one-hour option; writes cost 1.25 times base input for five minutes and 2 times for one hour; reads cost 0.1 times, with lower multipliers for some models (0.05 for Claude Opus 5.5 and Sonnet 5.5); the minimum cacheable length is 512 tokens for the newest models; at most 4 breakpoints; the system "checks at most 20 positions per breakpoint"; "different organizations never share caches", and on the Claude API caches are isolated per workspace; "a cache entry only becomes available after the first response begins".

What this requires (agent): items cited at an address (a content revision, a Task at an event number) so their rendering never changes; one canonical walk order; binding and stable items first, ranked and volatile items after the last breakpoint; the reader's role and any time or status that moves placed at the tail. Two things break it that Finding 4 did not name: **ranking by relevance** (a different reader or a later moment reorders the items, so ranked material must sit after the cached part), and **re-rendering an ancestor at its latest revision** (one edit to a root intent misses the cache of every descendant's reader; citing it at a revision and noting "newer revision exists" at the tail keeps the prefix).

#### 14. Corrections to Research 002 found in review
- Finding 3's statement that a parent reads only a hand-back is right, but the hand-back as defined in `task.md` (status, report, questions) lacks the **decisions taken**, which is the item Cognition's failure turns on.
- Finding 4 item 4 places the reader's role after the shared part; correct. It should also place ranking there (Finding 13).
- Proposal 2 (a summary is a content that `summarizes` a span) conflicts with content Research 001 question 16, whose default is that "a summary is discovered data". A summary made by a person or an agent is acquired (two summarizers differ); only a summary any party would compute the same way is discovered. The question is content's, not Task's.
- Proposal 7 (optimistic concurrency) contradicts the owner's decided direction; see Finding 11.
- Finding 6 says nothing outside says how to model a Task graph for a bounded reader. Still true of the sources found; the trackers' typed relations, previews and notification reasons (Findings 9 and 15) are the nearest practice, and none ties the bound to Task size.

#### 15. Attention: what trackers do, and what applies
(agent) GitHub subscribes a person automatically when they are assigned, open, comment, are mentioned or change a thread's state; delivery carries a reason (mention, review requested, assign, comment, state change, subscribed); the inbox has done, saved and custom filters; unsaved notifications are kept three months ([About notifications](https://docs.github.com/en/subscriptions-and-notifications/concepts/about-notifications), read). Linear routes work arriving from outside a team into a Triage inbox with a rotating responsibility ([Triage](https://linear.app/docs/triage), search summary). What applies: a delivery reason that names the reader's relation to the item; a triage role for unrouted arrivals; done as the reader's own act. What does not: subscription by commenting or by being mentioned, which makes volume grow with the number of people who write, not with what needs the reader.

### Proposals
All Tentative. Numbering continues Research 002's.

9. **A reference in text is content's mention; a backlink is derived.** Task relations are `part_of`, `blocks`, `changes` and thing's `supersedes`, each with a trigger; no `refers_to` enters the Task domain.
10. **Following any reference gives a card.** A card is a derived rendering of a Task at an event number: identity, title, status, outcome if ended, the check in one line, the Decision labels on it, the open questions on it, and a reference to its latest hand-back. Opening the whole target is an explicit pull.
11. **The view has three rings, decided by relation type, not by score.** Ring 0, whole: the reader's Task (intent, check, status, open questions, decisions) and what binds it by inheritance (ancestors' and siblings' decisions and constraints, ancestors as cards). Ring 1, cards: unended blockers, children, the superseded Task. Ring 2, handles: mentions and `changes` revisions, as title and summary reference. Ranking applies only in ring 2 and to pulled material.
12. **Entry and exit.** An item enters if it binds the Task, if the Task's progress waits on it, or if the reader pulled it. A blocker that ends collapses to one line. A pulled body leaves the view when the run compacts, replaced by a summary content that cites it. Ring 0 never leaves.
13. **When ring 0 does not fit, the Task is decomposed.** A rule attached to the claim refuses, or warns on, a claim whose ring 0 exceeds the claimant's stated bound; the remedy is child Tasks, not truncation.
14. **When something outside the view matters, the reader has three moves**: pull it (it enters ring 2), delegate (a child Task whose view holds it, returning a hand-back), or ask (a question on the Task, which blocks).
15. **A hand-back lists the decisions taken**, as Decision labels on the handing Task, besides status, report reference and questions.
16. **The person's view is the same view.** What a person is shown first is ordered: questions and approvals that wait on them; status changes on Tasks they hold or that block theirs; the rest as a digest. The inbox, counts and digest are derived; the subscription, the done act and a holder's WIP limit are acquired. A notification is never stored as source; it is derived from events, subscriptions and roles. Subscription is the notification domain's; the WIP limit is a rule on the claim capability.
17. **Approval is by kind of change.** The kind (comment-only, structural, sensitive) is a label on the content revision; the approval rule is rule's, attached through `condition_is`; the Task holds only the attachment.
18. **An agent run is an event span on the Task, held by the agent for its principal**; the conversation is a timeline the Task refers to.

### Open Questions
Revised defaults for questions 17 to 26, then new questions. Ordered by what they change: what the domain is first, then how a part is done.

- **33 (new). Is an agent's chat a run on a Task (an event span by its holder), with the conversation a timeline the Task refers to?** Default: yes. Blocks: the chat-as-Task shape, question 26, the Memar session mapping.
- **17 (changed). Is a reader's context a derived view of the Task graph?** Default: yes, one view capability for every reader, person or agent, given the reader's role and bound by the caller; home a pluggable under `modules-plugable/management/`. Reason: the attention problem and the context problem are one problem (Finding 10). Blocks: Proposals 10 to 16.
- **27 (new). Is a reference written in text a content mention, with backlinks derived and never placed on the target's timeline?** Default: yes. Blocks: the card, notification volume, any `refers_to` edge.
- **20 (changed). One changer per content at a time.** Default: yes, and already the owner's decided direction in `content.handoff.md`; the question is content's. The Task's own state has one writer, its holder. Blocks: claim, question 23.
- **23 (rejected default). Concurrent change to one content.** Default changed from optimistic to the decided direction: one changer; a second Task needing the content is blocked by the Task that holds it, or proposes through a child Task; no global lock. Reason: the previous default contradicted a decided owner direction, and the article's "no global lock" is about a global lock, not a per-content changer. Blocks: the conflict policy, test scenarios for two writers.
- **29 (new). Is a binding set larger than the reader's bound a reason to decompose the Task, never to rank binding items out?** Default: yes, as a rule on the claim. Blocks: Proposal 13, Task sizing.
- **22 (agree). `changes` points at content revisions, not paths.** Default: revisions; aligned with content Research 001 question 1. Blocks: K5.
- **21 (changed). Canonical, addressed, append-only order.** Default: yes, per identity (each Task's events, each content's revisions), never a global sequence. Reason: no global refs, as in the article. Blocks: cards at an event number, caching, audit.
- **19 (changed). What a child inherits by walk.** Default: ancestors' and siblings' decisions and constraints whole; ancestors as cards; no text unless pulled. Reason: siblings' decisions were missing and are the Cognition failure. Blocks: ring 0, question 30.
- **30 (new). Must a hand-back list the decisions the holder took?** Default: yes, as Decision labels on the handing Task. Blocks: the hand-back in `task.md`, question 15 of Research 001.
- **28 (new). Is the card the default thing a reader gets on following a reference, rendered at an event number?** Default: yes, derived. Blocks: the view, caching.
- **25 (agree). A parent reads the hand-back; the trace by permission.** Default unchanged; the trace is content. Blocks: visibility (question 11).
- **24 (changed). Review of intent, approval by kind of change.** Default: yes; the kind is a label on the revision, the rule is rule's. Reason: the article supports it; the boundary puts the kind with content and the check with rule. Blocks: approval on closure.
- **31 (new). Does the claim capability carry an optional WIP limit per holder, person or agent?** Default: yes, a rule set per organization. Blocks: Proposal 16.
- **32 (new). Is subscription the notification domain's, and the inbox always derived?** Default: yes. Blocks: Proposal 16.
- **34 (new). Does a view cite items at a revision for a run, with "newer revision exists" at the tail, or render the latest?** Default: at a revision within a run, refreshed when a run starts. Blocks: caching, staleness.
- **18 (moved). Is a summary a content that `summarizes` a kept span?** Default: yes when someone made it (acquired); discovered only when any party would compute it alike. Reason: it conflicts with content Research 001 question 16; the question is content's. Blocks: compaction, Proposal 12.
- **26 (agree). How agents run is its own concept.** Default: its own; the Task gives the view, the claim, and a place for the hand-back; the run gives the bound, the model and the cache. Blocks: question 33.

## Second opinion — a fresh agent, positions formed before reading the addendum (2026-10-18)
Written at the owner's request after his answers recorded in the [handoff](task.handoff.md#owners-answers-to-the-review-2026-10-18). A different model was tried and was unavailable for lack of credits, so the same tier ran; independence is only that its positions A to G were written before it read the addendum. Nothing here is ratified. It replaces question 33 and the addendum's reading of a run, adds `same_ask` as a candidate fifth Task relation, and adds four tests for a new Task versus a participant.

Written by an AI agent (Claude, model Opus 5.5, `claude-opus-5-5`, as reported by the runtime) for session 20261018-T170339Z-16088. A different model was wanted and was not available, so this is the same tier as the earlier reviewer. Every proposal is Tentative and changes no module document.

**Independence.** Positions A to G were formed from `task.md`, `task.handoff.md`, `task.research.002.md` lines 1 to 129, `content.handoff.md`, the group, delegate, timeline and text-mention documents, and Memar's Agency sections, and were written to a scratch file of the review session before the addendum (lines 130 to 229) was read. Section H is written after it. Where the final text below differs from that file, the change is said in H.

### A. A new user on a Task: a new Task, or a participant of the same Task?
**Position.** The new person (or agent, or organization) is a participant of the same Task unless what is asked of them meets one of four tests. If it meets any of them, it is a new Task, normally a child of the asking Task through `part_of`.

1. **Own check.** What they are asked can end, or fail, while the asking Task goes on: "give a written opinion on A to H" can be declined, can be late, can be answered badly, and the asking Task is not done or failed because of it.
2. **Own holder by delegation.** They must accept the work as their own act (`task.md`, Assign task rules: silence is not acceptance), and they work over a time of their own, with their own status.
3. **Own view.** They must see a different cut of the material from the Task's other readers: an independent opinion must not see the first opinion; a confidential consultation must not see everything; another organization works in its own space (Research 001, question 16).
4. **Own writes.** They will change content whose single changer is not the asking Task's holder (`content.handoff.md`, concurrency decision of 2026-10-05).

If none holds (they are asked one question, answer in the discussion, and the asking holder judges the answer), they are a participant: a member of the Task's group with a role, writing discussion entries.

**Worked example.** In session 17560 the owner wanted an opinion on Research 002. That opinion has its own check (positions on every question), its holder may be Blocked, and the second opinion (this one) needs a view without the first. All four tests hold, so 11200 and 16088 are Tasks, and they are children of 17560 through `part_of`: the session records already say "parent: 20261017-T162411Z-17560". The `#11200` that the owner compared to GitHub is therefore not only a mention; underneath it is `part_of`. By contrast, if during 17560 the owner had written "@Ali, is the outcome word 'abandoned' right in Persian?", Ali is a participant: one reply in the discussion, judged by the holder, no own check.

**Organization as participant.** An organization is a member of the Task's group (group allows organizations as members) and accepts through delegate. It never works inside our space: its own internal work on the answer is a Task in its own space, and what reaches our Task is its answer, placed in our discussion as content by the agent that speaks for it. Our Task does not see its internal Tasks; it sees the answer and who stands behind it.

**Many AI agents with near-identical context.** Near-identical context is a reason to share a cached view, not to share a Task. If each agent produces its own opinion (for diversity), each is a child Task with the same view; their outputs are compared by the parent's holder. If they produce parts of one output, each part is a child. If they only comment, they are participants. What none of them may do is write the Task's own state (status, check, decisions): that has one changer, the holder (Agency, "responsibility can be partitioned so that one Agent is responsible for that state at a time").

**What each choice does.**

| | Participant | New Task |
|---|---|---|
| Graph | a membership with role on the Task's group; their replies are contents with `reply_to` | a new identity, `part_of` the asker, its own group, check and status |
| A reader's context | their replies enter the Task's discussion, so every reader may meet them | the parent's reader sees only the child's hand-back (a card); the child's work stays out |
| History | one stream, all on the Task | two Tasks, each with its own events; the hand-back joins them |

**What it changes in the model.** `task.md` gains the four tests under "Task as a unit of agreement": "One Task is one thing asked, with one check" already implies test 1; tests 2 to 4 are added. Nothing new is needed in group or delegate.

### B. How a mention changes the path
**What a mention is.** Three different things travel under "mention", and they must be kept apart:

1. **Mention**: a relation from a content to a participant. It exists already as text's `(text)-[:mention]->(user)`, where the user "CAN be any type such as person, group, organization, bot"; content owns the resolved relation (owner's answer to Q27). By itself it gives nobody a right or a duty. Whether the mentioned one is told is the notification domain's.
2. **Invitation**: an act of someone with authority that adds a membership to the Task's group. Its acceptance is the invitee's act (delegate). A mention does not make anyone a member.
3. **Question**: a content that expects an answer from a named participant. If the Task's progress waits on it, the Task is Blocked and says on what (`task.md`, Status and Hand-back). A question is a content with a mention and a label "question to X"; it is not a Task unless test A applies.

**What the mentioned participant is given.** The view of the Task as it stands at the mention, cut by the participant's authority: intent, check, the decisions recorded on the Task and its ancestors, the open questions, the discussion entry that mentioned them and what it replies to, and cards for the other things it cites. Not the other participants' thinking (C), and not the whole discussion unless they pull it.

**What they may write.** Discussion entries (replies, proposals, objections), and their own thinking (C). They may not change the Task's intent, check, status or decisions; only the holder does.

**One coherent state.** The key is that a mention changes the mentioned participant's cognitive path, never the Task's. The Task's path changes only through an act of its holder: a recorded decision, a revision of the intent or check, a new child, a status move. Several participants who reasoned differently therefore produce several discussion entries, and one Task state.

- **Visible:** each participant's stated position (their reply), and which replies a decision rests on. Content's working verbs already have `supports` (Discussion to Decision); a decision cites the replies that support it, and a reply that disagrees stays, linked by `reply_to`.
- **Not visible by default:** how each reached their position (their thinking), and positions never written.

**Worked example.** The holder of 17560 mentions two reviewers. Reviewer 1 writes "Q23: keep the single changer"; Reviewer 2 writes "Q23: optimistic". The holder records the decision "Q23: single changer" with `supports` to Reviewer 1's reply. Reviewer 2's reply stays as the visible dissent. A later reader sees one decision, its support, and the dissent; neither reviewer's private reasoning.

**What it changes.** Nothing in Task's kernel. Content's `supports` (now only a working verb) becomes a real relation with a trigger: a decision without at least one support, or without "holder's own reason", is refused by a rule. The notification domain owns who is told of a mention.

### C. Thinking text
**Position.** The owner's direction is right, with one rule added to it.

- **What it is.** Thinking text is content: a participant's working record (reasoning, drafts, a tool trace). It is authored and owned by the participant who thought it. Its words are text's.
- **Where.** Not on the Task's discussion timeline. It is placed in the thinker's own timeline (content's "Twitter model": a content lives in its author's timeline and may be placed in others'), and related to the discussion entry or the hand-back it led to by a relation content owns, call it `trace_of` (thinking to the content it produced). The Task holds nothing; the trace is found from the reply.
- **Who reads it.** Whoever the thinker's authority and the organization's visibility rules allow, normally the participants of the Task and the holder of its parent. It is pulled, never pushed.
- **Default view.** Not in it. No participant is obliged to read it.

**The rule that makes this safe.** Nothing binds unless it is recorded where binding things live: a decision on the Task, a revision of intent or check, a question raised, or a discussion entry. A reader who skips all thinking text must be able to rely on that. Three things follow:

1. A decision is an addressable item (whatever Research 001 question 15 decides, a decision must have an identity that can be cited and inherited), and a decision cites its supports.
2. A reply states the assumptions it rests on, not only its conclusion; an assumption left only in thinking does not bind and may be ignored by others. This is Memar's "Externalize session state into shared artifacts" (Cognition, What Implementation Asymmetry Obliges).
3. A hand-back lists the decisions taken (agreeing with Q30). A decision found later only in a trace is not a decision; the finder raises it as a question on the Task.

This meets the earlier finding (decisions reach siblings whole; traces need not) exactly: thinking is a trace.

**Worked example.** This session's own reasoning is thinking text. Its report and `opinion.md` are the discussion and report contents. If this reasoning had concluded "the coordinator should merge 11200 and 16088" but written it nowhere else, the coordinator, reading only the report, is not misled: that conclusion does not bind, because it was not recorded.

**Gains.** Views stay small and cacheable; history is complete for audit and for the debrief of a run; a reader with a question can pull how a position was reached.

**Costs.** (1) The discipline of writing decisions and assumptions out falls on every participant; when it fails, the decision is lost to everyone who skips thinking, which is everyone by default. (2) An AI system's thinking, as a runtime exposes it, may be a summary or may not reflect what produced the answer; stored, it is a claim about the thinking, not the thinking, and must be labelled so. (3) Storage and visibility rules for a large, low-value body of content. (4) A person may write thinking they would not show; visibility must be the author's to narrow.

**What it changes.** Content gains a `trace_of` relation (or decides it is a kind of `reply_to` with a label); Task changes nothing; the hand-back in `task.md` gains "the decisions taken"; Research 001 question 15 gains a constraint (a decision is addressable).

### D. Chat as timeline, not run
**Position.** The owner's correction is accepted: a chat is a timeline holding contents, and "run" is the wrong word for its relation to a Task.

- **The relation between a timeline and a Task is derived, not stored.** A Task relates to contents: its intent, the discussion entries that reply to it or mention it, the questions raised on it, the revisions it `changes`, its hand-back. Each of those contents is placed in one or more timelines. "The span of chat T that belongs to Task X" is then discovered: the contents of T related to X. No span entity and no Task-to-timeline edge is needed.
- **One timeline serves several Tasks**, because different contents in it relate to different Tasks (`task.md`: "A conversation may hold several Tasks").
- **One Task refers to several spans**, because its related contents sit in several timelines.
- **An agent's activity**, the thing earlier called a run, is two things, neither of them a relation between a chat and a Task: (a) the agent's **holding** of the Task, which is the claim (a membership with role, from the claim event to the hand-back event), and (b) the agent's **execution record** (model, window, cache, budget, compactions), which belongs to the organization's concept of how agents run. The contents the agent wrote during the holding are ordinary contents in the timelines where they were placed. If a chat ends, nothing ends on the Task; if the holding ends without a hand-back, the Task returns to Queued or Blocked by its own rule.

**Checked against this coordinating session.**

- The owner's chat is one timeline (conversation 17560). Its contents relate to three Tasks: 17560 (define Task), 11200 (first review), 16088 (this opinion). One timeline, three Tasks.
- Task 16088 relates to contents in two timelines: the coordinator's chat (the brief, and later the hand-back) and this sub-agent's own transcript (its commands, its reading, its thinking). One Task, two spans.
- 16088's "run" is the sub-agent's claim from `memar session start` to its hand-back, plus the runtime's record that it ran on Opus 5.5 with a bounded window. Neither belongs to the chat or to the Task.
- Memar's mapping row "Conversation: a timeline of discussion; the Task refers to it and does not hold it" (`task.md`) should read: "the Task does not refer to a timeline; it relates to contents, which are placed in timelines".

**What it changes.** One row of the Memar term map in `task.md`; question 33 is withdrawn and replaced by "Is the relation between a Task and a timeline derived from the contents related to the Task?" (default: yes). How agents run gains the execution record; Task gains nothing.

### E. Summary as discovered
**Position.** Agree with the owner. What makes data discovered is that its authority lies in its sources: it can be recomputed from them, it is replaced when they change, and it is never the record. Determinism is not required. A summary has this property whether a person or a model wrote it; progress has it too, and is deterministic. So:

- **Who recomputes.** The capability that builds a reader's view (question 17), or a summarizer it calls. Never the Task.
- **When.** On demand, and again when a source changes. Because sources are append-only and addressed (question 21), "changed" is "a newer event or revision exists after the ones it was made from"; nothing has to be compared.
- **Do two readers see the same one?** Only if they share the inputs (the same sources at the same revisions), the procedure (summarizer, its version, its instructions), and the visibility cut. With a model as summarizer two computations differ, so the first result is kept and shared until its inputs change. A summary over content one reader may not see must never be shown to that reader: summaries are computed per cut, or only over content every reader of it may see.
- **What the cache needs.** The source addresses and revisions, the procedure's identity, the cut, when it was made, and a mark that it is derived. It is a cache entry, like an `edges-shortcut`, and can be thrown away.

**For compaction.** Compaction is an operation of how agents run on its own window; it may use a discovered summary, and it changes nothing in the Task graph.

**For the condensed hand-back.** The hand-back's binding parts are acquired facts written by the holder: status, outcome, the decisions taken, the questions raised, the reference to the report. The report itself is acquired content (what the holder wrote). Any shorter text made from the report is discovered: replaceable, and never the only place a decision is stated.

**Worked example.** The coordinator wants ten lines from this opinion. A summary computed from `opinion.md` at its revision, by a named model with named instructions, is cached; the owner and the coordinator see the same ten lines; if `opinion.md` is revised, the summary is dropped and recomputed. The decisions needed are not in the summary only: they are in the report's own section.

**What it changes.** Research 002 Proposal 2 (`summarizes` edge) is withdrawn as an edge; a summary is a cache entry with its inputs recorded. Content question 16 stands as decided by the owner.

### F. Task-to-Task edges beyond dependency
Test for a real edge: it has a creator, a removal, and a trigger (`task.md`, Model). Short list:

| Reason | Verdict | Why |
|---|---|---|
| **same ask** (includes duplicate) | real edge | Trigger: when the Task it points to completes, this one completes with it (its check held), or this one ends with outcome "duplicate" at once. Created by someone with authority over this Task; removed by an event. |
| duplicate | same as above | "Duplicate" is "same ask" found after both existed; one edge, the outcome word says which. |
| consults, answers | not new edges | Within one space it is `part_of` (A). Across organizations it is participation (A); the other organization's Task is in its own space. |
| derived from, follow-up | mention | B was created from something said in A's discussion; B's intent mentions that entry. No trigger. |
| related | mention or discovered | No trigger; a generic relation hides meaning (group.md, "a bare generic edge ... hides real semantics"). |

Outside practice agrees that a duplicate is an act, not a word: on GitHub a comment "Duplicate of #N" creates a "marked as duplicate" timeline event only when its writer has write access, and it can be undone by a new event (https://docs.github.com/en/issues/tracking-your-work-with-issues/administering-issues/marking-issues-or-pull-requests-as-a-duplicate, read through a page summary).

**Worked example.** Two departments each open "a Persian glossary of Task words". The second gets `same_ask` to the first; when the first completes, the second completes, and its participants are told by notification.

**What it changes.** The kernel becomes `part_of`, `blocks`, `changes`, `supersedes`, `same_ask`; nothing else is a Task relation.

### G. The questions that remain unclear to the owner
#### Q17. Is what a reader is given from a Task built each time from the graph, by a separate capability?
**Plain.** When a person or an agent opens a Task, they are shown a selection: intent, check, decisions, some discussion. Is that selection stored somewhere, or built fresh each time from the Tasks and contents, by a part of the system that is not Task itself?
**Example.** A reviewer opens Task 16088 and sees its intent, the parent's decisions and the open questions. Tomorrow a decision is added to the parent; the reviewer sees it at once.
**If yes:** nothing goes stale; the selection rule is one place to change; it costs computing it, and needs a cache. **If no (stored):** each change must update every stored view; views drift from the record.
**Recommended:** yes, built each time, by a pluggable capability, cached. One capability for people and agents, with the reader's role and bound as inputs.

#### Q19. What does a child Task get from the Tasks above it?
**Plain.** A step of a larger task must not break what was already decided above it. What, exactly, is passed down?
**Example.** 17560 decided "Task holds no text". Its child 16088 must know that, but need not read 17560's whole discussion.
**If decisions and checks only:** small views, but a child misses context it might need, and must pull it. **If everything:** nothing missed, but views grow with the depth and size of the tree and stop fitting.
**Recommended:** the ancestors' decisions, checks and constraints whole; the ancestors themselves as cards; no text unless pulled. Siblings' decisions reach a child through the parent: a child's decision that binds its siblings is raised to the parent, and the parent's holder records it there (see H, point 4).

#### Q23. Two Tasks want to change the same content at once: wait, or both change it and fix clashes later?
**Plain.** Two people edit one document. Either one waits for the other (one changer at a time), or both write and a later step repairs the clash.
**Example.** Tasks X and Y both revise `task.md`. With one changer, Y is blocked by X, or Y proposes its change through a child Task that X's holder applies.
**If one changer:** no clashes, an order everyone sees; but waiting, and a holder that does not finish holds others up. **If both write:** no waiting; but clashes, repair work, and decisions taken on content that later changed.
**Recommended:** one changer per content at a time, as decided on 2026-10-05; discussion entries are separate contents and never wait.

#### Q29. If what a Task requires a reader to know is more than the reader can hold, cut the Task up, or drop the less important items?
**Plain.** Every reader, person or agent, can hold only so much. If the things that bind a Task do not fit, either the Task is split into smaller Tasks, or some binding things are left out of the view.
**Example.** A Task carries forty decisions from above and thirty open questions; an agent's window holds the intent and twenty of them. Dropping the rest means the agent may break a decision it never saw.
**If cut up:** each piece fits and nothing binding is hidden; costs more Tasks and a holder who does the cutting. **If drop:** one Task, but silent mistakes.
**Recommended:** cut up, never drop binding items. The cutting is the holder's act, not a refusal by the system: the same Task may fit one reader and not another, so a rule on the claim only warns.

#### Q30. When a Task ends, must its hand-back list the decisions taken?
**Plain.** Today a hand-back says status, where the report is, and the questions. Should it also list every decision the holder took?
**Example.** 11200 decided "a summary is acquired". If its hand-back does not say so, 17560's holder may only learn it by reading the whole report.
**If yes:** the parent and its other children see what binds them without reading reports; costs the holder writing them out, and needs each decision to be an addressable item. **If no:** decisions sit inside reports and thinking; readers who skip them are misled.
**Recommended:** yes. It is also what makes the owner's thinking-text direction safe (C).

### H. Where this opinion differs from the earlier reviewer's addendum
Disagreements:

1. **Traces "on the Task's timeline" (Finding 11).** The addendum places traces on the Task's timeline, readable by permission. That puts them in the discussion stream every reader walks. This opinion places them in the author's timeline, related to the reply they produced (C), which is the owner's "different edge" and keeps the Task holding nothing.
2. **The run as "an event span on the Task" (Finding 12, Proposal 18, Q33).** Agreeing with the owner: the run is not on the Task and not the chat's relation to it. What the addendum calls a run is the claim (a holding interval) plus the execution record of how agents run (D). Its other half, "the conversation is a timeline the Task refers to", also changes: the Task relates to contents, and the timeline is reached through them; otherwise a Task referring to a chat imports all the other Tasks' contents in it.
3. **The Task's relations are exactly four (Finding 9, Proposal 9).** Agreeing with the owner that "same ask" is a fifth real edge, because it has a trigger (F). The addendum's argument against promoting mentions stands.
4. **Siblings' decisions whole in every child's view (Finding 11, Q19).** The set of siblings' decisions grows with the work of others, not with the reader's own Task, so decomposing the reader's Task (Q29) cannot keep it within the bound. This opinion passes sibling decisions through the parent: a decision that binds siblings is raised to the parent and recorded there by its holder. The cost is latency for siblings running at the same time; the remedy for that is a question on the parent that blocks them, not a direct sibling-to-sibling stream.
5. **Decomposition as a rule on the claim that refuses (Proposal 13, Q29).** The bound belongs to the reader, so one Task fits one claimant and not another; a refusing rule makes a Task's validity depend on who claims it. The rule should warn; decomposing is the holder's act.
6. **A summary "acquired when someone made it" (Finding 14, Q18).** Agreeing with the owner that it is discovered, for the reason in E: discovered means its authority is in its sources, not that every party computes it alike. The addendum's real worry, that two readers could see different summaries, is answered by the cache (E), not by making the summary a source.
7. **"Decision labels on the handing Task" (Finding 11, Proposal 15).** The handoff decided that Decision is a label on a Task, a kind of want; a Task carries that label once. A list of several decisions taken is therefore either a list of child Tasks labelled Decision, or decisions as items of their own (content's `produces`, `supports` and `changes` verbs already treat Decision as a node). The addendum's wording hides this choice; it is Research 001 question 15, now with the constraint that a decision must be addressable.

Agreements for a different reason:

- **Single changer (Q20, Q23).** The addendum's reason is that the earlier default contradicted a decided direction. This opinion agrees for a further reason: one changer is what lets a mention change a participant's path without changing the Task's (B).
- **Hand-back lists decisions (Q30).** Agreed; here it is the condition that makes not reading thinking text safe (C).
- **One view capability for people and agents (Q17).** Agreed; the shared thing is the rule that decides what binds and what the reader may see, not one rendering.
- **Mention as content's (Q27), card on following a reference (Proposal 10).** Agreed without change.

Additions not in the addendum: the four tests for a new Task (A); the three things called "mention" (B); organizations as participants working in their own space (A); a summary over content a reader may not see as a leak (E).

### What could not be verified
- The positions rest on the documents read in this session; `task.research.001.md` (78 KB) was not read, so its questions are known only through `task.handoff.md` and `task.md`.
- Session 11200's own report was not read; the earlier review is known only through the addendum.
- The GitHub duplicate behaviour is from a page summary by a small model; whether marking closes the issue was not stated in that summary.
- Whether any runtime exposes an AI system's thinking faithfully was not checked; C treats it as a claim.
- Content's `supports`, `produces` and `trace_of` are working verbs or proposals, not documented edges; their placement is content's to decide.

## Related Artifacts
- [task.research.001.md](task.research.001.md) — kernel, K5 `changes`, questions 11, 15, 16 that these extend (Review)
- [task.md](task.md) — the Model and Hand-back sections would take proposals 2 to 7 if accepted (Review)
- [task.handoff.md](task.handoff.md) — gains questions 17 to 26 (Update, done)
- [task.changelog.md](task.changelog.md) — entry for this research (Update, done)
- [content.md](../../knowledge/content/content.md), [content.handoff.md](../../knowledge/content/content.handoff.md) — revision identity, the `summarizes` verb, context assembly (Review)
- [text.md](../../knowledge/text/text.md) — keeping and versioning of summaries (Review)
- [timeline.md](../timeline/timeline.md) — the discussion a summary covers (Review)
- [delegate.md](../../rights/delegate/delegate.md), [group.md](../group/group.md) — holder and participation (Review)
- [status.md](../../knowledge/status/status.md) — shortcuts as derived caches (Review)
