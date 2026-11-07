# Hiring pipeline

## Model

- Candidate (unconfirmed): hiring-interview pipeline labels (source was a label-only file, no edge code): Requester, Referral, Talent ("high skill match"), Need/Approve pairs for HR / Technical / Manager / Chief / Board interviews; rejection cooldowns LockFor1Month / LockFor3Month / LockFor6Month / LockFor12Month; acceptance steps Designation, Negotiation, Reserved, ContractProposal.
- Target node unconfirmed — labels read as annotations on a hiring Task or on the staff-candidate relation, not as a standalone edge.

## Policies (rules)

- Interview stages pair need with approval: `NeedHRInterview`/`ApproveForHRInterview`, `NeedTechnicalInterview`/`ApproveForTechnicalInterview`, `NeedForManagerInterview`/`ApproveForManagerInterview`, `NeedForChiefInterview`/`ApproveForChiefInterview`, `NeedForBoardInterview`/`ApproveForBoardInterview`.
- "if not accepted or hired" → `LockFor1Month`, `LockFor3Month`, `LockFor6Month`, `LockFor12Month` — re-application cooldowns.
- "if accepted" → `Designation`, `Negotiation`, `Reserved`, `ContractProposal`.

## Placement

- **Correct here — the hiring pipeline is the staff capability's own vocabulary** (module skeleton: `staff/edges/`; only staff gives these labels meaning; prefer existing homes over inventing new modules).
- The Need/Approve pairs encode *who approves which interview round* — organization policy → rules (core never knows Rule), not pipeline-kernel code; the labels may stay as the pipeline's recorded shape while the approvals themselves live as rules.
- Cooldowns are time-bound re-application policy (same shape as other time limits): policy material, not staff-identity semantics; no dedicated module (parameters-vs-semantics).
- Not [task](../../../task/task.md) kernel: hiring stages describe the staff capability; whether the pipeline *runs on* a hiring Task is an open shape question, not a home-transfer.
