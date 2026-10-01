import assert from "node:assert/strict";

import type { Reach } from "../src/definition.ts";

// The one document the definitions are asked about, and the table the files behind its
// inclusions come from. Every test file in this set builds on these rather than each
// writing its own, because a shape that is pinned in four places is a shape that will be
// changed in one of them and not the other three.

/** One document exercising every name the goal names: a parameter, a body-local, a type
 *  the file declares, a type that arrived by `in`, and a variable that arrived by `in`. */
export const SOURCE = [
  'tp Bool in "math/boolean.kh"',
  "tp Reader ab",
  "tp Buffer cp {",
  "\tdata U8",
  "}",
  "tp Set mt (self Reader) (key String) (err Error) {",
  "\tvr local Buffer",
  "\tkey.CopyFrom(local)(err)",
  "\tBool.IsTrue()",
  "\tlimit.Compare()",
  "}",
  'vr limit in "math/limit.kh"',
  "",
].join("\n");

export const LINES = SOURCE.split("\n");

/** The character a name stands at on a line of the document above, read out of the
 *  source rather than written here, so a change to the fixture cannot leave a test
 *  asserting about a column that moved. */
export const at = (line: number, name: string): number => {
  const character = LINES[line]!.indexOf(name);
  assert.notEqual(character, -1, `line ${line} does not carry ${name}`);
  return character;
};

/** The same, for a test that writes its own document: the character a name stands at, and
 *  the line it stands on, both found rather than counted. */
export const linesOf = (source: string): string[] => source.split("\n");

export const characterOn = (lines: string[], line: number, name: string): number => {
  const character = lines[line]!.indexOf(name);
  assert.notEqual(character, -1, `line ${line} does not carry ${name}`);
  return character;
};

/** The files an inclusion's URI can address, as a table rather than a directory: what a
 *  definition may reach beyond the document is this toolchain's own seam, and a test
 *  states it as data. The table stands in for whatever a base resolves through — a
 *  manifest, a directory convention, a table like this one — and deliberately names no
 *  base, because the base is not a thing this toolchain chooses for itself and a fixture
 *  that named one would state a position no test is here to decide. */
export function reach(files: Record<string, string>): Reach {
  return {
    resolve: (path) => {
      const text = files[path];
      return text === undefined
        ? { because: `nothing here is at ${path}` }
        : { base: { directory: "/w", markedBy: "table" }, found: { uri: `file:///w/${path}`, text } };
    },
    held: () => undefined,
  };
}

export const FILES: Record<string, string> = {
  "math/boolean.kh": "// A truth value.\ntp Bool cp {}\n",
  "math/limit.kh": "vr limit U8\n",
};

export const URI = "file:///w/set.kh";

/** The reach the document above is asked through: the two files its inclusions name, and
 *  nothing else, so every answer that leaves the document is read against files this
 *  repository's tests wrote themselves. */
export const asking = reach(FILES);

/** A reach with a base and no files behind it, for a document whose inclusions are
 *  accounted for by nothing. */
export const emptyReach: Reach = {
  resolve: (path) => ({ because: `nothing declares how ${path} resolves` }),
  held: () => undefined,
};

/** A document that includes `Bool` and uses it in a body — the shape every question that
 *  has to leave the document starts from. */
export const INCLUDING = [
  'tp Bool in "math/boolean.kh"',
  "tp Run mt (self Bool) () () {",
  "\tBool.IsTrue()",
  "}",
  "",
].join("\n");

export const USING = { line: 2, character: characterOn(linesOf(INCLUDING), 2, "Bool") };
