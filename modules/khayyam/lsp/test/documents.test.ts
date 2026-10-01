import assert from "node:assert/strict";
import test from "node:test";

import { change, close, diagnosticsFor, holds, open, text } from "../src/documents.ts";
import { emptyReach } from "./definition-fixture.ts";

// What the server holds about a document, and what it does about that on the wire. The
// synchronization tests check all of this over stdio against a server this code starts;
// what they cannot reach is which text the answers were computed from, and the refusal
// path of a change — the answer those tests get says a refusal was published, not what it
// was computed against.

const WHOLE = ["tp Reader ab", 'tp Broken in "unterminated', ""].join("\n");
const CORRECTED = "tp Reader ab\n";

/** What a publication carries, as the client reads it. */
function payloadOf(publication: string): {
  method: string;
  params: { uri: string; version: null; diagnostics: Array<{ code: string }> };
} {
  return JSON.parse(publication.split("\r\n\r\n")[1]!);
}

const codesOf = (diagnostics: unknown): string[] =>
  (diagnostics as Array<{ code: string }>).map((diagnostic) => diagnostic.code);

/** One document, opened at the text the suite hands over and held for the test that asked
 *  for it — the table is this process's, so a document left behind would be answered
 *  about by the next test. */
function holding(uri: string): void {
  open(uri, WHOLE, emptyReach);
}

test("a document this server was told about is held, and one it was not is not", () => {
  const uri = "file:///w/held.kh";
  assert.equal(holds(uri), false, "a document that did not reach this server is not held");
  holding(uri);
  try {
    assert.equal(holds(uri), true);
    assert.equal(text(uri), WHOLE);
  } finally {
    close(uri);
  }
});

test("opening a document publishes what the frontend could not read of it", () => {
  const uri = "file:///w/opened.kh";
  holding(uri);
  try {
    assert.deepEqual(codesOf(diagnosticsFor(uri, emptyReach)!), [
      "unterminated-string",
      // The inclusion whose path could not be read is a form no declaration takes: the
      // file is reported in its own broken state rather than tidied into the one fault.
      "declaration-form",
    ]);
  } finally {
    close(uri);
  }
});

test("a change under the declared shape is applied, and the next publication is the changed text's", () => {
  const uri = "file:///w/changed.kh";
  holding(uri);
  try {
    const [published] = change(uri, [{ text: CORRECTED }], emptyReach);
    assert.equal(text(uri), CORRECTED, "an empty publication is only a clearing if the text behind it moved");
    const said = payloadOf(published!);
    assert.equal(said.method, "textDocument/publishDiagnostics");
    assert.equal(said.params.uri, uri);
    assert.deepEqual(codesOf(said.params.diagnostics), [], "the fault the document had is gone, and the file says so");
  } finally {
    close(uri);
  }
});

test("a change that contradicts the declared capability is refused, and the text stands", () => {
  const uri = "file:///w/refused.kh";
  holding(uri);
  try {
    const [refusal] = change(uri, [
      { text: CORRECTED, range: { start: { line: 1, character: 0 }, end: { line: 1, character: 6 } } },
    ], emptyReach);
    assert.equal(text(uri), WHOLE, "the document is left as it was: every answer after this is about that text");
    assert.deepEqual(codesOf(diagnosticsFor(uri, emptyReach)!), ["unterminated-string", "declaration-form"]);
    const said = payloadOf(refusal!);
    assert.equal(said.params.uri, uri, "the refusal stands on the document it was about");
    assert.deepEqual(codesOf(said.params.diagnostics), ["text-document-sync"]);
  } finally {
    close(uri);
  }
});

test("closing a document drops it, and clears the markers it had", () => {
  const uri = "file:///w/closed.kh";
  holding(uri);
  const cleared = payloadOf(close(uri));
  assert.equal(holds(uri), false, "the document is gone, so a question about it is a question about no document");
  assert.equal(text(uri), undefined);
  assert.equal(cleared.method, "textDocument/publishDiagnostics");
  assert.deepEqual(cleared.params.diagnostics, [], "an empty publication is the only way a client is told to drop them");
});

test("the diagnostics a document carries are the faults of the text it now holds", () => {
  const uri = "file:///w/re-published.kh";
  holding(uri);
  try {
    change(uri, [{ text: "tp A cp {}\n}\n" }], emptyReach);
    assert.deepEqual(codesOf(diagnosticsFor(uri, emptyReach)!), ["declaration-form"]);
  } finally {
    close(uri);
  }
});
