/* For license and copyright information please see the LEGAL file in the code repository */

import assert from "node:assert/strict";
import { mkdirSync, mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import test from "node:test";

import {
  type Binding,
  type Found,
  type Occurrence,
  type Outcome,
  type Request,
} from "../occurrences.ts";
import {
  printRename,
  renameDeclaration,
  RenameRefused,
  runRenameCommand,
  type Options,
  type Residue,
  type Summary,
} from "../declaration-rename.ts";

// The subject is the declaration-rename mechanism at `bundles/khayyam/services/rename/`: given the name
// of one declared type, it enumerates a corpus, turns the places a binding reports into a plan
// a reader can accept, and writes those places and no others — but only under an explicit
// `--write`, and only where the binding's own check still accepts the result.
//
// What an occurrence *is* is a binding's answer and is pinned by that binding's own tests,
// which know what a token is and what binds to what; nothing here knows what a token is. The
// binding below is a probe: it finds whole-word occurrences of the name on lines that carry
// `BIND`, reports what it cannot account for, and refuses a file whose text carries `BROKEN`.
// Every expectation here is therefore this mechanism's own behaviour over an answer it was
// handed. The other reader's pass is handed beside it, for the same reason: what a body of
// another language's source is, and what a run that includes it calls itself, are the target's
// facts and not this mechanism's.

// ── the probe binding ────────────────────────────────────────────────────────────

const PROBE: Binding = {
  language: "probe",

  find(request: Request): Found {
    const owners: Found["same_name"] = [];
    const taken: Found["taken"] = [];
    const carried: Found["carried"] = [];
    const longer: Found["longer_names"] = [];
    const fileRenames: string[] = [];
    /** Every whole-word occurrence of the name, with the line it stands on. */
    const found: { path: string; line: number; column: number; prose: boolean; carries: boolean }[] = [];
    for (const path of request.paths) {
      let source = "";
      try {
        source = readFileSync(join(request.root, path), "utf8");
      } catch {
        continue;
      }
      if (path.split("/").slice(-1)[0]!.replace(/\.unit$/, "") === request.name) {
        fileRenames.push(path);
      }
      source.split("\n").forEach((line, offset) => {
        const place = { path, line: offset + 1, form: "own", kind: request.name };
        if (line === `own ${request.name}`) owners.push(place);
        if (line === `own ${request.to}`) taken.push(place);
        if (line === `route ${request.name}`) carried.push({ ...place, form: "route" });
        if (line === `own ${request.name}_Longer`) {
          longer.push({ name: `${request.name}_Longer`, path, line: offset + 1 });
        }
        if (line === `own ${request.name}` || line === `route ${request.name}`) return;
        for (const match of line.matchAll(new RegExp(`\\b${request.name}\\b`, "g"))) {
          found.push({
            path,
            line: offset + 1,
            column: match.index + 1,
            prose: line.startsWith("#"),
            carries: line.includes("BIND"),
          });
        }
      });
    }

    let target: Found["target"] = null;
    const ambiguity: string[] = [];
    const wanted = request.declaration;
    if (wanted !== undefined) {
      const one = owners.find((place) => `${place.path}:${place.line}` === wanted);
      if (one === undefined) {
        ambiguity.push(`${wanted} is not a declaration of \`${request.name}\``);
      } else target = one;
    } else if (owners.length === 1) target = owners[0]!;
    else if (owners.length === 0) ambiguity.push(`no declaration is named \`${request.name}\``);
    else {
      ambiguity.push(
        `${owners.length} declarations are named \`${request.name}\`, so the name does not say which one this run is about: ` +
          owners.map((place) => `${place.path}:${place.line}`).join(", "),
      );
    }

    const sites: Found["sites"] = [];
    const leftAlone: Found["left_alone"] = [];
    const unread: Found["unread"] = [];
    for (const entry of found) {
      const at = {
        path: entry.path,
        line: entry.line,
        column: entry.column,
        length: request.name.length,
        role: "declaration",
      };
      // A declaration of something else is not a consumer of this name: where a second
      // declaration of it stands, everything that file plans is left and reported.
      const elsewhere = owners.some(
        (place) => place.path === entry.path && place !== target,
      );
      if (elsewhere) {
        leftAlone.push({ ...at, role: "declaration", why: "another declaration of the name stands in this file" });
      } else if (entry.carries) sites.push(at);
      else if (entry.prose) unread.push({ ...at, role: "unread", class: "prose", text: request.name });
      else leftAlone.push({ ...at, role: "unbound", why: "nothing binds the name here" });
    }
    return {
      name: request.name,
      same_name: owners,
      carried,
      taken,
      target,
      ambiguity,
      sites,
      left_alone: leftAlone,
      unread,
      longer_names: longer,
      file_renames: fileRenames,
      faults: [],
      missing: [],
    };
  },

  analyze(_path: string, source: string): Outcome {
    const at = source.split("\n").findIndex((line) => line.includes("BROKEN"));
    return at < 0
      ? { outcome: "accept" }
      : { outcome: "refuse", reason: "the probe refuses a file carrying BROKEN", line: at + 1 };
  },
};

/** The other reader's pass, as the target that owns it hands it over: it finds whole-word
 *  occurrences of the name on the other reader's own lines, and it says what a run that
 *  includes it is called. The mechanism is told neither what those lines are nor why. */
const PROBE_RESIDUE: Residue = {
  mode: "probe+other",
  find(text, name, path) {
    const sites: Occurrence[] = [];
    text.split("\n").forEach((line, offset) => {
      if (!line.startsWith("other ")) return;
      for (const match of line.matchAll(new RegExp(`\\b${name}\\b`, "g"))) {
        sites.push({
          path,
          line: offset + 1,
          column: match.index + 1,
          length: name.length,
          role: "other-identifier",
        });
      }
    });
    return { sites, left: [] };
  },
};

// ── the corpus ──────────────────────────────────────────────────────────────────

const DECLARING = `own Target
BIND Target
route Target
# Target is named in prose.
own Target_Longer
`;

const USING = `route Target
BIND Target
# Target again.
unbound Target
`;

function corpus(files: Record<string, string>): string {
  const root = mkdtempSync(join(tmpdir(), "identifier-rename-"));
  for (const [path, text] of Object.entries(files)) {
    mkdirSync(dirname(join(root, path)), { recursive: true });
    writeFileSync(join(root, path), text, "utf8");
  }
  return root;
}

function at(root: string, path: string): string {
  return readFileSync(join(root, path), "utf8");
}

function run(
  root: string,
  options: {
    name?: string;
    to?: string;
    declaration?: string;
    residue?: boolean;
    write?: boolean;
    binding?: Binding;
  } = {},
): Summary {
  return renameDeclaration(
    {
      root,
      unit: ".unit",
      name: options.name ?? "Target",
      to: options.to ?? "EventTarget",
      ...(options.declaration === undefined ? {} : { declaration: options.declaration }),
      ...(options.residue === true ? { residue: PROBE_RESIDUE } : {}),
      ...(options.write === undefined ? {} : { write: options.write }),
      values: ["modules"],
      excludes: [],
    },
    options.binding ?? PROBE,
  );
}

function refusal(fn: () => unknown): string {
  try {
    fn();
  } catch (error) {
    assert.ok(error instanceof RenameRefused, `refused with ${String(error)}`);
    return error.messages.join("\n");
  }
  assert.fail("the run planned something where it owes a refusal");
}

/** What one command answered: the exit code a caller reads its verdict from, and what it
 *  said while answering. The command reports a refusal on stderr rather than by throwing,
 *  so this is how a Test reads one. The binding is the one the caller hands over — there is
 *  one per process and nothing looks it up — and `residue` is the other reader's pass, where
 *  the run under a test was given one. */
function answered(
  argv: readonly string[],
  binding: Binding = PROBE,
  defaults: Partial<Options> = {},
  residue?: Residue,
): { code: number; said: string; printed: string } {
  const originalOut = process.stdout.write.bind(process.stdout);
  const originalError = process.stderr.write.bind(process.stderr);
  const collect =
    (into: { text: string }) =>
    (chunk: string | Uint8Array): boolean => {
      into.text += typeof chunk === "string" ? chunk : Buffer.from(chunk).toString("utf8");
      return true;
    };
  const said = { text: "" };
  const printed = { text: "" };
  process.stdout.write = collect(printed) as typeof process.stdout.write;
  process.stderr.write = collect(said) as typeof process.stderr.write;
  try {
    return { code: runRenameCommand(argv, binding, defaults, residue), said: said.text, printed: printed.text };
  } finally {
    process.stdout.write = originalOut;
    process.stderr.write = originalError;
  }
}

// ── the corpus the service chooses ──────────────────────────────────────────────

test("the run reads every unit under the paths it is given, in a fixed order", () => {
  const root = corpus({
    "modules/z/unit.unit": "route Target\nBIND Target\n",
    "modules/a/unit.unit": "own Target\nBIND Target\n",
    "modules/a/notes.md": "own Target\n",
  });
  const summary = run(root);
  assert.equal(summary.files, 2);
  assert.deepEqual(
    summary.sites.map((site) => site.path),
    ["modules/a/unit.unit", "modules/z/unit.unit"],
  );
});

test("a prefix the run is told to leave alone is not read", () => {
  const root = corpus({
    "modules/a/unit.unit": "own Target\nBIND Target\n",
    "modules/samples/unit.unit": "route Target\nBIND Target\n",
  });
  const summary = renameDeclaration(
    { root, unit: ".unit", name: "Target", to: "EventTarget", values: ["modules"], excludes: ["modules/samples/"] },
    PROBE,
  );
  assert.equal(summary.files, 1);
  assert.deepEqual(
    summary.sites.map((site) => site.path),
    ["modules/a/unit.unit"],
  );
});

// ── the plan ────────────────────────────────────────────────────────────────────

test("the plan is every place the binding reported, and the samples are its first places", () => {
  const root = corpus({
    "modules/a/declaring.unit": DECLARING,
    "modules/a/using.unit": USING,
  });
  const summary = run(root);
  assert.equal(summary.rule, "declaration-rename");
  assert.equal(summary.name, "Target");
  assert.equal(summary.to, "EventTarget");
  assert.equal(summary.occurrences, summary.sites.length);
  assert.deepEqual(
    summary.sites.map((site) => `${site.path}:${site.line}:${site.role}`),
    [
      "modules/a/declaring.unit:2:declaration",
      "modules/a/using.unit:2:declaration",
    ],
  );
  assert.deepEqual(summary.samples[0], {
    from: "Target",
    to: "EventTarget",
    path: "modules/a/declaring.unit",
    line: 2,
    column: 6,
    role: "declaration",
  });
});

test("the declaration is the place the binding named, and every route of it is reported", () => {
  const root = corpus({
    "modules/a/declaring.unit": DECLARING,
    "modules/a/using.unit": USING,
  });
  const summary = run(root);
  assert.deepEqual(summary.declaration, {
    path: "modules/a/declaring.unit",
    line: 1,
    form: "own",
  });
  assert.deepEqual(
    summary.same_name.map((place) => `${place.path}:${place.line}`),
    ["modules/a/declaring.unit:1"],
  );
  assert.deepEqual(
    summary.carried_by.map((place) => `${place.path}:${place.line}`),
    ["modules/a/declaring.unit:3", "modules/a/using.unit:1"],
  );
});

test("everything the binding found and did not plan is reported under a reason", () => {
  const root = corpus({
    "modules/a/declaring.unit": DECLARING,
    "modules/a/using.unit": USING,
  });
  const summary = run(root);
  assert.deepEqual(
    summary.left_alone.map((site) => `${site.path}:${site.line}:${site.role}:${site.why}`),
    ["modules/a/using.unit:4:unbound:nothing binds the name here"],
  );
  assert.deepEqual(
    summary.unread.map((entry) => `${entry.path}:${entry.line}:${entry.class}`),
    ["modules/a/declaring.unit:4:prose", "modules/a/using.unit:3:prose"],
  );
  assert.deepEqual(
    summary.longer_names.map((entry) => `${entry.name}@${entry.path}`),
    ["Target_Longer@modules/a/declaring.unit"],
  );
});

test("a file named after the declaration is reported and never renamed", () => {
  const root = corpus({
    "modules/a/Target.unit": "own Target\nBIND Target\n",
  });
  const summary = run(root);
  assert.deepEqual(summary.file_renames, ["modules/a/Target.unit"]);
  assert.match(at(root, "modules/a/Target.unit"), /^own Target\n/);
});

test("the printed plan names the mode, the count, and the files with their occurrences", () => {
  const root = corpus({
    "modules/a/declaring.unit": DECLARING,
    "modules/a/using.unit": USING,
  });
  const printed = printRename(run(root), 1);
  assert.match(printed[0]!, /^declaration modules\/a\/declaring\.unit:1 own {2}Target -> EventTarget$/);
  assert.match(printed[1]!, /^mode probe {2}files 2 {2}changed 2 {2}occurrences 2 {2}residue 0 {2}dry$/);
  assert.match(printed[2]!, /^ {2}modules\/a\/declaring\.unit:2:6 Target -> EventTarget \(declaration\)$/);
  assert.deepEqual(
    printed.filter((line) => /occurrence\(s\)$/.test(line)),
    ["  modules/a/declaring.unit  1 occurrence(s)", "  modules/a/using.unit  1 occurrence(s)"],
    "the plan shows the occurrences it was asked for, and the report carries them all",
  );
});

// ── dry by default ──────────────────────────────────────────────────────────────

test("a run writes nothing unless it is asked to, and the write changes only planned places", () => {
  const root = corpus({
    "modules/a/declaring.unit": DECLARING,
    "modules/a/using.unit": USING,
  });
  assert.equal(run(root).written, false);
  assert.match(at(root, "modules/a/declaring.unit"), /^BIND Target\n/m);

  const written = run(root, { write: true });
  assert.equal(written.written, true);
  const declaring = at(root, "modules/a/declaring.unit");
  assert.match(declaring, /^BIND EventTarget\n/m);
  assert.match(declaring, /^# Target is named in prose\.\n/m);
  assert.match(declaring, /^own Target_Longer\n/m);
  assert.deepEqual(written.files_changed, ["modules/a/declaring.unit", "modules/a/using.unit"]);
});

test("a place that does not hold the name refuses the write rather than guessing at it", () => {
  // The plan is built from one reading of the corpus and applied to another, so a site
  // standing where the name no longer stands is a disagreement between the two — here a
  // place reported twice, which the second application finds already rewritten.
  const root = corpus({
    "modules/a/one.unit": "own Target\nBIND Target\n",
    "modules/a/two.unit": "own Target\nBIND Target\n",
  });
  const stale: Binding = {
    ...PROBE,
    find: (request) => {
      const found = PROBE.find(request);
      return {
        ...found,
        sites: [...found.sites, { ...found.sites[0]! }],
      };
    },
  };
  assert.match(
    refusal(() => run(root, { declaration: "modules/a/one.unit:1", write: true, binding: stale })),
    /modules\/a\/one\.unit:2:6 holds "EventT", not "Target"/,
  );
  assert.match(at(root, "modules/a/one.unit"), /^BIND Target\n/m);
});

// ── the refusals before any plan ────────────────────────────────────────────────

test("a run given no name to rename, or the same name twice, is refused", () => {
  const root = corpus({ "modules/a/unit.unit": "own Target\nBIND Target\n" });
  assert.match(refusal(() => run(root, { name: "" })), /the name to rename and the name it becomes/);
  assert.match(refusal(() => run(root, { to: "Target" })), /nothing to rename/);
});

test("a name nothing declares is refused", () => {
  const root = corpus({ "modules/a/unit.unit": "own Target\nBIND Target\n" });
  assert.match(refusal(() => run(root, { name: "Nothing" })), /Nothing/);
});

test("a name the sources already declare is refused, and where it is taken is said", () => {
  const root = corpus({
    "modules/a/unit.unit": "own Target\nBIND Target\nown EventTarget\n",
  });
  const messages = refusal(() => run(root));
  assert.match(messages, /EventTarget/);
  assert.match(messages, /modules\/a\/unit\.unit:3/);
});

test("two declarations of the name are both reported and neither is planned", () => {
  const root = corpus({
    "modules/a/one.unit": "own Target\nBIND Target\n",
    "modules/a/two.unit": "own Target\nBIND Target\n",
  });
  const messages = refusal(() => run(root));
  assert.match(messages, /modules\/a\/one\.unit:1/);
  assert.match(messages, /modules\/a\/two\.unit:1/);
});

test("a --declaration picks one of two, and the other is left alone and reported", () => {
  const root = corpus({
    "modules/a/one.unit": "own Target\nBIND Target\n",
    "modules/a/two.unit": "own Target\nBIND Target\n",
  });
  const summary = run(root, { declaration: "modules/a/one.unit:1", write: true });
  assert.deepEqual(summary.declaration, { path: "modules/a/one.unit", line: 1, form: "own" });
  assert.match(at(root, "modules/a/one.unit"), /^BIND EventTarget\n/m);
  assert.match(at(root, "modules/a/two.unit"), /^BIND Target\n/m);
});

test("a --declaration that names no declaration of the name is refused", () => {
  const root = corpus({ "modules/a/unit.unit": "own Target\nBIND Target\n" });
  assert.match(
    refusal(() => run(root, { declaration: "modules/a/unit.unit:99" })),
    /modules\/a\/unit\.unit:99/,
  );
});

test("a path the run was given that cannot be read is refused rather than skipped", () => {
  const root = corpus({ "modules/a/unit.unit": "own Target\nBIND Target\n" });
  const missing: Binding = {
    ...PROBE,
    find: (request) => ({ ...PROBE.find(request), missing: ["modules/gone.unit"] }),
  };
  assert.match(refusal(() => run(root, { binding: missing })), /modules\/gone\.unit is in the paths/);
});

// ── the gate ────────────────────────────────────────────────────────────────────

test("a write the binding's check would newly refuse is not written, and nothing else is either", () => {
  const root = corpus({
    "modules/a/unit.unit": "own Target\nBIND Target\n",
  });
  const summary = run(root, { to: "BROKEN", write: true });
  assert.equal(summary.written, false);
  assert.deepEqual(Object.keys(summary.gate?.newly_refused ?? {}), ["modules/a/unit.unit"]);
  assert.match(at(root, "modules/a/unit.unit"), /^BIND Target\n/m);
});

test("a write the check accepts is written, and the gate is measured on the plan", () => {
  const root = corpus({
    "modules/a/unit.unit": "own Target\nBIND Target\n",
  });
  const summary = run(root, { write: true });
  assert.deepEqual(summary.gate?.newly_refused, {});
  // The gate is asked of the text the plan produces rather than of what is on disk, so a
  // refused plan is refused while nothing has been written; the plan is what the two
  // accept/refuse counts are about.
  assert.equal(summary.gate?.before.refuse, 0);
  assert.equal(summary.gate?.after.accept, summary.files);
});

test("a file already refused stays refused, and that is not a reason to refuse the write", () => {
  const root = corpus({
    "modules/a/unit.unit": "own Target\nBIND Target\n",
    "modules/b/broken.unit": "BROKEN but unrelated\n",
  });
  const summary = run(root, { write: true });
  assert.equal(summary.written, true);
  assert.equal(summary.gate?.before.refuse, 1);
  assert.deepEqual(summary.gate?.newly_refused, {});
});

test("the gate reads the rest of the corpus, so it sees the plan and not only the disk", () => {
  const root = corpus({
    "modules/a/unit.unit": "own Target\nBIND Target\n",
    "modules/b/other.unit": "nothing here\n",
  });
  const asked: string[] = [];
  let passes = 0;
  const watching: Binding = {
    ...PROBE,
    analyze: (path, source, read) => {
      // The first pass is asked of the disk and the second of the plan, and each walks the
      // whole corpus — which is what a resolution that reaches across files needs.
      if (asked.length === 0 || asked.length === 2) passes += 1;
      asked.push(path);
      assert.equal(read("modules/b/other.unit"), "nothing here\n");
      return PROBE.analyze(path, source, read);
    },
  };
  run(root, { binding: watching });
  assert.deepEqual([...new Set(asked)], ["modules/a/unit.unit", "modules/b/other.unit"]);
  assert.equal(asked.length, 4, "the gate is asked of the disk and then of the plan");
  assert.equal(passes, 2);
});

// ── the other reader's pass ──────────────────────────────────────────────────────

test("a run leaves the other reader alone unless it was asked for the pass", () => {
  const root = corpus({
    "modules/a/unit.unit": "own Target\nbegin other\nother Target\n",
  });
  const summary = run(root, { write: true });
  assert.equal(summary.mode, "probe");
  assert.deepEqual(summary.residue_sites, []);
  assert.match(at(root, "modules/a/unit.unit"), /begin other\nother Target\n/);
});

test("the residue mode rewrites a whole identifier of that spelling and reports the label it was handed", () => {
  const root = corpus({
    "modules/a/unit.unit": "own Target\nbegin other\nother Target\nother Target\n",
  });
  const summary = run(root, { residue: true, write: true });
  assert.equal(summary.mode, "probe+other");
  assert.deepEqual(
    summary.residue_sites.map((site) => `${site.line}:${site.role}`),
    ["3:other-identifier", "4:other-identifier"],
  );
  assert.match(at(root, "modules/a/unit.unit"), /begin other\nother EventTarget\nother EventTarget\n/);
});

test("the class of an entry the reader did not bind is reported as the reader classified it", () => {
  // Which text is this language's prose and which is another's source is the reader's own
  // fact, so the mechanism reports the `class` as it stands rather than rewriting it: a
  // class this file composed would be one it could not account for.
  const root = corpus({
    "modules/a/unit.unit": "own Target\nbegin other\n# Target in prose\nother nothing\n",
  });
  assert.deepEqual(
    run(root).unread.map((entry) => entry.class),
    ["prose"],
  );
});

// ── the command ─────────────────────────────────────────────────────────────────

test("the command is run in the binding it was handed, and names no language of its own", () => {
  const root = corpus({ "modules/a/unit.unit": "own Target\nBIND Target\n" });
  const named = answered(
    ["--root", root, "--name", "Target", "--to", "EventTarget", "modules"],
    { ...PROBE, language: "handed-probe" },
    { unit: ".unit" },
  );
  assert.equal(named.code, 0);
  assert.match(named.printed, /^mode handed-probe {2}files 1 /m);
  // A language on the command line is an argument this rule does not take, since the process
  // holds one binding and does not choose between them.
  const refused = answered(
    ["--root", root, "--name", "Target", "--to", "EventTarget", "--language", "absent-probe"],
    PROBE,
    { unit: ".unit" },
  );
  assert.equal(refused.code, 2);
  assert.match(refused.said, /--language is not an argument this rule takes/);
});

test("--residue asked of a process handed no reader is refused rather than run without one", () => {
  const root = corpus({ "modules/a/unit.unit": "own Target\nBIND Target\n" });
  const asked = answered(
    ["--root", root, "--name", "Target", "--to", "EventTarget", "--residue", "modules"],
    PROBE,
    { unit: ".unit" },
  );
  assert.equal(asked.code, 2);
  assert.match(asked.said, /--residue was asked for and this process was handed no reader to ask/);
});

test("the command writes its JSON report and answers its exit codes", () => {
  const root = corpus({
    "modules/a/unit.unit": "own Target\nBIND Target\n",
  });
  const report = join(root, "plan.json");
  const command = { ...PROBE, language: "command-probe" };
  const dry = answered(
    [
      "--root", root, "--name", "Target", "--to", "EventTarget",
      "--report", report, "modules",
    ],
    command,
    { unit: ".unit" },
  );
  assert.equal(dry.code, 0);
  assert.match(dry.printed, /^declaration modules\/a\/unit\.unit:1 own {2}Target -> EventTarget$/m);
  const written = JSON.parse(readFileSync(report, "utf8")) as Summary;
  assert.equal(written.mode, "command-probe");
  assert.equal(written.occurrences, 1);
  assert.equal(written.written, false);

  const refused = answered(
    ["--root", root, "--name", "Target", "--to", "Target"],
    command,
    { unit: ".unit" },
  );
  assert.equal(refused.code, 2, "a run that refused is not a success");
  assert.match(refused.said, /nothing to rename/);

  // A gate that refuses everything refuses before the plan as well, which is not a
  // refusal of the write; the probe's own gate is what turns the planned text into one.
  const gated = answered(
    ["--root", root, "--name", "Target", "--to", "BROKEN", "--write", "modules"],
    command,
    { unit: ".unit" },
  );
  assert.equal(gated.code, 1, "a write that was asked for and refused is not a success");
  assert.match(gated.printed, /newly refused modules\/a\/unit\.unit/);
  assert.match(at(root, "modules/a/unit.unit"), /^BIND Target\n/m);
});
