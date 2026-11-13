/* For license and copyright information please see the LEGAL file in the code repository */
import assert from "node:assert/strict";
import test from "node:test";
import { holding, PROBE } from "./harness.ts";
import { identifySource } from "../../services/inspect-declaration/inspect-declaration.ts";

export const BUDGET_SECONDS = 30;
export const SUBJECT = "Validate_Source language server adapter";

test("validation wire analyzes proposed text without replacing held text", async t => {
  const source = "tp Box cp {}\n";
  const server = await holding(source);
  t.after(() => server.stop());
  const answer = await server.request<any>("khayyam/validateSource", { proposal: { uri: PROBE, version: 2, wholeText: "tp Box cp {\n" } });
  assert.equal(answer.gateAccepted, false);
  assert.equal(answer.snapshot.version, 2);
  const inspected = await server.request<any>("khayyam/inspectDeclaration", { textDocument: { uri: PROBE, version: 1 }, position: { line: 0, character: 4 } });
  assert.equal(inspected.snapshot.hash, identifySource({ uri: PROBE, text: source }).hash);
  await assert.rejects(server.request("khayyam/validateSource", { proposal: { uri: PROBE, change: { base: { ...identifySource({ uri: PROBE, text: source, version: 1 }), version: 0 }, edits: [] } } }), /stale/);
});
