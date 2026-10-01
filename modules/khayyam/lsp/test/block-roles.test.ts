import assert from "node:assert/strict";
import test from "node:test";

import { semanticRoles } from "../src/semantic.ts";

// What the block a line stands in makes of the names on it: a capsule's field line
// declares where a body statement only uses, and a scope declared inside a method body
// carries its role and its statements. The block is a fact about the document and not
// about a line — which line opens the body is not on the line that stands in it — so this
// is the subject the role-per-identity suite cannot answer on its own.

test("a scope declared inside a method body carries the scope role", () => {
  const source = [
    "tp Host ab",
    "tp Run mt (self Host) () () {",
    "    tp Step sc {",
    "    }",
    "    vr local Host",
    "}",
    "",
  ].join("\n");
  const roles = semanticRoles(source).map((token) => `${token.text}:${token.role}`);
  assert.deepEqual(roles, [
    "tp:keyword",
    "Host:abstraction",
    "ab:subtype",
    "tp:keyword",
    "Run:method",
    "mt:subtype",
    // The owner type is Host, which this file declared as an abstraction, so it is
    // an abstraction here too: one identity, one role (the contract's first
    // principle). `method-owner-type` is the answer for an owner type this file
    // does not state.
    "Host:abstraction",
    "tp:keyword",
    "Step:scope",
    "sc:subtype",
    // The scope's own closing brace ends the scope, so what follows it is still
    // read as a method body: a variable declared there is a variable of the body.
    "vr:keyword",
    "local:method-local",
    "Host:abstraction",
  ]);
});

test("a block closed on its declaration's own line holds nothing after it", () => {  // `tp X cp {}` is a capsule with no fields, and `tp Y mt (...) (...) (...) {}`
  // is a method with an empty body; the corpus writes both. A block that opens and
  // closes on one line must not be treated as still open, or every line after it is
  // read inside a block that already ended.
  const source = [
    "tp Counter cp {}",
    "tp Run mt (self Counter) (limit Integer) () {",
    "\tlimit.Copy()",
    "}",
    "tp Add mt (self Counter) (other Integer) (sum Integer) {}",
    "tp Use mt (self Counter) (n Integer) () {",
    "\tAdd(n)",
    "}",
    "",
  ].join("\n");
  const roleOfText = (text: string) => semanticRoles(source).filter((token) => token.text === text);
  const limit = roleOfText("limit");
  assert.equal(limit.length, 2);
  assert.deepEqual(limit.map((token) => token.role), ["method-argument", "method-argument"]);
  const n = roleOfText("n");
  assert.deepEqual(n.map((token) => token.role), ["method-argument", "method-argument"]);
  const other = roleOfText("other");
  assert.deepEqual(other.map((token) => token.role), ["method-argument"]);
});

test("a parameter keeps the parameter role inside a scope's body", () => {
  // A scope is declared inside a method body and its statements are written there,
  // so a parameter of that method is that parameter inside the scope.
  const source = [
    "tp Host ab",
    "tp Run mt (self Host) (d Host) () {",
    "    tp Step sc {",
    "        d.Copy()",
    "    }",
    "}",
    "",
  ].join("\n");
  const rolesOf = (text: string) =>
    semanticRoles(source)
      .filter((token) => token.text === text)
      .map((token) => token.role);
  assert.deepEqual(rolesOf("d"), ["method-argument", "method-argument"]);
  assert.deepEqual(rolesOf("Copy"), ["method"]);
});
