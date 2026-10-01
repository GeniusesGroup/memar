/** The host side of the demo, on Node. It compiles
 *  `modules/khayyam/targets/js/demo/greeting.kh` to artifacts, supplies the one
 *  body-less method the program stands on, and runs one entry of it. Entry and
 *  lifecycle are this file's configuration, not the language's
 *  (docs/protocols/compiler.md → Entry and lifecycle are not grammar).
 *
 *  What the host supplies is the behaviour, and nothing else: a body-less method
 *  on a concrete capsule is the language's own signal that the implementation
 *  comes from the link phase. Where a library over that mechanism belongs is not
 *  this folder's business — the control-flow concept is modelled at
 *  `modules/process/control-flow/model.md`, and nothing is written here until the
 *  questions that model raises are answered.
 *
 *  Run it with `node demo/node-host.js`; pass `--what-changed` to see what the
 *  build compiled, stood in for, and wrote. */

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";
import { fileURLToPath } from "node:url";

import { build, pathsOf } from "../src/cache.ts";
import { readLinkMap } from "../src/link.ts";
import { run } from "../src/run.ts";

const REPOSITORY = new URL("../../../../../", import.meta.url);
const BUILD_ROOT = "modules/khayyam/targets/js/build";
const DEMO = "modules/khayyam/targets/js/demo/greeting.kh";

const read = (path) => {
  try {
    return readFileSync(new URL(path, REPOSITORY), "utf8");
  } catch {
    return undefined;
  }
};

const write = (path, text) => {
  const target = new URL(path, REPOSITORY);
  mkdirSync(dirname(fileURLToPath(target)), { recursive: true });
  writeFileSync(target, text, "utf8");
};

const linkMap = read("modules/khayyam/targets/js/link_map.json") ?? "";
const map = readLinkMap(linkMap);
if (!map.ok) {
  console.error(`the link map is not a map: ${map.problems.join("; ")}`);
  process.exit(1);
}

const report = build(
  { root: DEMO, files: { read }, links: map.map, buildRoot: BUILD_ROOT },
  {
    cache: {
      load: (uri) => {
        const stored = read(`${BUILD_ROOT}/.cache/${uri.replace(/\//g, "_")}.json`);
        return stored === undefined ? undefined : JSON.parse(stored);
      },
      save: (record) =>
        write(`${BUILD_ROOT}/.cache/${record.uri.replace(/\//g, "_")}.json`, JSON.stringify(record)),
    },
    sourceOf: read,
    write,
    currentText: read,
    buildRoot: BUILD_ROOT,
    host: "node",
    linkMap,
  },
);
if (!report.result.ok) {
  console.error(`the program is refused: ${report.result.problem}`);
  process.exit(1);
}
if (process.argv.includes("--what-changed")) {
  console.error(`compiled: ${report.compiled.join(", ") || "nothing"}`);
  console.error(`stood in for: ${report.reused.join(", ") || "nothing"}`);
  console.error(`written: ${report.written.join(", ") || "nothing"}`);
}

const paths = pathsOf(report.result.program);
const urlOf = (path) => new URL(path, REPOSITORY).href;
const load = (uri) => import(urlOf(paths[uri]));

const { Text } = await load(DEMO);
// A field is a variable, so a host hands the value over and the capsule holds the
// slot: what the language owns is the slot, and what a host creates is the value
// (docs/khayyam/khayyam.md → Separation of Syntax and Governance).
const greeting = new Text({ text: "Hello, Khayyam" });

await run(
  {
    uri: DEMO,
    units: [DEMO],
    method: "Greet",
    owner: { type: "Greeter" },
    influencing: [greeting],
    supplied: {
      [DEMO]: {
        "Greeter$Announce": () => {
          console.log("The host says hello.");
        },
        "Text$Print": (self) => {
          console.log(self.text.value);
        },
      },
    },
  },
  load,
);
