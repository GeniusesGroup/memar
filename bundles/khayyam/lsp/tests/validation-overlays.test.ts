/* For license and copyright information please see the LEGAL file in the code repository */
import assert from "node:assert/strict";
import test from "node:test";
import { mkdtempSync, writeFileSync, readFileSync, readdirSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { pathToFileURL } from "node:url";
import { resolutionReach } from "../src/workspace.ts";
import { validateSource } from "../../services/validate-source/validate-source.ts";

export const BUDGET_SECONDS = 30;
export const SUBJECT = "Validate_Source manifest overlay resolution without writes";

test("validation resolves new unsaved included units and preserves disk fallback and bytes", t => {
  const folder = mkdtempSync(join(tmpdir(), "khayyam-validation-"));
  t.after(() => rmSync(folder, { recursive: true, force: true }));
  writeFileSync(join(folder, "manifest.yaml"), "");
  writeFileSync(join(folder, "disk.kh"), "tp Disk ab\n");
  const uri = pathToFileURL(join(folder, "main.kh")).href;
  const included = pathToFileURL(join(folder, "unsaved.kh")).href;
  const overlays = [{ uri: included, version: 3, text: "tp New ab\n" }];
  const proposal = { uri, wholeText: 'tp New in "unsaved.kh"\ntp Disk in "disk.kh"\n' };
  const names = readdirSync(folder);
  const before = new Map(names.map(name => [name, readFileSync(join(folder, name))]));
  const reach = resolutionReach(target => overlays.find(source => source.uri === target)?.text);
  const answer = validateSource({ proposal, overlays }, reach);
  assert.equal(answer.gateAccepted, true);
  assert.equal(answer.documents.find(source => source.uri === included)?.version, 3);
  assert.ok(answer.inclusions.every(hop => hop.via === "a stated root"));
  assert.ok(answer.documents.some(source => source.uri === pathToFileURL(join(folder, "disk.kh")).href));
  overlays[0]!.text = "tp New cp {\n";
  const invalid = validateSource({ proposal, overlays }, reach);
  assert.equal(invalid.gateAccepted, false);
  assert.ok(invalid.diagnostics.some(fault => fault.source.uri === included && fault.word === "unbalanced-block"));
  assert.deepEqual(readdirSync(folder), names);
  for (const [name, bytes] of before) assert.deepEqual(readFileSync(join(folder, name)), bytes);
});
