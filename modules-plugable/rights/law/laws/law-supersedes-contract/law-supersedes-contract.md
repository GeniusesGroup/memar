---
Title: "Law supersedes contract"
Status: Draft
Start Date: 2026-09-23
ID: 497269
---

# Law supersedes contract
An organization may let a law take the place of a contract.

## Abstract
This statute is an instance of the [law](../../../../../modules/rights/law/law.md) type. An organization that adopts it allows a law to [supersede](../../../../../modules/identity/thing/edges/supersedes/supersedes.md) a [contract](../../../../../modules/rights/contract/contract.md). An organization that does not adopt it does not. The type does not decide.

## Introduction

### Motivation
Whether a law may put a contract out of that place is a choice of the people who live under the laws. [Contract within law](../contract-within-law/contract-within-law.md) is the other choice: a contract still binds its parties unless it explicitly contradicts a law in force, and it does not replace the contract node.

## Explanation

### Definition
Where this statute is in force, a law may supersede a contract: `(law)-[:supersedes]->(contract)`. The contract stays in the graph. It is no longer the arrangement in that place.

Where this statute is not in force, a law does not supersede a contract. The contract's own parties remain the ones who can replace it.
