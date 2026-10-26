# Task Rule — The abstraction of a requirement is written in Khayyam, and approved, before any code of it
Status: Draft

## The rule
- **Before any code of a requirement, its abstraction is written in Khayyam.** The abstraction is the skeleton: the types, each with the methods of [`detail.kh`](../../../../../modules/computer/type/protocol/detail.kh) that say what the type says of itself; the services, as [`service.kh`](../../../../../modules/process/service/protocol/service.kh) and [`services.kh`](../../../../../modules/process/services/protocol/services.kh) declare a service and a group of them; and the errors, in the module's `errors` folder ([errors](../errors-in-the-errors-folder/errors-in-the-errors-folder.md)). A protocol or an abstraction is Khayyam, never Python and never a Markdown document; Python is a realization of an abstraction already stated, and a name first made while coding is a fault.
- **It is approved before code begins.** A fresh agent that did not do the work approves it ([a reviewer is a fresh sub-agent](../reviewer-is-a-fresh-sub-agent/reviewer-is-a-fresh-sub-agent.md)), judging it against the requirement and the governing documents; and the owner approves it too where the existing rules send the decision to the owner. The approval is a record in the changelog of the module's document, and the task's plan names it as a step that comes before the first step that writes code.
- **No code of the requirement is committed to a module before.** A commit of a module's code whose abstraction was not approved first breaks the rule, even when its tests are green.
- **Where the abstraction needed is missing from Memar,** the agent writes it in Khayyam as part of this step, or records the gap in the handoff of the document it concerns and stops; it does not invent one in the realization.
- **The order inside a requirement** is: the abstraction in Khayyam, its approval, the tests ([tests first](../tests-first-and-scoped/tests-first-and-scoped.md)), then the code.

## Why it exists
The owner found the memory-layer task (20261023-T074642Z-5420) built against Memar's own principles: its contract was written as a Python protocol and described in a Markdown document, and the Khayyam that should have stated it was not written. Khayyam is stable enough to replace the Markdown description of a contract, and an abstraction fixed in the realization is a second design nobody reviewed.

## How a check would run
For each commit of code in a module, find the `.kh` files of the module's abstraction and the changelog record that approves them, both before the code's first commit; a module whose contract exists only in `.py` or `.md` files breaks the rule. This repository runs no automatic check of it today.
