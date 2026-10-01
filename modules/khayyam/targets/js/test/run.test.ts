import assert from "node:assert/strict";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";
import { spawnSync } from "node:child_process";
import test from "node:test";
import { fileURLToPath } from "node:url";

import { build, type BuildEnvironment } from "../src/cache.ts";
import { compileProgram } from "../src/program.ts";
import { emitUnit } from "../src/emit.ts";
import { readLinkMap, type LinkMap } from "../src/link.ts";
import type { FileSystem } from "../../../core/src/frontend.ts";

/** The repository, read through its root: a URI is written from the repository
 *  root, so that is the base a build resolves one at
 *  (modules/khayyam/rules/import-address/import-address.md). */
const REPOSITORY = new URL("../../../../../", import.meta.url);
const TARGET = new URL("../", import.meta.url);
const BUILD_ROOT = "modules/khayyam/targets/js/build";

const files: FileSystem = {
  read: (path) => {
    try {
      return readFileSync(new URL(path, REPOSITORY), "utf8");
    } catch {
      return undefined;
    }
  },
};

const write = (path: string, text: string): void => {
  const target = new URL(path, REPOSITORY);
  mkdirSync(dirname(fileURLToPath(target)), { recursive: true });
  writeFileSync(target, text, "utf8");
};

const DEMO = "modules/khayyam/targets/js/demo/greeting.kh";

function compile(): ReturnType<typeof compileProgram> {
  const source = readFileSync(new URL("../link_map.json", import.meta.url), "utf8");
  const map = readLinkMap(source);
  assert.equal(map.ok, true, map.ok ? "" : map.problems.join("; "));
  if (!map.ok) throw new Error("the map is not a map");
  return compileProgram({ root: DEMO, files, links: map.map, buildRoot: BUILD_ROOT });
}

function linksOf(compilation: ReturnType<typeof compileProgram>): LinkMap {
  const source = readFileSync(new URL("../link_map.json", import.meta.url), "utf8");
  const map = readLinkMap(source);
  assert.equal(map.ok, true, map.ok ? "" : map.problems.join("; "));
  if (!map.ok) throw new Error("the map is not a map");
  return map.map;
}

const environment: BuildEnvironment = {
  cache: { load: () => undefined, save: () => undefined },
  sourceOf: files.read,
  write,
  currentText: (path) => files.read(path),
  buildRoot: BUILD_ROOT,
  host: "test",
  linkMap: readFileSync(new URL("../link_map.json", import.meta.url), "utf8"),
};

const compiled = compile();

test("the demo program compiles on its own: one unit, and the host supplies what it does not declare", () => {
  assert.equal(compiled.ok, true, compiled.ok ? "" : compiled.problem);
  if (!compiled.ok) return;
  assert.deepEqual(
    compiled.program.units.map((unit) => `${unit.origin} ${unit.uri}`),
    [`compiled ${DEMO}`],
  );
});

test("a build writes the artifact and names where the unit's code stands", () => {
  assert.equal(compiled.ok, true);
  if (!compiled.ok) return;
  const report = build(
    { root: DEMO, files, links: compile().ok ? linksOf(compile()) : {}, buildRoot: BUILD_ROOT },
    environment,
  );
  assert.equal(report.result.ok, true, report.result.ok ? "" : report.result.problem);
  assert.deepEqual(report.compiled, [DEMO]);
  const manifest = JSON.parse(
    readFileSync(new URL(`${BUILD_ROOT}/manifest.json`, REPOSITORY), "utf8"),
  ) as { root: string; units: Record<string, string> };
  assert.equal(manifest.root, DEMO);
  assert.equal(manifest.units[DEMO], `${BUILD_ROOT}/modules/khayyam/targets/js/demo/greeting.js`);
  // The two methods the program declares without a body reach the host's table,
  // and the one it declares with a body is compiled into the artifact.
  const artifact = readFileSync(
    new URL(`${BUILD_ROOT}/modules/khayyam/targets/js/demo/greeting.js`, REPOSITORY),
    "utf8",
  );
  assert.match(artifact, /return \$supplied\["Greeter\$Announce"\]\(self\);/);
  assert.match(artifact, /Greeter\$Greet\$Print|function Greeter\$Greet/);
});

test("the artifact of the program runs under Node", () => {
  const result = spawnSync(process.execPath, [fileURLToPath(new URL("demo/node-host.js", TARGET))], {
    encoding: "utf8",
  });
  assert.equal(result.status, 0, result.stderr);
  assert.equal(result.stdout, "The host says hello.\nHello, Khayyam\n");
});

/** The shape the owner's ruling names: a capsule's own method hands its field to
 *  the method that writes it, and no method is given a field to write. It is here
 *  rather than in a probe because a probe can only show that it compiles, and what
 *  has to be shown is that the write lands. */
const CURSOR = [
  "tp Count cp {",
  "}",
  "",
  "tp Store mt (self Cursor) (value Count) (stored Count)",
  "",
  "tp Cursor cp {",
  "    position Count",
  "}",
  "",
  "tp Bump mt (self Cursor) (step Count) (moved Count) {",
  "    self.Store(step)(step)",
  "}",
  "",
  "tp Move mt (self Cursor) (step Count) (moved Count) {",
  "    self.Bump(self.position, step)()",
  "}",
  "",
].join("\n");

test("a capsule's own method hands its field to the method that writes it, and the field changes", async () => {
  const uri = "demo/cursor.kh";
  const result = compileProgram({
    root: uri,
    files: { read: (path) => (path === uri ? CURSOR : undefined) },
    links: {},
    buildRoot: "build",
  });
  assert.equal(result.ok, true, result.ok ? "" : result.problem);
  if (!result.ok) return;
  const artifact = emitUnit(result.program, uri);
  // The field is handed over as the slot it is, not as what is in it, which is
  // the whole of what makes the write land.
  assert.match(artifact, /Cursor\$Bump\(self, self\.position, step\$\);/);
  const module = (await import(
    `data:text/javascript,${encodeURIComponent(artifact)}`
  )) as Record<string, unknown>;
  const Cursor = module["Cursor"] as new (values: Record<string, unknown>) => {
    position: { value: unknown };
  };
  // The one method the host supplies is the one that writes: the language owns
  // the shape of the call and the slot it is given, and the host writes through it.
  (module["supply"] as (implementations: Record<string, unknown>) => void)({
    "Cursor$Store": (_self: unknown, _value: { value: unknown }, stored: { value: unknown }) => {
      stored.value = 2;
    },
  });
  const before = { at: 1 };
  const cursor = new Cursor({ position: before });
  (module["Cursor$Move"] as (owner: unknown, step: unknown) => void)(
    cursor,
    { value: 2 },
  );
  assert.equal(cursor.position.value, 2, "the field the method was handed is the field it changed");
  assert.notEqual(cursor.position.value, before, "and it is not the value it held before");
});
