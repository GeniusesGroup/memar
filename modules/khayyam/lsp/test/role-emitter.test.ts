import assert from "node:assert/strict";
import test from "node:test";

import { bindingsIn } from "../src/binding-table.ts";
import { itemsOnLine, type Item } from "../src/document-items.ts";
import { emitterInto, type Emitter, type SemanticToken } from "../src/role-emitter.ts";
import { readUnit } from "../../core/src/parse.ts";

// How one occurrence's role becomes a token: the extent the editor draws over, the role
// it draws it with, the sentence saying what the name IS, where it was declared, and the
// URI it arrived through when it arrived by an inclusion. Everything a token carries
// beyond the role name is what makes it readable and checkable rather than a colour, so
// the whole shape is pinned here — the stream tests read the roles and nothing else.

const SOURCE = [
  'tp Bool in "math/boolean"',
  "tp Reader ab",
  "vr held Reader",
  "",
].join("\n");
const BY_LINE = itemsOnLine(SOURCE);
const LINE = 2;

/** One document's bindings, over the items of the lines the reading walked. */
function theBindings(source = SOURCE): ReturnType<typeof bindingsIn> {
  return bindingsIn(readUnit("document.kh", source).unit.declarations, itemsOnLine(source));
}

/** One answer emitted over one line, and the token that came of it. */
function emittedBy(answer: (emitter: Emitter) => void, bound = theBindings(), line = LINE): SemanticToken[] {
  const tokens: SemanticToken[] = [];
  answer(emitterInto(tokens, line, bound));
  return tokens;
}

function itemOn(line: number, text: string): Item {
  return BY_LINE.get(line)!.find((candidate) => candidate.text === text)!;
}

test("a bound name carries its role, what it is, and where it was declared", () => {
  // A definition asked at this occurrence is the place in the third field, and the
  // sentence in the fourth is why the name IS that role rather than where it appears.
  assert.deepEqual(emittedBy((emitter) => emitter.resolve(itemOn(2, "held"), "identifier-reference")), [
    {
      line: 2,
      startChar: 3,
      length: 4,
      role: "variable",
      text: "held",
      resolvedTo: "held is a Variable declared in this file",
      declaredAt: { line: 2, startChar: 3, length: 4 },
      includedThrough: undefined,
    },
  ]);
});

test("a name that arrived by an inclusion is bound here and carries the URI it came through", () => {
  const [token] = emittedBy((emitter) => emitter.resolve(itemOn(0, "Bool"), "type-reference"));
  assert.equal(token!.role, "included-type");
  assert.equal(token!.resolvedTo, "Bool is included from another file");
  assert.equal(token!.declaredAt, undefined, "the declaration stands in another file, so there is no place here");
  assert.equal(token!.includedThrough, "math/boolean", "and this is where the question of its definition goes on to");
});

test("a name nothing binds is answered with the role the caller asked for, and says so", () => {
  // The fallback is what a renderer says when the file states no origin for the name,
  // so which role that is belongs to the caller; what this file states is that nothing
  // here binds it, and that is said rather than left to be inferred from a missing place.
  assert.deepEqual(
    emittedBy((emitter) => emitter.resolve({ kind: "ident", text: "absent", startChar: 0 }, "identifier-reference"), theBindings("")),
    [
      {
        line: 2,
        startChar: 0,
        length: 6,
        role: "identifier-reference",
        text: "absent",
        resolvedTo: "not bound in this file",
        declaredAt: undefined,
        includedThrough: undefined,
      },
    ],
  );
});

test("a role may be emitted for an item without a name being resolved at all", () => {
  // A reserved word, a subtype, a field's name and a call site are named by what
  // stands there rather than by a binding, so the role is emitted directly and carries
  // no place.
  assert.deepEqual(emittedBy((emitter) => emitter.at(itemOn(0, "tp"), "keyword", "reserved word")), [
    {
      line: 2,
      startChar: 0,
      length: 2,
      role: "keyword",
      text: "tp",
      resolvedTo: "reserved word",
      declaredAt: undefined,
      includedThrough: undefined,
    },
  ]);
});

test("a quoted form is emitted over its quotes, and declares nothing", () => {
  // The quotes are part of the extent a token must cover, so the token stands one
  // character back from the item and carries two more; and nothing is declared in a
  // literal, so the two fields that could name a place are absent rather than empty.
  const item = BY_LINE.get(0)!.find((candidate) => candidate.kind === "string")!;
  assert.deepEqual(emittedBy((emitter) => emitter.overQuotes(item, "file-uri", "the path math/boolean routes to"), theBindings(), 0), [
    {
      line: 0,
      startChar: 11,
      length: 14,
      role: "file-uri",
      text: '"math/boolean"',
      resolvedTo: "the path math/boolean routes to",
    },
  ]);
});
