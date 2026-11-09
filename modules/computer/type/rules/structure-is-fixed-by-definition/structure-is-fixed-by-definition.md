---
Title: "Type Rule — Structure Is Fixed by Definition"
Labels: Draft
Start Date: 2026-11-09
---
# Type Rule — Structure Is Fixed by Definition
A rule of this repository, held for [Type](../../type.md), for the operational checks of [Structure Is Fixed by Definition](../../type.md#structure-is-fixed-by-definition). It applies when designing, reviewing, or accepting a mechanism that runs after a system is realized.

## The rule
- **A running system executes its definition and never establishes structure.** Capabilities and constraints are fixed at definition time by the Types the definition declares. An instance holds values of those Types; it does not mint concepts, raise capability, or change constraints.
- **Selection among established alternatives is execution, not structure change.** Dispatch in a closed set fixed at definition time may run at runtime; the set itself may not grow while the system runs.
- **Runtime inputs are data.** User text, payloads, and parameters whose vocabulary is itself a defined Type exercise the definition; they do not extend it.
- **Consuming a platform or another system is not acquiring structure.** Calls through interfaces this definition names exercise the other party's Structure, not a change to this one.
- **Refuse registries, plugin loaders, and dynamic concept admission that introduce Types or capabilities only after start** unless every admitted concept was already a defined Type and the admission is selection among them.

## Why it exists
The Explanation states the principle; this rule is what get-rules-for-subject can hand an agent when the act is implementation or review. It is the structural twin of [Explicit Behavior Ownership](../explicit-behavior-ownership/explicit-behavior-ownership.md).

## Keep it or drop it
An organization may allow runtime structure minting and remain outside this rule; it then accepts identity and capability demoted to encountered data.

## What this rule does not claim
- It does not own deployment or configuration tooling; those realize this type-level rule in their own documents.
- It is enforced by no check this repository runs today.
