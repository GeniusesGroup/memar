/* For license and copyright information please see the LEGAL file in the code repository */

import assert from "node:assert/strict";
import test from "node:test";
import { inspectDeclaration, type SourceSnapshot } from "../inspect-declaration.ts";
import type { Reach } from "../../../lsp/src/definition.ts";

export const TIER = "unit";
export const BUDGET_SECONDS = 30;
export const COST = { subprocesses: 0, writes: false, waits: false };
const uri = "file:///unit/main.kh";
const snapshot = (text: string, version = 3): SourceSnapshot => ({ uri, text, version });
const absent: Reach = { resolve: () => ({ because: "no route" }), held: () => undefined };
const position = (text: string, line: number, name: string) => ({ line, character: text.split("\n")[line]!.indexOf(name) });

test("Inspect_Declaration returns declaration category and direct method signatures", () => {
  const text = "tp Box cp {}\ntp Copy mt (self Box) (input Box) (output Box)\n";
  const answer = inspectDeclaration(snapshot(text), position(text, 0, "Box"), absent);
  assert.equal(answer.state, "resolved");
  assert.equal(answer.declaration?.category, "cp");
  assert.deepEqual(answer.declaration?.provenance, []);
  assert.equal(answer.snapshot.version, 3);
  assert.match(answer.snapshot.hash, /^sha256:[0-9a-f]{64}$/);
  assert.equal(answer.reach.complete, true);
  assert.equal(answer.declaration?.methods?.complete, false);
  assert.equal(answer.declaration?.methods?.extent, "direct-in-reached-units");
  assert.deepEqual(answer.declaration?.methods?.entries.map(entry => entry.name), ["Copy"]);
  const method = inspectDeclaration(snapshot(text), position(text, 1, "Copy"), absent).declaration;
  assert.equal(method?.category, "mt");
  assert.deepEqual(method?.signature, {
    owner: [{ name: "self", type: "Box" }],
    influencing: [{ name: "input", type: "Box" }],
    influenced: [{ name: "output", type: "Box" }],
  });
});

test("Inspect_Declaration follows two includes and reads held target text and version", () => {
  const text = 'tp Box in "middle"\n';
  const target = "file:///unit/target.kh";
  const held = "// unsaved\ntp Box ab\n";
  const reach = {
    resolve: (address: string) => ({ via: "fixture", found: address === "middle"
      ? { uri: "file:///unit/middle.kh", text: 'tp Box in "target"\n' }
      : { uri: target, text: "tp Box cp {}\n" } }),
    held: (id: string) => id === target ? held : undefined,
    version: (id: string) => id === target ? 12 : undefined,
  };
  const answer = inspectDeclaration(snapshot(text), position(text, 0, "Box"), reach);
  assert.equal(answer.state, "resolved");
  assert.equal(answer.declaration?.category, "ab");
  assert.equal(answer.declaration?.location.uri, target);
  assert.equal(answer.declaration?.location.range.start.line, 1);
  assert.equal(answer.declaration?.snapshot.version, 12);
  assert.deepEqual(answer.declaration?.provenance.map(hop => hop.address), ["middle", "target"]);
  const changed = inspectDeclaration(snapshot(text), position(text, 0, "Box"), { ...reach, held: () => undefined });
  assert.notEqual(answer.declaration?.snapshot.hash, changed.declaration?.snapshot.hash);
  assert.equal(changed.declaration?.category, "cp");
});

test("Inspect_Declaration exposes unresolved reach without inventing category", () => {
  const text = 'tp Box in "absent"\n';
  const answer = inspectDeclaration(snapshot(text), position(text, 0, "Box"), absent);
  assert.equal(answer.state, "incomplete");
  assert.equal(answer.declaration, undefined);
  assert.equal(answer.reach.complete, false);
  assert.match(answer.reach.issues[0]!.reason, /no route/);
  const local = 'tp Box cp {}\ntp Missing in "absent"\n';
  const known = inspectDeclaration(snapshot(local), position(local, 0, "Box"), absent);
  assert.equal(known.state, "resolved");
  assert.equal(known.declaration?.category, "cp");
  assert.equal(known.reach.complete, false);
});

test("Inspect_Declaration reports unreadable resolution as incomplete", () => {
  const text = 'tp Box in "target"\n';
  const answer = inspectDeclaration(snapshot(text), position(text, 0, "Box"), {
    held: () => undefined,
    resolve: () => ({ found: { uri: "file:///unit/target.kh", text: "tp Box cp {\n" } }),
  });
  assert.equal(answer.reach.complete, false);
  assert.ok(answer.reach.issues.some(issue => issue.word === "unbalanced-block"));
  assert.equal(answer.declaration, undefined);
  assert.equal(answer.state, "incomplete");
});

test("Inspect_Declaration distinguishes diamonds from cycles and terminates real cycles", () => {
  const files: Record<string, string> = {
    left: 'tp Box in "target"\n', right: 'tp Extra in "target"\n', target: "tp Box cp {}\ntp Extra cp {}\n",
  };
  const reach: Reach = { held: () => undefined, resolve: address => ({ found: { uri: `file:///unit/${address}.kh`, text: files[address]! } }) };
  const diamond = 'tp Box in "left"\ntp Extra in "right"\n';
  const answer = inspectDeclaration(snapshot(diamond), position(diamond, 0, "Box"), reach);
  assert.equal(answer.state, "resolved");
  assert.equal(answer.reach.complete, true);
  assert.equal(answer.reach.documents.length, 4);
  files.target = 'tp Box in "left"\ntp Extra cp {}\n';
  const cycle = inspectDeclaration(snapshot(diamond), position(diamond, 0, "Box"), reach);
  assert.equal(cycle.state, "incomplete");
  assert.equal(cycle.declaration, undefined);
  assert.ok(cycle.reach.issues.some(issue => issue.word === "inclusion-cycle"));
});

test("Inspect_Declaration refuses quoted text as binding and uses UTF-16 half-open ranges", () => {
  const text = 'tp Box in "Box"\n';
  assert.equal(inspectDeclaration(snapshot(text), { line: 0, character: 12 }, absent).state, "not-a-name");
  const unicode = "tp Box cp {}\ntp Copy mt (self Box) (/*𐐀*/ next Box) ()\n";
  const answer = inspectDeclaration(snapshot(unicode), position(unicode, 1, "next"), absent);
  assert.equal(answer.state, "resolved");
  assert.equal(answer.declaration?.category, undefined);
  const start = unicode.split("\n")[1]!.indexOf("next");
  assert.deepEqual(answer.declaration?.location.range, { start: { line: 1, character: start }, end: { line: 1, character: start + 4 } });
});
