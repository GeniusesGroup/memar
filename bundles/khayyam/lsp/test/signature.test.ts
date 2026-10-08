import assert from "node:assert/strict";
import test from "node:test";

import { bindingsIn } from "../src/binding-table.ts";
import { itemsOnLine, type Place } from "../src/document-items.ts";
import { emitterInto, type SemanticToken } from "../src/role-emitter.ts";
import { signatureRoles } from "../src/signature-roles.ts";
import { semanticRoles } from "../src/semantic.ts";
import { readUnit } from "../../core/src/parse.ts";
import type { MethodDecl } from "../../core/src/sr.ts";

// What the three parenthesised groups of a method signature say about the names
// standing in them. A signature is the one line of the language where a name is
// declared rather than used, and its three groups say three different things — which is
// why it is walked on its own rather than as a line of statements. The first test below
// is the one the whole-file suite already made, kept as it was and measured through the
// whole reading; the rest measure this walk on its own, over one signature's items.

test("a type keeps its own role where a signature names it", () => {
  // A role names what an identifier IS, never where it appears, so an included type
  // named in a signature is still an included type and a type declared here is still
  // its own category. The position roles are what a renderer says for a name the
  // file does not bind, and so are only the answer for an unbound one.
  const source = [
    'tp Duration in "modules/time/duration"',
    "tp Timer ab",
    "tp Set mt (self Timer) (d Duration) () {",
    "\td.Copy()",
    "}",
    "tp Free mt (self Missing) (v Unknown) () {",
    "}",
    "",
  ].join("\n");
  const rolesOf = (text: string) =>
    semanticRoles(source)
      .filter((token) => token.text === text)
      .map((token) => token.role);
  assert.deepEqual(rolesOf("Duration"), ["included-type", "included-type"]);
  assert.deepEqual(rolesOf("Timer"), ["abstraction", "abstraction"]);
  assert.deepEqual(rolesOf("Missing"), ["method-owner-type"]);
  assert.deepEqual(rolesOf("Unknown"), ["method-argument-type"]);
});

/** One signature, with every case it has to tell apart: a type this file declares in
 *  the owner slot, a type that arrived by an inclusion as a parameter's type, a
 *  parameter, and a type nothing here declares. */
const SOURCE = [
  'tp Duration in "modules/time/duration"',
  "tp Timer ab",
  "tp Set mt (self Timer) (d Duration) (err Error) {}",
  "",
].join("\n");
const ITEMS = itemsOnLine(SOURCE).get(2)!;
const DECLARATIONS = readUnit("document.kh", SOURCE).unit.declarations;
const METHOD = DECLARATIONS.find((declaration) => declaration.form === "tp-mt") as MethodDecl;

/** One signature walked, and the tokens it answered with. */
function answered(): { tokens: SemanticToken[]; parameters: Map<string, Place | undefined> } {
  const tokens: SemanticToken[] = [];
  const emitter = emitterInto(tokens, 2, bindingsIn(DECLARATIONS, itemsOnLine(SOURCE)));
  return { tokens, parameters: signatureRoles(METHOD, ITEMS, 2, emitter) };
}

test("the owner slot's own name is the receiver, and the contract gives it no role", () => {
  // `self` in `(self Timer)` is the receiver, and the contract names no role for it, so
  // the grammar keeps it and the server says nothing about it. What it does name is the
  // type it belongs to, which is answered in its own right.
  const { tokens } = answered();
  assert.deepEqual(
    tokens.map((token) => `${token.text}:${token.role}`),
    ["Timer:abstraction", "d:method-argument", "Duration:included-type", "err:method-argument", "Error:method-argument-type"],
  );
  assert.equal(
    tokens.some((token) => token.text === "self"),
    false,
    "the receiver is answered with nothing, which is an answer and not a gap",
  );
});

test("a type named in a signature is still that type, wherever it was declared", () => {
  const { tokens } = answered();
  assert.equal(tokens.find((token) => token.text === "Duration")?.includedThrough, "modules/time/duration");
  assert.equal(tokens.find((token) => token.text === "Duration")?.declaredAt, undefined);
  assert.deepEqual(tokens.find((token) => token.text === "Timer")?.declaredAt, {
    line: 1,
    startChar: 3,
    length: 5,
  });
});

test("each parameter is a slot, declared where its name stands", () => {
  // The parameter's name is the slot it is declared in, so a use of it in the body
  // reaches here. A method's parameters are read from the parse and this walk finds
  // where each name stands, so both halves are asked for: the names, and the places.
  const { parameters } = answered();
  assert.deepEqual(Object.fromEntries(parameters), {
    d: { line: 2, startChar: 24, length: 1 },
    err: { line: 2, startChar: 37, length: 3 },
  });
});

test("a parameter the parse read and this walk did not find is a slot with no place", () => {
  // A file read with recovery can hold a line whose items are not the signature the
  // parse read from it. The parameter is known to be one even where the walk missed it,
  // and it carries no place — so a definition asked at that name is no answer rather
  // than one that points somewhere else.
  const tokens: SemanticToken[] = [];
  const emitter = emitterInto(tokens, 2, bindingsIn(DECLARATIONS, itemsOnLine(SOURCE)));
  const parameters = signatureRoles(METHOD, [{ kind: "ident", text: "tp", startChar: 0 }], 2, emitter);
  assert.deepEqual(Object.fromEntries(parameters), { d: undefined, err: undefined });
  assert.deepEqual(tokens, [], "no name of that line is a parameter of this signature");
});
