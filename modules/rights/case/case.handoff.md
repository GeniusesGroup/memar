# Case Handoff

## Topic & Purpose
The graded enforcement/coercion capability question: whether the ability to restrict another party's freedom of action (detaining a person, enforcing settlement of a debt) is a government-exclusive attribute or a graded capability any organization can hold in different scopes. Raised during tax-modeling/enforcement discussion; explicitly deferred to a dedicated chat.

## Status
Paused - deferred to a dedicated session; the core claim is untested.

## Decisions
None. The working hypothesis is under exploration:
- **Enforcement/coercion capability is a graded capability or permission scope** attached to an Organization (via certification, legal registration type, or explicit grant) - analogous to privilege rings in an OS kernel - rather than being hardcoded as an attribute exclusive to a "government" label (Tentative).
- **Core claim behind it**: small organizations (building security guard, private security company, a shop owner dealing with a dine-and-dash customer) exercise restricted forms of this capability today, implemented informally (paper records, ad hoc process) only because no affordable unified software made it explicit - not because they do not need it (Tentative).

## Ambiguities Resolved
- "Enforcement" is not a government monopoly by nature - resolved as a modeling question (graded scopes), though the legal boundaries per jurisdiction remain open.

## Open Questions
1. What determines the scope/ceiling of an organization's enforcement capability (a building guard can detain briefly and must hand off to police; a government has broader and different constraints like courts and due process)? - **blocks** the capability model.
2. Is this capability an edge property, a separate node type (a "Mandate" or "Authorization" node), or something else? - **blocks**.
3. Interaction with Code/Rule separation - hypothesis so far: the *existence* of an enforcement-capable edge/relationship is Code; the specific limits, due-process requirements, and escalation paths are Rule. Does not block, but shapes the split.

## Assumptions
- **Privilege-ring analogy transfers from OS kernels to organizational enforcement** - stability: Weak; motivating metaphor, not verified against legal reality.
- **Certification/registration type can serve as the grant mechanism** - stability: Unexamined; connects to the certificate concept in the estate discussions.

## Key Definitions Established
- Enforcement/coercion capability (working): the ability to restrict another party's freedom of action, existing in graded scopes across organization types.

## Proposed Next Steps
1. Run the test scenarios below against a candidate model (edge property vs Mandate node), one graph sketch each.
2. Decide the Code/Rule split for limits and escalation.
3. Reconcile with the rights-domain-boundaries work (Authority != Permission; does enforcement capability derive from Authority, Law, or registration?).

Test scenarios the model must pass:
- A residential/commercial complex guard detaining a dangerous individual temporarily
- A restaurant handling a customer who refuses to pay
- A government enforcing tax collection
- A private security company under contract to a business
- An online platform banning/suspending a user account (a "soft" form of restriction)

## Related Artifacts
- [`Readme.MD`](Readme.MD) - the Case domain this capability interacts with (Review during the session)
- [`../../computer/rule/README.md`](../../computer/rule/README.md) - Code/Rule separation (None)
- [`rights-domain-boundaries.handoff.md`](../rights-domain-boundaries.handoff.md) - Authority/Permission split (Related)
- Memar `docs/modeling.md` -> Separating Structure (Code) from Policy (Rule) (None)

## Notes
- The original context note (edges/topic-coercion-graded-capability.md) is retired into this handoff; its stale references (topic-case-dispute-domain.md, rfc-code-rule-separation.md) pointed to documents that have since moved - the current homes are this module's Readme.MD and the rule README respectively.
