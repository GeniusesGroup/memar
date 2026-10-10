---
Title: "The Type"
Status: Draft
Start Date: 2026-10-10
ID: 497671
---

# The Type

## Abstract
This document specifies Memar's Type module: what every realization of a Type carries so that the rest of a system can identify it, describe it to people, and know where it stands in its life. [Type](../../type.md) defines a Type as a semantic entity with an explicit identity and a defined contract; this module states the protocol through which that identity, the Type's human-facing details, and its life-cycle position are carried and read. It is stated without reference to any language, and how a language realizes it belongs to that realization.

## Introduction

### Motivation
A Type identified in one place, described in another, and versioned in a third drifts apart: the identifier a process compares, the text a person reads, and the record of whether the Type is still supported each change on their own schedule, and no party can tell which copy is authoritative. [Type → Human-facing identity](../../type.md#human-facing-identity) names this failure for human-facing metadata. This module gives each of these concerns one home, on the Type itself.

### Methodology
The requirements are derived downward from [Type](../../type.md) — its nominal identity, its rule for stateless Types, its Type metadata, and its principle that structure is fixed by definition — and from what a consumer already reads off a Type, chiefly [The Error](../process/error.md), which composes this module's identity, life cycle, and details. Where neither supports a requirement, the paired handoff records it as open instead of this document stating it.

## Explanation

### What this module owns
This module owns the protocol a Type is stated through: what identifies a Type, what describes it, what life-cycle position it holds, and how a consumer reads them. The concept of Type, its four categories, and the boundary of what is not a Type are [Type](../../type.md)'s, and this module does not restate them. A collection of Types — how many a system holds, and how one is found among them — is a different subject from a Type and is not owned here.

### Type identity
A Type answers "which Type is this?" from the Type alone, never from data an instance holds ([Type → Stateless Types](../../type.md#stateless-types)). It carries two identifiers for that answer:

- A **universally unique identifier**, produced by any mechanism that guarantees it is unique everywhere, so that two Types offered in different contexts never share one ([Type → Type Identity](../../type.md#type-identity)).
- A **short identifier**, taken from the leading 64 bits of the universally unique one, used to tell Types apart as domains where the shorter form serves.

Each identifier is also readable as Base64 text, for carriers that move text. Identity is the identifier alone: two Types are compared by their identifiers, and a consumer declares no second equivalence beside them ([The Error → Identity and equality](../process/error.md#identity-and-equality)).

### Type details and human-facing identity
A Type's human-facing identity — its localized names, labels, documentation, and localized descriptions of its behaviors and failures — belongs to the Type and has one source ([Type → Human-facing identity](../../type.md#human-facing-identity)). This module carries it as the Type's details:

- **About the Type in general**, for someone inspecting or managing it independently of any occurrence: the domain it belongs to, a one-line summary, and a longer overview.
- **About an occurrence**, for whoever meets one at the moment it happens: what the end user should do next, and what the developer or integrator should do next.
- **About the Type's own record**: an address where it is documented, the date it was issued, the date it expires, and the Type that replaces it, where one does.

Details are written for people, so what they say is vetted when the Type is defined: a detail can disclose how a system works, how to reach it, or something about its users, and each of those can be exploited.

The human-facing details are kept in companion artifacts beside the Type's definition, one per required human language, all sharing the Type's base name qualified by that language. They are never written inline in the functional definition, and never kept in external translation maps keyed by string lookup. A translator must be able to change their wording without a developer round-trip and without a full development environment, and such a change can never touch the functional definition; the tooling and workflow around a realization are what make that possible.

### Type life cycle
A Type holds a position in its own life cycle — where its definition stands between first release and the end of its support — and that position is part of what a consumer reads off it. This is a different subject from the stages [Type → Method — Type as Callable Behavior](../../type.md#method--type-as-callable-behavior) names for a Method (definition, composition, specialization, execution): it records the standing of the Type's definition among its consumers, not a stage of the Type's use. The issue date, expiry date, and replacing Type among the Type's details belong to the same record.

[The Error → Composition](../process/error.md#composition) already relies on four positions: `Experimental`, `Stable`, `Deprecated`, and `EndOfLife`. The set of positions this module requires is not yet stated, and the paired handoff records the ruling it waits on; until that ruling is given, no realization's list of positions is normative.

### Reading a Type
What a consumer may observe of a Type through this module is its identity, its details, and its life-cycle position, and the module offers reading operations over each of them and no operation that changes any of them.

### Crossing implementation languages
Where a Type is consumed in more than one implementation language, its identity and its details reach the other languages through output generated from the one source. They are never re-declared or re-translated there, and adding a language means generating again. Presentation layers, gateways, and generated bindings read the details from where they live, and keep no parallel mapping of their own.

### Implementation intent
A Type under construction that wants tools to scaffold it declares the Abstraction it targets through an ordinary construct of its own definition, as [Type → Implementation intent](../../type.md#implementation-intent) requires: it composes an intent-declaring Abstraction, or exposes a plainly named Method announcing the target. The protocol for that declaration is [the Tooling-Facing Implementation-Intent Declaration](./abstraction-implements.md), and this module does not restate it.

### Realization
This module is realized at [`modules/computer/type/`](../../../modules/computer/type/), whose README states what belongs there; the names of its declarations are that realization's own. A collection of Types is realized separately, at [`modules/computer/types/`](../../../modules/computer/types/).
