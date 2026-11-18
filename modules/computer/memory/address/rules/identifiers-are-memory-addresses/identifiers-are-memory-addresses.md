---
Title: "Address Rule — An Address Is Not a Domain Identifier"
Start Date: 2026-11-01
---
# Address Rule — An Address Is Not a Domain Identifier
A rule of this repository, held for [Memory Address](../../address.md). The owner ruled on 2026-11-01 that a private `ThingUUID` in every domain was wrong, and on 2026-11-17 that using `MemoryAddress` as that shared identity was wrong as well. A domain's subject identity is [A Domain Identifier Composes Identifier](../../../../../identity/identifier/rules/domain-identifier-composes-identifier/domain-identifier-composes-identifier.md). This rule says only what an address is not.

## The rule
- **An address names a place that retains state.** It is this module's subject. It is not the identity of a group, a content, a user, a thing, or any other domain's subject.
- **A domain does not import `MemoryAddress` to name its subject,** and a service does not take or return it for that subject. The domain's `<Subject>_Identifier` is the name, and other abstractions add that observer.
- **One retained thing still has one identity value.** Several domains that are lenses on that thing do not mint a second value and do not invent a second address to stand for it. The value is the identifier's; the address module does not supply a substitute id.
- **A human-facing string is display only.** It is never the form that is stored or compared as the id. That obligation belongs to the identifier the domain composes; this rule does not restate the identifier's members.

## Why it exists
The 2026-11-01 text of this rule told every domain to import `MemoryAddress` and to mint through this module's address service. Services then took `group MemoryAddress` as a method argument. The owner corrected that on 2026-11-17: the argument form is not how a subject is named here, and an address is a place, not every domain's id.

## Keep it or drop it
An organization may keep using an address value as a domain id and remain outside this rule, at the cost that a place and a subject are one type and a caller cannot see which module the subject follows.

## What this rule does not claim
- It does not declare `<Subject>_Identifier`. That declaration is the domain's, under the identifier rule linked above.
- It does not remove this module's mint of an address for a place, and it does not make `MemoryAddress` illegal inside this module.
- It does not list which domains are lenses on one thing. Each pair is decided where the subjects are decided, and then follows the one-value rule without a second mint.
