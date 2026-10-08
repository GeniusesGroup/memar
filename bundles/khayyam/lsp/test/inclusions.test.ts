import assert from "node:assert/strict";
import test from "node:test";

import { inclusionFindings } from "../src/inclusions.ts";
import { emptyReach, reach, URI } from "./definition-fixture.ts";
import type { Reach } from "../src/definition.ts";

// What a document claims about the files it includes, checked against the files that are
// there. A claim a toolchain cannot account for is a fault where the claim stands, and it
// is not the same kind of thing as a fault of reading: nothing was unread, the file said
// something this toolchain could not confirm. The two are reported together and neither
// stands for the other.

const SOURCE = [
  'tp Bool in "math/boolean.kh"', //      0  a type that arrives
  'tp Gone in "math/absent.kh"', //         1  a URI addressing nothing
  'tp Wrong in "math/wrong.kh"', //         2  a file declaring it as the other kind
  'tp Unnamed in "math/other.kh"', //       3  a file declaring no such name
  'vr limit in "math/limit.kh"', //         4  a variable that arrives
  "tp Local cp {}", //                       5  a declaration that is not an inclusion
  "",
].join("\n");

const FILES: Record<string, string> = {
  "math/boolean.kh": "tp Bool cp {}\n",
  // A file that declares the very name this document claims, as the other kind — the one
  // case that is a kind mismatch rather than a name the file does not declare.
  "math/wrong.kh": "vr Wrong U8\n",
  "math/other.kh": "tp Something cp {}\n",
  "math/limit.kh": "vr limit U8\n",
  "math/x.kh": "tp X cp {}\n",
};

const at = (line: number, name: string): number => {
  const character = SOURCE.split("\n")[line]!.indexOf(name);
  assert.notEqual(character, -1, `line ${line} does not carry ${name}`);
  return character;
};

/** The same table, over a base this test names, so that what a fault says about its base
 *  is the base it was given and not a fixture's. */
const table = reach(FILES);
/** The same table, over a root this test names, so that what a finding says about its root
 *  is the root it was given and not a fixture's. */
const from = (directory: string | undefined): Reach => ({
  ...table,
  resolve: (path) => {
    const resolved = table.resolve(path, URI);
    if (resolved.found !== undefined) return resolved;
    return {
      ...(directory === undefined ? {} : { base: { directory, markedBy: "table" } }),
      because: resolved.because,
    };
  },
});

test("an inclusion this toolchain can account for is not a fault", () => {
  assert.deepEqual(
    inclusionFindings(URI, 'tp Bool in "math/boolean.kh"\nvr limit in "math/limit.kh"\n', from("/w")).map((f) => f.reason),
    [],
    "both names are declared behind their URIs, and a file that says nothing wrong is not a fault",
  );
});

test("a URI addressing nothing is refused by the label that names it, on the name that carries it", () => {
  const findings = inclusionFindings(URI, SOURCE, from("/w"));
  const unresolved = findings.filter((finding) => finding.reason === "unresolved-import");
  assert.equal(unresolved.length, 1);
  const [fault] = unresolved;
  // The fault stands on the name, not on the whole line and not on the path: the name is
  // what the file claims, and the path is the claim about where it comes from.
  assert.deepEqual(
    { line: fault!.line, character: fault!.character, length: fault!.name.length },
    { line: 2, character: at(1, "Gone"), length: 4 },
  );
  assert.equal(fault!.name, "Gone");
});

test("a file that declares no such name, and one that declares it as the other kind, are two faults", () => {
  assert.deepEqual(
    inclusionFindings(URI, SOURCE, from("/w")).map((finding) => `${finding.reason}@${finding.line}`),
    ["unresolved-import@2", "kind-mismatch@3", "name-not-declared@4"],
    "each label says which of the three things went wrong, and a reader can act on each",
  );
});

test("a finding carries the reason resolution gave, because three different faults look alike otherwise", () => {
  // A file that is not in the repository, a repository whose root could not be found, and
  // a repository whose manifest declares nothing about how an address resolves are three
  // faults and one "not found", and only the sentence tells a reader which one happened:
  // writing the file fixes one, opening the repository as a folder fixes another, and
  // writing a manifest fixes the third.
  const [resolved] = inclusionFindings(URI, SOURCE, from("/w")).filter((f) => f.reason === "unresolved-import");
  assert.ok(resolved);
  assert.match(resolved.message, /nothing here is at math\/absent\.kh/, "the reason resolution gave is in it, verbatim");
  // The root itself is named by the resolution that found it, and what a finding carries is
  // the reason that resolution gave; the wire test is where the root is seen in the sentence.

  const [none] = inclusionFindings(URI, SOURCE, emptyReach).filter((f) => f.reason === "unresolved-import");
  assert.ok(none, "an inclusion nothing resolves is still a claim nothing accounts for");
  assert.match(none.message, /nothing declares how/, "and the reason is the one resolution gave");
  assert.doesNotMatch(none.message, /\/w/, "a root that was never found is not in the sentence");
});

test("a document that claims nothing about other files has no findings", () => {
  assert.deepEqual(
    inclusionFindings(URI, "tp A cp {}\n\ntp B ab\n", emptyReach).map((f) => f.reason),
    [],
    "a file with no inclusion is not a fault whatever the server can reach",
  );
  assert.deepEqual(inclusionFindings(URI, "", emptyReach), []);
  assert.deepEqual(inclusionFindings(URI, "tp\n}\n", emptyReach), [], "a file that could not be read has no claims to check");
});

test("a URI in a file that could not be read past is not claimed, and the reader is told about the reading instead", () => {
  // The reader recovers per declaration, so a declaration it could not read is not a
  // claim this server can hold against a file — and inventing one would fault a line
  // that says nothing. The declaration it did read is still a claim, and is still checked.
  const findings = inclusionFindings(URI, 'tp X in "math/x.kh"\nthis is not a declaration\n', from("/w"));
  assert.deepEqual(findings.map((f) => f.reason), [], "the one claim it did read is accounted for");
  assert.deepEqual(
    inclusionFindings(URI, 'tp X in "math/nothing.kh"\nthis is not a declaration\n', from("/w")).map((f) => f.reason),
    ["unresolved-import"],
    "and it is still checked when it is not",
  );
});
