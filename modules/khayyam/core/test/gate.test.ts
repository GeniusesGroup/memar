import assert from "node:assert/strict";
import test from "node:test";

import { parseUnit } from "../src/gate.ts";

// What a gate asks for: the whole unit, or the one fault that refuses it. Nothing sits
// between this call and the parser — no file system, no name resolution — so what is
// pinned here is the gate's own answer about the file's form. The matrix reads the same
// answer through `analyze`, which folds it into one outcome and carries a reason and a
// line out of it, so everything the frontend drops on the way is pinned here instead.

test("a unit with no fault comes back whole, each declaration on the line it was read on", () => {
  const result = parseUnit("main.kh", "tp Reader ab\nvr name Reader\n");
  assert.equal(result.ok, true, result.ok ? "" : `refused: ${result.fault.reason}`);
  if (!result.ok) return;
  assert.deepEqual(
    result.unit.declarations.map((declaration) => `${declaration.form}:${declaration.name}:${declaration.line}`),
    ["tp-ab:Reader:1", "vr:name:2"],
  );
});

test("the fault a gate names is the one met first", () => {
  // A second fault stands behind this one. Which of them a gate reports is the difference
  // between a diagnostic that points at the first thing wrong and one that points at the
  // last, and a file with two faults is the only case that tells the two apart.
  const result = parseUnit("main.kh", "tp A ab\nvr in W16\ntp B ab;\n");
  assert.equal(result.ok, false, result.ok ? "accepted a file with two faults" : "");
  if (result.ok) return;
  assert.equal(result.fault.reason, "keyword-as-identifier", result.fault.reason);
  assert.equal(result.fault.line, 2);
});

test("a gate returns no unit at all when it refuses one", () => {
  // Not a unit with a fault beside it: a refused unit is not a unit, and a consumer that
  // could go on to read a partial one would be reading a guess the fault forbids.
  const result = parseUnit("main.kh", "tp A ab\nvr in W16\n");
  assert.equal("unit" in result, false);
});

test("a fault carries the whole of the place it stands at", () => {
  // Column, length, and the text itself are what a consumer underlines, and the frontend
  // keeps only a reason and a line — so if nothing here pins them, nothing in the
  // toolchain does.
  const result = parseUnit("main.kh", "tp A ab;\n");
  assert.equal(result.ok, false);
  if (result.ok) return;
  assert.deepEqual(result.fault, {
    reason: "semicolon",
    line: 1,
    column: 8,
    length: 1,
    text: ";",
    extent: "declaration",
  });
});

test("a lexical fault is the gate's own finding, not one handed on to a parser", () => {
  // The character takes the rest of its line with it (the scanner owns that decision), so
  // what the gate reports is the scanner's fault at the scanner's own extent. A gate that
  // asked the parser instead would report a refusal at a place the file was never read to.
  const result = parseUnit("main.kh", "tp A cp {\n    addr [8]W\n}\n");
  assert.equal(result.ok, false);
  if (result.ok) return;
  assert.equal(result.fault.reason, "unexpected-character", result.fault.reason);
  assert.equal(result.fault.line, 2);
  assert.equal(result.fault.extent, "line");
});
