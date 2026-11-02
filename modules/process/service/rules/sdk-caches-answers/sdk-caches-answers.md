---
Title: "Service Rule — A Service's SDK Is the Only Place Its Answers Are Cached"
Labels: Draft
Start Date: 2026-10-31
---
# Service Rule — A Service's SDK Is the Only Place Its Answers Are Cached
A rule of this repository, held for [SDK](../sdk/sdk.md). It applies to every consumer of a service, in every language: a widget, a page, a command, a program.

## The rule
- **The SDK of a service is the only place the service's answers are cached.** What to keep, for how long and against which invalidation signal follow from the service's own consistency semantics, so the service's developer chooses them and delivers them in the SDK ([SDK → Aggregation and the cache](../sdk/sdk.md#aggregation-and-the-cache)).
- **A consumer never caches a service's answer.** It calls the SDK function each time it needs the answer and lets the SDK decide whether the call reaches the service. It keeps no copy to serve a later need and holds no invalidation logic, since it cannot know the service's consistency semantics.
- **What a consumer holds is the state of its own operation, not the service's data.** The working values one call returned that the next call of the same operation needs are held until the operation ends ([A Widget Aggregates, a Service Does One Thing](../../../../computer/ui/rules/widget-aggregates/widget-aggregates.md)).
- **The test:** if dropping the held value and calling the SDK again would give a different or staler result than holding it, the consumer holds a cache and must not.

## Why it exists
A copy outside the SDK is a cache whose invalidation the service's developer does not know, and composed copies of several services invalidate through cross-model logic nobody owns. The owner ruled on 2026-10-31, on the widget document, that the boundary between a widget's state and the SDK's cache must be explicit.

## Keep it or drop it
An organization may let consumers cache and remain conformant to Memar's concepts, at the cost that each consumer carries an invalidation strategy it cannot derive.

## What this rule does not claim
- It does not claim the SDK must cache: whether a service's answers are cached at all is the service developer's strategy.
- It is enforced by no check this repository runs today.
