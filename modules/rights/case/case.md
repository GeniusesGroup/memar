# Case

## rules
- Judges just set arbitrator for contracts and follow the case for any law broken situations.

## Kinds of case
This domain is the dispute node. A kind of dispute — theft, a conflicting law, an update of a law — is not part of that node. Those edges are optional and live in [claims](../../../modules-plugable/rights/claims/claims.md). An organization includes the ones it hears.

## Domain status and naming
The Case / Dispute Resolution domain is only partially modeled. Candidate umbrella name: `Case`. It is explicitly NOT directly connected to `Organization` - it connects to transactional domains like `Invoice` instead.

Key principle already established: avoid words that imply certainty/finality (e.g., "final ruling", "settled") unless the state they describe is modeled with an explicit state machine. Real-world legal outcomes labeled "final" are frequently not actually final - e.g., a third party's claim can overturn a supposedly final ruling years later, even under legal doctrines (such as Iranian law) that formally use the word "final" (qat'i). Modeling must use precise, revisable states rather than terminology suggesting permanence.

Related but distinct: the enforcement/coercion capability question (who can enforce an outcome and to what extent - see [case.handoff.md](case.handoff.md)) is separate from the dispute-resolution *process* modeled here.

### Open questions
- What triggers the creation of a Case node (a disputed Invoice, a violated Rule, something else)?
- What are the possible states of a Case, and what transitions between them are valid?
- **Does Liability live here?** (from the rights domain-boundaries proposal - awaiting review): the chain `Event --gives_rise_to--> Liability --creates--> Obligation` connects a damaging event to an obligation and then to a transaction. Is Liability a case/judiciary matter owned by this domain, or a rights-level concept that cases merely *establish*? The chain would connect rights, process, and accounting without collapsing them - decide who owns each link.
- How does a Case reference the Rule(s) allegedly violated, given the Rule temporal-validity question is unresolved (Memar `docs/modeling.md` -> Separating Structure (Code) from Policy (Rule))?
- How does resolution of a Case interact with the enforcement-capability model?
- **Settlement for, and case-relation-user.** Particular accusations now live in [claims](../../../modules-plugable/rights/claims/claims.md). [Settlement for](edges/settlement_for/settlement_for.md) still names what a dispute settles. Is that part of this type, or another optional kind? `case-relation-user.go` still sits in this folder.
