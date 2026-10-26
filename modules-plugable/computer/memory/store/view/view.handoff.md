# Memory View Handoff
Open work for `view.md`. Entries are mutable current state, revised as each item moves and removed when it resolves or is dropped. See [handoff.md](../../../../knowledge/documentation/handoff/handoff.md) for what a handoff is.

## Topic & Purpose
What the build of the view decided where no abstraction gave a name or a rule.

## Status
Active. Built by task `20261026-T192807Z-36152` (step 4 of `20261023-T074642Z-5420`); no presentation is registered yet, so `memar view refresh` refuses every class until the task module registers the Task's (task `20261023-T074643Z-5420`), and Memar's own manifest has no `view` line until the migration (P4).

## Decisions
Each is **Tentative**: taken by task `20261026-T192807Z-36152` where the code needed a name or a rule no abstraction gave, open to the owner's ruling, and each says what changing it costs.
- **The verb is routed by the router's own discovery, not by a line in the entry point.** The plan said the verb is declared in the router of `bundles/memar` the way `open` was. `open` is a function the router binds by one line; a verb is declared by its module's `describe`, and the router's test `RouterNamesNoVerb` refuses any string of the router holding a verb word, which a line naming `bundles.memar.services.view...` would. So `bundles/memar/services/view/view.py` declares `memar view` and `services/refresh.py` its sub-verb, which the router finds as it finds `resident` and `mcp`. Changing it costs the module's place.
- **A presentation is a function from a `Node` (an id and the bytes of each part by domain key) to relative paths with forward slashes and their bytes, registered by `register(class_name, presentation)`.** The document says a function from a node to paths and bytes; no abstraction of Memar names the node a presentation is handed, so `Node` is declared in [`view.py`](view.py). Changing it costs the presentations.
- **The list of the files the builder wrote is `.memar-view` in the folder, one line per file holding the SHA-256 of its bytes and its path.** The token is the store's own (SHA-256), so a file changed by hand is told from one whose node changed: drift is a file whose bytes are not the ones the list says were written. The list is read-only like the rest. Changing it costs one name and a rebuild of every view.
- **The folder is refused when it is the top of a working tree, or inside one that does not ignore it, asked of `git check-ignore`.** The document says a folder version control does not ignore; git is the version control of every Memar project today, so the builder asks git and nothing else, and a folder outside any working tree is accepted. Changing it costs one function.
- **Files the presentation no longer gives are removed, with the folders they leave empty.** The document says the builder touches only the files it wrote; removing one it wrote and no node shows keeps the view a function of the state. Changing it costs one loop.
