---
Title: "Khayyam Rule — Specification Verification"
Labels: Draft
Start Date: 2026-11-09
---
# Khayyam Rule — Specification Verification
A rule held for [Khayyam](../../khayyam.md), applying before nontrivial Khayyam code is written or explained.

## The rule
- **Read the live Khayyam specification for the construct in question; do not supply syntax from general language knowledge or analogy.**
- **When a translation construct does not map cleanly, locate its documented replacement pattern before proposing syntax.**
- **Treat language grammar and organization-specific toolchain rules as separate authorities.**
- **Before writing or approving an abstraction, resolve every influencing and influenced type and every composed member to its live declaration, following inclusions and re-exports.** An abstraction-owned signature names abstractions only, as [Abstraction → What You Cannot Do](../../abstraction/abstraction.md#what-you-cannot-do) requires. A type's name, its location in `protocol/`, an archived example or frontend acceptance does not establish its declaration kind.
- **A service-shaped abstraction is also checked against [Service Contract](../../../../process/service/rules/service-contract.md#the-rule).** Its separate Request and Response associations are explicit; a custom action method on the Service is refused by review.
- **Check the relation being modeled before accepting a type substitution.** Composition states required behavior; DeclaredAbstractions records intended implementation targets under its owning protocol. A domain role may extend the underlying value behavior and be exposed through a separately named observer. A service-specific observer uses GetRequest or GetResponse with its own service value type and records the general observer as intended metadata, as [Service Contract](../../../../process/service/rules/service-contract.md#the-rule) states. Numeric conversion belongs to Binary, with conceptual value types and explicit encoded-span inputs rather than fixed capsule widths in names.
- **Record the boundary of each check.** A successful parser/import check establishes those checks only. The review names any declaration-kind, service-shape or semantic invariant the tool did not verify.

## Why it exists
Khayyam's language and governance boundaries are its design; inventing a familiar-looking form changes that boundary instead of applying it.
