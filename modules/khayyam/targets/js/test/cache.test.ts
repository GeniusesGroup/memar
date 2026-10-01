import assert from "node:assert/strict";
import { mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import { build, keyOf, VERSIONS } from "../src/cache.ts";
import { readLinkMap, type LinkMap } from "../src/link.ts";
import type { BuildEnvironment, UnitRecord } from "../src/cache.ts";
import type { FileSystem } from "../../../core/src/frontend.ts";

/** A program of this test's own, so what it counts is what it caused. A root that
 *  includes a library is what the dependency cases need: one unit on its own
 *  cannot show that a change reaches the units that name it. */
const ROOT = "build-test/demo/root.kh";
const LIBRARY = "build-test/demo/library.kh";
const BUILD_ROOT = "modules/khayyam/targets/js/build";
const SCRATCH = `${BUILD_ROOT}/.cache-test`;

const at = (path: string): string => fileURLToPath(new URL(path, new URL("../../../../../", import.meta.url)));

const LIBRARY_SOURCE = [
  "tp Count cp {",
  "}",
  "",
  "tp Zero mt (self Count) () (value Count)",
  "",
  "tp Add mt (self Count) (a Count, b Count) (total Count)",
  "",
].join("\n");

const ROOT_SOURCE = [
  `tp Count in "${LIBRARY}"`,
  "",
  "tp Program cp {",
  "}",
  "",
  "tp Run mt (self Program) () () {",
  "    vr total Count",
  "    Count.Add(Count, Count)(total)",
  "}",
  "",
].join("\n");

const SOURCES: Record<string, string> = {
  [LIBRARY]: LIBRARY_SOURCE,
  [ROOT]: ROOT_SOURCE,
};

const linkMapSource = readFileSync(new URL("../link_map.json", import.meta.url), "utf8");
const map = readLinkMap(linkMapSource);
assert.equal(map.ok, true, map.ok ? "" : map.problems.join("; "));
if (!map.ok) throw new Error("the repository's map is not a map");
const links: LinkMap = map.map;

function read(path: string): string | undefined {
  try {
    return readFileSync(at(path), "utf8");
  } catch {
    return undefined;
  }
}

function write(path: string, text: string): void {
  mkdirSync(dirname(at(path)), { recursive: true });
  writeFileSync(at(path), text, "utf8");
}

interface Run {
  compiled: string[];
  reused: string[];
  written: string[];
}

function once(
  sources: Record<string, string>,
  linkMap = linkMapSource,
  versions?: { frontend: string; representation: string; backend: string },
): Run {
  const files: FileSystem = { read: (path) => sources[path] };
  const written: string[] = [];
  const environment: BuildEnvironment = {
    cache: {
      load: (uri) => {
        const stored = read(`${SCRATCH}/cache/${uri.replace(/\//g, "_")}.json`);
        return stored === undefined ? undefined : (JSON.parse(stored) as UnitRecord);
      },
      save: (record) =>
        write(`${SCRATCH}/cache/${record.uri.replace(/\//g, "_")}.json`, JSON.stringify(record)),
    },
    sourceOf: (uri) => sources[uri],
    write: (path, text) => {
      written.push(path);
      write(path.replace(BUILD_ROOT, SCRATCH), text);
    },
    currentText: (path) => read(path.replace(BUILD_ROOT, SCRATCH)),
    buildRoot: BUILD_ROOT,
    host: "test",
    linkMap,
    ...(versions === undefined ? {} : { versions }),
  };
  const report = build({ root: ROOT, files, links, buildRoot: BUILD_ROOT }, environment);
  assert.equal(report.result.ok, true, report.result.ok ? "" : report.result.problem);
  return {
    compiled: report.compiled,
    reused: report.reused,
    written: written.map((path) => path.replace(`${SCRATCH}/`, "")),
  };
}

// The scratch holds what a previous run of this file left, and a build that
// changed nothing must not be measured against it.
rmSync(at(SCRATCH), { recursive: true, force: true });

test("the first build compiles every unit and writes every artifact beside the manifest", () => {
  const first = once(SOURCES);
  assert.deepEqual(first.compiled, [LIBRARY, ROOT]);
  assert.deepEqual(first.reused, []);
  assert.deepEqual(first.written.sort(), [
    `${BUILD_ROOT}/build-test/demo/library.js`,
    `${BUILD_ROOT}/build-test/demo/root.js`,
    `${BUILD_ROOT}/manifest.json`,
  ]);
});

test("a second build over unchanged sources compiles nothing", () => {
  once(SOURCES);
  const second = once(SOURCES);
  assert.deepEqual(second.compiled, []);
  assert.deepEqual(second.reused, [LIBRARY, ROOT]);
  assert.deepEqual(second.written, []);
});

test("a change to one file compiles that file and the units that name it, and no other", () => {
  once(SOURCES);
  const changed = {
    ...SOURCES,
    [LIBRARY]: `${LIBRARY_SOURCE}\ntp Sub mt (self Count) (a Count, b Count) (difference Count)\n`,
  };
  const second = once(changed);
  // The library changed, so it and the program that names it are compiled again;
  // the program's own artifact did not move, so only the library's is written.
  assert.deepEqual(second.compiled, [LIBRARY, ROOT]);
  assert.deepEqual(second.reused, []);
  assert.deepEqual(second.written, [`${BUILD_ROOT}/${LIBRARY.replace(/\.kh$/, ".js")}`]);
});

test("a change that does not move an artifact writes nothing", () => {
  once(SOURCES);
  // A comment is this toolchain's own rule, and a line of it changes no artifact.
  const second = once({ ...SOURCES, [LIBRARY]: `${LIBRARY_SOURCE}\n// a line the comment rule allows\n` });
  assert.deepEqual(second.compiled, [LIBRARY, ROOT]);
  assert.deepEqual(second.written, []);
});

test("a change to the map's own text reaches every unit", () => {
  once(SOURCES);
  const second = once(SOURCES, `${linkMapSource}\n`);
  assert.deepEqual(second.compiled, [LIBRARY, ROOT]);
  assert.deepEqual(second.reused, []);
});

test("a change to a version of this toolchain reaches every unit", () => {
  once(SOURCES);
  const second = once(SOURCES, linkMapSource, {
    frontend: VERSIONS.frontend,
    representation: VERSIONS.representation,
    backend: "khayyam-js-backend-2",
  });
  assert.deepEqual(second.compiled, [LIBRARY, ROOT]);
  assert.deepEqual(second.reused, []);
});

test("a key carries the source, the versions, the environment, and the units it names", () => {
  const base = keyOf("hash", { host: "node", linkMap: "{}" }, ["a", "b"]);
  assert.notEqual(base, keyOf("other", { host: "node", linkMap: "{}" }, ["a", "b"]));
  assert.notEqual(base, keyOf("hash", { host: "browser", linkMap: "{}" }, ["a", "b"]));
  assert.notEqual(base, keyOf("hash", { host: "node", linkMap: "{ }" }, ["a", "b"]));
  assert.notEqual(base, keyOf("hash", { host: "node", linkMap: "{}" }, ["a", "c"]));
  assert.notEqual(base, keyOf("hash", { host: "node", linkMap: "{}" }, ["b", "a"]));
  assert.notEqual(
    base,
    keyOf("hash", { host: "node", linkMap: "{}", versions: { ...VERSIONS, backend: "other" } }, ["a", "b"]),
  );
});
