import assert from "node:assert/strict";
import test from "node:test";

import { definitionAt } from "../src/definition.ts";
import { at, asking, characterOn, emptyReach, INCLUDING, linesOf, reach, SOURCE, URI, USING } from "./definition-fixture.ts";

// A definition that has to leave the document. A name that arrived by `in` is declared
// nowhere in the file that names it, so the answer's own document is the file the URI
// addresses — and every file here is one these tests wrote, never a file the repository
// may curate, archive, or delete.

test("a type that arrived by an inclusion reaches the declaration in the file its URI names", () => {
  assert.deepEqual(definitionAt(URI, SOURCE, { line: 8, character: at(8, "Bool") }, asking), {
    uri: "file:///w/math/boolean.kh",
    line: 1,
    startChar: 3,
    length: 4,
    name: "Bool",
  });
});

test("a variable that arrived by an inclusion reaches its declaration the same way", () => {
  assert.deepEqual(definitionAt(URI, SOURCE, { line: 9, character: at(9, "limit") }, asking), {
    uri: "file:///w/math/limit.kh",
    line: 0,
    startChar: 3,
    length: 5,
    name: "limit",
  });
});

test("an inclusion's own line reaches the declaration it names, and its path reaches nothing", () => {
  // The line where the name is introduced is where a reader first meets it, so asking
  // there has to answer as everywhere else the name stands.
  assert.deepEqual(definitionAt(URI, SOURCE, { line: 0, character: at(0, "Bool") }, asking), {
    uri: "file:///w/math/boolean.kh",
    line: 1,
    startChar: 3,
    length: 4,
    name: "Bool",
  });
  assert.equal(definitionAt(URI, SOURCE, { line: 0, character: at(0, "math/boolean.kh") + 1 }, asking), null);
});

test("a name reached through a chain of inclusions reaches the declaration that is one", () => {
  // An inclusion is not a declaration — the name it names is declared elsewhere — so a
  // file that only includes a name has nothing to be sent to, and the question goes on
  // to the file it included from. A chain is not a single hop by accident: it is the
  // same reasoning applied twice, and a resolver that stopped at the first would be
  // answering with a use while claiming it was a declaration.
  assert.deepEqual(
    definitionAt(
      URI,
      INCLUDING,
      USING,
      reach({
        "math/boolean.kh": 'tp Bool in "math/truth.kh"\n',
        "math/truth.kh": "// A truth value.\ntp Bool cp {}\n",
      }),
    ),
    { uri: "file:///w/math/truth.kh", line: 1, startChar: 3, length: 4, name: "Bool" },
  );
});

test("two files that include a name from each other answer nothing rather than reading forever", () => {
  // A cycle of inclusions has no declaration anywhere in it, so there is no place to be
  // sent to; what has to be guaranteed is that the question stops. A resolver that
  // followed one hop twice would answer nothing at all — not a wrong place, no answer.
  assert.equal(
    definitionAt(
      URI,
      INCLUDING,
      USING,
      reach({
        "math/boolean.kh": 'tp Bool in "math/truth.kh"\n',
        "math/truth.kh": 'tp Bool in "math/boolean.kh"\n',
      }),
    ),
    null,
  );
});

test("a file behind an inclusion that names nothing has no declaration to reach", () => {
  // The URI resolves and the file is there, but it declares no name by that name. A
  // server that answered the inclusion line would send a reader to a place that holds
  // no declaration of anything.
  const source = ['tp Gone in "math/absent"', "tp Run mt (self Gone) () () {", "\tGone.Copy()", "}", ""].join("\n");
  const lines = linesOf(source);
  assert.equal(
    definitionAt(
      URI,
      source,
      { line: 2, character: characterOn(lines, 2, "Gone") },
      reach({ "math/absent": "tp Other cp {}\n" }),
    ),
    null,
  );
});

test("an inclusion whose URI addresses nothing has no definition", () => {
  // Two separate absences, and both answer the same way: there is no file, and there is
  // no base to resolve the URI from. Neither may answer with a place it guessed.
  assert.equal(definitionAt(URI, INCLUDING, USING, reach({})), null, "the URI addresses nothing");
  assert.equal(
    definitionAt(URI, INCLUDING, USING, emptyReach),
    null,
    "there is nothing to reach with",
  );
});

test("a file behind an inclusion that the scanner refuses is read up to the fault", () => {
  // The reader recovers per declaration, and the fault here ends the file rather than a
  // line, so what is left of the file is what stands before it. The definitions answer
  // from that reading rather than withholding everything because of one fault — which
  // is what the reader is for, and what the gate would refuse.
  const after = "// A truth value.\ntp Bool cp {}\n/* a comment that never closes\n";
  const before = "/* a comment that never closes\ntp Bool cp {}\n";
  assert.deepEqual(definitionAt(URI, INCLUDING, USING, reach({ "math/boolean.kh": after })), {
    uri: "file:///w/math/boolean.kh",
    line: 1,
    startChar: 3,
    length: 4,
    name: "Bool",
  });
  // The same file with the fault above the declaration: the fault ended the file, so
  // nothing stands after it and there is no declaration of `Bool` left to be sent to.
  assert.equal(definitionAt(URI, INCLUDING, USING, reach({ "math/boolean.kh": before })), null);
});

test("a reach with nothing behind it costs only the names that left the document", () => {
  const source = ['tp Bool in "math/boolean.kh"', "tp Reader ab", "tp Run mt (self Reader) () () {", "\tBool.IsTrue()", "}", ""].join("\n");
  const lines = linesOf(source);
  const nothing = emptyReach;
  assert.equal(definitionAt(URI, source, { line: 3, character: characterOn(lines, 3, "Bool") }, nothing), null);
  assert.deepEqual(
    definitionAt(URI, source, { line: 2, character: characterOn(lines, 2, "Reader") }, nothing),
    { uri: URI, line: 1, startChar: characterOn(lines, 1, "Reader"), length: 6, name: "Reader" },
    "a name the document itself declares is answered whatever else cannot be reached",
  );
});
