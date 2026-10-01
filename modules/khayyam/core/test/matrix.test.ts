import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

import { analyze, type FileSystem } from "../src/frontend.ts";
import type { RefusalReason } from "../src/sr.ts";

// The matrix over the archive: the corpus the toolchain is measured against, row for row.
// A form's meaning and a refusal's label are pinned one at a time in form.test.ts and
// refusal.test.ts against text written here, and neither of those can say whether a real
// file of the repository holds a form the toolchain admits or a fault it refuses — only a
// file read from the corpus can.

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

// The archive's own counter-examples, and files that carry the forms the toolchain
// accepts. An accept row is worth nothing on a file that holds no declaration —
// most of the corpus's control-flow files are a licence header and nothing else —
// so the guard below holds every accept row to that.
const ARCHIVE_EXPECTATIONS: ReadonlyArray<
  readonly [string, "accept" | "refuse", RefusalReason?]
> = [
  // Refused for a form the language does not have. The label says which fault.
  ["modules/memory/reference/weak.kh", "refuse", "keyword-as-identifier"],
  // if.kh is a draft whose owner and layout are open
  // (docs/protocols/process/control-flow.handoff.md), so the row holds only that the
  // draft is refused. Its faults — an Error import from a file that does not
  // declare it, a signature naming unbound types — are pinned by the
  // inline rows above, not by which one this file happens to report first.
  ["modules/process/control-flow/protocol/if.kh", "refuse"],
  // Accepted, and each of these says something: an inclusion that resolves, a
  // capsule, an abstraction composition, a method with more than one parameter.
  // Three files once refused as `declaration-form` and now belong here, because the
  // form that put them there is gone from the corpus: the method written without
  // `mt` that concurrency.kh, blocking.kh, and life_cycle.kh each carried. The
  // form itself is pinned by refusal.test.ts, which can hold text the corpus no
  // longer does; a matrix row can only report what a real file holds, and these
  // three hold the corrected form.
  ["modules/computer/runtime/protocol/concurrency.kh", "accept"],
  ["modules/computer/runtime/protocol/blocking.kh", "accept"],
  ["modules/computer/capsule/protocol/life_cycle.kh", "accept"],
  ["modules/process/control-flow/protocol/panic-recovery.kh", "accept"],
  ["modules/time/duration/nano-in-second.kh", "accept"],
  ["modules/computer/datatype/protocol/identifiers.kh", "accept"],
  ["modules/computer/datatypes/protocol/data-types.kh", "accept"],
  ["modules/computer/adt/hash_table/protocol/accessor.kh", "accept"],
  ["modules/net/srpc/protocol/srpc.kh", "accept"],
  ["modules/math/float/float-32.kh", "accept"],
];

for (const [path, expected, reason] of ARCHIVE_EXPECTATIONS) {
  test(`archive ${path} is ${expected}ed`, () => {
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

test("every accept row of the matrix is a file that declares something", () => {
  for (const [path, expected] of ARCHIVE_EXPECTATIONS) {
    if (expected !== "accept") continue;
    assert.match(archive(path), /^(tp|vr)\s/m, `${path} declares nothing, so accepting it proves nothing`);
  }
});
