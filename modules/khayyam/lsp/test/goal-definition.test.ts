import assert from "node:assert/strict";
import { writeFileSync } from "node:fs";
import { join } from "node:path";
import { pathToFileURL } from "node:url";
import test from "node:test";

import { discard, tree } from "./definition-wire-fixture.ts";
import { holding } from "./harness.ts";
import { characterOn, linesOf } from "./definition-fixture.ts";
import type { Location } from "./wire.ts";

// The goal, in one place and over the wire: a name in a method body, a parameter, a type
// and a variable that arrived by an `in`, and a declaration's own name — each to the place
// it is declared at, in one document, from the running server.
//
// Every other definition test in this folder answers one case, so that a failure says which
// case broke. This one states the goal itself, and the goal is the four of them together —
// which means it also states the one that is not answered yet and why, because a check that
// only says what works is a check of half a goal. The name that arrived by an address
// reaches no place, and what it reaches instead is a refusal naming the root that was found
// and the manifest that is not there
// ([modularity.handoff.md → Dependency Resolution and Companion Manifest](../../../../docs/khayyam/modularity.handoff.md)).
// The three names this document declares are answered whole.

const SOURCE = [
  'tp Error in "math/boolean.kh"', //         0  a type that arrived by an address
  "tp Capsule cp {}", //                          1  a declaration this file makes
  'vr external_vr in "math/boolean.kh"', //     2  a variable that arrived by one
  "tp Run mt (self Capsule) (n U8) () {", //     3  a parameter
  "\tvr scratch Capsule", //                      4  a declaration in a body
  "\tscratch.Copy(n)(external_vr)", //           5  a body naming three of them
  "}",
  "",
].join("\n");

const LINES = linesOf(SOURCE);
const at = (line: number, name: string): number => characterOn(LINES, line, name);

test("the three names this document declares reach the places they are declared at", async (t) => {
  const files = tree();
  t.after(() => discard(files));
  writeFileSync(join(files.root, "math", "boolean.kh"), ["tp Error ab {}", "vr external_vr U8", ""].join("\n"), "utf8");
  const server = await holding(SOURCE, { uri: files.uri });
  t.after(() => server.stop());
  const ask = (line: number, character: number) =>
    server.request<Location | null>("textDocument/definition", {
      textDocument: { uri: files.uri },
      position: { line, character },
    });
  const here = (line: number, name: string) => {
    const character = at(line, name);
    return { start: { line, character }, end: { line, character: character + name.length } };
  };

  // A name in a method body: the variable that body declared.
  assert.deepEqual(await ask(5, at(5, "scratch")), { uri: files.uri, range: here(4, "scratch") });
  // A parameter, asked where the body uses it and where the signature writes it. Its name
  // is a letter that occurs earlier in the line — in `Run` — so it is found from the
  // parentheses the signature writes it in.
  const parameter = {
    start: { line: 3, character: at(3, "(n U8)") + 1 },
    end: { line: 3, character: at(3, "(n U8)") + 2 },
  };
  assert.deepEqual(await ask(5, at(5, "n)")), { uri: files.uri, range: parameter });
  assert.deepEqual(await ask(3, at(3, "(n U8)") + 1), { uri: files.uri, range: parameter });
  // A declaration's own name, asked at the declaration and at a use of it: one place.
  assert.deepEqual(await ask(1, at(1, "Capsule")), { uri: files.uri, range: here(1, "Capsule") });
  assert.deepEqual(await ask(3, at(3, "Capsule")), await ask(1, at(1, "Capsule")));
});

test("the two names that arrived by an address reach no place, and are told why", async (t) => {
  // The fourth of the four, and the one the goal names that this toolchain does not
  // answer: an address is resolved through the declaring file of the project, and
  // where such a manifest is looked for is not ruled. The answer is a refusal that names
  // what is missing — not a place that may be wrong, and not a file reported missing that
  // may be there.
  const files = tree();
  t.after(() => discard(files));
  const server = await holding(SOURCE, { uri: files.uri });
  t.after(() => server.stop());
  const ask = (line: number, character: number) =>
    server.request<Location | null>("textDocument/definition", {
      textDocument: { uri: files.uri },
      position: { line, character },
    });

  assert.equal(await ask(0, at(0, "Error")), null, "a type that arrived by an address");
  assert.equal(await ask(5, at(5, "external_vr")), null, "and a variable that arrived by one");
  assert.equal(await ask(2, at(2, "external_vr")), null, "asked where the document names it too");

  const published = await server.firstPublishedFor(files.uri);
  assert.deepEqual(published.map((d) => d.code), ["unresolved-import", "unresolved-import"]);
  for (const diagnostic of published) {
    assert.match(diagnostic.message, /an address is resolved through the declaring file of the project/);
    assert.match(diagnostic.message, /declaring file, not a file/);
  }
});

test("a name is a name from inside it and not from the character after it", async (t) => {
  // The half of a reader's cursor this server answers on, and the half that is the
  // caller's to get right: a name ends where the next character begins, so the character
  // after a name is not inside that name — and on these lines it is a space, a closing
  // parenthesis or a line's end. A caller that asks one past the end is answered with
  // nothing, and nothing here is what a server that knows no definitions also answers, so
  // the two are indistinguishable in a log. Pinning the end of a name as a place that is
  // not that name is what keeps a caller from learning that the hard way.
  const files = tree();
  t.after(() => discard(files));
  const server = await holding(SOURCE, { uri: files.uri });
  t.after(() => server.stop());
  const ask = (line: number, character: number) =>
    server.request<Location | null>("textDocument/definition", {
      textDocument: { uri: files.uri },
      position: { line, character },
    });
  const inside = at(1, "Capsule");

  // Every character of the name answers the same place, so a caller's off-by-one is a
  // choice about which character of the name it aims at rather than about which name.
  for (let character = inside; character < inside + "Capsule".length; character += 1) {
    assert.notEqual(await ask(1, character), null, `asked inside the name at ${character}`);
  }
  assert.equal(await ask(1, inside + "Capsule".length), null, "and one past its end is not it");
  assert.equal(await ask(1, inside - 1), null, "and neither is the one before it, which is `tp `");
});
