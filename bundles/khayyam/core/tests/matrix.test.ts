/* For license and copyright information please see the LEGAL file in the code repository */

import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

import { analyze, type FileSystem } from "../src/frontend.ts";
import type { RefusalReason } from "../src/sr.ts";

const BUDGET_SECONDS = 30;
const TIER = "integration";
const COST = { subprocesses: 0, writes_files: false, clock_waits: false };
const SUBJECT = "Khayyam repository declaration acceptance matrix";
const options = { timeout: BUDGET_SECONDS * 1000 };
const REPOSITORY = new URL("../../../../", import.meta.url);

const archive = (relative: string): string =>
  readFileSync(new URL(relative, REPOSITORY), "utf8");

const archiveFileSystem: FileSystem = {
  read: (path) => {
    try {
      return readFileSync(new URL(path, REPOSITORY), "utf8");
    } catch {
      return undefined;
    }
  },
};

const ARCHIVE_EXPECTATIONS: ReadonlyArray<
  readonly [string, "accept" | "refuse", RefusalReason?]
> = [
  ["modules/computer/memory/reference/weak.kh", "refuse", "keyword-as-identifier"],
  ["modules/process/control-flow/protocol/if.kh", "refuse"],
  ["modules/computer/runtime/protocol/concurrency.kh", "accept"],
  ["modules/computer/runtime/protocol/blocking.kh", "refuse", "capsule-in-abstraction-signature"],
  ["modules/computer/capsule/protocol/life_cycle.kh", "accept"],
  ["modules/process/control-flow/protocol/panic-recovery.kh", "accept"],
  ["modules/time/duration/nano-in-second.kh", "accept"],
  ["modules/computer/type/protocol/identifiers.kh", "accept"],
  ["modules/computer/types/protocol/types.kh", "accept"],
  ["modules/computer/adt/hash_table/protocol/accessor.kh", "accept"],
  ["modules/net/srpc/protocol/srpc.kh", "accept"],
  ["modules/math/float/float-32.kh", "accept"],
];

for (const [path, expected, reason] of ARCHIVE_EXPECTATIONS) {
  test(`archive ${path} is ${expected}ed`, options, () => {
    const result = analyze(path, archive(path), archiveFileSystem);
    assert.equal(
      result.outcome,
      expected,
      result.outcome === "refuse" ? `refused as ${result.reason} at line ${result.line}` : "",
    );
    if (reason === undefined || result.outcome !== "refuse") return;
    assert.equal(result.reason, reason, result.reason);
  });
}

test("every accept row of the matrix is a file that declares something", options, () => {
  for (const [path, expected] of ARCHIVE_EXPECTATIONS) {
    if (expected !== "accept") continue;
    assert.match(archive(path), /^(tp|vr)\s/m, `${path} declares nothing, so accepting it proves nothing`);
  }
});
