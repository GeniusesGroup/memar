# Agency Rule — Context size opens a new chat late, and only from a reported figure
Status: Draft

## The rule
- **The threshold is a fraction of the window: past about half of it.** It is never an absolute number of tokens, because what a model holds well depends on the model.
- **It is decided only from a figure the runtime reports.** Where the runtime reports none, the agent neither estimates nor computes one: it carries on until a compaction happens or the runtime reports a figure, and spends no effort on deciding whether to continue.
- **Below about a third of the window a new chat is never opened because of context size.** A chat opened for another reason is unaffected.
- **Memar's own context counts in the window.** Memar usually puts a large context, about 100K tokens, into every chat; that base is part of the window and is no reason to leave early. A new chat pays the whole context again ([the prompt cache](/.agents/skills/memar/SKILL.md#context-window-and-compaction)), so leaving early is a cost.
- **Past the threshold the agent takes no further step locally:** it hands what remains of the task to a new chat on this same task with a new plan content, or delegates where Delegation allows a sub-agent. A limit of the context never opens a new task ([Later work returns to its task](/modules-plugable/management/task/rules/later-work-returns-to-its-task/later-work-returns-to-its-task.md)).

## Why it exists
An agent once opened a new chat at what it guessed was half a window that was in fact far larger. A fraction of a reported figure removes the guess, and the floor keeps the mistake from repeating.

## How a check would run
A chat that opened a new chat on context size with no reported figure, or below a third of the reported window, breaks the rule; this repository runs no automatic check of it today.
