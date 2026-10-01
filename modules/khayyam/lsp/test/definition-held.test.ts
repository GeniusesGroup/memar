import assert from "node:assert/strict";
import test from "node:test";

import { definitionAt, type Reach } from "../src/definition.ts";
import { asking, characterOn, emptyReach, linesOf, URI } from "./definition-fixture.ts";

// Where a definition points when the document it points into is one the reader has open
// with edits the disk does not have. A place on the wire is read by the editor against the
// text the editor holds, and this server's text of an open document is the editor's own —
// so a definition read from the disk would name a line the reader is not on, and a reader
// who followed it would land on the wrong line with nothing saying why.
//
// This is measured against a reach that states which text a document is read from, and not
// over the wire: the rule is only observable where an address resolves at all, and today
// none does, because no manifest declares how an address resolves
// ([modularity.handoff.md → Dependency Resolution and Companion Manifest](../../../../docs/khayyam/modularity.handoff.md)).
// The wire half of the rule is therefore not claimed here and not claimed anywhere; what is
// claimed is that the rule lives in the reach, so that turning addresses on cannot be the
// thing that forgets it.

const INCLUDING = ['tp Bool in "math/boolean.kh"', "tp Run mt (self Bool) () () {", "\tBool.IsTrue()", "}", ""].join("\n");
const ON_DISK = ["// a", "// b", "tp Bool cp {}", ""].join("\n");
const IN_THE_EDITOR = ["tp Bool cp {}", ""].join("\n");
const TARGET = "file:///w/math/boolean.kh";

/** A reach over one file, read from whatever the test says that file's text is. */
const reading = (from: string): Reach => ({
  resolve: () => ({ base: { directory: "/w", markedBy: "table" }, found: { uri: TARGET, text: from } }),
  held: () => from,
});

test("a definition into a document the editor holds names the line the editor is on", () => {
  const found = definitionAt(URI, INCLUDING, { line: 2, character: 4 }, reading(IN_THE_EDITOR));
  assert.deepEqual(found, { uri: TARGET, line: 0, startChar: 3, length: 4, name: "Bool" });
  assert.equal(IN_THE_EDITOR.split("\n")[0]!.slice(3, 7), "Bool", "and the name is on the line the answer names");
  assert.notEqual(found?.line, 2, "the disk's line is a different place, and the reader is not on it");
});

test("a definition follows what the reader last sent, so an unsaved edit moves it", () => {
  const position = { line: 2, character: 4 };
  assert.equal(definitionAt(URI, INCLUDING, position, reading(IN_THE_EDITOR))?.line, 0);
  // The editor adds a line above the declaration without saving, and the place moves with
  // the text the editor holds rather than with the file on disk.
  const edited = ["// c", ...IN_THE_EDITOR.split("\n")].join("\n");
  assert.equal(definitionAt(URI, INCLUDING, position, reading(edited))?.line, 1);
  assert.equal(edited.split("\n")[1]!.slice(3, 7), "Bool");
});

test("a document the reader holds no text for is read from where it is, because there is no buffer to read", () => {
  // The rule is which text a place is read against, not a preference for a buffer: a
  // document the editor never opened has no buffer, and the file is the only text there is.
  const found = definitionAt(URI, INCLUDING, { line: 2, character: 4 }, {
    resolve: () => ({ base: { directory: "/w", markedBy: "table" }, found: { uri: TARGET, text: ON_DISK } }),
    held: () => undefined,
  });
  assert.equal(found?.line, 2);
  assert.equal(ON_DISK.split("\n")[2]!.slice(3, 7), "Bool");
});

test("a reach that resolves nothing reaches nothing rather than guessing", () => {
  assert.equal(definitionAt(URI, INCLUDING, { line: 2, character: 4 }, emptyReach), null);
  assert.equal(
    definitionAt(URI, INCLUDING, { line: 2, character: 4 }, {
      resolve: (path, from) => ({ because: `nothing declares how ${path} resolves from ${from}` }),
      held: () => undefined,
    }),
    null,
  );
  assert.notEqual(definitionAt(URI, INCLUDING, { line: 2, character: 4 }, asking), null, "and a reach that does resolve reaches one");
});

test("a name the document declares itself never asks the reach, so an unresolvable address beside it costs nothing", () => {
  const source = ["tp Bool in \"math/nowhere.kh\"", "tp Own cp {}", ""].join("\n");
  const lines = linesOf(source);
  const asked: string[] = [];
  const found = definitionAt(URI, source, { line: 1, character: characterOn(lines, 1, "Own") }, {
    resolve: (path) => {
      asked.push(path);
      return { because: "nothing declares how this resolves" };
    },
    held: () => undefined,
  });
  assert.deepEqual(found, { uri: URI, line: 1, startChar: 3, length: 3, name: "Own" });
  assert.deepEqual(asked, [], "the reach was never asked, because this name is declared here");
});
