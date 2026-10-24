# Process Research 001 — Decomposing a Development
## Table of Contents
- [Status](#status)
- [Question and Goals](#question-and-goals)
- [Participants](#participants)
- [Methodology](#methodology)
- [Findings](#findings)
- [Open Questions](#open-questions)
- [Related Artifacts](#related-artifacts)
- [Notes](#notes)

## Status
Active

## Question and Goals
- **Question 1:** Is *decomposing a development into named sub-processes, each with its own written expectations* a Process concept Memar should own at the concept level, stated domain-independently? — **Answered**
- **Question 2:** If it is not, is the absence a correct scoping decision that should be stated, rather than an omission? — **Answered**
- **Goal 1:** establish what Memar's live documents already own about decomposition, so that any proposal is a change to something existing rather than an addition beside it — **Met**
- **Goal 2:** determine whether the concrete per-feature artifact set a software pipeline needs belongs to Memar or to consuming projects — **Met**
- **Goal 3:** keep the per-feature artifact templates, the phase pipeline, and checkbox-as-progress out of Memar's own model, whatever the answer to Question 1 turns out to be — **Met**
- **Scope:** what Memar's `docs/` owns about decomposing a development, and whether the absence of a per-feature artifact set is scoping or omission. Excludes the content of any feature pipeline, the choice of task-tracking tooling, estimation and scheduling, and the identification of a working chat {ARROW} the last of these was split into [Documentation — Handoff Research 001](../../modules-plugable/knowledge/documentation/handoff/handoff.research.001.md) once it became clear that a session is a record rather than a Process concept.

## Participants
- [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — `Questioner`, `Goal-setter`; decided Questions 2 and 3
- [Space Bunny Alpha](../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../CONTRIBUTORS.md#opencode)) — `Researcher`, `Reviewer` (Approved, with the open questions recorded)

## Methodology
**Questions 1–3.** A single reasoning pass over Memar's live `docs/` on 2026-10-04, prompted by the adoption filter of [Comparison: Memar and GitHub Spec Kit](../../docs/comparisons/spec-kit.001.md), which recorded the absence as a finding rather than resolving it. The pass read the sections of [Process](./process.md) bearing on decomposition — *Process Composition*, *Process and Workflow*, *Development as a Process*, *State and Transition*, *Expectations and Checks* — alongside Test Practice → Scaling (`modules/process/test/test.practice.md`), [Knowledge → Task-Centric Knowledge Evolution](../knowledge/knowledge.md#task-centric-knowledge-evolution), [Documentation Changelog → Tasks](../../modules-plugable/knowledge/documentation/changelog/changelog.md#tasks), and [Software → The software life cycle](software/software.md). A regex search over the doc set for *Task* and for *Task* in definitional position tested whether the unit of work is defined anywhere. Question 3 was then put to the owner, who had held the position across earlier chats and had already anticipated it; his decision is recorded with his attribution and is not this research's reasoning.

**Question 5.** A separate pass, also on 2026-10-04, over the primary sources: RFC 9562 (UUID versions 1, 6, 7, 8 and §6 on distributed generation), the ULID specification, the KSUID README, the W3C Trace Context recommendation, Anthropic's published context-engineering article, the Claude Code session and architecture documentation, LangGraph's checkpointer and persistence documentation, the Jupyter client session implementation, tmux(1), `git interpret-trailers`(1), the Conventional Commits specification, GitHub's issue-linking documentation, `adr-tools`, the Twelve-Factor App's disposability section, and the specification project's own PowerShell sources. Each claim below carries its source; claims that are reasoning from a source are marked as such, and the sub-agent that gathered the external evidence was instructed to distinguish a source's statements from its inferences, which it did throughout.

**Known blind spots.** The project-management literature was not consulted for Questions 1 and 2, and that absence did not limit them because both were answered from Memar's own model rather than from prior art. Database session identifiers and `screen(1)` were not reached. Cursor's rules and memory documentation was unreachable, so that category of prior art is absent. Twitter Snowflake's own specification was unreachable from every URL attempted — its repository is archived with no layout in its README — so the commonly cited bit layout is **not** asserted anywhere below, and RFC 9562's mention of Snowflake among the prior implementations analysed for UUIDv6 and v7 is the only attribution made. The web search facility was unavailable for the whole external pass, so every finding comes from sources already known rather than from open discovery; a dedicated essay on either side of the ephemeral-state question was therefore not found, and the findings on that question are assembled from artifact-level evidence with that limitation stated.

## Findings
### Answering Question 1: the concept exists; what is missing is its standing
**Memar already owns decomposition, and owns it in the Test protocol rather than in Process.** Test Practice → Scaling (`modules/process/test/test.practice.md`) defines the unit directly: "The unit of this part is **one development step** — a piece of work whose expectations can be stated in one pass and whose enactment can then be checked: a function, a defect fix, a document section, a feature, a protocol contract, a piece of store equipment being designed. A larger development is decomposed into steps and each runs the cycle below. Scale changes how much the expectation states, never whether it is stated first." The list is itself the evidence that Memar's unit of work is already domain-independent: it spans a function, a document section, and a piece of store equipment in one breath (Space Bunny Alpha — claimed; **Evidence**: `test.practice.md:13`).

**The concept a decomposed development is made of already exists, so stating it adds no new structure.** [Process → Development as a Process](./process.md#development-as-a-process) holds that a development "has an intent (the target stage its model states), participants, activities and interactions, state (the current stage), and outcomes — all per the topics above", that it is "carried as an umbrella term — a word that names no content of its own", and that "its content here is therefore exactly the Process topics above" (Space Bunny Alpha — claimed; **Evidence**: `process.md`, *Development as a Process*).

**The relation a decomposition uses is already stated, and it is not a tree.** [Process → Process Composition](./process.md#process-composition) holds that "a process may contain or depend upon other processes, and composition does not require the composed processes to lose their independent identity" (Space Bunny Alpha — claimed; **Evidence**: `process.md`, *Process Composition*).

**The answer: yes, Memar should own it, as a promotion rather than an addition.** The fact is true of Memar already and lives in a protocol document that scopes it to its own cycle, where nothing else cites it. Promotion means Process states that a development decomposes into developments, each with its own intent, participants, state, and written expectations, and cites Test Practice → Scaling (`modules/process/test/test.practice.md`) for the operational form rather than restating it ([Documentation → Content Rule](../../modules-plugable/knowledge/documentation/documentation.md#content-rule-no-fabricated-or-redundant-provenance)). The promotion is one paragraph and changes no definition; the finding that it needs no new concept is what makes it safe (Space Bunny Alpha — argued).

**What the promotion must not bring with it.** Three things that travel with decomposition in every pipeline examined, and that Memar declines on grounds independent of this research: a named phase sequence, since [Process and Workflow](./process.md#process-and-workflow) holds that "a workflow may therefore be a useful representation of a process without becoming the definition of that process"; per-artifact templates, since [Documentation Explanation → Optional Sections](../../modules-plugable/knowledge/documentation/explanation/explanation.md) holds that "a separate independent template per document purpose tends to produce definitional drift over time instead"; and progress recorded in the artifact, since the medium is not where progress lives (Space Bunny Alpha — argued).

### Answering Question 2: the absence is a correct scoping decision, and it is already stated in three places
**The absence of a per-feature artifact set is entailed by positions Memar holds.** [Process and Workflow](./process.md#process-and-workflow) separates a process from a representation of it; [Modeling](../../docs/modeling.md) makes the model the primary architectural artifact and states that a modeling chat "ends by writing the documents that understanding produced"; [Documentation Explanation → Optional Sections](../../modules-plugable/knowledge/documentation/explanation/explanation.md) declines a template per purpose for the whole document system (Space Bunny Alpha — argued; **Evidence**: the three sections named).

**Memar still states the path; what it declines is the finished delivery.** [README → Where Memar Stops, and Where Work Continues](https://github.com/GeniusesGroup/memar/blob/dc3d1433/README.md#where-memar-stops-and-where-work-continues) separates the two: a framework that carries a concept can show every project the shape that concept requires, and cannot hand that project the built system without that becoming a product. The [Organization](https://github.com/GeniusesGroup/organization) project develops the identity and structural core the generated delivery is made from, and Memar's Enterprise scope is where a built answer is delivered. The earlier reading of this absence as a coverage gap was wrong on the substance (Omid Hekayati — claimed; Space Bunny Alpha — recorded).

**Therefore: the per-feature artifact set is not owed, and saying so is the change.** [Software → The software life cycle](software/software.md) records IEEE Std 1058 project management as "No home yet; owed". That word is right for project management as an activity a project runs and wrong if read as a Memar concept in waiting (Omid Hekayati — decided the framing; Space Bunny Alpha — argued).

## Open Questions
- **Should Process state the decomposition as a promotion now?** The fact is already true and filed in the wrong place, and a promotion is one paragraph citing `test.practice.md` rather than restating it. It touches a document other documents reference, so it is the owner's call.
- **Should the IEEE 1058 row in `software.md` be rewritten?** Its "owed" is right for project management as an activity and misleading read as a concept in waiting. No change has been made to that table.
- **Does a project wanting to build on this need the project-management prior-art pass?** The blind spot is named under Methodology and did not limit the answers given here.

### Answers, pending the owner's review
**Question 1 " answered yes, as a promotion.** The fact is already true of Memar and lives in Test Practice " + chr(0x2192) + " Scaling (`modules/process/test/test.practice.md`), cited by nothing. [Process](./process.md) should state that a development decomposes into developments, each with its own intent, participants, state, and written expectations, citing the practice rather than restating it. Not applied: it changes a document many others reference.

**Question 2 " answered: the absence is a correct scoping decision, already entailed.** The per-feature artifact set is not owed. [Software](software/software.md)'s IEEE 1058 row needs its "owed" qualified rather than deleted.

## Related Artifacts
- [Process](./process.md): Question 1's promotion and Question 4's placement. No change applied to either; both are the owner's.
- [Documentation Explanation](../../modules-plugable/knowledge/documentation/explanation/explanation.md): its `ID` section is the worked precedent for Question 5's "sort key, not name" distinction. No change needed.

- Test Practice (`modules/process/test/test.practice.md`): holds the definition Question 1 found already exists. A promotion cites it.
- [Terminology](../../docs/terminology.md): the word *Task*, which this inquiry found undefined and weighted, is settled there by a decision of the owner's and is no longer part of it.
- [Software](software/software.md): carries the "owed" entry Question 2 separates into a scoping decision.
- [README](../../README.md): gained the limits section whose framing corrected Question 2's answer.
- [Comparison: Memar and GitHub Spec Kit](../../docs/comparisons/spec-kit.001.md): recorded the absence and recommended this inquiry. Its §7 and §8 statements are now known to be one true half and one assigned half.

## Notes
This research reached a different answer than the comparison that prompted it expected. The comparison framed the gap as Memar lacking a capability a neighboring project has; the pass found the capability present and filed where nothing cited it, and the half genuinely absent assigned on purpose to a scope outside the framework. **Memar owns how a development decomposes; the Enterprise scope owns what the resulting unit of work is.** That division was not visible while the two halves were reported as one absence.

Two questions left this record. *Should a Memar document own a definition for the word Task?* was answered by the owner rather than here, and its outcome is in [Terminology " + chr(0x2192) + " A Term Deliberately Left Open](../../docs/terminology.md#a-term-deliberately-left-open). *Should a session be identified, and may a timestamp identify it?* turned out to be a question about a record rather than about the Process concept, and became [Documentation " + chr(0x2192) + " Handoff Research 001](../../modules-plugable/knowledge/documentation/handoff/handoff.research.001.md). Both left because pairing them here would have made this concept document answer for subjects it does not own.
