# Law Normative Bootstrap Handoff

## Topic & Purpose
The philosophy-of-law problem the organization software's own architecture creates: when a new organization is founded *inside* the software, the founding process runs on the software's concepts (the agreement to start — even the name-choosing — would be Tasks with recorded positions and a vote), so the software effectively imposes its concepts as the founding fabric of every new organization. The disputed step: offering the platform's ratified base laws ("you accept the base laws of Geniuses.Group?") as an instance's first law. From the Task Management chat (2026-08-05).

## Status
Blocked on modeling Authority/Legitimacy — the bootstrap question reduces to it.

## Decisions
None ratified. The working decomposition is a hypothesis:
- **Law / Consent / Source-of-Authority must be modeled separately** (Explored-but-unresolved): the same base-law text can enter an organization through different authorities — platform inheritance, statute, external standard, or internal consensus — with different consequences. Modeling Law without Authority would bake one legitimacy story into every organization (the vocabulary-discipline failure pattern).
- Worked bootstrap shape (Explored-but-unresolved, step 3 disputed): instance opens → founding agreements recorded in-software (Tasks, votes) → platform base laws offered as starting identity → instance develops its own laws. Step 3 is simultaneously convenience, legitimacy inheritance, and the software's concepts becoming constitutionally prior.

## Ambiguities Resolved
- "Do base laws need per-instance ratification?" — resolved into a better question: it is not a software question but a Source-of-Authority question; the instance declares *which authority* it accepts norms from, and platform inheritance is merely one choice.

## Open Questions
1. Minimal model of **Authority/Legitimacy** — node type in rights? Edge class? (Candidate: `(norm)-[:authority_is]->(thing)`.) — **blocks** the bootstrap design.
2. Is Consent always an Agreement (contract sense) or sometimes a weaker record (a vote artifact)? — **blocks** representing founding acts.
3. Can an instance amend inherited base law — self-amendment from the base law itself, or separately established authority? — does not block the founding model.
4. Does the software represent state-legal existence at all, or only internal normativity? — shapes the whole bootstrap; revisit before design.
5. Chicken-and-egg: full per-instance ratification presupposes an instance can legislate before having any authority structure — the untangling this topic exists for.

## Assumptions
- **Platform-inherited base law risks becoming an unexamined constitution** (reflexive acceptance = consent without legitimacy) — stability: Strong (matches known DAO founding failure modes).
- **A "founding act" artifact** (recorded agreements/votes sequence, with the declared authority linked) will be needed — stability: Weak; untested.

## Key Definitions Established
- Law: the norm itself. Consent: an actor's acceptance of a norm. Source of Authority (Legitimacy): where the norm's binding force comes from. (Working decomposition — not yet ratified anywhere.)

## Proposed Next Steps
1. Model the minimal Authority/Legitimacy concept (open #1) — the gate for everything else.
2. Decide the Consent representation (open #2) against the existing contract and law vote edges.
3. Then revisit the bootstrap question as "which Authority does this organization declare as its Source of Norms".

## Related Artifacts
- [`README.md`](README.md) — module home (Update when the decomposition is ratified)
- [`law/README.md`](law/README.md) — Law's independent-source principle + vote edges (Review)
- [`contract/README.md`](contract/README.md) — Agreement/Consent side (Review)
- [`rights-domain-boundaries.handoff.md`](rights-domain-boundaries.handoff.md) — the broader rights map this sits in (Related)
- [`../management/task/edges/task-concept.md`](../management/task/edges/task-concept.md) — unresolved #11 mirrors this topic (None)

## Notes
- Prior art: social contract theory (Consent/Authority split), corporate formation law (standard-form constitutions = platform inheritance precedent), DAO on-chain constitutions (failure modes), ISO-style external-norm adoption.
- The source chat is retired; everything durable is here.
