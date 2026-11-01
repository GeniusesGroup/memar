# Task Rule — A task is compared with the others by everything it holds, by a comparer widget
Status: Draft

## The rule
A task's likeness to the others is judged mechanically, from everything either holds: title, plan, messages and the documents they name, never from titles alone. A machine's cost is cheaper than the cost of workers, so no part is left out to save it. The judging is asked of the text domain, which ranks and finds words ([finding words belongs to text](../text-owns-search/text-owns-search.md)); the task domain hands over what a task holds and understands none.

**Scale.** The design is for an organization with millions of tasks, not hundreds: no pass reads every task, and a rebuild per call is refused. The text domain keeps what ranking needs as a structure it updates when a text is made or changed (an event), not as a file beside the documents, and a query reads the structure. The ranking is normalized, so a likeness means the same in every call. Cost is measured on the existing tasks and on a synthetic corpus of a million before any threshold binds a maker.

**Single responsibility.** A base service does one thing. The comparer ranks: given a text it returns other tasks' ids with a likeness each, excluding the task itself and its relatives (parent, children, siblings made on purpose). Showing the result is the work of a widget, an aggregate of services, and a widget may show what several services answer, a task's status among them (the status is the answer of the service that owns status). The comparer widget is the aggregate "comparer": the comparing service, the status service and the display.

**Where it meets a maker** (a user is a human or an intelligence, and each meets the widget through the interface its kind uses):
- A human meets it in the GUI form as the title and text are typed, before the task exists. A Complete task is cited as done before, not closed as a duplicate.
- An intelligence meets it in the process that makes a task. The first build prints the ranked ids and holds nobody. A gate that holds the maker until a hit is continued or named as the reason the task is not a duplicate is added only after it is tested on the existing tasks and shown not to hold series or siblings.
- An event after the task is made, for a maker that never met the widget, is a separate plan item with its trigger and author named. A relation it proposes is `same_ask`, and who creates and removes it is named ([relations between tasks](../task-relations/task-relations.md)); it closes nothing by itself.

**The making process is split.** `ensure` does several things today; it becomes several single-purpose services (find or make the folder, write the plan, set labels and priority, and so on) and widgets that compose them, and the comparer is one of those widgets, in a pluggable module and not in a kernel module. The kernel never calls a pluggable module; a composing layer calls both.

## Why it exists
Opened tasks overlap, and an agent told to open a task for independent work has only its memory to judge independence by. Reading everything catches a repeat a title hides; keeping the structure up to date keeps the cost where the growth is.

## How a check would run
A fixture of a few tasks: a repeat is ranked first; an unlike task is not returned; a repeat found only in a message is returned; a repeat written in Persian is found; the task itself and its relatives are not returned; the comparing service's output holds ids and likeness and no status. Then the same on the existing tasks, and a timing on a corpus of a million. The statement is the owner's (2026-10-30, task 20261030-T073507Z-6324, three rounds of corrections), recorded in [Task](../../task.md#a-new-task-is-compared-where-it-is-made-and-after-it-exists); this repository runs no automatic check of it before the service is built.
