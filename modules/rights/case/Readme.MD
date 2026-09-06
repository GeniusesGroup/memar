# Case

## rules
- Judges just set arbitrator for contracts and follow the case for any law broken situations.

## Domain status and naming
The Case / Dispute Resolution domain is only partially modeled. Candidate umbrella name: `Case`. It is explicitly NOT directly connected to `Organization` — it connects to transactional domains like `Invoice` instead.

Key principle already established: avoid words that imply certainty/finality (e.g., "final ruling", "settled") unless the state they describe is modeled with an explicit state machine. Real-world legal outcomes labeled "final" are frequently not actually final — e.g., a third party's claim can overturn a supposedly final ruling years later, even under legal doctrines (such as Iranian law) that formally use the word "final" (qat'i). Modeling must use precise, revisable states rather than terminology suggesting permanence.

Related but distinct: the enforcement/coercion capability question (who can enforce an outcome and to what extent — see [topic-coercion-graded-capability.md](edges/topic-coercion-graded-capability.md)) is separate from the dispute-resolution *process* modeled here.

### Open questions
- What triggers the creation of a Case node (a disputed Invoice, a violated Rule, something else)?
- What are the possible states of a Case, and what transitions between them are valid?
- How does a Case reference the Rule(s) allegedly violated, given the Rule temporal-validity question is unresolved (Memar `docs/modeling.md` → Separating Structure (Code) from Policy (Rule))?
- How does resolution of a Case interact with the enforcement-capability model?
- Contradiction to resolve: this domain was recorded as "not yet modeled", yet `edges/` already contains `kidnap`, `stolen`, `illegal`, `settlement_for` and case-relation types. Are those a started model, placeholders, or misplacements?