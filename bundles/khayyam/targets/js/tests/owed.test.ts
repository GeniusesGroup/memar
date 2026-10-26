/* For license and copyright information please see the LEGAL file in the code repository */

// One pending Test per capability the plan still lists as owed
// (modules/process/test/test.practice.md#the-cycle → Pending). Each title carries
// `owed:<id>`, the identifier the document's `Owed: <id>` line carries
// (modules/knowledge/documentation/documentation.md → Owed or planned capability), and each is `todo`: it
// still runs, and a todo that passes is the runner telling a reader that the
// document's mark is stale. A Test here states the plan's own "done when" for its
// goal (bundles/khayyam/khayyam.handoff.md → The goals, in the order they come),
// in memory, so that none of them writes the build folder the other tests share.
// A Test here that passes loses its `owed:` mark and its `todo` in the same change
// as the document loses its `Owed:` line, and stays here as its goal's record.

import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

import { build, type BuildEnvironment, type UnitRecord } from "../src/cache.ts";
import { emitUnit } from "../src/emit.ts";
import { checkLinks, readLinkMap } from "../src/link.ts";
import { compileProgram } from "../src/program.ts";
import { run } from "../src/run.ts";
import type { FileSystem } from "../../../core/src/frontend.ts";

const REPOSITORY = new URL("../../../../../", import.meta.url);
const DEMO = "bundles/khayyam/targets/js/demo/greeting.kh";

const repository: FileSystem = {
  read: (path) => {
    try {
      return readFileSync(new URL(path, REPOSITORY), "utf8");
    } catch {
      return undefined;
    }
  },
};

const linkMapSource = readFileSync(new URL("../link_map.json", import.meta.url), "utf8");

test("a .kh program that needs no library control flow compiles to an ES module that runs", async () => {
  const map = readLinkMap(linkMapSource);
  assert.equal(map.ok, true);
  if (!map.ok) return;
  const compiled = compileProgram({ root: DEMO, files: repository, links: map.map, buildRoot: "build" });
  assert.equal(compiled.ok, true, compiled.ok ? "" : compiled.problem);
  if (!compiled.ok) return;
  const module = (await import(
    `data:text/javascript,${encodeURIComponent(emitUnit(compiled.program, DEMO))}`
  )) as Record<string, unknown>;
  const said: string[] = [];
  (module["supply"] as (implementations: Record<string, unknown>) => void)({
    "Greeter$Announce": () => said.push("announced"),
    "Text$Print": (self: { text: { value: string } }) => said.push(self.text.value),
  });
  const Text = module["Text"] as new (values: Record<string, unknown>) => unknown;
  const Greeter = module["Greeter"] as new (values: Record<string, unknown>) => unknown;
  const greeter = new Greeter({});
  (module["Greeter$Greet"] as (owner: unknown, greeting: unknown) => void)(
    greeter,
    { value: new Text({ text: "Hello, Khayyam" }) },
  );
  assert.deepEqual(said, ["announced", "Hello, Khayyam"]);
});

test("owed:khayyam.library-link-map every entry of the URI to JS-module map resolves and a program using library control flow runs", { todo: true }, () => {
  const map = readLinkMap(linkMapSource);
  assert.equal(map.ok, true);
  if (!map.ok) return;
  // An empty map resolves trivially, so the goal is not met by it: the map has to
  // hold entries, and each has to resolve against the protocol it names.
  assert.ok(Object.keys(map.map).length > 0, "the map holds no entry");
  assert.deepEqual(checkLinks(map.map, repository), []);
});

test("a page takes a .kh file, compiles it in the browser, and shows its output", async () => {
  // The page itself is driven by browser.check.ts, which needs an installed
  // browser (target.md → Compiling in a browser). What is checked here is what that
  // section promises of the page and of what it loads: the page takes a file and
  // text, it reaches the compiler the build step wrote rather than the one artifact
  // the Node build left beside it, the modules the build step takes in reach no
  // `node:` import, and the page's host glue compiles the demo and runs it.
  const PAGE = "bundles/khayyam/targets/js/demo/compile.html";
  const page = repository.read(PAGE);
  assert.notEqual(page, undefined, `${PAGE} is not there`);
  if (page === undefined) return;
  assert.match(page, /<input[^>]*type=["']file["']/i, "the page takes no file");
  assert.match(page, /<textarea/i, "the page takes no text");
  assert.doesNotMatch(page, /build\/manifest\.json/, "the page loads a prebuilt artifact");
  assert.match(page, /build\/compiler\/targets\/js\/src\/program\.js/, "the page does not load the compiler the build step wrote");

  const configText = repository.read("bundles/khayyam/targets/js/tsconfig.browser.json");
  assert.notEqual(configText, undefined, "the build step's configuration is not there");
  if (configText === undefined) return;
  const config = JSON.parse(configText) as { files: string[] };
  const reached = new Set<string>();
  const pending = config.files.map((file) => new URL(file, new URL("../tsconfig.browser.json", import.meta.url)).href);
  while (pending.length > 0) {
    const at = pending.pop()!;
    if (reached.has(at)) continue;
    reached.add(at);
    const text = readFileSync(new URL(at), "utf8");
    for (const match of text.matchAll(/(?:^|\n)\s*(?:import|export)\b[^"';]*?from\s+"([^"]+)"/g)) {
      const specifier = match[1]!;
      assert.ok(specifier.startsWith("."), `${at} imports ${specifier}, which is not one of the compiler's own modules`);
      pending.push(new URL(specifier, at).href);
    }
  }
  assert.ok(reached.size > config.files.length, "the build step takes in nothing its entry modules import");

  const host = await import("../demo/page-host.ts");
  const compiled = host.compileUnits({
    compiler: { compileProgram, emitUnit, readLinkMap },
    units: [{ uri: DEMO, source: repository.read(DEMO) ?? "" }],
    linkMap: linkMapSource,
    buildRoot: "build",
  });
  assert.equal(compiled.ok, true, compiled.ok ? "" : compiled.problem);
  if (!compiled.ok) return;
  const said: string[] = [];
  const load = host.loaderOf({
    program: compiled.program,
    texts: compiled.texts,
    urlOf: (text: string) => `data:text/javascript,${encodeURIComponent(text)}`,
  });
  const { Text } = (await load(DEMO)) as { Text: new (values: Record<string, unknown>) => unknown };
  await run(
    {
      uri: DEMO,
      units: [DEMO],
      method: "Greet",
      owner: { type: "Greeter" },
      influencing: [new Text({ text: "Hello, Khayyam" })],
      supplied: {
        [DEMO]: {
          "Greeter$Announce": () => void said.push("The host says hello."),
          "Text$Print": (self: unknown) => void said.push((self as { text: { value: string } }).text.value),
        },
      },
    },
    load,
  );
  assert.deepEqual(said, ["The host says hello.", "Hello, Khayyam"]);
});

test("unchanged work is not repeated, and a changed version invalidates every entry", () => {
  const sources: Record<string, string> = {
    "a/lib.kh": "tp Count cp {\n}\n",
    "a/root.kh": 'tp Count in "a/lib.kh"\n\ntp Program cp {\n}\n',
  };
  const stored = new Map<string, string>();
  const run = (text: Record<string, string>, backend = "v1") => {
    const environment: BuildEnvironment = {
      cache: {
        load: (uri) => {
          const record = stored.get(`cache/${uri}`);
          return record === undefined ? undefined : (JSON.parse(record) as UnitRecord);
        },
        save: (record) => void stored.set(`cache/${record.uri}`, JSON.stringify(record)),
      },
      sourceOf: (uri) => text[uri],
      write: (path, body) => void stored.set(path, body),
      currentText: (path) => stored.get(path),
      buildRoot: "build",
      host: "test",
      linkMap: "{}",
      versions: { frontend: "f1", representation: "r1", backend },
    };
    const report = build({ root: "a/root.kh", files: { read: (path) => text[path] }, links: {}, buildRoot: "build" }, environment);
    assert.equal(report.result.ok, true, report.result.ok ? "" : report.result.problem);
    return report;
  };
  run(sources);
  assert.deepEqual(run(sources).compiled, [], "a second build compiled something");
  assert.deepEqual(
    run({ ...sources, "a/lib.kh": "tp Count cp {\n}\n\ntp Other cp {\n}\n" }).compiled,
    ["a/lib.kh", "a/root.kh"],
    "a change to one file reaches that file and the unit that names it",
  );
  assert.deepEqual(run(sources, "v2").reused, [], "a changed backend left an entry in use");
});
