# Khayyam Python Target Changelog
This file records what changed in [target.md](./target.md) and what each change reached. See [Changelog](../../../../modules-plugable/knowledge/documentation/changelog/changelog.md) for what this file's structure means.

## Changelog

### The Python target opened with the profile for a mechanical conversion
- Time: 2026-10-24T16:00:00Z
- Type: Added
- Contributors:
  - [Claude](../../../../CONTRIBUTORS.md#claude) (Opus-5.5) — argued, drafted, applied

#### What changed
- [target.md](./target.md) opened with the profile a Python source follows so that its conversion to Khayyam is mechanical: domain code apart from host bindings, the table of admitted constructs with the Khayyam form each maps to, and the contract suite as the test that accepts a conversion.
- The profile is Tentative; its ratification and its place are asked in the [handoff](./target.handoff.md).

#### Deliberation
- The owner's ruling of 2026-10-24 (Python first, Khayyam later, the Python written so that conversion is mechanical) is the input; the Go port's residue is the evidence of what a source written without a profile leaves (Claude — argued).
- A host binding is not translated because its Khayyam form is a body-less method whose implementation the host supplies, as the JavaScript target supplies it at link (Claude — argued).

---

### The profile's evidence corrected and its open forms named
- Time: 2026-10-24T16:50:00Z
- Type: Changed
- Tasks:
  - main:.agents/tasks/20261024-T162240Z-16944/: Complete - applies the independent critique of task 20261024-T161344Z-16944 to the Python-first delivery path
- Contributors:
  - [Claude](../../../../CONTRIBUTORS.md#claude) (Opus-5.5) — applied the critique's findings

#### What changed
- [Motivation](./target.md#motivation): the Go residue is stated as the work the Go bridge never attempted, since the bridge writes no bodies and matches declarations by name and arity ([`go-clue-residue` → The rule](../go/rules/go-clue-residue/go-clue-residue.md#the-rule)); the count of files holding the residue is the one `rg -l "TODO\(go-migrate\)" --glob "*.kh"` gives on 2026-10-24, 1,814, with the Go target's 852 noted as a figure that command no longer gives; the residue is no longer offered as proof that its forms cannot cross.
- [Abstract](./target.md#abstract): the claim that conversion is mechanical now says what is settled (the admitted constructs) and what is open.
- [Methodology](./target.md#methodology): the four places `claim.py` breaks the profile are stated.
- [The rules](./target.md#the-rules): rows added for arithmetic and comparison (methods with an explicit error output, after [Variable → Domain-Driven Arithmetic](../../../../docs/khayyam/variable.md#domain-driven-arithmetic)), for indexing, slicing, lookup and length (a domain container capsule over the raw ADT protocols, the builtin access only in a host binding), and for names (the identifier-naming and qualified-names rules); the conditional row now cites the draft `IF`; loops and jumps are a row of their own, marked and not mapped; the import row says a `modules-plugable` module cannot be named; the `async` row states that Khayyam has a form and that the profile is stricter by choice.
- [What the profile does not yet cover](./target.md#what-the-profile-does-not-yet-cover) is new: loops and jumps, unbounded integers and formatted text, the import of a pluggable module.
- The [handoff](./target.handoff.md) gained three open questions, one per uncovered form, and a Tentative decision on what the checker assumes meanwhile; "Which host does a converted module run on first?" left Open Questions as a Tentative decision, decided when the conversion is planned, since nothing depends on it before then.

#### Deliberation
- The critique (task 20261024-T161344Z-16944, findings (b)1 to (b)6 and (f)3) read the residue rule and the control-flow protocol files; both were read again here and agree with it (Claude — checked).
- A form was added only where a Khayyam document states it; where none does, the form is an owner's question (Claude — argued).

#### Considered and not done
- Correcting the 852 in [Go target → Motivation](../go/target.md#motivation): that document was not among those this task may change.

---

### The owner's working answers to the profile's four open entries recorded as Tentative decisions
- Time: 2026-10-25T14:30:00Z
- Type: Changed
- Propagates to:
  - [target.md](./target.md): Pending - its rules and "What the profile does not yet cover" still read as awaiting the owner; to be carried by the deeper tasks when they settle.
  - [Bundles → A composition in a project of its own](../../../bundles.md#a-composition-in-a-project-of-its-own): Pending - its prose still calls the profile Tentative until ratified and the import of a pluggable module open; only its links were repointed to the handoff's Decisions.
- Tasks:
  - dev-knowledge:.agents/tasks/20261025-T140621Z-16944/: Closed - records the owner's acceptance of 2026-10-25
  - dev-knowledge:.agents/tasks/20261024-T074257Z-16944/: Reference - the design task whose report asked the entries
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) - decided
  - [Claude](../../../../CONTRIBUTORS.md#claude) (Opus-5.5 via Claude Code) - recorded

#### What changed
- On 2026-10-25 the owner accepted the recommended option of each of the four open entries of [the handoff](./target.handoff.md) as a working answer, each to be studied in depth in a task of its own. Each entry left Open Questions and is now a Tentative decision carrying its reasons, the options not taken, and its deeper task:
  - "Does the owner ratify the Python profile, and its place under the Khayyam toolchain?": ratified in place, task 20261025-T140522Z-16944.
  - "What Khayyam form does a profiled loop or jump convert to, while the flow library declares none?": admitted and marked, task 20261025-T140523Z-16944.
  - "What capsule does a Python integer holding a quantity become, and what form has text built from values?": a width-naming domain capsule, and a text method of the capsule that owns the text, task 20261025-T140524Z-16944.
  - "How does profiled Python import a module under `modules-plugable/`?": the alias `modules_plugable`, task 20261025-T140525Z-16944.
- The decision on what the checker assumes now names these working answers instead of the open entries; the decision on the profile's place no longer waits for a ratification. The Open Questions section, left empty, was removed.
