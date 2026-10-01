import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import test from "node:test";

import { holding, PROBE as URI, Server } from "./harness.ts";
import type { Diagnostic, Frame } from "./wire.ts";

// The synchronization capability is a statement about the wire, so it is measured on
// the wire: these drive the real server over its own stdio, the way the extension
// does, and a unit test of a helper would pass whatever shape the helper was given.
// How to speak to the server is [harness.ts](./harness.ts), which the definitions'
// wire tests use too.

/** The repository's own scratch file, read as a file rather than pasted as a string, so
 *  a question about a position in it is a question about a line of text that exists. */
const MAIN = fileURLToPath(new URL("../../../../main.kh", import.meta.url));

/** The owner's scratch file's shape, as the suite already carries it: a `>` the
 *  grammar has no form for takes the brace standing behind it, and the brace the
 *  block needed is the one left over with nothing to close. */
const FAULTY = [
  'tp Error in ""',
  "tp Capsule cp {}",
  "tp Run mt (self Capsule) (d Capsule) () {",
  "    tp step sc {",
  "        if d>1 {",
  "        }",
  "    }",
  "}",
  "",
].join("\n");
const CORRECTED = FAULTY.replace("if d>1 {", "if BiggerThan(d)(One) {");

test("the declared capability is Full, and a Full change is the shape that is read", async (t) => {
  const server = new Server();
  t.after(() => server.stop());
  const initialized = await server.request<{
    capabilities: { textDocumentSync: { openClose: boolean; change: number } };
  }>("initialize", { processId: process.pid, rootUri: null, capabilities: {} });
  // Full is `change: 1`, and Full is a statement about what the client sends: the whole
  // document's text, once, with no range. The whole test below is what that statement
  // has to buy, so the number is asserted rather than trusted.
  assert.equal(initialized.capabilities.textDocumentSync.change, 1);
  assert.equal(initialized.capabilities.textDocumentSync.openClose, true);
});

test("a corrected document is read whole, so its fault clears and its roles follow the text", async (t) => {
  const server = await holding(FAULTY);
  t.after(() => server.stop());
  const atOpen = await server.firstPublishedFor(URI);
  assert.deepEqual(
    atOpen.map((diagnostic) => `${diagnostic.code}@${diagnostic.range.start.line + 1}`),
    [
      "unexpected-character@5",
      "declaration-form@8",
      // The file's first line claims a name arrives through `""`, and nothing is behind
      // an empty path — so the claim is reported as well as the two faults of reading. The
      // two kinds of diagnostic are published together and neither stands for the other:
      // before this one existed, a file claiming something nothing accounted for reached
      // a reader as a file the toolchain had no trouble with.
      "unresolved-import@1",
    ],
    "the file as opened is read with the fault it has and the claim it cannot account for",
  );
  const tokensAtOpen = await server.tokensFor(URI);

  // What the client sends under a Full declaration: the whole text, once, no range.
  server.notify("textDocument/didChange", {
    textDocument: { uri: URI, version: 2 },
    contentChanges: [{ text: CORRECTED }],
  });
  const afterChange = await server.publishedFor(URI);
  // The two faults of reading are gone, and the claim that nothing accounts for is not:
  // the change fixed the body, not the inclusion, and a publication that said so is the
  // only way a client learns which of the two kinds of diagnostic a change cleared.
  assert.deepEqual(
    afterChange.map((diagnostic) => diagnostic.code),
    ["unresolved-import"],
    "a change that fixes reading does not clear a claim it did not fix, and neither does it keep the fault it did clear",
  );

  const tokens = await server.tokensFor(URI);
  assert.notDeepEqual(tokens, tokensAtOpen, "the roles must be asked for again and differ");
  // The roles are the corrected text's, not the open's: the corrected line carries the
  // invocation the fault had swallowed, and the roles stand where the corrected text
  // has them. (delta line, delta start, length, type - 0 is the contract's first role.)
  const lines = CORRECTED.split("\n");
  const placed: string[] = [];
  let line = 0;
  let character = 0;
  for (let at = 0; at < tokens.length; at += 5) {
    line += tokens[at]!;
    character = tokens[at] === 0 ? character + tokens[at + 1]! : tokens[at + 1]!;
    placed.push(lines[line]!.slice(character, character + tokens[at + 2]!));
  }
  assert.deepEqual(placed, [
    "tp", "Error", "in", '""',
    "tp", "Capsule", "cp",
    "tp", "Run", "mt", "Capsule", "d", "Capsule",
    "tp", "step", "sc",
    "if", "BiggerThan", "d", "One",
  ]);
});

test("a change carrying a range is refused by name, and the document is left as it was", async (t) => {
  const server = await holding(FAULTY);
  t.after(() => server.stop());
  server.notify("textDocument/didChange", {
    textDocument: { uri: URI, version: 2 },
    contentChanges: [{ text: CORRECTED }],
  });
  assert.deepEqual((await server.publishedFor(URI)).map((d) => d.code), ["unresolved-import"]);
  const before = await server.tokensFor(URI);

  // The shape the client used to send, under a capability that does not admit it. A
  // server that applied it would be answering about a document no editor holds, and
  // the fault the reader corrected would stay on the line with nothing saying why.
  server.notify("textDocument/didChange", {
    textDocument: { uri: URI, version: 3 },
    contentChanges: [
      {
        text: "Bigger",
        range: { start: { line: 4, character: 11 }, end: { line: 4, character: 20 } },
      },
    ],
  });
  const refused = await server.publishedFor(URI);
  const [refusal] = refused;
  assert.equal(refused.length, 1, "the mismatch is one diagnostic, on the document it is about");
  assert.equal(refusal!.code, "text-document-sync", "it is named by what it contradicts");
  // Named by the capability, by the field that contradicts it, and by what the reader
  // is looking at now: none of the three can be acted on without the other two.
  assert.match(refusal!.message, /textDocumentSync\.change is 1 \(Full\)/);
  assert.match(refusal!.message, /contentChanges\[0\] carries the range/);
  assert.match(refusal!.message, /not about the file on screen/);
  assert.deepEqual(await server.tokensFor(URI), before, "the refused change did not reach the text");
});

test("the next change of the declared shape takes the refusal off the file", async (t) => {
  const server = await holding(FAULTY);
  t.after(() => server.stop());
  server.notify("textDocument/didChange", {
    textDocument: { uri: URI, version: 2 },
    contentChanges: [{ text: CORRECTED }],
  });
  await server.publishedFor(URI);
  server.notify("textDocument/didChange", {
    textDocument: { uri: URI, version: 3 },
    contentChanges: [{ text: "Bigger", range: { start: { line: 4, character: 11 }, end: { line: 4, character: 20 } } }],
  });
  assert.equal((await server.publishedFor(URI))[0]!.code, "text-document-sync");

  // A client that reads the refusal and sends what the server declared is not left
  // carrying it: the mismatch is a property of the payload, not a mark on the file.
  server.notify("textDocument/didChange", {
    textDocument: { uri: URI, version: 4 },
    contentChanges: [{ text: FAULTY }],
  });
  assert.deepEqual(
    (await server.publishedFor(URI)).map((diagnostic) => diagnostic.code),
    ["unexpected-character", "declaration-form", "unresolved-import"],
  );
});

test("a change of more than one entry is refused, for the same reason", async (t) => {
  const server = await holding(FAULTY);
  t.after(() => server.stop());
  server.notify("textDocument/didChange", {
    textDocument: { uri: URI, version: 2 },
    contentChanges: [{ text: FAULTY }, { text: CORRECTED }],
  });
  const [refusal] = await server.publishedFor(URI);
  assert.equal(refusal!.code, "text-document-sync");
  assert.match(refusal!.message, /which is one content change carrying the whole document/);
  assert.match(refusal!.message, /carries 2\./);
});

test("a fault that follows another names it, its line, and what it cost", async (t) => {
  const server = await holding(FAULTY);
  t.after(() => server.stop());
  const [, consequence] = await server.firstPublishedFor(URI);
  assert.ok(consequence, "the file's two faults are both reported; neither is suppressed");
  // The closing brace left over at line 8 closes nothing, and standing alone it reads
  // as a stray form no declaration takes - true of every stray brace, and no reason to
  // go to line 5. So it names the fault it follows from, the line that fault stands
  // on, and what that fault cost, which is the brace that went with it.
  assert.equal(consequence!.range.start.line + 1, 8);
  assert.equal(
    consequence!.message,
    'declaration-form at line 8, column 1 — "}": a form no declaration takes here.' +
      " It follows from the unexpected-character at line 5: the rest of that line was not read," +
      " and a brace went with it, so this closing brace has nothing left to close." +
      " That declaration was not read; the lines around it still were.",
  );
});

test("a document this server holds no text for is refused by name, the way a definition is", async (t) => {
  // The same boundary the definitions are answered under, measured on the wire: an empty
  // token stream is a real answer for a real document, and must not be one for a document
  // that did not reach this server at all.
  const server = await holding(FAULTY);
  t.after(() => server.stop());
  await assert.rejects(
    () => server.tokensFor("file:///c:/scratch/never-opened.kh"),
    /textDocument\/didOpen never arrived/,
    "a fault answered as an empty token stream reads as a working server",
  );
});

/** The stream's own text: every token as {line, character, length, type}, with the
 *  type the legend the server advertised says it is. The deltas are the wire's shape,
 *  so they are walked rather than assumed. */
function placed(tokens: number[], legend: string[]): Array<{ line: number; character: number; length: number; type: string }> {
  const out: Array<{ line: number; character: number; length: number; type: string }> = [];
  let line = 0;
  let character = 0;
  for (let at = 0; at < tokens.length; at += 5) {
    line += tokens[at]!;
    character = tokens[at] === 0 ? character + tokens[at + 1]! : tokens[at + 1]!;
    out.push({ line, character, length: tokens[at + 2]!, type: legend[tokens[at + 3]!] ?? "not-in-legend" });
  }
  return out;
}

test("the stream carries a parameter's role at its use in a body as well as at its signature", async (t) => {
  // Measured on the wire against the repository's own file, because a question about
  // what the stream carries at a position is not answerable by reading the code that
  // builds it. The load-bearing rule of the display contract is that a name carries the
  // role of what it IS at every position, so the two answers have to be the same role
  // for the same name - and the editor's own reporting of a position is a separate
  // question, which this test does not speak to.
  const source = readFileSync(MAIN, "utf8");
  const lines = source.split("\n");
  const signature = 26;
  const use = 38;
  // The two positions are read out of the file rather than written here, so a change to
  // the file cannot leave this test asserting about a line that moved.
  const at = (line: number, text: string) => lines[line]!.indexOf(text);
  assert.ok(lines[signature]!.includes("err Error"), "the signature line is the one this test is about");
  assert.ok(lines[use]!.trimStart().startsWith("err."), "the body line is the one this test is about");

  const server = new Server();
  t.after(() => server.stop());
  const initialized = await server.request<{ capabilities: { semanticTokensProvider: { legend: { tokenTypes: string[] } } } }>(
    "initialize",
    { processId: process.pid, rootUri: null, capabilities: {} },
  );
  const legend = initialized.capabilities.semanticTokensProvider.legend.tokenTypes;
  server.notify("initialized", {});
  const uri = "file:///c:/scratch/main.kh";
  server.notify("textDocument/didOpen", { textDocument: { uri, version: 1, text: source } });

  const tokens = placed(await server.tokensFor(uri), legend);
  const answer = (line: number, character: number) =>
    tokens.filter((token) => token.line === line && token.character === character);
  assert.deepEqual(
    answer(signature, at(signature, "err Error")),
    [{ line: signature, character: at(signature, "err Error"), length: 3, type: "method-argument" }],
    "the parameter in the signature carries the role the contract gives it",
  );
  assert.deepEqual(
    answer(use, at(use, "err.Clone")),
    [{ line: use, character: at(use, "err.Clone"), length: 3, type: "method-argument" }],
    "the same parameter, used in the body, carries that same role in the stream the server sends",
  );
  // The neighbour on that line is there too, so the two answers are a pair rather than a
  // single token that happens to be alone: the method call is the one identity, and it
  // is a different role.
  assert.deepEqual(
    answer(use, at(use, "Clone")),
    [{ line: use, character: at(use, "Clone"), length: 5, type: "method" }],
    "the method called there is a method, and the stream says so beside the parameter",
  );
});
