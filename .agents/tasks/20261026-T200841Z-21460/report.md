---
ID: 20261026-T200841Z-21460
Title: Rules that make every task develop abstractions first in Khayyam, tests before code, and keep documents free of code; enforce them in the Memar skill
Status: Complete
---
# Report

## What ran
Read the rules folder, the skill, `A Fact in Code Is Written Once`, `detail.kh` and the memory-layer output. Wrote seven rules (abstraction first, errors folder, no comments, documents restate no code, tests first and scoped, lowest model in a delegation, refused hand-back), committed as 11567d080ced. Wrote the audit `docs/audit-memory-layer-output.md`. Cited the rules in `.agents/skills/memar/SKILL.md` and in `memar task ensure --help` (source `modules/management/task/services/new.py`). A fresh sub-agent (sonnet, kind critique; the rules are reviewed by the owner too) reviewed them; its findings were applied except the ones listed below. Models: this task ran on sonnet 5.5, standard level.

## Check
`memar content check` on the rules and the audit: 0 problems. `memar task ensure --help` prints the new citations; `new.py` compiles. Its tests were not run.

## Result
Rules committed. NOT committed: `SKILL.md` and `new.py` carry uncommitted edits of another task besides mine, so they must be committed with that task's. The audit and this task folder are not yet committed. Not done: citing the rules in the normative-reference lists (they need `reviewed` marks and are the owner's), the carry-out brief (`modules-plugable/ai`, another task's uncommitted files), a pinning test for the rule constants in `new.py`.

## Left open
## Decisions needed
- Does the no-comment ban bind Python docstrings and comments too? (written: yes, until he rules)
- Which module owns a test runner that reads `BUDGET_SECONDS` and stops a run over it? None exists.
- Add the rules to the Implement/Plan normative lists (with review marks)?
