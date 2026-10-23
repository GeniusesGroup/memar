# Dideban Handoff

## Topic & Purpose
Physical security/protection requirement modeling: whether protection is a shared requirement across organizations of vastly different scale (a few-square-meter shop vs a multi-hundred-floor complex), with the requirement itself identical and only execution scale differing - comparable to Android vendors sharing one kernel and differing in GUI/vendor layer. Raised as an example in the shared-requirements discussion; not yet modeled.

## Status
Paused - flagged for a dedicated chat; nothing modeled.

## Decisions
None. The claim under exploration:
- **Physical protection is a shared base requirement** whose process set should become formal (as Code and/or Rule), with scale/vendoring as configuration on top (Tentative).
- Scoping caution (Tentative): hardware/software bundling considerations are a market/delivery observation and must be kept separate from the graph model discussion.

## Ambiguities Resolved
- "Physical protection is not just install a CCTV camera" - resolved into a process view: the requirement implies a set of processes needing formalization: incident detection and classification; notification/escalation workflow; possible handoff into the Case/Dispute domain if an incident involves a person; possible handoff into the enforcement-capability model if physical restraint is involved.

## Open Questions
1. What is the minimal shared process set (Code) across all organization sizes for this requirement? - **blocks** modeling.
2. Which parts legitimately vary by organization/jurisdiction/scale and should be Rule rather than Code? - **blocks**.
3. Does this domain need its own node type, or does it decompose entirely into existing domains (Case, enforcement capability, notification/Content)? - **blocks** the module boundary.

## Assumptions
- **The Android kernel/GUI analogy holds** (same requirement kernel, scale-dependent vendor layer) - stability: Weak; motivating, unverified.
- **Existing domains can absorb most of it** (Case, enforcement capability, notification) - stability: Unexamined; the third open question tests it.

## Key Definitions Established
None yet - "physical protection" itself still needs a working definition before the Code/Rule split can be discussed.

## Proposed Next Steps
1. Define a working definition of physical protection (process inventory, not hardware inventory).
2. Draft the minimal shared Code set; mark scale-varying parts as Rule candidates.
3. Test decomposition into existing domains before admitting a new node type.

## Related Artifacts
- [`README.md`](README.md) - the Dideban bundle home (Update when the domain boundary is decided)
- [`../../modules/rights/case/case.handoff.md`](../../modules/rights/case/case.handoff.md) - enforcement-capability and Case handoffs (Related)
- [`../../modules/computer/rule/README.md`](../../modules/computer/rule/README.md) - Code/Rule split (None)

## Notes
- The original context note (topic-physical-security-requirement-modeling.md) is retired into this handoff; its references to topic-case-dispute-domain.md and topic-coercion-graded-capability.md point to documents that have since moved (Case Readme.MD and the case handoff respectively).
