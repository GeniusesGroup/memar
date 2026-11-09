---
Title: "Modeling Rule — Relationship Audit"
Labels: Draft
Start Date: 2026-11-09
---
# Modeling Rule — Relationship Audit
A rule held for [Modeling](../../modeling.md), for auditing every edge and loop-edge.

## The rule
1. Verify that the relation joins independent concepts rather than data or a disguised classification.
2. Verify that it does not hide a rule or constraint.
3. Justify its cardinality and direction.
4. When it is a shortcut, prove that it remains derivable from existing authoritative edges.

## Why it exists
Relationships are architectural claims. Auditing them prevents a graph from hiding data, policy, or an untraceable second source of truth in an edge.
