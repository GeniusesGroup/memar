# Cognition Handoff
Open work for `cognition.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../modules/knowledge/documentation/handoff/handoff.md) for what a handoff is.

## Open Questions

### Conversation formalization as Protocol
- State: whether a conversation between two cognitive systems should be formally specified as a Protocol in Memar's sense — with its own document — or whether that over-formalizes an activity whose norms are stated conceptually here. Related: what is lost, conceptually, when the medium is asynchronous and persistent (a repository comment thread) rather than live — whether that changes the model or only the medium's properties.
- Next: decide if a protocol treatment earns its place (see Anticipated Work). Do not grow medium properties in the base meanwhile.

### Discourse-norm enforcement
- State: which of the discourse norms, if any, are strict enough to warrant linter-style verification in written artifacts versus remaining conversational disciplines; and whether the "hidden reasoning" warrant in the proportional-criticism norm should be parameterized (e.g. by the maturity of the artifact being criticized) or whether the qualitative statement — now tied to inspectable material — suffices.
- Next: propose a linter check when a norm violation first appears in a written artifact.

### Intra-system thinking
- State: the conversation model and most discourse norms address inter-system exchange; most agent work under this document is solitary reading and drafting. The 2026-09-15 upgrade closed part of the gap: *Report absence*, the artifact-as-claim norm, asymmetry obligations (no self-citation as fact; declare context limits; externalize state), and the structural fallacy definition all bind intra-system work. Whether further solitary-only rules are needed remains open.
- Next: examine when a solitary-analysis rule beyond those is first needed.

### Further cognitive-science grounding
- State: what further cognitive-science grounding deserves adoption as the document matures — working memory constraints on exchange design, dual-process accounts of evaluation, or others — and by what criterion each is admitted.
- Next: admit grounding when a norm needs a better-specified basis.

### Is questioning an elementary operation?
- State: forming a question — turning what the material lacks into something that can be asked — is exercised by intake, by the practice's "ask what the material lacks," and by the TizFekri vocabulary's پرسشگری; the critical-thinking literature's "question at issue" names the same thing. Whether it is an operation of its own or generation aimed at a gap is undecided.
- Next: admit it when a document's work is shown to depend on it in a way generation does not cover.

### Elements of thought as a component class
- State: the critical-thinking literature (Paul and Elder) pairs its standards with elements of thought — purpose, question, information, concepts, assumptions, inferences, implications, point of view. Several are already present here as disciplines (goal, assumptions) or operations (inference); whether the rest — what a piece of cognitive material is made of, rather than what is done to it — earn a component class of their own is undecided.
- Next: decide when a norm or practice needs to name a part of cognitive material that no current component names.

### A change's size is judged by its reach, and the judge is the one least likely to examine it
- State: moved 2026-10-19 from README.md → Where Memar Stops (a section removed when organization joined this repository; task 20261019-T183339Z-19720). Its claim: the practice has no threshold below which it is skipped. A change's size is judged by the participant about to make it, from inside the exchange where it is proposed, and that judgment is the one least likely to be examined, because the exchange feels too small to hold one. A one-line edit to a definition is a large-scope change. Loading the practice costs a few reads; a concept quietly redefined is paid for, silently, by every document that cites it. [Confirm before large-scope changes](./cognition.md#confirm-before-large-scope-changes) already turns on reach rather than line count; the point about who judges, and why, is not in it.
- Next: fold the point about who judges into that norm, or into [Cognition Practice → Norm Application Points](./cognition.practice.md#norm-application-points), when the norm is next revised.

## Settled This Chat (removed from Open when closed)

### Two concerns believed conflated — seam sharpened
- Was: owner suspected model/derivation vs operational discourse-norms were mixed, and that the practice was not the right operational home.
- Settled shape (2026-09-15): the live seam is **conversation-model-plus-norms** (where normative work happens) versus the **modes/operations reference layer** (which does not currently derive the norms). Norms stay in the base; procedural residue (confirm deliverable, conceptual-root questioning, intake checkpoints) lives in the practice's Norm Application Points. Full re-scope of the practice from critique-first to norms-first is deferred until critique procedures outgrow the file — not forced now.
- Claimants: Claude (Opus-5) claimed the sharper seam; ChatGPT (GPT-5.6-terra) claimed several norms were underived from the conversation model alone; the body now states that honestly; Omid Hekayati decided the boundary cut and the consult-other-systems norm.

## Anticipated Work
- The component classes — operations, standards, disciplines — grow as Memar's work demonstrates dependence on a further member, each addition argued in this document's changelog; the translation table of named kinds gains a row when a name keeps arriving in the project's work, never a section.
- **TizFekri vocabulary survey:** map the TizFekri institute's practice vocabulary (پرورش مهارت‌های اجرایی، پرسشگری/استدلال‌ورزی/تصمیم‌گیری نقادانه، دلیل آوردن و نقد دلایل، «باهم اندیشیدن» و «با هم ساختن»، #اندیشیدن_آموختنی_است) against this document's components — including the *consult other cognitive systems* norm against باهم اندیشیدن / با هم ساختن; the survey decides whether any mapping earns a place in the body or stays a reference.
- **Use-rule reader test:** watch whether working chats actually translate named kinds into components and hold input, steps, and output to the standards, or keep reaching for the names; revise wording where the rule still requires interpretation.
- If the conversation-as-two-cognitive-systems model is formalized as a Protocol, this document remains the conceptual home and the protocol document the normative one, following the project's concept/implementation separation.
- Deeper cognitive-science grounding is expected to refine the norms over time — replacing qualitative statements with better-specified ones as the underlying science warrants.
- Candidate graduation (not scheduled): the named kinds left the Abstract when the model was rebuilt on components; if the translation table grows past a translation aid, graduate it to a companion Explanation under the progressive-migration pattern, keeping the components here.
- Binding-constraint diagnosis: Spec Kit names context-window exhaustion with its timing as a first-class cause; the skill holds the response (session economy, bounded delegation) but not the causal diagnosis. One sentence in the skill, or a rejected-with-reason line — owner's call, keeping the skill a pointer, never a copy.
