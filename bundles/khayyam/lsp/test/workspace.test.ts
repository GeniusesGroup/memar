import assert from "node:assert/strict";
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve as resolvePath } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import test from "node:test";

import { resolutionOf, resolutionReach } from "../src/workspace.ts";

// What an address a document writes resolves to, and why not when it does not. Measured on
// trees this file wrote rather than on this repository, because a repository's own root
// holding a file named `manifest.yaml` is a fact about that repository's owner — and whether
// it is a declaration is not something a test here may decide by looking at its content.

// This repository's root, which is a document of the project the walk starts in.
const ROOT = resolvePath(fileURLToPath(new URL("../../../../", import.meta.url)));
const IN_THE_REPOSITORY = pathToFileURL(join(ROOT, "main.kh")).href;

/** A tree with a declaring file and whatever else the test needs. */
function tree(files: Record<string, string>): string {
  const root = mkdtempSync(join(tmpdir(), "khayyam-workspace-"));
  for (const [where, what] of Object.entries(files)) {
    const at = join(root, where);
    mkdirSync(dirname(at), { recursive: true });
    writeFileSync(at, what, "utf8");
  }
  return root;
}

const drop = (root: string): void => {
  rmSync(root, { recursive: true, force: true });
};

test("a document in a project that has declared nothing is refused, and the sentence says what to write", (t) => {
  const root = tree({ "unit.kh": "" });
  t.after(() => drop(root));
  const resolved = resolutionOf(pathToFileURL(join(root, "unit.kh")).href, "modules/boolean.kh");
  assert.equal(resolved.found, undefined, "nothing declares where this project ends, so nothing resolves");
  assert.equal(resolved.base, undefined, "and no base is claimed, because none was found by looking anywhere");
  assert.match(resolved.because ?? "", /declaring file of the project/, "the rule, stated once");
  assert.match(resolved.because ?? "", /declaring file, not a file/, "the sentence says what to write");
});

test("a document in a project that has declared its end reaches the file its address names", (t) => {
  const root = tree({ "manifest.yaml": "", "modules/boolean.kh": "tp Bool cp {}\n", "src/unit.kh": "" });
  t.after(() => drop(root));
  const here = pathToFileURL(join(root, "src", "unit.kh")).href;
  const resolved = resolutionOf(here, "modules/boolean.kh");
  assert.equal(resolved.via, "a stated root", "and which mechanism answered is named");
  assert.equal(resolved.found?.text, "tp Bool cp {}\n");
  assert.deepEqual(resolved.base?.directory, root);
});

test("with a reach, an address in one of these trees resolves to the document it names", (t) => {
  const root = tree({ "manifest.yaml": "", "modules/boolean.kh": "tp Bool cp {}\n", "src/unit.kh": "" });
  t.after(() => drop(root));
  const here = pathToFileURL(join(root, "src", "unit.kh")).href;
  const reach = resolutionReach();
  assert.equal(reach.resolve("modules/boolean.kh", here).found?.text, "tp Bool cp {}\n");
  assert.equal(reach.resolve("modules/nowhere.kh", here).found, undefined);
  assert.match(reach.resolve("modules/nowhere.kh", here).because ?? "", /declares itself the root/);
});

test("a document this server holds is reached before anything else, because a place is read against the editor's text", (t) => {
  const root = tree({ "manifest.yaml": "", "modules/boolean.kh": "tp Bool cp {}\n", "src/unit.kh": "" });
  t.after(() => drop(root));
  const held = "tp Bool cp {}\n";
  const here = pathToFileURL(join(root, "src", "unit.kh")).href;
  assert.equal(resolutionReach(() => held).held(here), held);
  assert.equal(resolutionReach().held(here), undefined, "and a document this server holds none of is held none of");
});

test("the reach a reader gets refuses rather than guessing when the address names nothing", () => {
  // The property that matters about a resolver with no manifest: it must not invent a place.
  // A reader told only "nothing there" cannot act, and one sent to a guessed path is worse —
  // so the question of where a project ends is asked first and its absence is the answer.
  const reach = resolutionReach();
  const answered = reach.resolve("anything.kh", IN_THE_REPOSITORY);
  assert.equal(answered.found, undefined, "no address resolves without a project to resolve it against");
  assert.ok((answered.because ?? "").length > 0, "and the reason is a sentence rather than nothing");
  assert.doesNotMatch(answered.because ?? "", /^\s*$/);
});

test("a reader is told which mechanism answered, so a refusal names the one that did not", (t) => {
  const root = tree({ "memar.manifest.json": '{"claim":"memar/*"}', "modules/boolean.kh": "", "src/unit.kh": "" });
  t.after(() => drop(root));
  const here = pathToFileURL(join(root, "src", "unit.kh")).href;
  const resolved = resolutionOf(here, "modules/boolean.kh");
  assert.equal(resolved.via, "a module manifest");
  assert.equal(resolved.found, undefined, "a manifest this server cannot yet ask answers nothing");
  assert.match(resolved.because ?? "", /does not yet know how to ask it anything/);
  assert.doesNotMatch(resolved.because ?? "", /a stated root/, "and it is not passed off as the other form");
});