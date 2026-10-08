import assert from "node:assert/strict";
import test from "node:test";

import { definitionAt } from "../src/definition.ts";
import { at, asking, LINES, SOURCE, URI } from "./definition-fixture.ts";

// A definition inside one document: the name, the place its binding is declared at, and
// the extent of the declared name. What has to leave the document is
// [definition-across-inclusion.test.ts](./definition-across-inclusion.test.ts), what has
// no declaration to reach is [definition-absence.test.ts](./definition-absence.test.ts),
// and what a body's order does to any of it is
// [body-order.test.ts](./body-order.test.ts).

test("a name used in a method body reaches the parameter it names", () => {
  assert.deepEqual(definitionAt(URI, SOURCE, { line: 7, character: at(7, "key") }, asking), {
    uri: URI,
    line: 5,
    startChar: at(5, "key"),
    length: 3,
    name: "key",
  });
});

test("a parameter named in a signature reaches that slot, and a use of it reaches the same place", () => {
  // One name is one binding at every position it stands in, so the two answers are the
  // same place. A definition that answered the use and not the signature would be
  // saying the name is two things.
  const asked = { line: 5, character: at(5, "key") };
  assert.deepEqual(
    definitionAt(URI, SOURCE, asked, asking),
    definitionAt(URI, SOURCE, { line: 7, character: at(7, "key") }, asking),
  );
});

test("a name declared in a method body reaches the declaration in that body, not the one at file level", () => {
  const source = [
    "tp Buffer cp {}",
    "vr held Buffer",
    "tp Run mt (self Buffer) () () {",
    "\tvr held Buffer",
    "\tCopy(held)()",
    "}",
    "",
  ].join("\n");
  const lines = source.split("\n");
  const use = { line: 4, character: lines[4]!.indexOf("held") };
  assert.deepEqual(
    definitionAt(URI, source, use, asking),
    { uri: URI, line: 3, startChar: lines[3]!.indexOf("held"), length: 4, name: "held" },
    "the body is the narrower scope, so the name in the body is the body's declaration",
  );
  // The file-level declaration of the same name is a different declaration, and asking
  // at it reaches itself.
  assert.deepEqual(
    definitionAt(URI, source, { line: 1, character: lines[1]!.indexOf("held") }, asking),
    { uri: URI, line: 1, startChar: lines[1]!.indexOf("held"), length: 4, name: "held" },
  );
});

test("a declaration's own name reaches itself", () => {
  for (const [line, name] of [[1, "Reader"], [5, "Set"], [3, "data"]] as const) {
    assert.deepEqual(
      definitionAt(URI, SOURCE, { line, character: at(line, name) }, asking),
      { uri: URI, line, startChar: at(line, name), length: name.length, name },
      `${name} at line ${line} is declared there`,
    );
  }
});

test("a name this file declares, used in a signature, reaches the declaration", () => {
  assert.deepEqual(definitionAt(URI, SOURCE, { line: 5, character: at(5, "Reader") }, asking), {
    uri: URI,
    line: 1,
    startChar: at(1, "Reader"),
    length: 6,
    name: "Reader",
  });
});

test("the extent is the declared name and nothing else", () => {
  // A reader who asks about `err` is sent to `err`; a range covering the whole
  // declaration would put the cursor at the start of the signature instead, which is a
  // different question from the one that was asked. Asked at a declaration the answer is
  // on the line it was asked about, and asked at a use it is the same name where it was
  // declared; either way the extent is the name and never the whole declaration.
  for (const [line, name] of [[1, "Reader"], [5, "Set"], [5, "err"], [3, "data"], [7, "local"]] as const) {
    const found = definitionAt(URI, SOURCE, { line, character: at(line, name) }, asking);
    assert.ok(found, `${name} at line ${line} has no definition`);
    assert.equal(LINES[found!.line]!.slice(found!.startChar, found!.startChar + found!.length), name);
    assert.equal(found!.name, name);
  }
});
