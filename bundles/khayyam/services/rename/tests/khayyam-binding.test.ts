/* For license and copyright information please see the LEGAL file in the code repository */

import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdirSync, mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import { khayyamBinding, khayyamResidue } from "../khayyam-binding.ts";

import { renameDeclaration, type Summary } from "../declaration-rename.ts";

// The subject is the Khayyam binding at
// [`bundles/khayyam/services/rename/khayyam-binding.ts`](../khayyam-binding.ts), asked in process by
// the declaration-rename mechanism (`bundles/khayyam/services/rename/declaration-rename.ts`). The rule
// that service realizes is
// `bundles/khayyam/rules/declaration-rename/declaration-rename.md`: given the name of one
// declared type, the rule plans every place in the repository where that name is written as
// that declaration's own name, and rewrites those places and no others.
//
// What an occurrence *is* is this binding's answer, and it is Khayyam's: `scan` says what a
// token is and `readUnit` with `referencedTypes` says what a declaration references. The
// The mechanism's own behaviour — the corpus it reads, the plan it prints, dry and `--write`, the
// gate, the exit codes — is stated by the mechanism's own Test, beside it. The expectations
// below are the Khayyam half of the same rule: which places bind the name, which do not, and
// why each one that does not is reported rather than rewritten.

const REPOSITORY = fileURLToPath(new URL("../../../../../", import.meta.url));

/** The sources' own licence header, which every `.kh` file opens with under the comment
 *  policy rule. It is read rather than written so this suite cannot drift from the sources
 *  it is about. */
const LICENSE = readFileSync(
  join(REPOSITORY, "modules/time/duration/nano-in-second.kh"),
  "utf8",
).split("\n")[0]!;

// `modules/e/protocol/Target.kh` holds the declaration; `modules/e/protocol/detector.kh`
// imports it and composes it. The Go clue block at the end of the importer is residue, and
// its `Target` is a Go interface member written as a bare name — which is not a token
// `scan` reads, because `scan` reads the whole block as a comment, and is only a site
// because the residue mode reads the block's own extent.
const TARGET = `${LICENSE}

// Target is the thing a listener registers on. Target stays spelled here in prose.
// TargetKeeper composes it, and a parameter may be spelled Target too.
tp Target ab

// Fire fires it.
tp Fire mt (self Target) (t Target) ()

tp TargetKeeper ab {
    Target
}

// Compare names a parameter Target, which is a parameter and not the type.
tp Compare mt (self TargetKeeper) (Target TargetKeeper) ()

vr Target_Seen Target
`;

const DETECTOR = `${LICENSE}

// The path is a URI and not a name; Target appears in it as the file's own name.
tp Target in "modules/e/protocol/Target.kh"

tp Detector ab {
    Target
}
tp Detect mt (self Detector) (t Target) ()

// TODO(go-migrate):
/*
package e_p

type Detector interface {
    Target
}
*/
`;

const RIVAL = `${LICENSE}

tp Target ab
`;

function corpus(files: Record<string, string>): string {
  const root = mkdtempSync(join(tmpdir(), "khayyam-rename-"));
  for (const [path, text] of Object.entries(files)) {
    mkdirSync(dirname(join(root, path)), { recursive: true });
    writeFileSync(join(root, path), text, "utf8");
  }
  return root;
}

function at(root: string, path: string): string {
  return readFileSync(join(root, path), "utf8");
}

/** One run over a corpus of the test's own, or over this repository's sources. The two
 *  kinds of tree need different answers — a synthetic one is where the rule's refusals are,
 *  and the real one is where the rule's reach is — so each says which it is. `residue` hands
 *  the mechanism this port's own pass over a Go clue block, which is where the mode's reader
 *  lives now that the shared contract does not hold one. */
function rename(
  root: string,
  options: {
    name?: string;
    to?: string;
    declaration?: string;
    residue?: boolean;
    write?: boolean;
  } = {},
): Summary {
  return renameDeclaration(
    {
      root,
      unit: ".kh",
      name: options.name ?? "Target",
      to: options.to ?? "EventTarget",
      ...(options.declaration === undefined ? {} : { declaration: options.declaration }),
      ...(options.residue === true ? { residue: khayyamResidue } : {}),
      ...(options.write === undefined ? {} : { write: options.write }),
      values: ["modules"],
      excludes: [],
    },
    khayyamBinding,
  );
}

// The enumeration

test("every place that names the declaration is planned, and nothing else is", () => {
  const root = corpus({
    "modules/e/protocol/Target.kh": TARGET,
    "modules/e/protocol/detector.kh": DETECTOR,
  });
  const summary = rename(root);
  assert.deepEqual(
    summary.sites.map((site) => `${site.path}:${site.line}:${site.role}`),
    [
      "modules/e/protocol/Target.kh:5:declaration",
      "modules/e/protocol/Target.kh:8:signature",
      "modules/e/protocol/Target.kh:8:signature",
      "modules/e/protocol/Target.kh:11:composition",
      "modules/e/protocol/Target.kh:17:vr-type",
      "modules/e/protocol/detector.kh:4:inclusion",
      "modules/e/protocol/detector.kh:7:composition",
      "modules/e/protocol/detector.kh:9:signature",
    ],
  );
});

test("the declaration is named by the place and the line it stands at, and its route is reported", () => {
  const root = corpus({
    "modules/e/protocol/Target.kh": TARGET,
    "modules/e/protocol/detector.kh": DETECTOR,
  });
  const summary = rename(root);
  assert.deepEqual(summary.declaration, {
    path: "modules/e/protocol/Target.kh",
    line: 5,
    form: "tp-ab",
  });
  assert.deepEqual(summary.same_name.map((place) => `${place.path}:${place.line}`), [
    "modules/e/protocol/Target.kh:5",
  ]);
  assert.deepEqual(summary.carried_by, [
    { path: "modules/e/protocol/detector.kh", line: 4, form: "tp-in", kind: "tp" },
  ]);
});

test("the write renames every planned place and nothing else", () => {
  const root = corpus({
    "modules/e/protocol/Target.kh": TARGET,
    "modules/e/protocol/detector.kh": DETECTOR,
  });
  const summary = rename(root, { write: true });
  assert.equal(summary.written, true);
  const target = at(root, "modules/e/protocol/Target.kh");
  const detector = at(root, "modules/e/protocol/detector.kh");
  assert.match(target, /\ntp EventTarget ab\n/);
  assert.match(target, /\ntp Fire mt \(self EventTarget\) \(t EventTarget\) \(\)/);
  assert.match(target, /\ntp TargetKeeper ab \{\n {4}EventTarget\n\}/);
  assert.match(target, /\nvr Target_Seen EventTarget\n/);
  assert.match(detector, /\ntp EventTarget in "modules\/e\/protocol\/Target\.kh"/);
  assert.match(detector, /\ntp Detector ab \{\n {4}EventTarget\n\}/);
  assert.match(detector, /\ntp Detect mt \(self Detector\) \(t EventTarget\) \(\)/);
  assert.deepEqual(summary.files_changed, [
    "modules/e/protocol/Target.kh",
    "modules/e/protocol/detector.kh",
  ]);
});

// The three places a name is written without naming the declaration

test("a name in a comment is left alone and reported", () => {
  const root = corpus({
    "modules/e/protocol/Target.kh": TARGET,
    "modules/e/protocol/detector.kh": DETECTOR,
  });
  const summary = rename(root, { write: true });
  assert.deepEqual(
    [...new Set(summary.unread
      .filter((entry) => entry.class === "comment")
      .map((entry) => `${entry.path}:${entry.line}`))],
    [
      "modules/e/protocol/Target.kh:3",
      "modules/e/protocol/Target.kh:4",
      "modules/e/protocol/Target.kh:14",
      "modules/e/protocol/detector.kh:3",
    ],
  );
  const after = at(root, "modules/e/protocol/Target.kh");
  assert.match(after, /\/\/ Target is the thing a listener registers on\. Target stays spelled here in prose\./);
  assert.match(after, /\/\/ Compare names a parameter Target,/);
  assert.match(after, /\ntp EventTarget ab\n/);
});

test("an `in` path is a string literal and is never a name", () => {
  const root = corpus({
    "modules/e/protocol/Target.kh": TARGET,
    "modules/e/protocol/detector.kh": DETECTOR,
  });
  const summary = rename(root, { write: true });
  assert.deepEqual(
    summary.unread
      .filter((entry) => entry.class === "string-literal")
      .map((entry) => `${entry.path}:${entry.line}`),
    ["modules/e/protocol/detector.kh:4"],
  );
  assert.match(at(root, "modules/e/protocol/detector.kh"), /\ntp EventTarget in "modules\/e\/protocol\/Target\.kh"/);
});

test("a longer name carrying the name is a different declaration, and is reported as one", () => {
  const root = corpus({
    "modules/e/protocol/Target.kh": TARGET,
    "modules/e/protocol/detector.kh": DETECTOR,
  });
  const summary = rename(root, { write: true });
  const inside = summary.unread.filter((entry) => entry.class === "part-of-longer-identifier");
  assert.deepEqual(
    inside.map((entry) => `${entry.path}:${entry.line}:${entry.text}`).sort(),
    [
      "modules/e/protocol/Target.kh:10:TargetKeeper",
      "modules/e/protocol/Target.kh:15:TargetKeeper",
      "modules/e/protocol/Target.kh:15:TargetKeeper",
      "modules/e/protocol/Target.kh:17:Target_Seen",
    ],
  );
  assert.deepEqual(
    summary.longer_names.map((entry) => `${entry.name}@${entry.path}`),
    ["TargetKeeper@modules/e/protocol/Target.kh", "Target_Seen@modules/e/protocol/Target.kh"],
  );
  const target = at(root, "modules/e/protocol/Target.kh");
  assert.match(target, /\ntp TargetKeeper ab \{/);
  assert.match(target, /\nvr Target_Seen EventTarget\n/);
});

test("a parameter named like the declaration is a parameter and not the type", () => {
  const root = corpus({
    "modules/e/protocol/Target.kh": TARGET,
    "modules/e/protocol/detector.kh": DETECTOR,
  });
  const summary = rename(root, { write: true });
  assert.deepEqual(
    summary.left_alone
      .filter((site) => site.role === "parameter-name")
      .map((site) => `${site.path}:${site.line}:${site.why}`),
    ["modules/e/protocol/Target.kh:15:a parameter names a value, not a type"],
  );
  assert.match(
    at(root, "modules/e/protocol/Target.kh"),
    /\ntp Compare mt \(self TargetKeeper\) \(Target TargetKeeper\) \(\)/,
  );
});

// A file whose name carries the name

test("a file named after the declaration is reported and never renamed", () => {
  const root = corpus({
    "modules/e/protocol/Target.kh": TARGET,
    "modules/e/protocol/detector.kh": DETECTOR,
  });
  const summary = rename(root);
  assert.deepEqual(summary.file_renames, ["modules/e/protocol/Target.kh"]);
  assert.match(at(root, "modules/e/protocol/Target.kh"), /\ntp Target ab\n/);
});

test("a file whose name is the name in another spelling is reported too", () => {
  const root = corpus({
    "modules/e/protocol/Target.kh": TARGET,
    "modules/f/protocol/target.kh": RIVAL.replaceAll("Target", "Ftarget"),
  });
  assert.deepEqual(rename(root).file_renames, [
    "modules/e/protocol/Target.kh",
    "modules/f/protocol/target.kh",
  ]);
});

// The residue the port left behind

test("the residue is left by default, and is reported as residue rather than as prose", () => {
  const root = corpus({
    "modules/e/protocol/Target.kh": TARGET,
    "modules/e/protocol/detector.kh": DETECTOR,
  });
  const summary = rename(root, { write: true });
  assert.deepEqual(summary.residue_sites, []);
  assert.deepEqual(
    summary.unread
      .filter((entry) => entry.class === "go-residue")
      .map((entry) => `${entry.path}:${entry.line}`),
    ["modules/e/protocol/detector.kh:16"],
  );
  assert.match(
    at(root, "modules/e/protocol/detector.kh"),
    /type Detector interface \{\n {4}Target\n\}/,
  );
});

test("the residue mode rewrites a whole Go identifier inside the block and names its mode", () => {
  const root = corpus({
    "modules/e/protocol/Target.kh": TARGET,
    "modules/e/protocol/detector.kh": DETECTOR,
  });
  const summary = rename(root, { residue: true, write: true });
  assert.equal(summary.mode, "khayyam+go-residue");
  assert.deepEqual(
    summary.residue_sites.map((site) => `${site.path}:${site.line}:${site.role}`),
    ["modules/e/protocol/detector.kh:16:go-identifier"],
  );
  const detector = at(root, "modules/e/protocol/detector.kh");
  assert.match(detector, /type Detector interface \{\n {4}EventTarget\n\}/);
  assert.match(detector, /\ntp Detect mt \(self Detector\) \(t EventTarget\) \(\)/);
});

test("the residue mode reads past the characters Go spells that this scanner does not", () => {
  // The member stands behind a pointer type, so the scanner stops at the `*` and takes the
  // rest of the line with it. A mode that took the scanner's stream as it stands would
  // find no identifier on this line at all, which is why the block is read again from
  // where the scanner stopped.
  const root = corpus({
    "modules/e/protocol/Target.kh": TARGET,
    "modules/e/protocol/detector.kh": DETECTOR.replace(
      "type Detector interface {\n    Target\n}",
      "type Detector interface {\n    Target *Target\n}",
    ),
  });
  const summary = rename(root, { residue: true });
  assert.deepEqual(
    summary.residue_sites.map((site) => `${site.line}:${site.column}`),
    ["16:5", "16:13"],
  );
});

test("the residue mode leaves a Go comment and a Go string alone", () => {
  const root = corpus({
    "modules/e/protocol/Target.kh": TARGET,
    "modules/e/protocol/detector.kh": DETECTOR.replace(
      "type Detector interface {\n    Target\n}",
      "type Detector interface {\n    // Target stays spelled here.\n    Label() string { return \"Target\" }\n    Target\n}",
    ),
  });
  const summary = rename(root, { residue: true, write: true });
  assert.deepEqual(summary.residue_sites.map((site) => site.line), [18]);
  assert.match(
    at(root, "modules/e/protocol/detector.kh"),
    / {4}\/\/ Target stays spelled here\.\n {4}Label\(\) string \{ return "Target" \}\n {4}EventTarget\n\}/,
  );
});

test("a block sealed by its sha256 is left whole and reported", () => {
  const sealed = DETECTOR.replace(
    "// TODO(go-migrate):\n/*",
    "// TODO(go-migrate):\n// --- go-source: 0123\n/*",
  ).replace("*/\n", "*/\n// --- end go-source: 0123\n");
  const root = corpus({
    "modules/e/protocol/Target.kh": TARGET,
    "modules/e/protocol/detector.kh": sealed,
  });
  const summary = rename(root, { residue: true, write: true });
  assert.deepEqual(summary.residue_sites, []);
  assert.deepEqual(summary.residue_left, [
    "modules/e/protocol/detector.kh: line 12: sealed by its sha256, so it is left whole",
  ]);
});

// The real sources

test("a real declaration reaches every file of this repository that names it", () => {
  // The enumeration is what this rule is for, and a synthetic tree cannot show that it
  // reaches every consumer: only the sources can. `Timer` is renamed dry, so the check is
  // that every planned place holds the name and that the reach is wider than one file.
  const summary = rename(REPOSITORY, { name: "Timer", to: "EventTimer" });
  assert.equal(summary.declaration.path, "modules/time/timer/protocol/timer.kh");
  const paths = new Set(summary.sites.map((site) => site.path));
  assert.ok(paths.has("modules/time/timer/protocol/timer.kh"));
  assert.ok(paths.has("modules/time/timer/protocol/timing.kh"));
  assert.deepEqual(summary.file_renames, ["modules/time/timer/protocol/timer.kh"]);
  assert.equal(summary.mode, "khayyam");
  for (const site of summary.sites) {
    const line = at(REPOSITORY, site.path).split("\n")[site.line - 1]!;
    assert.equal(line.slice(site.column - 1, site.column - 1 + site.length), "Timer");
  }
});

test("the sources' residue mode finds only whole identifiers, and says what it could not read", () => {
  // The same rule over the real sources in its residue mode. What this pins is the shape of
  // the answer rather than a count, which is the sources' and not the rule's: every site
  // is a whole Go identifier, it stands on the name alone, and every block this mode could
  // not read is reported rather than guessed at.
  const summary = rename(REPOSITORY, { name: "Timer", to: "EventTimer", residue: true });
  assert.equal(summary.mode, "khayyam+go-residue");
  assert.deepEqual([...new Set(summary.residue_sites.map((site) => site.role))], ["go-identifier"]);
  assert.ok(
    summary.residue_sites.length > 0,
    "the sources' timer residue names `Timer`, so the mode must find it",
  );
  for (const site of summary.residue_sites) {
    const line = at(REPOSITORY, site.path).split("\n")[site.line - 1]!;
    assert.equal(line.slice(site.column - 1, site.column - 1 + site.length), "Timer");
    // A longer name is a longer name: a site stands on the whole token and never on part
    // of one, which is the whole of what stands between this and a text substitution.
    assert.match(line.slice(site.column - 1 + site.length, site.column + site.length), /[^\p{L}\p{Nd}_]/u);
  }
  assert.ok(
    summary.residue_left.some((entry) => entry.includes("does not lex")),
    "the sources hold residue this mode cannot read whole, and a run that hid that would be lying",
  );
});

// The invocation

test("the command reaches the sources with no root of its own, and names what it plans", () => {
  // The command carries the repository root and the toolchain's own exclusions; the mechanism
  // carries neither. Nothing in process could catch that root pointing one level off, because
  // a root that resolves to a folder with no units under it is an empty corpus and an empty
  // corpus refuses every name rather than planning the wrong one — so the wiring is stated here,
  // over the command as a reader runs it.
  const command = join(REPOSITORY, "bundles/khayyam/services/rename/rename.ts");
  const run = spawnSync(
    process.execPath,
    [command, "--name", "Timer", "--to", "EventTimer", "--samples", "0"],
    { cwd: join(REPOSITORY, "bundles/khayyam"), encoding: "utf8" },
  );
  assert.equal(run.status, 0, run.stderr);
  assert.match(
    run.stdout,
    /^declaration modules\/time\/timer\/protocol\/timer\.kh:\d+ tp-ab {2}Timer -> EventTimer$/m,
  );
  assert.match(run.stdout, /^mode khayyam {2}files [1-9]\d* /m);
});

test("the residue mode is reached by the flag the rule documents, and names its own label", () => {
  const command = join(REPOSITORY, "bundles/khayyam/services/rename/rename.ts");
  const run = spawnSync(
    process.execPath,
    [command, "--name", "Timer", "--to", "EventTimer", "--residue", "--samples", "0"],
    { cwd: join(REPOSITORY, "bundles/khayyam"), encoding: "utf8" },
  );
  assert.equal(run.status, 0, run.stderr);
  assert.match(run.stdout, /^mode khayyam\+go-residue {2}files [1-9]\d* /m);
});
