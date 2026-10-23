---
Title: "Law — optional parts"
Status: Draft
Start Date: 2026-10-20
ID: 497910
---

# Law — optional parts
The optional parts an organization attaches to the [law](../../../modules/rights/law/law.md) type, held as one pluggable module.

## Abstract
The law type is kernel; what an organization may choose otherwise about law sits here, in one module that is installed and removed as one unit. Its parts are the words commenters attach to laws ([labels](labels/labels.md)), the laws the law domain introduces by its own rules ([laws](laws/laws.md)), and validity, one or more edges that raise a law's identity ([validity](edges/validity/validity.md)). The rule domain's rules written and run under law take a `rules/` part when the first one exists. Which parts and which words an organization takes is configuration inside this module, not a module each. This module restates nothing of the law type.

## Introduction

### Motivation
The parts stood as siblings of one another under `modules-plugable/rights/` (`law-labels`, `law-validity`, `laws`), each removable alone, so nothing said they were one capability of one kernel type, and a part stood beside the module it is a part of. The owner ruled on 2026-10-20 that they are one module with one removal unit, named for the kernel module whose optional parts it holds ([Modules Research 001 → Owner decisions needed](../../../.agents/tasks/20261019-T191746Z-12632/docs/modules.research.001.md#6-owner-decisions-needed), D1 to D3; [Pluggable → Operational rules](../../../modules/knowledge/modularity/labels/pluggable.md#operational-rules)).

## Explanation

### Definition
- A part is never a module of its own: it has no manifest, and its removal is the removal of this module or a configuration of it.
- `rules/` holds rules of the rule domain, and `laws/` holds laws; a rule and a law are different subjects, so neither folder holds the other's.
- Validity is a relation of a law, not a rule, so it is an edge under `edges/`.
- The module's manifest is [`law.manifest.yaml`](law.manifest.yaml).

## Related Artifacts
- [Law](../../../modules/rights/law/law.md) — the kernel type these parts attach to (Depends_on)
- [Law Handoff](../../../modules/rights/law/law.handoff.md) — the type's working state and the ruling that placed these parts here (Related)
- [Claims](../claims/claims.md) — optional kinds of dispute, a separate module (Related)
