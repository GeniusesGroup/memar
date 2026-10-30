# Task Rule — Sub-agents run one at a time
Status: Draft

## The rule
Sub-agents run one at a time, each to its end, unless the owner asks otherwise; and a sub-agent starts no sub-agents of its own.

## Why it exists
Several at once spend the owner's usage limit together and are all cut off midway, leaving half-made edits.

## How a check would run
Two sub-agents of one task running at once, or a sub-agent that started another, break the rule. Moved on 2026-10-26 from the Memar skill (task 20261026-T120341Z-16244); this repository runs no automatic check of it today.
