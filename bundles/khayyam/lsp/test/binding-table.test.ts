import assert from "node:assert/strict";
import test from "node:test";

import { ROLES } from "../src/contract.ts";
import { bindingsIn, DECLARED, included } from "../src/binding-table.ts";
import { itemsOnLine } from "../src/document-items.ts";
import { readUnit } from "../../core/src/parse.ts";

// What a name in a document binds to, and what that binding is: the role it carries
// when it is declared, where it was declared in this document, and whether it arrived
// through an inclusion. This is the table a role follows, so it is fixed here on its
// own — the role stream can only be read against it, and a stream that looks right can
// still have bound a name to the wrong declaration.

const SOURCE = [
  'tp Bool in "math/boolean"',
  "tp Reader ab",
  "tp Set mt (self Reader) (key String) (err Error) {}",
  "vr held Reader",
  "",
].join("\n");

/** The table of one document, built the way the reading builds it: the declarations
 *  the parse recovered, against the items the scan found on their lines. */
function tableOf(source: string, items = itemsOnLine(source)) {
  return bindingsIn(readUnit("document.kh", source).unit.declarations, items);
}

const TABLE = tableOf(SOURCE);

test("the role a declaration's own name carries, one entry per declaration form", () => {
  // A form is one thing said two ways, so the two ways are held in one entry and are
  // changed together; what each entry carries is the role and the sentence that says
  // what the name IS, which is the whole of what a role answers.
  assert.deepEqual(DECLARED, {
    "tp-in": { role: "included-type", origin: "included from another file" },
    "vr-in": { role: "included-variable", origin: "included from another file" },
    "tp-cp": { role: "capsule", origin: "a Capsule declared in this file" },
    "tp-ab": { role: "abstraction", origin: "an Abstraction declared in this file" },
    "tp-mt": { role: "method", origin: "a Method declared in this file" },
    "tp-sc": { role: "scope", origin: "a Scope declared in this file" },
    vr: { role: "variable", origin: "a Variable declared in this file" },
  });
});

test("every role a declaration form carries is a role the display contract defines", () => {
  for (const [form, declared] of Object.entries(DECLARED)) {
    assert.ok(ROLES.includes(declared.role), `${form} carries ${declared.role}, which is not in the contract`);
  }
});

test("a name binds to the declaration the file read it in", () => {
  for (const [name, form] of [
    ["Reader", "tp-ab"],
    ["Set", "tp-mt"],
    ["held", "vr"],
  ] as const) {
    assert.equal(TABLE.bindingOf(name)?.form, form, `${name} is declared here`);
  }
});

test("a name this file does not declare binds to nothing", () => {
  // A type the file does not declare, and a method called on something, are both
  // names no binding answers, which is a different answer from one a binding answers
  // with no place.
  for (const name of ["String", "Copy", "key"]) {
    assert.equal(TABLE.bindingOf(name), undefined, `${name} is not bound in this file`);
  }
});

test("a name this file declares was declared where its own name stands", () => {
  assert.deepEqual(TABLE.placeOf("Reader"), { line: 1, startChar: 3, length: 6 });
  assert.deepEqual(TABLE.placeOf("Set"), { line: 2, startChar: 3, length: 3 });
  assert.deepEqual(TABLE.placeOf("held"), { line: 3, startChar: 3, length: 4 });
  assert.equal(TABLE.placeOf("String"), undefined, "a name nothing binds has no place either");
});

test("a name that arrived by an inclusion is bound here and declared elsewhere", () => {
  const binding = TABLE.bindingOf("Bool");
  assert.equal(binding?.form, "tp-in");
  assert.equal(included(binding!), true);
  assert.equal(
    TABLE.placeOf("Bool"),
    undefined,
    "an inclusion is not a declaration of the name, so there is no place for it in this file",
  );
  // The two absences are different, which is why they are not one absent value: the
  // name stands on the inclusion line, but that line is a use of it.
  assert.deepEqual(TABLE.nameStandsAt(binding!), { line: 0, startChar: 3, length: 4 });
});

test("a later declaration of the same name does not displace an inclusion", () => {
  // A name collision is an architecture error, not a disambiguation problem, so the
  // first binding is the one the whole document answers from.
  const table = tableOf(['tp Bool in "math/boolean"', "tp Bool cp {}", ""].join("\n"));
  assert.equal(table.bindingOf("Bool")?.form, "tp-in");
});

test("the declaration the parse read on a line is that line's declaration", () => {
  assert.equal(TABLE.declarationOnLine(2), TABLE.bindingOf("Reader"), "lines are one-based, as the representation counts them");
  assert.equal(TABLE.declarationOnLine(3)?.form, "tp-mt");
  assert.equal(TABLE.declarationOnLine(4)?.form, "vr");
  assert.equal(TABLE.declarationOnLine(99), undefined, "a line no declaration stands on has no declaration");
});

test("a declaration is paired with its line by the line, not by counting", () => {
  // The declaration and the place of its own name come from two different readings of
  // the file, so the pairing is what can be lost: given items from a file that is not
  // this one, every declaration is still bound and none of them carries a place.
  const table = tableOf(SOURCE, itemsOnLine("tp Other ab\n"));
  assert.equal(table.bindingOf("Set")?.form, "tp-mt", "the binding survives");
  assert.equal(table.placeOf("Set"), undefined, "no place is found for a name that is not on the line");
  assert.equal(table.nameStandsAt(table.bindingOf("Set")!), undefined);
});
