import assert from "node:assert/strict";
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import test from "node:test";

import { declaringAbove, foundIn, statedBoundary } from "../src/manifest.ts";
import { answerFrom } from "../src/resolve.ts";

// Finding a declaring file and reading what it says, measured against real directories,
// because a test that faked the walk would be testing the fake. The order the owner ruled
// (2026-09-30): a project declares where it ends with a file, a reader walks upward from a
// file's own directory until it meets one, and the one it meets first answers.
//
// The two forms are what this file is about: `memar.manifest.{format}` for a project with
// something to say, and `manifest.yaml` for the project whose whole declaration is that the
// file is there. The second is the one most projects will write, it is the one that resolves
// today, and the first is deliberately *not* made to behave like it — a project that wrote a
// claim and got a path answer would never learn its claim was in a file nobody reads.

/** A tree holding the given files, and its own root.
 *  @param files paths relative to the tree's root, each to that file's content */
function tree(files: Record<string, string>): string {
  const root = mkdtempSync(join(tmpdir(), "khayyam-resolve-"));
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

test("a project's minimal declaring file is a marker, and its text is not read", (t) => {
  // The stronger half of the owner's ruling: a project whose only declaration is where it
  // ends needs to write one file and nothing else. Reading its text would mean guessing at
  // YAML this server has no parser for, and a manifest read as nothing is a manifest that
  // declares nothing — the quietest wrong answer available.
  const root = tree({ "manifest.yaml": "anything: at all\nnot: a declaration\n", "src/unit.kh": "" });
  t.after(() => drop(root));
  const walked = declaringAbove(join(root, "src"), undefined);
  assert.equal(walked.at, join(root, "manifest.yaml"));
  assert.equal(walked.form, "minimal");
  assert.equal(walked.read, undefined, "its text was not read, so nothing is said about it");
  assert.equal(walked.unreadable, undefined, "and it is not a file this server failed to read either");
});

test("under a stated root, an address resolves to a document and the answer says which mechanism answered", (t) => {
  const root = tree({ "manifest.yaml": "", "modules/boolean.kh": "tp Bool cp {}\n", "src/unit.kh": "" });
  t.after(() => drop(root));
  const here = join(root, "src", "unit.kh");
  const answered = answerFrom(declaringAbove(here, undefined), "modules/boolean.kh", here);
  assert.equal(answered.via, "a stated root");
  assert.equal(answered.found?.uri.endsWith("/modules/boolean.kh"), true);
  assert.equal(answered.found?.text, "tp Bool cp {}\n");
  assert.equal(answered.because, undefined, "an answer that resolves carries no complaint");
  assert.deepEqual(answered.base?.directory, root, "and the base is the directory the marker is in");
});

test("an address that names nothing under a stated root says so in a sentence with both parts", (t) => {
  // Two things a reader has to act on and which used to be reported as one: the root was
  // found, and the address reached nothing. A reader told only "not found" cannot tell which
  // of the two is wrong, and writing the file is not the repair in both cases.
  const root = tree({ "manifest.yaml": "", "src/unit.kh": "" });
  t.after(() => drop(root));
  const here = join(root, "src", "unit.kh");
  const answered = answerFrom(declaringAbove(here, undefined), "modules/nowhere.kh", here);
  assert.equal(answered.found, undefined);
  assert.equal(answered.via, "a stated root");
  assert.match(answered.because ?? "", /declares itself the root/, "the root was found");
  assert.match(answered.because ?? "", /names nothing under it/, "and the address reached nothing");
});

test("an address is read under the root even when the writing file is far below it", (t) => {
  const root = tree({ "manifest.yaml": "", "modules/boolean.kh": "", "src/a/b/c/unit.kh": "" });
  t.after(() => drop(root));
  const here = join(root, "src", "a", "b", "c", "unit.kh");
  const answered = answerFrom(declaringAbove(here, undefined), "modules/boolean.kh", here);
  assert.equal(answered.found?.uri.endsWith("/modules/boolean.kh"), true, "depth is not a base");
});

test("a rich manifest is read and reported as read, and does not fall through to the minimal form's answer", (t) => {
  // The reason the two forms are separate rather than one form with more fields: a project
  // that wrote a claim and received a path answer would never learn that its claim was in a
  // file nobody reads. Silence here is the failure this whole separation exists to prevent.
  const root = tree({ "memar.manifest.json": '{"claim":"memar/*"}', "modules/boolean.kh": "tp Bool cp {}\n", "src/unit.kh": "" });
  t.after(() => drop(root));
  const here = join(root, "src", "unit.kh");
  const walked = declaringAbove(here, undefined);
  assert.equal(walked.form, "declared");
  assert.deepEqual(walked.read, { claim: "memar/*" }, "JSON was read");
  const answered = answerFrom(walked, "modules/boolean.kh", here);
  assert.equal(answered.via, "a module manifest", "and it is named, not the other form");
  assert.equal(answered.found, undefined, "a manifest this server cannot yet ask answers nothing");
  assert.match(answered.because ?? "", /does not yet know how to ask it anything/);
});

test("a rich manifest in a format this server does not read is named, not approximated", (t) => {
  const root = tree({ "memar.manifest.yaml": "claim: memar/*\n", "src/unit.kh": "" });
  t.after(() => drop(root));
  const here = join(root, "src", "unit.kh");
  const walked = declaringAbove(here, undefined);
  assert.equal(walked.form, "declared");
  assert.equal(walked.read, undefined);
  assert.match(walked.unreadable?.reason ?? "", /issue/, "and the remedy is one entry of work");
});

test("a directory holding both forms is refused, because choosing between them invents a precedence", (t) => {
  const root = tree({ "manifest.yaml": "", "memar.manifest.json": "{}", "src/unit.kh": "" });
  t.after(() => drop(root));
  const walked = declaringAbove(join(root, "src"), undefined);
  assert.equal(walked.at, undefined, "and no form answers, because picking one would be a decision nobody made");
  assert.equal(walked.ambiguous?.length, 2);
  assert.match(walked.because ?? "", /may not choose between them/);
  assert.deepEqual(
    foundIn(root).map((each) => each.form),
    ["minimal", "declared"],
    "and both are found, each telling which form it is",
  );
});

test("the nearest declaring file answers, and a nested project's marker is its own root", (t) => {
  // Nesting is the case the owner's ruling has to serve: a whole framework as one project and
  // each of its parts as another. A subdirectory that declares itself is that subdirectory's
  // root, which is what makes the two levels possible without either one dictating the other.
  const root = tree({
    "manifest.yaml": "",
    "modules/boolean.kh": "",
    "parts/thing/manifest.yaml": "",
    "parts/thing/inside.kh": "",
  });
  t.after(() => drop(root));
  const outer = join(root, "parts", "thing");
  assert.equal(declaringAbove(join(root, "parts"), undefined).at, join(root, "manifest.yaml"));
  assert.equal(declaringAbove(outer, undefined).at, join(outer, "manifest.yaml"));
  const here = join(outer, "inside.kh");
  const answered = answerFrom(declaringAbove(here, undefined), "inside.kh", here);
  assert.equal(answered.found?.uri.endsWith("/parts/thing/inside.kh"), true, "the part resolves against itself");
});

test("a file that is not a declaring file is not one, and the walk carries on past it", (t) => {
  // A repository can hold a file called `manifest.yaml` that describes the project for the
  // outside world and says nothing about addresses. Under the owner's ruling the name *is* the
  // declaration, so this repository's own root file is one — which is a question for its owner
  // and not something a resolver may decide by looking at the content.
  const root = tree({ "readme.yaml": "", "manifest.yaml": "", "src/unit.kh": "" });
  t.after(() => drop(root));
  assert.deepEqual(
    foundIn(root).map((each) => join(each.at.slice(root.length + 1), "..")).length,
    1,
    "one declaring file, and it is not the readme",
  );
  assert.equal(declaringAbove(join(root, "src"), undefined).at, join(root, "manifest.yaml"));
});

test("with no declaring file anywhere, the answer names where the walk stopped", (t) => {
  const root = tree({ "src/unit.kh": "" });
  t.after(() => drop(root));
  const walked = declaringAbove(join(root, "src"), root);
  assert.equal(walked.at, undefined);
  assert.equal(walked.stopped, "boundary");
  assert.match(walked.because ?? "", /boundary stated in advance/);
  assert.doesNotMatch(walked.because ?? "", /\.agents|\.git/, "no directory name is what ends a walk");
});

test("a boundary stated in advance that is not above the file neither bounds it nor refuses it", (t) => {
  const root = tree({ "src/unit.kh": "" });
  t.after(() => drop(root));
  const elsewhere = tree({ "manifest.yaml": "", "other/unit.kh": "" });
  t.after(() => drop(elsewhere));
  const walked = declaringAbove(join(root, "src"), elsewhere);
  assert.equal(walked.at, undefined, "nothing above a temp directory declares anything");
  assert.equal(walked.stopped, "filesystem", "so the walk ended where it really ended");
});

test("this repository's own root is where its documents say it is", (t) => {
  const told = process.env.MEMAR_ROOT;
  t.after(() => {
    if (told === undefined) delete process.env.MEMAR_ROOT;
    else process.env.MEMAR_ROOT = told;
  });
  const root = tree({ "src/unit.kh": "" });
  t.after(() => drop(root));
  delete process.env.MEMAR_ROOT;
  assert.equal(statedBoundary(), undefined, "unset means nothing is stated in advance");
  process.env.MEMAR_ROOT = root;
  assert.equal(statedBoundary(), root);
  assert.equal(declaringAbove(join(root, "src"), undefined).stopped, "boundary");
});