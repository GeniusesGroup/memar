import assert from "node:assert/strict";
import test from "node:test";

import { answer, discard, NO_MANIFEST, tree } from "./definition-wire-fixture.ts";
import { holding, Server } from "./harness.ts";
import { characterOn, linesOf } from "./definition-fixture.ts";

// A definition that would have to leave the document, over the wire. The base an address is
// resolved from is the manifest of the module that wrote it, and where such a manifest is
// looked for is not ruled, so nothing looks for one and the address resolves by nothing.
// So the honest answer to a question about a name that arrived by an address is nothing,
// and the publication beside it says what is missing.
//
// That is a refusal and not a missing feature left unnoticed, and these tests are what say
// so: a reader who followed one of these names before this ruling was sent to a place this
// toolchain could not account for, and one who follows it now is told why there is nowhere
// to go. What changes when a manifest exists is what `resolve` answers, and nothing here
// knows anything about a manifest.

const SOURCE = [
  'tp Bool in "math/boolean.kh"',
  "tp Run mt (self Bool) () () {",
  "\tBool.IsTrue()",
  "}",
  "",
].join("\n");

test("a name that arrived by an address reaches no place, because nothing declares how the address resolves", async (t) => {
  const files = tree();
  t.after(() => discard(files));
  const server = await holding(SOURCE, { uri: files.uri });
  t.after(() => server.stop());

  assert.equal(await answer(server, files.uri), null, "there is nowhere to send a reader to");
  const [published] = await server.firstPublishedFor(files.uri);
  assert.equal(published.code, "unresolved-import", "and the document says so where the claim stands");
  assert.match(published.message, NO_MANIFEST, "naming what is missing rather than a file that may be there");
  assert.match(published.message, new RegExp(files.uri.replace(/\\/g, "\\\\")), "and the document that made the claim");
});

test("the workspace a client states is not what resolves an address, and both clients are answered the same", async (t) => {
  // The base used to come off the wire, which made this server right only for a reader who
  // opened the root and wrong for every reader who opened a folder inside it. The base is
  // the manifest of the module that wrote the address now, and a client's window is not
  // that module, so what a client says about which folder it has open is a fact about the
  // client and not about where an address resolves.
  const files = tree();
  t.after(() => discard(files));
  const workspace = `file:///${files.root.replace(/\\/g, "/")}`;

  const asFolder = new Server();
  try {
    await asFolder.request("initialize", {
      processId: process.pid,
      rootUri: null,
      workspaceFolders: [{ uri: workspace, name: "khayyam" }],
      capabilities: {},
    });
    asFolder.notify("initialized", {});
    asFolder.notify("textDocument/didOpen", { textDocument: { uri: files.uri, version: 1, text: SOURCE } });
    assert.equal(await answer(asFolder, files.uri), null, "a client that states a folder is answered the same");
  } finally {
    asFolder.stop();
  }

  const stating = await holding(SOURCE, { uri: files.uri, workspace });
  try {
    assert.equal(await answer(stating, files.uri), null, "and a client that states a root is answered the same");
  } finally {
    stating.stop();
  }
});

test("a name the document declares itself still reaches its place, whatever the address beside it does", async (t) => {
  // The refusal is about the address, and it must not spread to the rest of the file: a
  // reader whose file has one unresolvable address can still be sent to every declaration
  // the file makes, and a server that refused the whole file would have nothing to say.
  const files = tree();
  t.after(() => discard(files));
  const source = [SOURCE.replace("\tBool.IsTrue()", "\tRun.Enter()()"), "tp Own cp {}\n", ""].join("\n");
  const server = await holding(source, { uri: files.uri });
  t.after(() => server.stop());
  const lines = linesOf(source);
  const own = await server.request("textDocument/definition", {
    textDocument: { uri: files.uri },
    position: { line: 2, character: characterOn(lines, 2, "Run") },
  });
  assert.deepEqual(own, {
    uri: files.uri,
    range: { start: { line: 1, character: 3 }, end: { line: 1, character: 6 } },
  });
  assert.equal((await server.firstPublishedFor(files.uri)).length, 1, "and the one claim is still the one claim");
});
