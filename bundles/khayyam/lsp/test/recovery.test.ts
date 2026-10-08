import assert from "node:assert/strict";
import test from "node:test";

import { analyse, semanticRoles } from "../src/semantic.ts";

// What a reader is given for a document the frontend could not read in full: the roles of
// the part that was read, and the faults that say what the rest cost. The recovery is per
// declaration and at the line break that ends one (docs/khayyam/khayyam.md → Declaration
// separator), so one unreadable line costs the file that line and nothing else — and a
// fault that follows another says so, because repairing the first is what takes the
// second away.

test("a lexical fault does not take the display of everything before it with it", () => {
  const source = [
    "tp Reader ab",
    "tp Set mt (self Reader) (key String) (err String) {",
    "    key.CopyFrom(reader)(err)",
    "}",
    'tp Broken in "unterminated',
    "",
  ].join("\n");
  // The roles of a document the parser refuses are a guess, and are not what is
  // claimed here: what is claimed is that the lines before the fault are still
  // found, and found at the place they occupy.
  const body = semanticRoles(source).filter((token) => token.line === 2);
  assert.deepEqual(
    body.map((token) => [token.startChar, token.length, token.text]),
    [
      [4, 3, "key"],
      [8, 8, "CopyFrom"],
      [17, 6, "reader"],
      [25, 3, "err"],
    ],
  );
});

/** The shape of the owner's scratch file at the repository root: a method body
 *  holding statements the grammar has no form for. `goto` is not a keyword and the
 *  grammar admits no operator (docs/khayyam/khayyam.md → Scope, and → Method
 *  Invocation Rules), so the line is refused at the `>`. */
const UNREADABLE = [
  'tp Error in ""',
  "tp Capsule cp {}",
  "tp Run mt (self Capsule) (d Capsule) () {",
  "    goto end",
  "    tp loop sc {",
  "        if d>1 {",
  "        }",
  "    }",
  "}",
  "vr tail Capsule",
  "",
].join("\n");

test("a file the frontend could not read in full is read for the rest of it", () => {
  // Recovery is per declaration and at the line break that ends one
  // (docs/khayyam/khayyam.md → Declaration separator), so the unreadable line costs the
  // file that line and nothing else. A reader is not left looking at a file the
  // toolchain cannot account for.
  const { roles, faults } = analyse(UNREADABLE);
  // Two, and the second is the first's consequence: the unreadable line carried the
  // brace that would have closed the scope, so the file's own blocks no longer line
  // up and the brace left over at line 9 is a declaration no declaration takes. Both
  // are reported, because a reader is owed the file's own state and not a tidy one.
  assert.deepEqual(
    faults.map((fault) => `${fault.reason}@${fault.line}:${fault.column}(${fault.extent})`),
    ["unexpected-character@6:13(line)", "declaration-form@9:1(declaration)"],
  );
  const declared = roles
    .filter((token) => token.role === "keyword")
    .map((token) => `${token.text}:${token.line + 1}`);
  assert.deepEqual(declared, ["tp:1", "tp:2", "tp:3", "tp:5", "vr:10"]);
  // The declaration after the fault still carries its own roles, which is what a
  // reader pairing declarations by position instead of by the line they stand on
  // would have lost.
  assert.equal(roles.find((token) => token.text === "tail")?.role, "variable");
  assert.equal(roles.find((token) => token.text === "Capsule" && token.line === 9)?.role, "capsule");
});

test("a fault says where it stands, what it is, and what it cost", () => {
  const { faults } = analyse(UNREADABLE);
  const [fault] = faults;
  assert.ok(fault);
  assert.equal(fault!.reason, "unexpected-character");
  assert.equal(fault!.line, 6);
  assert.equal(fault!.column, 13);
  assert.equal(fault!.text, ">");
  // The extent is where reading went on, and it is the language's unit that says so:
  // the line's break ends what the line carried.
  assert.equal(fault!.extent, "line");
});

test("a fault that is a consequence of another names it, and names its line", () => {
  // The unreadable line carried the brace that would have closed the scope, so the
  // closing brace left over at line 9 closes nothing. Standing on its own it reads as
  // a stray form no declaration takes, which is true of every stray brace and gives a
  // reader no line to go to; it names the fault it follows from instead, because
  // repairing line 6 is what takes this fault away with it.
  const [, consequence] = analyse(UNREADABLE).faults;
  assert.ok(consequence);
  assert.equal(consequence!.reason, "declaration-form");
  assert.equal(consequence!.text, "}");
  // The fault is still reported where it stands, with the reason and the extent the
  // file's broken structure is reported by; naming the cause adds to it and takes
  // nothing from it, because losing the information that the structure is broken
  // would cost more than the wording does.
  assert.equal(consequence!.extent, "declaration");
  assert.ok(consequence!.because, "the fault says nothing about what it follows from");
  assert.equal(consequence!.because!.reason, "unexpected-character");
  assert.equal(consequence!.because!.line, 6);
  assert.equal(consequence!.because!.column, 13);
});

test("a closing brace with nothing before it follows from nothing", () => {
  // Nothing in this file was unbalanced, so there is no earlier fault to name. The
  // fault stands on its own account, and a cause invented for it would send a reader
  // to a line that is not where the fault is.
  const { faults } = analyse("tp A cp {}\n}\n");
  assert.equal(faults.length, 1);
  assert.equal(faults[0]!.reason, "declaration-form");
  assert.equal(faults[0]!.text, "}");
  assert.equal(faults[0]!.because, undefined);
});

test("a fault a gate names is the one met first, and carries no cause", () => {
  // A gate refuses with one fault and stops; there is no second fault for the first to
  // have caused, so the attribution is a reader's and never reaches the gate's answer.
  const { faults } = analyse(UNREADABLE);
  const [first] = faults;
  assert.ok(first);
  assert.equal(first!.reason, "unexpected-character");
  assert.equal(first!.because, undefined);
});

test("a line that is not a declaration declares nothing", () => {
  // `goto end` is two words side by side, which is the shape of a `vr` declaration
  // and not one. Reading it as a declaration told a reader that `goto` was a
  // variable of this file's own and that `end` was a type it named; neither name is
  // bound here, so both are what the contract says a bare use is.
  const roles = semanticRoles(UNREADABLE)
    .filter((token) => token.line === 3)
    .map((token) => `${token.text}:${token.role}`);
  assert.deepEqual(roles, ["goto:identifier-reference", "end:identifier-reference"]);
});

test("a document the parser refuses still answers rather than throwing", () => {
  for (const source of ["tp\n", "tp X\n", "}\n", "tp X cp {\n", "vr\n"]) {
    assert.doesNotThrow(() => semanticRoles(source), source);
  }
});
