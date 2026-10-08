# Case Research 002 — Multiple claims in a petition (Iran and Germany)

## Table of Contents

- [Status](#status)
- [Question and goal](#question-and-goal)
- [Participants](#participants)
- [Method](#method)
- [Findings](#findings)
  - [Iran — civil procedure](#iran--civil-procedure)
  - [Germany — civil procedure (Klagehäufung / Teilurteil)](#germany--civil-procedure-klagehäufung--teilurteil)
  - [Cross-cutting notes for phase 0](#cross-cutting-notes-for-phase-0)
- [Questions for Omid](#questions-for-omid)

## Status

Complete

## Question and goal

**Questions**

1. How are petitions (dadkhast) with multiple claims structured and ruled on under Iranian civil procedure? — Answered (with statutory gaps marked)
2. How does a comparable civil-law system (Germany: Klagehäufung / Teilurteil) handle the same points? — Answered
3. For each system: how is each claim individuated; how are parties and their role per claim stated; must a ruling address each claim and what happens when one is skipped; how may parties/claims be amended after filing; how is pre-filing completeness enforced? — Answered per topic below

**Goals**

- Provide inspectable, English-language comparative description (not a model) to inform `case.research.001` and the pilot question on separate structured rulings per claim.
- Record Omid's premises separately from sourced findings.
- End with precise blocking questions for Omid.

**Scope**

- Iran: Omid's premises plus English scholarly or official English translations of statute; Persian web sources excluded.
- Germany: primary (official English ZPO translation) plus one English scholarly comparative source; France not needed (German sources sufficient).
- Read-only context from `organization` (`modules/rights/case`, `bundles/justice`) noted but not edited.
- No modeling, no code, no PR.

## Participants

| Participant | Role | Review |
|---|---|---|
| Run 1 (Research A) agent `bc-83df6472-7c3a-5b8a-bf87-3bab8090c8bd` | Researcher | Not yet reviewed |

## Method

Single-pass desk research, 2026-09-26.

1. Loaded phase-0 brief: `docs/development-plan.md`, `docs/project-context.md`.
2. Loaded Memar Research facet structure from `memar/docs/documentation-research.md` (core sections only).
3. Read-only scan of `organization/modules/rights/case` and `bundles/justice` for existing role vocabulary and pilot defects (petition as ordered edge; role ambiguity across claims).
4. Sources consulted (inspectable URLs only):
   - **Iran statute (English translation):** [Civil Procedure Law of Iran](https://www.iranbestlawyer.com/wp-content/uploads/2024/11/Civil-Procedure-Law-of-Iran.pdf) — cited as *Iran CPC (Eng. trans.)*; article numbers checked against in-text headings (note: Article 298 text appears under an "Article 297" heading in this translation).
   - **Iran scholarship (English):** Fathi, "A Feasibility Study of Multiple Claims within a Single Petition in Iranian Civil and Administrative Proceedings" ([journal page](https://cpl.qom.ac.ir/article_4468.html?lang=en)); Hasanzadeh, "Issuing a Verdict on Part of a Civil Lawsuit" ([journal page](https://jplr.atu.ac.ir/article_20931.html?lang=en), [PDF](https://jplr.atu.ac.ir/article_20931_5b7436c89c739d4ebe618dc7c1e277f2.pdf)); Hatami & Taghipourian Gilani, "Regulations Governing Joinder of Plaintiffs in Civil Litigation" ([journal page](http://jlawst.ir/article-1-1067-en.html)).
   - **Germany statute (official English):** [Code of Civil Procedure (ZPO) — English](https://www.gesetze-im-internet.de/englisch_zpo/englisch_zpo.pdf) — cited as *ZPO (Eng.)*.
   - **Germany scholarship (English):** Hoegen, "Required Joinder of Claims" ([Michigan Law Review](https://repository.law.umich.edu/cgi/viewcontent.cgi?article=7212&context=mlr)).
5. Where a point is not supported by these sources: **not found** (no reconstruction from training data).

**Omid's premises** (from development plan / project context — not findings):

- A petition with several claims needs a **separate structured ruling per claim**.
- Courts sometimes **skip a claim** or issue one **blanket rejection** (bi-haqqi).
- The graph must show a skipped or silently merged claim and must state **each party's role on each claim**.
- Current petition shape lists persons without stating role per claim.

## Findings

### Iran — civil procedure

#### Default rule and joinder of multiple claims

- The **principle of independence of claims** is the default: ordinarily each claim is initiated by a **separate petition** and adjudicated independently (Fathi, abstract).
- **Joinder of claims** (cumul des demandes) in one petition is an exception when claims are **connected** (*lien de connexité* / sufficient connection) (Fathi).
- **Article 65, Iran CPC (Eng. trans.):** if **multiple unrelated claims** are filed in one petition and the court **cannot address them all in a single trial**, it **separates** the claims and addresses each individually; for claims outside jurisdiction it issues **non-jurisdiction** and refers onward.
- Fathi distinguishes two joinder situations:
  - **Legally connected claims:** the court is **obligated to hear all claims jointly**, even lacking territorial/relative jurisdiction in some cases.
  - **Unconnected claims but collectively competent:** joinder is **discretionary**; appellate courts may not review that discretion.
- In **administrative justice**, if joined claims lack sufficient connection the clerk notifies the claimant to separate; failure can lead to **dismissal/inadmissibility** — Fathi notes **silence of the civil code** on an equivalent administrative-style sanction for ordinary civil proceedings.
- **Article 141, Iran CPC (Eng. trans.):** two lawsuits are **"fully related"** when a decision in one **would affect** the other; counterclaims from the same source or closely related are heard **together** with the original case.
- **Article 103, Iran CPC (Eng. trans.):** other lawsuits **related to the pending case** in the same court are heard **together** (consolidation by court).

**Claim individuation in the petition**

- **Article 51, Iran CPC (Eng. trans.)** requires one petition form to state: parties; **subject and value** of the claim; **obligations and grounds**; **specific relief**; evidence; signature. If a party holds a procedural title (guardian, trustee, executor, company manager), that title **must be specified**.
- The statute **does not** require numbering or labeling each claim as a separate sub-unit when several are joined. Fathi traces joinder doctrine through Article 65 and related practice but does not supply a mandatory petition template for multi-claim enumeration.
- **Article 65** is framed as **separation** of unrelated joined claims, not as a positive joinder checklist.
- **English scholarly term for multiple claims in one petition:** Fathi uses **joinder of claims**; connection types discussed include **same origin**, **conditional** (*manvot*), and **complete connection** — full English exposition of Article 141's "complete connection" as the upper bound of **indivisibility of claims** (as distinct from indivisibility of a single claim): **not found** in the English sources consulted (Persian-only article on indivisibility of claims cited by Hasanzadeh was not used).

**Parties and role per claim**

- Petition identifies **petitioner** and **respondent(s)** with identity and residence (Article 51). **Multiple defendants:** extra copies per defendant (Article 60).
- Procedural titles (guardian, attorney, company manager, etc.) are stated **once in the petition** when applicable (Article 51 note; Article 59 for representative authority document).
- **Third-party entry** (Article 131 ff., Iran CPC Eng. trans.): third party must submit a petition stating **purpose** clearly; separate copy rules.
- Hatami & Taghipourian (2024): in Iranian law, **multiple individuals with similar or common issues cannot collectively sue a common defendant** as a general mechanism (contrast with U.S. joinder of parties). With **solidarity**, each may sue individually; without solidarity, **whether claims can be separated** determines individual suits and court entry. With **multiple defendants**, plaintiff may sue all or some depending on **joint liability** and separability.
- **Per-claim party-role matrix in the petition (e.g., person X is plaintiff on claim 1, defendant on claim 2):** **not found** in statute or English scholarship consulted.

**Ruling on each claim; skipped or blanket treatment**

- **Article 4, Iran CPC (Eng. trans.):** courts must issue **specific determinations** for each case and **not broad or general rulings**.
- **Article 296, Iran CPC (Eng. trans.):** written judgment must include parties, **subject and parties' requests**, reasoning, legal basis.
- **Partial ruling on a divisible matter:**
  - **Article 104:** at end of hearing, if lawsuit is **divisible** and a ruling can be issued on part, the court **may** do so and continue on the remainder.
  - **Article 298** (text at Iran CPC Eng. trans. p. corresponding to "If the case can be divided…"): upon **claimant's request**, if only part requires ruling, court **must** rule on that part and continue on the rest.
- Hasanzadeh (2026): Articles 104 and 298 overlap; Article 298 **obliges** ruling on concluded part of divisible claim; Article 104 is better read as **discretionary** except when petitioner requests; primary purpose is **division of a single claim**, though articles **may also apply to multiple claims**.
- **When court issues judgment on only part without explicit division** (oversight): statute is **silent** (Hasanzadeh). Scholarly proposal: treat like divisible case — court should be **obliged to rule on unaddressed part**; if **indivisible**, verdict should extend to unaddressed part and partial treatment is **appealable error**.
- **Omid's premise** (blanket bi-haqqi rejection or silent skip of one claim in a multi-claim petition): treated as **practice observation**; **no English scholarly source** using the term bi-haqqi or documenting blanket multi-claim rejection was found. Hasanzadeh's "unaddressed part" analysis is the closest English doctrinal hook.

**Amendment of parties and claims after filing**

- **Article 98, Iran CPC (Eng. trans.):** plaintiff may **reduce** demand anytime; **increasing** demand or **changing nature** of claim only if it relates to the **original lawsuit**, shares a **common cause**, and is declared **by end of first session**.
- Fathi notes plaintiff's power to join multiple claims is primarily **until petition filing**; Article 98 continues but **limits** post-filing change.
- **Adding parties / third parties after filing:** Articles 131–137 (third-party intervention and summoning); not a free amendment of the original petition structure.
- **Formal rule for amending one claim in a multi-claim petition without touching others:** **not found**.

**Pre-filing completeness**

- **Article 51** content requirements (subject, grounds, relief, evidence, parties).
- **Articles 53–56:** clerk accepts but **suspends** if fees/stamps missing or items 2–6 of Article 51 incomplete; **written deficiency notice**; **10 days** to cure; else **dismissal order** by clerk (appealable within 10 days).
- **Article 56:** missing petitioner name/residence → dismissal within two days.
- **Article 64:** court reviews file; if complete, sets hearing (minimum 5 days after notification; 2 months if abroad).
- **Article 66:** if petition still incomplete for court to proceed, deficiencies listed; **10 days** to cure; else **dismissal**.

---

### Germany — civil procedure (Klagehäufung / Teilurteil)

#### Klagehäufung (consolidation / joinder of claims)

- **§ 260 ZPO (Eng.):** several claims of the plaintiff against **one and the same defendant** may be consolidated in **one action**, even on different grounds, if the court is **competent for all** and the claims may be dealt with in the **same type of proceedings** (Verfahrensart).
- Hoegen (1957): this is **permissive joinder** — "free joinder" within ordinary proceedings, subject to jurisdictional and procedure-type limits; aggregate amount may determine jurisdiction when value-based.
- **§ 145 ZPO (Eng.):** court **may separate** several claims in one complaint into **separate proceedings** if factually justified (court order with reasons).
- **§ 147 ZPO (Eng.):** consolidation of **pending** proceedings with legal ties or that **could have been asserted in one complaint**.

**Claim individuation in the statement of claim**

- **§ 253(2) ZPO (Eng.):** statement of claim must include party and court designation; **exact information on subject matter and grounds** of the claim; **precisely specified petition** (prayer for relief).
- Hoegen: the **complaint** must state grounds and prayer; **cause of action** and **res judicata** scope are individualized per claim in German theory.
- **Objective Klagehäufung:** multiple **Streitgegenstände** (dispute objects) side by side — each corresponds to a separable procedural claim with its own prayer/facts (described in German doctrinal summaries; English exposition in Hoegen § I).
- **§ 253(2) does not** explicitly require a numbered claim schedule, but **each joined claim must be identifiable** through distinct subject/ground/petition elements.

**Parties and role per claim**

- **§ 253(2) no. 1 ZPO (Eng.):** designation of **parties**.
- **§§ 59–62 ZPO (Eng.):**
  - **§ 59:** joint plaintiffs/defendants if **community of interest** in the right or **same factual and legal cause**.
  - **§ 60:** similar claims/obligations, essentially similar cause.
  - **§ 61:** joined parties generally litigate as **individuals** unless civil law provides otherwise.
  - **§ 62:** **necessary joinder** where legal relationship must be established **uniformly** toward all joined parties.
- **Subjective Klagehäufung** (several defendants for several claims): requires **§ 260** plus **§§ 59 ff.** (Hoegen; German doctrinal practice — English detail in Hoegen).
- **Per-claim role assignment in the complaint** (same person as plaintiff on claim A, defendant on claim B): **not found** as an explicit ZPO requirement in sources consulted.

**Ruling on each claim; Teilurteil; skipped claims**

- **§ 301 ZPO (Eng.):**
  - If only **one of several claims** in an action is ready for final decision, or only **part of a claim**, court delivers **final judgment (partial judgment / Teilurteil)**.
  - For a **single unified claim** disputed on **merits and amount**, partial judgment on amount only if concurrently **§ 304 interlocutory judgment on merits** of the remainder.
  - Court **may forgo** partial judgment if **unreasonable** under circumstances (§ 301(2)).
- Hoegen: German joinder does not foreground "splitting" doctrine like U.S. required joinder; **res judicata** still attaches per claim/cause.
- **Obligation to decide every joined claim before closing the action:** **not found** as an absolute rule; mechanism is **partial judgment** when decision-ready, else continuation. Risk of **contradictory decisions** across partial judgments is a known doctrinal concern (German commentary cited in search summaries; English primary text: § 301 only).
- **Silent failure to rule on one joined claim:** **not found** as a labeled ZPO category; would fall under general judgment requirements (**§ 313** form/content) and appellate law — specific English source on "skipped claim in Klagehäufung": **not found**.

**Amendment of parties and claims after filing**

- **§ 263 ZPO (Eng.):** after dispute is pending, modification of complaint allowed if **defendant consents** or court finds it **expedient**.
- **§ 264 ZPO (Eng.):** **not** a modification if: factual/legal corrections only; extension/limitation of relief **without changing cause of action**; different object claimed due to **later changes** (listed cases).
- **§ 261(2) ZPO (Eng.):** claim lodged **only during proceedings** becomes pending when served in hearing or by conforming written pleading.
- **§ 265 ZPO (Eng.):** disposition/assignment of disputed object does not end proceedings; successor rules limited.
- **Party substitution / Klageänderung changing defendants per claim:** governed by § 263 framework; detailed per-claim amendment taxonomy in English: **not found** beyond general rules.

**Pre-filing completeness**

- **§ 253 ZPO (Eng.):** mandatory content for statement of claim (parties, court, subject, grounds, petition); copies for service unless electronic filing.
- **§ 280 ZPO (Eng.):** separate hearing on **admissibility** of action (referenced in ZPO structure).
- **§ 296 ZPO (Eng.):** refusal to accept **late** submissions — post-filing completeness enforced in proceedings, not only at filing.
- **Specific ZPO article requiring court to reject complaint before service for incomplete § 253:** English text lists admissibility hearing (§ 280) but a single pre-service dismissal analogue to Iran's Articles 53–56: **not found** in detail in sources consulted (may exist in German practice via § 277/296 — mark **not found** for strict equivalence).

---

### Cross-cutting notes for phase 0

| Topic | Iran (sourced) | Germany (sourced) |
|---|---|---|
| Join several claims in one filing | Exception; Art. 65 separates unrelated; Fathi on connected vs discretionary joinder | Rule; § 260 if competence + same procedure type |
| Individuate claims in filing | Art. 51 elements per case; no numbered multi-claim schema found | § 253(2) per claim subject/ground/petition |
| Party role per claim | Party titles in petition; no per-claim role matrix found | Party designation; joinder rules §§ 59–62; no per-claim role matrix found |
| Partial / per-claim ruling | Arts. 104, 298; Art. 4 specific determinations; Hasanzadeh on gaps | § 301 Teilurteil; § 304 for merit splits |
| Skipped claim | Statutory silence on oversight; Omid premise on practice | not found (English) |
| Post-filing amendment | Art. 98 (limited); third-party arts. 131+ | §§ 263–264 |
| Pre-filing completeness | Arts. 51–56, 64–66 with time-bound cure/dismissal | § 253; late-stage § 296; strict parallel not found |

**Organization read-only context:** `case` module lists justice role labels (Plaintiff, Defendant, Judge, etc.) in `case-relation-user.go` but does not bind them to individual claims. `bundles/justice` approves/declines claim types without per-claim ruling structure — product requirement, not Iranian/German law.

## Questions for Omid

1. **Skipped / bi-haqqi ruling (blocks `case` ruling edge shape):** When a court rejects all claims with one formula (bi-haqqi) or addresses only some claims in a multi-claim petition, should the model record that as (a) one ruling node with an explicit "unaddressed claim" flag per claim, (b) separate ruling nodes only for claims actually ruled on, or (c) a single merged outcome with appeal-stage correction? No English source defines bi-haqqi; your practice premise is the only input.

2. **Per-claim party role (blocks petition–party edges):** Iranian Article 51 and German § 253 require party identification and (for Iran) procedural titles, but neither requires stating each person's role **per claim**. Should the organization model **require** per-claim role on the petition anyway (normative design), or only record roles that the statute/parties actually supply?

3. **Claim individuation in dadkhast (blocks petition internal structure):** Should multiple claims in one petition be modeled as (a) separate `case` nodes linked to one petition edge, (b) ordered sub-requests inside one petition node, or (c) another shape? Statute requires grounds and relief but not numbered claim slots; your current "ordered edge among case nodes" is the baseline to attack.

4. **Indivisibility vs separability (blocks partial-ruling rules):** For Iran, Hasanzadeh ties partial rulings to divisible lawsuits; Fathi ties joinder to "connection." Which test should govern when the model allows a partial ruling on one of several joined claims — **divisibility of the lawsuit**, **complete connection** (Article 141), or your operational rule from practice?

5. **Amendment after first session (blocks claim lifecycle):** Iran Article 98 cuts off increase/change of nature after the **first session** unless tied to original cause. Should an amended claim be a **new case node**, a **revision of the same case**, or a **petition amendment event** on the existing graph? Statute does not answer graph shape.
