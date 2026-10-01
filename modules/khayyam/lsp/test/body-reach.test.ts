import assert from "node:assert/strict";
import test from "node:test";

import { definitionAt } from "../src/definition.ts";
import { semanticRoles } from "../src/semantic.ts";
import { asking, characterOn, linesOf, URI } from "./definition-fixture.ts";

// How far a name a body declares reaches, which is a different question from whether the
// line a use stands on matters ([body-order.test.ts](./body-order.test.ts)): two passes
// change the order of the uses, and the reach of a name is the block that holds its
// declaration statement.

const rolesOf = (source: string, name: string): string[] =>
  semanticRoles(source)
    .filter((token) => token.text === name)
    .map((token) => `${token.line}:${token.role}`);

test("a declaration is bound in the block that contains the statement, not the block it opens", () => {
  // The block holding a declaration statement is the one the name is bound in, and for a
  // Scope declared in a method body that is the method body, which is what lets a driver
  // name the scope it is about: the `CF.ELSE(elseProcess)` a line above the
  // `tp elseProcess sc` that declares it. A `vr` written inside a scope is a different
  // case, because the block holding that statement is the scope.
  const source = [
    "tp Host ab",
    "tp Run mt (self Host) () () {",
    "    tp First sc {",
    "        vr only Host",
    "    }",
    "    tp Second sc {",
    "        only.Enter()()",
    "        First.Enter()()",
    "        Second.Enter()()",
    "    }",
    "}",
    "",
  ].join("\n");
  const lines = linesOf(source);
  const at = (line: number, name: string) => characterOn(lines, line, name);
  // A `vr` inside a scope is that scope's own, and reaches nothing beside it.
  assert.equal(definitionAt(URI, source, { line: 6, character: at(6, "only") }, asking), null);
  assert.equal(definitionAt(URI, source, { line: 3, character: at(3, "only") }, asking)?.line, 3);
  // A Scope declared in the method body is the method body's, so its name is answered
  // throughout the method, inside its own statements and inside a block beside them.
  assert.equal(definitionAt(URI, source, { line: 7, character: at(7, "First") }, asking)?.line, 2);
  assert.equal(definitionAt(URI, source, { line: 8, character: at(8, "Second") }, asking)?.line, 5);
  assert.deepEqual(rolesOf(source, "First"), ["2:scope", "7:scope"]);
  assert.deepEqual(rolesOf(source, "only"), ["3:method-local", "6:identifier-reference"]);
});

test("a body's name does not leave the body", () => {
  const source = [
    "tp Host ab",
    "tp Run mt (self Host) () () {",
    "    vr held Host",
    "}",
    "tp Other mt (self Host) () () {",
    "    held.Enter()()",
    "}",
    "",
  ].join("\n");
  const lines = linesOf(source);
  assert.equal(definitionAt(URI, source, { line: 5, character: characterOn(lines, 5, "held") }, asking), null);
  assert.deepEqual(rolesOf(source, "held"), ["2:method-local", "5:identifier-reference"]);
});

test("a file-level name of the same text keeps its own role where a body does not declare it", () => {
  const source = [
    "tp Host ab",
    "vr held Host",
    "tp Run mt (self Host) () () {",
    "    held.Enter()()",
    "}",
    "",
  ].join("\n");
  const lines = linesOf(source);
  assert.deepEqual(rolesOf(source, "held"), ["1:variable", "3:variable"]);
  assert.equal(definitionAt(URI, source, { line: 3, character: characterOn(lines, 3, "held") }, asking)?.line, 1);
});
