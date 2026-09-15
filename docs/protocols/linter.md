---
Title: "Linter"
Status: Draft
Start Date: 2026-06-22
ID: 495025
---

# Linter

## Abstract
A **linter** is a system that enforces governance rules on programs that are already well-formed as existence. It does not decide what may exist — that is the [Compiler](./compiler.md). It decides how well-formed instances must flow, name, and relate, under a rule set an organization can replace without forking a language. This document is Memar's protocol for that system: what a linter is, how it is distinct from a compiler, that a governance rule is authored in the document that owns its subject and only *checked* here, and that a linter must not become a second compiler. The protocol is language-independent: the same split — ontology in the compiler, governance in the linter — applies to a C or Go toolchain as to any other.

## Introduction

### Motivation
A language that bakes architectural policy into grammar forces every project using it to inherit that policy. The opposite failure is quieter: a toolchain that treats "important" governance as if it were grammar, until disabling a check is treated as forking the language. Both failures collapse the same distinction. This document exists so that governance has a named home that is *designed* to be configurable, and so that a rule about errors, memory, modularity, or naming is not invented inside a linter specification merely because a linter is the tool that will flag it.

The second gap is authorship. Before this protocol, it was not stated how a governance rule is written: which document owns it, what a check must name, and which tier (error, warning, suggestion) it may carry. Without that, each linter team re-derives policy from language lore, and the linter becomes the de-facto owner of rules it should only enforce.

### Methodology
The compiler/linter split is the same line [Khayyam](../khayyam/khayyam.md) states as *Separation of Syntax and Governance* — existence versus flow — lifted out of that language's documents because the line is a protocol concern, not a grammar. The authorship rule (a rule lives in the document that owns its subject) is the pattern [The Error](./error.md#enforcement-of-the-each-error-is-its-own-type-rule) already exercises for the `Err` prefix: that document owns the convention; a linter, if configured to, checks it. This document generalizes that pattern and does not re-list per-subject rules.

## Explanation

### What a linter is
A linter is a system that takes a program the compiler has accepted as well-formed, together with a configured rule set, and reports where the program violates those rules. Its outputs are diagnostics — errors, warnings, suggestions — not a new language. A program that fails only the linter is still a program of that language; it has failed an organization's governance posture.

### Linter versus compiler
**The compiler enforces ontology** — whether a type, value, or relationship may appear at all. Disabling a compiler rule changes what programs exist.

**The linter enforces governance** — policies about how already-well-typed instances move, name, and relate. Disabling a linter rule changes how well those programs are kept, not whether they are programs.

A decision that *creates* or *denies* existence belongs in the compiler precisely because a linter rule can be disabled. Memory-safety path coverage is governance ([Memory → Safety enforcement is governance](./memory.md#safety-enforcement-is-governance)); an uninitialized read is ontology ([Memory → Uninitialized reads are refused](./memory.md#uninitialized-reads-are-refused)). The same test applies to every candidate diagnostic: if turning it off would admit a program the language's specification says cannot exist, it is a compiler concern wearing a linter's name.

The failure this topic exists to prevent is the linter quietly becoming a second compiler — hardening governance into de-facto language restrictions.

### A rule's home is its subject's document
A governance rule is stated in the document that owns the subject the rule is about. The linter does not own the rule; it owns the *check*. [The Error](./error.md#enforcement-of-the-each-error-is-its-own-type-rule) is the standing example: the `Err`-prefix convention lives there, as a non-binding convention whose enforcement, if any, is per-organization linter configuration. Naming, modularity, encapsulation, and memory-path coverage follow the same placement. This document is not a catalogue of those rules and does not grow by absorbing them.

### How a governance rule is authored
Until a notation is designed (see the paired handoff), a rule that this protocol will accept as a linter check has these required members, stated in the owning document:

- **Subject** — which claim, convention, or contract term is being checked, with a link to that claim's home.
- **Tier** — error, warning, or suggestion. Suggestion is the default for conventions; error is earned by a flow-correctness claim (for example path-complete teardown under [Memory](./memory.md)), and remains organization-overridable.
- **Default** — whether a reference configuration ships the check on or off.
- **Override** — that an organization may relax or replace the check without forking a language.

The notation itself — a capability interface, a configuration schema, a Syllab-level annotation — is not settled. What is settled is that the linter does not invent rules that have no home outside it.

### Configuration and override
A linter ships a reference configuration, not a unique legal configuration. Organizations add, relax, and replace checks. Custom governance rules plug into the same machinery rather than living in ad-hoc scripts. A conformance suite, when one exists, tests that a linter implementation honors this protocol's split and the authorship members above — it does not freeze any one organization's rule set.

### Analysis consumes compiler events, not library names
A linter (and any analysis library it uses) subscribes to events the [Compiler](./compiler.md) emits — entering and leaving a scope, taking or skipping a branch — rather than recognizing a particular library's constructs by name. Branch exclusivity is learned from those events. Special-casing one control-flow library's `IF` as if it were grammar undoes the compiler's own refusal to privilege libraries, and it undoes it on the analysis side where the mistake is harder to see.

### Assistance writes source, on request
When a linter or companion tool generates code — accessors, teardown calls, suggested types — it writes **explicit source** the author can read, review, and refuse, matching [Memory → Teardown is explicit, and automation writes source](./memory.md#teardown-is-explicit-and-automation-writes-source). It does not synthesize a public surface the author never requested. Mechanical generation of an accessor for every field recreates public fields with extra steps; generation is faithful only when requested deliberately.

### Tooling may present structure first
A linter's companion IDE or editor MAY fold continuous declaration blocks and, on first open, fold bodies so contracts are visible before implementations. Fold state SHOULD persist and be overridable: aggressive folding can disorient a reader who does not yet know the file's shape. Which syntactic forms count as a "declaration block" is a realization fact of the language being edited, not this protocol. Persistence unit (per-file, per-project, per-session) and whether folding should degrade for very small files are unsettled — see the paired handoff.
