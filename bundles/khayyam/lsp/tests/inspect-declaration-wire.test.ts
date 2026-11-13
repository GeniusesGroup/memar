/* For license and copyright information please see the LEGAL file in the code repository */

import assert from "node:assert/strict";
import test from "node:test";
import { holding, PROBE } from "./harness.ts";
import type { InspectionAnswer } from "../../services/inspect-declaration/inspect-declaration.ts";

export const TIER = "system";
export const BUDGET_SECONDS = 30;
export const COST = { subprocesses: 1, writes: false, waits: false };

test("Inspect_Declaration wire answers current unsaved version and refuses stale questions", async t => {
  const server = await holding("tp Box cp {}\n");
  t.after(() => server.stop());
  const ask = (version: number, line: number) => server.request<InspectionAnswer>("khayyam/inspectDeclaration", {
    textDocument: { uri: PROBE, version }, position: { line, character: 4 },
  });
  const initial = await ask(1, 0);
  assert.equal(initial?.snapshot.version, 1);
  assert.equal(initial?.declaration?.category, "cp");
  server.notify("textDocument/didChange", {
    textDocument: { uri: PROBE, version: 2 }, contentChanges: [{ text: "// unsaved\ntp Box ab\n" }],
  });
  const edited = await ask(2, 1);
  assert.equal(edited.snapshot.version, 2);
  assert.equal(edited.declaration?.category, "ab");
  assert.equal(edited.declaration?.location.range.start.line, 1);
  assert.notEqual(initial.snapshot.hash, edited.snapshot.hash);
  await assert.rejects(ask(1, 1), /version/);
  server.notify("textDocument/didChange", {
    textDocument: { uri: PROBE, version: 1 }, contentChanges: [{ text: "tp Stale cp {}\n" }],
  });
  assert.equal((await ask(2, 1)).snapshot.hash, edited.snapshot.hash);
});
