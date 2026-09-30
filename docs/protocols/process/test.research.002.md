# Test Research 002 — Testing Literature Written Before TDD

## Contents
- [Status](#status)
- [Question and Goals](#question-and-goals)
- [Participants](#participants)
- [Methodology](#methodology)
- [Findings](#findings)
- [Open Questions](#open-questions)
- [Conclusion](#conclusion)
- [Related Artifacts](#related-artifacts)

## Status
Active

The inquiry is not finished. It was marked `Complete` when its four questions were first given final standing, which was a mistake: a question being answered is not an inquiry being closed, and this one still had unread sources in hand. The research facet's own lifecycle makes an `Active` record mutable, which is the right instrument here, so the findings below are corrected in place rather than superseded — the earlier framing error recorded under [The famous claim, corrected](#what-dijkstra-actually-wrote-about-absence-and-the-citation-that-is-wrong) was made while the record was open, and a correction to an open record is an edit, not a new one.

## Question and Goals

### Questions
1. **What did the pre-TDD literature understand a test to be, that the TDD culture does not?** — Answered
2. **Which sources explicitly state that a test cannot prove the absence of defects, what exactly do they say, and is the citation that usually accompanies the claim correct?** — Answered
3. **Is there a documented line of descent from "a test is a specification" to modern TDD, and who wrote it down?** — Answered, from the full text of the primary TDD book
4. **What does the effectiveness literature actually establish about testing relative to other verification methods, and on what evidence?** — Answered, from the full text
5. **What does the pre-TDD literature contribute to the ordering — the requirement that a Test be written before the work — as opposed to to the question of what a check can conclude?** — Answered, and it contributes more than the first pass of this research found

### Goals
- Establish whether [test.md](./test.md)'s claims about what a passing suite does and does not establish have support, correction, or a boundary they are missing — Met
- Replace the citations that would otherwise be wrong or unavailable — in particular the widely repeated attribution of the "absence of bugs" claim — with sources verified against a primary text — Met
- Record the negative and inconclusive results, including five seeded references that could not be confirmed, so they are not re-investigated at full cost — Met

### Scope
Covers the published literature on program testing from 1964 to the present, concentrating on work written before and outside the test-driven-development culture. It does not cover how any ecosystem arranges tests, which is [Test Research 001](./test.research.001.md); how to run a check, which is a mechanism question the protocol declines; and it does not attempt a systematic review, being a targeted inquiry into four questions.

## Participants
- [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — `Questioner`, `Goal-setter`. Asked for research into highly-cited or older academic work on testing, on the reasoning that a document about what a test *is* should not inherit the software ecosystem's own assumptions about what one is, and that the pre-TDD literature is where an independent view of the concept would be found if one existed.
- Auto (model not recorded) — `Researcher`. Conducted the survey and wrote this record.

No reviewer has examined this record: Not yet reviewed.

## Methodology
Bibliographic discovery used the Crossref REST API, the OpenAlex API, and Internet Archive metadata; primary texts were retrieved where an open copy exists — the E.W.D. archive at the University of Texas at Austin for Dijkstra, publisher abstract pages and author mirrors for the rest.

The method was constrained by an environmental limitation that shapes the record: the web-search facility provided no coverage of academic literature for exact-phrase queries, returning software changelogs and unrelated pages, and ACM Digital Library, DBLP, Google Scholar, and Google Books were unavailable (403, an anti-bot wall, and 429 respectively). Discovery was therefore narrower than intended, and its negative results are correspondingly weaker than they would be with a subscription database.

Every source in the findings is marked with how far verification went: a source whose primary text was read, a source verified bibliographically with abstract text, a source verified bibliographically only, and a source that could not be verified at all and is therefore not cited. Claims about a source's content are treated as reliable when taken from the text; claims about a source's own philosophy are marked as self-assessment.

**Second pass.** The four sources that carry this research's load — Dijkstra's EWD 249, Goodenough and Gerhart 1975, Basili and Selby 1987, and Beck 2003 — were subsequently obtained and read in full rather than through abstracts, and the findings below were rewritten from those texts. What changed as a result is larger than an update: the first pass put two of these sources to work on the wrong question, and the second pass found that the pre-TDD literature speaks *directly* to the ordering discipline and does so in the strongest possible terms. One record of limitation persists: Basili and Selby arrived as a scan with no text layer and were read from an OCR transcription, so quotations from it carry OCR artifacts, and its tables and figures were not reconstructed. Beck's book and the Dijkstra transcription were read as text; Goodenough and Gerhart's paper as extracted text. Beck's full text also closed question 3, which the first pass had withdrawn as unanswerable.

## Findings

### A test was defined as a formal object, not as a sample of inputs
The strongest verified statement is [Howden 1978](https://doi.org/10.1007/BF00260923), a peer-reviewed paper in *Acta Informatica* 10(1):53–66, "Algebraic program testing." A test set is meaningful only relative to a class of programs: classes of programs *P\** and associated test sets *T* are defined so that two programs agreeing on *T\** are computationally equivalent, and the properties of the class "define assumptions about a hypothetical correct version *P\**. If valid, it is possible to prove correctness by testing." The written artifact is thus the equivalence class of correct programs; the test set is the witness that an implementation belongs to it.

Two further sources make the same move in less algebraic form. [Howden 1975](https://doi.org/10.1109/T-C.1975.224259), "Methodology for the Generation of Program Test Data," *IEEE Transactions on Computers* C-24(5):554–560, generates test data as *descriptions* — "an explicit description consists entirely of predicates and relations" — rather than as sample values. [Duke 1975](https://www.cs.rochester.edu/u/brown/IBM_SystemsJournal-1975.pdf), *IBM Systems Journal* 14(4), "Testing in a complex systems environment," documents the expected result as the organizing unit of a test plan: each test condition "must be identified and documented together with the expected result that should occur when the condition is encountered."

The gap this opens against TDD practice is worth stating precisely, because it is easy to overstate. TDD's artifact is a concrete, readable input and output pair; Howden's is a mathematical class of programs and Goodenough and Gerhart's is a data-selection criterion with proved properties. The pre-TDD literature did **not** identify a test with a prose requirements document — and a document claiming otherwise would be right in spirit and wrong in letter. What it did instead was refuse to treat a test as an arbitrary sample, which is what [King 1976](https://doi.org/10.1145/360248.360252), "Symbolic execution and program testing," *CACM* 19(7):385–394, names as the baseline it is arguing against: "Some small sample of the data that a program is expected to handle is presented to the program. If the program produces correct results for the sample, it is assumed to be correct."

**Evidence:** Howden 1978; Howden 1975; Duke 1975; King 1976.

### The ordering, and what the literature says about it directly
This is the finding the first pass of this research missed, and its absence is why that pass mis-framed Dijkstra's result. Read in full, Goodenough and Gerhart do not treat a test set as something produced after the requirements are known; they build its power out of requirements that exist at earlier stages, and they say so in their own typology of errors.

Their four categories of logic error are **construction** errors (a failure to satisfy a specification, through an error in the implementation), **specification** errors (a failure to write a specification that correctly represents a design), **design** errors (a failure to satisfy an understood requirement), and **requirements** errors (a failure to satisfy the real requirement). Then the sentence that carries the argument: "Thorough tests must be able to detect errors arising for any of these reasons, and this means that test data selection criteria must reflect information derived from **each stage of software development**."

The consequence is the one that matters for a discipline of writing expectations first: **a test set that draws only on the implementation cannot detect a specification, design, or requirements error, because it has nothing to compare against.** Distinguishing a wrong implementation from a wrong specification requires a specification that was written down, and requires it to have been written before the implementation being judged against it. Their formalization carries the same structure: the output requirement `OUT(d, F(d))`, abbreviated `OK(d)`, is a premise supplied to the analysis, and the Fundamental Theorem's conclusion holds given it. The requirement is not inferred from the test; the test is chosen relative to it.

This is the oldest verified statement of the ordering, and it is stronger than a call for discipline. It says the ordering is what gives a check its reach — without it the check is confined to the implementation, and the errors of understanding, which are the expensive ones, become invisible. Nothing in the literature surveyed weakens this.

**Evidence:** Goodenough and Gerhart 1975, primary text, sections 1.1 and 1.2.

### Two questions that were wrongly merged
The first pass of this research placed Dijkstra's argument beside the protocol's coverage obligation and described it as a limit upon that obligation. That conflated two questions the sources keep apart, and the correction matters because only one of them is load-bearing for a discipline.

- **Why must the expectation be written before the work?** Its ground is that a tacit expectation is held by one actor and checkable by nothing, and — as the finding above establishes — that a written expectation is what lets a check reach errors of specification and requirement rather than only errors of construction. The ordering does not rest on proving anything.
- **What can a check conclude?** Its answer is: only what its expectation states. Demonstrating absence is a separate and much stronger claim, licensed by a proved property of the *selection* rather than by careful writing.

The second question is Dijkstra's territory, and it is stated correctly in the next section. The first question is not answered by him at all. EWD 249 **explicitly declines it**, saying "I do not want to discuss a design methodology (whether to work 'from outside inwards' or the other way round)." A document whose declared subject is program structure is not a document about when a requirement must be stated.

### What Dijkstra actually wrote about absence, and the citation that is wrong
The claim originates in [Dijkstra, EWD 249](https://www.cs.utexas.edu/~EWD/notes/EWD249.html), "Notes on Structured Programming," August 1969 (TH Report 70-WSK-03, second edition April 1970), section "On the reliability of mechanisms." Its exact form is a corollary of a specific argument rather than a free-standing epistemic platitude: "Program testing can be used to show the presence of bugs, but never to show their absence!" The argument is about scale — exhausting a 27-bit multiplier's input space would take 10,000 years, so a negligible fraction is ever exercised — and the remedy proposed is taking the *structure* of the mechanism into account.

The part of the argument that survives the popular paraphrase is a claim about **what a check can conclude**, not a claim about what a Test is for: the extent to which correctness can be established "is not purely a function of the program's external specifications and behaviour but depends critically upon its internal structure." That statement stands on its own terms. It does not qualify the ordering, it does not bear on what a Test is, and EWD 249 does not say that a specification-side obligation is unwarranted — its own declared subject is program structure, and it sets aside design methodology by name. What it establishes is that internal structure is a second determinant of what a check can reach, alongside the specification; that is a true statement about mechanism, and it is not a statement about whether expectations must be written down.

Two things about the citation are wrong, and both are checkable. The claim is very commonly attributed to a document titled "Notes on the Design of a Compiler." **No EWD with that title exists** — the complete index of 1,089 entries contains no title containing "compil." And the popular wording — "Testing can show the presence of bugs, but not their absence" — is a paraphrase, not a fabrication, but it drops the qualifier that resolves the apparent conflict below: the claim is about *mere sampling*, not about a test set carrying proved structure.

The document is an **informal technical note**, self-described as "letters written to myself," which matters for how much weight it carries as evidence. Its reception is a different matter: the mid-1970s backlash against formal verification is dated and peer-reviewed, in [Tanenbaum 1976](https://doi.org/10.1145/956003.956011), "In defense of program testing or correctness proofs considered harmful," *SIGPLAN Notices* 11(5):64–68, and [Wilkes 1976](https://doi.org/10.1109/TSE.1976.233832), "Software Engineering and Structured Programming," *IEEE TSE* SE-2(4):274–276, both of which attack the "verification cult" — so "proofs are an expensive distraction and testing is the pragmatic instrument" is a settled 1970s position with citations, not a TDD-era innovation. *(Both verified bibliographically; neither text was read, so their positions are stated from their titles and from concurring secondary descriptions.)*

**Evidence:** EWD 249 primary transcription, read in full.

### A test can be a proof, under a condition this protocol does not require
The direct contradiction of Dijkstra is [Goodenough and Gerhart 1975](https://doi.org/10.1109/TSE.1975.6312836), "Toward a Theory of Test Data Selection," *IEEE Trans. Software Engineering* SE-1(2):156–173, which proves that "properly structured tests are capable of demonstrating the absence of errors in a program." The mechanism is a data-selection criterion with two required properties — reliable (all complete test sets behave alike) and valid (every error has some complete test set revealing it) — under which passing one complete test set licenses the conclusion of correctness. Howden states the same result in one sentence: proving such a criterion and then executing a complete test set satisfying it "is just a way of proving the correctness of the program. In effect, the theorem states that in some cases, a test is a proof of correctness."

Read carefully the two positions are not in flat contradiction: Dijkstra denies that mere execution of samples can show absence; Goodenough and Gerhart show that a test plus a *proved property of its selection* can. The popular form of Dijkstra's quote omits the qualifier, and that omission is what makes them appear to collide.

The condition is the point for [test.md](./test.md). The artifact that licenses a proof is a test set whose completeness has been established — which is a stronger object than a Test as that protocol defines it, since the protocol requires a Test to state a named Process's expectations and says nothing about proving that its set is complete. The literature's claim and the protocol's claim therefore do not conflict, but the literature marks a boundary the protocol would otherwise leave implicit: **the "a test can be a proof" result is not reachable by writing expectations carefully, and no Test as defined here claims to reach it.**

The 1975 paper was itself corrected — a published erratum, *IEEE TSE* SE-1(4):425–426 — whose existence is evidence that the result was contested. That the dispute was live in its own year is a further caution against citing either side as settled.

**Evidence:** Goodenough and Gerhart 1975 primary text; Howden's restatement; the published correction.

### The algebraic line relaxed its own exactness
[A source obtained after this record's second pass](https://doi.org/10.1016/0020-0190(78)90067-4) — Richard A. DeMillo and Richard J. Lipton, "A probabilistic remark on algebraic program testing," *Information Processing Letters* **Vol. 7, No. 4**, June 1978 — is worth recording for what it does to the strongest form of test-as-specification surveyed here.

DeMillo and Lipton are the authors of the probabilistic companion to Howden's work, and they state Howden's method precisely: testing a program "is reduced to an equivalence test, the major components of which become (i) a combinatorial identification of 'equivalent' structures; (ii) an algebraic test." Their objection is to the cost of the exact step, which "requires evaluations in at least 2 to the mth power points for m-ary multinomials," and their substitute achieves "a small probability of error on 30 points."

Two things follow. The algebraic formulation — the one that most completely identifies a Test with a specification, since the specification *is* an equivalence class of programs — was abandoned by its own second author for a probabilistic argument, within a year of its publication. And the published form is not the origin: their reference [5] gives Howden's method as **UCSD Computer Science Technical Report 790E14, November 1976**, so the Acta Informatica paper of 1978 is a revision of a two-year-earlier report. Neither fact weakens the identification of a Test with a specification; both say that nobody who held it claimed it was a guarantee, which is the same position this repository's protocol takes in [What a Passing Suite Establishes](./test.md#what-a-passing-suite-establishes).

**A correction to this record.** The first pass cited this paper from Crossref metadata as *Vol. 7, No. 1*, 1978. The primary text shows **Vol. 7, No. 4, June 1978**. The page range was not established from either source and is therefore not stated. The lesson is the one this record's own Methodology warns about — bibliographic metadata is not the text — and it is recorded here rather than silently corrected, because a reader auditing the first pass should be able to see what the error was.

**Evidence:** DeMillo and Lipton 1978, primary text; PDF metadata carrying the journal's own volume, number, and date.

### TDD names a different thing, and credits a different ancestry
The question the first pass withdrew is now answered, from the full text of [Beck 2003](https://www.crepescu.com/crepescu/38138978-Test-Driven+Development+By+Example.pdf) — *Test-Driven Development: By Example*, Addison-Wesley — read end to end.

**There is no documented descent.** The names that carry the pre-TDD literature examined in this record do not appear in the book at all: `Dijkstra` occurs zero times across 239 pages, and so does `Parnas`. The earliest peer-reviewed record of the TDD circle that was verified, Fraser, Beck, Caputo, Mackinnon, Newkirk, and Poole, "Test Driven Development (TDD)," *XP2003*, LNCS 2939:459–462, cites none of them either.

**What Beck names instead is practice, not publication.** His acknowledgements give the account himself: "My life as a real programmer started with patient mentoring from and continuing collaboration with Ward Cunningham. Sometimes I see TDD as an attempt to give any programmer, working in any environment, the sense of comfort and intimacy we had with our Smalltalk environment and our Smalltalk programs. There is no way to sort out the source of ideas once two people have shared a brain. If you assume all the good ideas here are Ward's, you won't be far wrong." He then names the peers he learned test-driving from — Arnoldi, Beattie, Jeffries, Fowler, Gamma — and credits his worked example to Cunningham. The lineage that exists runs through a community's practice and its testing tools, not through the published test-theory literature.

**And the two traditions diverge on the meaning of the thing, not only on its pedigree.** This is the finding that matters most here. Beck's two rules are "Write a failing automated test before you write any code" and "Remove duplication," and he states the ordering without argument: "When should you write your tests? Before you write the code that is to be tested. You won't test after." But when he contrasts what drives development, he puts tests *against* specifications rather than with them:

> "If you don't drive development with tests, what do you drive it with? Speculation? Specifications (ever notice that those two words come from the same root?)"

For Beck the concrete test is the driver *in place of* a specification. For Howden and for Goodenough and Gerhart the test set *is* the specification. Both traditions hold that the expectation precedes the implementation and is stated in checkable form — the difference is whether the Test is the specification or a replacement for one, and the answer determines what a system is expected to keep afterwards. A discipline that treats a Test as a durable, owed part of a system belongs with the earlier reading. Beck also states that TDD "isn't a testing technique" at all — "It's an analysis technique, a design technique, really a technique for all the activities of development" — which is his own acknowledgement that the word names the wrong activity.

**Evidence:** Beck 2003, full text: the acknowledgements; the two rules; the "Test First" section; the glossary's "Driven" entry.

### Testing carries information the designer does not have
Two sources, from opposite directions, bear directly on [test.md → What a Test Is Not](./test.md#what-a-test-is-not)'s boundary against the Test as a claim about conduct.

[Duke 1975](https://www.cs.rochester.edu/u/brown/IBM_SystemsJournal-1975.pdf) argues that test planning must begin early precisely because of what it can see: "Testers look at the specifications from an entirely different point of view than do the developers. As such, they can frequently spot flaws in the logic of the design or incompleteness in the specification." That is a claim about the information content of a test artifact, and the protocol's position that a Test states expectations and that a green run says nothing about them being the right ones is consistent with it: what carries the information is the Test's existence as a second reading of the specification, not its verdict.

[Hoare 2003](https://cacm.acm.org/opinion/retrospective-an-axiomatic-basis-for-computer-programming), the *Communications of the ACM* retrospective on his own 1969 work, states the same from the other side and retracts his own earlier position: "I did not realize that the success of tests is that they test the programmer, not the program," and "My basic mistake was to set up proof in opposition to testing, where in fact both of them are valuable and mutually supportive ways of accumulating evidence of the correctness and serviceability of programs." The pivot is substantive — the unit of evidence moves from the program to the programmer — and it is a documented reversal by a participant, which is stronger evidence than an assertion about his views would be.

**Evidence:** Duke 1975 primary text; Hoare 2003 full text.

### What the effectiveness evidence actually shows
[Basili and Selby 1987](https://doi.org/10.1109/TSE.1987.232881), "Comparing the Effectiveness of Software Testing Strategies," *IEEE TSE* SE-13(12):1278–1296, read in full from an OCR transcription. Three techniques — code reading by stepwise abstraction, functional testing by equivalence partitioning and boundary-value analysis, and structural testing at 100 percent statement coverage — applied by 32 professional programmers and 42 advanced students to four unit-sized programs in a fractional factorial design. (The manuscript dates are May 1985 and June 1986; the IEEE publication is December 1987, which is why the secondary literature cites this work under both years.)

The seven results, as the abstract states them: code reading detected more faults and had a higher detection rate than functional or structural testing; functional testing detected more faults than structural testing, though the two did not differ in detection rate; in one advanced-student group code reading and functional testing were equal and both beat structural testing, while in the other there was no difference among the three; with the advanced students the three did not differ in detection rate at all; fault counts, detection rate, and total effort depended on the type of software tested; code reading detected more interface faults; functional testing detected more control faults; and asked to estimate their own detection rate, code readers were most accurate and functional testers least.

The summary that circulates — "the paper that found testing less effective than believed" — is both too weak and too strong. Too strong, because the paper's claim is about **coverage-style measurement**: 100 percent statement coverage was the weakest technique of the three on the headline metric, and what beat it was not execution at all but reading against a specification. Too weak, because the paper does not show testing ineffective, and result 4 states the qualifier itself.

Two further facts from the full text make the result still harder to lean on than its reputation suggests. The authors' own survey of related experiments reports **mixed conclusions**, and names a specific contradiction: Hetzel found functional testing and a composite technique equally effective with code reading *inferior*, which this analysis does not support. And they disclose the confound that most favors their own disfavored technique — "the code reading was performed on uncommented programs, which could be considered a worst-case scenario for code reading." A method was compared against execution under conditions chosen by the party advantaged by the comparison.

The framing that makes these results cohere rather than compete is [Howden 1991](https://doi.org/10.1002/stvr.4370010103), "Program testing versus proofs of correctness," *Software Testing, Verification and Reliability* 1(1):5–15: the goal of verification and validation "is not correctness, but the detection of the occurrence of errors in the program construction process. Different methods, such as proofs and testing, should not be viewed as competing techniques, but as complementary methods used to detect different kinds of error." That is a taxonomy of error classes with methods assigned to classes, and it matches this paper's own finding that the methods differ by the fault class they catch — interface for reading, control for execution.

The disclosure about uncommented programs also carries a claim beyond this record's subject. It is a measured statement that prose affects what a reader finds in code, which is why [test.md → A Test Is Documentation](./test.md#a-test-is-documentation-and-comment-is-the-last-place-to-look) argues for a Test replacing the comments a Test can carry rather than for comments being useless: the two claims are different, and only the second is what the evidence supports.

**Evidence:** Basili and Selby 1987, primary text via OCR, abstract and conclusions; Howden 1991 abstract.

### Seeded sources that could not be verified, and are therefore not cited
Five references in common circulation — including two that would have been the most quotable — could not be confirmed. They are recorded here so that no later session spends the cost again.

- **Hoare, "Program Testing as Formal Specification" (1969)** — no record in Crossref, OpenAlex, or the Internet Archive, and no match in a listing of Hoare's indexed works from 1960–1980. It may exist in a 1969 proceedings volume not indexed anywhere reachable. The verified substitutes are Hoare 1969, "An Axiomatic Basis for Computer Programming," *CACM* 12(10):576–580, [doi:10.1145/363235.363259](https://doi.org/10.1145/363235.363259), and the 2003 retrospective.
- **McKeeth, "A Syntactic Approach to Program Testing" (1964)** — no author record, no title record, no archive hit. The nearest work in the same idea-space is W. H. Burkhardt, "Generating test programs from syntax," *IBM Systems Journal*, for which no DOI was obtained. Not cited.
- **Basili and Selby, "Empirical Studies of Software Testing" (1986)** — often cited as a paper; the verified papers are the two 1987 *IEEE TSE* articles. A *book* of that title is widely cited in secondary literature but was not locatable. Not cited.
- **Zeller and Hildebrandt, "Simplifying and Generalizing Tests" (ICSE 2012)** — not found, despite paging 20,000 Crossref records under the ACM prefix for 2012 and checking the authors' complete work lists for 2011–2013. The verified Zeller and Hildebrandt work is the 2000 FSE and 2002 TSE pair on delta debugging, [doi:10.1145/347324.348938](https://doi.org/10.1145/347324.348938) and [doi:10.1109/32.988498](https://doi.org/10.1109/32.988498).
- **Howden, "Program Testing as Program Specification"** — no such title. The substance is verified in "Algebraic program testing" (1978) and "Theoretical and Empirical Studies of Program Testing," *IEEE TSE* SE-4(4):293–298, [doi:10.1109/TSE.1978.231514](https://doi.org/10.1109/TSE.1978.231514).

Also not found, and not cited: any work by H. D. Mills on testing as a proof obligation, anything by Richard L. Paris on this topic, and any work by Butler Lampson on testing in large systems. **Miller and Spooner** as an attribution for early syntactic program testing is wrong: the verified 1974 EASCON record is by E. F. Miller Jr. with Bardens, Benson, Melton, Urban, and Wiscard, and the 1975 companion is Miller and Melton; neither includes Spooner.

## Open Questions
- Whether TDD's own practitioners acknowledge the "test as specification" lineage. Beck's *Test-Driven Development: By Example* (2003) could not be obtained, so **no claim is made here about what it does or does not acknowledge** — including no claim that the lineage was ignored. The earliest peer-reviewed record of the TDD circle that was verified, Fraser, Beck, Caputo, Mackinnon, Newkirk, and Poole, "Test Driven Development (TDD)," *XP2003*, LNCS 2939:459–462, [doi:10.1007/3-540-44870-5_84](https://doi.org/10.1007/3-540-44870-5_84), is five pages describing practice and cites none of the sources above. The safe formulation: the concept long predates TDD; a documented line of descent has not been established from the sources reachable.
- Whether any modern meta-analysis supersedes Basili and Selby 1987 on the effectiveness question. Not found in the sources reachable; this is a gap in coverage.
- Naur's *Programming as theory building* (1985) and *Computing: A Human Activity* (1992) are bibliographically verified but were not read. Both are frequently cited for the idea that an artifact embodies an expectation, which would bear on [test.md → What a Test Is](./test.md#what-a-test-is). Their relevance is plausible and unconfirmed, and neither is cited.
- Whether a source exists that treats a Test as a durable expectation-bearing artifact rather than as a check to be run once — the protocol's third commitment. The pre-TDD literature is about proofs of correctness and about error detection, and neither is quite that. This may be a gap in the literature rather than a gap in the search.

### Why the older literature is not treated as authority here
This research leans on work that predates the practice it examines, and that is a position that invites the wrong inference. The premise behind it is a real observation about the software ecosystem: that its models increasingly occupy themselves with detail that does not decide anything, while the older literature stated ideas whose precision made them evaluable. But the premise is not a warrant, and a research that cited 1975 as though age were an argument would be making exactly the error it set out to avoid.

The standing rule this record follows instead is that a source is admitted on what it argues and how well it argues it, never on its date. The older idea is weighed and either it holds or it does not — and on this subject it largely does hold, as [The ordering](#the-ordering-and-what-the-literature-says-about-it-directly) shows. That conclusion is reached from Goodenough and Gerhart's own argument, not from their precedence, and it would stand unchanged if the paper were twenty years younger.

Age is also not a sign of soundness, and this project's own history supplies the counter-example worth carrying. "Everything is a file" is an idea of exactly the kind this record admires — old, general, and precise enough to shape everything built on it — and it is a catastrophe that the ecosystem never named. Serializing structured data to a byte stream on a file, and requiring another process to read it and reconstruct the structure, discards the structure at the moment of writing and reconstructs it by a second, independent guess; two parties must then agree on a format neither of them designed for the other's benefit, and every property the type system or the schema guaranteed is now a convention that can be violated silently. Nothing in the arrangement is justified by the domain, and no document says it is a mistake, so it continues.

The general form is what matters here: **an idea's antiquity is independent of its merit, and a widely inherited idea that nobody has ever named as a mistake is the most dangerous kind there is** — because the absence of criticism is being read as the presence of agreement. That is the failure mode this research could have fallen into, had it treated the pre-TDD literature as authoritative because it was older and more precise rather than because it was argued.

*(Attributed to [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati), who raised this caution while the corpus was being assembled. One correction to the same observation belongs on the record: this project has not documented that criticism. "Everything is a file" appears in [Framework → Explicit and Implicit Frameworks](../../framework.md#explicit-and-implicit-frameworks) and in [System](../../system.md) as a worked example of an *implicit framework element* — a principle that constrains a system's design space whether or not it is written down — and is never criticized in this repository. If the critique is wanted, it has no home yet.)*

## Conclusion
Question 1 is answered: the pre-TDD literature understood a test as a formal object — a class of correct programs, a data-selection criterion with proved properties, a predicate-level description of a required input region — and refused to treat it as an arbitrary sample. That supports [test.md](./test.md)'s insistence that a Test be of a named Process rather than of code, while qualifying it in one respect: the formal object is stronger than the protocol's artifact, so "a test as specification" in that literature does not mean what it means in TDD practice.

Question 2 is answered and the popular citation is corrected. The claim is Dijkstra's, in EWD 249, an informal technical note, and it is very commonly misattributed to a compiler paper that does not exist.

Question 3 is answered, from the primary TDD book. There is **no documented descent** from this literature to TDD — Dijkstra and Parnas appear nowhere in Beck's 239 pages, and Beck credits a Smalltalk practice and a peer group instead. The absence is not a gap in this research but a finding about the record. And the two traditions diverge on meaning rather than only on pedigree: Beck puts tests *against* specifications, Goodenough and Gerhart make the test set the specification.

Question 4 is answered within its evidence and with its confounds stated: coverage-style structural testing is not a reliable proxy for fault detection, specification-based reading is a serious competitor on unit-sized programs, the authors' own literature review found mixed results, and their disfavored technique was run under a worst-case condition they disclose.

**Question 5 is the one that changes the protocol's own content**, and it was added because the first pass answered it wrongly. The ordering is not a call for hygiene and does not rest on the possibility of proof. Its ground, stated by the literature in 1975 and matching what [Process → Expectations and Checks](../../process.md#expectations-and-checks) already says, is reach: a check that draws only on the implementation cannot distinguish a wrong implementation from a wrong specification, because it has nothing else to compare against. Writing the expectation first is what lets a check reach the errors of understanding, which are the expensive ones. The ordering binds in every domain for that reason, and no source surveyed weakens it.

**Graduating into [test.md](./test.md)**: the ordering and its ground replace the framing the first pass installed, which had put Dijkstra's conclusion about mechanism beside the protocol's coverage obligation and read as a limit upon it. The two questions are now separated in the document, the error taxonomy is cited as the ground for the ordering, Beck's divergence is the reason the protocol does not adopt TDD's framing of a Test as a driver in place of a specification, and the note on antiquity and merit is recorded so the citation is not mistaken for a warrant.

This research stays **Active**. The corpus is not exhausted: the next sources worth reading are Howden's *Algebraic program testing* (1978), which is the strongest statement of test-as-specification and was verified bibliographically only, and the three Naur chapters that bear on expectation-first — "Problem Formulation" (1971), "Proof of Algorithms by General Snapshots" (1966), and "Programming as Theory Building" (1985) — of which only the table of contents has been seen.

## Related Artifacts
- [test.md](./test.md) — the protocol this research bears on. Two boundaries added, cited here as `Evidence`.
- [test.changelog.md](./test.changelog.md) — the entry recording those revisions, citing this record.
- [process.md → Expectations and Checks](../../process.md#expectations-and-checks) — the concept-layer topic that owns the definition of a check. This research adds no redefinition there; it found no source that contradicts what that topic states.
- [test.research.001.md](./test.research.001.md) — the companion research on ecosystem arrangement, which concerns the realization rather than the concept and shares no question with this record.
