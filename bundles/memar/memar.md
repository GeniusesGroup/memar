---
Title: "Memar"
Labels: Draft
Start Date: 2026-10-07
ID: 497607
---
# Memar
## Abstract
This bundle is the home of the **Memar server**: the program through which a person or an agent works on a repository the Memar way — creating a module or a service, generating a service's SDK, building and deploying an application. It is a [bundle](../README.md) rather than a module because it runs operations that modules own rather than owning one itself. No specification of it is written yet, and nothing here realizes it yet. What the folder holds today is what `memar-go` had for that role, carried over by the port and still in its archived Go: the program's entry and command registration (`main.kh`, `init-cmd.kh`, `init-server.kh`, `const.kh`, `locale.eng.kh`), the application's lifecycle (`app/`), and the `locale` command (`locale/`). The direction this bundle is to take, and what is still open about it, are in the paired handoff.

## What belongs here
What only the server does: receiving a request for one of Memar's operations, routing it to the module that owns the operation, and answering. An operation another module owns stays in that module even when the server is how it is reached — creating a module is [`computer/module/`](../../modules/computer/module/)'s, generating a service's SDK is [`process/service/`](../../modules/process/service/)'s, and a module's error SDK is [`process/error/`](../../modules/process/error/)'s.

## The server is a release, and a chat changes release only by an explicit update
The Memar server a chat reaches is one compiled binary named `memar` in the operating system's process list, built from the modules this bundle declares in its `manifest.yaml` by the target [`targets/python`](./targets/python/), and installed as a release under `bin` of the project (owner, 2026-11-10: `bin`, not `temp/bin`, so wiping scratch does not drop the active command). The pointer `bin/current` names the release new calls start, and the scripts `bin/memar` and `bin/memar.cmd` follow it, so an agent application is registered with the script and never with a release folder. The shell's active `memar` is only that `bin` entry on PATH. Legacy `bundles/memar` PATH entries are removed on install/update. Each installed release is also mirrored under the machine's per-user data folder (`%LOCALAPPDATA%/Memar/releases` on Windows), and the shim prefers that copy so the process is not held to a Low-integrity label the checkout may carry; the checkout `bin` tree remains the pointer and the build home. The command-line face is to move into a separate `memar_cli` bundle so this server release carries no CLI surface.
- **The binary holds the code and finds none by the file system.** Documents, `.kh` files and the records branch are data and stay outside it; where the project is, is given to a call and is not read from the place of a code file.
- **A running server keeps the release it started with.** A change to the checkout reaches no running chat; only `memar update` builds a new release and moves the pointer to it, and the previous release is kept to run if the new one does not start. No fingerprint of files and no replacement of a worker by a change of files is part of a call.
- **The notice that a newer release exists is written to `temp/memar.log` of the project** and is not shown at the next command.
- **The bundle names exactly the modules it uses and carries no others;** services, the module list and the faces (command line, MCP, a future HTTP) are separate, and no service names a face.
- **When an agent's change needs a release to take effect,** the rule [an agent that changed the server updates it](/modules-plugable/management/task/rules/an-agent-that-changed-the-server-updates-it/an-agent-that-changed-the-server-updates-it.md) says who calls `memar update` and when.
