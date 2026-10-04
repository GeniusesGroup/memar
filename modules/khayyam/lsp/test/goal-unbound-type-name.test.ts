import assert from "node:assert/strict";
import test from "node:test";

import { characterOn, linesOf } from "./definition-fixture.ts";
import { holding, PROBE } from "./harness.ts";
import type { Diagnostic } from "./wire.ts";

// The goal, in one document and over the wire: a `.kh` file that names a type nothing in it
// declares and no `in` brings in is published with an `unbound-type-name` diagnostic on that
// name — so the next human who renames an abstraction by hand is told by the editor rather
// than by the gate they never ran.
//
// The defect this is for is one the sources held: an abstraction renamed by hand to
// `EventTarget` while three of its method signatures still said `(self Target)`. The gate
// refuses that unit ([core/src/frontend.ts](../../../core/src/frontend.ts)) and the editor
// said nothing, so the file read as a file the toolchain had no trouble with.
//
// Every position the language names a type in is asked, because the goal is the check rather
// than one place it happens to be reached: a signature, a capsule field, an abstraction
// composition. And every case that is not a fault is asked too, because a check that only
// says what works is a check of half a goal — a qualified `pkg.Type`, which the rule states
// carries no check at all; a name an `in` brings in, which is bound by the file's own word
// whatever the address behind it resolves to; and a variable's type, which the question does
// not reach. The document is written here rather than read off
// [`event-target.kh`](../../../../modules/process/event/protocol/event-target.kh): the
// sources are an unreviewed archive, and a shape pinned to it changes when someone curates it.

/** The three positions, each naming a type nothing in the file answers, and each bound name
 *  written beside it so that a bound name and an unbound one are read off one document. */
const DOCUMENT = [
  "tp EventTarget ab", //                                       0
  "", //                                                        1
  "tp DispatchEvent mt (self Target) (event Event) (err Error)", // 2  the owner slot
  "tp Event cp {}", //                                          3
  "tp Error cp {}", //                                          4
  "", //                                                        5
  "tp Holder cp {", //                                          6
  "\ttarget Target", //                                         7  a capsule field
  "}", //                                                       8
  "tp Nothing ab {", //                                         9
  "\tPhantom", //                                               10  an abstraction composition
  "}", //                                                       11
  "", //                                                        12
];

const SOURCE = DOCUMENT.join("\n");
const LINES = linesOf(SOURCE);
/** The three names this document leaves unbound, each with the line it stands on, so that a
 *  change to the fixture moves every assertion with it rather than leaving one behind. */
const NAMES = [
  [2, "Target"],
  [7, "Target"],
  [10, "Phantom"],
] as const;

/** The sources defect as it stood: an abstraction renamed by hand, and one signature that the
 *  rename did not reach. Kept apart from the document above because this is the pair a reader
 *  meets — a marker on the file, and the same file a moment later without one — and because a
 *  change to it is the repair itself. */
const DEFECT = [
  "tp Event cp {}",
  "tp Error cp {}",
  "tp EventTarget ab",
  "tp DispatchEvent mt (self Target) (event Event) (err Error)",
  "",
].join("\n");
const REPAIRED = DEFECT.replace("(self Target)", "(self EventTarget)");
const QUALIFIED = DEFECT.replace("(self Target)", "(self pkg.Target)");

const codesOf = (diagnostics: Diagnostic[]): string[] => diagnostics.map((d) => d.code);

test("a name nothing in the file answers is published on the name, in every position the language names a type in", async (t) => {
  const server = await holding(SOURCE);
  t.after(() => server.stop());
  const published = await server.firstPublishedFor(PROBE);

  assert.deepEqual(
    codesOf(published),
    ["unbound-type-name", "unbound-type-name", "unbound-type-name"],
    "and nothing else is published for a file that reads whole and claims nothing",
  );
  assert.deepEqual(
    published.map((diagnostic) => diagnostic.range.start.line),
    NAMES.map(([line]) => line),
    "in the order the names stand on the lines they stand on",
  );
  for (const [at, diagnostic] of published.entries()) {
    const [line, name] = NAMES[at]!;
    const character = characterOn(LINES, line, name);
    assert.equal(diagnostic.range.start.character, character, `line ${line}: the finding stands on the name`);
    assert.equal(diagnostic.range.end.character, character + name.length, `line ${line}: and covers it and nothing else`);
    assert.equal(diagnostic.severity, 1, "a refusal is an error rather than a hint");
    assert.equal(diagnostic.source, "khayyam");
    assert.match(diagnostic.message, new RegExp(`"${name}"`), "the sentence names what is unbound");
    assert.match(diagnostic.message, /no declared or included name answers/);
    assert.match(diagnostic.message, /no "in" declaration brings it in/, "and what is missing");
    assert.match(
      diagnostic.message,
      /every role and every definition is still answered from what the file declared/,
      "and that nothing else in the file is affected",
    );
  }
});

test("what this check does not ask about is published as nothing", async (t) => {
  // Three documents, and one empty publication each. A check that marked any of them would be
  // a check of something the gate does not refuse a unit over, which is the disagreement this
  // server may not have with the toolchain it is the front of.
  const variable = ["vr held Target", ""].join("\n");
  for (const [why, source] of [
    ["the defect with the signature repaired", REPAIRED],
    ["the same name qualified, which the rule states carries no check today", QUALIFIED],
    ["a variable's type, which is not one of the positions the rule names", variable],
  ] as const) {
    const server = await holding(source);
    t.after(() => server.stop());
    assert.deepEqual(await server.firstPublishedFor(PROBE), [], why);
  }
});

test("a name an `in` brings in is bound by the file's own word, whatever the address behind it resolves to", async (t) => {
  // The two answers are about two different things and neither stands for the other: the
  // claim cannot be accounted for, and the name it brings is still a name this file binds.
  // A reader told the second because of the first would rename a declaration that is right.
  const server = await holding(
    ['tp Ghost in "math/nowhere.kh"', "tp Holder cp {", "\ttarget Ghost", "}", ""].join("\n"),
  );
  t.after(() => server.stop());
  const published = await server.firstPublishedFor(PROBE);
  assert.deepEqual(codesOf(published), ["unresolved-import"]);
  assert.match(published[0]!.message, /an address is resolved through the declaring file/);
});

test("the two answers a document already carried are still published beside this one", async (t) => {
  // Three kinds on one document, and none of them standing for another: a fault of reading,
  // a claim nothing accounts for, and a name the file's own names do not answer. A reader
  // shown only the third would think the file reads whole, and one shown only the first
  // would think nothing about its names was wrong.
  const server = await holding([
    'tp Ghost in "math/nowhere.kh"', //                                     0  a claim
    "tp EventTarget ab", //                                                 1
    "tp DispatchEvent mt (self Target) (event Ghost) (err Event)", //        2  a name
    "tp Event cp {}", //                                                    3
    "/* the writer left this open", //                                       4  reading stops here
    "", //                                                                  5
  ].join("\n"));
  t.after(() => server.stop());
  assert.deepEqual(codesOf(await server.firstPublishedFor(PROBE)), [
    "unterminated-block-comment",
    "unresolved-import",
    "unbound-type-name",
  ]);
});

test("one unbound name in two places is two findings, because a reader has two lines to look at", async (t) => {
  // The gate names one and refuses the unit; a reader of a document has to be sent to each
  // place, and a name used twice is two lines. The variable on the third line is the other
  // half of the same question: the gate does not ask about a variable's type, so neither
  // does this, and a walk over the signatures rather than over the gate's own references
  // would have marked it.
  const source = ["tp EventTarget ab", "tp DispatchEvent mt (self Target) (event Target) ()", "vr other Target", ""].join("\n");
  const lines = linesOf(source);
  const server = await holding(source);
  t.after(() => server.stop());
  const published = await server.firstPublishedFor(PROBE);
  assert.deepEqual(codesOf(published), ["unbound-type-name", "unbound-type-name"]);
  assert.deepEqual(
    published.map((diagnostic) => diagnostic.range.start.character),
    [
      characterOn(lines, 1, "(self Target)") + "(self ".length,
      characterOn(lines, 1, "(event Target)") + "(event ".length,
    ],
    "one finding on each of the two places the name stands, and none on the variable's",
  );
});

test("a change that binds the name takes the marker off the file", async (t) => {
  const server = await holding(DEFECT);
  t.after(() => server.stop());
  assert.deepEqual(codesOf(await server.firstPublishedFor(PROBE)), ["unbound-type-name"], "one to begin with");
  server.notify("textDocument/didChange", {
    textDocument: { uri: PROBE, version: 2 },
    contentChanges: [{ text: REPAIRED }],
  });
  assert.deepEqual(
    await server.publishedFor(PROBE),
    [],
    "an empty publication is how a client is told a fault is gone",
  );
});
