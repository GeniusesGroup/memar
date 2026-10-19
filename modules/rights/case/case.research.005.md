# Case Research 005 — Vote aggregation

## Table of Contents

- [Status](#status)
- [Question and goal](#question-and-goal)
- [Participants](#participants)
- [Method](#method)
- [Findings](#findings)
  - [1. What “majority” means with three ballot choices](#1-what-majority-means-with-three-ballot-choices)
  - [2. Partial grant versus a new claim](#2-partial-grant-versus-a-new-claim)
  - [3. How numeric remedies are aggregated](#3-how-numeric-remedies-are-aggregated)
  - [4. Sources requiring each adjudicator to state a quantity](#4-sources-requiring-each-adjudicator-to-state-a-quantity)
  - [5. Omid's premises tested](#5-omids-premises-tested)
- [Questions for Omid](#questions-for-omid)

## Status

Complete

## Question and goal

**Questions**

| # | Question | Status |
|---|----------|--------|
| Q1 | When several adjudicators vote on one claim with three choices (for claimant, for respondent, abstain), what does “majority” mean, and how is abstention treated? | Answered (with gaps marked) |
| Q2 | Is a partial grant (less than requested) the same claim or a new claim an adjudicator would have to introduce? | Answered |
| Q3 | How are numeric remedies (money, months) aggregated when adjudicators disagree — median, issue-by-issue majority, average, lowest, highest? | Answered |
| Q4 | Do any opened sources require each adjudicator to state a quantity rather than yes/no? | Answered |
| Q5 | Do any opened sources tie vote secrecy to aggregation rules? | Answered (negative) |

**Goals**

| Goal | Status |
|------|--------|
| Provide an inspectable English-language survey from scholarly or official sources only | Met |
| Test Omid's premises separately from sourced findings | Met |
| Write **not found** where sources do not support a point | Met |
| End with precise blocking questions for Omid | Met |

**Scope**

- In scope: collegial adjudication and judgment aggregation as general ideas; civil-law *Teilurteil* and criminal sentencing only as evidence about partial grants and numeric outcomes, not as the model.
- Out of scope: country-by-country procedure surveys (see `research-a.md`, `research-b.md`); modeling or code; vote-secrecy design (another run).
- Omid's premises (majority not average; abstain as negative with reason; smaller amount via chained new claim) are tested, not adopted.

## Participants

| Participant | Roles | Review |
|-------------|-------|--------|
| bc-5d2260e2-fc82-5f73-95db-068e5c8a4927 (Composer agent, vote-aggregation run) | Researcher | Not yet reviewed |

## Method

Single-pass desk research, 27 September 2026.

1. Loaded Memar Research facet core from `memar/docs/documentation-research.md` and citation practice from `memar/docs/knowledge.practice.md`.
2. Read `research-a.md` and `research-b.md` only as assignment brief (not as evidence in this file).
3. Searched and opened English scholarly articles, official treaty/statute texts, court rules, and encyclopedia entries. A finding is stated only from text this pass opened. **Not found** means not found in those opened sources, not proof that no such text exists.

**Sources opened (Evidence)**

- Lewis A. Kornhauser and Lawrence G. Sager, “The One and the Many: Adjudication in Collegial Courts,” 81 Cal. L. Rev. 1 (1993), <https://lawcat.berkeley.edu/nanna/record/1114609/files/fulltext.pdf>
- Christian List, “The theory of judgment aggregation: An introductory review” (manuscript, August 2009), <http://fitelson.org/ace/alvin_seminar/ld_talk/list_review.pdf>
- Franz Dietrich and Christian List, “Collective intelligence through aggregation,” Phil. Trans. R. Soc. B 381: 20240454 (2026), <https://royalsocietypublishing.org/rstb/article-pdf/doi/10.1098/rstb.2024.0454/6133087/rstb.2024.0454.pdf>
- Serena Forlati, “Infra Petita,” Max Planck Encyclopedia of International Procedural Law, Oxford Public International Law, <https://opil.ouplaw.com/view/10.1093/law-mpeipro/e3113.013.3113/law-mpeipro-e3113>
- UNCITRAL Arbitration Rules (2021), United Nations, <https://uncitral.un.org/sites/default/files/media-documents/uncitral/en/21-07996_expedited-arbitration-e-ebook.pdf>
- Statute of the International Court of Justice, UN, Arts 55–56, <https://www.un.org/en/about-us/un-charter/statute-of-the-international-court-of-justice>
- Max Planck Encyclopedia, “Deliberation and Drafting: International Court of Justice (ICJ),” <https://opil.ouplaw.com/view/10.1093/law-mpeipro/e3399.013.3399/law-mpeipro-e3399>
- Rome Statute of the ICC, Art 74 (decision) and Art 78(3) (sentencing), ICRC database, <https://ihl-databases.icrc.org/en/ihl-treaties/icc-statute-1998/article-74>
- ICC sentencing practice summary, Legal Tools, <https://www.legal-tools.org/clddoc/63c036adda2e6b7a7c07cf61>
- Federal Rules of Civil Procedure, Rules 48, 54, 56 (Cornell LII), <https://www.law.cornell.edu/rules/frcp/>
- Kimball v. Walden, 171 W.Va. 579, 301 S.E.2d 210 (1983), via vLex summary, <https://case-law.vlex.com/vid/kimball-v-walden-no-890214511>
- “Quotient Verdicts in Florida,” 13 U. Fla. L. Rev. 315 (1960), <https://scholarship.law.ufl.edu/cgi/viewcontent.cgi?article=3819&context=flr>
- Todd Z. Yates, “Abstention: The Unexpected Power of Withholding Your Vote,” 43 Conn. L. Rev. 585 (2010), <https://scholar.smu.edu/cgi/viewcontent.cgi?article=1080&context=law_faculty>
- ASCCC, “Abstentions, Quorum, and Nuance,” <https://asccc.org/content/abstentions-quorum-and-nuance>
- Official English ZPO excerpts on *Teilurteil* (§ 301) as summarized in `research-a.md` — cross-checked against Gesetze-im-Internet English ZPO PDF cited there.

## Findings

### 1. What “majority” means with three ballot choices

#### 1.1 Binary majority in collegial courts and arbitration

Opened official rules typically define **majority among those who vote on the decision**, not among all members with a three-way ballot.

- **UNCITRAL Arbitration Rules (2021), Art 33(1):** “When there is more than one arbitrator, any award or other decision of the arbitral tribunal shall be made by **a majority of the arbitrators**.” No third “abstain” option appears; the rule is binary on the tribunal’s output.
- **ICJ Statute, Art 55(1):** “All questions shall be decided by **a majority of the judges present**.” Art 55(2) gives the President a casting vote on a tie.
- **ICC Rome Statute, Art 74(3):** judges “shall attempt to achieve unanimity … failing which the decision shall be taken by **a majority of the judges**.”

These texts do not define a ballot with separate “for claimant,” “for respondent,” and “abstain” labels. They define how the **collective decision** is reached once judges or arbitrators have taken positions.

#### 1.2 Abstention: vote, non-vote, or counted against a party?

Treatment **varies by institution**; opened sources do not agree on a single rule.

| Source | Abstention treatment |
|--------|---------------------|
| **ICJ Internal Practice** (reported in MPEiPro “Deliberation and Drafting”) | Judges **cannot abstain** on a decision; they must vote **affirmative or negative** (Art 8(v) Internal Practice Resolution). |
| **Robert’s Rules of Order** (summarized by ASCCC) | On a typical majority vote, **abstentions do not count** toward the outcome; only yes and no votes are tallied. |
| **Absolute quorum rules** (Yates, Conn. L. Rev.) | Under **absolute quotas**, an abstention **functions the same as a “no” vote** — it cuts into the affirmative total needed to pass. |
| **U.S. Supreme Court practice** (Jacobi & Kontorovich, cited in later literature; not opened in full this pass) | Empirical claim that **abstention essentially never occurs** on the merits despite conditions that would predict it; institutional incentives (*stare decisis*, *Marks* doctrine) favor participation. |
| **Argentine Supreme Court** (same secondary citation) | **Abstention does occur**; pivotal judges abstain less often — treated as strategic non-participation, not as a neutral non-vote. |

**Not found** in opened sources: a general rule that abstention is automatically counted **against the claimant** (or against the respondent). Yates argues abstention is **not** neutral indifference under many voting procedures — it can **tip the scale** toward one side — but the direction depends on the **specific quorum and counting rule**, not on a fixed “against claimant” default.

**Not found:** an opened English scholarly or official source that defines **majority** on a **three-option** ballot (claimant / respondent / abstain) for collegial adjudication. Judgment-aggregation literature (List 2009; Dietrich & List 2026) treats **binary** judgments (accept/reject propositions) or **numeric** values, not a dedicated three-way merits ballot with abstention as a first-class outcome.

#### 1.3 Plurality and issue-by-issue majority (related, not identical)

- **Kornhauser & Sager (1993):** collegial courts can use **case-by-case** voting (majority on the bottom-line outcome) or **issue-by-issue** voting (majority on each legal premise, then apply doctrine). The choice can **change who wins** (doctrinal paradox).
- **List (2009):** **propositionwise majority** (issue-by-issue) can yield **logically inconsistent** collective judgments when propositions are interconnected — the discursive/doctrinal paradox.

These are about **how many binary or doctrinal issues** are aggregated, not about a three-label merits ballot.

### 2. Partial grant versus a new claim

Opened sources treat **awarding less than requested** as a decision **on the same claim**, not as requiring the adjudicator to file a new claim.

- **Forlati, “Infra Petita,” para 16 (MPEiPro):** “Nor does the principle prevent arbitrators and judges from **upholding specific claims only in part**; **the rest of the claim is thus deemed to be rejected**, even if the judgment or award does not specify it expressly.”
- **Swiss Federal Supreme Court practice** (summarized in Bratschi/Kluwer arbitration commentary opened via search snippets): awarding **less than requested** is **not** *ultra* or *extra petita*; it is ***ad minus*** (from the greater to the lesser) — “the mere finding that the claim is justified is not as far-reaching as the awarding of such an amount.”
- **Germany, § 301 ZPO (Eng., via research-a cross-check):** if only **part of a claim** is ready, the court may render a **partial judgment (*Teilurteil*)** on that part while the action continues — same action, not a new claim.
- **U.S. FRCP Rule 56(a):** summary judgment may be sought and granted on **“the part of each claim or defense”**; Rule 54(b) allows **partial final judgment** on fewer than all claims in the same case file.

**Not found:** a source requiring an adjudicator who would grant a **smaller amount** to **reject the original claim**, **introduce a new narrower claim**, and **accept that** instead. The opened doctrine runs the opposite way: partial success on the **same** claim, with the ungranted portion **deemed rejected** (Forlati) or left for later proceedings (§ 301 *Teilurteil*; FRCP 54(b)).

**Infra petita** (Forlati) covers failure to decide a claim at all — omission — not partial quantification. UNCITRAL Art 39(1) allows a party to request an **additional award** for claims **presented but not decided** — again omission, not partial grant.

### 3. How numeric remedies are aggregated

#### 3.1 Collegial courts: liability versus quantity

**Kornhauser & Sager (1993)** analyze aggregation of **binary legal issues** (contract formed? breach? liable?), not arithmetic combination of **damages figures** or **months of custody**. They show **no single default** when case-by-case and issue-by-issue protocols diverge, and they do not prescribe averaging of remedy amounts.

#### 3.2 Judgment aggregation theory (numeric values)

**Dietrich & List (2026)** and **List (2009)** survey aggregation when each member assigns a **numeric value**:

| Rule | Opened description | Typical use in sources |
|------|-------------------|------------------------|
| **Majority / propositionwise** | Majority on **binary** propositions; issue-by-issue | Default in doctrinal paradox examples; can be inconsistent across linked issues |
| **Median** | Middle value when individual estimates are ordered; **robust to outliers**; for odd *n*, majorities find it “not too high” and “not too low” (Dietrich & List 2026) | Galton’s ox-weight experiment; authors say median “performs reasonably well” overall |
| **Average (arithmetic mean)** | Sum divided by *n*; requires a **ratio scale**; **not** defined on ordinal grades | Common in forecasting; can be manipulated; fails consistency constraints when variables are linked (Table 2 example: median/average on *x*, *y*, *z* with *z* = *x* × *y*) |
| **Quantile / lowest / highest** | 0-quantile = lowest; 1-quantile = highest; 0.5 = median (Dietrich & List 2026) | Generalized family; not identified as standard court practice |
| **Distance-based / Kemeny–median** | Minimize total distance to individual judgments (List 2009 cites economic-theory literature) | Theoretical resolution of doctrinal paradox; not described as live court procedure |
| **Dictatorship** | One member’s value wins | Impossibility literature; not democratic default |

**Average versus majority on merits:** For **binary** collective judgments under independence and other axioms, **linear pooling collapses to dictatorship** (Dietrich & List cite List & Pettit line; List 2009 §6). So **majority on yes/no issues** and **averaging on quantities** answer **different question types**; averaging is **not** the standard aggregation of **merits votes**.

#### 3.3 Jury damages: deliberation, not mechanical average

- **FRCP Rule 48(c):** after verdict, the court **may poll jurors individually** — each juror’s assent is verified; not a numeric aggregation rule.
- **Quotient verdict doctrine** (Kimball; Florida L. Rev.): each juror states a **damage amount**, figures are summed and divided — **invalid** if jurors **agreed in advance** to be bound by the quotient. Using an average **only as a deliberation starting point**, without prior binding agreement, can be **valid**.
- **District of Kansas civil jury instructions (official):** jurors must reach a **unanimous** verdict through **deliberation**; damages must be based on evidence, not speculation — **no rule** that the court averages individual juror numbers.

So in opened common-law jury sources, **numeric remedy** emerges from **consensus after discussion**, not from a published **median/lowest/highest** formula across jurors’ written quantities.

#### 3.4 Criminal sentencing (evidence only)

**ICC Art 78(3)** (Rome Statute; Legal Tools summary): when multiple crimes are convicted, the chamber **(1)** pronounces an **individual sentence for each crime**, then **(2)** a **joint sentence** specifying total imprisonment. The joint sentence **cannot be less than the highest individual sentence**; overlap between crimes is handled in the **two-step** process, not by averaging judges’ preferred months.

**ICC Art 74(3):** merits decision by **majority** if not unanimous. Opened ICC sentencing materials describe **chamber deliberation** producing **one** sentence decision; they do **not** prescribe taking the **median** or **average** of each judge’s preferred term.

**Not found:** an English scholarly rule stating that collegial criminal panels **aggregate** disagreeing sentence lengths by **median**, **average**, **lowest**, or **highest** as a fixed formula. Opened ICC law uses **majority decision-making** plus **structured sentencing steps**, not arithmetic of individual numeric ballots.

#### 3.5 Secrecy and aggregation

**ICC Art 74(4):** “The deliberations of the Trial Chamber **shall remain secret**.”

**Not found** in opened sources: a rule that **secret voting** determines **which numeric aggregation function** (median vs average vs majority) applies. Secrecy appears as **deliberative confidentiality**, not as a tie between ballot secrecy and aggregation method. (Vote-secrecy design is explicitly out of scope for this run.)

### 4. Sources requiring each adjudicator to state a quantity

| Source | Requirement |
|--------|-------------|
| **Quotient verdict cases** (Kimball; Florida L. Rev.) | Each juror **may** specify an amount as part of a **quotient procedure**; the vice is **prior agreement to be bound**, not stating a number per se. |
| **FRCP Rule 48(c) polling** | Each juror **affirms or denies** the **verdict as a whole** after decision — not a mandatory pre-deliberation numeric ballot. |
| **ICC Art 78(3) sentencing** | Chamber pronounces **individual sentences per crime** then a **joint sentence** — institutional **output structure**, not a rule that **each judge** must file a private numeric vote before aggregation. |
| **Dietrich & List (2026)** | **Modeling** assumes each individual submits a numeric **evaluation** *Jᵢ* — theoretical, not a procedural requirement of any one court. |

**Not found:** an opened **official procedural rule** for **collegial judges** (as distinct from juries in quotient-verdict case law) that **requires each adjudicator to record a specific monetary or custodial quantity** before the collective remedy is formed. Opened collegial-court sources emphasize **majority on the decision** and **written reasons**, not per-judge damage figures.

### 5. Omid's premises tested

| Premise | Result in opened sources |
|---------|-------------------------|
| **Majority, not average, for merits** | **Supported** for binary merits: ICJ/ICC/UNCITRAL use **majority** on decisions; judgment-aggregation literature treats **majority/propositionwise** as the democratic default for yes/no issues. **Average** applies to **numeric estimates** in social-choice models, not to replacing a **for/against** merits vote. |
| **Abstain as negative with written reason** | **Not found** as a general rule. Abstention ranges from **excluded** (ICJ) to **ignored in the tally** (RONR) to **equivalent to no** (absolute quota). Yates: abstention can **favor one side** depending on procedure — not fixed as “against claimant.” **Written reason for abstention:** not found as a requirement in opened adjudication rules. |
| **Smaller amount requires new chained claim** | **Contradicted** by Forlati (partial uphold → rest **deemed rejected**, same claim), § 301 *Teilurteil*, FRCP partial judgment, and *ad minus* arbitration doctrine. |
| **Adjudicators must state a quantity** | **Weak support only** in jury **quotient** case law (optional deliberation tactic) and in **theoretical** aggregation models — **not found** as a general collegial-judge rule. |

## Questions for Omid

1. **Three-way ballot definition:** Opened sources use **binary** votes (for/against, liable/not, majority on award) or **numeric estimates** in theory — not “claimant / respondent / abstain.” Should the pilot define **abstain** procedurally (non-vote, no, or separate outcome), or is a three-label merits ballot a **new** rule without opened precedent?

2. **Abstain and the claimant:** If abstention is **not** uniformly “against the claimant” in opened rules, should a pilot rule **fix** that direction, or adopt **RONR-style** non-counting, or **ICJ-style** prohibition of abstention on merits?

3. **Partial numeric grant:** Sources treat less-than-requested relief as **same claim, remainder rejected** (Forlati). Does the pilot adopt that, or does Omid still want **claim-splitting** for smaller amounts despite no opened support?

4. **Numeric aggregation function:** For disagreeing adjudicators (3 vs 6 vs 12 months), opened theory offers **median**, **average**, **quantiles**, and **majority-on-linked-issues** — each with inconsistency or manipulation risks. Which function is intended for the pilot: **median** (Dietrich & List’s favored compromise), **majority on liability then single judge sets quantity**, **deliberative consensus** (jury model), or something else?

5. **Per-adjudicator quantity ballot:** Should adjudicators record **for/against only**, or **for/against plus amount**? Opened collegial rules do **not** require the latter; quotient-verdict law concerns **juries** and **binding** pre-agreements. Is a mandatory numeric ballot a **deliberate departure**?

6. **Issue-by-issue versus case-by-case:** Kornhauser & Sager show the **protocol choice changes outcomes**. Should liability, quantity, and remedy type be aggregated **separately** (premise-based / issue-by-issue), or only on **bottom-line disposition** (case-by-case)?

7. **Linked constraints:** If quantity must satisfy legal relationships (e.g., total ≤ requested; custody months tied to offense grade), Dietrich & List show **issue-wise median/average can break constraints**. Should aggregation be **constraint-aware** (optimization/distance-based rules) rather than raw median/majority?
