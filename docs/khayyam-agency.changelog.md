# Agency in Khayyam Changelog

## Changelog

### Initial draft, as khayyam-concurrency.md
- Time: 2026-06-30T00:00:00Z
- Type: Added
- Cited:
  - [Control Flow in Khayyam](./khayyam-control_flow.md) — Depends_on: this document builds on the precedent set by that document of keeping behavioral policies as ordinary library-driven mechanisms rather than new syntax.
  - [Framework](./framework.md) — Depends_on.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, argued: original design decisions — no `go`/`async`/`await` keywords, definition-site (not call-site) tagging of a method's synchronous/asynchronous nature via an abstraction, user-space scheduling aligned with Unikernel/Exokernel architecture, and the function-coloring-avoidance argument for why syntax-level concurrency primitives were rejected.

#### Summary
Established that Khayyam embeds no concurrency model into its syntax. A method's synchronous or asynchronous nature is an intrinsic property of its own definition, tagged via an abstraction, not a choice made by the caller. Execution runs on user-space threads managed by framework-level schedulers. Written as a single flat document (`Summary` / `Guide-level explanation` / `Reference-level explanation` / `Drawbacks` / `Rationale and alternatives` / `Prior art` / `Unresolved questions` / `Future possibilities`), ahead of this project's Explanation-facet specification and its documentation-changelog convention — no paired changelog file existed until this one.

---

### Renamed to khayyam-agency.md and reframed through the Agency lens
- Time: 2026-08-17T00:00:00Z
- Type: refactor
- Cited:
  - [Agency](./agency.md) — Depends_on: this document's central new claim — that a Worker/Actor-style representation should not be hard-coded into a language's grammar — is stated in Agency's own terms (Execution Agent as a representation, not a primitive) rather than reconstructed independently here.
  - [Process](./process.md) — Depends_on: the Concurrency topic's escalating decision chain (shared state → ... → synchronization → locking) is cited directly as the reasoning a `go`-style keyword would bypass.
- Propagates to:
  - khayyam-control_flow.md: Reference only — this document's citation of Control Flow's own general syntax-minimalism argument was checked against the current file and found accurate; no change needed there.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested, argued: raised, in the same conversation as the Agency/Process/Worker Telegram-post discussion, that `khayyam-concurrency.md` did not need to remain an independent, narrowly-scoped document, and proposed two alternatives — merging it into `khayyam-control_flow.md`, or renaming and broadening it to `khayyam-agency.md` so that Khayyam-specific design decisions could be discussed through the same Agency lens the project had just finished applying to `process.md`; explicitly asked for an independent recommendation rather than agreement; argued that baking concurrency primitives into the language (as most languages do, under pressure from prior art) is the same category of naive modeling this project's Agency and Process documents already name — treating Worker/Actor as a primitive rather than as a representation of a bounded execution responsibility — and that Khayyam should not add that flawed abstraction merely because other languages do.
  - [Claude](../CONTRIBUTORS.md#claude) — reviewed, rewrote, recommended: read `khayyam-control_flow.md` in full before recommending; recommended against merging into it, on the grounds that concurrency and control flow are different subjects that happen to share a design philosophy (library-driven, not syntax-driven) — a philosophy `khayyam-control_flow.md` already states generally enough to be cited rather than needing the two documents merged; recommended the rename to `khayyam-agency.md`, scoped for now to the concurrency-specific content that already existed, with an explicit Unresolved question left open about whether the document's scope should later grow to cover other Agency-flavored Khayyam decisions, rather than speculatively writing that broader scope now; migrated the document into the current Explanation-facet template; moved front-matter `Citations` (which had a duplicate, YAML-invalid `Citations:` key from the original draft) and `Author(s)` into this changelog; computed a UTC-hour-count ID (495210, from the original Start Date) to replace the placeholder-looking `000011`, matching the convention `khayyam-control_flow.md` and this project's other documents already use; added "Concurrency Decisions as Agency, Not Syntax" as new content connecting the original, independently-reasoned design decisions to Agency's and Process's later, independently-developed vocabulary, explicit that the connection is retrospective rather than a rewrite of the original motivation.

#### Summary
`khayyam-concurrency.md` is renamed `khayyam-agency.md` and migrated to the current template. No existing technical content (definition-site tagging, user-space scheduling, function-coloring avoidance) was removed or weakened. A new topic, "Concurrency Decisions as Agency, Not Syntax," states explicitly what was previously only implicit: that rejecting `go`/`async`/`await` as keywords avoids the same modeling error Agency and Process later named independently (treating an execution representation as a primitive rather than as a stand-in for a bounded responsibility), and that this convergence is being recorded now, after the fact, not claimed as the original reasoning. A malformed, duplicate `Citations` key in the original front matter is resolved by the same front-matter migration already applied elsewhere in this project. The document's own placeholder ID (`000011`) is replaced with a UTC-hour-count identifier consistent with its sibling documents.

#### Rationale and alternatives
- **Merging into `khayyam-control_flow.md` (considered, rejected).** Both documents share a design philosophy — the compiler exposes minimal primitives, named behavior is a library decision — but concurrency and control flow (branching, looping, error propagation) are different subjects a reader would look for separately; `khayyam-control_flow.md` is already substantial, and the shared philosophy is already stated generally enough there to be cited by this document rather than requiring the two to merge. This also matches `process.md`'s own precedent of keeping Concurrency as its own topic rather than folding it into a general control-flow-equivalent topic.
- **Expanding this document's scope immediately to cover every Agency-flavored Khayyam decision (considered, rejected for now).** Omid's proposal explicitly floated a broader scope; this pass keeps the document's actual content limited to what already existed (concurrency), and records the broader-scope question as an Unresolved question rather than writing speculative content for design decisions (e.g. method-ownership-by-other-methods) that have not themselves been finalized yet.

---

### Closed the method-ownership speculative question after checking khayyam-method.md directly
- Time: 2026-08-17T00:00:00Z
- Type: Fixed
- Cited:
  - [Method in Khayyam](./khayyam-method.md) — Reference: checked directly to resolve Unresolved question 3, rather than continuing to speculate about its content secondhand.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: asked for khayyam-method.md to be checked given this document's own speculative mention of method-ownership as a possible future Agency connection.
  - [Claude](../CONTRIBUTORS.md#claude) — reviewed, rewrote: read khayyam-method.md's Method Structure topic directly and found that a method's "owner" there is a type-system attachment point (the type a callable behavior is structurally attached to — a capsule, an abstraction, or another method), not a party responsible for or delegating an action. The two documents share the word "owner" but not the underlying concept. Updated Unresolved question 3 to record this as a closed sub-question rather than leaving it as an open possibility.

#### Summary
The candidate connection between Khayyam's method-ownership model and Agency, raised speculatively in the previous entry, does not hold up on inspection — resolved as a non-connection rather than left open.

---

### Removed premature Worker/Actor naming from Unresolved questions and Future possibilities
- Time: 2026-08-17T00:00:00Z
- Type: Fixed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued: pointed out that even proposing a specific execution mechanism's name or shape — including as a mere Future-possibility suggestion, not a language feature — risks the same category of error this document argues against, since naming "Worker" or "Actor" in prose can quietly become the assumed answer the same way a keyword would in grammar; also noted that this document's own name changed from concurrency-specific to Agency-general, and that it should not stay implicitly concurrency-only just because concurrency is the only fully worked-out example so far.
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote: removed "Worker"/"Actor" naming from Unresolved question 2, Future possibilities, and the closing paragraph of "Concurrency Decisions as Agency, Not Syntax," replacing each with unnamed language ("a standard-library representation of an execution Agent," "whatever it ends up being called"), leaving the concrete design and vocabulary entirely to a future runtime/compiler-focused document rather than suggesting a shape here.

#### Summary
This document had drifted into naming a specific mechanism ("Worker/Actor package") in three places while arguing against exactly that kind of premature naming. All three are now unnamed, leaving the actual design and vocabulary to a dedicated future document.

---

### Broadened beyond concurrency: Agency Beyond Concurrency topic added, title changed, compiler/runtime-boundary content migrated in
- Time: 2026-08-17T00:00:00Z
- Type: Changed
- Cited:
  - [Abstraction in Khayyam](./khayyam-abstraction.md) — Depends_on: the new "Agency Beyond Concurrency" topic is grounded directly in that document's own "Is Khayyam's Structural Satisfaction Model Sufficient..." Unresolved question, checked firsthand before writing.
  - [khayyam-design_philosophy.md] — Depends_on: "Khayyam Is Not Its Own Compiler or Runtime" is migrated from that document's Reference-level explanation, as part of that document's planned retirement.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued, requested: pushed back on three places where this document, despite arguing against premature mechanism-naming, had itself named "Worker/Actor" as a proposed package — asked for all three to be de-named; separately asked that this document's scope not stay implicitly concurrency-only now that its title no longer says "concurrency," and offered to supply any document needed to check a real connection rather than have one guessed at; confirmed `khayyam-design_philosophy.md` is slated for retirement and that transferable content should move into documents already in scope, including this one.
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote: removed "Worker"/"Actor" naming from three locations (Unresolved question 2, Future possibilities, and the closing paragraph of *Concurrency Decisions as Agency, Not Syntax*), replacing each with unnamed language. Requested and read `khayyam-abstraction.md` and `khayyam-design_philosophy.md` before writing anything further, per the standing practice this review has followed since an earlier, incorrect speculative connection (method-ownership) was caught and reverted. Added "Agency Beyond Concurrency: Intentional vs. Accidental Contract Satisfaction," reframing `khayyam-abstraction.md`'s own open question (structural vs. intentional abstraction satisfaction) through Agency's vocabulary (an `agent_for`-style relationship requires a declared, intentional undertaking; Khayyam's current structural model has none in this sense) without taking a position on which of that document's three resolution options is correct. Retitled the document from "Agency in Khayyam: Concurrency Without Baked-In Primitives" to "Agency in Khayyam" and rewrote the Abstract to introduce both instances rather than reading as concurrency-only. Migrated "Khayyam Is Not Its Own Compiler or Runtime" into Future possibilities, reinforcing why this document does not design an execution-Agent representation itself.

#### Summary
This document no longer reads as concurrency-specific. Its title, Abstract, and Unresolved questions now reflect two checked instances (concurrency; abstraction satisfaction) rather than one, and three places that had drifted into naming a specific mechanism ("Worker/Actor") despite the document's own argument against doing so are now unnamed. "Khayyam Is Not Its Own Compiler or Runtime," migrated from the document slated for retirement, now backs the claim that designing an execution-Agent representation belongs to a separate runtime/compiler document rather than to this one.

---

### Reverted: compiler/runtime-boundary content does not belong in this document
- Time: 2026-08-17T00:00:00Z
- Type: Fixed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued: pointed out that migrating "Khayyam Is Not Its Own Compiler or Runtime" into this document was an odd choice, since Khayyam already has (or needs) a dedicated compiler/runtime document — specifically to tell a future organization building a Khayyam compiler what problems others already ran into, so they aren't reproduced — and that content belongs there, not here; supplied `Khayyam-compiler.md` as the existing document this content should eventually connect to, while noting he has not yet reviewed that document closely himself.
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote: removed the compiler/runtime-boundary elaboration ("the language specification defines *what* is guaranteed... a specific compiler or runtime defines *how*...") from Future possibilities, leaving only the original, simpler pointer to Khayyam's compiler/runtime documentation generally. Did not migrate the underlying content into `Khayyam-compiler.md` in this pass — that document has its own, larger migration pending and is being handled as a separate, self-contained task.

#### Summary
This document no longer carries compiler/runtime-boundary content. Future possibilities points at Khayyam's compiler/runtime documentation without elaborating on what that boundary is — that elaboration belongs with the compiler/runtime documentation itself.
