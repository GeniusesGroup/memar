<!--
  NOTE: this is a seed document, not a finished specification. It carries the
  knowledge-management DISCIPLINE content extracted from Memar's documentation
  on 2026-09-05, when `docs/knowledge-management.md` was renamed (pure `git mv`,
  commit `2dc8576`, history preserved) and re-scoped to `docs/knowledge.md`
  (the concept). The concept and the modeling principles live in Memar
  (https://github.com/GeniusesGroup/memar/blob/main/docs/knowledge.md);
  THIS document is the intended home of knowledge management as an organizational
  practice — creation workflows, tacit-to-explicit conversion, sector adoption,
  and change management. It is a placeholder to be picked up and actually
  designed in a dedicated session (the pending "Organization project" obligation
  recorded in Memar's docs/knowledge.changelog.md).

  Provenance & recovery:
  - Full decision provenance: Memar `docs/knowledge.changelog.md` (2026-09-05
    entries: rename, re-scope, purpose chain in `docs/framework.md`, cross-links
    retargeted in `docs/system.md`, `docs/thinking.md`, `docs/agency.md`,
    `docs/protocols/filesystem.md`).
  - The seed below is a DISTILLATION. The full generalized cross-domain
    framework this was extracted from — the nine principles fully developed,
    cross-domain comparison tables, software-specific section, prior art, Q&A,
    and all citations — is recoverable from Memar's git history:
    `git show 4b8fc31:docs/knowledge-management.md`.

  Convention (from the transfer session, 2026-09-05): never cite chat-context
  folders (Memar `chats-context/`, this repo `____Chats/`) from any document
  body — they are ephemeral working state and are gitignored or transient by
  design. Everything durable from working sessions must land in real documents.
-->

# Knowledge Management in Organizations

## Status
Seed — extracted content awaiting a dedicated design session. Not yet structured to Memar's Explanation-facet template (Memar's documentation rules and facet specs are defined in Memar `docs/documentation.md`; this repository's existing docs use lighter "context note / seed" conventions — see the `topic-*.md` and seed files across the module folders).

## Framing claim (to be argued, not assumed)
**Knowledge management failure is the root cause of most organizational dysfunction** — not process inadequacy, not tooling gaps, not communication problems per se. This claim was carried out of Memar's concept document on 2026-09-05 because it is an *organizational* claim, and the Organization project is where it can be argued against real organizational models (departments, roles, staff, tasks, meetings — the `management/*` and `identity/*` modules) rather than asserted.

The claim must be re-grounded here as a falsifiable proposition: what would count as organizational dysfunction, what would count as its root cause, and what evidence would show KM failure is *not* the root cause in a given case.

## What Memar already owns (do not restate — link)
- The concept of knowledge and the Data → Information → Knowledge → Document hierarchy: Memar `docs/knowledge.md` → Definition.
- The nine modeling principles (storage ≠ content, identity independent of location, first-class relationships, projection ≠ model, task-centric evolution, context recovery, multi-hierarchy classification, communication ≠ repository, fine granularity): Memar `docs/knowledge.md` → Principles for Modeling Knowledge.
- The concept's place in Memar's web, with the scope boundary ("the organizational discipline belongs to the Organization project"): Memar `docs/knowledge.md` → Knowledge in Memar's Concept Web.
- The purpose chain — knowledge (material) → thinking (activity) → intelligence (quality) → agency (exercise) → goals (beyond the chain, e.g. quality of life) — and Memar's goal statement ("Memar is a system that can, across a wide range of cognitive tasks and without task-specific training for each problem, build a reliable model of reality, revise it with new evidence, and reason and decide independently toward a goal"): Memar `docs/framework.md` → Memar's Purpose Space: From Knowledge to Agency. (No standalone `intelligence.md` exists — intelligence is an output relation of the other concepts, per the Science-inline-in-system.md precedent.)
- Agency's dependence on shared knowledge and Cognitive Debt: Memar `docs/agency.md` → Agency and Knowledge Management.
- The discourse norms governing how knowledge material travels between thinking systems: Memar `docs/thinking.md`.
- The questioning/research/evaluating procedures (kept in Memar deliberately — thinking disciplines, not organizational ones; revisit this split if the dedicated session turns out to need them here): Memar `docs/knowledge.practice.md`.

This document's subject is what an *organization* does with those constraints: how knowledge is created, converted from tacit to explicit, preserved across personnel transitions, discovered by the members who need it, and revised as evidence changes — as practice, workflow, and organizational structure.

## Reading order for the dedicated session
1. This seed (below) — the extracted organizational content.
2. Memar `docs/knowledge.md` — the concept home; especially *Knowledge in Memar's Concept Web* (scope boundary) and the nine principles.
3. Memar `docs/agency.md` → *Agency and Knowledge Management* and *Cognitive Debt* — why collective agency depends on shared knowledge.
4. Memar `docs/framework.md` → *Memar's Purpose Space* — where knowledge sits in the goal chain.
5. Memar `docs/knowledge.practice.md` — the kept-in-Memar thinking procedures.
6. Memar `docs/knowledge.changelog.md` — full decision provenance and the pending obligation this document must discharge.

## Extracted content (verbatim from the Memar document, pending redesign)

### The Knowledge-Creating Company as process model
Nonaka & Takeuchi's SECI model (Socialization, Externalization, Combination, Internalization) established knowledge as a dynamic, social process rather than a static asset. The organizational machinery — how tacit knowledge converts to explicit and back, and how that conversion is made measurable — is this document's core subject once designed. Operationalizations with measurable dimensions for KM assessment exist in the literature (see References).

### Sector application patterns

#### Healthcare
- **Tacit knowledge loss**: experienced clinicians carry procedural and diagnostic knowledge that leaves when they retire. The "tricks of the trade" that distinguish adequate from excellent care are rarely documented.
- **Information silos**: patient data exists in EHRs, lab systems, imaging archives, pharmacy systems, and paper notes — often poorly integrated.
- **Protocol compliance vs. clinical judgment**: balancing standardized protocols (explicit knowledge) with individualized care (tacit knowledge application).
- **Handoff failures**: critical knowledge lost during shift changes, patient transfers, and care setting transitions.
- Principle applications: stable identifiers across systems (identity ≠ location); morbidity-mortality conferences, tumor boards, and case reviews ARE task-centric knowledge evolution; treatment orders should link to clinical reasoning, differential diagnosis, and evidence base (context recovery).

#### Education
- **Tacit knowledge in teaching**: master teachers possess pedagogical intuition, classroom management techniques, and student engagement strategies that resist formal documentation.
- **Curriculum fragmentation**: learning objectives, assessments, and instructional materials exist in disconnected systems.
- **Faculty turnover**: departing faculty take course designs, research directions, and institutional knowledge with them.
- **Assessment-to-learning disconnect**: grades (documents) substitute for understanding of student learning (knowledge).
- Principle applications: a learning resource belongs simultaneously to subject area, grade level, prerequisite chain position, and assessment alignment (multi-hierarchy classification); faculty meetings and office hours produce valuable knowledge that should be captured without burdening participants (communication extraction); individual learning objectives, misconceptions, and teaching techniques are the atomic units (granularity).

#### Manufacturing
- **Operator expertise**: veteran operators possess machine intuition, troubleshooting heuristics, and process optimization knowledge developed over years.
- **Process-documentation gap**: SOPs rarely capture how experienced operators actually handle edge cases.
- **Quality knowledge dispersion**: root causes, corrective actions, and lessons learned spread across quality systems, maintenance logs, and operator experience.
- **Supply chain knowledge**: supplier capabilities, material specifications, and logistics knowledge distributed across procurement, engineering, and operations.
- Principle applications: a part-number hierarchy (storage) is not a process knowledge map (content); Root Cause Analysis, 8D reports, and kaizen events ARE task-centric knowledge evolution; bill-of-materials containment is one relationship among many — process sequences, failure-mode links, and supplier dependencies deserve first-class representation. Lean KM adds waste reduction in knowledge processes and continuous improvement.

#### Legal
- **Precedent management**: finding relevant prior cases, motions, and arguments across matters and attorneys.
- **Expertise location**: knowing which lawyer has experience with specific issues, judges, or opposing counsel.
- **Matter continuity**: when attorneys leave or matters transfer, preserving strategic context and client history.
- **Research duplication**: multiple researchers investigating the same legal questions across matters.
- Principle applications: legal citations are content-derived identifiers stable across databases (identity ≠ location); precedent citation, jurisdictional authority, argument support/opposition, and attorney expertise are critical relationship types beyond matter-document containment; a filed brief should preserve the strategy memo, partner comments, rejected arguments, and client instructions (context recovery).

#### Small and Medium Enterprises
- **Informal knowledge culture**: knowledge resides entirely with founders or key employees, undocumented and unstructured.
- **Resource constraints**: limited budget for dedicated KM tools or personnel.
- **Scale-appropriate solutions**: enterprise KM systems are oversized for small teams; ad-hoc solutions are fragile.
- **Succession risk**: founder or key employee departure can devastate organizational knowledge.
- Adoption path (incremental, no new infrastructure required): stable identifiers for important artifacts; five minutes after each project/client/matter recording what was decided and why (task-centric history); summarizing important decisions out of email threads into persistent records (communication extraction).

### Organizational questions this document must answer
1. How do these practices apply in highly regulated industries (healthcare, legal, finance), where compliance mandates certain records — and those records are DOCUMENTS in Memar's framework, whose contextual richness KM practice must preserve?
2. How do SMEs with limited resources adopt the principles incrementally?
3. "Who has time for this? We have patients to treat / students to teach / cases to win / products to ship" — the answer: organizations are ALREADY spending time on knowledge management, inefficiently. Time spent searching, relearning what someone else knows, repeating mistakes, and onboarding replacements IS KM failure cost.
4. How do cultural factors (national culture, professional norms, organizational climate) affect adoption — do the practices need cultural localization?
5. How does an organization promote a conversation thread into a structured Task, extract a Decision into a recorded artifact, and link a casual discussion to a formal Concept Definition — as workflow, in the actual `management/task`, `management/meeting`, `knowledge/*` module structures of this repository?

## Open design questions (for the dedicated session)
- How the KM practices map onto this repository's existing modules — `knowledge/*` (content, knowledge_unit, question, answer, skill, label, status) and `management/*` (task, meeting, timeline, staff, department), plus `identity/organization`. The modules already instantiate parts of Memar's principles; the document should describe practice in terms of the real model, not in the abstract.
- Whether "Knowledge Management" is one document or a family (creation, preservation, discovery, revision) once designed.
- Where the organizational claim ("KM failure is the root cause of most organizational dysfunction") is argued: here, or in an analysis document with evidence from the modules.
- Memar's changelog records this document as a `Propagates to: Pending` obligation (2026-09-05): the dedicated session that turns this seed into a real document discharges it — when done, the obligation should be marked Done in Memar's `docs/knowledge.changelog.md`.
- **The tool gap (from the 2026-08-04 Task Management chat)**: the actual pain observed during knowledge development is not model quality but the interaction model of current chatbots ("Prompt → Response"), which forces the human to carry context between agents and to manage multi-step document production by hand. The hypothesized shape of what is missing — an **AI-native Knowledge Development Environment** (neither IDE, chat, wiki, nor task manager, but a combination): concepts with status and stakeholders, affected-documents links, open questions, and agent contributions landing as artifacts instead of chat messages. Larger context windows do not solve this (which idea was finalized? which is still contested? which document does a decision affect? are KM questions, not context questions), and multi-agent frameworks (AutoGen/CrewAI/LangGraph-class) target task execution, not knowledge-lifecycle management. This session should decide whether that environment is in scope for this project or remains an external tool requirement.

## References (carried from the Memar document's citations; verify before relying)
- Nonaka & Takeuchi, "The Knowledge-Creating Company" (HBR, 1991) — SECI model.
- "Key success factors of knowledge management systems for optimizing organizational performance" (Heliyon, 2025).
- "Organizational Knowledge and Knowledge Management — A New Framework" (2024).
- "Managing Knowledge in Organizations: A Nonaka's SECI Model Operationalization" (PMC, 2019).
- "Knowledge Management in Health Organizations: A Systematic Literature Review" (2025).
- "Knowledge management and higher education institute: Review" (2024).
- "14 Steps Toward Lean Knowledge Management" (2022).
- "Knowledge Management in Small and Medium Enterprises: A Systematic Literature Review" (JKM, 2024).
- "The Implementation of Knowledge Management in Health and Social Care Organisations" (PMC, 2025).
- "Tacit Knowledge Sharing in Educational Organizations" (Toknow Press).
