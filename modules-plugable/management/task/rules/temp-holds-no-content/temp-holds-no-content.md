# Task Rule — The scratch folder holds no content
Status: Draft

## The rule
- **A text that becomes a content of a task is not written to a file of `temp/` first,** because the MCP verbs take it directly. A task's `temp/` holds what has no content value, such as the output of a script.

## Why it exists
The owner's ruling, given in chat on 2026-11-01 while task 20261026-T200843Z-21460 was running, and recorded in the plan of task 20261101-T060801Z-24804. The reason below is the writer's inference, not the owner's: a text written to `temp/` and then posted from it leaves two copies of the same text.

## How a check would run
A file in a task's `temp/` whose body equals the body of a numbered content of the same task breaks the rule. Today nothing runs this check. Its scope is identical copies only: a text that differs, or was never posted, is not decided by it.

## Owed
Each item is owed by task 20261101-T060801Z-24804; the ids after `Owed:` are labels, not tasks. None is done.
- `memar content check` is to report the file described above. Owed: task.temp-duplicate-check.
  - The writer's specification, to be confirmed by the owner: the body is the text after the front matter block, and a final newline is ignored.
- The parameter `stdin` of the MCP verbs is to be renamed `text`, by the owner's ruling. Owed: task.verb-text-parameter.

## Open points
These are the writer's inference, not the owner's ruling. Whether the verbs keep their file options is not ruled, so neither is what follows from it.
- The ending in `get_task_init_context.py` tells the agent to post its report with `--content-file SCRATCHFILE`, a file in the task's `temp/`.
- `TEMP_SENTENCE` in [`temp.py`](../../services/temp.py) names two things `temp/` holds: a script's output without content value, which agrees with this rule, and a draft changelog record before it is appended, a case this rule does not decide.
- Whether either string is to change is open.

## What this rule does not claim
- It does not claim any owed item is done.
