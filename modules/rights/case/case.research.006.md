# Case Research 006 — Blind collegial voting

## Table of Contents

- [Status](#status)
- [Question and Goals](#question-and-goals)
- [Participants](#participants)
- [Methodology](#methodology)
- [Findings](#findings)
  - [1. Blind collegial voting (independent opinions before pooling)](#1-blind-collegial-voting-independent-opinions-before-pooling)
  - [2. Hiding the adjudicator from parties while binding the vote to a real person](#2-hiding-the-adjudicator-from-parties-while-binding-the-vote-to-a-real-person)
- [Questions for Omid](#questions-for-omid)

## Status

Complete

## Question and Goals

**Questions**

| # | Question | Status |
|---|----------|--------|
| Q1 | Do English scholarly or official sources describe requiring independent collegial opinions or votes before pooling, and do they document failure modes where one expert drafts and others sign, or anchoring/cascade effects in deliberating versus simultaneous secret ballots? | Answered |
| Q2 | Do English scholarly or official sources describe hiding an adjudicator's identity from parties while still binding each vote to a real person for later pooling and audit? | Answered |

**Goals**

| Goal | Status |
|------|--------|
| Evaluate the two ideas on their own, using inspectable English scholarly or official sources only | Met |
| Describe what the sources actually do or find — not a graph or organization design | Met |
| Where no inspectable source was found, write **not found** and do not reconstruct from training data | Met |
| End with blocking questions for Omid | Met |

**Scope**

In scope: blind/simultaneous/independent collegial voting; expert-panel independence; anchoring and information cascades; anonymized judging; sealed identity with audit; binding a vote to a person without revealing that person to parties. Out of scope: modeling the justice bundle graph; code; country-specific procedure surveys (see `research-a.md`, `research-b.md`). Read-only awareness of pilot context only.

## Participants

| Participant | Roles | Review |
|-------------|-------|--------|
| Omid | Questioner, Goal-setter | Not a reviewer of this file |
| bc-e6601049-3868-5929-86be-5ad92ce0e7f7 | Researcher | Not yet reviewed |

## Methodology

Single-pass desk research, 27 September 2026. Loaded Memar Research facet structure from `memar/docs/documentation-research.md` (mandatory core sections). Web search and direct fetch of English scholarly articles, law-review essays, official rules, agency guidance, and technical specifications. Persian and non-English sources excluded. Where a point is not supported by a source consulted here: **not found**.

**Sources consulted (inspectable URLs)**

- Barry, "Judging Better Together: Understanding the Psychology of Group Decision-Making on Panel Courts and Tribunals," *International Journal for Court Administration* (2023): https://iacajournal.org/articles/10.36745/ijca.479
- Hirschi, Luchkina & Mavrogenis, "Judicial Deliberation," MPI Luxembourg Working Paper (2022): https://www.mpi.lu/fileadmin/mpi/medien/research/WPS/MPILux_WP_2022_2__Judicial_Deliberation_LHetal_final__003_.pdf
- Kolb, "Secrecy of Deliberations," *Max Planck Encyclopedia of Public International Law*: https://opil.ouplaw.com/display/10.1093/law-mpeipro/e2123.013.2123/law-mpeipro-e2123
- Drozdova, "Ex Ante Versus Ex Post Deliberations: Two Models of Judicial Deliberations in Courts of Last Resort," *U. Conn. Law* working paper: https://digitalcommons.lib.uconn.edu/cgi/viewcontent.cgi?article=1285&context=law_papers
- Kelemen, "Dissenting Opinions in Constitutional Courts," *German Law Journal* 14(8) (2013): https://www.cambridge.org/core/services/aop-cambridge-core/content/view/FF33A6CB627C4E0773C0E4F12ACDAD9F/S2071832200002297a.pdf/dissenting_opinions_in_constitutional_courts.pdf
- Demetriou, "The Role of Référendaires at the European Court of Justice," *EC Tax Journal* 7(1) (2003/4): https://khpplc.co.uk/wp-content/uploads/2024/09/ectj-vol-7-1-1-the-role-of-referendaires-at-the-european-court-marie-demetriou.pdf
- Vermeule, "Open-Secret Voting" (draft, Collège de France symposium): https://www.college-de-france.fr/media/jon-elster/UPL31839_Vermeule_scrutin.pdf
- Urfalino & Costa, "Public and Oral Voting in FDA's Advisory Committees" (draft): https://www.college-de-france.fr/sites/default/files/documents/jon-elster/UPL5102174867140254047_UPL12995_urfalino_costa_scrutin.pdf
- Newham & Midjord, "Do Expert Panelists Herd? Evidence from FDA Committees," DIW Discussion Paper 1825 (2019): https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3476536
- Bag & Sharma, "Sequential Expert Advice: Superiority of Closed-Door Meetings" (2018): https://cie.itam.mx/sites/default/files/u779/secret-advice-02march18.pdf
- Rafiee Rad & Roy; Eckert et al., "Anchoring as a Structural Bias of Deliberation," *Erkenntnis* (2024): https://link.springer.com/article/10.1007/s10670-024-00814-7
- Brazilian collegial anchoring experiment (SciELO): https://www.scielo.br/j/rdgv/a/fdfQjMgY7q3v4Y4LfCyRFXF/abstract/?lang=en
- Zamir & Engel, "Sunlight Is the Best Disinfectant—Or Is It? Anonymity as a Means to Enhance Impartiality," *Arizona Law Review* 63:1063 (2021): https://arizonalawreview.org/pdf/63-4/63arizlrev1063.pdf
- OpenMed, "Blinded clinician adjudication" (official docs): https://openmed.life/docs/evaluation/blinded-adjudication/
- Benaloh et al., ElectionGuard specification v2.1.0: https://cryptojedi.org/papers/EG-spec-v2.1.0.pdf
- Benaloh, "SOBA: Secrecy-preserving Observable Ballot-level Audit" (EVT/WOTE 2011): https://static.usenix.org/events/evtwote11/tech/final_files/Benaloh.pdf
- BlindReview eprint (2026): https://eprint.iacr.org/2026/888.pdf
- Federal Rules of Evidence 706 (official, LII): https://www.law.cornell.edu/rules/fre/rule_706
- FJC, *Reference Manual on Scientific Evidence* 2d ed., ch. on court-appointed experts: https://www.fjc.gov/sites/default/files/2012/sciman0c.pdf
- Smith v. Arizona, 602 U.S. 779 (2024) — via JAAPL summary: https://jaapl.org/content/54/1/109

**Limits:** No systematic meta-review; no non-English corpus; technical papers describe mechanisms in peer review/elections, not civil courts, unless noted.

## Findings

### 1. Blind collegial voting (independent opinions before pooling)

#### What collegial courts actually do

- **Secret deliberation is the norm; simultaneous secret ballot is not.** Hirschi, Luchkina & Mavrogenis survey collegiate courts worldwide and report that, in most systems analysed, judges communicate on the case before judgment, usually in **secret deliberation** after any oral hearing — not through a published simultaneous ballot (MPI Luxembourg WP 2022). Kolb (*MPEPIL*, "Secrecy of Deliberations") states that most international and municipal courts follow a basic rule of **secrecy of deliberations** so judges can exchange views without outside pressure; the ICJ holds deliberations behind closed doors while hearings remain open to parties.
- **Two deliberation cultures, both draft-heavy.** Drozdova distinguishes **ex ante** courts (French/European style: merits opinion drafted and negotiated **before** the conference vote) from **ex post** courts (US Supreme Court style: conference vote after argument, then opinion circulation). In both, she finds decisions emerging through **multiple small-group interactions** involving judicial assistants, not one prolonged face-to-face debate — so "deliberation" in practice often means sequential exposure to drafts and notes, not isolated simultaneous votes.
- **Rapporteur/draft-first workflow is institutional, not accidental.** At the CJEU, Demetriou describes a judge rapporteur producing a **draft judgment** (first draft often written by a référendaire) for deliberation; the judgment must be **signed by all judges** who heard the case, with **no dissenting opinions** — minority judges still participate until the text is something they can sign. Kelemen notes that in many European constitutional courts voting is **secret**, every judge **signs** the decision, and the public learns who dissented only if a judge writes a separate opinion.
- **"One writes, others sign" as a described failure mode:** not found as that exact phrase in the sources above. What *is* documented: (a) CJEU practice where the rapporteur's first draft sets the agenda and aims to avoid controversial points (Demetriou); (b) US **surrogate expert** testimony where a second expert repeats a non-testifying analyst's conclusions — courts treat non-independent "independent opinion" as constitutionally insufficient (*Smith v. Arizona*, 602 U.S. 779 (2024), summarized JAAPL 2026); (c) Italian constitutional practice of **replacing the rapporteur judge** to draft the judgment as a possible signal of internal dissent (Panizza, cited in Kelemen) — a procedural substitute for published dissent, not blind voting.

#### Anchoring, cascades, and order effects

- **First opinion anchors later speakers.** Rafiee Rad & Roy's deliberation model (*Erkenntnis* 2024) shows **anchoring as a structural bias**: when participants announce preferences sequentially and update after each step, the **first ranking announced** pulls later announcements toward it; compounding updates make later voices comparatively weak. A Brazilian simulation (SciELO, RDGV) finds preliminary evidence that **rapporteur-recommended damages** anchor other "judges'" awards in a medical-liability scenario.
- **Cascade / herd behaviour in expert panels.** Barry (*IJCA* 2023) reviews **cascade effects** (following those who spoke first) and cites mock-jury work where the **fourth juror** in a six-person jury was sensitive to the preceding vote sequence. Newham & Midjord (DIW 2019) exploit FDA's **2007 switch from sequential to simultaneous voting**: structurally estimated **~9% of sequential votes are "herd votes"**; ~half of panelists are willing to vote against private assessment when earlier votes point the other way; **simultaneous voting improves information aggregation** in their model. Urfalino & Costa (FDA draft) argue **oral sequential voting** lets later votes be influenced by earlier ones; the 2007 reform moved to **simultaneous electronic voting** (votes locked before disclosure), while keeping votes **public and attributable** to each expert — transparency to watchers, not secrecy from colleagues.
- **Secrecy of advice versus transparency of advice.** Bag & Sharma (2018) model two experts giving **sequential cheap-talk advice** to a decision-maker with career concerns: **secrecy (closed-door) weakly dominates transparency** for decision quality because secrecy lets the **late expert be pivotal** more often; under transparency an early opinion can **stifle** valuable late views. This is expert-advice theory, not a court rule, but it targets the same failure mode: seeing others' views before committing.
- **Deliberation can amplify error as well as correct it.** Barry summarizes **conformity**, **dissent aversion**, and **group amplification of error** on panel courts; experimental work on mock juries is mixed on whether deliberation dampens or amplifies bias. Vermeule (open-secret voting draft) proposes **open vote followed by secret vote** as a second-opinion mechanism for **expert panels and advisory committees** where members share goals but hold dispersed information; he notes FDA's 2008 move toward **public balloting** for transparency, and suggests agencies might combine public and secret ballots — not a rule courts apply.

#### Independent opinion requirements (court experts)

- **FRE 706** and the FJC *Reference Manual* describe **court-appointed experts** as **testifying witnesses**: parties may depose and cross-examine; appointment is meant to address party-expert shopping, with acknowledged risk that court-appointed experts gain an "aura of infallibility" (FRE 706 advisory notes, LII). The manual distinguishes **Rule 706 experts** (evidence to the trier of fact) from **technical advisors** (non-testifying advice to the judge). **not found** in these sources: a procedural rule requiring each panel member to file a sealed independent report before seeing colleagues' reports in ordinary civil collegial courts.
- **Constitutional "independent opinion"** in US forensic practice means the testifying expert must genuinely analyze underlying material, not parrot an absent analyst (*Smith*; State v. Ortiz-Zape, 367 N.C. 1 (2013), dissent discussion).

#### Summary table (Q1)

| Topic | What sources report |
|-------|---------------------|
| Deliberation vs simultaneous secret ballot | Collegial courts: **secret deliberation** standard; **simultaneous secret ballot** before deliberation: **not found** as a general court rule |
| One drafts, others sign | **Rapporteur draft + collective signature** documented (CJEU, many constitutional courts); **"sign without reading"**: **not found** |
| Anchoring / first opinion | **Supported** in deliberation models and experiments (Rafiee Rad & Roy; Brazilian collegial simulation) |
| Sequential vs simultaneous voting | **Sequential increases herding** in FDA expert panels; simultaneous voting improved aggregation (Newham & Midjord; Urfalino & Costa) |
| Blind independent reports before pooling | **not found** for collegial civil courts; **supported** as design goal in expert-committee voting reform literature |

### 2. Hiding the adjudicator from parties while binding the vote to a real person

#### Anonymity of decision-makers (general)

- Zamir & Engel (*Arizona L. Rev.* 2021) argue **concealing decision-maker identity** can improve impartiality when gainers and losers could pressure or reward the decider; examples include **anonymous juries**, **double-blind peer review**, WHO emergency committees (identity confidential until work completes), and the **S&P 500 Index Committee** (members historically anonymous). They stress **anonymity and accountability are not mutually exclusive**: reasons may be published without naming individuals; **internal accountability** (editors, auditors, fellow committee members) can persist; **scope** and **time** of anonymity vary (Part III F–I).
- **Secret voting vs anonymous decision-maker:** Section III.G draws a distinction: **anonymous decision-making** hides *who* decided; **secret voting** hides *how each member voted* while identities may be known. Secret ballots can **complement** anonymity in committees but reduce **internal accountability** among members.
- **Judges identified to parties; deliberation secret:** Kolb and MPI Luxembourg confirm parties typically know **which judges sit**; secrecy covers **deliberations and vote breakdown**, not assignment. ECJ: no published dissent; vote counts not in the main judgment (Kolb; Kelemen).
- **Hiding trial judge identity from parties in ordinary civil litigation:** **not found** as a standing procedural device in the sources consulted. Anonymous juries protect **jurors**, not judges. Per curiam and unsigned opinions address **opinion authorship**, not concealing which judge was assigned to the case (literature on per curiam: **not found** in depth here).

#### Binding vote to person + audit without party-visible identity

Sources describe this pattern outside courts:

| Source | What it does |
|--------|----------------|
| **OpenMed blinded adjudication** | Reviewer packets show only `candidate-a`, `candidate-b`, etc.; a separate **`SealedIdentityMapping`** (HMAC commitment) binds each alias to a private reviewer identity and output digest; **authorized auditor** verifies mapping after adjudication; identity disclosure is a **separate authorized step** (OpenMed docs 2026). |
| **ElectionGuard** | Each ballot encrypted under a public key; voter can verify **their** ballot was recorded; guardians/quorum can decrypt for tally; published record supports **end-to-end verifiability** without revealing how others voted (Benaloh spec 2.1.0). |
| **SOBA (Benaloh 2011)** | Publishes contest-level cast vote records with **shrouded links** between ballot styles and votes so observers check outcomes **without** learning voter identity; commitments are **binding** and later **openable** for audit. |
| **BlindReview (eprint 2026)** | Cryptographic peer-review protocol: **anonymous** to authors and (in design) chair during review; **end-to-end verifiable** with proofs; chair can later challenge conflicts **after** identities revealed in a later phase. |
| **Zamir & Engel** | **Intermediate solutions**: identity known to some roles (editor, auditor) but not to affected parties; delayed revelation (Part III F, H, I). |

**not found:** an English scholarly or official source describing a **national civil court** that assigns a known judge to a case for administration but shows parties only an opaque role alias while storing a **cryptographically bound** vote trace for later pool aggregation — the pattern appears in **peer review, elections, and benchmark adjudication**, not in ordinary justice procedure literature consulted here.

#### Tension: transparency of judges vs candour

- Zamir & Engel note anonymity may reduce **effort and justification** (citing Tetlock on accountable mock jurors). Separate law-and-economics work on **publication rules** (e.g. GLEA 2021 paper on judicial candor) argues unrestricted attribution of opinions to named judges can make judges **less candid** when watched. That supports **confidentiality of reasoning or vote**, not necessarily **hiding assignment** from parties.

## Questions for Omid

1. **Independence mechanism (blocks adjudication task design):** Sources support **simultaneous voting** and **non-sequential exposure to colleagues' views** for expert panels (FDA), and **rapporteur-first drafting** in collegial courts — but not a court rule of sealed independent reports before any shared draft. Should the pilot require **simultaneous sealed votes**, **independent written opinions before deliberation**, or **only** bar sequential oral voting? No English source orders all three for courts.

2. **Public vs secret vote after pooling (blocks vote visibility):** FDA and Vermeule treat **attributable public votes** as accountability; Newham & Midjord treat **simultaneous** but still **public** votes as fixing herding. Zamir & Engel treat **secret ballot** as distinct from **anonymous decision-maker**. Should parties see **how many** judges voted each way without names, **named votes** after judgment, or **never** — and is judge **assignment** secret, or only **vote breakdown**?

3. **Rapporteur / draft-first (blocks workflow):** CJEU and ex ante supreme courts normalize **one draft that others sign**. Is the failure mode you care about **draft-first collegiality itself**, or only **signing without an independent preliminary vote/opinion**? Sources document the workflow; they do not label it a pathology.

4. **Anonymity scope (blocks party-facing identity):** Zamir & Engel and OpenMed separate **party-visible alias** from **auditor-held identity mapping**. Should parties see **no judge identity at all**, **a panel without names**, or **named judges but secret deliberation/votes**? **not found:** civil-court precedent for hiding the assigned judge from parties while keeping an auditable person-bound vote.

5. **Audit authority (blocks who can deanonymize):** OpenMed and ElectionGuard assign **verification** to auditors/guardians, not to parties. Who in the pilot may **open the binding** between vote and user — internal audit only, parties on appeal, or public after final judgment? Sources do not answer for courts.

6. **Role + case→user edge (blocks graph shape):** Literature describes **roles** (rapporteur, member) and **assignment** separately from **party-visible identity**. You want a **role** plus a **case→user** edge while parties see neither. Should the party-visible layer show only **"the court"** / **panel seat ID**, with user resolution restricted to **task-assignment and audit paths**? No source prescribes that graph; confirm intended visibility rules.
