import assert from "node:assert/strict";
import test from "node:test";

import { discard, NO_MANIFEST, tree } from "./definition-wire-fixture.ts";
import { holding } from "./harness.ts";
import type { Diagnostic } from "./wire.ts";

// What a reader is told about a document's claims on other files, measured on the wire —
// the claim and the fault are two answers and a publication carries both, so what is
// measured here is a reader's whole picture of one file rather than one of its two kinds.

const codesOf = (diagnostics: Diagnostic[]): string[] => diagnostics.map((d) => d.code);

test("a claim nothing accounts for is published, on the name, saying which address and what is missing", async (t) => {
  const files = tree();
  t.after(() => discard(files));
  const server = await holding('tp Bool in "math/nowhere.kh"\n', { uri: files.uri });
  t.after(() => server.stop());

  const published = await server.firstPublishedFor(files.uri);
  assert.deepEqual(codesOf(published), ["unresolved-import"]);
  assert.deepEqual(published[0]!.range.start, { line: 0, character: 3 }, "the claim stands on the name");
  assert.match(published[0]!.message, /math\/nowhere\.kh/, "and the sentence says which address");
  assert.match(published[0]!.message, NO_MANIFEST, "and what is missing rather than a file that may be there");
  assert.match(published[0]!.message, new RegExp(files.uri.replace(/\\/g, "\\\\")), "and the document that made the claim");
});

test("every claim in one file is refused by the same sentence, because the module that wrote them is one thing", async (t) => {
  // Three addresses, one refusal. This was two sentences two days ago — one naming a
  // missing file for each — and the specific version was the false one: two of those files
  // are present. The owner's ruling makes a claim's fault a fact about the module rather
  // than about the file behind the address, so the sentence is the same whatever address
  // stands there, and one mistake in a manifest reads as one mistake rather than as one
  // per referring line.
  const files = tree();
  t.after(() => discard(files));
  const source = [
    'tp Bool in "math/boolean.kh"',
    'tp Other in "math/nowhere.kh"',
    'vr third in "elsewhere/other.kh"',
    "",
  ].join("\n");
  const server = await holding(source, { uri: files.uri });
  t.after(() => server.stop());
  const published = await server.firstPublishedFor(files.uri);
  assert.deepEqual(codesOf(published), ["unresolved-import", "unresolved-import", "unresolved-import"]);
  for (const diagnostic of published) {
    assert.match(diagnostic.message, NO_MANIFEST);
    assert.match(diagnostic.message, /declaring file, not a file/);
  }
});

test("a document that claims nothing is published with nothing on it", async (t) => {
  const files = tree();
  t.after(() => discard(files));
  const server = await holding("tp A cp {}\n", { uri: files.uri });
  t.after(() => server.stop());
  assert.deepEqual(await server.firstPublishedFor(files.uri), [], "an empty publication is the clearing, and this is it");
});

test("a fault of reading and a claim nothing accounts for are published together, and neither stands for the other", async (t) => {
  // A file with a character the grammar has no form for AND an address that resolves to
  // nothing: one is reading, the other is a claim, and a reader who saw only the first
  // would think the file was whole.
  const files = tree();
  t.after(() => discard(files));
  const source = ['tp Bool in "math/nowhere.kh"', "tp A cp {", "    what>", "}", ""].join("\n");
  const server = await holding(source, { uri: files.uri });
  t.after(() => server.stop());
  const published = await server.firstPublishedFor(files.uri);
  assert.deepEqual(codesOf(published).sort(), ["unexpected-character", "unresolved-import"]);
});
