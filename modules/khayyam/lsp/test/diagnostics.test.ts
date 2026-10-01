import assert from "node:assert/strict";
import test from "node:test";

import { diagnosticOf, refusalDiagnostic } from "../src/diagnostics.ts";
import type { Fault } from "../../core/src/sr.ts";

// What a fault is said to be, to whoever is reading the line it stands on. The wire tests
// assert one message end to end, for a fault that follows another; everything else here —
// a fault that stands on its own, a fault that cost the rest of the file, a line that
// ends where the fault stands — was reachable only by reading the code that builds the
// sentence rather than by asking what it says.

const faultOf = (over: Partial<Fault> = {}): Fault => ({
  reason: "unexpected-character",
  line: 6,
  column: 13,
  length: 1,
  text: ">",
  extent: "line",
  ...over,
});

interface Diagnostic {
  range: { start: { line: number; character: number }; end: { line: number; character: number } };
  severity: number;
  code: string;
  source: string;
  message: string;
}

function saidOf(fault: Fault): Diagnostic {
  return diagnosticOf(fault) as Diagnostic;
}

test("a fault is shown on the line it stands on, as an error, under its own label", () => {
  const said = saidOf(faultOf());
  assert.deepEqual(said.range, {
    start: { line: 5, character: 12 },
    end: { line: 5, character: 13 },
  });
  assert.equal(said.severity, 1, "a refusal is an error rather than a hint");
  assert.equal(said.code, "unexpected-character", "the code is the refusal label this toolchain draws from");
  assert.equal(said.source, "khayyam");
  assert.equal(
    said.message,
    'unexpected-character at line 6, column 13 — ">": a character the grammar has no form for; the dot of invocation is the only operator it has. The rest of that line was not read.',
  );
});

test("a line that ends where the fault stands is said so rather than quoted", () => {
  // `JSON.stringify("")` would put two quote marks on the screen where there is nothing
  // to quote, which reads as a token rather than as the absence of one.
  const said = saidOf(faultOf({ reason: "unterminated-string", column: 20, length: 0, text: "" }));
  assert.equal(said.message.includes("the line ends there"), true);
  assert.equal(said.message.includes('""'), false, "and not as a quoted empty form");
});

test("what a fault cost is said, and it is the language's own unit", () => {
  for (const [extent, cost] of [
    ["line", "The rest of that line was not read"],
    ["declaration", "That declaration was not read; the lines around it still were"],
    ["file", "Nothing after it could be read"],
  ] as const) {
    const said = saidOf(faultOf({ extent }));
    assert.equal(said.message.endsWith(`${cost}.`), true, `a ${extent} fault says what it cost`);
  }
});

test("a fault that follows another names it, its line, and what that cost", () => {
  const said = saidOf(
    faultOf({ reason: "declaration-form", line: 9, column: 1, text: "}", extent: "declaration", because: faultOf() }),
  );
  assert.equal(
    said.message,
    'declaration-form at line 9, column 1 — "}": a form no declaration takes here.' +
      " It follows from the unexpected-character at line 6: the rest of that line was not read," +
      " and a brace went with it, so this closing brace has nothing left to close." +
      " That declaration was not read; the lines around it still were.",
  );
});

test("a fault that follows nothing says so, and a brace that closes nothing is told apart", () => {
  // Standing on its own, `a form no declaration takes here` at a closing brace is true of
  // every stray brace, so the sentence names what makes this one odd. A fault that is
  // not a brace adds nothing rather than naming a cause that does not exist.
  assert.equal(
    saidOf(faultOf({ reason: "declaration-form", line: 9, column: 1, text: "}", extent: "declaration" })).message,
    'declaration-form at line 9, column 1 — "}": a form no declaration takes here.' +
      " It is a closing brace and no block is open, so it closes nothing." +
      " That declaration was not read; the lines around it still were.",
  );
  assert.equal(
    saidOf(faultOf({ reason: "keyword-as-identifier", column: 3, length: 2, text: "tp" })).message,
    "keyword-as-identifier at line 6, column 3 — \"tp\": a reserved word used as a name. The rest of that line was not read.",
  );
});

test("a change this server cannot read is refused on the document it was about", () => {
  // A payload this server cannot read is the same kind of fault as a character it cannot
  // read, and it stands on the document that carries it: a line in a log nobody opens is
  // how a dead server read as a success.
  const said = refusalDiagnostic("contentChanges[0] carries a range") as Diagnostic;
  assert.deepEqual(said.range, {
    start: { line: 0, character: 0 },
    end: { line: 0, character: 0 },
  });
  assert.equal(said.code, "text-document-sync", "named by what it contradicts");
  assert.equal(said.severity, 1);
  assert.match(said.message, /contentChanges\[0\] carries a range/);
  assert.match(said.message, /not about the file on screen/);
});
