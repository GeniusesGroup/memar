# Approval Rules (`modules-plugable/knowledge/documentation/approval/rules/`)
Rules for how an approval is asked for, read and recorded. The general Memar concept of Rule is defined in [`modules/process/rule/rule.md`](../../../../../modules/process/rule/rule.md); a Rule is held by the module that owns its subject ([Rule → Which Module a Rule Belongs To](../../../../../modules/process/rule/rule.md#which-module-a-rule-belongs-to)), and the subject here is [Approval](../approval.md).

| Rule | Subject | Tier | What it is |
| --- | --- | --- | --- |
| [An Approval Earns Its Cost When a Command Can Falsify the Claim](./approval-earns-its-cost-when-a-command-can-falsify/approval-earns-its-cost-when-a-command-can-falsify.md) | When to ask for an approval | Governance | Ask where a command can show the claim false; a claim reading decides rarely earns the second party |
| [A Review Request Has Four Parts](./review-request-has-four-parts/review-request-has-four-parts.md) | What a request to a reviewer carries | Governance | Claim, evidence, boundaries and the verdict asked for, and no more |
| [A Verdict Is a Finding, Not a Gate](./a-verdict-is-a-finding/a-verdict-is-a-finding.md) | How a verdict is read and recorded | Governance | Permitted, withheld with a reason, or withheld because the evidence was wrong |
| [Changed Work Gets a New Reviewer](./changed-work-gets-a-new-reviewer/changed-work-gets-a-new-reviewer.md) | Who reviews work changed after a review | Governance | A reviewer that has seen the claim is not asked again |
| [No Second System, No Approval](./no-second-system-no-approval/no-second-system-no-approval.md) | What counts as a reviewer | Governance | A second cognitive system, never a second pass by the first |
| [Approved Means Checked, Not Correct](./approved-means-checked-not-correct/approved-means-checked-not-correct.md) | What a reader may take from an approval | Governance | A second party checked; it does not certify correctness |

The Rules are governance-tier and are enforced by no check this repository runs today; an organization adopting this repository's Rules may keep, relax, or replace any of them without forking anything.
