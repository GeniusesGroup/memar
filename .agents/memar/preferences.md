---
sessions:
records:
---
# Memar preferences
This file is this project's own: `memar install` creates it when it is absent and never rewrites it, unlike the README beside it, which an install rewrites. The front matter holds what Memar's tools read. `sessions` is the folder new session folders are made in: a path relative to the project's top folder, or an absolute one, but neither that top folder itself nor a drive or filesystem root; left empty, they are made in temp/sessions/ inside the project, which its VCS should ignore (for Memar itself, its own temp/sessions/). Memar's daily sweep never touches a session folder made in the `sessions` folder: keeping, committing, or deleting it is the project's. `records` says whether a session's records — its whole folder except the claim, caches, binary files, files over 256 KB that are not documents, and its own temp folder — are kept on the branch dev-knowledge of the project's own repository, at .agents/sessions/<id>/ there, by `memar session archive` (and added by the sweep before it moves a folder): `on`, `off`; left empty, they are. Nothing is pushed. Below this paragraph, write any preference agents should follow on this project.

## Not every idea belongs in Memar
The owner's note (2026-10-13): an idea that needs concepts Memar does not define (a Task, a User, an AI model, how a model is chosen or how agents are run) most likely belongs in the `organization` repository, whose job includes how models work, not in Memar. When such an idea turns up, say so, and either raise it in the organization repository or open a queued session there for it, so it is not forgotten; do not write it into Memar as a patch on someone else's approach.
