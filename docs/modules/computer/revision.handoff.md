# Revision Handoff

## Topic & Purpose
Open work for [`revision.md`](./revision.md), the Revision contract (enumerate sources, reviewable plan, explicit write, refuse-on-newly-broken, report). See the repository's [documentation-handoff.md](../../documentation-handoff.md) for what a handoff is.

## Status
Draft contract under owner review. The twin split and the Binding narrowing are decided in `bundles/khayyam/services/rename/rename-management.handoff.md`; this file holds what the contract itself still owes.

## Open Questions
- **Portability bound:** the contract claims only what was lifted from examined mechanisms. Under what evidence may a clause be claimed for a language this repository does not have — a second examined mechanism, a proof of language-independence, or never?
- **Exit codes and plan renderings:** per-target by decision, but two realizations with incompatible exit codes cannot share a runner. Is a shared taxonomy owed, and if so where does it live — here, a Rule, or the runner's own contract?
- **Concurrent revisions over the same sources:** the contract states one run against stated sources. When two runs overlap — the second run's sources changed mid-flight — does the run re-enumerate, refuse, or merge? Decided direction (owner, 2026-10-05): serialize through the owning changer (per-entity lock), never timestamp reconciliation; time/version acceptance is high-cost and rejected as default. What, if anything, this contract owes the overlap beyond that direction — e.g. stale-sources detection as a refusal condition — is open. The storage answer (content-addressability, idempotent per-record edits) and the organizational answer (who may write when) live in their own layers.

## Anticipated Work
- Follow-through of the Binding narrowing in the rule's own documents (sources/plan/write/gate/report clauses re-homed, residue members staying per-target).
