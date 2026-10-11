/* For license and copyright information please see the LEGAL file in the code repository */

import assert from "node:assert/strict";
import test from "node:test";

import { readUnit } from "../src/reader.ts";
import { referencePlaces } from "../src/references.ts";
import { declaredName, referencedTypes, type Declaration } from "../src/sr.ts";

// Where a name stands, and only that. Every row here asks the same question a tool asks —
// "in this source, where is the type name this declaration references written?" — and every
// consumer of that answer is a tool: a rename has to place what it rewrites, and a language
// server has to place what it draws. No test in core asked it before this file, which is why
// two walks over the same tokens had already parted company (lsp/src/reference-places.ts and
// services/rename/khayyam-binding.ts each wrote one).

/** The declaration the reader produced for `name`. A placement question is asked about a
 *  declaration a reader produced, so the rows read one through `readUnit` rather than writing
 *  the shape out — a row that built its own declaration would be asking about a form no file
 *  in the repository has. */
function declaration(source: string, name: string): Declaration {
  const read = readUnit("main.kh", source);
  const found = read.unit.declarations.filter((one) => declaredName(one) === name);
  const faults = read.faults.map((fault) => `${fault.reason} at line ${fault.line}`);
  assert.deepEqual(faults, [], `reading the source to reach ${name} reported faults`);
  assert.equal(found.length, 1, `${name} was not read exactly once`);
  return found[0]!;
}

/** Where each place stands, as `line:column text`. The column is the one the scanner found
 *  the name at, so a row that pins it pins the scanner's own count and not a recount. */
const stands = (places: { line: number; column: number; text: string }[]): string[] =>
  places.map((place) => `${place.line}:${place.column} ${place.text}`);

test("an inclusion places the name it routes, never the URI beside it", () => {
  // `in` is a routing operator and the URI is how the declaration says which file
  // (`docs/khayyam/khayyam.md`, Import Mechanism (`in`)); a quoted string names no type, so a
  // walk that reported one would place a place where a name cannot stand. Both inclusions are
  // one row because they are the same form written on either top-level keyword.
  const source = 'tp Bool in "lib/boolean.kh"\nvr MaxTimeout in "lib/config.kh"\n';
  assert.deepEqual(stands(referencePlaces(source, declaration(source, "Bool"))), ["1:4 Bool"]);
  assert.deepEqual(stands(referencePlaces(source, declaration(source, "MaxTimeout"))), [
    "2:4 MaxTimeout",
  ]);
});

test("a variable places its type, in the slot where `vr` writes it", () => {
  // `vr {name} {type}` puts the type where `tp` puts its subtype keyword
  // (`docs/khayyam/khayyam.md`, Variable), so the type is read from its own slot; a walk that
  // went looking for the subtype would read nothing and report nothing.
  const source = "tp W16 ab\nvr maxW16 W16\n";
  assert.deepEqual(referencePlaces(source, declaration(source, "maxW16")), [
    { line: 2, column: 11, length: 3, text: "W16" },
  ]);
});

test("a capsule places each field's type and each composition entry, in the order they stand", () => {
  // A capsule's block holds two shapes, and which one an entry is decides which of its names
  // is the reference (`docs/khayyam/khayyam.md`, Capsule): two names are a field and its type,
  // one is an abstraction the capsule composes. The block opens and closes on lines of its
  // own here, which is where the entries stand.
  const source =
    "tp ServerConfig cp {\n    Host String\n    Port W16\n    TLSConfig TLSConfig\n    Scroll\n}\n";
  assert.deepEqual(stands(referencePlaces(source, declaration(source, "ServerConfig"))), [
    "2:10 String",
    "3:10 W16",
    "4:15 TLSConfig",
    "5:5 Scroll",
  ]);
});

test("a capsule whose block opens and closes on its own line places what is inside it", () => {
  // `tp Counter cp {}` opens and closes on one line and leaves nothing open, so a walk that
  // began at the line after the declaration's own would step over the whole block and answer
  // nothing at all. The line is where the declaration is read, not where it ends.
  const source = "tp Counter cp { count W16 }\n";
  assert.deepEqual(stands(referencePlaces(source, declaration(source, "Counter"))), ["1:23 W16"]);
});

test("an abstraction places every entry of its composition block", () => {
  // An abstraction composes other abstractions in a block, and every name on those lines is
  // one (`docs/khayyam/khayyam.md`, Abstraction). Several entries are the ordinary shape of
  // such a block; one would not tell a walk that keeps them apart from a walk that reads one.
  const source = "tp ADT ab {\n    DataType\n    Field_MediaType\n    Key\n}\n";
  assert.deepEqual(stands(referencePlaces(source, declaration(source, "ADT"))), [
    "2:5 DataType",
    "3:5 Field_MediaType",
    "4:5 Key",
  ]);
});

test("a body-less abstraction places nothing, because it composes nothing", () => {
  // The composition block is optional (`docs/khayyam/khayyam.md`, Abstraction), and a
  // declaration with no block is the form most abstractions in this repository are written
  // in. A walk that reached past the line's end for a brace that is not there would read the
  // next declaration's tokens as this one's.
  const source = "tp Reader ab\ntp Element ab\n";
  assert.deepEqual(referencePlaces(source, declaration(source, "Reader")), []);
});

test("a method places its three groups' types and never a parameter's own name", () => {
  // A group alternates a parameter's name with its type (`docs/khayyam/khayyam.md`, Method),
  // and a name is a value while a type is a type: `(self Reader)` writes the same word twice
  // for two different things, and only the slot says which. A walk that reported every
  // identifier in a group would place a parameter spelled like a type — the influencing group
  // here names its parameter `Reader` — and the place would be a value standing where a
  // rename would write a type.
  const source =
    "tp Reader ab\ntp Element ab\ntp Error ab\ntp Read mt (self Reader) (Reader Element) (err Error)\n";
  assert.deepEqual(stands(referencePlaces(source, declaration(source, "Read"))), [
    "4:18 Reader",
    "4:34 Element",
    "4:48 Error",
  ]);
});

test("a qualified reference is one place of the whole name", () => {
  // `pkg.Type` is one reference the reader counted once, and the dots are punctuation between
  // its tokens (`expectTypeReference`, core/src/parse.ts). One place covers the whole of it:
  // two places would let a caller rewrite half the name and read the other half as text.
  const source = "tp Error ab\ntp Raise mt (self Error) () (err error_p.Error)\n";
  assert.deepEqual(referencePlaces(source, declaration(source, "Raise")), [
    { line: 2, column: 19, length: 5, text: "Error" },
    { line: 2, column: 34, length: 13, text: "error_p.Error" },
  ]);
});

test("a method's body is not walked, and the groups beside it are kept", () => {
  // A body is carried as text rather than read as declarations, so a name inside one is not a
  // reference the reader counted. The signature's places are kept anyway: a body is what the
  // parse could not read, and the places before it are the ones it did read. The signature
  // here is on one line and the body on the lines below, which is the ordinary shape.
  const source =
    "tp Host ab\ntp Run mt (self Host) (name String) () {\n    Host.Error()\n}\n";
  assert.deepEqual(stands(referencePlaces(source, declaration(source, "Run"))), [
    "2:17 Host",
    "2:29 String",
  ]);
});

test("a scope places nothing, and says so rather than walking its block", () => {
  // A scope's block holds commands and no types, and the reader never read any of it as
  // declarations — its `parseBlock` joins a body's tokens into one string
  // (`docs/khayyam/khayyam.md`, Scope). The parse refuses the form at the top level as well
  // (`scope-placement`), so no declaration like this one is in any file; it is written out
  // because the reader would not produce it and the answer for the shape is still owed.
  const source = "tp Host ab\ntp Run mt (self Host) () () {\n    tp Step sc {\n        a command\n    }\n}\n";
  const scope: Declaration = { form: "tp-sc", name: "Step", line: 3, body: "a command" };
  assert.deepEqual(referencePlaces(source, scope), []);
});

test("the places of a form the reader counts references for are the references it counted", () => {
  // The reader's answer is which names a declaration references (sr.ts) and this module's is
  // where each of them stands, so the two have to be the same list in the same order or one
  // of them is describing something else. A capsule writes its fields ahead of its
  // composition entries in the representation, so this is also the row that pins where the
  // two answers would part company if a block interleaved the two shapes — the walk answers
  // in the order they stand, which is the order a source is read in.
  const capsule =
    "tp ServerConfig cp {\n    Host String\n    Port W16\n    Scroll\n}\n";
  const abstraction = "tp ADT ab {\n    DataType\n    Key\n}\n";
  const method =
    "tp Reader ab\ntp Error ab\ntp Read mt (self Reader) (data Reader) (err Error)\n";
  for (const [source, name] of [
    [capsule, "ServerConfig"],
    [abstraction, "ADT"],
    [method, "Read"],
  ] as const) {
    const read = declaration(source, name);
    assert.deepEqual(
      referencePlaces(source, read).map((place) => place.text),
      referencedTypes(read),
      `${name}: the walk placed a different list than the reader counted`,
    );
  }
});
