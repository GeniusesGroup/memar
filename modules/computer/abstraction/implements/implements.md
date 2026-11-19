---
Title: "Implements — Tooling-Facing Implementation Intent"
Labels: Draft
Start Date: 2026-07-08
ID: 495413
---
# Implements — Tooling-Facing Implementation Intent

## Abstract
Implements is the module that owns how a type declares, for tools, which abstractions it intends to implement before structural satisfaction is complete. The contract is [`Abstraction_Implements`](protocol/implements.kh); the checkable conditions are under [`rules/`](rules/README.md). This document states only what those cannot: why the signal exists and what it is not.

## Why a tooling signal
Some abstractions expand to many methods. Scaffolding an incomplete capsule needs a reliable intent marker *before* the capsule satisfies the target structurally — satisfaction alone has nothing to detect on an unfinished type. The language adds no intent keyword; a capsule implements `DeclaredAbstractions`, whose influenced [`Abstractions`](../protocol/abstractions.kh) value receives each claimed target by `Push` from [`Container_Push`](../../adt/container/protocol/push.kh) ([Type → Implementation intent](../../type/type.md#implementation-intent)).

## What it is not
It is not runtime type safety, sealing, or a substitute for structural satisfaction. It is not composition of `Abstraction_Implements` (or of the target) into the capsule body. Organizations may lint against branching on the declaration at runtime; the contract remains with tooling.

## Where the contract lives
- Protocol: [`protocol/implements.kh`](protocol/implements.kh). The returned collection type is owned with Abstraction: [`../protocol/abstractions.kh`](../protocol/abstractions.kh) (composes `Container_Push`).
- Rules: [`rules/intent-via-implements`](rules/intent-via-implements/intent-via-implements.md).
