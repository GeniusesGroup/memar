# Test Changelog

## Changelog

### Protocol drafted, and the TDD document absorbed into it
- Time: 2026-09-30T00:00:00Z
- Type: Added
- Cited:
  - [../../process.md](../../process.md) - Depends_on: the concept document that owns the definition of an expectation and a check, and already states that they precede enactment.
  - [test.research.001.md](./test.research.001.md) - Evidence: no language specification and no standards body mandates any test layout, naming rule, or discovery scheme, which is what makes a placement condition a Rule rather than a standard.
  - [test.research.002.md](./test.research.002.md) - Evidence: the 1975 error taxonomy grounding the ordering in reach; the ecosystem's own account of TDD as a Test driving development *in place of* a specification; the absence of any documented descent from that literature to TDD; and Basili and Selby's disclosure that uncommented programs made their code reading a worst case.
  - [../../documentation-explanation.md → Merging before Final](../../documentation-explanation.md) - Depends_on: the rule authorizing the absorption below, since both documents were `Draft`.
  - [../computer/linter.md](../computer/linter.md) - Depends_on: the authorship rule that keeps the structural conditions out of this document.
  - [../../modeling.md](../../modeling.md) - Extends: the principle that commitments become explicit before they become costly.
  - [../../khayyam/khayyam.md](../../khayyam/khayyam.md) - Depends_on: the mechanism a type's human-facing text is written by, and the grammar that makes opaque code structurally impossible.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) - raised the placement question and ruled that the structural conditions are Rules rather than protocol text; asked whether the TDD document should be deleted and its content absorbed here; corrected the framing of the ordering and that a Test is not limited to code; ruled that a comment is not the destination for why a decision was made, and supplied the `sc` case; and ruled that the skill must bind non-software work too
  - Auto (model not recorded) - drafted both documents, conducted both researches from primary texts, wrote the rules and the tooling, and carried out the absorption
- Propagates to:
  - [test.practice.md](./test.practice.md): Added - the paired procedure, carrying two units: the development cycle and the Test artifact.
  - [test.handoff.md](./test.handoff.md): Added - open state, including the questions carried over from the absorbed document.
  - [test.research.001.md](./test.research.001.md): Added - how language ecosystems arrange tests, and who owns each convention.
  - [test.research.002.md](./test.research.002.md): Added - the testing literature written before TDD, read from primary texts, with its negative results recorded.
  - [../../../modules/process/test/](../../../modules/process/test/): Added - the module realizing this protocol, carrying the placement and naming Rules this document points to.
  - [../../../AGENTS.md](../../../AGENTS.md): Done - a section stating that text is not to be put into a file through a shell, with the command that does it instead.
  - [../../../.agents/scripts/memar-documentation.py](../../../.agents/scripts/memar-content.py): Done - gained `write`, `edit`, and `check`, because a document silently damaged by an encoding round trip is the failure this session produced twice.
  - [../../../.agents/scripts/README.md](../../../.agents/scripts/README.md): Done - gained a section on putting text into a file, and one on what a subfolder there is for.
  - [../../../.agents/scripts/tests/install.py](../../../.agents/scripts/tests/memar-install.py): Done - the installer's Tests moved out of the folder that owns what they check, into one named for the role, and the suite still passes.
  - [../../../.agents/skills/memar/SKILL.md](../../../.agents/skills/memar/SKILL.md): Updated - a development step now binds to a Test written first.
  - [../ddd.md](../lib/process/ddd.md): Done - its TDD relationship entry retargeted, since a document that no longer exists cannot be a sibling case.
  - [../ddd.handoff.md](../lib/process/ddd.handoff.md): Done - its pointer to the expectation-and-check step retargeted.
  - [../../process.handoff.md](../../process.handoff.md): Done - its two links retargeted here and to this document's handoff.
  - [../../process.changelog.md](../../process.changelog.md): Done - the link the absorption invalidated retargeted, and its historical entries on the absorbed document annotated.
  - [../../documentation-explanation.changelog.md](../../documentation-explanation.changelog.md): Done - annotated alongside its existing pointer to the removed changelog.
  - [../comparisons/superpowers.001.md](../../comparisons/superpowers.001.md): Done - three lines that attributed a Memar protocol to a name that no longer names one retargeted.
  - [../../documentation-changelog.md](../../documentation-changelog.md) - Reference: within one working session an entry may still be revised, which is why this session's six drafts are one entry.

#### What changed
- Added [test.md](./test.md), stating the Test as the written expectations of a named Process, produced before the work and kept as a standing part of the system that owes them. It separates the Test from the check and from the runner, states the obligation a system carries over the parts of its protocol surface whose expectations are decidable, what a Test may assume, what a passing suite does and does not establish, and the routing among development under the discipline, verification, and inquiry. It states no structural rule and points to the Rules that carry them instead.
- Added [The Expectation Is Written Before the Work](./test.md#the-expectation-is-written-before-the-work), grounding the ordering in reach: a check drawing only on an implementation cannot distinguish a wrong implementation from a wrong specification, because it has nothing else to compare against, so writing the expectation first is what lets a check reach the errors of understanding. The order within a step is stated as model, then protocol or abstraction, then Test, then enactment, on the ground that a Test written against an enactment with no stated contract has already decided the contract by producing the enactment.
- Added [The Form the Expectation Takes Is the Domain's](./test.md#the-form-the-expectation-takes-is-the-domains): a building's employer's requirement is a Process's expectations, and a drawing or a building-information model is how that requirement is written, because it is the form this domain's checks can be applied to and it moves a disagreement out of the reading of a sentence and into the comparison of a thing both parties can see.
- Added [A Test Is Documentation, and Comment Is the Last Place to Look](./test.md#a-test-is-documentation-and-comment-is-the-last-place-to-look), as a destination map rather than a ranking of two: what must hold is a Test; what a thing is and what a reader needs to read belongs to the thing's own declarations, which is the mechanism the language document describes and the grammar enforces; why a decision was made belongs to the artifact's structured companion, chosen by the facet that owns that kind of statement; and a comment is what remains when none of those can hold, which this repository's comment policy records as a fallback the direction of travel is away from.
- Added [The Ecosystem's Name for This Is TDD, and This Protocol Does Not Adopt It](./test.md#the-ecosystems-name-for-this-is-tdd-and-this-protocol-does-not-adopt-it), recording the name once and the reasons the protocol declines it: TDD names a practice this protocol applies beyond software, and Beck's own formulation puts a Test in place of a specification where this document makes a Test the specification.
- Absorbed `tdd.md` and its practice, handoff, and changelog, then removed them. The four topics it owned moved across; the development cycle became [The Cycle](./test.practice.md) in the practice beside the procedure for the artifact; the three questions its absorption does not answer were carried into [test.handoff.md](./test.handoff.md) and the two its absorption does were removed.
- Corrected a framing error found while reading the primary texts. An earlier draft placed Dijkstra's conclusion about what a check can conclude beside this document's coverage obligation and described it as a limit upon that obligation, conflating two questions: why the expectation must be written first, whose ground is reach, and what a check can conclude, whose answer is that only the expectation's own statement. EWD 249 does not address the first — it declines design methodology by name — and nothing in the literature weakens it.
- Added [What Would Take This Further, and What Would Not](./test.md#what-would-take-this-further-and-what-would-not), so that a reader who meets the result that a test can be a proof does not suspect the document of having missed it, with the reason it does not apply here: what licenses the conclusion is a proved property of the selection, which is a stronger object than a Test this protocol defines.
- Moved 54 archived Test artifacts into a `tests/` folder in the module that owns each, dropped the `_test` marker from their names, and moved the installer's Test suite to `.agents/scripts/tests/`.

#### Considered and not done
- **Keeping a short protocol document under the TDD name as a pointer.** It would preserve the vocabulary practitioners arrive with, and would make this document depend on a name whose established meaning — a Test as a driver in place of a specification — differs from what this document states. A reader who knows the word finds it named in one topic here.
- **Moving the ordering into [Process → Expectations and Checks](../../process.md#expectations-and-checks).** The concept layer already states that expectations precede enactment, and that is where the definition belongs. What it does not state is the reach argument for why a development must do it, and a claim about what a check can detect is a protocol-layer claim about the artifact the check reads.
- **Writing that comments should be eliminated.** The one measured statement on the question runs the other way. The claim is scoped to the subset a Test can carry.
- **Romanticizing the older literature.** The sources are admitted on what they argue and how well they argue it, never on their date; the caution that an idea's antiquity is independent of its merit, with this repository's own example of an inherited idea nobody ever named as a mistake, is recorded in the research rather than assumed away.
- **Correcting the absorbed document's changelog into this one wholesale.** Its load-bearing rejections are recorded here as considered-and-not-done; per [Merging before Final](../../documentation-explanation.md) no citation entry points at the abandoned document, and per the changelog facet its history does not become a second home for the same decisions.

---

### A failing check names the artifact that owes the repair
- Time: 2026-10-04T00:00:00Z
- Type: Added
- Cited:
  - [Comparison: Memar and GitHub Spec Kit](../../comparisons/spec-kit.001.md) - **Reference**: whose Adapt filter produced the item. Spec Kit's `/analyze` is strictly read-only and its Next Actions name the owning command per finding class, under the doctrine "return to the earlier step that owns them and fix them at the source".
- Propagates to:
  - [test.md](./test.md): None needed - [What a Passing Suite Establishes](./test.md#what-a-passing-suite-establishes) already separates what a run proves from the claim that the work is finished; this is the reporting form of that separation, not a new claim.
  - [documentation.md](../../documentation.md): None needed - no artifact-structure rule changes.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) - decided
  - [Space Bunny Alpha](../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../CONTRIBUTORS.md#opencode)) - drafted

#### What changed
- [The Cycle](./test.practice.md#the-cycle) gains a clause on what a failing check hands back. A check that fails for the wrong reason names the artifact that owns the repair, and the two failures have different destinations: an expectation that turned out to be wrong or incomplete is repaired in the document that states the contract, recorded there as a change rather than made silently; a contract that holds but is not yet enacted is repaired by the work, and the artifact that owes it is the one whose expectations are unsatisfied.
- The clause states why the distinction is load-bearing rather than tidy: naming the wrong one sends the next participant to correct a document that was right, which costs more than the finding was worth. This is the disposition step the practice already required, given a destination.

#### Considered and not done
- **A machine-readable result carrying the destination (not taken):** the obligation is on what a report says, and a format is the tool's decision. A participant whose check returns only a boolean still owes the sentence.
- **Naming the destination in `test.md` rather than the practice (rejected):** the practice is where steps are stated, and this is one more of them. The base protocol owns the claims; the practice owns the procedure that reports on them.

---

### The umbrella reading is declared standing
- Time: 2026-10-05T05:30:00Z
- Type: Changed
- Cited:
  - [Comparison: Memar and GitHub Spec Kit](../../comparisons/spec-kit.001.md) - **Reference**: the requirements-home fork and its domain-generality constraint.
- Propagates to:
  - [test.md](./test.md): Done - one standing-interpretation sentence at the section's close.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) - directed, decided
  - [Meta AI](../../../CONTRIBUTORS.md#meta-ai) (muse-spark via [OpenCode](../../../CONTRIBUTORS.md#opencode)) - argued, applied

#### What changed
- The umbrella-requirement section now states its own standing: no separate requirements document is planned, and a narrated desire stating checkable expectations satisfies the protocol in whatever artifact the domain's checks apply to. No structural rule added; building, bill-of-quantities, and acceptance-schedule examples keep first-class standing beside the user story.

---

### The party's own mind holds the discipline, and an expectation must let it decide
- Time: 2026-10-05T00:00:00Z
- Type: Added
- Propagates to:
  - [test.md](./test.md): Done — two places: the check's own description, and what an expectation must reach under the form clause.
  - [process.handoff.md](../../process.handoff.md): Done — the mirror handoff's baseline-and-declared-limit question was closed from the concept layer; the four-roles question under the same section stays open, as does its mirror here.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Space Bunny Alpha](../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- [Test, Check, and Runner](./test.md#test-check-and-runner) now states what performing the comparison is: a cognitive act, held to this document as written by every party that judges an instance and to nothing laxer than this document states, whatever evidence that party uses and whether or not anything ran. A green run, a review, and an inspection are named as evidence the party weighs; none of them is the comparison.
- [The Form the Expectation Takes Is the Domain's](./test.md#the-form-the-expectation-takes-is-the-domains) gains the clause the form clause had been missing — what the discipline needs in order to decide. Varying the form does not vary what a Test must reach, because the party holding this document decides rather than a mechanism: a Test states the model it is checked against, the instance it is checked on, and, where the checked subject can degrade, the limit on how much worse that instance may be on the way. Where the subject cannot degrade, the Test states the state that must hold at the end, and that state is the one the instance is measured against — this discipline's own requirement of such a domain, not an exemption from it.
- The clause ends by keeping the form the domain's: these are what an expectation has to reach, not fields it has to fill, and an artifact reaching them in its own vocabulary satisfies the protocol.

#### Deliberation
- Omid Hekayati ruled, in Persian: "As to how a process is to be evaluated, if it is to be evaluated it must be shaped in the mind of every party by the strictness of that very document test, and we must not weaken anything. If I have misunderstood again, explain it again so I can state my opinion more precisely." The ruling names this document as the measure, so the protocol layer states both halves it owns: the discipline the party applies, and the decidability the expectation must carry to be judged by it.
- Space Bunny Alpha placed the two statements at the two places that already own them rather than in a new section: the check's description for the discipline, the form clause for what an expectation must reach. A new section would have repeated both owners.
- The three things an expectation must reach were stated as reach, not as a schema, per the ruling's own second half: nothing may be weakened, but the shape stays the domain's, which is what this section already denies. A mandated field list would have hardened a form the section exists to leave open.
- Whether the ruling reaches [Test, Verification, and Inquiry](./test.md#test-verification-and-inquiry) was examined and answered no: verification is this document's own boundary, stated before the ruling, and a verification's artifact still carrying Test's obligations is not a licence to evaluate with a laxer standard — that sentence is recorded below as found, not edited.

#### Considered and not done
- Binding the discipline on *inquiry* processes beyond what this document already states for them: an inquiry's expectations are its evidence, decision, and record, and the ruling adds no fourth thing to them.
- Adding a worked example of a degrading subject and its declared limit: not taken; this document states no structural rule, and an example would fix a shape the domain owns.

---

### The floor carries what an expectation must reach, and a green run reports what the party establishes
- Time: 2026-10-05T17:20:58Z
- Type: Changed
- Propagates to:
  - [modeling.md](../../modeling.md): Pending - its maturity gate carries the parallel clause the floor sentence just shed; the exact wording is reported to that file's owner rather than edited here.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Space Bunny Alpha](../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- [A Test Is Part of the System That Owes It](./test.md#a-test-is-part-of-the-system-that-owes-it) states the floor in the terms the discipline needs: a system has met this protocol when, for every decidable expectation, it holds a Test reaching the model, the instance, and — where the subject can degrade — the limit on how much worse it may be. Having a Test per decidable expectation is no longer by itself the completion criterion, because a Test can exist for an expectation too thin to decide.
- [Test, Check, and Runner](./test.md#test-check-and-runner) keeps the substitution this section exists to stop while restoring what a run is entitled to be: a green suite reports that the checks it performed passed, and what that report may not stand in for is the comparison itself or anything about the Test or the runner beyond what the run performed. It remains evidence the judging party weighs, bounded by the next section, and the party decides what follows.
- [What a Passing Suite Establishes](./test.md#what-a-passing-suite-establishes) now has the establishing on the right side: a green run reports the one thing, and what establishes it is the party's act of comparison, which no run performs for it. The three substitutions the section rules out are unchanged and now follow from that difference rather than from the run's own verb.
- [The Form the Expectation Takes Is the Domain's](./test.md#the-form-the-expectation-takes-is-the-domains) received the smaller edit rather than a restatement. Its form paragraph already ended with a paragraph stating what a Test must reach, so the sentence claiming that only "the ordering and the checkable form" bind contradicted the paragraph after it; it now defers to that reach and says the checkable form is a domain's way of carrying it, never a substitute for it.
- [test.practice.md → The Artifact](./test.practice.md#the-artifact), step 3, extends the another-agent test past intelligibility: the reader must also find the model, the instance, and the degradation limit, and an expectation that leaves a reader asking what would count as met is not yet stated.
- [test.practice.md → Scaling](./test.practice.md#scaling) no longer makes the artifact the mechanically checkable subset at feature scale. Every expectation of the Process is in the artifact; the mechanically checkable subset carries the discipline by run and the rest by the party that owes the check.
- [test.practice.md → Boundary: When a Test Is Not the Artifact](./test.practice.md#boundary-when-a-test-is-not-the-artifact) states that the non-executable record satisfies the standing while its verdict is the party's act rather than a runner's — the standing was never the verdict, and the absence of a runner is not a release from the standard.

#### Considered and not done
- Adding the three things an expectation must reach to the obligation's first boundary, over Processes not lines: that bullet is about what is enumerated, and repeating the reach there would say the same thing a third time in one section.
- Editing the clause "scale changes how much an expectation states, never whether it is stated first", which appears in [test.practice.md → The Cycle](./test.practice.md#the-cycle) and again in [process.md → Development decomposition](../../process.md#development-decomposition): both were outside this change's scope and are reported instead.

---

### Test tiers with labeled seams
- Time: 2026-10-07T03:45:00Z
- Type: Changed
- Cited:
  - [Documentation — Comparison → Hindsight](../../comparisons/hindsight.001.md) - Evidence: Hindsight's three eval tiers (deterministic blackbox, scheduled real-model judged, external benchmark) — each with its verdict party and its tier. A verdict that borrows authority from a stronger tier manufactures evidence.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Space Bunny Alpha](../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- [Scaling](./test.practice.md#scaling) gains a *Tiers with labeled seams* subsection: deterministic checks on every change, model-dependent checks on a schedule, and single-home benchmarks; each tier states which party produces its verdict, and no tier borrows a stronger tier's authority.

#### Considered and not done
- **A fixed CI schedule** (not taken): the tiering states which party runs which tier and why, and leaves cadence to the consuming project's runner rather than inventing one cadence here.

---

### Review of the uncommitted changes of 2026-10-12
- Time: 2026-10-12T09:45:50Z
- Type: Changed
- Contributors:
  - [Claude](../../../CONTRIBUTORS.md#claude) (Sonnet-5.5) — reviewed, revised

#### What changed
- Fixed `test.md`, *What a Passing Suite Establishes*: the change had altered "three substitutions" to "four", but the section lists three things a green run does not establish (conformance, the rightness of the expectations, behavior not exercised). Restored to three.
- Fixed `test.research.001.md`, Open Questions, the bullet on the singular role folders: the change replaced `core/test/` with `services/*/test/`, which is not a path that exists, and the toolchain's test folders were all moved to the plural `tests/` in commit 8f63a66. The bullet now keeps the survey's `core/test/` and records the move, so the drift half of the question is shown as closed while the missing convention document stays open.
