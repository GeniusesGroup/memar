import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

import { compileProgram, emitUnit } from "../src/program.ts";
import { readLinkMap } from "../src/link.ts";
import type { FileSystem } from "../../../core/src/frontend.ts";

/** The repository, read through its root: a URI is written from the repository
 *  root (modules/khayyam/rules/import-address/import-address.md). */
const REPOSITORY = new URL("../../../../../", import.meta.url);
const BUILD_ROOT = "modules/khayyam/targets/js/build";
const PROBES = "modules/khayyam/targets/js/bootstrap";

const files: FileSystem = {
  read: (path) => {
    try {
      return readFileSync(new URL(path, REPOSITORY), "utf8");
    } catch {
      return undefined;
    }
  },
};

function compiles(name: string): { ok: true; artifact: string } | { ok: false; problem: string } {
  const source = readFileSync(new URL("../link_map.json", import.meta.url), "utf8");
  const map = readLinkMap(source);
  assert.equal(map.ok, true, map.ok ? "" : map.problems.join("; "));
  if (!map.ok) throw new Error("the map is not a map");
  const uri = `${PROBES}/${name}.kh`;
  const compiled = compileProgram({ root: uri, files, links: map.map, buildRoot: BUILD_ROOT });
  if (!compiled.ok) return { ok: false, problem: compiled.problem };
  return { ok: true, artifact: emitUnit(compiled.program, uri) };
}

test("a program can already do what this target's libraries are made of", () => {
  const result = compiles("compose");
  assert.equal(result.ok, true, result.ok ? "" : result.problem);
  if (!result.ok) return;
  // A scope, a driver naming it, a call that carries a value in and receives what
  // the call wrote into a slot, and an early return: the four things a body holds.
  assert.match(result.artifact, /function \$Then\$\(\)/);
  assert.match(result.artifact, /Text\$Print\(self\);/);
  assert.match(result.artifact, /const askedText\$ = \{ value: undefined \};/);
  assert.match(result.artifact, /Text\$Ask\(self, what\$, askedText\$\);/);
  assert.match(result.artifact, /return;/);
});

test("a program's own code cannot reach a character of a text it holds", () => {
  // Nothing is refused here, and that is the finding. The unit reads, the body
  // is a call, and what the text holds is decided outside â€” so the only route to
  // a character is a method with no body, which the language's link form exists
  // to arrange.
  const result = compiles("character");
  assert.equal(result.ok, true, result.ok ? "" : result.problem);
  if (!result.ok) return;
  assert.match(result.artifact, /const at\$ = at;/);
  assert.match(result.artifact, /return \$supplied\["Text\$CharacterAt"\]\(self, at\$, character\$\);/);
});

test("a program cannot make the value a method was asked to produce", () => {
  // `Fresh` does everything a body can do with creation: declare the slot, and
  // call a method that writes it. What fills the slot is still the host's.
  const result = compiles("construct");
  assert.equal(result.ok, true, result.ok ? "" : result.problem);
  if (!result.ok) return;
  assert.match(result.artifact, /const made\$ = \{ value: undefined \};/);
  assert.match(result.artifact, /Holder\$Make\(self, made\$\);/);
  assert.match(result.artifact, /return \$supplied\["Holder\$Fill"\]\(self, count\$\);/);
});

test("a field is a variable: a method reaches its own capsule's field and calls on what it holds", () => {
  const result = compiles("state");
  assert.equal(result.ok, true, result.ok ? "" : result.problem);
  if (!result.ok) return;
  // The slot is the language's, and what is in it is the host's: the field is a
  // cell the constructor fills from the values a host hands over.
  assert.match(result.artifact, /this\.position = \{ value: values === undefined \? undefined : values\.position \};/);
  assert.match(result.artifact, /Count\$Increment\(self\.position\.value, step\$\);/);
});

test("a call cannot be given a field to write, which is the rule this level holds open", () => {
  const result = compiles("write-field");
  assert.equal(result.ok, false, result.ok ? "accepted" : "");
  if (result.ok) return;
  assert.match(
    result.problem,
    /self\.position: a call cannot influence a field: what a call writes is a name the body binds/,
  );
});

test("a method can be a parameter, and no unit can declare the type that holds it", () => {
  const result = compiles("behaviour");
  assert.equal(result.ok, false, result.ok ? "accepted" : "");
  if (result.ok) return;
  assert.equal(result.problem, `${PROBES}/behaviour.kh is refused: unbound-type-name`);
});

test("a body has no form that repeats a command", () => {
  const result = compiles("repeat");
  assert.equal(result.ok, true, result.ok ? "" : result.problem);
  if (!result.ok) return;
  // The probe's only command is a scope, so what it can drive is nothing: there
  // is no repetition in the grammar, and the library that would supply it is the
  // jump this target's own control-flow unit is built on.
  assert.match(result.artifact, /function \$KeepGoing\$\(\)/);
  assert.doesNotMatch(result.artifact, /^\s+\$KeepGoing\$\(/m);
});
