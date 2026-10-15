# Forked Sub-Agent Changelog

## Changelog

### Initial draft — the expectation of a forked sub-agent, its cost, and four open questions
- Time: 2026-10-13T06:30:00Z
- Type: Added
- Cited:
  - [../../../agency.md](../../../agency.md) - Depends_on: delegation and Context are consumed there; the fork is a delegation whose handed Context is the delegator's own.
  - [../../../cognition.md](../../../cognition.md) - Depends_on: the claim status of a child's answer and the unverified reading a child inherits.
  - [../../../modeling.practice.md](../../../modeling.practice.md) - Depends_on: the workflow the document was modeled by.
  - [../README.md](../README.md) - Depends_on: the membership criterion that places it.
- Propagates to:
  - `.agents/skills/memar/SKILL.md`: Done - the Delegation section links this document.
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) - requested; stated the expectation (fork from a point, shared cached prefix, answers only, further waves from earlier points) and drafted the request to the runtime's maker
  - [Claude](../../../../CONTRIBUTORS.md#claude) (Sonnet 5.5 via Claude Code) - claimed, modeled, drafted

#### What changed
- Created [forked-subagent.md](./forked-subagent.md): the five-part expectation, the concepts (parent, fork point, child, wave, answer, shared prefix), the split between what the runtime owns and what Memar owns, the cost reasoning in terms of write and read prices, and what Memar does until a runtime offers it.
- Created the paired handoff carrying the four questions from the owner's draft request, a placement question, and the owner's sending of that request.

#### Considered and not done
- **A category of Memar's modules (rejected)**: the subject is a runtime Memar does not own, so [the Modules criterion](../../README.md#membership-criterion) sends a position on it to `lib/`.
- **Vendor prices in the document (not done)**: figures are the runtime's to publish and change; the cost is stated in symbols, with a worked example left to the handoff.
- **Changing the skill's delegation test (not done)**: it is written for cold starts and stays so until a fork exists to learn from; the skill only links this document.
