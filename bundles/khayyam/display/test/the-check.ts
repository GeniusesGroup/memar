// The check, run as a process, and the verdict it left behind.
//
// The check's verdict is its own last line, and the last line is the only place a
// reader learns what the check concluded. So it is read here as a value rather than
// watched as output: the status, the last line, and the lines it refused are three
// things a test can be written about.
//
// The check is run as a process, because a unit test of a helper would pass whatever
// shape the helper was handed - the same reason lsp/test/sync.test.ts drives the real
// server over its own stdio.
import { spawnSync } from "node:child_process";
import { join } from "node:path";
import { EXTENSION } from "./shipped.ts";

export const VERIFIER = join(EXTENSION, "scripts", "verify-roles.mjs");

export interface Verdict {
  status: number;
  /** The last line the check wrote to stdout, which is its verdict. */
  verdict: string;
  /** The lines it wrote to stderr under `FAIL`, which is what it refused. */
  refusals: string[];
  out: string;
}

/** Runs the check as a process, over the shipped contract, manifest and themes or over
 *  a copy of any of them. The manifest is the second argument, so a run against a copy
 *  of it still reads the contract the extension ships - the check is asked about the
 *  manifest, not handed a different contract to fail on. The themes root is the third:
 *  the check resolves a contributed theme's `path` against it and counts what the
 *  extension ships from `<root>/themes`, so a run over a copy is asked the same
 *  questions a run over the shipped files is. */
export function run(
  contractPath: string | undefined = undefined,
  manifestPath: string | undefined = undefined,
  themesRoot: string | undefined = undefined,
): Verdict {
  const args = [VERIFIER];
  if (contractPath !== undefined) args.push(contractPath);
  if (manifestPath !== undefined) args.push(manifestPath);
  if (themesRoot !== undefined) args.push(themesRoot);
  const result = spawnSync(process.execPath, args, { encoding: "utf8" });
  const out = result.stdout ?? "";
  const lines = out.split(/\r?\n/).filter((line) => line.trim() !== "");
  const refusals = (result.stderr ?? "")
    .split(/\r?\n/)
    .filter((line) => line.startsWith("  - "))
    .map((line) => line.slice(4));
  return { status: result.status ?? -1, verdict: lines[lines.length - 1] ?? "", refusals, out };
}
