---
Title: "Address Rule — Identifiers Are Memory Addresses"
Start Date: 2026-11-01
---
# Address Rule — Identifiers Are Memory Addresses
A rule of this repository, held for [Memory Address](../../address.md). It applies wherever a domain mints or names a retained thing by id. It is held by Address because an address is what names a place that retains state, and every domain that needs only a lens on that place follows this module's mint rather than declaring an id type of its own.

## The rule
- **A new identifier is minted as a memory address**, through this module's mint abstraction (`Address_Mint.Mint` → `MemoryAddress`), not as a `ThingUUID` or any other domain's private id type. Every domain follows that one abstraction.
- **The concrete way to mint is each organization's choice.** The abstraction is required; the algorithm, length and encoding of the bytes are parameters of the realization (kernel-neutrality: the subject is “an address is minted”; which bytes an organization picks does not change what an address means).
- **What is kept is bytes.** A machine reads the identifier as a byte string. A human-facing string of an address is display only and is **never** the form that is stored or compared as the id.
- **One retained thing has one address.** When several domains are lenses on the same thing — for example a thing and the order placed on it, or a thing and its members — they use **that one address**. A second address for the same thing is forbidden: it duplicates work (membership, placement, references) and invents an identity where none exists. A domain that is only a lens declares no competing id type; it imports `MemoryAddress` and attaches its parts and edges to that address ([Modularity → A Concept Has One Owner Module](../../../../../knowledge/modularity/rules/one-owner/one-owner.md)).
- **Two different things keep two addresses,** and the relationship between them is an explicit edge. Sharing an address is not a convenience for unrelated subjects ([Modularity → One Term, One Identity](../../../../../knowledge/modularity/modularity.md#one-term-one-identity)).
- **Which lenses a thing carries is settled per case,** not by a fixed list here. Instances already ruled: a thing's address is the address of the order placed on it and of the members it has. Further pairs are recorded where they are decided, and then follow this rule without re-asking whether a second address should be minted.

## Why it exists
The owner ruled on 2026-11-01 that making every identifier a `ThingUUID` was wrong from the start: domains need one shared mint structure under memory, as an abstraction whose concrete bytes each organization chooses, and machines must not treat a human string as the kept id. The same day, a redesign of a stored shape required that a thing, the order placed on it and its members share one id so membership is not done twice. Both claims live here so agents do not re-ask them per domain.

## Keep it or drop it
An organization may mint domain-private ids and map them, or keep a string form as the stored id, and remain outside this rule, at the lasting cost of duplicate membership and reference work, of sync between maps, and of treating a display string as identity.

## What this rule does not claim
- It does not pick the organization's mint algorithm or the byte scheme of the address.
- It does not list every domain pair that shares an address; each pair is a finding about whether the subject is one thing or two.
- It does not replace a module's `Type_UUID` (the stamp of a stored shape under [module-replacement](../../../../../knowledge/modularity/rules/module-replacement/module-replacement.md)).
- It does not by itself rewrite every existing `ThingUUID` field; migration of each domain is that domain's work once it imports `MemoryAddress`.
