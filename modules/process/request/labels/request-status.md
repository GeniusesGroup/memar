# Request states

## Model

- Candidate (unconfirmed): request states — Approving (awaiting approval), Rejected, Processing (in progress/pending), Processed (completed), Failed, Canceled, Compensated.

## Policies (rules)

- Approving: awaiting approval. Processing: in progress or pending. Processed: completed. Also recorded: Rejected, Failed, Canceled, Compensated. No transition rule is recorded.

## Placement

- These names are filed on the status module.
- `status.md` puts a domain's own statuses on that domain. These names describe a request lifecycle, so the request module is the other candidate home.
