/* For license and copyright information please see the LEGAL file in the code repository */
import assert from "node:assert/strict";
import test from "node:test";
import { identifySource } from "../../inspect-declaration/inspect-declaration.ts";
import { validateSource } from "../validate-source.ts";

export const BUDGET_SECONDS = 30;
export const SUBJECT = "Validate_Source: protocol/validate-source.kh";
const uri = "file:///main.kh";
const reach = { held: () => undefined, resolve: () => ({ because: "no route" }) };
const whole = (text: string) => ({ uri, version: 8, wholeText: text });

test("Validate_Source exposes reader/gate refusals and bounded guarantees", () => {
  const malformed = validateSource({ proposal: whole("tp Box cp {}\ntp Run mt (self Box) () () {\nself.Go()\n}\n") }, reach);
  assert.equal(malformed.gateAccepted, false);
  assert.ok(malformed.diagnostics.some(d => d.word === "declaration-form" && d.source.uri === uri && d.range.start.line === 2));
  const indented = validateSource({ proposal: whole("tp Box cp {}\ntp Run mt (self Box) () () {\n    self.Go()\n}\n") }, reach);
  assert.deepEqual(indented.diagnostics.find(d => d.word === "declaration-form")!.range.start, { line: 2, character: 13 });
  const valid = validateSource({ proposal: whole("tp Box cp {}\ntp Run mt (self Box) () () {\nself.Go()()\n}\n") }, reach);
  assert.equal(valid.gateAccepted, true);
  assert.equal(valid.snapshot.version, 8);
  assert.equal(valid.typeSafetyEstablished, false);
  assert.equal(valid.executionEstablished, false);
  assert.ok(valid.checks.some(c => c.subject === "method-and-argument-types" && c.state === "unsupported"));
  assert.ok(validateSource({ proposal: whole("tp Run mt (self Missing) () ()\n") }, reach).diagnostics.some(d => d.word === "unbound-type-name"));
  assert.ok(validateSource({ proposal: whole('tp Box in "missing"\n') }, reach).diagnostics.some(d => d.word === "unresolved-import"));
});

test("Validate_Source pins unsaved included text and attributes its faults", () => {
  const target = "file:///included.kh";
  const routed = { held: () => undefined, resolve: () => ({ found: { uri: target, text: "tp Box ab\n" }, via: "fixture" }) };
  const proposal = whole('tp Box in "included"\n');
  assert.equal(validateSource({ proposal }, routed).gateAccepted, true);
  const overlays = [{ uri: target, version: 4, text: "tp Box cp {\n" }];
  const before = structuredClone(overlays);
  const invalid = validateSource({ proposal, overlays }, routed);
  assert.equal(invalid.gateAccepted, false);
  const diagnostic = invalid.diagnostics.find(d => d.word === "unbalanced-block")!;
  assert.equal(diagnostic.source.uri, target);
  assert.equal(diagnostic.source.version, 4);
  assert.ok(invalid.documents.some(d => d.uri === target && d.hash === diagnostic.source.hash));
  assert.deepEqual(overlays, before);
});

test("Validate_Source applies changes only to exact bases and refuses malformed proposals", () => {
  const base = { uri, version: 7, text: "tp Old ab\n" };
  const held = { ...reach, held: () => base.text, version: () => base.version };
  const edit = { range: { start: { line: 0, character: 3 }, end: { line: 0, character: 6 } }, text: "New" };
  const change = { base: identifySource(base), edits: [edit] };
  const answer = validateSource({ proposal: { uri, version: 8, change } }, held);
  assert.equal(answer.snapshot.hash, identifySource({ uri, text: "tp New ab\n" }).hash);
  assert.equal(answer.snapshot.version, 8);
  assert.equal(base.text, "tp Old ab\n");
  assert.throws(() => validateSource({ proposal: { uri, change: { ...change, base: { ...change.base, version: 6 } } } }, held), /stale/);
  assert.throws(() => validateSource({ proposal: whole("tp A ab"), overlays: [base, base] }, held), /duplicate/);
  assert.throws(() => validateSource({ proposal: { ...whole("tp A ab"), change } }, held), /exactly one/);
  for (const character of [-1, 999, 0.5]) {
    assert.throws(() => validateSource({ proposal: { uri, change: { ...change, edits: [{ ...edit, range: { start: { line: 0, character }, end: { line: 0, character } } }] } } }, held), /range/);
  }
  const unicode = { uri, version: 1, text: "tp A ab\n/*😀*/\n" };
  assert.throws(() => validateSource({ proposal: { uri, change: { base: identifySource(unicode), edits: [{ text: "", range: { start: { line: 1, character: 3 }, end: { line: 1, character: 3 } } }] } } }, { ...held, held: () => unicode.text, version: () => 1 }), /range/);
});
