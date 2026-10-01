import assert from "node:assert/strict";
import test from "node:test";

import { ROLES, scopeFor } from "../src/contract.ts";
import { semanticRoles } from "../src/semantic.ts";

// What the roles of a document say about the names standing in it: one role per identity,
// the same at every position that identity stands in. The load-bearing claim is the first
// test here — a role names what a name IS, never where it appears — so this file is the
// suite that holds a role from drifting into a position.
//
// What a line's own shape makes a name is in [block-roles.test.ts](./block-roles.test.ts),
// what a signature says is in [signature.test.ts](./signature.test.ts), and what a reader
// is still given for a document the frontend could not read is in
// [recovery.test.ts](./recovery.test.ts).

const SOURCE = [
  'tp Bool in "memar/math/boolean"',
  'tp Reader ab',
  "tp Buffer cp {",
  "\tdata U8",
  "}",
  "tp Set mt (self Reader) (key String) (err Error) {",
  "\tvr local Buffer",
  "\tkey.CopyFrom(local)(err)",
  "\tBool.IsTrue()",
  "}",
  "",
].join("\n");

function roleOf(text: string, occurrence = 0): string {
  const found = semanticRoles(SOURCE).filter((token) => token.text === text);
  const token = found[occurrence];
  assert.ok(token, `'${text}' #${occurrence} not found in the analysed source`);
  return token.role;
}

test("every role the resolver emits is a role the display contract defines", () => {
  for (const token of semanticRoles(SOURCE)) {
    assert.ok(ROLES.includes(token.role), `${token.role} is not in the contract`);
  }
});

test("a type brought in by an inclusion keeps the inclusion role everywhere it is used", () => {
  assert.equal(roleOf("Bool", 0), "included-type"); // the inclusion line
  assert.equal(roleOf("Bool", 1), "included-type"); // the use in a method body
});

test("an inclusion and a local abstraction do not share a role", () => {
  assert.equal(roleOf("Bool", 0), "included-type");
  assert.equal(roleOf("Reader", 0), "abstraction"); // the declaration
});

test("a parameter keeps the parameter role in the signature and in the body", () => {
  assert.equal(roleOf("key", 0), "method-argument");
  assert.equal(roleOf("key", 1), "method-argument");
});

test("a parameter and an included type do not share a role", () => {
  assert.notEqual(roleOf("key", 0), roleOf("Bool", 0));
});

test("a variable declared in a method body is not a parameter", () => {
  // The owner's split of 2026-09-28: a `vr` in a body and a `vr` at file level are
  // two identities with two different scopes of validity, so they are two roles
  // (display.json -> method-local). This assertion was `variable` until the split;
  // the shape it fixes is the name the body declaration now carries.
  assert.equal(roleOf("local", 0), "method-local");
  assert.notEqual(roleOf("local", 0), roleOf("key", 0));
});

test("a name declared in a method body carries its role at its declaration and at its use", () => {
  // A role names what an identifier IS, never where it appears, so the split is not
  // a declaration-site role with a fallback at the use site: the use in the body
  // resolves to the declaration and answers the same role (display.json -> principles).
  assert.equal(roleOf("local", 1), "method-local");
});

test("a parameter, a name declared in a body and a name declared at file level are three roles", () => {
  // The three the owner named, side by side in one body, so a reader of the stream
  // has all three at once and the answer is not two roles where three were asked for.
  const source = [
    "tp Buffer cp {}",
    "vr held Buffer",
    "tp Run mt (self Buffer) (p Buffer) () {",
    "\tvr scratch Buffer",
    "\tscratch.Copy(p)(held)",
    "}",
    "",
  ].join("\n");
  const rolesOf = (text: string) =>
    semanticRoles(source)
      .filter((token) => token.text === text)
      .map((token) => token.role);
  assert.deepEqual(rolesOf("p"), ["method-argument", "method-argument"]);
  assert.deepEqual(rolesOf("scratch"), ["method-local", "method-local"]);
  assert.deepEqual(rolesOf("held"), ["variable", "variable"]);
  assert.equal(new Set([...rolesOf("p"), ...rolesOf("scratch"), ...rolesOf("held")]).size, 3);
});

test("a name declared at file level keeps the file-level role inside a body", () => {
  // The other half of the split, and the reason the file-level role was not renamed:
  // a `vr` at file level is the same identity wherever it is used, body included.
  const source = [
    "tp Buffer cp {}",
    "vr held Buffer",
    "tp Run mt (self Buffer) () () {",
    "\tvr scratch Buffer",
    "\tCopy(held)(scratch)",
    "}",
    "",
  ].join("\n");
  const rolesOf = (text: string) =>
    semanticRoles(source)
      .filter((token) => token.text === text)
      .map((token) => token.role);
  assert.deepEqual(rolesOf("held"), ["variable", "variable"]);
  assert.deepEqual(rolesOf("scratch"), ["method-local", "method-local"]);
});

test("a body declaration that shadows a file-level name is the body's own", () => {
  // The body is the narrower scope, so a name declared in it is that declaration for
  // the length of the body even where the file declares the same name. A name collision
  // is an architecture error rather than a disambiguation problem, and the reader is told
  // which of the two it is looking at.
  const source = [
    "tp Buffer cp {}",
    "vr same Buffer",
    "tp Run mt (self Buffer) () () {",
    "\tvr same Buffer",
    "\tCopy(same)()",
    "}",
    "",
  ].join("\n");
  const inside = semanticRoles(source).filter((token) => token.line === 4);
  assert.deepEqual(
    inside.map((token) => `${token.text}:${token.role}`),
    ["Copy:method", "same:method-local"],
  );
  assert.equal(semanticRoles(source).find((token) => token.text === "same" && token.line === 1)?.role, "variable");
});

test("a type declared in this file keeps its own role when used", () => {
  assert.equal(roleOf("Buffer", 0), "capsule");
  assert.equal(roleOf("Buffer", 1), "capsule");
});

test("a method keeps the method role at its declaration and at a call site", () => {
  assert.equal(roleOf("CopyFrom"), "method");
  assert.equal(scopeFor("method"), "entity.name.function.khayyam");
});

test("keywords and subtypes are told apart", () => {
  assert.equal(roleOf("tp", 0), "keyword");
  assert.equal(roleOf("in", 0), "subtype");
});

test("an inclusion path is a file uri", () => {
  const tokens = semanticRoles(SOURCE);
  const uri = tokens.find((token) => token.role === "file-uri");
  assert.ok(uri);
  assert.match(uri!.text, /^".*"$/);
});

test("a capsule field is not a variable", () => {
  assert.equal(roleOf("data"), "capsule-field");
});

test("no two tokens cover the same place in the document", () => {
  for (const source of [SOURCE, "vr other Nothing\n", "tp A cp {\n  x y\n}\n"]) {
    const tokens = semanticRoles(source);
    for (let at = 1; at < tokens.length; at += 1) {
      const previous = tokens[at - 1]!;
      const token = tokens[at]!;
      const overlaps =
        token.line === previous.line && token.startChar < previous.startChar + previous.length;
      assert.ok(!overlaps, `${token.text} at L${token.line}:${token.startChar} overlaps ${previous.text}`);
    }
  }
});

test("an unbound name is an identifier reference, never a declaration", () => {
  const tokens = semanticRoles("vr other Nothing\n");
  const roles = tokens.map((token) => `${token.text}:${token.role}`);
  assert.deepEqual(roles, ["vr:keyword", "other:variable", "Nothing:type-reference"]);
});

test("a quoted form that is no inclusion's path is not a path", () => {
  // The contract gives a quoted literal the `string` role and names the role
  // reserved; `file-uri` is the path an `in` inclusion routes to, so a literal in a
  // body is not one.
  const source = ["tp Host ab", "tp Run mt (self Host) () () {", '\td.Copy("2")', "}", ""].join("\n");
  const literal = semanticRoles(source).find((token) => token.role === "string");
  assert.ok(literal);
  assert.equal(literal!.text, '"2"');
  assert.equal(semanticRoles(source).filter((token) => token.role === "file-uri").length, 0);
});
