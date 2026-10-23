---
Title: "Claims"
Status: Draft
Start Date: 2026-09-23
ID: 497268
---

# Claims
Optional kinds of dispute. Not the case type.

## Abstract
A [case](../../../modules/rights/case/case.md) is the dispute node. A kind of dispute is an edge an organization includes. Theft, kidnapping, an illegal thing, annulment of a later law, and annulment for an update are edges in this module. They are not fields of the case type, and they are not one module each under rights.

## Introduction

### Motivation
The case domain had already collected particular accusations beside the dispute node. A new accusation was then added there, on the strength of that collection. The collection was the mistake. The node is what a legal action points at. The kind is optional.

## Explanation

### Definition
Each document under `edges/` is one kind: `(case)-[:…]->(…)`. The case node stays in the case domain. An organization that does not hear a kind leaves that edge out.

The edges here now are stolen, kidnap, illegal, annul-law-for-conflict, and annul-law-for-update. [Settlement for](../../../modules/rights/case/edges/settlement_for/settlement_for.md) is still on the case domain: it names what a dispute settles, not a particular accusation. Whether it belongs with these kinds is open.

## Phase 0 draft

A petition is the order among cases. That order is its own reason, and links between claims are pluggable. A complaint (shekvaieh) is a claim-type [label](labels/complaint/complaint.md). It groups claim types, plus the text explanation a type already carries. It is not a node and not a kind. This module does not gain a petition edge or a complaint edge.

[Registry inquiry](edges/registry-inquiry/registry-inquiry.md) is its own claim, like any other. It is not a draft-gate that must exist before other cases. It is optional in the same way as the kinds above. An organization that does not inquire leaves it out. The claimant must prove the need. The result is an information package. The requester does not receive the underlying records.

Kidnap is an edge from the claim or case to the kidnapped user. It stays. Stolen stays an edge of that kind of claim. Illegal and both annul-law edges stay. Nothing in this draft deletes them or redraws them into the defendant edge. A pluggable module may attach a process when a kidnap claim arrives. Civil versus criminal is a label, not a different adjudication model. Execution is a compelled service whose input is not only a number. Those two words stay unregistered under [claim labels](labels/labels.md). Which labels an organization uses are pluggable. Registering the two words is not required to keep one adjudication model.

After a ruling exists, a third party's attack is a new case, and the claim type is annulment of that ruling. During the proceeding, a third-party objection is a linked claim heard together. Each of those reasons is its own edge. There is no generic edge meaning only that two claims are related. The edges are pluggable, and they are not drawn in the kernel. A vote on one case is never a vote on the other. A claim has one defendant.
