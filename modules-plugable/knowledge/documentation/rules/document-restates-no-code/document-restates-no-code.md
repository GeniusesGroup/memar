# Task Rule — A document does not restate code
Status: Draft

## The rule
A document of a module says what its code cannot: the reason, the trade-off, the audience and the history ([A Fact in Code Is Written Once](../../../../knowledge/documentation/documentation.md#a-fact-in-code-is-written-once)). A section whose sentences only describe a file's members — its functions, fields, signatures, cases or values — is a copy, and is removed or replaced by a link to the file. A task that writes code writes no document first that states the code's facts: the abstraction in Khayyam comes first, and the document says only what it does not.

## Why it exists
The owner found a 64-line `store.md` that restated a Python contract. A restated fact has no way back to its source, and the next change to the code leaves it wrong while nothing fails.

## How a check would run
For each section of a changed document, take the identifiers it names and look each up in the module's files; a section where every sentence names a member of one file and gives no reason, trade-off, audience or history breaks the rule. Owed: a command that does this over a module; until then a reviewer applies it, and `memar content check` does not.
