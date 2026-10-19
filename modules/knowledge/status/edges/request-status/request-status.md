# Request states

## Model

- Candidate (unconfirmed): request states — Approving (awaiting approval), Rejected, Processing (in progress/pending), Processed (completed), Failed, Canceled, Compensated.

## Policies (rules)

- Approving: awaiting approval. Processing: in progress or pending. Processed: completed. Also recorded: Rejected, Failed, Canceled, Compensated. No transition rule is recorded.

## Placement

- These names are filed on the status module.
- [status.md](../../status.md) puts a domain's own statuses on that domain. These names describe a request lifecycle, so the request module is the other candidate home.
- The doc stays here until that is decided. Whether Compensated is the transaction-side link is the open question below.

## Open questions

- reconcile with memar process/request lifecycle; is Compensated the transaction-side link ([transaction.handoff.md](../../../../economics/transaction/transaction.handoff.md) §6)?

