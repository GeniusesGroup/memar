---
Title: "Khayyam Rule — Identifier Naming"
Status: Draft
Start Date: 2026-09-26
ID: "497336"
---

# Khayyam Rule — Identifier Naming
Khayyam's rules live one rule per folder under [`modules/khayyam/rules/`](../README.md), and this is the rule for the convention an organization holds its identifiers to — which script, which transliteration, which casing, and how names carry domain meaning. It is a rule of an organization, stated here because the grammar leaves the choice open: [Khayyam → Language Keyword in a Glance](../../../../docs/khayyam/khayyam.md#language-keyword-in-a-glance) states what an identifier is and stops there.

## The rule
The grammar's identifier admits any script; this repository holds itself to the conventions below. An organization may state different conventions, or none.

- **PascalCase** for capsule names, abstraction names, method names, and field names inside capsules.
- **Domain-meaningful names**: a variable or type name states a domain concept, not a machine representation or type detail. Because every `vr` carries an explicit type annotation, the name is free to state the *why* rather than the *what* ([Variable in Khayyam → Self-Documenting Code and No Magic Numbers](../../../../docs/khayyam/variable.md#self-documenting-code-and-no-magic-numbers)).
- **No type-redundant prefixes**: Hungarian-notation-style prefixes (`intCount`, `strName`) are unnecessary and discouraged.
- **Module-constant variables**: file-level `vr` names that serve as module constants use PascalCase (e.g. `MaxTimeout`), matching capsule naming.
- **Avoid generic capsule names**: names such as `Manager`, `Handler`, and `Helper` indicate missing domain specificity and are discouraged.
- **Names without package context**: a name must state its own domain meaning rather than relying on a package or directory prefix to supply missing context ([Modularity in Khayyam → Naming Without Package Context](../../../../docs/khayyam/modularity.md#naming-without-package-context)); `ParentCommand` is preferred over `Parent` when seen alone.
- **No throwaway capsule names**: a single-use capsule created only to avoid closure syntax must still receive a domain-meaningful name; a badly named throwaway capsule is a naming-convention concern, not a reason to add closure syntax ([Encapsulation in Khayyam → Closures as Implicit Capsule Syntax](../../../../docs/khayyam/encapsulation.md#closures-as-implicit-capsule-syntax)).

Abstraction names that frame technical capability rather than domain concept (`Readable`, `Writable`, `Filterable`) are governed separately by the [abstraction naming heuristic rule](../abstraction-naming-heuristic/abstraction-naming-heuristic.md). Method verb-phrase shape is governed by the [method verb phrases rule](../method-verb-phrases/method-verb-phrases.md). Collision qualification is governed by the [qualified names rule](../qualified-names/qualified-names.md).

## Why it exists
Because the grammar accepts any script and any spelling the lexer can read, a convention is a choice rather than a restriction — which is exactly why it has to be a deliberate one. The state this rule replaces was the reverse: an ASCII-only repertoire and scattered "suggested conventions" written into language documents as if they were the language's, which would have made a developer writing Persian or Chinese names unable to conform to the specification and would have let organizational style drift apart from the grammar's positive claims.

## Keep it or drop it
An organization may keep any convention it likes here — ASCII only, one script, camelCase, snake_case, transliterated names — or none. Acceptance answers whether the convention fits the organization holding it, not whether it is valid; an unaccepted convention may still be the right one for the project that proposed it, and that project is expected to enforce it in its own repository.

## What this rule does not claim
- It does not claim the grammar restricts names to a script, casing, or domain vocabulary.
- It does not claim one script is better than another, or that a transliteration is a name.
- It does not claim case-sensitivity or the reservation of the seven keywords, which are the language's own.
- It does not claim a name may collide with another module's; that is the [qualified names rule](../qualified-names/qualified-names.md), independent of style.
- It does not claim utility-oriented capsule names (`Utils`, `Helpers`, `Common`) are forbidden; that is the [domain capsule naming rule](../domain-capsule-naming/domain-capsule-naming.md).

## Open questions
This rule's own open state lives in its [handoff](./identifier-naming.handoff.md).
