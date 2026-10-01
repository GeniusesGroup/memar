import assert from "node:assert/strict";
import test from "node:test";

import { braceDepth, itemsOnLine, placeOf } from "../src/document-items.ts";

// What the scanner hands back before anything asks what a name is: the items of each
// line, in the columns the editor counts, and how far one line's braces carry the
// file. Every role, every diagnostic and every definition is placed against this, so
// what is fixed here is the origin all three count from — a column counted from
// anywhere but the start of its line sends a reader to the wrong character.

test("a line's items are the ones the scanner read, in the columns the editor counts", () => {
  const byLine = itemsOnLine("tp Reader ab\nvr held Reader\n");
  assert.deepEqual(byLine.get(0), [
    { kind: "ident", text: "tp", startChar: 0 },
    { kind: "ident", text: "Reader", startChar: 3 },
    { kind: "ident", text: "ab", startChar: 10 },
  ]);
  assert.deepEqual(byLine.get(1), [
    { kind: "ident", text: "vr", startChar: 0 },
    { kind: "ident", text: "held", startChar: 3 },
    { kind: "ident", text: "Reader", startChar: 8 },
  ]);
});

test("the breaks between lines and the end of the file stand on no line of items", () => {
  const byLine = itemsOnLine("tp Reader ab\n\nvr held Reader");
  assert.equal(byLine.has(1), false, "a blank line carries no item and is not a hole in the walk");
  assert.deepEqual(
    byLine.get(2)!.map((item) => item.text),
    ["vr", "held", "Reader"],
  );
  assert.equal(byLine.size, 2, "the file ends after its last line and no line stands on nothing");
});

test("a quoted form's item stands on the first character inside its quotes", () => {
  // The scanner reports a string's column from inside the quotes, so an item's own
  // place is not the extent a token must cover: the quotes are part of what covers it,
  // which is why the emitter of a quoted form steps back one character to take them in.
  const item = itemsOnLine('tp Bool in "math/boolean"\n').get(0)![3]!;
  assert.deepEqual(item, { kind: "string", text: "math/boolean", startChar: 12 });
  assert.deepEqual(placeOf(0, item), { line: 0, startChar: 12, length: 12 });
});

test("a scan that stopped at a fault still hands back what it read", () => {
  // A document with one unterminated quoted form is not left with no display at all:
  // the items before the fault are the ones the rest of the reading is measured
  // against, and the line after it is read whole.
  const byLine = itemsOnLine('tp Broken in "unterminated\ntp Reader ab\n');
  assert.deepEqual(
    byLine.get(0)!.map((item) => item.text),
    ["tp", "Broken", "in"],
  );
  assert.deepEqual(
    byLine.get(1)!.map((item) => item.text),
    ["tp", "Reader", "ab"],
  );
});

test("how far a line's braces carry the file", () => {
  const brace = (text: string) => braceDepth([{ kind: "punct", text, startChar: 0 }]);
  assert.equal(brace("{"), 1, "`tp Counter cp {}` leaves a block open behind it");
  assert.equal(brace("}"), -1, "a closing brace comes back out of one");
  assert.equal(braceDepth([]), 0, "a line with no brace carries the file nowhere");
  assert.equal(
    braceDepth([
      { kind: "punct", text: "{", startChar: 0 },
      { kind: "punct", text: "}", startChar: 1 },
    ]),
    0,
    "a block that opens and closes on one line leaves nothing open",
  );
});

test("a brace that is text is a character of the text, not a delimiter", () => {
  assert.equal(braceDepth([{ kind: "string", text: "{", startChar: 0 }]), 0);
  assert.equal(braceDepth([{ kind: "ident", text: "}", startChar: 0 }]), 0);
});

test("a place is the item's own extent on the line it stands on", () => {
  assert.deepEqual(placeOf(2, { kind: "ident", text: "Reader", startChar: 3 }), {
    line: 2,
    startChar: 3,
    length: 6,
  });
});
