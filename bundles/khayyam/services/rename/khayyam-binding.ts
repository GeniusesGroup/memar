// Every place in a repository where the name of one declared type is written as that
// declaration's own name. This is the **Khayyam half** of the declaration-rename rule, asked
// in process by [`declaration-rename.ts`](./declaration-rename.ts) beside it, which is where
// the places reported here become a plan, a report, and a write. It reads `core/` and nothing
// else, which is what keeps it beside the rule's mechanism instead of inside the target the
// port writes.
//
// What lives here and not in the service is Khayyam's: `scan` says what a token is - so
// a `//` comment, a `/* */` block, and a string literal are not tokens, and an identifier
// is a whole token rather than a run of characters (`docs/khayyam/khayyam.md`,
// Identifiers) - `readUnit` says what a unit declares, `referencePlaces`
// (`core/src/references.ts`) says where inside a declaration each name it references
// stands, and `visibleNames` (`core/src/frontend.ts`) says which names a file sees. The
// service owns the corpus, the plan, the report, the write and the gate, and it owns none
// of that — it asks this file through the `Binding` it was handed and takes the places as
// they stand. What decides an occurrence is therefore the language's own machinery and
// nothing else. This module supplies the role a place is reported under and the cross-file
// binding, and a site is planned for a rewrite only where those places say the declaration
// references the name and the file's own declarations say the name arrives from the file
// the declaration stands in. Everything else is reported under a name saying what it is,
// because "not rewritten" is only useful next to "why not".
//
// The two parts of this file that are not the occurrence finder are the gate and the
// residue, and both are here for the same reason: each asks Khayyam's own machinery a
// question the service cannot answer alone. `analyze` is what says whether a plan still
// means anything, and the end-of-file Go clue block of a ported file is Go text read with
// Khayyam's lexics, which is why the residue is handed to the service as a `Residue` beside
// this binding rather than asked through it: the port left that text, so the port's reader
// for it belongs to this side of the seam and not to the shared contract.
//
// A request is {"root": repository root, "paths": [repository-relative .kh], "name": "X",
// "to": "Y", "declaration": "path:line"}; `declaration` is the caller's answer
// to a body of source that declares the name more than once, and this checks it rather than
// trusting it. Run this file over a request JSON of that shape to have the report alone.
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { pathToFileURL } from "node:url";

import { analyze, type FileSystem, visibleNames } from "../../core/src/frontend.ts";
import { referencePlaces, type ReferencePlace } from "../../core/src/references.ts";
import { readUnit } from "../../core/src/reader.ts";
import { scan, type Token } from "../../core/src/scan.ts";
import {
  declaredName,
  declarationKind,
  type Declaration,
} from "../../core/src/sr.ts";

import type { Residue } from "./declaration-rename.ts";

import type {
  Binding,
  Found,
  Occurrence,
  Outcome,
  Reader,
  Request,
} from "./occurrences.ts";

/** Where a name is written as a name: the declaration itself, the `in` that brings it,
 *  and the positions a declaration references another type in. */
export type Role = "declaration" | "inclusion" | "signature" | "field" | "composition" | "vr-type";

/** Why an identifier token the scanner read is not rewritten. */
type LeftAlone =
  | "declaration"
  | "parameter-name"
  | "unbound"
  | "qualified-reference"
  | "unresolved-import"
  | "local-collision"
  | "method-body"
  | "walk";

/** Where the raw text of the name stands in text no token covers, or in a token that is
 *  not this name: a comment, a string literal, or the inside of a longer identifier. A
 *  comment inside a Go clue block is the port's own rather than Khayyam's — the scanner
 *  reads the whole block as one comment, so this is the label that says whose comment it
 *  is, and it is said here because this is where the block's extent is known. */
type Unread = "comment" | "go-residue" | "string-literal" | "part-of-longer-identifier" | "unknown";

/** A place the service reports, with the role in the vocabulary of this file rather than
 *  in one the service would have to know. `go-identifier` is the second reader's own: a
 *  whole identifier inside a block of another language's source, which no reader of this
 *  language binds. */
export type Site = Occurrence & {
  role: Role | LeftAlone | "go-identifier" | "unread" | "string-literal" | "longer-identifier";
};

interface Place {
  path: string;
  line: number;
  form: string;
  kind: string;
}

function lineOffsets(source: string): number[] {
  const offsets = [0];
  for (let index = 0; index < source.length; index += 1) {
    if (source[index] === "\n") offsets.push(index + 1);
  }
  return offsets;
}

function placeOf(offsets: number[], token: { line: number; column: number }): number {
  return offsets[token.line - 1]! + token.column - 1;
}

function spanOf(offsets: number[], token: Token): { start: number; end: number } {
  const start = placeOf(offsets, token);
  return token.kind === "string"
    ? { start: start - 1, end: start + token.text.length + 2 }
    : { start, end: start + token.text.length };
}

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

/** One file read: its tokens, its declarations, and where every token stands. A
 *  declaration occupies the lines from its own line to the line before the next
 *  declaration's (`docs/khayyam/khayyam.md`, Declaration separator). */
interface Reading {
  path: string;
  source: string;
  tokens: Token[];
  offsets: number[];
  spans: { start: number; end: number; token: Token }[];
  declarations: Declaration[];
  faults: { reason: string; line: number }[];
}

function readAt(path: string, source: string): Reading {
  const scanned = scan(source);
  const read = readUnit(path, source);
  const offsets = lineOffsets(source);
  return {
    path,
    source,
    tokens: scanned.tokens,
    offsets,
    spans: scanned.tokens
      .filter((token) => token.kind !== "eof")
      .map((token) => ({ ...spanOf(offsets, token), token })),
    declarations: read.unit.declarations,
    faults: read.faults.map((fault) => ({ reason: fault.reason, line: fault.line })),
  };
}

function declarationSlices(reading: Reading): { declaration: Declaration; tokens: Token[] }[] {
  const starts = reading.declarations.map((declaration) => {
    let at = 0;
    while (at < reading.tokens.length && reading.tokens[at]!.line < declaration.line) at += 1;
    return at;
  });
  return reading.declarations.map((declaration, order) => ({
    declaration,
    tokens: reading.tokens.slice(
      starts[order]!,
      order + 1 < starts.length ? starts[order + 1]! : reading.tokens.length,
    ),
  }));
}

/** The place the scanner read for one token, which is the shape every place in this
 *  report has: a place `referencePlaces` handed over and a place this file read off the
 *  scanner's own stream are the same fact, and the report holds one of them. */
function atToken(token: Token): ReferencePlace {
  return {
    line: token.line,
    column: token.column,
    length: token.text.length,
    text: token.text,
  };
}

/** The role a place is reported under, which `referencePlaces` does not carry and will
 *  not: it answers where a name stands and never what shape it took, and the shape is
 *  what this report is written in. A form's own references all take one role; a capsule's
 *  block and an abstraction's are the ones that hold two. */
function roleOf(reading: Reading, declaration: Declaration, place: ReferencePlace): Role {
  switch (declaration.form) {
    case "vr":
      // A variable's type stands where a `tp` writes its subtype
      // (`docs/khayyam/khayyam.md`, Variable).
      return "vr-type";
    case "tp-mt":
      return "signature";
    case "tp-cp":
    case "tp-ab":
      // A block entry is a field written `name Type` or a composition entry written as a
      // name alone (`docs/khayyam/khayyam.md`, Capsule; Abstraction), and entries are
      // newline-separated, so which of the two a place is is what stands beside it on its
      // own line.
      return besideNothing(reading, place) ? "composition" : "field";
    default:
      // The forms that reach no place of a type, and are answered before a role is asked
      // for: an `in` routes a name and a scope's block is opaque text to the reader
      // (`docs/khayyam/khayyam.md`, Scope).
      return "inclusion";
  }
}

/** Whether nothing stands beside `place` on its own line. */
function besideNothing(reading: Reading, place: ReferencePlace): boolean {
  const from = reading.offsets[place.line - 1]!;
  const to = reading.source.indexOf("\n", from);
  const entry = reading.source.slice(from, to < 0 ? reading.source.length : to);
  return entry.replace(place.text, "").trim() === "";
}

/** The token a method's body begins at: the one after the `)` that closes its third group,
 *  which is where its signature ends (`docs/khayyam/khayyam.md`, Method). The places stop
 *  at the groups — a body is opaque text to the reader, so no name in one is a reference
 *  the reader counted — and this is the one place their answer does not reach, and the
 *  whole of what tells an identifier in a body apart from a parameter name. Negative
 *  where the groups do not stand where the form says they do, which leaves every
 *  identifier in the declaration to be reported as one nothing accounts for. */
function signatureEnd(tokens: Token[]): number {
  let index = 3;
  for (let group = 0; group < 3; group += 1) {
    if (tokens[index]?.text !== "(") return -1;
    let depth = 1;
    index += 1;
    while (depth > 0) {
      const token = tokens[index];
      if (token === undefined || token.kind === "eof") return -1;
      if (token.text === "(") depth += 1;
      else if (token.text === ")") depth -= 1;
      index += 1;
    }
  }
  return index;
}

/** The file each name this file sees is bound to: a local declaration binds in this file,
 *  and an `in` binds in the file behind it.
 *
 *  Which names the file sees is `visibleNames`' answer
 *  ([`core/src/frontend.ts`](../../core/src/frontend.ts)): it resolves the `in` clauses
 *  and checks the kinds behind them, and it is the resolver the gate asks through
 *  `analyze`, so a name this run plans a rewrite for is one the gate would have resolved
 *  too. Which file brought a visible name is a fact about this file's own declarations and
 *  is read from them, because `visibleNames` says which names are visible and never which
 *  file one came from.
 *
 *  A refusal arrives beside the set rather than in place of it, and the set is the whole
 *  of what is read here: an `in` whose URI does not resolve, a name the file behind it
 *  does not declare, or a kind that does not match (`docs/khayyam/khayyam.md`, Import
 *  Mechanism (`in`)) each stop it at the name that refused, so the names after it were
 *  never laid over this file at all. A name the set does not hold is therefore a name
 *  whose home this run cannot establish, and it stays unbound — the outcome a file with
 *  no `in` and no declaration of the name already gives, and the one that plans no
 *  rewrite. The file is not read as fully resolved on the strength of a set the resolver
 *  did not finish, and its refusal is not lost either: the gate asks `analyze` over every
 *  file the run read and counts the files that refuse. */
function bindings(
  reading: Reading,
  readings: readonly Reading[],
): Map<string, { path: string; collision?: string }> {
  const { visible } = visibleNames(
    { path: reading.path, declarations: reading.declarations },
    { read: (path) => readings.find((other) => other.path === path)?.source },
  );
  const bound = new Map<string, { path: string; collision?: string }>();
  // The two layers are laid as `visibleNames` lays them: a routed name first, this file's
  // own declarations over it. A name bound twice is reported against the binding it came
  // over, which is what the two collision texts name.
  for (const routed of [true, false]) {
    for (const declaration of reading.declarations) {
      const inclusion = declaration.form === "tp-in" || declaration.form === "vr-in";
      if (inclusion !== routed) continue;
      const name = declaredName(declaration);
      if (!visible.has(name)) continue;
      const previous = bound.get(name);
      bound.set(name, {
        path: inclusion ? declaration.path : reading.path,
        ...(previous === undefined
          ? {}
          : {
              collision:
                `${routed ? "already included from" : "already bound as"} ${previous.path}`,
            }),
      });
    }
  }
  return bound;
}

function resolveFile(readings: Reading[], uri: string): Reading | undefined {
  return readings.find((reading) => reading.path === uri);
}

/** A file name and a declared name compared without their spelling's case or its
 *  separators, so `Target_Race_Event` and `target-race-event.kh` are the one name
 *  written twice. This only ever produces a report: which spelling a repository gives a
 *  file is the [import address rule]'s owner, and a rule that renamed files would be
 *  choosing a convention rather than applying one. */
function sameSpelling(left: string, right: string): boolean {
  const fold = (text: string): string => text.toLowerCase().replace(/[-_]/g, "");
  return fold(left) === fold(right);
}

function occurrences(
  readings: Reading[],
  name: string,
  to: string,
  wanted: string | undefined,
): Found {
  const sameName: Place[] = [];
  const carried: Place[] = [];
  const taken: Place[] = [];
  const longerNames: { name: string; path: string; line: number }[] = [];
  const fileRenames: string[] = [];
  const faults: { path: string; reason: string; line: number }[] = [];
  for (const reading of readings) {
    for (const fault of reading.faults) faults.push({ path: reading.path, ...fault });
    // Only the file's own name, never a directory's: a module directory is named after its
    // concept on purpose, and every file under it would then be reported.
    const base = reading.path.split("/").slice(-1)[0]!.replace(/\.kh$/, "");
    if (sameSpelling(base, name)) fileRenames.push(reading.path);
    for (const declaration of reading.declarations) {
      const declared = declaredName(declaration);
      const place: Place = {
        path: reading.path,
        line: declaration.line,
        form: declaration.form,
        kind: declarationKind(declaration),
      };
      if (declared === name) {
        if (declaration.form === "tp-in" || declaration.form === "vr-in") carried.push(place);
        else sameName.push(place);
      } else if (declared.includes(name)) {
        longerNames.push({ name: declared, path: reading.path, line: declaration.line });
      }
      if (declared === to) taken.push(place);
    }
  }

  let target: Place | null = null;
  const ambiguity: string[] = [];
  if (wanted !== undefined) {
    const found = sameName.find((place) => `${place.path}:${place.line}` === wanted);
    if (found === undefined) {
      ambiguity.push(
        `${wanted} is not a declaration of \`${name}\`; the sources declare it at ` +
          (sameName.map((place) => `${place.path}:${place.line}`).join(", ") || "nowhere"),
      );
    } else target = found;
  } else if (sameName.length === 1) {
    target = sameName[0]!;
  } else if (sameName.length === 0) {
    ambiguity.push(`no declaration in the sources is named \`${name}\``);
  } else {
    ambiguity.push(
      `${sameName.length} declarations are named \`${name}\`, so the name does not say which one this run is about: ` +
        sameName.map((place) => `${place.path}:${place.line} (${place.form})`).join(", ") +
        ". The language calls a collision an architecture error rather than a disambiguation problem" +
        " (`docs/khayyam/khayyam.md`, Import Mechanism (`in`)), so none of them is picked silently; pass" +
        " --declaration to name the one this run is about.",
    );
  }

  const sites: Site[] = [];
  const leftAlone: Site[] = [];
  const site = (
    reading: Reading,
    place: ReferencePlace,
    role: Site["role"],
    why?: string,
  ): Site => ({
    path: reading.path,
    line: place.line,
    column: place.column,
    length: place.length,
    role,
    ...(why === undefined ? {} : { why }),
  });

  if (target !== null) {
    for (const reading of readings) {
      const bound = bindings(reading, readings);
      for (const { declaration, tokens } of declarationSlices(reading)) {
        const places = referencePlaces(reading.source, declaration);
        const isInclusion = declaration.form === "tp-in" || declaration.form === "vr-in";
        const declaresHere = !isInclusion;
        const home = isInclusion ? declaration.path : reading.path;
        // The declared name is the second token of the declaration's own line — `tp Name …`,
        // `vr Name …`, which is the shape the parser reads — and not a reference, so it is
        // not among the places.
        const declared = tokens[1]!;

        // It is a place the name stands only when that name is the one this run is about:
        // a declaration of something else is not a consumer of it.
        if (declared.text === name) {
          if (declaresHere && home !== target.path) {
            leftAlone.push(
              site(
                reading,
                atToken(declared),
                "declaration",
                `another declaration of \`${name}\` stands elsewhere`,
              ),
            );
          } else if (isInclusion && home !== target.path) {
            const reads = resolveFile(readings, home) !== undefined;
            leftAlone.push(
              site(
                reading,
                atToken(declared),
                reads ? "walk" : "unresolved-import",
                reads
                  ? `it brings \`${name}\` from ${home}, which is not the file this run is about`
                  : `\`${home}\` is not among the files this run read`,
              ),
            );
          } else {
            sites.push(
              site(reading, atToken(declared), isInclusion ? "inclusion" : "declaration"),
            );
          }
        }

        // A routed name is the declaration's own name and not a use of a type: an `in`
        // declares the name here and binds it in the file behind it
        // (`docs/khayyam/khayyam.md`, Import Mechanism (`in`)), so the one place its line
        // holds is the place the name is declared, reported above.
        for (const place of places) {
          if (isInclusion) continue;
          if (place.text.includes(".")) {
            if (place.text.split(".").slice(-1)[0] === name) {
              leftAlone.push(
                site(
                  reading,
                  place,
                  "qualified-reference",
                  `a qualified reference is accepted without a binding check, so \`${place.text}\` is not read as this declaration`,
                ),
              );
            }
            continue;
          }
          if (place.text !== name) continue;
          const where = bound.get(name);
          if (where === undefined) {
            leftAlone.push(
              site(
                reading,
                place,
                "unbound",
                "no declaration and no `in` brings the name into this file",
              ),
            );
          } else if (where.collision !== undefined) {
            leftAlone.push(site(reading, place, "local-collision", where.collision));
          } else if (where.path !== target.path) {
            leftAlone.push(site(reading, place, "walk", `it names \`${name}\` at ${where.path}`));
          } else {
            sites.push(site(reading, place, roleOf(reading, declaration, place)));
          }
        }

        // Everything else the scanner read in the declaration. A parameter names a value,
        // never a type, so one spelled like the declaration is left alone and reported
        // because a reader of the line is owed the distinction; and the reader describes a
        // declaration's types and not its body's, so an identifier in a body is left
        // alone and reported rather than guessed at.
        const bodyFrom = declaration.form === "tp-mt" ? signatureEnd(tokens) : -1;
        const placed = new Set(places.map((place) => `${place.line}:${place.column}`));
        for (let index = 0; index < tokens.length; index += 1) {
          const token = tokens[index]!;
          if (token.kind !== "ident" || token.text !== name) continue;
          if (index === 1 || placed.has(`${token.line}:${token.column}`)) continue;
          if (index < bodyFrom) {
            leftAlone.push(
              site(
                reading,
                atToken(token),
                "parameter-name",
                "a parameter names a value, not a type",
              ),
            );
          } else if (bodyFrom >= 0) {
            leftAlone.push(
              site(
                reading,
                atToken(token),
                "method-body",
                "a method body is opaque text to the reader, so what it binds is undecided",
              ),
            );
          } else {
            leftAlone.push(
              site(
                reading,
                atToken(token),
                "walk",
                "no position in this declaration accounts for this token",
              ),
            );
          }
        }
      }
    }
  }

  // Every occurrence of the name in the raw text, classified by the token covering it.
  // What no token covers is a comment, and a name is written in prose as often as in
  // code - the reader that reads a comment is the one writing it. A comment inside a Go
  // clue block is the port's, so it is reported as the port's and not as prose: the block's
  // extent is this file's own answer, and a run that reported it as prose would be
  // answering a question about Go source with Khayyam's words.
  const unread: (Site & { class: Unread; text: string })[] = [];
  for (const reading of readings) {
    const regions = residueBlocks(reading.source.split("\n")).map((block) => ({
      from: block.marker + 1,
      to: block.last + 1,
    }));
    let from = reading.source.indexOf(name);
    while (from >= 0) {
      const line = lineOf(reading.offsets, from);
      const place = {
        path: reading.path,
        line,
        column: from - reading.offsets[line - 1]! + 1,
        length: name.length,
      };
      const covering = reading.spans.find((span) => span.start <= from && from < span.end);
      if (covering === undefined) {
        const inBlock = regions.some((region) => line >= region.from && line <= region.to);
        unread.push({
          ...place,
          role: "unread",
          class: inBlock ? "go-residue" : "comment",
          text: name,
        });
      } else if (covering.token.kind === "string") {
        unread.push({
          ...place,
          role: "string-literal",
          class: "string-literal",
          text: name,
        });
      } else if (covering.token.kind === "ident" && covering.token.text !== name) {
        unread.push({
          ...place,
          role: "longer-identifier",
          class: "part-of-longer-identifier",
          text: covering.token.text,
        });
      } else if (covering.token.kind !== "ident") {
        unread.push({ ...place, role: "unread", class: "unknown", text: name });
      }
      from = reading.source.indexOf(name, from + 1);
    }
  }

  return {
    name,
    same_name: sameName,
    carried,
    taken,
    target,
    ambiguity,
    sites,
    left_alone: leftAlone,
    unread,
    longer_names: longerNames.sort((left, right) =>
      left.path === right.path ? left.line - right.line : left.path < right.path ? -1 : 1,
    ),
    file_renames: fileRenames.sort(),
    faults,
    missing: [],
  };
}

function main(): void {
  const request = JSON.parse(readFileSync(process.argv[2]!, "utf8")) as Request;
  process.stdout.write(JSON.stringify(findOccurrences(request)));
}

/** What the language's own scanner and reader say about `name` across the request's
 *  paths. This is the whole of the finder's answer; what a caller does with it is the
 *  caller's own. */
export function findOccurrences(request: Request): Found {
  const readings: Reading[] = [];
  const missing: string[] = [];
  for (const path of request.paths) {
    let source: string | undefined;
    try {
      source = readFileSync(join(request.root, path), "utf8");
    } catch {
      missing.push(path);
    }
    if (source !== undefined) readings.push(readAt(path, source));
  }
  const report = occurrences(readings, request.name, request.to, request.declaration);
  return { ...report, missing };
}

// The gate, as the binding answers it: the frontend's verdict on one path's text, with
// `read` standing in for the files this run has not written yet — so a plan is checked
// before it is written, which is the only order in which the check is worth anything.
export function analyzeWith(
  path: string,
  source: string,
  read: Reader,
): Outcome {
  const fileSystem: FileSystem = { read };
  const result = analyze(path, source, fileSystem);
  return result.outcome === "accept"
    ? { outcome: "accept" }
    : { outcome: "refuse", reason: result.reason, line: result.line };
}

// The Go clue block, as the rule finds it. `end_blocks` in `targets/go/khayyam_source.py`
// states it: an end-of-file Go clue block is a `// TODO(go-migrate):` line directly above
// `/*`, or above a `// --- go-source: ` header and its `/*`; a block under that header is
// sealed by its sha256 and carries a `// --- end go-source: ` line below its `*/`. The rule
// is restated here rather than imported, because the bridge's reader reads the block with
// the Go lexer and this one reads it with the Khayyam scanner; where a block closes is the
// scanner's answer, below.
const GO_MIGRATE_MARKER = /^\s*\/\/\s*TODO\(go-migrate\)/;
const GO_SOURCE_HEADER = "// --- go-source: ";
const GO_SOURCE_END = "// --- end go-source: ";

interface ResidueBlock {
  /** Zero-based line indexes, because a block is a range of a file and a range has no
   *  one-based form. */
  marker: number;
  body: number;
  close: number;
  last: number;
  sealed: boolean;
}

/** The line the block's closing marker stands on, or null when the file's tail holds no
 *  close at all. `scan` reads a block comment as one token run and refuses an unterminated
 *  one over the rest of the file, so the smallest tail of the file it reads whole is where
 *  the block ends: the block's extent is the scanner's own reading of the comment, found by
 *  asking it. */
function closeOf(lines: readonly string[], open: number): number | null {
  const reads = (last: number): boolean =>
    scan(lines.slice(open, last + 1).join("\n")).ok;
  if (!reads(lines.length - 1)) return null;
  let low = open + 1;
  let high = lines.length - 1;
  while (low < high) {
    const middle = (low + high) >> 1;
    if (reads(middle)) high = middle;
    else low = middle + 1;
  }
  return low;
}

/** Every end-of-file Go clue block of a file. A marker whose block never closes is not a
 * block and the walk carries on past it; the bridge stops there instead, which can only
 * differ for a file whose unclosed block is followed by another marker, and a marker
 * inside an unclosed comment is not one. */
function residueBlocks(lines: readonly string[]): ResidueBlock[] {
  const blocks: ResidueBlock[] = [];
  let index = 0;
  while (index + 1 < lines.length) {
    const following = lines[index + 1]!.trim();
    const sealed = following.startsWith(GO_SOURCE_HEADER);
    if (!GO_MIGRATE_MARKER.test(lines[index]!) || (following !== "/*" && !sealed)) {
      index += 1;
      continue;
    }
    const open = index + (sealed ? 2 : 1);
    if (lines[open]?.trim() !== "/*") {
      index += 1;
      continue;
    }
    const close = closeOf(lines, open);
    if (close === null) {
      index += 1;
      continue;
    }
    const last = sealed && lines[close + 1]?.startsWith(GO_SOURCE_END) === true ? close + 1 : close;
    blocks.push({ marker: index, body: open + 1, close, last, sealed });
    index = last + 1;
  }
  return blocks;
}

type Read =
  | { ok: true; tokens: Token[]; unreadable: string[] }
  | { ok: false; reason: string };

/** Every whole identifier the scanner reads in `text`, with `line`/`column` naming where
 *  `text` itself starts. Nothing here re-implements a lexer's rules: what an identifier is
 *  is `scan`'s answer, and a place is a site only where the scanner read a whole token
 *  equal to the name — which is what keeps `PacketTarget` from matching a `Target` rename.
 *
 *  What this does over the scanner's own stream is read again what the scanner skipped. It
 *  takes the rest of a line with it when it meets a character it does not read, and a Go
 *  body is full of them — `*` alone is enough — so without this the mode would find none
 *  of the identifiers after the first pointer on a line.
 *
 *  What that does not cover is stated here, because it is the boundary between this and the
 *  Go lexer the bridge used. A double-quoted string and a comment of either form are the
 *  scanner's own already, so a name inside either is not rewritten. A Go rune literal is
 *  read as its characters and a backquoted raw string is read as Go text, where the Go
 *  lexer read each as one literal: a name inside either is rewritten here and would not
 *  have been there, and a comment marker inside a raw string is an opener to this scanner,
 *  so a block holding one is read as a comment to its end — left whole and reported rather
 *  than half-read. A region the scanner refuses whole is reported the same way. That is the
 *  price of not re-implementing Go's lexical rules, and it costs a site only where a raw
 *  string names the declaration, which is a body of source this mode reports rather than guesses at.
 */
function goIdentifiers(text: string, line: number, column: number): Read {
  const result = scan(text);
  if (!result.ok) {
    return { ok: false, reason: `${result.fault.reason} at line ${result.fault.line + line - 1}` };
  }
  const offsets = lineOffsets(text);
  /** Where `text`'s own offset stands in the file: the first line is offset by the caller's
   *  column and every other line begins at one, as it does in the source. */
  const place = (at: number): { line: number; column: number } => {
    const standing = lineOf(offsets, at);
    return {
      line: standing + line - 1,
      column: (standing === 1 ? column - 1 : 0) + (at - offsets[standing - 1]!) + 1,
    };
  };
  const tokens: Token[] = [];
  for (const token of result.tokens) {
    if (token.kind !== "ident") continue;
    const at = place(offsets[token.line - 1]! + token.column - 1);
    tokens.push({ ...token, line: at.line, column: at.column });
  }
  const unreadable: string[] = [];
  for (const fault of result.faults) {
    if (fault.reason !== "unexpected-character" || fault.extent !== "line") continue;
    // The rest of the fault's line, which the scanner took with it, read again from where
    // it stopped — and placed by its own offset, so a region inside a region lands where
    // the file says it does.
    const from = offsets[fault.line - 1]! + fault.column - 1 + fault.length;
    const to = text.indexOf("\n", from);
    const at = place(from);
    const part = goIdentifiers(
      text.slice(from, to < 0 ? text.length : to),
      at.line,
      at.column,
    );
    if (!part.ok) {
      unreadable.push(`line ${fault.line + line - 1}: ${part.reason}`);
      continue;
    }
    tokens.push(...part.tokens);
    unreadable.push(...part.unreadable);
  }
  return { ok: true, tokens, unreadable };
}

/** (the Go clue block places whose whole Go identifier is `name`, what was left). A block
 *  sealed by its sha256 is left whole: rewriting inside one would make the seal a lie, and
 *  the go-clue-residue rule already holds that a sealed block is only ever removed whole. */
function goSites(
  lines: readonly string[],
  name: string,
  path: string,
): { sites: Site[]; left: string[] } {
  const sites: Site[] = [];
  const left: string[] = [];
  for (const block of residueBlocks(lines)) {
    if (block.sealed) {
      left.push(`line ${block.marker + 1}: sealed by its sha256, so it is left whole`);
      continue;
    }
    const read = goIdentifiers(lines.slice(block.body, block.close).join("\n"), block.body + 1, 1);
    if (!read.ok) {
      left.push(`line ${block.body + 1}: the block does not lex: ${read.reason}`);
      continue;
    }
    for (const entry of read.unreadable) {
      left.push(`line ${block.body + 1}: a part of the block does not lex: ${entry}`);
    }
    for (const token of read.tokens) {
      if (token.text !== name) continue;
      sites.push({
        path,
        line: token.line,
        column: token.column,
        length: name.length,
        role: "go-identifier",
      });
    }
  }
  return { sites, left };
}

/** The binding this module is: what a name means in Khayyam, and what a plan must still
 *  mean for `analyze` to accept it. The caller hands this to a run rather than looking it
 *  up, because there is one of it and this process holds no other. */
export const khayyamBinding: Binding = {
  language: "khayyam",
  find: findOccurrences,
  analyze: analyzeWith,
};

/** The residue pass this port needs, handed to the mechanism beside the binding rather than
 *  reached through it: which language left the text is this file's own fact, and the label a
 *  run that includes this pass reports itself under is written here with both names in it. */
export const khayyamResidue: Residue = {
  mode: `${khayyamBinding.language}+go-residue`,
  find: (text, name, path) => goSites(text.split("\n"), name, path),
};

// `rename.ts` beside this file hands the binding and the residue pass to the service;
// running this file asks the finder for the places alone, which is what a session inspecting
// one name by hand needs.
if (process.argv[1] !== undefined && pathToFileURL(process.argv[1]).href === import.meta.url) {
  main();
}
