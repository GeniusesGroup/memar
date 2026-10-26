# Normative References — Mechanical
A mechanical task searches, counts, moves or rewrites by a rule given to it in full, so what it must not get wrong is how files and history are touched, and it reads these.

- [Content → Deleting, moving, restoring, and committing](../../../../../modules/knowledge/content/content.md#deleting-moving-restoring-and-committing) — the acts on files and history it takes only through `_host_git_cli.py` and the filesystem services, so nothing it moves or deletes is lost. `reviewed 142f0e0f0557`
- [Content → Putting text into a file](../../../../../modules/knowledge/content/content.md#putting-text-into-a-file) — how its rewrites reach a file without losing a non-ASCII character. `reviewed 3cd21f2c7971`
