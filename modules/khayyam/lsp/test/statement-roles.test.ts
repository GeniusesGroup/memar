import assert from "node:assert/strict";
import test from "node:test";

import { bindingsIn } from "../src/binding-table.ts";
import { type Item, type Place } from "../src/document-items.ts";
import { emitterInto, type SemanticToken } from "../src/role-emitter.ts";
import { statementRoles, type StatementScope } from "../src/statement-roles.ts";

// What a line that declares nothing says about the names standing on it: a statement
// inside a method body, or a line outside any declaration. The two are one walk,
// because a bare use is a bare use either way — what the body adds is the knowledge
// the body has (a parameter of the method above, a variable this body declared), and
// that is what this measures on its own.

/** Nothing is bound here, so every name is answered by what the walk says about it
 *  rather than by what the document declares — which is what makes a bare use visible. */
const NOTHING_BOUND = bindingsIn([], new Map<number, Item[]>());

/** One line walked with one body behind it, and the tokens it answered with. */
function answered(items: Item[], scope: StatementScope | undefined): SemanticToken[] {
  const tokens: SemanticToken[] = [];
  statementRoles(items, scope, emitterInto(tokens, 0, NOTHING_BOUND));
  return tokens;
}

const IN_A_BODY: StatementScope = {
  parameters: new Map([["err", { line: 4, startChar: 3, length: 3 } as Place]]),
  declares: (text) =>
    text === "scratch"
      ? {
          role: "method-local",
          origin: "the variable scratch declared in this body",
          place: { line: 5, startChar: 3, length: 6 },
        }
      : undefined,
  declaresMethod: () => false,
};

const ident = (text: string, startChar = 0): Item => ({ kind: "ident", text, startChar });
const punct = (text: string, startChar = 0): Item => ({ kind: "punct", text, startChar });

test("a name before the opening parenthesis is a Method called there", () => {
  // The dot operator is the language's only invocation form, so the name before the
  // parenthesis is a Method — the same role it carries at its declaration.
  const tokens = answered([ident("Copy"), punct("("), punct(")")], IN_A_BODY);
  assert.deepEqual(
    tokens.map((token) => `${token.text}:${token.role}`),
    ["Copy:method"],
  );
  assert.equal(tokens[0]!.resolvedTo, "a Method called here");
  assert.equal(tokens[0]!.declaredAt, undefined, "a call site is not a place a name is declared at");
});

test("a parameter keeps the parameter role wherever in the body it is used", () => {
  const tokens = answered([ident("err"), punct("("), ident("reader"), punct(")")], IN_A_BODY);
  assert.deepEqual(
    tokens.map((token) => `${token.text}:${token.role}`),
    ["err:method-argument", "reader:identifier-reference"],
  );
  assert.equal(tokens[0]!.resolvedTo, "a parameter of the method above");
  assert.deepEqual(tokens[0]!.declaredAt, { line: 4, startChar: 3, length: 3 });
});

test("a name the body declared carries its role at its use", () => {
  const tokens = answered([ident("scratch")], IN_A_BODY);
  assert.equal(tokens[0]!.role, "method-local");
  assert.equal(tokens[0]!.resolvedTo, "the variable scratch declared in this body");
  assert.deepEqual(tokens[0]!.declaredAt, { line: 5, startChar: 3, length: 6 });
});

test("punctuation is not a name, and the words around it are answered one by one", () => {
  const tokens = answered(
    [punct("("), ident("vr"), ident("mt"), { kind: "string", text: "2", startChar: 12 }, ident("greet")],
    IN_A_BODY,
  );
  assert.deepEqual(
    tokens.map((token) => `${token.text}:${token.role}`),
    ["vr:keyword", "mt:subtype", '"2":string', "greet:identifier-reference"],
  );
  assert.equal(tokens[0]!.resolvedTo, "reserved word");
  assert.equal(tokens[3]!.resolvedTo, "not bound in this file");
});

test("a quoted literal carries no place and no URI", () => {
  // The quotes are part of the extent a token must cover, so the emitted token stands
  // one character back; and nothing is declared in a literal, so the two places a token
  // could name are both absent rather than empty.
  const tokens = answered([{ kind: "string", text: "2", startChar: 12 }], IN_A_BODY);
  assert.deepEqual(tokens, [
    {
      line: 0,
      startChar: 11,
      length: 3,
      role: "string",
      text: '"2"',
      resolvedTo: "a quoted literal, which no inclusion states here",
    },
  ]);
});

test("with no body behind it, a call form is a bare use and nothing more", () => {
  // A line outside any declaration declares nothing, and the knowledge a method body
  // gives a line — that a name before a parenthesis is a Method called here — is
  // knowledge about that body. Outside one, every name is what the document binds.
  const tokens = answered([ident("Copy"), punct("("), ident("greet")], undefined);
  assert.deepEqual(
    tokens.map((token) => `${token.text}:${token.role}`),
    ["Copy:identifier-reference", "greet:identifier-reference"],
  );
});

test("a call to a Method this file declares is resolved against its declaration, not the position", () => {
  // The parenthesis says the name is called; the declaration says which Method it is. A
  // role follows the binding, never the position, so a Method the document declares is
  // answered by the same table every other name is — and it carries the place it is
  // declared at, which is what a definition asked at the call site is read from.
  const byLine = new Map<number, Item[]>([
    [7, [ident("tp", 0), ident("Greet", 3), ident("mt", 9)]],
  ]);
  const declared = bindingsIn(
    [
      {
        form: "tp-mt",
        name: "Greet",
        line: 8,
        owner: [],
        influencing: [],
        influenced: [],
        body: null,
      },
    ],
    byLine,
  );
  const tokens: SemanticToken[] = [];
  statementRoles(
    [ident("Greet"), punct("("), punct(")")],
    { ...IN_A_BODY, declaresMethod: (text) => declared.bindingOf(text)?.form === "tp-mt" },
    emitterInto(tokens, 0, declared),
  );
  assert.deepEqual(
    tokens.map((token) => `${token.text}:${token.role}`),
    ["Greet:method"],
  );
  assert.equal(tokens[0]!.resolvedTo, "Greet is a Method declared in this file");
  assert.deepEqual(tokens[0]!.declaredAt, { line: 7, startChar: 3, length: 5 });
});
