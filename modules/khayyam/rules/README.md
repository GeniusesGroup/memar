# Khayyam Rules (`modules/khayyam/rules/`)

## What this folder is
The general Memar concept of Rule — ownership, `rules/` beside `protocol/`, linters, and rule engines — is defined in [`docs/rule.md`](../../../docs/rule.md). This folder is **one catalog** of Rules for Khayyam work in this repository.

These rules are introduced by Geniuses.Group for work in Khayyam; they are not part of the Khayyam language, and another organization may define and enforce its own rule set for the same language.

Khayyam's rules: conditions this repository's toolchain enforces or its sources are held to, each with its subject and with whether it gates compilation, reports governance, or rewrites source. A rule's normative claim — what the language means — stays in the document that owns its subject under [`docs/khayyam/`](../../../docs/khayyam/); this folder holds the executable form and cites that claim. The members a rule declares are the rule model's, and the model has not fixed them: the record is the [toolchain handoff → *Rule model: one authored rule, two request paths, and a compile-time gate*](../execution.handoff.md), which enumerates identity, subject, condition, consumes, produces, enforcement and scope and states that every one of them is provisional, its **Rule** and **rule engine** protocol work being unfinished. Until that work settles them, this index claims none of them: what a rule document states is the four things [below](#what-a-rule-document-states), and a member the model has not fixed is not among them. Nothing here is final.

Each rule has its own folder, holding a main document named after the rule, a handoff beside it carrying that rule's open questions, and this pointer README. The folder listing below is the index; the documents are not restated here.

Observer and mutator abstractions (`Observer_X`, `Mutator_X`) are governed by the [ADT observer and mutator rule](../../computer/adt/rules/observer-mutator/observer-mutator.md), not Khayyam grammar.

## The rules
| Rule | Subject | Enforcement | Scope | What it is |
| --- | --- | --- | --- | --- |
| [Comment Forms](./comment-forms/comment-forms.md) | The `//` and `/* … */` markers | Compiler input (the scanner) | Unit | Which comment markers this toolchain reads, and why the choice is a tool's |
| [Comment Policy](./comment-policy/comment-policy.md) | The license header, and where documentation lives | Governance | Repository | What every `.kh` file opens with, and where prose belongs while a type has no documentation method |
| [Code Scope Placement](./scope-placement/scope-placement.md) | Where a `sc` may be declared | Compiler gate (`scope-placement`) | Unit | Scopes inside method bodies, and why an organization may drop the rule |
| [Import Address](./import-address/import-address.md) | The form of an `in` path | Resolver (accepts any shape that resolves) | Unit | The value is a URI and the scheme is dependency management's; the spelling of a file's name is the owner's |
| [Unresolved Import](./unresolved-import/unresolved-import.md) | An `in` path with nothing behind it | Compiler gate (`unresolved-import`) | Unit | The first of the four import-resolution rules |
| [Name Not Declared](./name-not-declared/name-not-declared.md) | An `in` naming what the target does not declare | Compiler gate (`name-not-declared`) | Unit | The second |
| [Kind Mismatch](./kind-mismatch/kind-mismatch.md) | A `tp` form naming a `vr`, or the reverse | Compiler gate (`kind-mismatch`) | Unit | The third |
| [Unbound Type Name](./unbound-type-name/unbound-type-name.md) | A type name nothing declares or includes | Compiler gate (`unbound-type-name`) | Unit | The fourth |
| [Identifier Naming](./identifier-naming/identifier-naming.md) | Script, transliteration, casing, domain meaning | Governance | Repository | PascalCase and domain-meaningful names this repository holds itself to |
| [Abstraction Naming Heuristic](./abstraction-naming-heuristic/abstraction-naming-heuristic.md) | Abstraction names framing domain vs capability | Governance | Repository | Domain-concept framing over technical-capability names |
| [Qualified Names](./qualified-names/qualified-names.md) | Names that collide across modules | Governance | Repository | The name carries its module where it is declared, and a collision is reported |
| [Receiver Parameter Naming](./receiver-parameter-naming/receiver-parameter-naming.md) | The owner parameter name in a method signature | Governance | Repository | Suggests `self` where any name is grammar-valid |
| [Lifecycle Method Names](./lifecycle-method-names/lifecycle-method-names.md) | Teardown and absence method spellings | Governance | Repository | Conventional `Deinit`/`Free`/`IsNull` names for this repository |
| [Domain Capsule Naming](./domain-capsule-naming/domain-capsule-naming.md) | Utility-category capsule names | Governance | Repository | Discourages `Utils`/`Helpers`/`Common` dumping-ground capsules |
| [File Layout](./file-layout/file-layout.md) | File size and declaration order | Governance | Repository | Short single-responsibility files, contracts-first reading order |
| [Type as Argument](./type-as-argument/type-as-argument.md) | Bare type or closure-style `mt` at call sites | Governance | Repository | Flags type-as-value and implicit-capsule method passes |
| [Orphan Extension](./orphan-extension/orphan-extension.md) | Methods attached outside the owning directory | Governance | Repository | Local directory extension permitted; distant attachment reported |
| [Abstraction Scaffolding](./abstraction-scaffolding/abstraction-scaffolding.md) | Linter delegation and satisfaction assists | Governance | Repository | Scaffolding and remediation without grammar magic |
| [Receiver Method Names](./receiver-method-names/receiver-method-names.md) | A method name no file imports | Governance | Repository | The method keeps the bare name, because the receiver supplies the context |
| [Method Verb Phrases](./method-verb-phrases/method-verb-phrases.md) | The shape of a method name | Governance | Repository | A method name is a verb phrase that states what the method does |
| [Method Separation](./method-separation/method-separation.md) | Blank lines between method declarations | Source rewrite (`tidy --rule method-separation`) | Unit | One blank line between two methods in a file that carries prose |
| [Go Clue Residue](./go-clue-residue/go-clue-residue.md) | The Go clue block a ported file ends with | Source rewrite (`tidy --rule go-clue-residue`) | Unit | The block keeps only what the Khayyam declarations do not yet carry |
| [Commented Generic Bindings](./commented-generic-bindings/commented-generic-bindings.md) | Generic Go methods left in a clue block | Source rewrite (`tidy --rule commented-generic-bindings`) | Unit | A type parameter whose constraint names one abstraction becomes that abstraction in a real method |
| [Result Parameter Names](./result-parameter-names/result-parameter-names.md) | Parameter names the port generated | Source rewrite (`tidy --rule result-parameter-names`) | Unit | `resultN` and `argN` are named after the first letter of their type |

## This set is a floor, not a ceiling
The rules stated here are the ones this repository holds itself to. The set is explicitly open to extension, in both directions:

- **A rule this repository has not thought of is not thereby wrong.** Bring it — an issue or a pull request is the way in, and Memar is receptive to good rules.
- **A rule proposed here and not accepted is not thereby wrong either.** Acceptance answers whether the rule fits *this* repository, not whether it is valid. An unaccepted rule may still be the right rule for the project that proposed it.
- **You may keep that rule in your own organization's repository and enforce it in your own code.** That is a supported outcome, not a workaround: the same subject, a different owner, a different rule set. What belongs here is the rules worth sharing — those whose subject is the language itself, and whose absence would change what Khayyam programs may mean for everyone.

## Why it works this way
This is the point of Khayyam and of the architecture around it: nothing is simply right or wrong, and a claim is answered where it belongs rather than forced down to the lowest abstraction. A rule that is right for a codebase is not thereby a claim about every codebase, and a rule that belongs to a project is not thereby a defect in the language.

The base documents under [`docs/`](../../../docs/) do the other half of that work: they state what is certain about the language, and they do not carry prohibitions. A condition whose handling may differ between one tool and the next is stated by the tool that applies it, which is why a rule that used to sit in a language document — the comment forms, the `sc` placement limit, the shape of an import path — is a folder here instead, and why the language document's own statement of the matter is a positive principle rather than a list of things the grammar refuses.

## Membership criterion
A rule belongs here when all of the following hold:
- its subject is Khayyam itself — the language or a contract Khayyam owns;
- it is executable as a condition over analysis input, not a statement of intent;
- it cites the document that states its normative claim;
- it states its enforcement class (gates compilation, reports governance, or rewrites source) and its scope (a unit or a repository).

A rule about your own project's conventions does not belong here — it belongs to your project, and saying so is a legitimate answer, not a rejection. A rule about how this repository's *documentation* is written does not belong here either: its subject is the documentation, not Khayyam, and it is carried as a decision in the [toolchain handoff](../execution.handoff.md) instead.

## What a rule document states
Each rule's document says four things: what the rule is, why it exists, whether an organization may keep it or drop it, and what it does not claim. The last of these is load-bearing rather than a formality — it is what keeps a rule from reading as a language guarantee, and it is where a second toolchain's freedom to differ is written down.
