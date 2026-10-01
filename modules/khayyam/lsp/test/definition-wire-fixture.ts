import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { pathToFileURL } from "node:url";

import type { Server } from "./harness.ts";
import type { Location } from "./wire.ts";

// Two real files, written by the tests that need them: a document that includes a name
// from another file, and that file. Over the wire this is the one shape that cannot be a
// table, because the server reads the file behind an inclusion's URI from the base it was
// told — so a real file has to be there. It is written into a directory of its own under
// the operating system's temporary directory rather than borrowed from this repository,
// because no file this repository may curate, archive, or delete may be the one a shape is
// pinned to.

export interface Tree {
  /** The directory to state as the workspace, and the one to remove afterwards. */
  root: string;
  /** The document to open, and the URI a client would open it under. */
  uri: string;
  /** Where the file behind the inclusion sits, and the URI the answer must carry. */
  includedUri: string;
  /** That file's own lines, so a test can say the name the answer names is on the line
   *  the answer says — the guard a borrowed file never carried. */
  includedLines: string[];
}

/** Writes the two files and returns where they are. The directory deliberately carries **no**
 *  declaring file, so every fixture here measures the refusal a project gets for having
 *  declared nothing — which is the case the server was in for three days and the one worth
 *  pinning over the wire. A fixture that planted a `manifest.yaml` would be measuring the
 *  other case, and that case is measured in [resolve.test.ts](./resolve.test.ts) where the
 *  tree can be arranged on purpose.
 *
 *  So a `.git` directory is not planted either, and would mean nothing if it were: a
 *  version-control entry is not a declaration, and one was once read as one. */
export function tree(): Tree {
  const root = mkdtempSync(join(tmpdir(), "khayyam-definition-"));
  mkdirSync(join(root, "math"));
  const included = ["// A truth value.", "tp Bool cp {}", ""];
  writeFileSync(join(root, "set.kh"), SOURCE, "utf8");
  writeFileSync(join(root, "math", "boolean.kh"), included.join("\n"), "utf8");
  return {
    root,
    uri: pathToFileURL(join(root, "set.kh")).href,
    includedUri: pathToFileURL(join(root, "math", "boolean.kh")).href,
    includedLines: included,
  };
}

/** Removes a tree this module wrote. Given to a test's `after`, so a failed test leaves
 *  nothing behind either. */
export function discard(files: Tree): void {
  rmSync(files.root, { recursive: true, force: true });
}

export const SOURCE = [
  'tp Bool in "math/boolean.kh"',
  "tp Run mt (self Bool) () () {",
  "\tBool.IsTrue()",
  "}",
  "",
].join("\n");

const at = (line: number, name: string): number => {
  const character = SOURCE.split("\n")[line]!.indexOf(name);
  assert.notEqual(character, -1, `line ${line} does not carry ${name}`);
  return character;
};

/** What the server answers for the included name used in the body. */
export const answer = (server: Server, uri: string) =>
  server.request<Location | null>("textDocument/definition", {
    textDocument: { uri },
    position: { line: 2, character: at(2, "Bool") },
  });

/** Where the name is declared in the file behind the URI, read out of what that file
 *  holds rather than written here. */
export const DECLARED = { line: 1, character: 3, length: 4 };

/** The sentence a document is given for the claim it cannot account for: an address is
 *  resolved through the manifest of the module that wrote it, and where such a manifest is
 *  looked for is not ruled, so nothing says how this address resolves. */
export const NO_MANIFEST = /an address is resolved through the declaring file of the project it is written in/;

export { at };
