import assert from "node:assert/strict";
import { readFileSync, writeFileSync } from "node:fs";
import { createRequire } from "node:module";
import { join } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import test from "node:test";

import { discard, tree } from "./definition-wire-fixture.ts";
import { holding } from "./harness.ts";

// The other end of the wire claim. The server answers `textDocument/definition` and a
// suite drives it over its own stdio to prove it ([goal-definition.test.ts](./goal-definition.test.ts)),
// but a server that answers is not a reader that is sent anywhere: this extension builds
// its own LSP client rather than a library one, so every feature the editor routes to a
// provider is one this extension has to register itself. The roles are registered; the
// definitions were not, and a go-to-definition in the editor therefore asked nothing and
// found nothing, which reads exactly like a file with no declarations in it.
//
// What is checked here is the client half, in the one place it can be checked outside an
// editor: the request this extension sends and the reading of what comes back, which are
// pure and are therefore in a file of their own that requires nothing from the editor. The
// registration itself is a statement about the extension's own source, read here as the
// file it is rather than against a copy, because a value the check keeps honest can only
// be judged where a reader finds it.

const ROOT = fileURLToPath(new URL("../../../../", import.meta.url));
const SCRIPTS = join(ROOT, ".agents", "vscode", "extensions", "khayyam-language", "scripts");
const require = createRequire(join(SCRIPTS, "adapter-base.js"));
const adapter = require("./definition.js") as {
  definitionRequest(uri: string, position: { line: number; character: number }): unknown;
  readTarget(answer: unknown): { uri: string; range: unknown } | null;
};

test("the request the client sends is the one the server answers", () => {
  assert.deepEqual(adapter.definitionRequest("file:///c:/w/set.kh", { line: 4, character: 11 }), {
    textDocument: { uri: "file:///c:/w/set.kh" },
    position: { line: 4, character: 11 },
  });
});

test("an answer that names a place is read as that place", () => {
  // The editor is sent a document and a range, and nothing else: the server's answer
  // carries no name and no role, and a place is all a definition is
  // ([definition.ts](../src/definition.ts)).
  assert.deepEqual(
    adapter.readTarget({
      uri: "file:///c:/w/math/boolean.kh",
      range: { start: { line: 1, character: 3 }, end: { line: 1, character: 8 } },
    }),
    {
      uri: "file:///c:/w/math/boolean.kh",
      range: { start: { line: 1, character: 3 }, end: { line: 1, character: 8 } },
    },
  );
});

test("no definition stays no definition, and is not read as a place", () => {
  // A name nothing declares answers with nothing, and nothing is the answer the editor
  // reads as "there is nothing to go to" — not as a place at the start of the file,
  // which is what an answer read leniently would send a reader to.
  assert.equal(adapter.readTarget(null), null);
  assert.equal(adapter.readTarget(undefined), null);
});

test("an answer that is not a place is refused by name, the way a token stream with no tokens is", () => {
  // Answering something rather than failing is how a dead request came to a reader as a
  // document with no roles, and cost three rounds to tell apart. So an answer this
  // cannot read is said, and the editor is sent nothing.
  for (const answer of [{}, { uri: "file:///c:/w/a.kh" }, { range: {} }, { uri: 1, range: {} }, 7, "a.kh", []]) {
    assert.throws(() => adapter.readTarget(answer), /definition/i, JSON.stringify(answer));
  }
});

test("the extension registers a definition provider over the language, and sends the request", () => {
  // The registration is what makes the editor ask at all: a provider that does not exist
  // is a request no reader makes, and the answer the server is ready with never reaches
  // one. This reads the extension's own source because a registration is a fact about
  // that file and about nothing else.
  const client = readFileSync(join(SCRIPTS, "client.js"), "utf8");
  assert.match(client, /registerDefinitionProvider/, "no provider is registered, so nothing is asked");
  assert.match(client, /textDocument\/definition/, "the provider sends no request the server answers");
  assert.match(
    client,
    /definitionProvider/,
    "the server's own capability is not read, so the client does not know the server answers definitions",
  );
});

test("the extension's own request, over the real server, is answered with what the server can account for", async (t) => {
  // The two halves together, which is the only claim that is the goal: this extension's
  // request, sent the way its provider sends it and read the way its reader reads it,
  // against the running server. What the server can account for today is a name the
  // document declares itself, and a name that arrived by an address is refused with a
  // reason — so the answer here is a place for one and nothing for the other, and the
  // extension's reader turns each into what the editor needs. A server that answered a
  // request nothing sends is not a feature, and this is the check that the request exists.
  const files = tree();
  t.after(() => discard(files));
  const source = ["tp Capsule cp {}", "tp Run mt (self Capsule) () () {", "\tEnter()()", "}", ""].join("\n");
  writeFileSync(join(files.root, "set.kh"), source, "utf8");
  const server = await holding(source, { uri: files.uri });
  t.after(() => server.stop());

  // Asked the way the provider asks it: the parameters come from the extension's own file.
  const asked = adapter.definitionRequest(files.uri, { line: 1, character: 3 }) as {
    textDocument: { uri: string };
    position: { line: number; character: number };
  };
  const answer = await server.request<unknown>("textDocument/definition", asked);
  const target = adapter.readTarget(answer);
  assert.ok(target, "a name the document declares is one the extension is sent to");
  assert.equal(target.uri, files.uri);
  const range = target.range as { start: { line: number; character: number }; end: { line: number; character: number } };
  assert.equal(source.split("\n")[range.start.line]!.slice(range.start.character, range.end.character), "Run");

  // And a name that arrived by an address is refused rather than guessed at, which the
  // extension's reader answers as no definition and the editor shows as nothing to go to.
  const claimed = ['tp Bool in "math/boolean.kh"', "tp Run mt (self Bool) () () {", "\tBool.IsTrue()", "}", ""].join("\n");
  server.notify("textDocument/didChange", {
    textDocument: { uri: files.uri, version: 2 },
    contentChanges: [{ text: claimed }],
  });
  const [published] = await server.publishedFor(files.uri);
  const refused = await server.request<unknown>("textDocument/definition", {
    textDocument: { uri: files.uri },
    position: { line: 2, character: 4 },
  });
  assert.equal(adapter.readTarget(refused), null, "nothing to send a reader to, and no wrong place instead");
  assert.match(published.message, /an address is resolved through the declaring file of the project/);
});
