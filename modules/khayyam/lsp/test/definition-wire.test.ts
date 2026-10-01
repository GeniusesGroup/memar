import assert from "node:assert/strict";
import test from "node:test";

import { holding, PROBE, Server } from "./harness.ts";
import type { Location } from "./wire.ts";
import { characterOn, linesOf } from "./definition-fixture.ts";

// What a definition is on the wire: a document and a range, or nothing. These drive the
// real server over its own stdio, because a statement about the wire is only checkable on
// the wire — a unit test of a helper passes whatever shape the helper was handed.
//
// Every document here is one this file wrote. [`main.kh`](../../../../main.kh) is the
// owner's test file for the language and the extension, and the corpus is an unreviewed
// archive: a shape pinned to either is a shape that changes when someone curates either.

const SOURCE = [
  "tp Buffer cp {}",
  "vr held Buffer",
  "tp Run mt (self Buffer) (n U8) () {",
  "\tvr scratch Buffer",
  "\tscratch.Copy(n)(held)",
  "}",
  "",
].join("\n");

const LINES = linesOf(SOURCE);
/** The character a parameter's name stands at in a signature, found from the parenthesis it
 *  is written in: the name is a letter that occurs earlier in the line — in `Run`, in
 *  `Buffer` — and an index of the name alone would point at one of those. */
const slotOf = (lines: string[], line: number, written: string) => characterOn(lines, line, written) + 1;
/** What the server answers on the wire for the name standing on a line, which is the
 *  question these tests are about — not what the toolchain's own function answers for
 *  the same position, which the unit tests in this set already cover. */
const ask = (server: Server, line: number, name: string) =>
  server.request<Location | null>("textDocument/definition", {
    textDocument: { uri: PROBE },
    position: { line, character: characterOn(LINES, line, name) },
  });

test("the server declares that it answers definitions", async (t) => {
  const server = new Server();
  t.after(() => server.stop());
  const initialized = await server.request<{ capabilities: { definitionProvider: boolean } }>(
    "initialize",
    { processId: process.pid, rootUri: null, capabilities: {} },
  );
  // A capability the client reads before it asks for anything: a provider the server
  // does not declare is one the editor never sends the request to, so the answer below
  // would be a claim about a request no reader makes.
  assert.equal(initialized.capabilities.definitionProvider, true);
});

test("a name in a body reaches the slot that declares it, over the wire", async (t) => {
  const server = await holding(SOURCE);
  t.after(() => server.stop());
  const signature = 2;
  const use = 4;
  assert.deepEqual(await ask(server, use, "scratch"), {
    uri: PROBE,
    range: {
      start: { line: 3, character: characterOn(LINES, 3, "scratch") },
      end: { line: 3, character: characterOn(LINES, 3, "scratch") + 7 },
    },
  });
  assert.deepEqual(await ask(server, use, "n"), {
    uri: PROBE,
    range: {
      start: { line: signature, character: slotOf(LINES, signature, "(n U8)") },
      end: { line: signature, character: slotOf(LINES, signature, "(n U8)") + 1 },
    },
  });
  // The same answer at the declaration itself: one binding answers at every position it
  // stands in, and a definition that answered the use only would say otherwise.
  assert.deepEqual(await ask(server, 3, "scratch"), await ask(server, use, "scratch"));
  assert.deepEqual(await ask(server, 4, "held"), {
    uri: PROBE,
    range: {
      start: { line: 1, character: characterOn(LINES, 1, "held") },
      end: { line: 1, character: characterOn(LINES, 1, "held") + 4 },
    },
  });
});

test("a position standing on no name answers nothing, and that is an answer", async (t) => {
  const server = await holding(SOURCE);
  t.after(() => server.stop());
  for (const [line, character] of [[0, 0], [4, 0], [6, 0]] as const) {
    assert.equal(
      await server.request<Location | null>("textDocument/definition", {
        textDocument: { uri: PROBE },
        position: { line, character },
      }),
      null,
      `${line}:${character}`,
    );
  }
});

test("a definition is answered from the text the document was last changed to", async (t) => {
  // The document is what the server holds, so a definition asked after a change is
  // about the changed text. A signature that gained a group moves the slot the
  // parameter is declared at, and the answer has to move with it rather than stay where
  // it was when the question was first put.
  const after = SOURCE.replace("(n U8)", "(x U8) (n U8)");
  const server = await holding(SOURCE);
  t.after(() => server.stop());
  const before = await ask(server, 4, "n");
  assert.equal(before?.range.start.character, slotOf(LINES, 2, "(n U8)"));

  server.notify("textDocument/didChange", {
    textDocument: { uri: PROBE, version: 2 },
    contentChanges: [{ text: after }],
  });
  await server.publishedFor(PROBE);
  const moved = await ask(server, 4, "n");
  const afterLines = linesOf(after);
  assert.equal(moved?.range.start.character, slotOf(afterLines, 2, "(n U8)"));
  assert.notEqual(
    moved?.range.start.character,
    before?.range.start.character,
    "the slot moved, so the test is about the change and not about a coincidence",
  );
});

test("a document this server holds no text for is refused by name, the way roles are", async (t) => {
  const server = await holding(SOURCE);
  t.after(() => server.stop());
  await assert.rejects(
    () =>
      server.request("textDocument/definition", {
        textDocument: { uri: "file:///c:/scratch/never-opened.kh" },
        position: { line: 0, character: 0 },
      }),
    /textDocument\/didOpen never arrived/,
    "an empty answer for a document the server never read would be a fault read as a success",
  );
});
