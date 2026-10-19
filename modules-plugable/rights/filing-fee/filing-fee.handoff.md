# Filing fee Handoff

## Topic & Purpose
Open state for [filing-fee.md](filing-fee.md), the pluggable rule that states what a filer is charged around a case. The case structure does not hold the price.

## Status
Active. The module has a home and no formula.

## Open Questions

1. **Which recorded quantities does the fee rule read?** [filing-fee.md](filing-fee.md) names one input it can read, the maximum a party states it will pay, and it says the numeric thresholds are examples for pluggable policy rather than a formula. No list of the recorded quantities a fee schedule is built from exists in this repository. An implementer therefore has no input list to write a schedule against. Matters because the module was given a home precisely so that organizations can differ in schedule; a schedule with no declared inputs is not that. Blocks any concrete schedule, and blocks the decision on whether the fee is one module or several.

## Assumptions
- **Weak.** That the maximum a party states is the only input. It is the only one recorded, which is not the same as being the only one.

## Related Artifacts
- [filing-fee.md](filing-fee.md) — Review. Its Open questions section holds only the rank term, which is closed.
- [judge-assignment.md](../judge-assignment/judge-assignment.md) — Review. Who sits, and what it costs, vary for different reasons; the two modules share the accept-or-decline of a cap.

## Notes
- This question was number 10 of the pilot synthesis and number 11 of the pilot model draft. It was never closed and no repository document carried it.
