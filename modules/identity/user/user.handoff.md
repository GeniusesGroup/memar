# User — Handoff

Open state for the `identity/user` domain. Converted 2026-10-02.

## `UserUUID` is empty, and that is the question
`tp UserUUID ab` carries no requirements, so any capsule satisfies it
structurally and nothing about a user identifier is stated. The Go said nothing
either — `type UUID thing_p.UUID` is a re-spelling, not a contract. Before
implementers arrive, decide whether a user UUID must require behavior: render for
the text domain (the thing UUID's comment said "usually use to SET/GET and show
locale title by knowledge/text domain"), equality for comparison, or nothing.
Until that is decided, `UserUUID` states nothing that `ThingUUID` does not.

Rule 6 treats the empty abstraction as a design smell, so this is recorded rather
than shipped silently.

## The UUID is one concept under many names
`thing/protocol/dt-uuid.kh` declares `ThingUUID`. This file declares `UserUUID`,
which the Go defined as `type UUID thing_p.UUID` — the same concept re-spelled.
Khayyam has no alias form, so the corpus now holds two declarations of one
concept. `identity/organization` imports `UserUUID`; `identity/time` and
`identity/uri` import `ThingUUID`. That fork needs one ruling: either every domain
imports the thing declaration, or the concept is declared once and the per-domain
files import it. It is not settled here, because the ruling belongs to the thing
domain, which owns the concept.

## A dangling note in the Go
The Go source carried a comment "// Register new user — TODO::: not yet designed;
was a dangling comment in the Go source." on `UserID`. It names an event that was
never designed. It is recorded here rather than in the source, per rule 5, and it
is still undesigned.

## Method naming across the corpus
`UserID` here takes its name from the owner (`User`), following the Go and the
one converted sibling. `identity/time` produced `TimeID` on `Field_TimeID` and
`identity/uri` produced `URIID` on `Field_URIID`, while memar's own converted
protocols spell the same thing `GetURI`, `GetURI` style. The repository should
pick one convention and sweep the ninety-odd `dt-uuid.kh` files; the two
conventions now disagree inside this repository.

## What the conversion did not settle
- Whether a user's identity may ever diverge from its thing identity. `URIModel`
  in `identity/uri` composes `ThingModel`, so a URI record's identity is its thing
  identity; the same question applies here.
- The concrete UUID capsule: it belongs to the implementation layer, not to
  `protocol/`. Its home directory is undecided.

## Shown verification, after reading a real onboarding contract

### Topic & Purpose
A session read a real worked example of the *Shown verification* idea in this
module's base document: Middle East Bank's "Web services for non-in-person
identity verification and product creation in retail banking" (Persian, version
45, 114 pages, last edited 2026-05-10; source PDF lives outside the repository in
the owner's Downloads). The question this thread exists to answer: is *shown
verification* a field/status on `User`, a kernel domain of its own, or a
capability above the foundations — and what does this case prove about each?

### Decisions
- **Not a field or mark on `User` by itself** — confidence: Tentative. Reasoning:
  the case shows a verification is a family, not a value: claim, evidence
  (document photos, signature, video, an OTP possession check), checking
  authority (civil registry, postal address, banking-system blacklists), verdict,
  time, scope, expiry, revocation. The source itself demonstrates the collapse
  this shape produces: one flat application status
  (`INITIATED,CREATE,INPROGRESS,RETRY,REJECTED,DONE,EXCEPTION`) carries all of
  it, `RETRY` embeds a JSON array of per-item errors *inside a description
  string*, and `DONE` conflates "packet complete" with "person proven". Memar's
  own warning names this pattern: a field such as `discount` on an Invoice may
  incorrectly collapse a potentially independent family of behaviors
  (Modularity → *Rules as a Provisional Term → Scope Matters*). Rejected
  alternative: adopting the backlog's "verified mark" as the whole idea — the
  mark survives only as the *shown surface*, never as the model.
- **Not a kernel domain** — confidence: Tentative. The foundational test
  (Modularity → *What Earns Foundational Status*) passes without it: the subject
  sits on `identity/user`/`person`, claim+evidence already has a shape in
  `rights/case`, shared statuses are loop-edges in `knowledge/status`, gating is
  `computer/rule`, acting-for is `rights/delegate` (which this module's own
  backlog already says must be reconciled). Nothing forces fabricating or
  bending a foundation, and *Foundational Concepts Should Remain Few* treats an
  industry name ("identity verification", KYC, onboarding) as prima facie a
  capability, not a Concept — the vocabulary-discipline gate applies before any
  concept is accepted. Rejected alternative: a new kernel `identity/verification`
  domain.
- **Candidate shape: one pluggable capability** — confidence:
  Explored-but-unresolved. Under `modules/modules.md`, a capability owns the
  relationship, its rules, and its processing together (Capability
  Completeness); consuming domains expose an attachment point — a reference
  edge named after the concern — and never grow a field for it. Where it is
  filed (`modules-plugable/identity/...` vs an edge on an existing domain) is
  not decided here.
- **Adopt/fork verdict on `rights/case` (next step 1, executed) — confidence:
  Tentative.** Adopt: the evidence relation and its policies —
  `(case)-[:evidence]->(thing)`, the holder does not own the bytes, several
  evidence edges per holder, and above all "attaching the thing is not a ruling
  that the thing is authentic" — this capability's own
  attachment-versus-binding line, already stated by another domain. Fork: the
  claim grain. `rights/case`'s `claim` is an unconfirmed case-to-case
  proceeding candidate with no who-may-create recorded, and there the
  proposition *is* the case with one ruling per case (`edges/subject/subject.md`);
  verification needs per-attribute claims each with its own expiring,
  revocable verdict — different cardinality, different lifecycle. Rejected:
  reusing the `claim` label as-is (no bare edges — the label itself says it is
  not ratifiable); giving verdicts the case's one-ruling finality
  (expiry/revocation would have no home). What would make this wrong: a ruling
  that must accept a proposition while refusing one attached evidence item as
  two queryable results — the capability's per-claim nodes already absorb that
  case, so the fork stands.
- **Who-may-create policy for the verdict record — confidence: Tentative.**
  Create: only by the capability's own check processing (rule-gated). The
  subject asserts claims and attaches evidence but never creates a verdict; a
  third-party collector — a `rights/delegate` actor — may submit only, so
  judgment and collection never share an actor (the case's split
  accountability — bank accountable, third party collecting, registry check
  optional — is the failure this guard exists for). Remove: verdicts are
  revoked, not deleted; revocation carries reason, actor, time, and the record
  stays so "why did we believe this" remains answerable. Triggers
  (no-bare-edges): a new unrevoked, in-scope verdict makes the subject's badge
  read true and re-evaluates consumer rules; revocation re-evaluates them the
  same way — and because no grant is ever stored (see the consumer decision),
  there is nothing to cascade or unwind. Rejected: subject self-assertion (no
  judgment occurred); consumer-set (accountability without evidence — the
  bank's model); an admin flipping a status outside a check (an unanswerable
  verdict). Deliberate residue kept open as Q3: legal erasure versus history.
- **First consumer attachment point: economics account creation — confidence:
  Tentative.** The gate is a Rule the consumer attaches through the generic
  `condition_is` edge to a rule node (the kernel never references `rule`
  directly); the rule body reads the subject's verdicts directly — unrevoked,
  in-scope, registered authority, issued within T — never the badge. The
  account kernel gains nothing: its own philosophy already refuses fields for
  evaluated facts ("deliberately no AvailableBalance"), and modeling.md's own
  staff-prerequisite example puts the condition in a Rule without changing the
  edge type. What it triggers: account creation is admitted or not at evaluation
  time; a later revocation re-evaluates future actions and unwinds nothing
  retroactively. Rejected: a `kycStatus` field on the account (duplicates
  verdict truth and drifts — the same rejection account.md gives  balance-on-node); policy reads of the display badge (derived for showing,
  not for deciding).

### Key Definitions Established
- **Verification** *(working definition; confidence: Tentative — not yet through
  vocabulary-discipline's ratification home, which is its own open question 1
  there)*: the act of establishing that a claim is true — it takes a claim,
  submits it to a check against something that can contradict it, and yields a
  result attributable to who checked, how, and when. The dictionary sense
  consulted (verify: to make true, to establish the truth of; Persian تأیید
  درستی carries the same root sense) fixes no object: what is verified is
  whatever the claim asserts — a person's details in this case, an address or a
  document elsewhere. The dictionary carries none of the ecosystem's
  qualifiers; those are the rejects below.
- **Rename guard (weak)**: the term kept is `verification`. Rejected spellings,
  each disqualified for a qualifier it would import that the definition does
  not carry: `identity verification` (freezes one object into the name — the
  machinery is the same whatever the claim asserts); `KYC` (imports a
  compliance pipeline and a counterparty framing); `proofing` (imports
  document-centricity); `authenticity check` (conflates origin with truth —
  authentication's job, not verification's).
- **Reduction hypothesis** (recorded per vocabulary-discipline even while the
  term is kept): verification reduces to *claim + check + verdict over an
  existing subject* — shapes this tree already has or can have (`rights/case`'s
  evidence relation and its attachment-≠-authenticity policy, a `rule` decision
  as the check, a node/status as the verdict; the per-attribute claim has no
  home yet — it is the draft's own shape, cf. the adopt/fork decision).
  What the word names that the three pieces alone do not is the **binding**:
  that this check bears on this claimant's claim. If that binding proves to be
  a relation already owned elsewhere, the word survives only as a capability's
  label; the draft below assumes it is the capability's own semantics
  (Tentative). If the hypothesis falls, none of this thread's decisions changes
  — non-foundationality was tested against Memar's rules, not against the term.

### Capability Draft
Sketch for the session that picks this up — Explored-but-unresolved; nothing
here is ratified, and no file in the tree yet asserts it.

- **Responsibility**: establish the truth of claims about a subject, each
  verdict answerable — who checked, how, when, in what scope, valid until when,
  still standing or revoked.
- **Owned together (Capability Completeness)**: claims split per asserted
  attribute (the case's flat `{code,value}` bag is the anti-pattern it proves);
  evidence attached to its claim with provenance — who produced it, how, when —
  plus the retention rule for immutable evidence; checks against authorities
  through a `condition_is` → rule edge (the kernel never references `rule`
  directly); per-claim verdicts carrying `checkedBy, method, at, scope,
  expiresAt, revokedAt`; the expiry/revocation processing; and the binding rule —
  possession of a SIM proves control of a mobile, nothing more, and an authority
  query that was never run is recorded as *no check*, never as a passed one (the
  case's optional civil-registry inquiry).
- **Not owned here**: the consumer's gating policy — which verdicts suffice is
  the consumer's rule attached to the attachment point (Modularity → *Rules as
  a Provisional Term → Scope Matters*: behaviors at different levels do not
  become one concern); differences between organizations in collection workflow
  are configuration (rules), not new modules — a difference in parameters is
  configuration, a difference in processing semantics may be a distinct module.
- **Attachment point**: `user` — and `thing`, if the subject generalizes —
  exposes a concern-named reference edge: where behavior may attach, never what
  shape that behavior takes.
- **Placement test, executed**: Foundational test (*What Earns Foundational
  Status*) — the draft expressed through the remaining abstractions (subject
  `identity/user`, evidence `rights/case/edges/evidence`, check `computer/rule`, verdict
  machinery `knowledge/status`, acting-for `rights/delegate`) fabricates and
  bends nothing → not foundational. This is the *attempt to express* the test
  demands, run on a requirement that exists now. Pluggable test: independent
  responsibility with its own lifecycle (claim → evidence → check → verdict →
  expiry/revocation), attaching through an explicit relationship → a capability
  above the foundations.
- **Candidate placements, with their rejections**: `modules-plugable/identity/verification/`
  — a capability name in the category of the domain it instantiates through,
  satisfying both folder rules (pluggable folders carry capability names;
  `modules-plugable/identity/<core-domain-name>/` is forbidden). Wrinkle for the
  owner: that folder currently holds identity *kinds* (business, government,
  society, bot), so a capability there changes its reading. Rejected: a bare
  edge on `user` (no-bare-edges: no stated who-may-create-or-remove and
  what-it-triggers, and expiry/revocation/binding would have no owner);
  splitting across `computer/request` + `knowledge/status` + `computer/rule`
  (Capability Completeness: one responsibility, three owners); kernel
  `identity/verification` (foundational test above).

### Ambiguities Resolved
- **"The mark: a label on the user, or a status?"** (the base document's own
  review question). Resolved — confidence: Tentative — how: applied the
  promotion test `knowledge/status.handoff.md` already records — a status
  becomes a node when the status itself is the subject of further relations. A
  shown verification *is* such a subject (checked-against, evidence, method,
  time, expiry, revocation), so it is not a loop-edge marker; and storing both a
  marker and that record would hold one concern in two places (*One
  Authoritative Location per Concern's Data*). Resulting shape: the verdict
  record is the node; the badge is a **derived read** of "has a current,
  in-scope, unrevoked verdict" — a stored `edges-shortcut/` cache only if read
  cost ever demands one, and its document would name the source edges it
  recomputes. Still open after this: who may create that record (Q1 below), what
  the binding must require (Q2), and whether `rights/case`'s evidence notion
  transfers here (Assumptions, Weak). The grain question is closed; the
  authority question is not.
- **Does `rights/case`'s claim/evidence shape transfer to proofing?** (this
  thread's Weak assumption). Resolved — confidence: Tentative — how: read
  `rights/case/edges/evidence.md`, `edges/claim.md`, and `edges/subject.md`
  and split the assumption in two — the evidence relation and its policies
  transfer as written (adopt), the claim/proposition grain does not (fork) —
  recorded with reasoning as the adopt/fork decision above; the assumption
  bullet is removed rather than left stale.

### Open Questions
1. **Who is an authority, and who may register one?** The who-may-create
   policy in Decisions creates a verdict only from a check against a
   *registered* authority — the registration itself is undesigned: is an
   authority an organization related to the capability by a relation of its
   own, and who may create that relation (the state, the organization itself,
   a rule)? Why: this list is the policy's central guard, and it cannot default
   — in the case the bank judged data a third party collected while the one
   authoritative check (civil registry) was *optional* and time-gated,
   accountability and evidence held by different parties, and no record
   survived of why the bank believed the claim. Blocks: yes for adopting the
   policy. Path: model authority registration as its own relation with a
   stated who-may-create before the policy is ratified.
2. **What must the binding require before a verdict may be issued?** The
   Capability Draft assigns binding (and evidence provenance) to this
   capability; what stays open is the requirement itself — is control of a
   mobile plus self-supplied documents ever enough for a verdict, or does a
   claim of identity need a check that can contradict it (registry photo match,
   document genuineness, liveness)? The case binds only possession: OTP to the
   applicant's SIM, self-supplied photos and a video, no liveness, no
   genuineness, no match against the registry's own photo — and a later document
   version *removed* the selfie step. Why: without a stated requirement,
   "verified" records only that a packet arrived — the case's central defect.
   Blocks: no for shape, yes for real adoption. Path: express the requirement
   as a rule attached to the capability — level of assurance is policy, not
   core — and let authorities be relations, not booleans.
3. **Expiry, revocation, re-verification — and the no-removal clause.** The
   base document says once the mark is on, the passport image cannot be removed;
   the case has no revocation and no per-verdict expiry at all. Is immutability
   of *evidence* compatible with revocability of the *verdict* and with data
   minimization? Why: a revoked verdict that still shows its mark is worse than
   none. Blocks: no. Path: separate the evidence-retention rule from the verdict
   lifecycle; both belong to the capability.
4. **Which in-repo requirement consumes it first?** A first consumer is drafted
   in Decisions (economics account creation, as a rule — not a field), matching
   the case where product creation silently consumed `DONE`. What stays open:
   no module-level record in this tree asserts account-opening admission today;
   the stated requirement is `membership-and-identity`'s named
   identity-verification platform — a bundle approach page, not a module
   requirement. Does the gate attach at membership admission, at account
   creation, or at both? Why: the foundational test runs on requirements that
   exist, not anticipated ones, and the answer decides where the first
   attachment point is actually drawn. Blocks: yes for drawing it (not for the
   draft). Path: put the requirement question to the consuming domain's own
   handoff rather than deciding it here.

### Assumptions
- The bank contract is representative of regulated non-face-to-face onboarding
  practice rather than one outlier — stability: Unexamined. If wrong, several
  cited failure modes narrow to one bank, but the field/domain test was run
  against Memar's rules, not against the bank, and stands regardless.
- "Shown verification" in the base document's Idea backlog is still the live
  seed of this idea (nothing ratified elsewhere in the tree) — stability: Strong
  (read 2026-10-09).

### Related Artifacts
- [`user.md`](user.md) — Idea backlog, *Shown verification* and *Labels to find
  users*: its review questions are sharpened but not answered here (Update, when
  the owning session revisits).
- [`../../knowledge/status/status.handoff.md`](../../knowledge/status/status.handoff.md)
  — the general node-vs-loop-edge question whose test resolved this thread's
  grain; the general question there stays open (Review).
- [`../../rights/case/case.md`](../../rights/case/case.md) and its
  `edges/evidence`, `edges/claim`, `edges/subject` docs — read for the
  adopt/fork test; evidence adopted, claim grain forked (Decisions). Action:
  Review — `claim.md` itself warns it is an unconfirmed case-to-case candidate,
  which is what forced the fork.
- [`../../economics/account/account.md`](../../economics/account/account.md) —
  first drafted consumer; its no-field philosophy (availability is
  rule-evaluated, "deliberately no AvailableBalance") is the pattern the gate
  follows, so its kernel needs no change. Action: Review when the capability is
  ratified.
- [`../../management/vocabulary-discipline.handoff.md`](../../management/vocabulary-discipline.handoff.md)
  — the extraction gate was run for "verification" this session (Key
  Definitions above); its ratification home is vocabulary-discipline's own
  open question 1 (Review).
- [`../../../bundles/government/modules/membership-and-identity/membership-and-identity.md`](../../../bundles/government/modules/membership-and-identity/membership-and-identity.md)
  — names "the society's intelligent identity-verification platform" as a
  prerequisite and assumes ZKP attestation (stability: Weak there); Q1 and Q2
  bear directly on that assumption (Review).
- Source: the bank PDF named in Topic & Purpose; its extracted text was scratch
  in a Memar task folder, not a repository artifact (None).

### Proposed Next Steps
1. Resolve authority registration (Q1) — the policy's central guard; no
   dependencies.
2. Express the binding requirement as a rule (Q2), then settle expiry versus
   legal erasure (Q3) — both feed the policy's residue; depends on 1.
3. Decide where the first attachment point is drawn — membership admission or
   account creation (Q4) — and draft its rule body concretely; depends on 2 for
   the requirement values.
4. Carry the definition and rename guard to vocabulary-discipline's ratification
   home (its own open question 1) — independent; once ratified, the definition
   leaves this handoff for that record.

Completed 2026-10-09 and recorded above: vocabulary extraction and rename
guard; claim/evidence/verdict restatement; adopt/fork test against `rights/case`;
who-may-create policy with rejected alternatives; first consumer draft with
its rejections. The prior list's steps 1–3 are these.

### Notes
- Second thread, deliberately not opened here (one handoff per topic): the case
  had to split its province/city code lists because the postal and civil-registry
  databases disagree, and it forbids a "99 = other" escape. Authority-scoped
  code systems likely belong with `identity/taxon` or `knowledge/label` and
  deserve their own session; meanwhile the case's amount-band table (codes
  01–12) is published with lower bounds exceeding upper bounds from band 03 on
  — a PDF-as-contract with no machine-checkable schema, evidence for the
  vocabulary gate, not for this topic's shape.

## Research 001 questions and next steps (2026-10-18)

### Status
Proposals only, from [user.research.001.md](user.research.001.md) (eleven scenarios, a three-element kernel, four rival models and an identity-scope axis, a mapping of every file, eleven missing pieces sketched, twenty-two test scenarios, ten contradictions). Nothing is ratified; every item is **Tentative**, **Explored** or **Deferred**, none Decided. Settled facts above, including the whole "Shown verification" thread, are not re-argued; the research keeps verification as the existing Explored pluggable draft.

### Open Questions raised by the research
Each carries a recommended default and what it blocks; the full text is in the research's [Open Questions](user.research.001.md#8-open-questions-for-the-owner). The first three change what the domain is.

1. **Must a user be able to act, or may it be only a subject?** Default: an admitted subject; an acting user is recognisable (holds a current key) or is acted for. Blocks: the authentication section of [user.md](user.md) (contradiction C1: companies, wards, the dead and guests cannot hold a key), `UserModel`, the delegate scope.
2. **Is identity minted per registration (several users per human, linked only by an explicit `same_as` claim), or is one human or company one user everywhere?** Default: per registration. Blocks: the `UserUUID` fork above, cross-organization follow, what the verification capability may assume about uniqueness.
3. **Where does the key-to-user binding live, and is a hardware key ever the identity?** Default: the token domain owns the binding for any thing; a hardware key is one kind of key; recovery is a pluggable. Blocks: user.md's CPU-key question, recovery, bots with many instances.
4. **Is kind a loop and not part of the identifier?** Default: yes; the type mask becomes a derived selector. Blocks: retiring `dt-type.kh`, `dt-id.kh`, `internal/user.kh`; survey Q4.
5. **Is *closed* one state with a recorded cause, and is *blocked* only the justice or fraud status?** Default: yes to both. Blocks: the `status/` folder; the legacy lifecycle verbs.
6. **Are the legacy `UserDomain` statuses the user's own or its membership of a society (agent's inference from the status texts)?** Default: membership. Blocks: the destination of `_import/user-domain`.
7. **Who may admit a user?** Default: the thing itself, an enrolment rule, a guardian for a ward, or a registry process, each leaving its requester. Blocks: the undesigned register service named at the top of this file.
8. **Is a guest a kind of user or a state of a connection?** Default: a connection's state. Blocks: the `Guest` and `Unset` constants.
9. **How does an organization act, and where is the authority recorded?** Default: only through other users by acting-for; the external fact is a dated record in the verification capability. Blocks: organization admission, and verification Q1 above.
10. **What happens to a user at death or dissolution?** Default: standing *closed* with a cause, keys revoked and kept, heirs act through the heir relation, nothing deleted.
11. **Is erasure a state, an event on data, or outside the domain?** Default: an event on profile data that keeps identity, standing and signatures. Blocks: verification Q3 above, mention tombstones.
12. **Where do per-user preferences live?** Default: with the capability that reads them. Blocks: content receipts and limits.
13. **Does the application keep a derived "labels to find users" lookup?** Default: derived, as an analytics query. Blocks: the backlog idea in user.md.
14. **What must a `UserModel` require beyond `ThingModel`?** Default: the standing accessor and "recognisable now?". Blocks: any `UserModel` (rule 6).
15. **Does `user` stay a thin kernel domain or become a loop on thing?** Default: stays (the foundational test does not by itself decide). Blocks: the folder and ninety-odd consumers.

### Next Steps
1. Owner answers questions 1 to 3 first; they change what the domain is.
2. On the defaults, still Tentative: write the domain's Model and Policies from the three kernel elements (identity, admission, standing), amend the authentication sentence in user.md, and add a `status/` folder; do not write a `UserModel` before question 14.
3. Settle the `UserUUID` fork under question 2, then sweep the consumers listed in the organization handoff.
4. Send the destinations for the Go and `_import` residue to their owners (reachability to uri and notification, membership to organization, acting-for to delegate, names and pictures to text and thing), then retire the residue; no folder moves before the owner answers questions 4, 5 and 6.
5. Open the credential-binding sketch in the token handoff and the recovery sketch as a pluggable; ask delegate to take threshold, scope and ending cause (delegate handoff open question 4).
6. Reconcile contradictions C1 to C10 in the documents that own each side.

### Related Artifacts added
- [user.research.001.md](user.research.001.md) — the research; the eight sections, the sibling reconciliation, the contradictions (Update).
- [user.changelog.md](user.changelog.md) — the record of this addition (Update).

## Deactivation instead of deletion (idea, not ratified)
- State: carried 2026-10-19 from organization's `modules/computer/token/token.md` → Idea backlog from service code comments, when organization merged into memar (task 20261019-T103359Z-18676 recorded it in [token.changelog.md](../../computer/token/token.changelog.md); it is placed here because it is about the user). The idea: deleting a user entirely is not realistic, given the legal complexity, so registration warns the user about deactivation instead of promising deletion. Review discipline per [vocabulary discipline](../../management/vocabulary-discipline.handoff.md).
- Questions: is the sign-up warning a registration concern of User, while Token only revokes credentials on deactivation? Does deactivate-versus-delete need a user status that Token only reacts to? Who owns the legal-retention policy, the rule domain or [Rights](../../rights/rights.md)?
