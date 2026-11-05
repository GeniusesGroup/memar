# Normative References — Mechanical
A mechanical task searches, counts, moves or rewrites by a rule given to it in full, so what it must not get wrong is how files and history are touched, and it reads these.

- [Filesystem Practice → Deleting, moving, restoring, and committing](../../../../../modules-plugable/computer/memory/filesystem/filesystem.practice.md#deleting-moving-restoring-and-committing) — the acts on files and history it takes only through the `memar git` verbs and the filesystem services, so nothing it moves or deletes is lost. `reviewed e64286aae6ea`
- [Modularity Rule — A Refactor Moves in Order → The rule](../../../modularity/rules/refactor/refactor.md#the-rule) — a move is a pure move, its importers are found and repointed in one batch with the old path alive, and only unit tests run until the last step. `reviewed b235f30aee30`
- [Filesystem Practice → Putting text into a file](../../../../../modules-plugable/computer/memory/filesystem/filesystem.practice.md#putting-text-into-a-file) — how its rewrites reach a file without losing a non-ASCII character. `reviewed e99cd2662e2d`
