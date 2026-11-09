---
Title: "Type Rule — Map Concepts onto Realizations"
Labels: Draft
Start Date: 2026-11-09
---
# Type Rule — Map Concepts onto Realizations
A rule of this repository, held for [Type](../../type.md), for turning identified concepts into named realizations. It applies after [Modeling](../../../../../docs/modeling.md) has decided that a concept exists.

## The rule
- **One concept is one named entity.** Nominal identity: never merge semantically distinct concepts because their structures match; never split one concept because structures differ.
- **Instance variation within one concept is data fields on its realization, not new Types.** If a member of a static family later acquires genuine per-instance data, that one capsule graduates to a data carrier; the static members of the family remain distinct Types.
- **A stateless concept is still a Type, and each MUST be its own named entity** ([Stateless Types](../../type.md#stateless-types)). Detection: every distinguishable fact about it is fixed at definition time, and two variables of the type are indistinguishable. Never represent such concepts as a name string, tag value, or enum inside one shared container filled in at runtime.
- **A multi-outcome call declares the Abstraction as the outcome type;** the returned value's concrete Type carries which-one occurred. Dispatch among candidates may defer to runtime; identification of any single concept stays a direct type assertion. Exhaustiveness over an open Abstraction is a need the Type model does not itself meet; until something meets it, callers rely on manual completeness discipline.
- **Naming conventions for a static-concept family live in that family's governing document,** and are non-binding unless a contract requires them.

## Gray zones
- Incidental metadata (one timestamp field on a status-like entity) does not make it a data carrier — rerun the modeling test on responsibility, not field presence.
- A pragmatic exception (externally-defined specification with an open-ended set of variants) may justify a shared variant-carrying type — record the exception explicitly where used.
- Optional-field accumulation that is meaningful only for some instances signals merged concerns — route back to modeling.
- Structural match from languages that type by structure has no identity force here.
- A registry that admits new concepts at runtime must pass the modeling test for every concept it admits and must not violate [Structure Is Fixed by Definition](../../type.md#structure-is-fixed-by-definition).

## Why it exists
Absorbed from the former Type Practice companion so the operational mapping steps sit beside Type as rules rather than a second document under `docs/`.

## Keep it or drop it
An organization may choose different mapping conventions and remain conformant to Memar's Type concept; it then owns the cost of identity demoted to runtime data.

## What this rule does not claim
- It does not decide whether something is a concept; that is Modeling's.
- It is enforced by no check this repository runs today.
