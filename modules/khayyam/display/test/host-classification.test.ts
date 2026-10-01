// A role's kind, judged against the host's own registered list.
//
// A kind is not a matter of taste and not a matter of memory: it is whatever the host
// registers, and that list is read out of the installed product's own bundle rather
// than written here, because a list written here is a list that can agree with a wrong
// contract. The four tests below are the four ways a role's `kind` can fail to say
// what kind of thing the name is, or to say it for a type the host does not have.
import assert from "node:assert/strict";
import { existsSync, readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";
import test from "node:test";
import { contractWith } from "./provoke.ts";
import { CONTRACT, roleNamed } from "./shipped.ts";
import { run } from "./the-check.ts";

/** The host's own bundle, found the way the check finds it. The kinds are read out of
 *  the product, not out of a list written here, because a list written here is a list
 *  that can agree with a wrong contract. */
const HOST_CANDIDATES = [
  join(process.env.LOCALAPPDATA ?? "", "Programs", "Microsoft VS Code", "resources", "app", "out"),
  join(process.env.LOCALAPPDATA ?? "", "Programs", "Microsoft VS Code"),
  join(process.env.ProgramFiles ?? "", "Microsoft VS Code", "resources", "app", "out"),
  join(process.env.ProgramFiles ?? "", "Microsoft VS Code"),
  join(process.env["ProgramFiles(x86)"] ?? "", "Microsoft VS Code", "resources", "app", "out"),
];

function hostBundle(): string | undefined {
  if (process.env.KHAYYAM_HOST_BUNDLE && existsSync(process.env.KHAYYAM_HOST_BUNDLE))
    return process.env.KHAYYAM_HOST_BUNDLE;
  for (const root of HOST_CANDIDATES) {
    const flat = join(root, "vs", "workbench", "workbench.desktop.main.js");
    if (existsSync(flat)) return flat;
    if (!existsSync(root)) continue;
    for (const entry of readdirSync(root, { withFileTypes: true })) {
      if (!entry.isDirectory()) continue;
      const nested = join(root, entry.name, "resources", "app", "out", "vs", "workbench", "workbench.desktop.main.js");
      if (existsSync(nested)) return nested;
    }
  }
  return undefined;
}

test("the kinds are the host's own registered types, read out of the host's bundle", () => {
  // `function T4n()` in the bundle is the host registering its own classification at
  // load: twenty-four `registerTokenType` calls and eight `registerTokenModifier` calls.
  // Every `kind.standardType` this contract names has to be one of the twenty-four, and
  // the count is checked so a parse that silently found nothing cannot pass.
  const bundle = hostBundle();
  assert.ok(bundle, `the host's bundle was not found; set KHAYYAM_HOST_BUNDLE. Looked in:\n${HOST_CANDIDATES.join("\n")}`);
  const source = readFileSync(bundle, "utf8");
  // `function T4n()` registers through a local helper, so the calls read `o("id",<description>,<scopes>,<superType>)`.
  const registered = [...source.matchAll(/o\("([^"]+)",\w+\(\d+,null\),(\[\[.*?\]\]|\[\]|void 0)(?:,("(?:[^"]*)"|void 0))?/g)].map(
    (m) => m[1],
  );
  const modifiers = [...source.matchAll(/registerTokenModifier\("([^"]+)"/g)].map((m) => m[1]);
  assert.equal(new Set(registered).size, 24, `the host's registered list did not parse as 24 types, from ${bundle}`);
  assert.equal(modifiers.length, 8, `the host's registered modifier list did not parse as 8, from ${bundle}`);

  const contract = JSON.parse(readFileSync(CONTRACT, "utf8"));
  const named = contract.roles.filter((role: any) => role.kind?.standardType);
  for (const role of named)
    assert.ok(
      registered.includes(role.kind.standardType),
      `'${role.name}' names a kind '${role.kind.standardType}' the host does not register`,
    );
  const verdict = run();
  assert.equal(verdict.status, 0, `the check refused something:\n${verdict.refusals.join("\n")}`);
  assert.match(verdict.out, /24 registered token types/);
});

test("a role whose kind names a type the host does not register is refused", () => {
  const path = contractWith((contract) => {
    roleNamed(contract, "capsule").kind = { standardType: "record", statement: "a claim about nothing the host knows" };
  });
  const verdict = run(path);
  assert.equal(verdict.status, 1, "a kind the host does not register cannot pass");
  assert.ok(
    verdict.refusals.includes(
      "contract: role 'capsule' names the kind 'record', which the host does not register: a kind is the host's own " +
        "standard type, read out of the product's own bundle, and 'record' is not among the 24 it registers",
    ),
    `the unknown kind was not among what was refused:\n${verdict.refusals.join("\n")}\n${verdict.out}`,
  );
});

test("a role that states no kind at all is refused, and so is one that states two answers", () => {
  const silent = contractWith((contract) => delete roleNamed(contract, "variable").kind);
  const nameless = run(silent);
  assert.equal(nameless.status, 1);
  assert.equal(
    nameless.refusals[0],
    "contract: role 'variable' states no kind, so nothing says what kind of thing the name is; a role states the " +
      "host's own standard type it is a kind of, or that it is this language's own root with no standard counterpart",
  );
  const both = contractWith((contract) => {
    roleNamed(contract, "scope").kind.standardType = "type";
  });
  const contradicted = run(both);
  assert.equal(contradicted.status, 1);
  assert.equal(
    contradicted.refusals[0],
    "contract: role 'scope' states itself a root and also names the standard type 'type': a root is a kind the host " +
      "has no counterpart for, and a role that is both is neither",
  );
});

test("a root that does not say why is refused, and a non-root that gives no standard type is refused", () => {
  const silent = contractWith((contract) => delete roleNamed(contract, "scope").kind.because);
  const nameless = run(silent);
  assert.equal(nameless.status, 1);
  assert.equal(
    nameless.refusals[0],
    "contract: role 'scope' is declared a root and does not say why: 'because' is the one place a reader is told what " +
      "this language adds to the host's vocabulary, so the reason is not optional",
  );
  const missing = contractWith((contract) => delete roleNamed(contract, "type-reference").kind.standardType);
  const unstated = run(missing);
  assert.equal(unstated.status, 1);
  assert.equal(
    unstated.refusals[0],
    "contract: role 'type-reference' states neither a root nor a standard type, so nothing says what kind of thing the " +
      "name is",
  );
});
