# Documentation — Comparison Changelog

## Changelog

### Consolidated the comparison method from `comparisons/README.md` into this document, generalized to any project
- Time: 2026-10-07T03:45:00Z
- Type: Added
- Cited:
  - [Comparisons folder](../../../../docs/comparisons/) — Reference: the essay folder this document governs; discovered by listing, not indexed here.
  - [Comparison: Memar and Hindsight](../../../../docs/comparisons/hindsight.001.md) — Evidence: the disclosure quota, whose origin is that essay's own unverified claims and off-repo benchmarks; the second-opinion pass on counts and citations; and the treatment of a collapsed history as a source-status finding.
  - [Comparison: Memar and Tensorus](../../../../docs/comparisons/tensorus.001.md) — Evidence: the triple-marking requirement, raised by a project whose disclosure reached its code and its README while its own maturity verdict sat unreached in the repository root.
  - [Comparison: Memar and Hindsight](../../../../docs/comparisons/hindsight.001.md) — Evidence: the second-opinion pass on counts and citations, and the treatment of a collapsed history as a source-status finding.
- Propagates to:
  - README.md: Done — the public pointer now names this document.
  - docs/README.md: Rejected — the folder entry already covers where essays live, and restating the method there would duplicate it.
  - comparisons/README.md: Done — replaced by a git symlink whose blob is `../documentation-comparison.md`, staged with mode `120000`.
  - documentation-comparison.handoff.md: Done — opened with the two obligations the changelog must not carry.
  - hindsight.md: Done — the standing-principles link retargeted at this document, its absorptions marked inline, and one unverified claim corrected.
  - tensorus.md: Done — the absorptions and the merged research thread marked inline.
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [Space Bunny](../../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../../CONTRIBUTORS.md#opencode)) — drafted, applied

#### What changed
- Created `documentation-comparison.md` (ID 497579, Status: Draft) consolidating the former `docs/comparisons/README.md`: the fairness rules and the standing principles are preserved, and the file gains a symmetric Abstract, a proper front matter, and the Explanation facet's body structure.
- The document was generalized on review: it specifies a kind of essay a project may write, and this repository's essays are stated as its arrangement rather than as the rule. The first draft had smuggled one project's identity into the method itself — where the essays live, and a project-specific rule stated as the method's own.
- `docs/comparisons/README.md` is now a git symlink to `../documentation-comparison.md`. This repository sets `core.symlinks = false`, so the working tree holds the target path as plain text and the entry is staged with `git update-index --cacheinfo 120000`; a plain `git add` would record it back as a regular file and turn the symlink into a two-line stub. `content check docs` reports "no newline at end of file" for the same path, which is the checker reading a link's target as text. Both consequences are recorded in the paired handoff, which is where live obligations belong, not here.
- A critique pass by a party that did not draft the document reshaped it: the required shape became a numbered section rather than a sentence in the Abstract; a rule about where essays live replaced a paragraph naming this repository's placement; the essay's obligations were extended explicitly, because an essay is no facet's document and the cross-cutting conventions did not reach it by their own terms; the four dated requirements were scoped forward rather than claimed of the essays that predate them; and the document's own production history was removed from its body.

#### Considered and not done
- **Leaving the document scoped to Memar**: rejected on review. A method that names one adopting project cannot be adopted by another, and the owner's intent was a document every project installs and uses for its own comparisons.
- **Removing `docs/comparisons/README.md` outright**: the symlink now carries the path, and pre-existing relative links resolve to this document through it.
- **Rewriting historical citations in changelog entries**: entries such as `knowledge.changelog.md` cite `comparisons/README.md` because that is what was consulted at the time; the symlink resolves those citations, and rewriting them would misstate the record.
- **Adding membership links from this document to individual essays**: the Content Rule forbids fabricated or redundant indexes; essays are discovered by listing the folder.
- **Changing the fairness rules' substance**: rules 1–7 keep their content; the change is whose model they are written against.

---

### Essays carry an ordinal, the location is stated rather than offered, and the sections speak of the essay
- Time: 2026-10-07T05:20:00Z
- Type: Changed
- Cited:
  - [Documentation — Research](../research/research.md) - Reference: the ordinal and supersession rules this document now follows for the same reason - a re-examination is a newer record, not a rewrite.
  - [Documentation — Explanation](../explanation/explanation.md) - Premise: a body section speaks of the subject it governs, not of the container the subject happens to sit in.
- Propagates to:
  - docs/comparisons/: Done - all eight essays renamed to <project>.001.md; fourteen files carried inbound links to them and were retargeted.
  - documentation.handoff.md: Reference - none needed.
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) - decided
  - [Space Bunny](../../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../../CONTRIBUTORS.md#opencode)) - argued, drafted, applied

#### What changed
- A new section, [How an essay is identified over time](./comparison.md#how-an-essay-is-identified-over-time), states the naming rule: one essay per examination, <project>.001.md then <project>.002.md, the ordinal carrying creation order and nothing else. The distinction it turns on is correction against re-examination - a wrong citation or a moved count is fixed in the file that is wrong, while a project examined again at a later revision gets a new essay that cites the first, so a reader can always tell which state of both projects an argument was made against. All eight essays were renamed accordingly, and the fourteen files holding inbound links were retargeted, historical changelog citations among them: a path that no longer resolves is a broken link, and the entry that cites it is a record of a claim rather than of a filename.
- The location section now states where the essays are - docs/comparisons/, with the folder's README.md a symlink to this document - and keeps only the two rules that generalize: listing rather than indexing, and one essay per file named after its project. The previous wording offered the location as a project's decision, which in this repository it is not, and would have had agents re-asking a settled question in every later chat.
- The two sections that spoke of the folder now speak of the essay, and the sections are titled accordingly.

#### Considered and not done
- **Renaming only the essays written from now** (rejected): two naming conventions in one folder is the drift the Content Rule exists to prevent, and the corpus is small enough that one rename settles it.
- **Keeping the bare names and numbering only the second examination** (rejected): that is the form the Research facet rejected for the same reason - the first file's name would change the moment a second appeared, and renaming breaks every reference already held.

---

### The facet's closed lists leave the specification for their types
- Time: 2026-10-17T12:00:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — ruled (2026-10-16)
  - [Claude](../../../../CONTRIBUTORS.md#claude) (Sonnet 5.5) — applied

#### What changed
- The ten stages of an essay are no longer listed in [The essay's required shape](./comparison.md#the-essays-required-shape); the type `EssayStage` gives them and their order.
- Why: the owner ruled on 2026-10-16 that every field a facet declares is a type, and that once typed the prose restating it leaves the document, keeping the reason ([A Fact in Code Is Written Once](../documentation.md#a-fact-in-code-is-written-once)); the types are in this facet's `primitive/`.
- Made in task 20261016-T194831Z-4504.
