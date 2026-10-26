# Task Rule — A delegation states who checks the result and names the lowest model that is enough
Status: Draft

## The rule
[The need rule](../model-follows-need/model-follows-need.md) decides the level; this rule adds only that the plan of a delegated task states who checks the result and how deeply, that the delegation names the level when the sub-agent starts, and that one that names the strongest level says in the plan which of the need rule's three facts raised it.

## Why it exists
Every delegation of the memory-layer task (20261023-T074642Z-5420) ran on the strongest model, though the delegating agent and the owner reviewed each result. The need rule already forbids it; this rule makes the plan show the answer.

## How a check would run
Read each delegated task's plan for the line stating who checks, and compare the model its report says ran with the level that line gives. This repository runs no automatic check of it today.
