/* For license and copyright information please see the LEGAL file in the code repository */

import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, writeFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";
import { spawnSync } from "node:child_process";

import { checkFiles, parseCheckArguments } from "../check-files.ts";

// A corpus on disk: the command reads files, so the rows write real ones into a folder of
// their own and hand it as --root. Nothing here depends on the folder the run starts in.
function corpus(files: Record<string, string>): string {
  const root = mkdtempSync(join(tmpdir(), "kh-check-"));
  for (const [path, text] of Object.entries(files)) {
    mkdirSync(join(root, path, ".."), { recursive: true });
    writeFileSync(join(root, path), text);
  }
  return root;
}

const GOOD = "tp Thing ab\n";

test("arguments: --root and at least one file are required", () => {
  assert.equal(parseCheckArguments([]).ok, false);
  assert.equal(parseCheckArguments(["--root", "/r"]).ok, false);
  assert.equal(parseCheckArguments(["a.kh"]).ok, false);
});

test("arguments: --root, --draft REPO_PATH=LOCAL and files are read", () => {
  const parsed = parseCheckArguments(["--root", "/r", "--draft", "x/y.kh=/tmp/d.kh", "x/y.kh", "z.kh"]);
  assert.equal(parsed.ok, true);
  if (parsed.ok) {
    assert.equal(parsed.value.root, "/r");
    assert.deepEqual(parsed.value.files, ["x/y.kh", "z.kh"]);
    assert.equal(parsed.value.drafts.get("x/y.kh"), "/tmp/d.kh");
  }
});

test("arguments: a draft not shaped REPO_PATH=LOCAL is refused", () => {
  assert.equal(parseCheckArguments(["--root", "/r", "--draft", "nope", "a.kh"]).ok, false);
});

test("a file the front end accepts is reported accept", () => {
  const root = corpus({ "a.kh": GOOD });
  try {
    const result = checkFiles({ root, files: ["a.kh"], drafts: new Map() });
    assert.deepEqual(result.lines, ["accept  a.kh"]);
    assert.equal(result.refused, 0);
  } finally { rmSync(root, { recursive: true }); }
});

test("a refused file is reported with its path, reason and line, and counted", () => {
  const root = corpus({ "a.kh": GOOD, "b.kh": "tp Thing ab\nzzz not khayyam @@\n" });
  try {
    const result = checkFiles({ root, files: ["a.kh", "b.kh"], drafts: new Map() });
    assert.equal(result.refused, 1);
    assert.equal(result.lines[0], "accept  a.kh");
    assert.match(result.lines[1]!, /^refuse  b\.kh  [a-z-]+( line \d+)?$/);
  } finally { rmSync(root, { recursive: true }); }
});

test("a file that is not there is reported refuse, not thrown", () => {
  const root = corpus({});
  try {
    const result = checkFiles({ root, files: ["missing.kh"], drafts: new Map() });
    assert.equal(result.refused, 1);
    assert.match(result.lines[0]!, /^refuse  missing\.kh  file not found$/);
  } finally { rmSync(root, { recursive: true }); }
});

test("a draft stands in for the repository path it names", () => {
  const root = corpus({});
  const scratch = corpus({ "draft.kh": GOOD });
  try {
    const result = checkFiles({ root, files: ["new/time.kh"], drafts: new Map([["new/time.kh", join(scratch, "draft.kh")]]) });
    assert.deepEqual(result.lines, ["accept  new/time.kh"]);
  } finally { rmSync(root, { recursive: true }); rmSync(scratch, { recursive: true }); }
});

test("the command: prints, and exits 0 on accept, 1 on refuse, 2 on a bad command line", () => {
  const root = corpus({ "a.kh": GOOD, "b.kh": "@@@\n" });
  const command = join(import.meta.dirname, "..", "check.ts");
  try {
    const run = (...args: string[]) => spawnSync(process.execPath, [command, ...args], { encoding: "utf8", cwd: tmpdir() });
    const ok = run("--root", root, "a.kh");
    assert.equal(ok.status, 0);
    assert.match(ok.stdout, /accept {2}a\.kh/);
    assert.equal(run("--root", root, "a.kh", "b.kh").status, 1);
    const bad = run("a.kh");
    assert.equal(bad.status, 2);
    assert.match(bad.stderr, /--root/);
  } finally { rmSync(root, { recursive: true }); }
});
