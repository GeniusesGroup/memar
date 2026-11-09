---
Title: "Modeling Rule — Implementation Contamination"
Labels: Draft
Start Date: 2026-11-09
---
# Modeling Rule — Implementation Contamination
A rule held for [Modeling](../../modeling.md), for separating the domain model from a technical source.

## The rule
- **Check whether database tables, UI screens, API shapes, or framework and language features have been treated as domain constraints.**
- **When contamination is found, separate the parts that model reality from the implementation concern that leaked into the model.**

## Why it exists
An implementation-shaped model preserves the limits of a current mechanism rather than the responsibilities and relationships of the domain.
