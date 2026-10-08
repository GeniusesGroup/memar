# Filing fee
What a filer is charged around a case. The case structure does not hold the price.

## Model

- No fee field on the case.
- This module owns the rule that states the charge. The charge, when it is money, is a transaction in the economics domain. This module does not define the transaction.

## Policies (rules)

- There is no cap on creating cases.
- Until the party accepts the full fee, only the fixed system fee is charged. That charge is the brake on empty cases.
- Adjudication cost is judge person-hours plus a fixed system fee.
- A party may state a maximum they will pay. A judge may accept that cap or decline the seat. Declining the seat is assignment, recorded on [judge assignment](../judge-assignment/judge-assignment.md). The maximum is an input this module can read. Declining a seat is not the same act as stopping the case because wealth ran out.
- There is no wealth cap on how long a party may continue. Continuation depends on the vote margin. The numeric thresholds are examples for pluggable policy. They are not a fee formula.
- Specialty, rank, and fee are self-declared and must carry evidence. Not an exam and not a badge. The kernel does not compute the fee from rank. The pattern is wider than judges. A music mentor is his example. This module does not model that wider pattern.
- The case structure (parties, service, votes, ruling shortcut) does not change when the schedule changes.

## Placement

- **Pluggable, under `modules-plugable/rights/`.** The fee is a condition on filing and on adjudication. Organizations differ in the schedule without rewriting the case.
- **Nearest alternative rejected:** a kernel fee formula on the case. A formula in the kernel would freeze one schedule into every organization.
- **Nearest alternative rejected:** a count of cases as the brake. The brake is the fixed system fee charged before the party accepts the full fee.
- **Not** [judge assignment](../judge-assignment/judge-assignment.md). Who sits, and what it costs, vary for different reasons. The judge's accept-or-decline of a cap is the boundary the two modules share.

## Open questions

- None for a rank term in the fee. The fee is the declared fee, with evidence. A new judge entering outside the seated count is an example, not a rule of this module.
