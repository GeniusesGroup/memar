# Case Research 003 — Common law and one ODR system

## Table of Contents

- [Status](#status)
- [Question and goal](#question-and-goal)
- [Participants](#participants)
- [Method](#method)
- [Findings](#findings)
  - [A. United States federal courts (FRCP)](#a-united-states-federal-courts-frcp)
  - [B. British Columbia Civil Resolution Tribunal (CRT)](#b-british-columbia-civil-resolution-tribunal-crt)
  - [C. Cross-cutting observations for Phase 0](#c-cross-cutting-observations-for-phase-0)
- [Questions for Omid](#questions-for-omid)

## Status

Active — Run 2 (Research B), Phase 0 justice pilot.

## Question and goal

**Questions**

| # | Question | Status |
|---|----------|--------|
| Q1 | How does a common-law system (US federal: FRCP 18/20/54(b)) structure multiple claims and parties, state each party's role, require or permit per-claim decisions, allow amendment, and divide work between people and systems? | Answered (US FRCP sources consulted) |
| Q2 | How does a real operating ODR system (BC Civil Resolution Tribunal) do the same? | Answered (CRT Rules and official help pages consulted) |
| Q3 | What in these systems bears on the Phase 0 pilot defects (role per person per claim; separate ruling per claim; functional authorization)? | Partially answered — descriptive only; modeling deferred to Run 3 |

**Goals**

| Goal | Status |
|------|--------|
| Produce an English comparative description (not a model) from inspectable formal/official sources | Met |
| Cover claim individuation, party roles per claim, decision requirements, amendment, pre-filing completeness/registry lookup, and software vs human vs agent division | Met |
| End with precise blocking questions for Omid | Met |

**Scope**

- In scope: US Federal Rules of Civil Procedure (joinder, pleading, partial judgment); BC CRT Standard Rules (effective 20 February 2024) and official CRT help pages.
- Out of scope: Iran; civil-law systems (Run 1); draft edges or code; England CPR (US FRCP chosen as the common-law source named in the Run 2 brief); marketplace ODR (BC CRT preferred source available).
- Not read: `research-a.md` (independent context required).

## Participants

| Participant | Roles | Review |
|-------------|-------|--------|
| bc-1d2ca162-a589-553e-bbb2-acb2d57256d5 (Composer agent, Run 2) | Researcher | Not yet reviewed |

## Method

Single-reasoning-pass desk research. Sources limited to formal rules and official tribunal/government pages in English. Where a required point was not found in those sources, the finding states **not found** rather than reconstructing from memory.

Primary sources:

- Federal Rules of Civil Procedure (Cornell LII mirrors of the official rules): Rules 8, 10, 13, 15, 18–21, 42, 54 — https://www.law.cornell.edu/rules/frcp/
- *Civil Resolution Tribunal Standard Rules* (in force 20 February 2024) — https://civilresolutionbc.ca/wp-content/uploads/CRT-Standard-Rules-in-force-February-20-2024.pdf
- BC CRT official help pages — https://civilresolutionbc.ca/help/
- BC business/organization name search guidance (CRT-hosted link to Corporate Registry / OrgBook) — https://civilresolutionbc.ca/name-search

Read-only organization context (not sources): `modules/rights/case`, `bundles/justice`.

## Findings

### A. United States federal courts (FRCP)

#### A.1 Claim individuation

A federal civil action is a single case file that may contain multiple **claims for relief** (original claims, counterclaims, crossclaims, third-party claims).

- **Pleading form.** Rule 10(b) requires numbered paragraphs and, when clarity would be served, each claim founded on a **separate transaction or occurrence** in a **separate count**. Rule 8(a) requires a short plain statement of each claim and a demand for relief (which may be alternative).
- **Joinder of claims (Rule 18).** A party asserting any claim may join **as many independent or alternative claims as it has against an opposing party**. Joinder of claims is a **pleading** rule; properly joined claims need not be tried together if fairness or convenience justifies separate treatment (Advisory Committee Note to Rule 18).
- **Related claims by other parties.** Rule 13 governs counterclaims (compulsory if arising from the same transaction/occurrence, otherwise permissive) and crossclaims among coparties. Rule 13(i) links separate trials and Rule 54(b) judgments on counterclaims/crossclaims.

There is no FRCP rule that assigns a stable global "claim ID" across the life of the case; individuation is by **count / claim for relief** in pleadings and by the court's later orders.

#### A.2 Stating each party's role per claim

Parties appear in the action under **procedural roles**, not as an undifferentiated person list:

- **Caption (Rule 10(a)).** The complaint title must **name all parties**; later pleadings may refer generically to other parties after naming the first on each side.
- **Joinder of parties (Rule 20).** Persons may be joined as plaintiffs or defendants when claims arise from the same transaction/occurrence (or series) and a common question of law or fact will arise. Rule 20(a)(3): the court may grant judgment **to one or more plaintiffs according to their rights, and against one or more defendants according to their liabilities** — liability is party-specific, not necessarily uniform across all joined claims.
- **Required joinder (Rule 19).** Certain interested persons must be joined if feasible; the pleader must state names and reasons for nonjoinder (Rule 19(c)).
- **Role types across claims.** The same natural person may simultaneously be plaintiff on one claim, defendant on a counterclaim, third-party plaintiff, etc. The rules govern **capacity in the action** (plaintiff, defendant, third-party defendant, crossclaimant) rather than requiring a matrix of (person × claim × role label) in the complaint. **Not found** in FRCP: an explicit requirement that the complaint list, for every named person, that person's role **on each separate claim**.

Representation of a party (attorney of record) is governed by local court rules and practice, not the cited FRCP provisions.

#### A.3 Whether and how each claim must be decided

- **Default: one final judgment.** Historically, federal courts disfavor piecemeal finality; appeals lie from final judgments (Rule 54(b) Advisory Committee Note cites *Catlin v. United States*, 324 U.S. 229 (1945)).
- **Partial judgment (Rule 54(b)).** When an action presents **more than one claim for relief** or **multiple parties**, the court **may** direct entry of a **final judgment as to one or more, but fewer than all, claims or parties** only if it **expressly determines that there is no just reason for delay**. Without that determination, an order adjudicating fewer than all claims or parties **does not end the action** as to those claims/parties and **may be revised** before a judgment adjudicating all claims and all parties' rights and liabilities.
- **Separate trials (Rule 42(b)).** For convenience, prejudice, or economy, the court **may order a separate trial** of one or more claims, counterclaims, crossclaims, or third-party claims.
- **Mandatory per-claim written ruling.** **Not found** in FRCP 54 or related joinder rules: a requirement that the court issue a separate structured ruling on every pleaded claim before closing the case. A court may dispose of some claims via Rule 54(b), summary judgment, dismissal, or settlement, while others remain pending.

#### A.4 Amendment of parties and claims after filing

- **Amendments (Rule 15).** A party may amend once as a matter of course within specified time windows; otherwise with consent or leave, which **should be freely given when justice so requires**. Rule 15(c) **relation back** can apply to amendments changing the party against whom a claim is asserted, within notice and identity conditions.
- **Adding/dropping parties (Rule 21).** Misjoinder is not a ground for dismissal; the court may **add or drop a party** and **sever any claim against a party** on just terms.
- Counterclaim timing amendments are governed through Rule 15 (former Rule 13(f) abrogated; Committee Note 2009).

#### A.5 Pre-filing completeness and registry lookup

- **Pleading content (Rules 8, 10, 19(c)).** The initiator must state claims, name parties in the caption, and identify persons required to be joined if feasible.
- **Automated registry validation at filing.** **Not found** in FRCP: mandatory electronic lookup of corporate/registries before acceptance. Federal courts use electronic filing systems (e.g., CM/ECF) in practice, but the cited rules do not prescribe registry integration or pre-filing completeness checks beyond pleading requirements.

#### A.6 Software, humans, and identity vs role/authorization

| Function | Typical actor | Notes from rules |
|----------|---------------|------------------|
| Drafting/joining claims and parties | Party or attorney (human) | Rules assume pleadings filed by parties; no "agent" category in FRCP |
| Filing | Party/attorney via court e-filing (software-mediated) | Not specified in cited rules |
| Joinder/necessary-party decisions | Court (human judge) | Rules 19–21, 42, 54(b) |
| Partial vs final judgment | Court (human judge) | Rule 54(b) express determination |
| Binding the client | Party; attorney by representation (local practice) | FRCP does not define representative authorization graph |

**Not found** in FRCP: rules distinguishing an AI agent from a human representative.

---

### B. British Columbia Civil Resolution Tribunal (CRT)

The CRT is a statutory online tribunal with jurisdiction over strata disputes, small claims (up to $5,000), motor-vehicle injury disputes (up to $50,000), and other listed matters. Process is designed for lay participants using web forms and a CRT account.

#### B.1 Claim individuation

- **Application structure.** An applicant completes a **Dispute Application Form** listing **claims** and, for each claim, at least one **remedy** (what the tribunal should order) (CRT help: "What are remedies?").
- **Relatedness rule (Rule 2.1(5)–(6)).** All claims in one application must be **related**; unrelated claims may be split into separate applications, refused, or not issued.
- **Practical limit (official help).** Applicants are advised to limit an application to **one or two issues (claims)** plus interest/fees; more claims usually lengthen the process; unrelated claims may require separate applications.
- **Automatic claim split.** The form may **automatically create separate claims** for interest and/or fees and expenses when selected (help: "What information do I need to apply?").
- **Per-claim argument budgets (Rule 7.3(5)–(6)).** Tribunal Decision Plan arguments are measured **per claim** (character limits for applicant, respondent, reply), signalling that claims are distinct units through adjudication even when filed together.

Counterclaims and third-party claims are separate claim objects added by respondents under Part 3.

#### B.2 Stating each party's role per claim

CRT uses explicit participant categories:

| Participant kind | Role | Source |
|----------------|------|--------|
| **Applicant** | Initiates dispute; may be multiple with one **primary applicant** | Rule 1.3(2); help "What are participants?" |
| **Respondent** | Person/organization the claim is against; **each must respond separately** | help "What are participants?" |
| **Primary applicant** | Among multiple applicants: starts process, contact person, **authority to bind all applicants** | Rule 1.3(2) |
| **Contact person** | For organizations (strata, company, society, etc.): **acts on behalf of the organization** — speaks to CRT, receives documents, uploads evidence, makes agreements | Rule 1.14; help "What is a contact person?" |
| **Representative** | Speaks officially for a participant, submits evidence/arguments, **may make agreements**; usually needs tribunal permission except in accident claims (lawyer) and some insurer situations | Rule 1.16; help "What is a representative?" |
| **Helper** | Assists but **may not** communicate for the party or bind them | Rule 1.16(3); help "What is a representative?" |
| **Litigation guardian** | Required for minors and adults with impaired mental capacity | Rule 1.13 |
| **Third-party respondent** | Added when a respondent brings a third-party claim | Rule 3.3; help "What is a third-party claim?" |

Organization "contact person" is **not** the same as "representative" (help pages distinguish them). A person may be a user account holder (CRT account, Rule 1.8(2)) while acting in one of the above **process roles**.

**Not found** in CRT Rules: a mandatory data field listing, for every participant, their role **on each separate claim** in a multi-claim dispute. Claims name respondents; remedies attach to claims; party type (applicant/respondent/third party) is dispute-level with per-claim argument tranches.

#### B.3 Whether and how each claim must be decided

- **Phases.** After filing: optional negotiation/facilitation (case management), then **Tribunal Decision Process** if unresolved (Rules 5.1, 7.1).
- **Claims going forward (Rule 5.4(1)(b)).** When facilitation ends, the case manager **confirms the claims that are going forward for decision**.
- **Partial resolution by agreement (Rule 5.2).** Parties may resolve **any or all** claims by consent order; if only some claims settle, a draft consent order may proceed immediately or with the Tribunal Decision Plan (Rule 5.2(7)).
- **Withdrawal (Rule 6.1).** A party may withdraw **one or more** claims (with permission after assignment to a tribunal member).
- **Default (Rules 4.2–4.3).** Applicant may seek default decision when respondents do not respond; tribunal may assume liability and determine amounts.
- **Final decisions (Rule 9.4).** Rules address privacy, payment mechanics, and publication bans; **not found**: explicit requirement that the tribunal issue a separate written decision section for **each** claim analogous to FRCP 54(b)'s partial finality doctrine. Per-claim argument structure (Rule 7.3) and consent-on-some-claims (Rule 5.2) imply claims can be resolved individually, but a blanket "must rule on every claim separately" rule was **not found**.

#### B.4 Amendment of parties and claims after filing

**Rule 1.19 — Amendments to Dispute Notices and Dispute Response Forms**

- Applicant or respondent may request amendment (contact tribunal, specify changes, pay fee).
- Tribunal considers stage, nature of change, prejudice, and other factors.
- **Generally no amendments after the tribunal decision process begins**, except extraordinary circumstances.
- Amended Dispute Notice: re-service on new or non-responding respondents; responding parties may amend responses if amendment is substantive.
- Tribunal **may at any time order that a party be added** and give directions (Rule 1.19(6)).

**During facilitation (Rule 5.3(4)).** Case manager may permit a party to **add, revise, or withdraw a claim**, add a party, and set steps/costs.

**Third-party and counterclaims (Rules 3.2–3.3).** Respondents add claims/parties by prescribed forms and fees within time limits (counterclaim within 30 days of response; third-party claim with 30-day service window).

#### B.5 Pre-filing completeness and registry lookup

Official pre-filing checklist (help: "What information do I need to apply?"):

- Legal names and addresses of all applicants and respondents
- Representative or contact person name/email where applicable
- **Strata claims:** strata corporation/section **legal name** and **most recent mailing address on file at the Land Title Office**
- Motor-vehicle claims: ICBC detailed responsibility assessment (CL 722) when applicable
- Short description, remedies sought, fee payment or waiver

**Registry / name lookup (not automated by CRT rules text):**

- Applicants are directed to find legal names via **OrgBook BC** and Corporate Registry searches (CRT page https://civilresolutionbc.ca/name-search , linking to BC government registry services).
- Service rules use **Registrar of Companies** registered office addresses (Rule 2.7) and **Land Title Office** addresses for strata corporations (Rules 2.2(5), 2.6).
- **Initial completeness review (Rule 2.1(2)).** After application, tribunal may issue Dispute Notice, **request more information**, or explain why no Dispute Notice will issue — human/staff review, not described as automated registry verification.

#### B.6 Software, humans, and identity vs role/authorization

| Function | Actor | Mechanism |
|----------|-------|-----------|
| Application intake | **Software** (online forms) + **CRT staff** review | Rule 2.1; help "How do I make a claim?" |
| Account / identity | **User** creates CRT account (Rule 1.8(2)) | Login identity |
| Organization binding | **Contact person** with authority to bind org (Rules 1.14, 1.16) | Role + authorization, not merely user ID |
| Multi-applicant binding | **Primary applicant** (Rule 1.3(2)) | Named role with bind authority |
| Representation | **Representative** (often lawyer/family/friend) with tribunal permission in most matter types | Rule 1.16; distinct from helper |
| Case management | **Case manager** (human) | Rules 5.1–5.5, 7.2 — directs process, reviews communications in facilitation |
| Adjudication | **Tribunal member** (human) | Rules 7.1, 9.1–9.4 |
| Service | **Software** (tribunal may serve by mail/email) and/or **applicant** | Rules 2.2–2.10 |
| Non-compliance sanctions | **Tribunal** may decide on incomplete record | Rule 1.4 |

**Automated agents (AI).** **Not found** in CRT Rules or cited help pages: any category for an AI agent distinct from representative, helper, or contact person.

---

### C. Cross-cutting observations for Phase 0

These are descriptive comparisons for later modeling runs; they are not model proposals.

1. **Claim individuation.** Both systems allow multiple claims in one proceeding but use different units: FRCP **counts/claims for relief** in pleadings; CRT **claims with remedies** in a dispute file, with stronger administrative pressure to keep claims few and related.
2. **Role per person per claim.** FRCP assigns **procedural roles** (plaintiff/defendant/counterclaimant) that can differ across claims for the same person, but does not require an explicit per-claim role matrix in the initiatory document. CRT separates **participant type** (applicant/respondent/third party) from **authorization roles** (primary applicant, contact person, representative, litigation guardian) but **not found**: explicit per-claim role assignment for every person.
3. **Separate ruling per claim.** FRCP **permits** early finality on some claims (Rule 54(b)) but does not **mandate** a ruling on every claim before closure. CRT **tracks claims separately** through decision preparation and consent/default paths; mandatory separate written ruling per claim — **not found**.
4. **Amendment.** Both allow post-filing changes with court/tribunal control; CRT tightens amendments once the tribunal decision process starts (Rule 1.19(3)).
5. **Registry lookup.** CRT pushes applicants toward **manual** registry/name searches before filing; FRCP has no equivalent in the cited rules. Neither source describes fully automated pre-filing registry validation.
6. **User vs role.** CRT is explicit: CRT **account/user** ≠ **contact person** / **representative** / **primary applicant** / **litigation guardian**. FRCP distinguishes **party** from **attorney of record** via practice, not the cited rules.
7. **Justice bundle note (out of phase scope).** The justice bundle's marketplace ADR record describes binary approve/decline per claim without procedural detail (`bundles/justice/justice.md`); CRT provides richer official process documentation and is used here instead.

## Questions for Omid

1. **Claim unit (`case` graph).** In the organization model, should one **claim** correspond to an FRCP "claim for relief" / separate count, to a CRT **claim-plus-remedy** pair, or to something else? This blocks how petition edges attach to multiple `case` nodes and whether remedies are part of the claim node.

2. **Per-claim ruling obligation.** Neither FRCP nor CRT **requires** a separate final ruling on every claim in all circumstances (partial judgment/consent/default are permitted). Should the petition model nonetheless **require** a structured ruling per claim (your bi-haqqi concern), or only record rulings when the process produces them? This blocks whether "skipped claim" is a validation error or an allowed state.

3. **Functional role placement.** CRT separates **contact person** (organization actor with bind authority) and **representative** (permission-based advocacy) from the login **user**. Should organization mirror this under `modules-plugable` as functional roles tied to `AuthorizationRuleID`, and which CRT roles (primary applicant, contact person, representative, litigation guardian, helper) are in scope for Phase 0? This blocks the pilot question on where authorization lives.

4. **Role per person per claim.** Sources do not show a general requirement to state each person's role on **each** claim separately (as opposed to procedural role in the proceeding). Is that matrix an **Iran-specific** requirement you want modeled anyway, or should the graph only store proceeding-level roles plus claim-party links? This blocks whether petition must carry a (person × claim × role) structure or a lighter shape.

5. **Pre-filing registry lookup.** CRT expects applicants to obtain registry/Land Title data before filing, but rules describe **human** lookup, not automated validation. Should a petition support **provisional filing** pending registry confirmation, and if so is that a `user` action, a functional role under `modules-plugable`, or an automated agent step? This blocks attachment of inquiry edges to delegate/registry domains.
