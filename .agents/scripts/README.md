# Scripts
This file is the work instruction for a session that reaches Memar without the `memar` command: how Memar is installed, and the rules a session follows when it deletes, moves, restores, or commits anything, or puts text into a file. A session that has `memar` needs it only for those acts. What a file here accepts is declared by the file itself — `-Help` for [`install.ps1`](./install.ps1), `--help` for [`install.sh`](./install.sh) and for every command — and what it is for and why, by its opening comment; ask them, not this page.

## Installing Memar — onto a machine, then into a project
1. Fetch the bootstrap into a file: [install.sh](https://raw.githubusercontent.com/GeniusesGroup/memar/main/.agents/scripts/install.sh) on POSIX, [install.ps1](https://raw.githubusercontent.com/GeniusesGroup/memar/main/.agents/scripts/install.ps1) on Windows. In a Memar checkout the same two files sit beside this README.
2. Read its opening comment before running it, and ask it for its help — `install.ps1 -Help`, `install.sh --help`.
3. Run it only as that comment and that help say.

The bootstrap obtains the checkout and hands it to `memar install` ([the installer](../../bundles/memar/install/install.py)), which settles the machine, the project it is told with `--project NAME` or `--project-path PATH`, and the agent apps. Whatever else Memar needs and the machine lacks — Python, git — comes through the bootstrap as well; if it cannot supply it, stop and say so.

One environment variable holds the path of the Memar checkout, and everything that needs Memar reads it; nothing guesses a location or keeps a second copy. `memar install --root` prints it. Where a checkout exists but `memar` is not on the path, run `python <checkout>/.agents/scripts/memar <verb>`.

A web chatbot can be given Memar only as a skill file or pasted text, from [`../skills/memar/`](../skills/memar/); no script covers that case.

## Deleting, moving, restoring, and committing
The [`host/`](./host/) shelf wraps tools the machine already has with the constraint a session improvises past: [`host/fs.py`](./host/fs.py) for the filesystem, [`host/git.py`](./host/git.py) for version control. Both are run with Python by their path inside the checkout; neither is a `memar` verb ([`host/README.md`](./host/README.md) says why).

- Deleting, moving, discarding, stashing, restoring, and committing go through those two files, each asked for its own `--help`, so the act stays recoverable.
- Never the host's own command for those acts — `rm`, `Remove-Item`, `git rm`, `git restore`, `git checkout` of paths, `git clean`, a plain `git commit` — and never a command a runtime rewrites.
- In a working tree other sessions share, commit only this session's paths. The records of the task's sessions are not among them: `memar session archive` keeps them on the records branch.
- Every commit names the sessions it carries out, with `--session-id` for each; the message itself names none. A commit that carries out none says `--no-session`.
- One session task gets one commit, made by the coordinating session after the human approves; a sub-agent never commits. A finding after the commit is folded into it. A move rides with the commit as long as each moved file stays above git's rename threshold; otherwise the move is committed first, alone.
- When a commit stops partway, do what its message says, with one of the two commands it prints. Never delete a lock file to get past one.
- Every `host/git.py` verb that acts on a repository takes it with `--repository PATH` and never reads the folder it is run from.
- If those files are not at hand or do not cover the act, stop and say so.

## Putting text into a file
Text reaches a file through a file-write tool or `memar content write` and `edit`, never through a shell's own text handling — redirection, `echo`, `Set-Content`, a read-then-write round trip — which loses non-ASCII characters without a trace. Where another session may write the same file, use the `memar content` verbs: they take the per-file lock.

## Maintaining this folder
For whoever adds, renames, or removes a file here.

- **Nothing is said here that a file or its `--help` already says.** The owning file carries its own why, `--help` carries only what a caller needs; a second copy drifts.
- **Everything here is provisional** and is eventually code in modules, in Khayyam. Python written here is written as Memar would write it — one service one file, a fact declared once in a type — so that the conversion changes syntax only.
- **The CLI surface is provisional** too: Memar is moving toward a server agents converse with, reached through [sRPC](../../modules/net/srpc/srpc.md), and through MCP only by the [guest adapter](../../modules/knowledge/classification/classification.handoff.md#mcp-as-a-guest-adapter).
- **A one-time migration is never a file here.** It lives in the `services/` folder of the session that does the change.
- **A file that grows past the mark** is split by concern, not the mark raised; [`tests/script_size.py`](./tests/script_size.py) holds the mark.
- **The project registry and Khayyam's dependency management are developed only together;** nothing is added to either before they are one ([the open question](../../modules/knowledge/documentation/handoff/handoff.handoff.md#khayyams-dependency-management-and-memars-project-registry-one-design-and-nothing-added-to-either-before-it-exists)).
- **A script is told its project** with `--project NAME` or `--project-path PATH`, declared once in [`find.py`](../../modules/process/project/services/find.py), and never reads the folder it was started in. A verb that does is a defect.

### The shelves
A file's shelf is decided by what it belongs to, not by who calls it.

- **The top** is what is reached from outside: the router [`memar`](./memar) with `memar.cmd`, the bootstraps and this README. The router knows no verb, no argument and no help text.
- **The verbs live in modules** under [`modules/`](../../modules/), [`modules-plugable/`](../../modules-plugable/) and [`bundles/`](../../bundles/), each a folder with a file of its own name and a `services/` folder of capabilities. The router finds them by walking those three roots and this folder, which holds one provisional module until it has its place: [`mcp/`](./mcp/), the MCP adapter, bound for `modules-plugable/net/mcp/` ([the guest adapter](../../modules/knowledge/classification/classification.handoff.md#mcp-as-a-guest-adapter)). No module imports a module that imports it back ([`tests/module_graph.py`](./tests/module_graph.py)).
- **[`machine/`](./machine/) and [`host/`](./host/)** are what modules share. `machine/` is the machine's, not Memar's. A type belongs to the `primitive/` folder of the module of its subject.

Each shelf and each module keeps its own `tests/`; the top's [`tests/`](./tests/) checks the router and what spans every module. The folder states the role, so a file's name does not.
