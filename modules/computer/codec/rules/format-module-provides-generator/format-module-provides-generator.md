---
Title: "Codec Rule — Format Module Provides Generator"
Labels: Draft
Start Date: 2026-11-10
ID: 498421
---
# Codec Rule — Format Module Provides Generator
A rule held for [Codec](../../codec.md), beside [Format Adjuncts](../format-adjuncts/format-adjuncts.md).

## The rule
- **Every format that Memar adds under `modules/computer/codec/` (or as a registered format capability) offers a realization of [`Generate_Format_Adjunct`](../../services/generate-format-adjunct/protocol/generate-format-adjunct.kh).** That service writes or completes the encode/decode methods in the type’s `<base>.codec.<format>.kh` companion ([Format Adjuncts](../format-adjuncts/format-adjuncts.md)).
- **A format module that ships only a prose document or only a runtime library, with no generator service for the languages it claims to support, is incomplete** and may not be treated as a registered Memar format path.
- **Syllab’s existing Go generator** under `modules/computer/codec/syllab/services/go-methods/` is a **precedent realization**, not a second contract: new formats satisfy the same `Generate_Format_Adjunct` surface (or an explicit bind that maps their service onto it). Language-specific details stay inside the realization; the adjunct path and format name stay on the shared request/response types.
- **The generator does not own store, medium, or display seams.** It only produces structure↔format methods for seam (a).

## Why it exists
Without a required generator service, each format invents a private way to attach encode/decode to types, and agents stop at prose rules that no tool can apply. Owner (2026-11-10), task `20261110-T102002Z-25056`.

## What this rule does not claim
- It does not require every type in the repository to already have every format’s adjunct.
- It does not require one generator implementation language; each format supports the languages it claims.
