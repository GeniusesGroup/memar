import assert from "node:assert/strict";
import test from "node:test";

import { readUnit } from "../src/reader.ts";

// What a reader answers: what of a unit could be read, and every fault met while reading
// it, side by side. No test in this module calls the reader — the matrix asks the gate,
// and the language server asks it through a display question — so everything pinned here
// is unpinned everywhere in core today.

test("a reader reports every fault, not the first one it met", () => {
  // The gate answers once, so it can only name the first fault. A reader owes a diagnostic
  // for each fault, and a reader that reported one fault for two faults would leave the
  // author fixing the file and discovering the second one only on the next run.
  const read = readUnit("main.kh", "tp A ab\nvr in W16\ntp B ab;\ntp C ab\n");
  assert.deepEqual(
    read.faults.map((fault) => `${fault.reason}:${fault.line}`),
    ["keyword-as-identifier:2", "semicolon:3"],
  );
});

test("reading goes on past a fault, at the line break that ends the declaration", () => {
  // Recovery is per declaration and at that line break
  // (docs/khayyam/khayyam.md → Declaration separator), so the three readable declarations
  // stand in the unit and each carries the line it was read on — the line is what pairs a
  // recovered declaration with the place a fault was reported.
  const read = readUnit("main.kh", "tp A ab\nvr in W16\ntp B ab;\ntp C ab\n");
  assert.deepEqual(
    read.unit.declarations.map((declaration) => `${declaration.form}:${declaration.name}:${declaration.line}`),
    ["tp-ab:A:1", "tp-ab:B:3", "tp-ab:C:4"],
  );
});

test("an inclusion written without its in keyword costs its own line, not the inclusions beside it", () => {
  // An inclusion is one line like any other declaration, so a malformed one is refused on
  // its own and the resolvable inclusions either side of it are read as themselves.
  const read = readUnit(
    "main.kh",
    'tp Bool in "lib/boolean.kh"\ntp Error "memar/process/error"\ntp D ab\n',
  );
  assert.deepEqual(
    read.unit.declarations.map((declaration) => `${declaration.form}:${declaration.name}`),
    ["tp-in:Bool", "tp-ab:D"],
  );
  assert.equal(read.faults.length, 1);
  assert.equal(read.faults[0]!.reason, "declaration-form", read.faults[0]!.reason);
  assert.equal(read.faults[0]!.line, 2);
});

test("a lexical fault does not take the lines above it with it", () => {
  // The fault stands at a character and every line above it ended where it says it did, so
  // those lines are read and the fault is reported beside them. A reader that dropped the
  // whole file would answer a display question about a file with nothing in it.
  const read = readUnit("main.kh", "tp A cp {\n    addr [8]W\n}\ntp B ab\n");
  assert.deepEqual(
    read.unit.declarations.map((declaration) => `${declaration.form}:${declaration.name}`),
    ["tp-cp:A", "tp-ab:B"],
  );
  assert.deepEqual(
    read.faults.map((fault) => `${fault.reason}:${fault.line}:${fault.extent}`),
    ["unexpected-character:2:line"],
  );
});

test("a fault that follows another names the one it follows from", () => {
  // The closing brace was not written there; an earlier fault took a block with it. Only a
  // reader that met both can say so, and only the cause tells an author which repair takes
  // the other away.
  const read = readUnit("main.kh", "tp A ab\nvr in W16\n}\ntp B ab\n");
  assert.deepEqual(
    read.faults.map((fault) => `${fault.reason}:${fault.line}:${fault.text}`),
    ["keyword-as-identifier:2:in", "declaration-form:3:}"],
  );
  assert.deepEqual(read.faults[1]!.because, {
    reason: "keyword-as-identifier",
    line: 2,
    column: 4,
    length: 2,
    text: "in",
    extent: "declaration",
  });
});

test("a reader reports a form the language cannot decide and leaves names to the analyser", () => {
  // A signature naming a type the unit never declares is a form the parser reads whole; who
  // declares it is the analyser's question, and a reader that refused it would cost the
  // display every declaration in the file over one reference it cannot check.
  const read = readUnit("main.kh", "tp Use mt (self Owner) () (err Error)\n");
  assert.deepEqual(
    read.unit.declarations.map((declaration) => `${declaration.form}:${declaration.name}`),
    ["tp-mt:Use"],
  );
  assert.deepEqual(read.faults, []);
});
