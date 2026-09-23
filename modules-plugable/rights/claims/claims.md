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
