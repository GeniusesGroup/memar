// The command that reaches the declaration-rename service for Khayyam:
// `node rename/rename.ts --name OLD --to NEW [--declaration PATH:LINE] [--residue] [--samples N]
// [--report PATH] [--root PATH] [--exclude PREFIX] [paths…]`.
//
// This file is the declaration-rename rule's own invocation, and the only one: the mechanism
// beside it is not runnable on its own, so a run is reached through this command or not at
// all. It is invoked over argv because that is what the no CLI or TUI decision
// ([`khayyam.handoff.md`](../../khayyam.handoff.md) → Decisions) carves out — build
// tooling is developer-side and is not the product's interaction surface, so a developer's
// one-off rename is a command and not an app. Were the rule's subject the product's own
// interaction, it would owe an app instead, and `lsp/src/` is where that would live.
//
// It stands here rather than in the service because it is Khayyam's half of the seam: it is
// the one file that says *which* language answers, by handing the service the binding it
// answers with, and it says which other reader `--residue` means as well. The service owns
// the corpus, the plan, the report, the write, the gate, the command line and the exit codes;
// this file supplies this repository's corpus facts and nothing about what a name binds to.

import { resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { runRenameCommand } from "./declaration-rename.ts";

import { khayyamBinding, khayyamResidue } from "./khayyam-binding.ts";

/** What a run leaves `bundles/khayyam/` alone by default: the toolchain's own `.kh` files
 *  are samples and test programs, not the ported sources this rule is about. */
const EXCLUDES: readonly string[] = ["bundles/khayyam/"];

/** The repository this rule was asked about, which is the checkout the rule sits in: four
 *  levels above this file, so `rename/` beside `core/` and `targets/`. */
const REPOSITORY = resolve(fileURLToPath(import.meta.url), "../../../../..");

process.exitCode = runRenameCommand(
  process.argv.slice(2),
  khayyamBinding,
  { root: REPOSITORY, unit: ".kh", excludes: EXCLUDES },
  khayyamResidue,
);
