import assert from "node:assert/strict";
import test from "node:test";

import { definitionAt } from "../src/definition.ts";
import { at, asking, characterOn, linesOf, SOURCE, URI } from "./definition-fixture.ts";

// A name nothing declares, and what "nothing" is when the document cannot be read. A
// definition that answers is a place a reader is sent, so every case here is a case where
// a sent place would be wrong: a reserved word, punctuation, a name no binding answers, a
// file the reader could not read in full, and a name the display contract does not
// recognise as an identity at all.

test("a name nothing declares has no definition", () => {
  const nowhere: Array<[number, number, string]> = [
    [5, 0, "tp"], //            a reserved word
    [5, 10, "("], //            punctuation
    [5, at(5, "String"), "String"], //   a type this file does not declare
    [7, at(7, "CopyFrom"), "CopyFrom"], // a method on a type, which no declaration here names
    [3, at(3, "U8"), "U8"], //  a type this file does not declare
  ];
  for (const [line, character, what] of nowhere) {
    assert.equal(definitionAt(URI, SOURCE, { line, character }, asking), null, `${what} at ${line}:${character}`);
  }
});

test("a position standing on nothing answers nothing rather than the nearest name", () => {
  for (const [line, character] of [[0, 0], [5, 2], [5, 9], [10, 0], [12, 0]] as const) {
    assert.equal(definitionAt(URI, SOURCE, { line, character }, asking), null, `${line}:${character}`);
  }
});

test("a receiver in a signature's owner slot has no definition, and that is one decision with its role", () => {
  // The owner group says which type a method belongs to, and what stands in front of it
  // is the receiver, whose meaning the type beside it supplies. The display contract
  // gives the type a role and the receiver none, and a role the contract does not
  // recognise is not an identity this toolchain may follow — so the receiver is not
  // bound, and neither the declaration nor a use of it is answerable. The two absences
  // are one decision: making the receiver followable is a change to the contract, and a
  // display distinction is added there first, never smuggled in through a reader.
  const source = ["tp Buffer cp {}", "tp Run mt (self Buffer) () () {", "}", ""].join("\n");
  const lines = linesOf(source);
  assert.equal(definitionAt(URI, source, { line: 1, character: characterOn(lines, 1, "self") }, asking), null);
  assert.notEqual(characterOn(lines, 1, "Buffer"), -1, "the owner type is the one the contract does name");
  assert.notEqual(
    definitionAt(URI, source, { line: 1, character: characterOn(lines, 1, "Buffer") }, asking),
    null,
    "the type in the owner slot is a name the file declares, and is answered as one",
  );
});

test("a name in a document the reader could not read in full reaches what was read", () => {
  // The recovery is per declaration, so a line the frontend could not read costs the
  // file that line and nothing else — a definition is part of what a reader is owed
  // for the rest of the file, and it is lost by exactly the same fault as a role.
  const source = [
    "tp Reader ab",
    "tp Run mt (self Reader) () () {",
    "    goto end",
    "    Copy(reader)",
    "}",
    "tp Later ab",
    "",
  ].join("\n");
  const lines = linesOf(source);
  assert.equal(
    definitionAt(URI, source, { line: 3, character: characterOn(lines, 3, "reader") }, asking),
    null,
    "the name after the fault is not bound, so it has no definition",
  );
  assert.deepEqual(
    definitionAt(URI, source, { line: 5, character: characterOn(lines, 5, "Later") }, asking),
    { uri: URI, line: 5, startChar: characterOn(lines, 5, "Later"), length: 5, name: "Later" },
    "the declaration after the fault still answers",
  );
});

test("a document that cannot be read at all answers nothing rather than throwing", () => {
  for (const source of ["tp\n", "tp X\n", "}\n", "tp X cp {\n", "vr\n", "/* unterminated"]) {
    assert.doesNotThrow(() => definitionAt(URI, source, { line: 0, character: 0 }, asking), source);
  }
});
