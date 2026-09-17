# Content Handoff

## Topic & Purpose
Open questions and anticipated work for the Content model document (`content.md`), relocated there when the documentation method removed unresolved-question lists and the Discussion wrapper from base documents' bodies.

## Status
Active

Open work for `content.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](./documentation-handoff.md) for what a handoff is.

## Open Questions

### Are navigate/embed/execute properties of the Reference edge, or consumer-determined?
- State: moved 2026-09-11 from the Reference topic's retired Discussion wrapper. Nothing in the topic settles whether the different things a consumer might do upon encountering a Reference ("navigate," "embed," "execute") are properties of the edge itself (e.g., a `mode` field) or entirely determined by the consuming Thing's own rules.
- Next: test against concrete cross-modal cases as the Interaction concern develops.

### What scope does Lexical Token uniqueness actually take?
- State: moved 2026-09-11 from the Lexical Token vs. Sense topic's retired Discussion wrapper. Whether uniqueness is global across a system (the working decision) vs. local per document — and whether it requires finer-grained scoping rules — is unexamined.
- Next: examine multi-party, multi-document scenarios in consumer projects such as `organization`.

### How do overlapping or nesting compound tokens behave?
- State: moved 2026-09-11 from the same wrapper. Token composition (the polysemy mechanism) has not been tested against real multi-word phrases that overlap or nest.
- Next: run real corpus cases through the composition rule.

### Does the Addressable Entity principle admit an a-priori test?
- State: moved 2026-09-11 from the Addressability topic's retired Discussion wrapper. The principle is honestly circular (recorded in the body); the body also names the alternative empirical framing — what units are naturally independently referenced within a medium's own conventions — as the direction worth pursuing.
- Next: pursue the empirical framing rather than a predictive test.

### Is Composition's `contains` edge the same primitive family as Reference?
- State: moved 2026-09-11 from the Composition topic's retired Discussion wrapper. Whether containment is a typed edge no different in kind from `refers-to`/`mentions`, or ownership/lifecycle requires its own distinct primitive, has not been tested against enough real cases to decide.
- Next: test against cases where containment implies lifecycle obligations (aggregates) versus not (presentation trees).

### Does the project need a minimal, rendering-agnostic arrangement primitive?
- State: moved 2026-09-11 from the Layout topic's retired Discussion wrapper. Whether even a minimal abstraction (ordering, grouping, priority — algorithms entirely left to renderers) is warranted, versus zero shared vocabulary, is unresolved; the body defers this to a dedicated document once sufficient concrete cases exist.
- Next: see the dedicated Layout/Theme document under Anticipated Work.

### Where does Theme's authority end, and does user-authored composition freedom extend beyond styling?
- State: moved 2026-09-11 from the Theme topic's retired Discussion wrapper. The Theme/Layout/Launcher-like-boundary relationship is unresolved, as is the more radical possibility that end users may compose their own Widget/Page arrangements (the Android Launcher analogy, recorded in the body's Where Theme's Authority Ends).
- Next: decided together with the arrangement question in the dedicated Layout/Theme document.

### What addressing mechanism supports deep recursive addressability?
- State: moved 2026-09-11 from the Multi-Instance topic's retired Discussion wrapper. Current URL structure does not naturally accommodate arbitrarily deep addressability into a Composition graph; the question's recurrence across unstructured content and Composition is itself evidence that Addressability is one shared primitive, but the concrete mechanism is unresolved here.
- Next: design the deep-addressing mechanism; coordinate with the Platform layer (PersiaOS) where cross-runtime synchronization is concerned.

### Must the Authoring Model be a new syntax, or a disciplined HTML/Markdown subset?
- State: moved 2026-09-11 from the Authoring Syntax topic's retired Discussion wrapper. Both remain live candidates — a new compact syntax, or a subset of HTML/Markdown compiled through an intermediate tool that strips scattered metadata (`title`, `property`, `content` attributes and similar) in favor of short `refers-to-type` edges resolved from a Type Definition. Neither is chosen.
- Next: prototype both against real legacy templates (the invoice examples).

### What is the testable criterion for "Khayyam-manner"?
- State: moved 2026-09-11 from the Khayyam-manner topic's retired Discussion wrapper. The two properties (no unwrapped primitives; absolute encapsulation) are stated informally; without a pass/fail test the label risks being claimed by any language.
- Next: derive the criterion from concrete cases — see the anticipated short document below.

### Where is the boundary between structural delimitation and embedded semantic tagging?
- State: moved 2026-09-11 from the Structural Notation topic's retired Discussion wrapper. Flagged high-priority: the Position A/B question (pure delimiter vs. implicit semantic tagging, e.g. Markdown's `#`) is directly testable against this project's own YAML-front-matter-plus-inline-Markdown convention, and the document's own ASCII tree/graph diagrams already demonstrably exhibit Position-B behavior (recorded in the body).
- Next: see the self-audit under Anticipated Work.

### How does the model cover media that is neither pure text nor a typed capsule?
- State: the document-wide cross-cutting question, moved 2026-09-11 from the retired document-level Discussion. Media (image, audio, video) may need region/timestamp addressing while no Type system currently governs their internal structure; the question belongs to no single topic.
- Next: examine when media topics develop; relates to the Addressability questions above.

### Can one Content participate in multiple Timelines, and is Timeline a distinct concern?
- State: the knowledge-management session modeled organizational history as Content units attached to one or more Timelines — the pattern where a post lives in its author's timeline and reaches others' timelines through re-entry, without duplicating the unit. This is also what makes knowledge.md's Task-Centric principle realizable: one Task's outcome can appear in several participants' views while remaining one Content. content.md defines Composition, Reference, and (unresolved) Arrangement, but names no Timeline concern and no ordering semantics such a view requires; `knowledge.md` formerly pointed its scope boundary at a "Timeline" domain model here, which did not exist — that dangling reference was removed.
- Next: decide whether Timeline is a distinct concern, or a consumer-side projection under Arrangement/Composition, when the first multi-timeline case is worked in a consumer project such as `organization`.

## Anticipated Work

### A concrete Authoring Syntax prototype
- State: from the retired document-level Future possibilities. Compile an Authoring Model to Khayyam graph calls and test against real legacy templates (the invoice examples referenced throughout the document) to validate the concept/implementation split claimed across the concern topics.
- Next: after the Authoring-Model syntax question above narrows the candidate space.

### A dedicated Layout/Theme document
- State: from the retired Future possibilities. Once enough real Composition examples exist across at least GUI and one non-visual modality (VUI or Braille) to test candidate rendering-agnostic arrangement vocabularies and the Theme/Layout/Launcher boundary.
- Next: collect the cases; carry the two related Open Questions above.

### A testable "Khayyam-manner" criterion
- State: from the retired Future possibilities. Likely its own short document, derived from concrete cases of languages that do and do not qualify.
- Next: draft once implementation experience accumulates.

### A self-audit of this project's own Markdown+front-matter convention
- State: from the retired Future possibilities. Test the Position A/B question against the documentation format this very document is written in — directly testable against material already in daily use, unlike most other open questions.
- Next: run when documentation-method work next touches the authoring format.

### Cross-modal rendering experiments
- State: from the retired Future possibilities. Take a single Semantic Graph instance through both a GUI renderer and a VUI renderer, to empirically test whether the Semantic/Interaction/Rendering separation claimed throughout actually holds under real multi-modal pressure.
- Next: depends on the first renderer implementations.

### Independent verification of the AI-generated prior-art survey
- State: from the retired Future possibilities. Particularly the unresolved CKML entry, before any of its conclusions are relied upon elsewhere.
- Next: primary-source review of the CKML entry.
