# Documentation Rules (`modules-plugable/knowledge/documentation/rules/`)
Rules for the conditions a document is held to. The general Memar concept of Rule is defined in [`modules/process/rule/rule.md`](../../../../modules/process/rule/rule.md); a Rule is held by the module that owns its subject ([Rule → Which Module a Rule Belongs To](../../../../modules/process/rule/rule.md#which-module-a-rule-belongs-to)).

| Rule | Subject | Tier | What it is |
| --- | --- | --- | --- |
| [A Document Restates No Code](./document-restates-no-code/document-restates-no-code.md) | What a document may say of code | Governance | A section that only describes a file's members is a copy and goes |
| [No Record Is Written Beside a Document](./no-record-beside-a-document/no-record-beside-a-document.md) | Where a change, a decision or a question is kept | Governance | A record is a content on a task's timeline, never a file beside the document |
| [A Rejected Position Leaves the Body](./rejected-position-leaves-the-body/rejected-position-leaves-the-body.md) | What a body says of a replaced formulation | Governance | The body states what holds; a rejected position is deleted and its alternative goes to a decision's Options |
| [No Derivative Inventory](./no-derivative-inventory/no-derivative-inventory.md) | What a document lists and what the doer reads | Governance | A pointer file lists no collection, and the doer enumerates no document set the task does not need |
| [A README Is a Link to the Main Document](./readme-is-a-link-to-the-main-document/readme-is-a-link-to-the-main-document.md) | The README of a folder | Governance | With a main document the README is a symbolic link to it (mode 120000), without one a real file |
| [A Template Document and Its Rules Trace Both Ways](./spec-and-procedure-trace-both-ways/spec-and-procedure-trace-both-ways.md) | The match between a template document and its module's rules | Governance | A mismatch in either direction is a defect in one of the two |

The Rules are governance-tier and is enforced by no check this repository runs today; an organization adopting this repository's Rules may keep, relax, or replace it without forking anything.
