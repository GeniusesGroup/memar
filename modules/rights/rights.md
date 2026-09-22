# Rights

Rights covers the normative layer of organizations: law, ownership, contract, case, and delegation of authority.

## Boundary notes (from the domain-boundary proposal — awaiting review)

- **Accounting is outside Rights.** Accounting records and measures rights; it does not create them. "Who owns X?" (here) and "how is that ownership entered in the books?" (there) are different problems — `Rights → Accounting` is a gives-rise-to relation, not containment.
- **Estates are subjects of rights, not members of this category.** An estate can simultaneously carry identity, rights, accounting, product, and location perspectives — several lenses over one reality, not several estates (see [`identity/estate/estate.handoff.md`](../identity/estate/estate.handoff.md)).
- **Rights come first; ownership/legal relations arise from rights** (Omid, confirmed in the estate session) — ownership is not the primitive that grants rights.

Topics:
- [law/law.md](law/law.md) — the law *type* (text plus companions; frozen once voting). Proposed statutes are instances; they live as modules of the bundle that enforces them ([Bundles](../../bundles/bundles.md)).
- [normative-bootstrap.handoff.md](normative-bootstrap.handoff.md) — founding laws of an organization: the Law / Consent / Source-of-Authority question raised by bootstrapping new organization instances inside the software.
- [rights-domain-boundaries.handoff.md](rights-domain-boundaries.handoff.md) — a **proposal awaiting review** for the internal boundary of the rights domain (Ownership / Contract / Law / Obligation / Permission? / Authority? / Liability?).

## Idea backlog from edge code comments

Raw proposals extracted from comment notes inside edge `.go` files (comments remain in code as source). Review discipline per `modules/management/vocabulary-discipline.handoff.md`. Nothing below is ratified.

### case roles - `case/edges/case-relation-user.go`
- **Idea**: justice role labels for case participants: Judge, Jury, Plaintiff, Defendant (with Suspect commented), Lawyer, TrialAttorney, Counsellor, JudicialOfficer (bailiff noted), Witness. Plus scattered decision-vocabulary notes: decision types (Dismissal, Invalidate, Guilty, Conditionally - "true only if something else happens first"), responsibility types including relative/joint liability, "organization that claim service must call".
- **Review questions**: are participant roles the same role mechanism as `modules/management/role` or case-specific? Do decision types need an explicit state machine (the no-finality principle in the case README)? Liability vocabulary intersects the rights-domain-boundaries handoff open question.

### case relations - `case/edges/case-relation-service.go`, `case-relation-case.go`, `case.go`
- **Idea**: ClaimService (claim must be a service run by a specific organization; order of services matters, e.g. identity theft); ClaimRelation (proceeding relation between cases); a complaint-URL sketch (sabz.city complaints with tel/orgID params) as a case-entry channel.
- **Review questions**: is ClaimService an edge to the service domain (economics) - and does the order-of-services need sequence semantics? The URL sketch is UI, not model.

### law status - `law/edges/law-status.go`
- **Idea**: law states Closed/Denied (comment-level only).
- **Review questions**: reconcile with the general status domain and the normative-bootstrap handoff (amendment/repeal of base law).