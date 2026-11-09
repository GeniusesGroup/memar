---
Title: "Modeling Rule — Shared Relation Placement"
Labels: Draft
Start Date: 2026-11-09
---
# Modeling Rule — Shared Relation Placement
A rule held for [Modeling](../../modeling.md), for placing a relation that may span domains.

## The rule
1. Name the relation independently of the event that raised it and search the graph for an existing relation with that meaning.
2. Ask which other domains need the same relation.
3. When several domains need it, define it once in the domain that already covers every record those domains are; otherwise keep it in the one needing domain.
4. Let each domain retain its own rule for when its records take the shared relation.

## Why it exists
One relation owned by several domains becomes several competing edges for the same concern.
