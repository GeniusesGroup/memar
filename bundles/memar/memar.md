---
Title: "Memar"
Status: Draft
Start Date: 2026-10-07
ID: 497607
---

# Memar
## Abstract
This bundle is the home of the **Memar server**: the program through which a person or an agent works on a repository the Memar way — creating a module or a service, generating a service's SDK, building and deploying an application. It is a [bundle](../README.md) rather than a module because it runs operations that modules own rather than owning one itself. No specification of it is written yet, and nothing here realizes it yet. What the folder holds today is what `memar-go` had for that role, carried over by the port and still in its archived Go: the program's entry and command registration (`main.kh`, `init-cmd.kh`, `init-server.kh`, `const.kh`, `locale.eng.kh`), the application's lifecycle (`app/`), and the `locale` command (`locale/`). The direction this bundle is to take, and what is still open about it, are in the paired [handoff](./memar.handoff.md).

## What belongs here
What only the server does: receiving a request for one of Memar's operations, routing it to the module that owns the operation, and answering. An operation another module owns stays in that module even when the server is how it is reached — creating a module is [`computer/module/`](../../modules/computer/module/)'s, generating a service's SDK is [`process/service/`](../../modules/process/service/)'s, and a module's error SDK is [`process/error/`](../../modules/process/error/)'s.
