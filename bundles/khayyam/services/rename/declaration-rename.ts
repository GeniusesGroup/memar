// The declaration-rename mechanism: given the name of one declared type, the places a
// binding reports become a plan a reader can accept, a JSON report, and — only under an
// explicit `--write` — a change to the sources.
//
// The rule this file realizes is `bundles/khayyam/rules/declaration-rename/declaration-rename.md`,
// and it is this rule's own mechanism, beside the binding that answers for Khayyam
// ([`khayyam-binding.ts`](./khayyam-binding.ts)). Everything here is the enumeration of a
// corpus, a plan, a report, a write, a gate and a command, and every question of the form
// "does this place bind the name" is asked of the `Binding` the caller handed this run
// ([`occurrences.ts`](./occurrences.ts)). There is one binding and the caller says which,
// so this file neither looks one up nor has a run without one to ask.
//
// Three of the rule's properties are this file's whole reason to exist, and each is a
// refusal rather than a warning: nothing is written without `--write`; a plan is printed
// before anything is written, per file, with sample old→new pairs; and a write that would
// leave any file newly refused by the binding's own check is refused and nothing is written
// at all. That gate is asked in process, over the same file system the binding resolves
// against, because a write checked by a second process that could hold a different view of
// the sources are not a check. The name the run is given must also be free: a `--to` the
// sources already declare is refused before any plan, and two declarations carrying one
// name are both reported and neither is planned.
//
// There is one other mode, named in every run's output and never stamped into the source:
// `--residue`, which also rewrites the name inside a body of source another language left in
// a file of this one. What that body is, how its identifiers are read, and what a run
// including it calls itself are facts of the port that left it and not of this mechanism:
// the caller hands the pass itself as a `Residue` (see `runRenameCommand` below) and this
// file applies it and reports it, so the label under which the run is reported is one the
// mechanism is handed rather than one it composes out of two languages it does not hold.

import { readdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { join, relative, resolve } from "node:path";

import {
  type Binding,
  type Occurrence,
  type Reader,
} from "./occurrences.ts";

/** A place a rewrite stands at. The two passes' places are of this shape, which is why one
 *  function applies both: what is written where is not the reader's business. */
interface Writable {
  path: string;
  line: number;
  column: number;
  length: number;
}

/** A pass over a body of source a language other than this run's left in a file of its own
 *  — the Go clue block of a ported file is one — asked for by name rather than reached
 *  through the binding, because which language left the text is the target's own fact and
 *  this mechanism holds no reader for it. */
export interface Residue {
  /** What a run that includes this pass calls itself, both languages' names in the target's
   *  own hand (`khayyam+go-residue`): the mechanism composes no label out of languages it
   *  does not hold, so a run with a pass reports under whatever its pass says it is. */
  readonly mode: string;
  /** The places `name` stands inside `text`, and what the pass could not account for there.
   *  Both are reported; neither is guessed at. */
  find(text: string, name: string, path: string): { sites: Occurrence[]; left: string[] };
}

/** Every reason one run has to refuse, in the order it found them and without repeats, so
 *  one run reports all of them. */
export class RenameRefused extends Error {
  readonly messages: string[];

  constructor(messages: readonly string[]) {
    super([...new Set(messages)].join("\n"));
    this.messages = [...new Set(messages)];
  }
}

export interface Options {
  /** The repository the sources stand in. */
  root: string;
  /** What one unit of this corpus's source is called: the file-name suffix a run reads
   *  under. It is the corpus's own word and not this service's, which is why it is asked
   *  for rather than fixed here. */
  unit: string;
  /** Repository-relative files or directories to read; `modules` when none is given. */
  values?: readonly string[];
  /** Repository-relative prefixes to leave alone. A corpus choice rather than a rule:
   *  nothing here decides which of a caller's own sources are samples. */
  excludes?: readonly string[];
  name: string;
  to: string;
  /** `PATH:LINE` of the declaration, when the sources declare the name more than once. */
  declaration?: string;
  /** Whether the run also asks another reader about a body of source left in these files.
   *  The pass is the caller's, and `--residue` asks for it by name rather than naming one:
   *  see `runRenameCommand` below for where the two meet. */
  residue?: Residue;
  write?: boolean;
  samples?: number;
}

export interface Summary {
  rule: "declaration-rename";
  /** What the run calls itself: the binding's own name, or the label the residue pass was
   *  handed when one was included. */
  mode: string;
  name: string;
  to: string;
  files: number;
  declaration: { path: string; line: number; form: string };
  same_name: { path: string; line: number; form: string; kind: string }[];
  carried_by: { path: string; line: number; form: string; kind: string }[];
  occurrences: number;
  files_changed: string[];
  sites: Occurrence[];
  left_alone: Occurrence[];
  unread: (Occurrence & { class: string; text: string })[];
  longer_names: { name: string; path: string; line: number }[];
  /** What the residue pass found and could not account for, empty unless one ran: the report
   *  names both, because a pass that read something and left it is still a thing the reader
   *  of this report is owed. */
  residue_sites: Occurrence[];
  residue_left: string[];
  file_renames: string[];
  faults: { path: string; reason: string; line: number }[];
  samples: { from: string; to: string; path: string; line: number; column: number; role: string }[];
  written: boolean;
  gate?: {
    before: { accept: number; refuse: number };
    after: { accept: number; refuse: number };
    newly_refused: Record<string, { outcome: string; reason?: string; line?: number }>;
  };
}

/** The repository-relative units a run reads: under each of its `values`, every unit
 *  beneath it, minus the prefixes it leaves alone. The order is the order the units are read
 *  and their occurrences reported in, so it is fixed rather than whatever a directory walk
 *  happens to give. */
function collectUnits(
  root: string,
  unit: string,
  values: readonly string[],
  excludes: readonly string[],
): string[] {
  const found = new Set<string>();
  for (const value of values.length === 0 ? ["modules"] : values) {
    const path = resolve(root, value);
    for (const candidate of unitsUnder(path, unit)) {
      const relativePath = relative(root, candidate).replaceAll("\\", "/");
      if (excludes.some((prefix) => relativePath.startsWith(prefix))) continue;
      found.add(relativePath);
    }
  }
  return [...found].sort();
}

function unitsUnder(path: string, unit: string): string[] {
  let stats;
  try {
    stats = statSync(path);
  } catch {
    return [];
  }
  if (stats.isFile()) return [path];
  if (!stats.isDirectory()) return [];
  const found: string[] = [];
  for (const entry of readdirSync(path, { withFileTypes: true })) {
    const child = join(path, entry.name);
    if (entry.isDirectory()) found.push(...unitsUnder(child, unit));
    else if (entry.name.endsWith(unit)) found.push(child);
  }
  return found.sort();
}

function lineOffsets(text: string): number[] {
  const offsets = [0];
  for (let index = 0; index < text.length; index += 1) {
    if (text[index] === "\n") offsets.push(index + 1);
  }
  return offsets;
}

/** The one-based line `at` stands on in a text whose lines begin at `offsets`. */
function lineOf(offsets: number[], at: number): number {
  let low = 0;
  let high = offsets.length - 1;
  while (low < high) {
    const middle = (low + high + 1) >> 1;
    if (offsets[middle]! <= at) low = middle;
    else high = middle - 1;
  }
  return low + 1;
}

/** `text` with each site replaced by `to`, last site first so the offsets before it still
 *  stand. Every site is checked against the text before it is used: a site whose place does
 *  not hold the name is a disagreement between this module and the binding, and a rename
 *  that guesses is worse than no rename. */
function applySites(text: string, sites: readonly Writable[], name: string, to: string): string {
  const offsets = lineOffsets(text);
  const ordered = [...sites].sort((left, right) =>
    left.line === right.line ? right.column - left.column : right.line - left.line,
  );
  let rewritten = text;
  for (const site of ordered) {
    const at = offsets[site.line - 1]! + site.column - 1;
    if (rewritten.slice(at, at + site.length) !== name) {
      throw new RenameRefused([
        `${site.path}:${site.line}:${site.column} holds ${JSON.stringify(rewritten.slice(at, at + site.length))}, not ${JSON.stringify(name)}`,
      ]);
    }
    rewritten = rewritten.slice(0, at) + to + rewritten.slice(at + site.length);
  }
  return rewritten;
}

/** The binding's own check on each path, with `overrides` standing in for files that are
 *  not written yet — so a plan is checked before it is written, which is the only order in
 *  which the check is worth anything. */
function gateOutcomes(
  binding: Binding,
  root: string,
  paths: readonly string[],
  overrides: Record<string, string>,
): Record<string, { outcome: string; reason?: string; line?: number }> {
  const read: Reader = (path) => {
    if (Object.hasOwn(overrides, path)) return overrides[path];
    try {
      return readFileSync(join(root, path), "utf8");
    } catch {
      return undefined;
    }
  };
  const outcomes: Record<string, { outcome: string; reason?: string; line?: number }> = {};
  for (const path of paths) {
    const source = read(path);
    if (source === undefined) {
      outcomes[path] = { outcome: "missing" };
      continue;
    }
    const result = binding.analyze(path, source, read);
    outcomes[path] =
      result.outcome === "accept"
        ? { outcome: "accept" }
        : { outcome: "refuse", reason: result.reason, line: result.line };
  }
  return outcomes;
}

export function renameDeclaration(options: Options, binding: Binding): Summary {
  const root = resolve(options.root);
  const { name, to } = options;
  if (name === "" || to === "") {
    throw new RenameRefused(["declaration-rename is given the name to rename and the name it becomes"]);
  }
  if (name === to) {
    throw new RenameRefused([`\`${name}\` and \`${to}\` are the same spelling; there is nothing to rename`]);
  }
  const paths = collectUnits(root, options.unit, options.values ?? [], options.excludes ?? []);
  const report = binding.find({ root, paths, name, to, declaration: options.declaration });
  if (report.ambiguity.length > 0) throw new RenameRefused(report.ambiguity);
  if (report.missing.length > 0) {
    throw new RenameRefused(
      report.missing.map((path) => `${path} is in the paths this run was given and could not be read`),
    );
  }
  if (report.taken.length > 0) {
    throw new RenameRefused([
      `\`${to}\` is already declared, so the rename would collide with it: ` +
        report.taken.map((place) => `${place.path}:${place.line}`).join(", "),
    ]);
  }

  const target = report.target;
  if (target === null) {
    // The binding answers a body of source that declares the name nowhere with a refusal of
    // its own, so this is the two disagreeing rather than a case of its own; either way a
    // run that picked a declaration would be guessing.
    throw new RenameRefused([`no declaration in the sources is named \`${name}\``]);
  }

  const originals = new Map<string, string>();
  for (const relativePath of paths) {
    originals.set(relativePath, readFileSync(join(root, relativePath), "utf8"));
  }

  const sitesByFile = new Map<string, Occurrence[]>();
  for (const site of report.sites) {
    const standing = sitesByFile.get(site.path);
    if (standing === undefined) sitesByFile.set(site.path, [site]);
    else standing.push(site);
  }

  const residue = options.residue;
  const changed = new Map<string, string>();
  const residueReported: Occurrence[] = [];
  const residueLeft: string[] = [];
  for (const [relativePath, original] of originals) {
    const text = original.replaceAll("\r\n", "\n");
    const wanted = sitesByFile.get(relativePath) ?? [];
    if (wanted.length === 0 && residue === undefined) continue;
    let renamed = applySites(text, wanted, name, to);
    if (residue !== undefined) {
      // The residue pass reads the text the first pass produced, and its sites are
      // applied to that same text, so a file carrying both kinds of site is rewritten once
      // against one text rather than two.
      const found = residue.find(renamed, name, relativePath);
      residueReported.push(...found.sites);
      residueLeft.push(...found.left.map((entry) => `${relativePath}: ${entry}`));
      renamed = applySites(renamed, found.sites, name, to);
    }
    if (renamed !== text) {
      const newline = original.includes("\r\n") ? "\r\n" : "\n";
      changed.set(relativePath, renamed.replaceAll("\n", newline));
    }
  }

  const every = [...originals.keys()].sort();
  const before = gateOutcomes(binding, root, every, {});
  const after = gateOutcomes(binding, root, every, Object.fromEntries(changed));
  const refusedBefore = new Set(every.filter((path) => before[path]?.outcome === "refuse"));
  const refusedAfter = new Set(every.filter((path) => after[path]?.outcome === "refuse"));
  const newlyRefused = [...refusedAfter]
    .filter((path) => !refusedBefore.has(path))
    .sort()
    .map((path) => [path, after[path]!] as const);

  const summary: Summary = {
    rule: "declaration-rename",
    mode: residue === undefined ? binding.language : residue.mode,
    name,
    to,
    files: originals.size,
    declaration: {
      path: target.path,
      line: target.line,
      form: target.form,
    },
    same_name: report.same_name,
    carried_by: report.carried,
    occurrences: report.sites.length,
    files_changed: [...changed.keys()].sort(),
    sites: report.sites,
    left_alone: report.left_alone,
    unread: report.unread,
    longer_names: report.longer_names,
    residue_sites: residueReported,
    residue_left: residueLeft,
file_renames: report.file_renames,
faults: report.faults,
    samples: report.sites.slice(0, options.samples ?? report.sites.length).map((site) => ({
      from: name,
      to,
      path: site.path,
      line: site.line,
      column: site.column,
      role: site.role,
    })),
    written: false,
    gate: {
      before: { accept: every.length - refusedBefore.size, refuse: refusedBefore.size },
      after: { accept: every.length - refusedAfter.size, refuse: refusedAfter.size },
      newly_refused: Object.fromEntries(newlyRefused),
    },
  };

  if (newlyRefused.length > 0) return summary;
  if (options.write === true) {
    for (const [relativePath, text] of changed) {
      writeFileSync(join(root, relativePath), text, "utf8");
    }
    summary.written = true;
  }
  return summary;
}

/** The dry run's report: what the declaration is, what it becomes, every place that
 *  changes, and everything that was found and left. */
export function printRename(summary: Summary, samples: number): string[] {
  const declaration = summary.declaration;
  const lines = [
    `declaration ${declaration.path}:${declaration.line} ${declaration.form}  ${summary.name} -> ${summary.to}`,
    `mode ${summary.mode}  files ${summary.files}  changed ${summary.files_changed.length}  occurrences ${summary.occurrences}  residue ${summary.residue_sites.length}  ${summary.written ? "written" : "dry"}`,
  ];
  for (const sample of summary.samples.slice(0, samples)) {
    lines.push(`  ${sample.path}:${sample.line}:${sample.column} ${sample.from} -> ${sample.to} (${sample.role})`);
  }
  if (summary.files_changed.length > 0) {
    lines.push("files changed:");
    for (const path of summary.files_changed) {
      const count = summary.sites.filter((site) => site.path === path).length;
      lines.push(`  ${path}  ${count} occurrence(s)`);
    }
  }
  for (const site of summary.left_alone) {
    lines.push(`left alone ${site.path}:${site.line}:${site.column} (${site.role})${site.why === undefined ? "" : `: ${site.why}`}`);
  }
  if (summary.unread.length > 0) {
    lines.push("found in text the reader does not bind:");
    for (const entry of summary.unread) {
      lines.push(`  ${entry.path}:${entry.line}:${entry.column} ${entry.class} ${entry.text}`);
    }
  }
  if (summary.longer_names.length > 0) {
    lines.push("declarations whose name carries this name:");
    for (const entry of summary.longer_names) {
      lines.push(`  ${entry.path}:${entry.line} ${entry.name}`);
    }
  }
  for (const entry of summary.residue_left) lines.push(`residue left: ${entry}`);
  for (const path of summary.file_renames) {
    lines.push(`file named after the declaration, reported and never renamed: ${path}`);
  }
  if (summary.gate !== undefined) {
    lines.push(
      `check accept/refuse before ${summary.gate.before.accept}/${summary.gate.before.refuse}  after ${summary.gate.after.accept}/${summary.gate.after.refuse}`,
    );
    for (const [path, outcome] of Object.entries(summary.gate.newly_refused)) {
      lines.push(`  newly refused ${path}: ${outcome.reason} at line ${outcome.line}`);
    }
  }
  return lines;
}

interface Invocation {
  options: Partial<Options>;
  /** Occurrences to print; the report itself carries them all. */
  samples: number;
  report?: string;
  /** Whether the run asked for another reader's pass. What that pass *is* is the caller's,
   *  so this is the request and not the answer: the caller resolves it against the one it
   *  handed over, and a run that asked with nothing to ask is refused below. */
  residue?: boolean;
}

/** What one command line asked for: the options the run takes, how many occurrences to
 *  print, where the JSON report goes when one was asked for, and whether the other reader
 *  was asked for. Which binding answers is not here, because a command line does not choose
 *  one: the process has exactly one and the caller handed it over. An option the command
 *  line did not carry is left undefined rather than defaulted here, so that a caller's
 *  defaults and this file's own reach the run in the right order. */
function parse(argv: readonly string[]): Invocation {
  const options: Partial<Options> = {};
  const values: string[] = [];
  const excludes: string[] = [];
  let samples = 10;
  let report: string | undefined;
  let residue: boolean | undefined;
  for (let index = 0; index < argv.length; index += 1) {
    const value = argv[index + 1];
    switch (argv[index]) {
      case "--write":
        options.write = true;
        continue;
      case "--residue":
        residue = true;
        continue;
      case "--root":
        options.root = value!;
        break;
      case "--name":
        options.name = value!;
        break;
      case "--to":
        options.to = value!;
        break;
      case "--declaration":
        options.declaration = value!;
        break;
      case "--exclude":
        excludes.push(value!);
        break;
      case "--samples":
        samples = Number(value);
        break;
      case "--report":
        report = value;
        break;
      default:
        if (argv[index]!.startsWith("--")) {
          throw new RenameRefused([`${argv[index]} is not an argument this rule takes`]);
        }
        values.push(argv[index]!);
        continue;
    }
    index += 1;
  }
  return {
    options: {
      ...options,
      ...(values.length === 0 ? {} : { values }),
      ...(excludes.length === 0 ? {} : { excludes }),
    },
    samples,
    ...(report === undefined ? {} : { report }),
    ...(residue === undefined ? {} : { residue }),
  };
}

// What this service reaches on its own when nothing else is said: the working directory,
// and every file in it as one corpus of plain text rather than of units.
const REACHED = { root: process.cwd(), unit: "", name: "", to: "" } satisfies Options;

/** The command: parse argv, run in the binding the caller handed over, print the plan,
 *  write the JSON report where one was asked for, and answer an exit code. `defaults` is
 *  what the caller supplies about its own corpus — what a unit of it is called and which of
 *  its sources a run leaves alone are the caller's facts and not this service's. `residue`
 *  is the other reader's pass, where the caller's language has one and `--residue` asks for
 *  it. */
export function runRenameCommand(
  argv: readonly string[],
  binding: Binding,
  defaults: Partial<Options> = {},
  residue?: Residue,
): number {
  try {
    const invocation = parse(argv);
    const asked = invocation.residue === true;
    // A run that asked for the other reader and was handed none is refused rather than run
    // without it: the two modes report under different names, and a `--residue` that quietly
    // found nothing would be a mode no reader of the report could tell from the default one.
    if (asked && residue === undefined) {
      throw new RenameRefused([
        "--residue was asked for and this process was handed no reader to ask",
      ]);
    }
    // The reach this service reaches on its own, then the caller's corpus, then whatever
    // the command line carried: a default the caller supplied beats this file's and loses to
    // an argument, and an argument that was not given leaves the default standing.
    const options: Options = {
      ...REACHED,
      ...defaults,
      ...invocation.options,
      ...(asked ? { residue } : {}),
    };
    const summary = renameDeclaration(options, binding);
    if (invocation.report !== undefined) {
      writeFileSync(invocation.report, JSON.stringify(summary, null, 2), "utf8");
    }
    process.stdout.write(`${printRename(summary, invocation.samples).join("\n")}\n`);
    // A write that was asked for and refused is not a success, and a caller reading only
    // the exit code must not hear one.
    return options.write === true && !summary.written ? 1 : 0;
  } catch (error) {
    if (!(error instanceof RenameRefused)) throw error;
    for (const message of error.messages) process.stderr.write(`error: ${message}\n`);
    return 2;
  }
}
