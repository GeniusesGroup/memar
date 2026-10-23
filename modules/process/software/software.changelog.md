# Software Changelog

## Changelog

### Initial recording of the Software concept
- Time: 2026-09-10T00:00:00Z
- Type: Added
- Cited:
  - [Software Configuration Management](https://en.wikipedia.org/wiki/Software_configuration_management) — Reference: surfaced during the layering session as the lifecycle prior-art direction; its activity taxonomy (configuration identification, baselines, change control, status accounting, audit) informs the lifecycle positioning.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — directed
  - [Super Z](../../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — drafted

#### What changed
- The placeholder document established the settled positions: software as the objective manifestation of a system of aggregated processes; software not limited to the computer world (the computer is the dominant substrate, not the defining one); "software ecosystem" flagged as undefined and excluded from carrying weight; the IEEE software documentation family (730, 828, 829, 830, 1012, 1016, 1028, 1058, 1063) recorded as the prior-art taxonomy of the lifecycle concern space, mapped to the homes the framework already owns.
- Full definition refinement, lifecycle treatment, scope-boundary decision, and standard-successor verification are owed to dedicated chats (see the paired handoff).
- The document was founded from the Immutable Infrastructure layering session's findings, so the dedicated chat does not restart from zero.

#### Deliberation
- Founding the document was directed during that chat: the deployment-governance scoping surfaced the ambiguity of "software" and "ecosystem", and the valuable findings were to be captured in a founded document rather than scattered session notes (Omid Hekayati — directed).

---

### "Software ecosystem" read through the established Ecosystem definition
- Time: 2026-09-10T11:32:04Z
- Type: Changed
- Propagates to:
  - software.handoff.md: Done — the "Terminology decision on ecosystem" anticipated-work item removed as graduated.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Super Z](../../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote

#### What changed
- The founding session's interim position — "ecosystem" undefined, must not carry weight until Memar decides — is superseded: the [System document has since established the definition](../../../docs/system.md#ecosystem), and the document now reads "software ecosystem" through it.
- The section was retitled from `"Software ecosystem" is not a Memar term` to `"Software ecosystem"` and rewritten: the term names the ecosystem formed around software practice; a software system is a constituent such an ecosystem can form around, never the ecosystem itself; the marketing sense remains a Business Term carrying no weight, with the naming-the-concrete-relationships discipline kept as the response to it.
- The Abstract's "treated as undefined until Memar decides otherwise" clause was replaced accordingly.

#### Deliberation
- The supersession was directed in the ecosystem de-ambiguation session: the audit showed the corpus's ecosystem uses conforming to the structural sense, and the owner approved the definition and the reference fixes together (Omid Hekayati — decided).

---

### IEEE 1012 row's Khayyam hyperlink removed per citation direction
- Time: 2026-09-23T07:07:01Z
- Type: Fixed
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Mimo](../../../CONTRIBUTORS.md#mimo) (mimo-v2.6-flash via [OpenCode](../../../CONTRIBUTORS.md#opencode)) — applied

#### What changed
- The Software verification and validation row now reads "abstraction conformance in the Khayyam documents is the compile-time verification face". The claim is unchanged; the upward hyperlink into `khayyam/abstraction.md` is removed.

#### Deliberation
- A base document never links into `khayyam/` — plain-text naming only (Omid Hekayati — decided).

---

### The owed rows say what kind of owed
- Time: 2026-10-05T05:30:00Z
- Type: Changed
- Cited:
  - [Process Research 001](../process.research.001.md) - **Reference**: `owed` is right for project management as an activity and misleading read as a concept in waiting.
- Propagates to:
  - [software.md](./software.md): Done - the 830 and 1058 cells qualified in place.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) - directed, decided
  - [Meta AI](../../../CONTRIBUTORS.md#meta-ai) (muse-spark via [OpenCode](../../../CONTRIBUTORS.md#opencode)) - argued, applied

#### What changed
- The requirements row now names the standing interpretation (Test's umbrella-requirement reading) and marks full treatment owed as modeling-constraints working-out, not as a second artifact. The project-management row now reads owed as an activity projects run, not as a Memar concept in waiting, with the unit-of-work question assigned to consuming projects and finished delivery to Enterprise.

---

### Review of the uncommitted changes of 2026-10-12
- Time: 2026-10-12T09:45:29Z
- Type: Reviewed
- Contributors:
  - [Claude](../../../CONTRIBUTORS.md#claude) (Sonnet-5.5) — reviewed

#### What changed
- Reviewed; no change needed. Checked the working tree against HEAD for `software.md`, `software.handoff.md` and `software.changelog.md`: the requirements and project-management rows of the lifecycle table now match the 2026-10-05T05:30:00Z entry above, which cites a statement the Process research makes (`owed` right for project management as an activity, misleading as a concept in waiting) and a Test section that exists; the handoff's requirements-home question stays open, as the row says full treatment is still owed; the handoff and table link changes resolve; no removal.
- `memar content check` on the three files reports no problem.

---

### No hidden inputs
- Time: 2026-10-16T12:00:00Z
- Type: Changed
- Propagates to: none
- Contributors:
  - [Claude](../../../CONTRIBUTORS.md#claude) (Sonnet 5.5) - drafted, applied

#### What changed
- In [software.md](./software.md), a new subsection *No Hidden Inputs* under Explanation: inputs are explicit, old shapes are converted by a script and not kept readable by the core, and what can be a type is not written as prose.
- Why: the owner ruled this on 2026-10-13 and asked on 2026-10-16 that such rulings live in Memar's documents.
- Rests on the owner's statement; Khayyam's *Zero-Magic Core* (`docs/khayyam/khayyam.md`) is the same principle for the language.

---

### The document moves to `modules/process/software/`
- Time: 2026-10-17T14:30:00Z
- Type: Changed
- Cited:
  - [Modules → What does not belong here](../../README.md#what-does-not-belong-here) — `Depends_on`: a concept document stands beside the module or category of its subject
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Claude](../../../CONTRIBUTORS.md#claude) (Sonnet-5.5) — applied

#### What changed
- `docs/software.md`, `software.changelog.md` and `software.handoff.md` moved to a new module, `modules/process/software/`, whose `README.md` is a link to this document. Links to the three documents were rewritten and nothing else in them changed.
- The handoff gained one entry, on whether the life-cycle declarations of `computer/type` and `computer/capsule` belong to this module. They were read and not moved: a Type's carrying a life-cycle state is a property of Type, and the state set itself is software's, so the question is how the two split.
- Occasion: the owner's ruling of 2026-10-17 that this document's subject is a process and that its module is the one to create now.
