# Task Rule — The model a task runs on follows what the task needs
Status: Draft

## The rule
- **A task runs on the cheapest reasoning model its need allows, and no stronger.** Choosing a model too strong for the work is the same fault as choosing one too weak: it costs the owner for no better result. The need is judged from three facts, in this order, and never from the task's kind alone:
  1. **Who checks the result, and how deeply.** A result the owner reviews, or a later step that a fresh reviewer carries out, lowers the need: a flaw is caught there. A result nobody checks raises it.
  2. **How open the judgment is.** Carrying out a settled design, or applying a rule already written, needs less than deciding what the design or the rule is.
  3. **What a wrong result costs if it goes unnoticed.** A result that other work builds on, or that is hard to undo, raises the need.
- **The levels are named by what the model can do, not by a product.** From lowest: *small* (search, count, move, rerun a script, and carry out a written operational plan step by step, which even the smallest model can do when a stronger one made the plan and its result is checked), *standard* (reasoning beyond a stated plan, or judgment whose result is checked), *deep* (open judgment whose result nobody checks and whose error is costly). No document or tool in Memar names a product or a version.
- **The kind is a starting point, not the answer.** A `mechanical` kind starts at mechanical; every other kind starts at the lowest level its plan allows: a task that carries out a settled, written plan starts at small, and nothing makes standard the default; the level moves up only by the three facts above; deep is chosen only when the plan says no one checks the result and an error is costly, or when the owner asks for it.
- **The plan states the facts.** Whoever writes or queues the plan says in it, in a line, who checks the result and how deeply; the agent that takes the task up reads the level from it. A plan that states nothing is read as: the owner reviews.
- **A plan that states no kind** is read from its Request: if the Request decides what a design or a rule is, or critiques, the agent ends Blocked saying the plan states no kind, for the delegator to state it; otherwise it starts at the lowest level its facts allow.
- **A model that is not available is not chosen.** A stronger model that is refused (no credits, a limit) is not available; the task goes on with the best usable one, and the report says which model ran.
- **An agent that judges its own reasoning too weak for the task** writes, in the report, that and why, names the level it ran at and what it lacked, ends Blocked, and asks for another agent to take the task up one level above.
- **The rule is written once, here.** The skill, the contexts that tools print, the help of a command, and the kinds cite it and print no level of their own beyond what the plan carries.

## Why it exists
A fixed model for a kind made agents pick the most costly model whether or not the result is checked afterwards. The owner reviews design and critique results in person, so the extra cost bought no better outcome; the need is what the task's own checking leaves unchecked.

## How a check would run
Search the skill, the contexts and helps that tools print, and the task kinds' documents for a sentence that fixes a model level by kind alone ("strongest", "cheaper", "deep" tied to a kind word); each is a defect unless it cites this rule. `memar content check` reports a citation whose link is broken.
