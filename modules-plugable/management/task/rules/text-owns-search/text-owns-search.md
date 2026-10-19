# Task Rule — Finding words belongs to text
Status: Draft

## The rule
Neither Task nor content understands text. Finding a word or a phrase, and any retrieval over text such as BM25, belongs to the text domain. The service that loads what a worker found into its context has no domain yet; the domain is created first.

## Why it exists
A domain that does not understand text must not search it.

## How a check would run
A Task or content document that specifies search or ranking of words breaks the rule. The statement is the owner's, recorded in [the Task handoff](../../../../../modules/management/task/task.handoff.md#owners-answers-to-the-six-questions-2026-10-18); this repository runs no automatic check of it today.
