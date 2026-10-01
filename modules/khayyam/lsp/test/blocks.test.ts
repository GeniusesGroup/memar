import assert from "node:assert/strict";
import test from "node:test";

import { openBlocks, type Declared } from "../src/blocks.ts";
import { itemsOnLine } from "../src/document-items.ts";

// The blocks a document holds open as it is walked, and how far its braces carry it —
// the two together are what says which block a line stands in and whether it leaves one
// open behind it. A role follows the binding, but which binding a name answers to
// depends on this, so the depth counting and the stack are fixed here on their own.

const linesOf = (source: string) => itemsOnLine(source).get(0) ?? [];

/** What a body declaring a name on a line holds for it: the identity, the sentence
 *  saying so, and the place the name stands. A block holds the role as well as the
 *  place because a body holds a `method-local` and a `scope`, which are two identities
 *  and not one name in two positions. */
const local = (line: number, role = "method-local"): Declared => ({
  role,
  origin: `the variable on line ${line} declared in this body`,
  place: { line, startChar: 1, length: 4 },
});

test("a block the file enters is the block the lines inside it stand in", () => {
  const blocks = openBlocks();
  const signature = blocks.entered(linesOf("tp Run mt (self Reader) () () {"));
  assert.deepEqual(signature, { before: 0, after: 1 }, "the signature leaves one block open behind it");
  blocks.opened("mt", signature.after);
  const statement = blocks.entered(linesOf("\tCopy(reader)"));
  assert.equal(statement.before, 1, "the statement stands one block in");
  assert.equal(blocks.enclosing()?.kind, "mt");
  // A block is left when the file comes back out of it, which is what the next line's
  // depth says: the closing brace is on the line the file is still standing in it.
  const closing = blocks.entered(linesOf("}"));
  assert.deepEqual(closing, { before: 1, after: 0 });
  assert.equal(blocks.enclosing()?.kind, "mt", "the closing brace stands in the block it closes");
  blocks.entered(linesOf("tp Other ab"));
  assert.equal(blocks.enclosing(), undefined, "and the line after it stands in no block at all");
});

test("a block that opens and closes on its own line leaves nothing open", () => {
  // `tp X cp {}` is a capsule with no fields and `tp Y mt (…) (…) (…) {}` is a method
  // with an empty body; the corpus writes both. A block that opens and closes on one
  // line must not be treated as still open, or every line after it is read inside a
  // block that already ended.
  const blocks = openBlocks();
  assert.deepEqual(blocks.entered(linesOf("tp Counter cp {}")), { before: 0, after: 0 });
  assert.equal(blocks.enclosing(), undefined, "there is no block for the next line to stand in");
});

test("a brace on a line no declaration opened still counts towards the depth", () => {
  // A body statement may open a block no declaration opened, and a count that read
  // only the declaration lines lost its place on the first one.
  const blocks = openBlocks();
  const signature = blocks.entered(linesOf("tp Run mt (self Reader) () () {"));
  blocks.opened("mt", signature.after);
  const opensInBody = blocks.entered(linesOf("\tif d {"));
  assert.equal(opensInBody.after, 2, "the statement's own brace is counted");
  const closesInBody = blocks.entered(linesOf("\t}"));
  assert.equal(closesInBody.before, 2);
  assert.equal(blocks.enclosing()?.kind, "mt", "the method is still what that line stands in");
});

test("a brace closes nothing, so the depth never falls below zero", () => {
  const blocks = openBlocks();
  assert.deepEqual(blocks.entered(linesOf("}")), { before: 0, after: 0 });
  assert.equal(blocks.enclosing(), undefined);
});

test("the nearest block that declares a name is the one the name is", () => {
  // The body is the narrower scope, so a name declared in it is that declaration for
  // the length of the body even where the file declares the same name. A name
  // collision is an architecture error rather than a disambiguation problem, and the
  // reader is told which of the two it is looking at.
  const blocks = openBlocks();
  const method = blocks.entered(linesOf("tp Run mt (self Reader) () () {"));
  blocks.opened("mt", method.after);
  blocks.enclosing()!.locals.set("same", local(1));
  const scope = blocks.entered(linesOf("\ttp Step sc {"));
  blocks.opened("sc", scope.after);
  blocks.enclosing()!.locals.set("same", local(2));
  assert.deepEqual(blocks.declares("same"), local(2));
  assert.equal(blocks.declares("nothing"), undefined, "a name no open block declares is not declared here");
});

test("a name only an enclosing block declares is still declared here", () => {
  const blocks = openBlocks();
  const method = blocks.entered(linesOf("tp Run mt (self Reader) () () {"));
  blocks.opened("mt", method.after);
  blocks.enclosing()!.locals.set("held", local(1));
  const scope = blocks.entered(linesOf("\ttp Step sc {"));
  blocks.opened("sc", scope.after);
  assert.deepEqual(blocks.declares("held"), local(1));
});

test("a statement belongs to the nearest method that is open", () => {
  // A scope's statements are written inside the method that holds it, so a parameter
  // of that method is that parameter wherever in its body it is used.
  const blocks = openBlocks();
  const method = blocks.entered(linesOf("tp Run mt (self Reader) () () {"));
  blocks.opened("mt", method.after);
  const scope = blocks.entered(linesOf("\ttp Step sc {"));
  blocks.opened("sc", scope.after);
  blocks.entered(linesOf("\td.Copy()"));
  assert.equal(blocks.method()?.kind, "mt");
  const closesScope = blocks.entered(linesOf("\t}"));
  assert.equal(closesScope.after, 1);
  assert.equal(blocks.method()?.depth, method.after, "the scope's own closing brace leaves the method it was written in");
  blocks.entered(linesOf("}"));
  blocks.entered(linesOf("tp Other ab"));
  assert.equal(blocks.method(), undefined, "and once the file has come back out of the method, no statement stands in one");
});

test("a block that is no method is no method a statement belongs to", () => {
  const blocks = openBlocks();
  const capsule = blocks.entered(linesOf("tp Buffer cp {"));
  blocks.opened("cp", capsule.after);
  blocks.entered(linesOf("\tdata U8"));
  assert.equal(blocks.method(), undefined, "a capsule's field line declares, so it is not a statement");
});

test("a block a declaration gives names to is held with those names", () => {
  const blocks = openBlocks();
  const line = blocks.entered(linesOf("tp Set mt (self Reader) (key String) {}"));
  blocks.opened("mt", line.after, {
    parameters: new Map([["key", { line: 0, startChar: 27, length: 3 }]]),
    fields: new Set(["data"]),
    composition: new Set(["Reader"]),
  });
  const block = blocks.enclosing()!;
  assert.equal(block.parameters.get("key")?.startChar, 27);
  assert.deepEqual([...block.fields], ["data"]);
  assert.deepEqual([...block.composition], ["Reader"]);
  assert.deepEqual([...block.locals], [], "a block starts with nothing declared in its body");
});
