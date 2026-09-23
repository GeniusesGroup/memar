# Software Changelog

## Changelog

### Initial recording of the Software concept
- Time: 2026-09-10T00:00:00Z
- Type: Added
- Cited:
  - [Software Configuration Management](https://en.wikipedia.org/wiki/Software_configuration_management) — Reference: surfaced during the layering session as the lifecycle prior-art direction; its activity taxonomy (configuration identification, baselines, change control, status accounting, audit) informs the lifecycle positioning.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — directed
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — drafted

#### What changed
- The placeholder document established the settled positions: software as the objective manifestation of a system of aggregated processes; software not limited to the computer world (the computer is the dominant substrate, not the defining one); "software ecosystem" flagged as undefined and excluded from carrying weight; the IEEE software documentation family (730, 828, 829, 830, 1012, 1016, 1028, 1058, 1063) recorded as the prior-art taxonomy of the lifecycle concern space, mapped to the homes the framework already owns.
- Full definition refinement, lifecycle treatment, scope-boundary decision, and standard-successor verification are owed to dedicated sessions (see the paired handoff).
- The document was founded from the Immutable Infrastructure layering session's findings, so the dedicated session does not restart from zero.

#### Deliberation
- Founding the document was directed during that session: the deployment-governance scoping surfaced the ambiguity of "software" and "ecosystem", and the valuable findings were to be captured in a founded document rather than scattered session notes (Omid Hekayati — directed).

---

### "Software ecosystem" read through the established Ecosystem definition
- Time: 2026-09-10T11:32:04Z
- Type: Changed
- Propagates to:
  - software.handoff.md: Done — the "Terminology decision on ecosystem" anticipated-work item removed as graduated.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote

#### What changed
- The founding session's interim position — "ecosystem" undefined, must not carry weight until Memar decides — is superseded: the [System document has since established the definition](./system.md#ecosystem), and the document now reads "software ecosystem" through it.
- The section was retitled from `"Software ecosystem" is not a Memar term` to `"Software ecosystem"` and rewritten: the term names the ecosystem formed around software practice; a software system is a constituent such an ecosystem can form around, never the ecosystem itself; the marketing sense remains a Business Term carrying no weight, with the naming-the-concrete-relationships discipline kept as the response to it.
- The Abstract's "treated as undefined until Memar decides otherwise" clause was replaced accordingly.

#### Deliberation
- The supersession was directed in the ecosystem de-ambiguation session: the audit showed the corpus's ecosystem uses conforming to the structural sense, and the owner approved the definition and the reference fixes together (Omid Hekayati — decided).

---

### IEEE 1012 row's Khayyam hyperlink removed per citation direction
- Time: 2026-09-23T07:07:01Z
- Type: Fixed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Mimo](../CONTRIBUTORS.md#mimo) (mimo-v2.6-flash via OpenCode) — applied

#### What changed
- The Software verification and validation row now reads "abstraction conformance in the Khayyam documents is the compile-time verification face". The claim is unchanged; the upward hyperlink into `khayyam/abstraction.md` is removed.

#### Deliberation
- A base document never links into `khayyam/` — plain-text naming only (Omid Hekayati — decided).
