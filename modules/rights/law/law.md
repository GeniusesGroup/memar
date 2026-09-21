# Law

Law is the independent normative source determining which rights, obligations, and behaviors are possible, valid, forbidden, or enforceable.

## Principle (from the rights domain-boundaries proposal - awaiting review)

Law is **not an attribute of a right** (`Right -> law = ...` is the anti-pattern): it is an independent source that governs rights and contracts - alongside contract, court decision, and registration as other origins of rights.

## Open questions

- Law vs Rule: what is the boundary between a law here and the `modules/computer/rule` domain (executed vs normative)?
- Per-instance ratification vs inherited base law: see [the normative-bootstrap handoff](../normative-bootstrap.handoff.md) - do an organization's base laws need per-instance approval, or does accepting the platform's base laws count as the first law?
- The vote edges here (`vote-agree`, `vote-disagree`, `vote-abstention`, `widgets/election`) - do they satisfy the Consent side of the Law/Consent/Source-of-Authority split (see the normative-bootstrap handoff), or is Consent still unmodeled?

- Law status proposal (raw comment): Closed, Denied - where do law states live (status domain, or law-status edges)? Reconcile with the normative-bootstrap handoff (amendment/repeal of base law) and the Code/Rule temporal-validity question.