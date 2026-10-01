import assert from "node:assert/strict";
import test from "node:test";

import { analyze, type FileSystem } from "../src/frontend.ts";
import type { RefusalReason } from "../src/sr.ts";

// One statement of how a row is written, and of the file system a row is handed, because
// a row written twice is written twice differently: the second copy is shaped to whatever
// the rows that own it happened to need. The rows themselves live in the files whose names
// say what a row is about — a form in form.test.ts, a refusal in refusal.test.ts, the
// corpus in matrix.test.ts — and this file holds only what all of them write with.

export const memory = (files: Record<string, string> = {}): FileSystem => ({
  read: (path) => files[path],
});

export function accepts(
  name: string,
  source: string,
  files: Record<string, string> = {},
): void {
  test(`accepts ${name}`, () => {
    const result = analyze("main.kh", source, memory(files));
    assert.equal(
      result.outcome,
      "accept",
      result.outcome === "refuse" ? `refused: ${result.reason}` : "",
    );
  });
}

/** The label is part of what is being asserted: a rule that refuses is not the
 *  same rule as any other rule that refuses, and a row that only says "refused"
 *  would pass on a fault the row is not about. */
export function refuses(
  name: string,
  reason: RefusalReason,
  source: string,
  files: Record<string, string> = {},
): void {
  test(`refuses ${name}`, () => {
    const result = analyze("main.kh", source, memory(files));
    assert.equal(
      result.outcome,
      "refuse",
      result.outcome === "accept" ? "accepted" : `refused as ${result.reason} at line ${result.line}`,
    );
    if (result.outcome !== "refuse") return;
    assert.equal(result.reason, reason, result.reason);
  });
}
