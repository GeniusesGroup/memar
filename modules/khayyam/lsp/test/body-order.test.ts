import assert from "node:assert/strict";
import test from "node:test";

import { definitionAt } from "../src/definition.ts";
import { semanticRoles } from "../src/semantic.ts";
import { asking, characterOn, linesOf, URI } from "./definition-fixture.ts";

// What a body's order does to a name. The language fixes a declaration's line and states
// nothing about the order of a body's statements, so a reading that resolves a use against
// the names it has already passed makes a name two things: the body-local on the line
// after its declaration and a bare use on the line before it. A body is therefore read in
// two passes — bind what it declares, then resolve what it uses — and what a name is
// wherever it stands does not depend on which line it stands on.
//
// Both answers are asserted here, because they are one decision: a role says what a name
// is and a definition says where it is declared, and a reading that fixed one and not the
// other would leave a reader with a coloured name and nowhere to go, or a place and no
// way to tell what it is.

const rolesOf = (source: string, name: string): string[] =>
  semanticRoles(source)
    .filter((token) => token.text === name)
    .map((token) => `${token.line}:${token.role}`);

/** A body that names a Scope on the line before the `tp` that declares it, and a `vr`
 *  after it, and a call to a method the file declares below the body. */
const BEFORE_AND_AFTER = [
  "tp Host ab",
  "tp Run mt (self Host) () () {",
  "    Use(Step)", //        a scope named before the line that declares it
  "    tp Step sc {",
  "        Step.Enter()()", //   the scope's own name, inside the scope
  "    }",
  "    Later.Enter()()", //   a variable used before the line that declares it
  "    vr Later Host",
  "    Add()", //            a call to a method the file declares below the body
  "}",
  "tp Add mt (self Host) () () {}",
  "",
].join("\n");

const LINES = linesOf(BEFORE_AND_AFTER);
const asking0 = { line: 2, character: characterOn(LINES, 2, "Step") };

test("a name a body declares is that name on every line of the body, not only the ones after its declaration", () => {
  assert.deepEqual(rolesOf(BEFORE_AND_AFTER, "Step"), ["2:scope", "3:scope", "4:scope"]);
  assert.deepEqual(rolesOf(BEFORE_AND_AFTER, "Later"), ["6:method-local", "7:method-local"]);
});

test("a use before its declaration reaches the same place a use after it does", () => {
  for (const [use, declared] of [
    [asking0, 3],
    [{ line: 4, character: characterOn(LINES, 4, "Step") }, 3],
  ] as const) {
    const found = definitionAt(URI, BEFORE_AND_AFTER, use, asking);
    assert.ok(found, `line ${use.line} reaches nothing`);
    assert.equal(found!.line, declared, `line ${use.line} reaches line ${declared}`);
    assert.equal(found!.name, "Step");
    assert.equal(
      LINES[found!.line]!.slice(found!.startChar, found!.startChar + found!.length),
      "Step",
    );
  }
  const later = definitionAt(URI, BEFORE_AND_AFTER, { line: 6, character: characterOn(LINES, 6, "Later") }, asking);
  assert.equal(later?.line, 7);
  assert.equal(later?.name, "Later");
});

test("a call to a method this file declares reaches that method, wherever the call stands", () => {
  // A role follows the binding, never the position: the parenthesis says the name is
  // called, and the declaration says which Method it is. A method this file does not
  // declare is a method on something else and is named by nothing here, so the call
  // carries the role and no place.
  const found = definitionAt(URI, BEFORE_AND_AFTER, { line: 8, character: characterOn(LINES, 8, "Add") }, asking);
  assert.deepEqual(found, {
    uri: URI,
    line: 10,
    startChar: characterOn(LINES, 10, "Add"),
    length: 3,
    name: "Add",
  });
  const source = ["tp Host ab", "tp Run mt (self Host) () () {", "\tAbsent.Enter()()", "}", ""].join("\n");
  const lines = linesOf(source);
  // `Enter` is the name before the parenthesis, so it is the one a call names; `Absent`
  // is the receiver the call is made on, and this file declares no such name.
  assert.equal(definitionAt(URI, source, { line: 2, character: characterOn(lines, 2, "Enter") }, asking), null);
  assert.deepEqual(rolesOf(source, "Enter"), ["2:method"]);
  assert.deepEqual(rolesOf(source, "Absent"), ["2:identifier-reference"]);
});

test("a body that could not be read in full still binds what it did read", () => {
  // The recovery is per declaration and a body is opaque text to the parser, so a line
  // the scanner refuses costs the file that line; the names the rest of the body declares
  // are still bound, and a use of one reaches it whichever side of the fault it stands.
  const source = [
    "tp Host ab",
    "tp Run mt (self Host) () () {",
    "    tp First sc {",
    "    }",
    "    use> here",
    "    First.Enter()()",
    "}",
    "",
  ].join("\n");
  const lines = linesOf(source);
  assert.equal(definitionAt(URI, source, { line: 5, character: characterOn(lines, 5, "First") }, asking)?.line, 2);
  assert.deepEqual(rolesOf(source, "First"), ["2:scope", "5:scope"]);
});
