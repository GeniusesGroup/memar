import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

import { checkLinks, readLinkMap } from "../src/link.ts";
import type { FileSystem } from "../../../core/src/frontend.ts";
import type { LinkEntry } from "../src/link.ts";

/** The repository is read through its root, the base the import-address rule
 *  fixes for a URI (modules/khayyam/rules/import-address/import-address.md). */
const REPOSITORY = new URL("../../../../../", import.meta.url);

const repository: FileSystem = {
  read: (path) => {
    try {
      return readFileSync(new URL(path, REPOSITORY), "utf8");
    } catch {
      return undefined;
    }
  },
};

const ENTRY: LinkEntry = {
  module: "modules/khayyam/targets/js/lib/branch.js",
  protocol: "docs/protocols/process/control-flow.md",
  checked: [
    {
      requirement:
        "flow constructs are explicit operations over the primitive that groups a branch body",
      at: "Library-Defined Control Flow",
    },
    {
      requirement: "the generic conditional takes an explicit branch scope",
      at: "The Generic Form: IF/ELSE",
    },
  ],
  declares: {
    Condition: { kind: "capsule" },
    Scope: { kind: "capsule" },
    IF: { kind: "abstraction" },
    ELSE: { kind: "abstraction" },
    OnTrue: {
      kind: "method",
      owner: "IF",
      ownerParameter: "self",
      influencing: [
        { name: "condition", type: "Condition" },
        { name: "branch", type: "Scope" },
      ],
      influenced: [],
    },
    OnFalse: {
      kind: "method",
      owner: "ELSE",
      ownerParameter: "self",
      influencing: [
        { name: "condition", type: "Condition" },
        { name: "branch", type: "Scope" },
      ],
      influenced: [],
    },
  },
  provides: { Condition: "Condition", IF: "IF", ELSE: "ELSE", OnTrue: "OnTrue", OnFalse: "OnFalse" },
};

const MAP = {
  "modules/khayyam/targets/js/lib/branch.kh": ENTRY,
};

test("a map is a table of URI to entry, and an entry names a module, a protocol document, and what was checked", () => {
  const result = readLinkMap(JSON.stringify(MAP));
  assert.deepEqual(result.ok, true, result.ok ? "" : result.problems.join("; "));
  if (!result.ok) return;
  assert.deepEqual(result.map, MAP);
});

test("a map that is not JSON is refused, saying what it could not read", () => {
  const result = readLinkMap("{");
  assert.equal(result.ok, false);
  if (result.ok) return;
  assert.equal(result.problems.length, 1);
});

test("an entry that names no protocol document is refused", () => {
  const { protocol: _omitted, ...withoutProtocol } = ENTRY;
  const result = readLinkMap(JSON.stringify({ "a.kh": withoutProtocol }));
  assert.equal(result.ok, false);
});

test("an entry that records no conformance check is refused, because the record is what the map is for", () => {
  const result = readLinkMap(
    JSON.stringify({ "a.kh": { ...ENTRY, checked: [] } }),
  );
  assert.equal(result.ok, false);
});

test("an entry that provides nothing is refused", () => {
  const result = readLinkMap(JSON.stringify({ "a.kh": { ...ENTRY, provides: {} } }));
  assert.equal(result.ok, false);
});

test("an entry that declares nothing in place of the unit is refused", () => {
  const result = readLinkMap(JSON.stringify({ "a.kh": { ...ENTRY, declares: {} } }));
  assert.equal(result.ok, false);
});

test("a method the map declares with no owner group is refused", () => {
  const onTrue = ENTRY.declares["OnTrue"];
  assert.ok(onTrue !== undefined && onTrue.kind === "method");
  const { ownerParameter: _omitted, ...withoutOwner } = onTrue;
  const result = readLinkMap(
    JSON.stringify({ "a.kh": { ...ENTRY, declares: { ...ENTRY.declares, OnTrue: withoutOwner } } }),
  );
  assert.equal(result.ok, false);
});

test("a name the map provides is one it declares", () => {
  const result = readLinkMap(
    JSON.stringify({ "a.kh": { ...ENTRY, provides: { Absent: "Absent" } } }),
  );
  assert.equal(result.ok, false);
});

test("a key that is not a URI naming a .kh unit is refused", () => {
  const result = readLinkMap(JSON.stringify({ "modules/thing.js": ENTRY }));
  assert.equal(result.ok, false);
});

test("an empty map is a map: nothing is linked, and everything compiles from its own source", () => {
  const result = readLinkMap("{}");
  assert.equal(result.ok, true);
  if (!result.ok) return;
  assert.deepEqual(result.map, {});
  assert.deepEqual(checkLinks(result.map, repository), []);
});

test("every entry of the repository's own map resolves", () => {
  const source = readFileSync(new URL("../link_map.json", import.meta.url), "utf8");
  const result = readLinkMap(source);
  assert.equal(result.ok, true, result.ok ? "" : result.problems.join("; "));
  if (!result.ok) return;
  assert.deepEqual(checkLinks(result.map, repository), []);
});

/** A repository holding what the entry above names, so each of the three faults
 *  below is the one it is about and not another. */
const held: FileSystem = {
  read: (path) => {
    const table: Record<string, string> = {
      "lib/branch.js": "export const IF = {};",
      [ENTRY.module]: "export const IF = {};",
      "docs/protocols/process/control-flow.md": repository.read("docs/protocols/process/control-flow.md") ?? "",
    };
    return table[path];
  },
};

test("an entry whose module is not there is reported against its URI", () => {
  const problems = checkLinks({ "lib/branch.kh": { ...ENTRY, module: "lib/absent.js" } }, held);
  assert.deepEqual(problems, [
    { uri: "lib/branch.kh", about: "the module lib/absent.js is not there" },
  ]);
});

test("an entry whose protocol document is not there is reported against its URI", () => {
  const problems = checkLinks(
    { "lib/branch.kh": { ...ENTRY, protocol: "docs/protocols/absent.md" } },
    held,
  );
  assert.deepEqual(problems, [
    { uri: "lib/branch.kh", about: "the protocol document docs/protocols/absent.md is not there" },
  ]);
});

test("a check recorded against a section the document does not have is reported", () => {
  const problems = checkLinks(
    {
      "lib/branch.kh": {
        ...ENTRY,
        checked: [{ requirement: "a claim", at: "A Section That Is Not There" }],
      },
    },
    held,
  );
  assert.deepEqual(problems, [
    {
      uri: "lib/branch.kh",
      about: "the protocol document has no section A Section That Is Not There",
    },
  ]);
});

test("every unit the map stands in for is a unit that declares what the map declares", () => {
  const source = readFileSync(new URL("../link_map.json", import.meta.url), "utf8");
  const result = readLinkMap(source);
  assert.equal(result.ok, true);
  if (!result.ok) return;
  for (const [uri, entry] of Object.entries(result.map)) {
    const unit = repository.read(uri);
    assert.notEqual(unit, undefined, `${uri} is not a file in the repository`);
    for (const name of Object.keys(entry.declares)) {
      const declares = new RegExp(`^\\s*(tp|vr)\\s+${name}\\b`, "m");
      assert.match(unit!, declares, `${uri} does not declare ${name}`);
    }
  }
});
