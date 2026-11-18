---
Title: "Identifier"
Labels: Draft
---
# Identifier
## Abstract
Identifier owns the shared identity value and generation protocol used throughout Memar. A domain gives an identity its meaning and lifecycle; the common owner supplies its creation and comparison. This keeps independently delivered modules interoperable without an organization-specific allocation agreement.

## Introduction
### Motivation
A private allocator or truncated identity in each consumer makes the same declared concept depend on where it is used. A shared identity is retained by its subject and derived into every realization that uses that subject.

## Explanation
### Shared ownership
The shared [Identifier](protocol/identifier.kh) protocol keeps identity and its initialization under one owner, with its companion details. Type declarations, streams, calls, frames and retained instances reach the same generation owner. The domain consuming an identifier owns what it identifies, when it comes into existence and how long it remains in use.
### Definition and realization
A declared Type retains its identity in its authoritative definition. SDKs and implementations of that published contract derive it from that definition. Selecting a destination selects the organization serving the contract.
### Presentation
[The binary codec](protocol/identifier.codec.binary.kh) makes retained identity transferable through the shared Codec capability. [The optional readable companion](protocol/identifier.codec.readable.kh) serves reversible technical interchange. Localized display remains a receiving-context choice, so changing a calendar or audience leaves the retained identity unchanged. Native reference bindings live in [value.py](value.py) and [readable.py](readable.py). Consumers reuse this owner conversion when they already know the value represents an Identifier.
### Admission
The delivered SDK brings the shared declarations into the consuming bundle. [Types](../../computer/types/protocol/types.kh) supplies the catalog boundary used when the bundle checks its SDK dependency closure. Conflict checking protects the assembled executable and complements the generation contract.
