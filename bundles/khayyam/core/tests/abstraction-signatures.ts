/* For license and copyright information please see the LEGAL file in the code repository */

import assert from "node:assert/strict";
import test from "node:test";
import { analyze } from "../src/frontend.ts";

const BUDGET_SECONDS = 30;
const TIER = "unit";
const COST = { subprocesses: 0, writes_files: false, clock_waits: false };
const SUBJECT = "Khayyam abstraction signature declaration-kind validation";
const options = { timeout: BUDGET_SECONDS * 1000 };
const fs = (files: Record<string, string> = {}) => ({ read: (path: string) => files[path] });

for (const [name, source, files] of [
  ["local capsule input", "tp Spec ab\ntp Value cp {}\ntp Read mt (self Spec) (value Value) ()\n", {}],
  ["local capsule output", "tp Spec ab\ntp Value cp {}\ntp Read mt (self Spec) () (value Value)\n", {}],
  ["imported capsule input", 'tp Value in "value.kh"\ntp Spec ab\ntp Read mt (self Spec) (value Value) ()\n', { "value.kh": "tp Value cp {}\n" }],
  ["imported receiver and capsule output", 'tp Spec in "spec.kh"\ntp Value in "value.kh"\ntp Read mt (self Spec) () (value Value)\n', { "spec.kh": "tp Spec ab\n", "value.kh": "tp Value cp {}\n" }],
  ["reexported capsule output", 'tp Value in "middle.kh"\ntp Spec ab\ntp Read mt (self Spec) () (value Value)\n', { "middle.kh": 'tp Value in "value.kh"\n', "value.kh": "tp Value cp {}\n" }],
] as const) {
  test(name, options, () => {
    const result = analyze("main.kh", source, fs(files));
    assert.equal(result.outcome, "refuse");
    if (result.outcome !== "refuse") return;
    assert.equal(result.reason, "capsule-in-abstraction-signature");
    assert.equal(result.line, 3);
    assert.equal(result.reference?.parameter, "value");
    assert.equal(result.reference?.type, "Value");
    assert.equal(result.reference?.declarationLine, name.startsWith("local") ? 2 : 1);
  });
}

test("abstract values need no target realization", options, () => {
  assert.equal(analyze("main.kh", "tp Spec ab\ntp Value ab\ntp Read mt (self Spec) (value Value) (result Value)\n", fs()).outcome, "accept");
});

test("capsule receiver may use capsules", options, () => {
  assert.equal(analyze("main.kh", "tp Spec cp {}\ntp Value cp {}\ntp Read mt (self Spec) (value Value) (result Value)\n", fs()).outcome, "accept");
});

test("missing import keeps its original diagnostic", options, () => {
  const result = analyze("main.kh", 'tp Value in "missing.kh"\ntp Spec ab\ntp Read mt (self Spec) () (value Value)\n', fs());
  assert.equal(result.outcome, "refuse");
  if (result.outcome === "refuse") assert.equal(result.reason, "unresolved-import");
});

test("cyclic reexports are refused without recursion", options, () => {
  const result = analyze("main.kh", 'tp Value in "a.kh"\ntp Spec ab\ntp Read mt (self Spec) () (value Value)\n', fs({
    "a.kh": 'tp Value in "b.kh"\n',
    "b.kh": 'tp Value in "a.kh"\n',
  }));
  assert.equal(result.outcome, "refuse");
  if (result.outcome === "refuse") assert.equal(result.reason, "unresolved-type-declaration");
});
