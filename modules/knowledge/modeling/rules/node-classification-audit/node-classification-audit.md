---
Title: "Modeling Rule — Node Classification Audit"
Labels: Draft
Start Date: 2026-11-09
---
# Modeling Rule — Node Classification Audit
A rule held for [Modeling](../../modeling.md), for auditing a node's structural role.

## The rule
- **Classify every node as an independent concept, a relationship mistaken for a node, data mistaken for a node, a loop-edge or classification mistaken for a node, or mixed.**
- **Flag unclassifiable, mixed, and misclassified nodes.**
- **Decompose a mixed node into separate nodes joined by an explicit relationship.**

## Why it exists
A node earns its role from responsibility and relationships, not from the presence of a label or data.
