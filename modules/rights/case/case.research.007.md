# Case Research 007 — Arbitration as expert

## Table of Contents

- [Status](#status)
- [Question and Goals](#question-and-goals)
- [Participants](#participants)
- [Methodology](#methodology)
- [Findings](#findings)
  - [Omid's premises (not findings)](#omids-premises-not-findings)
  - [Judge vs arbitrator vs expert — source definitions](#judge-vs-arbitrator-vs-expert--source-definitions)
  - [Testing premise 1: seated judge must not hand dispute to arbitrator](#testing-premise-1-seated-judge-must-not-hand-dispute-to-arbitrator)
  - [Testing premise 2: arbitrator is not "any ordinary adjudicator"](#testing-premise-2-arbitrator-is-not-any-ordinary-adjudicator)
  - [Testing premise 3: contract-named experts advise; judge rules from aggregate](#testing-premise-3-contract-named-experts-advise-judge-rules-from-aggregate)
  - [Expert determination vs arbitration — similarities and differences](#expert-determination-vs-arbitration--similarities-and-differences)
  - [Hybrid expert models (panel advises vs decides)](#hybrid-expert-models-panel-advises-vs-decides)
  - [Civil claim vs criminal complaint as one process](#civil-claim-vs-criminal-complaint-as-one-process)
- [Questions for Omid](#questions-for-omid)

## Status

Active

Reopened on 2026-10-07. It was recorded as Complete, which the facet reserves for an inquiry whose every question carries a final per-question status and which then carries a Conclusion. This file has no Conclusion, and items 2, 3, and 6 under `Questions for Omid` were left open. He has said the adjudication questions this research covers are settled in a later chat, so the inquiry is not finished.

## Question and Goals

**Questions**

1. How do English scholarly and official sources (UNCITRAL, expert determination, hybrid expert adjudication) define judge, arbitrator, and expert — and do they support or contradict Omid's proposed split? — Answered
2. What similarities and differences between arbitration and expert determination would force two role types in a justice model, and which would not? — Answered
3. Do any consulted sources treat civil claims and criminal complaints as one procedural process (especially in digital/agent forums), or explicitly refuse to? — Answered (mostly **not found** on digital/agent unification)

**Goals**

- Test Omid's definitions against inspectable sources; record **not found** where sources are silent.
- State similarities/differences relevant to whether judge and arbitrator must remain separate types.
- End with precise blocking questions for Omid.
- No graph model, no code, no repository edits.

**Scope**

- English scholarly and official sources only.
- UNCITRAL Model Law, UNCITRAL Arbitration Rules, UNCITRAL Notes on Organizing Arbitral Proceedings; WIPO/DIS expert-determination materials; selected English scholarship on experts in arbitration and on civil/criminal procedural reform.
- Read-only context from organization `case` / `contract` modules noted but not edited.
- Omid's premises are hypotheses to test, not adopted findings.

## Participants

| Participant | Role | Review |
|---|---|---|
| Research run agent `bc-e513f8ef-ca59-5384-8954-d03114e4fc50` | Researcher | Not yet reviewed |

## Methodology

Single-pass desk research, 2026-09-27.

1. Loaded Memar Research facet structure from `memar/docs/documentation-research.md` (mandatory core sections).
2. Read-only scan of organization `modules/rights/case` and `modules/rights/contract` for pilot vocabulary (`judge`, `arbitrator`, contract disputes).
3. Sources consulted (inspectable URLs only):
   - **UNCITRAL Model Law on International Commercial Arbitration (2006)** — [official ebook PDF](https://uncitral.un.org/sites/default/files/media-documents/uncitral/en/19-09955_e_ebook.pdf), cited as *UNCITRAL Model Law*.
   - **UNCITRAL Notes on Organizing Arbitral Proceedings (2016)** — [PDF](https://uncitral.un.org/sites/default/files/media-documents/uncitral/en/arb-notes-2016-e.pdf), cited as *UNCITRAL Arb. Notes*.
   - **UNCITRAL Arbitration Rules** — [overview page](https://uncitral.un.org/en/texts/arbitration/contractualtexts/arbitration).
   - **WIPO — What is Expert Determination?** — [page](https://www.wipo.int/en/web/amc/expert-determination/what-is-exp).
   - **DIS — Expert determination** (official) — [page](https://www.disarb.org/en/arbitration-and-alternative-dispute-resolution/expert-determination).
   - **DIS Practice Note on the Use of Experts in Arbitration** — [PDF](https://www.disarb.org/fileadmin/user_upload/Foerderung_Vernetzung/DIS-Praxislabor_Praxisgruppe_Sachverstaendige_Practice_Note_Experts.pdf).
   - **Ruth Fenton**, "A Civil Matter for a Common Expert" (2006) — [Pepperdine DRLJ](https://digitalcommons.pepperdine.edu/drlj/vol6/iss2/4).
   - **John Kendall**, *Dispute Resolution: Expert Determination* (2d ed. 1992) — cited via Fenton and practitioner summaries.
   - **Ünüvar**, "The Role of Experts in International Arbitration" — [Istanbul University journal PDF](https://cdn.istanbul.edu.tr/file/JTA6CLJ8T5/DF3570CDE6384FC79BF9A1DA3252442C).
   - **Saidov**, "Challenging A Third-Party Expert Determination" (2019) — [NUS PDF](https://law.nus.edu.sg/wp-content/uploads/2020/04/018_2019_Djakhongir-Saidov.pdf).
   - **Swiss Federal Supreme Court analysis** (expert determination vs arbitration) — [Landolt & Koch article PDF](https://static.showit.co/file/2fQ6yf-Ti5oR321RPuMa1g/325307/article_phl_expertdetermination_swiss_court_distinguishes_between_expert_determination_and_arbitration.pdf).
   - **Lexology** — "Conflicts between Expert Determination Clauses and Arbitration Clauses" — [article](https://www.lexology.com/library/detail.aspx?g=b9490021-ee1d-4770-a4b9-8db94d12fa56).
   - **Ion Meyn**, "Why Civil and Criminal Procedure Are So Different: A Forgotten History" (2017) — [Fordham Law Review](https://fordhamlawreview.org/issues/why-civil-and-criminal-procedure-are-so-different-a-forgotten-history/).
   - **Rosen-Zvi & Gideon**, "Overcoming Procedural Boundaries" — [Virginia Law Review / Stanford copy](https://www.law.stanford.edu/wp-content/uploads/sites/default/files/event/266730/media/slspublic/Rosen-Zvi-Overcoming-Procedural_boundaries.pdf).
   - **Belgium JustOne** (digital case platform) — [Bridg case study](https://www.bridg-software.eu/en/solutions/justone).
4. Where a point is not supported by these sources: **not found** (no reconstruction from training data).

## Findings

### Omid's premises (not findings)

From the justice-pilot brief and organization read-only context — to be tested, not adopted:

1. A **seated judge** whom a party chose and paid must **not** hand the dispute to an **arbitrator**.
2. An **arbitrator** is not "any ordinary person who can adjudicate."
3. An **arbitrator** is an **expert the contract parties named**, and the **judge rules from the aggregate** of those experts' opinions.
4. The **civil-claim vs criminal-complaint** split is a paper-era detail; a computer-and-agent forum might treat them as **one process**.

Organization read-only note, added 2026-10-07: `case.md` no longer carries a rule in which judges set an arbitrator for contract disputes; the evening of 2026-09-27 replaced it with one judge edge, and `judge.md` no longer asks whether the voter is the case judge or the contract's arbitrator. Item 3 under `Questions for Omid` therefore rests on a premise the repository has withdrawn, and the answer is on [case.handoff.md](case.handoff.md) under Ambiguities Resolved.

### Judge vs arbitrator vs expert — source definitions

| Role (source usage) | Who appoints | Primary function | Binding output | Typical enforcement |
|---|---|---|---|---|
| **Court judge** (state litigation) | State / court roster | Adjudicates dispute in public court process | Judgment | Court enforcement machinery |
| **Arbitrator / arbitral tribunal** (UNCITRAL Model Law) | Parties (Art. 11); court assists only on appointment/challenge (Arts. 6, 11) | **Decides** the dispute; issues **award** (Art. 31) | Arbitral award | National arbitration statutes; New York Convention for foreign awards |
| **Expert witness** (party- or tribunal-appointed in arbitration) | Party or tribunal (UNCITRAL Arb. Notes paras 92–105) | **Assists** tribunal with specialized knowledge; does not issue award | Expert report / testimony | None standalone — evidence for tribunal |
| **Expert determiner** (expert determination) | Parties by contract (WIPO; Saidov) | **Decides** defined issue using expertise | Determination (contractual) | Breach-of-contract action; not NYC award (Fenton; Kendall via Fenton) |

**UNCITRAL Model Law, Art. 5:** "In matters governed by this Law, **no court shall intervene** except where so provided in this Law."

**UNCITRAL Model Law, Art. 8(1):** If an action is brought on a matter covered by an arbitration agreement, the court **shall refer the parties to arbitration** (on timely request), unless the agreement is void — i.e. **exit litigation, enter arbitration**, not delegate while remaining the deciding forum.

**UNCITRAL Model Law, Art. 26(1):** The arbitral tribunal **may appoint experts to report** on issues **to be determined by the arbitral tribunal** — decision stays with the tribunal.

**UNCITRAL Arb. Notes, para. 101:** A tribunal-appointed expert's function is preparing a report or **assisting the tribunal** in understanding technical issues.

**Fenton (2006):** In **expert determination**, "the experts themselves make the decision"; in arbitration, experts clarify issues so the tribunal can decide. Expert-determination outcomes are binding as **contract**, not enforceable like arbitral awards under the New York Convention.

**WIPO:** Parties may select an expert together; the determination is **binding unless the parties agree otherwise**.

**DIS (expert determination):** Parties jointly select an "arbitration expert" (DIS terminology); the decision is **provisionally binding** until set aside or modified by a **court or arbitral tribunal**.

### Testing premise 1: seated judge must not hand dispute to arbitrator

**What sources support**

- **Separation of forums:** Art. 8 requires **referral to arbitration** (parties leave the court process for a parallel arbitral process), not a seated judge retaining the case while an arbitrator decides it. Art. 5 limits court intervention in arbitral matters.
- **Tiered contract design:** Lexology (expert determination vs arbitration conflicts): parties may require expert determination **first**, then **review by an arbitral tribunal** — sequential forums, not simultaneous delegation from a seated judge.
- **DIS:** Recommends combining expert determination with arbitration; expert decision is **provisionally** binding and may be set aside by court or tribunal.

**What sources contradict or do not match the premise**

- **Party-chosen and paid decision-makers are standard in arbitration:** UNCITRAL Model Law Art. 11(3)(a) — in a three-arbitrator tribunal, **each party appoints one arbitrator**; parties routinely pay tribunal costs. This is not framed as a judge "handing off" a seated case, but it **is** party-chosen, party-paid adjudication outside the court.
- **Court's role at the gateway:** The court **does** send disputes to arbitrators when an arbitration agreement exists (Art. 8). That is incompatible with "never hand to arbitrator" if read broadly — but it is **referral out**, not delegation while the judge remains the deciding officer.

**Not found**

- A rule that a **seated judge whom a party chose and paid** must not hand a dispute to an arbitrator — as Omid phrases it (party-chosen **judge**, still seated). Consulted international sources distinguish **state judges** from **party-appointed arbitrators**; they do not describe a hybrid "party-paid seated judge" who may or may not delegate. **Not found** in consulted English official/scholarly sources.

### Testing premise 2: arbitrator is not "any ordinary adjudicator"

**Partial support (specialization / qualification)**

- UNCITRAL Model Law Art. 11(5): appointing authority must have **due regard to qualifications required by the parties' agreement**.
- UNCITRAL Arb. Notes, paras 92–93: experts and arbitrators are selected for **specialized knowledge** where needed.
- Practitioner literature (e.g. selection-of-arbitrators scholarship cited in search results): tribunals may be designed with a **legally trained chair** and **party-appointed technical specialists**.

**Contradiction (arbitrator as adjudicator, not mere expert)**

- UNCITRAL Model Law Arts. 28–31: the **arbitral tribunal decides** the dispute and issues a **signed award** with reasons.
- Fenton, Lexology, Swiss Supreme Court analysis: **arbitration** yields an **award** with **res judicata**-type effect (Swiss analysis); **expert determination** binds on **narrower contractual grounds** without that arbitral status.
- An arbitrator is therefore **not** "any ordinary person" only in the weak sense that parties may require qualifications — but sources **do** treat arbitrators as **ordinary adjudicators of the dispute** (private judges), not as non-adjudicative specialists.

**Not found**

- A definition of **arbitrator** as exclusively a **non-deciding** contract-named expert. Sources reserve that role for **expert witnesses** and **expert determiners**, not arbitrators.

### Testing premise 3: contract-named experts advise; judge rules from aggregate

**Strong contradiction in arbitration sources**

- **Decision-maker is the tribunal, not the experts:** UNCITRAL Model Law Art. 26(1) — experts report on issues **to be determined by the arbitral tribunal**.
- **Delegation of adjudication prohibited:** Ünüvar (citing Redfern & Hunter, IBA commentary): accepting expert opinions without tribunal assessment **delegates the arbitrator's adjudicative function to an expert, which is prohibited** in international arbitration.
- Same source: tribunal **shall not, in any case, delegate its adjudication duty and authority** to a legal expert.
- **UNCITRAL Arb. Notes, paras 95–98:** Party-appointed experts may produce **joint reports** on agreement/disagreement; tribunal still decides.
- **Fenton (Channel Tunnel example):** A **panel of experts** may give an interim decision, but parties may later go to **arbitration**, and the tribunal **could reverse** the experts' decisions.

**Closer to Omid's model — but under different labels**

- **Expert determination (WIPO, Saidov, DIS):** Parties name an expert (or experts); the expert **decides** the referred issue. There is **no separate judge** aggregating opinions — the expert **is** the decision-maker for that issue.
- **DIS three-expert panel:** Each party appoints one expert; two appoint a chairman; the panel issues a **provisionally binding** decision — closer to "named experts decide," still **without** a separate judge aggregating (DIS official page).
- **Expert teaming (DIS Practice Note; practitioner literature):** Tribunal appoints one expert from each party's list; they produce a **joint report**; **tribunal** still adjudicates — advises, does not replace judge.

**Summary vs premise 3**

| Element of Omid's premise | In consulted sources |
|---|---|
| Contract parties **name** experts | Yes — expert determination, party-appointed arbitrators/experts |
| Experts are **not** free-standing public judges | Yes — private appointment |
| A **separate judge** rules from **aggregate of expert opinions** | **Not found** as the standard arbitration pattern; **contradicted** where tribunal must not delegate adjudication. Closest match: **expert determination** (expert decides) or **expert reports as evidence** before a tribunal/judge — not "judge aggregates named arbitrators." |

### Expert determination vs arbitration — similarities and differences

#### Similarities (would **not** by themselves force two types)

- Both are **contractually agreed** private dispute resolution (Fenton; WIPO; Lexology).
- Both use **independent third parties** (DIS; WIPO).
- Both can involve **party-appointed specialists** (UNCITRAL Arb. Notes; DIS).
- Both aim at **finality** on defined issues (subject to narrow challenge grounds — Saidov; Fenton).
- **Hybrid and tiered clauses** are common: expert determination for technical issues, arbitration for broader disputes (Lexology; DIS).
- **Expert teaming / joint expert reports** blur evidentiary and decision lines but still leave a tribunal/judge as award-maker in arbitration (DIS Practice Note; UNCITRAL Arb. Notes).

#### Differences (would **force** two types if the model must track source law)

| Dimension | Arbitration | Expert determination |
|---|---|---|
| **Who decides** | Arbitral tribunal | Expert(s) |
| **Legal basis** | Arbitration statutes / Model Law | Contract (WIPO; Lexis guidance) |
| **Due process** | Statutory procedural fairness (Fenton; Kendall via Fenton) | Whatever contract provides; often minimal (Fenton) |
| **Enforcement** | Arbitral award; NYC internationally (Fenton) | Contract action; not NYC award (Fenton; Swiss analysis) |
| **Scope of powers** | Broad dispute resolution (Lexology) | Narrow, defined issues (WIPO; DIS; Saidov) |
| **Challenge grounds** | Statutory setting-aside (Lexology) | Fraud, collusion, material departure from instructions, etc. (Fenton; Saidov) |
| **Res judicata** | Award character (Swiss analysis) | Binding without full res judicata (Swiss analysis) |
| **Expert's role inside arbitration** | Assist tribunal only (UNCITRAL; Ünüvar) | N/A — expert **is** determiner |

**For a pilot model:** If "judge" must mean **state/seated adjudicator** and "arbitrator" must mean **private adjudicator issuing an award**, sources **force** separation. If "arbitrator" is redefined as **contract-named technical expert**, sources align that role with **expert determination** or **expert witness**, **not** with UNCITRAL **arbitrator** — and the deciding judge/tribunal remains a **separate** type.

### Hybrid expert models (panel advises vs decides)

| Model | Experts' role | Decision-maker | Source |
|---|---|---|---|
| Party-appointed expert witnesses | Evidence / opinion | Tribunal or court | UNCITRAL Arb. Notes paras 94–100; Fenton |
| Tribunal-appointed expert | Report / assist understanding | Tribunal | UNCITRAL Model Law Art. 26; UNCITRAL Arb. Notes para. 101 |
| Expert teaming | Joint report after party-nominated lists | Tribunal | DIS Practice Note; Global Arbitration News (Sachs) |
| Expert determination panel (DIS) | Decide referred issue | Experts (provisional) | DIS official expert-determination page |
| Dispute review board / Channel Tunnel panel | Interim decision | Experts (reversible later) | Fenton (Channel Tunnel) |
| Adjudication (construction) | Binding interim | Adjudicator (expert profile) | Fenton |

**Pattern:** Whenever sources describe **hybrid** arrangements, they still distinguish **(a)** those who **decide** and **(b)** those who **inform** the decision — and treat **undisclosed delegation** of (a) to (b) as impermissible in arbitration (Ünüvar).

### Civil claim vs criminal complaint as one process

**Sources that compare or propose unification (not digital/agent-specific)**

- **Meyn (2017):** The first draft Federal Rules of Criminal Procedure (1941) proposed a **unified procedural code** for **all litigation**, civil and criminal; the final 1944 rules **split** them after committee conflict. Meyn questions whether civil and criminal procedure **inherently** require different treatment.
- **Rosen-Zvi & Gideon, "Overcoming Procedural Boundaries":** Proposes replacing the civil/criminal procedural split with a model on two axes — **balance of power between parties** and **severity of sanction** — not on civil vs criminal label.

**Digital platforms — shared infrastructure only**

- **Belgium JustOne:** One platform carries **criminal** and developing **civil** modules; case files transfer between prosecution and court **without re-entry** — shared workflow IT, not a merged substantive/procedural code ([Bridg case study](https://www.bridg-software.eu/en/solutions/justone)).
- **Greece OSDDY-PP, Palestine Mizan, Spain Digital Justice:** Integrated **case management** across civil and criminal courts — administrative integration; consulted English descriptions do **not** merge civil claims and criminal complaints into one adjudicative procedure.

**Not found**

- An English scholarly or official source that treats **civil claim** and **criminal complaint** as **one adjudicative procedure** because of **computers or agents**.
- A source that **explicitly refuses** such unification **on digital/agent grounds** (as opposed to traditional civil/criminal distinctions Meyn and Rosen-Zvi discuss).

**Brief assessment of Omid's premise 4:** Reform literature **does** question the civil/criminal procedural split on **policy/history** grounds (Meyn; Rosen-Zvi). Digital justice projects **unify case files and workflows**, not the underlying claim/complaint procedural taxonomy. **Not found:** agent/computer forum as justification for a single process.

## Questions for Omid

1. **Label for contract-named experts:** Consulted sources call party-named deciders **experts** (expert determination) or **arbitrators** (private adjudicators). Your premise 3 uses **arbitrator** for the expert role. Should the pilot model use source-aligned labels (`expert determiner` / `expert witness` vs `arbitrator`), or is renaming intentional?

2. **Who aggregates:** If the judge rules from an aggregate of contract-named experts' opinions, is that aggregate a **formal vote/mechanism** on the case, or the judge's reasoned judgment after reading expert outputs? Sources prohibit **automatic** incorporation of expert opinions into awards without tribunal assessment (Ünüvar) — what is the pilot rule?

3. **Judge "sets arbitrator" (organization open question):** `case.md` says judges set the arbitrator on contract disputes. Does that mean (a) the judge **appoints** contract experts before deciding, (b) the judge **refers** parties to a separate arbitral process (Art. 8 pattern), or (c) the judge **records** parties' pre-named experts only? This blocks the `judge` edge vs contract `arbitrator` edge.

4. **Party-chosen judge:** Premise 1 assumes a **party-chosen, party-paid judge**. Is that the pilot's `judge` edge (odd pool on case), a different role, or a contract-only forum? UNCITRAL party-paid appointees are **arbitrators**, not state judges — clarify which source category the pilot reuses.

5. **Two types — minimum split:** Sources force at least **decision-maker** vs **expert assistant** (and often **court judge** vs **private arbitrator** for enforcement). Can the pilot collapse `judge` and `arbitrator` into one adjudicator type with a `forum` attribute, or must contract experts remain a third type?

6. **Civil vs criminal in one process:** Meyn/Rosen-Zvi support **procedural reform** axes, not digital/agent unification. Should the pilot (a) keep separate claim/complaint entry types with shared case infrastructure (like JustOne), or (b) pursue a single filing type? No consulted source validates (b) on computer/agent grounds.
