// What the manifest contributes, and what it may not contribute.
//
// The manifest is the one file that hands the editor its values, so every entry of its
// `contributes` block is a claim about the contract and is judged against it here: the
// colour rules keyed by a role's own name, the super types that carry a role's kind to
// the host, and the three fields by which a theme is identified to a reader. The bridge
// is the one contribution that is refused rather than checked, because it decides the
// value for every reader whose theme is not ours.
import assert from "node:assert/strict";
import { readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import test from "node:test";
import { manifestWith, themeIn, themesRoot } from "./provoke.ts";
import { CONTRACT, EXTENSION, MANIFEST, THEMES } from "./shipped.ts";
import { run } from "./the-check.ts";

test("a manifest that contributes a bridge is refused, and the refusal names the roles it claims", () => {
  // The bridge is the one contribution that would let a host's theme overwrite a value
  // the contract states, so its presence is the defect rather than a missing value.
  const copy = manifestWith((manifest) => {
    manifest.contributes.semanticTokenScopes = [
      { language: "khayyam", scopes: { "method-argument": ["variable.parameter.khayyam"] } },
    ];
  });
  const verdict = run(CONTRACT, copy);
  assert.equal(verdict.status, 1, "a manifest that offers a bridge cannot pass");
  assert.ok(
    verdict.refusals.some((line) => line.startsWith("package.json: contributes semanticTokenScopes for [method-argument],")),
    `the bridge was not among what was refused:\n${verdict.refusals.join("\n")}\n${verdict.out}`,
  );
});

test("a role the colour rules leave out is refused, and the message says the bridge is not there to style it", () => {
  // The colour rules are the only mechanism, so a role missing from them reaches no
  // colour of its own and a host discards its token before it can override the grammar.
  const copy = manifestWith((manifest) => {
    const rules = manifest.contributes.configurationDefaults["[khayyam]"][
      "editor.semanticTokenColorCustomizations"
    ].rules;
    delete rules["method-argument"];
  });
  const verdict = run(CONTRACT, copy);
  assert.equal(verdict.status, 1);
  assert.ok(
    verdict.refusals.includes(
      "package.json: the legend entry 'method-argument' keys no editor.semanticTokenColorCustomizations rule under " +
        "that spelling, so the token the server answers with it reaches no colour of its own, and the manifest " +
        "contributes no semanticTokenScopes that could style it",
    ),
    `the missing role was not among what was refused:\n${verdict.refusals.join("\n")}\n${verdict.out}`,
  );
});

test("a rule keyed a spelling of its own is refused, and so is the legend entry it should have keyed", () => {
  // The legend is read out of the server's own module, so the two sides are compared
  // rather than derived from each other: a check that rebuilt the legend would agree
  // with its own derivation. The refusal is stated from both ends on purpose - the
  // entry with no rule, and the rule with no entry - because either one alone is a
  // spelling that a later reader would have to guess at.
  const copy = manifestWith((manifest) => {
    const rules = manifest.contributes.configurationDefaults["[khayyam]"][
      "editor.semanticTokenColorCustomizations"
    ].rules;
    rules["method_argument"] = rules["method-argument"];
    delete rules["method-argument"];
  });
  const verdict = run(CONTRACT, copy);
  assert.equal(verdict.status, 1);
  assert.ok(
    verdict.refusals.includes(
      "package.json: the legend entry 'method-argument' keys no editor.semanticTokenColorCustomizations rule under " +
        "that spelling, so the token the server answers with it reaches no colour of its own, and the manifest " +
        "contributes no semanticTokenScopes that could style it",
    ),
    `the entry with no rule was not among what was refused:\n${verdict.refusals.join("\n")}\n${verdict.out}`,
  );
  assert.ok(
    verdict.refusals.includes(
      "package.json: editor.semanticTokenColorCustomizations.rules styles 'method_argument', which is no name in the " +
        "server's advertised legend",
    ),
    `the rule with no entry was not among what was refused:\n${verdict.refusals.join("\n")}\n${verdict.out}`,
  );
});

test("the manifest offers a dark and a light theme, each named by the fields the manifest itself carries", () => {
  // A theme is identified to a reader by three fields and by nothing else: the label the
  // picker shows, the uiTheme the picker marks it by, and the file the path names. All
  // three come from the manifest, so no other file in this repository has a name for a
  // theme and none of them can be right about one on its own.
  const manifest = JSON.parse(readFileSync(MANIFEST, "utf8"));
  const offered = manifest.contributes?.themes ?? [];
  assert.deepEqual(
    offered.map((theme: any) => theme.uiTheme).sort(),
    ["vs", "vs-dark"],
    "the manifest offers exactly one light theme and one dark theme, and nothing else",
  );
  const paths = new Set<string>();
  for (const theme of offered) {
    assert.equal(typeof theme.label, "string", "a theme the picker cannot name");
    assert.ok(theme.label.length > 0, "a theme the picker cannot name");
    assert.equal(typeof theme.path, "string", `${theme.label} names no file`);
    paths.add(theme.path);
    const file = JSON.parse(readFileSync(join(EXTENSION, theme.path), "utf8"));
    assert.equal(file.name, theme.label, `${theme.path} names '${file.name}' and the manifest offers '${theme.label}'`);
    assert.equal(
      file.type,
      theme.uiTheme === "vs-dark" ? "dark" : "light",
      `${theme.path} declares type '${file.type}' under a '${theme.uiTheme}' contribution`,
    );
  }
  assert.equal(paths.size, offered.length, "two contributions naming one file is one theme offered twice");
});

test("a contribution whose label, uiTheme or path disagrees with the file it names is refused", () => {
  // The three fields a theme is identified by are each a claim about the same file, and a
  // disagreement between two of them is a theme a reader sees under one name and as
  // another. The two-way count is the other direction of the same check: a theme file
  // nothing offers is a sheet no reader reaches.
  const copy = manifestWith((manifest) => {
    manifest.contributes.themes[0].label = "Khayyam";
  });
  const named = run(CONTRACT, copy);
  assert.equal(named.status, 1);
  assert.ok(
    named.refusals.includes(
      "package.json: contributes the theme 'Khayyam', but the file it points at is named 'Memar Dark'",
    ),
    `the label that names another theme was not among what was refused:\n${named.refusals.join("\n")}\n${named.out}`,
  );
  const light = manifestWith((manifest) => {
    manifest.contributes.themes[0].uiTheme = "vs";
  });
  const mislabelled = run(CONTRACT, light);
  assert.equal(mislabelled.status, 1);
  assert.ok(
    mislabelled.refusals.includes(
      "package.json: contributes the theme 'Memar Dark' as a 'vs' theme, but the file it points at is a 'dark' one",
    ),
    `the uiTheme that contradicts the file was not among what was refused:\n${mislabelled.refusals.join("\n")}\n${mislabelled.out}`,
  );
  const absent = manifestWith((manifest) => {
    manifest.contributes.themes[0].path = "./themes/khayyam-absent.json";
  });
  const missing = run(CONTRACT, absent);
  assert.equal(missing.status, 1);
  assert.ok(
    missing.refusals.includes(
      "package.json: contributes the theme 'Memar Dark', whose path './themes/khayyam-absent.json' names no file the " +
        "extension ships",
    ),
    `the path that names no file was not among what was refused:\n${missing.refusals.join("\n")}\n${missing.out}`,
  );
  const root = themesRoot();
  writeFileSync(join(root, "themes", "khayyam-third.json"), "{}\n");
  const unoffered = run(CONTRACT, MANIFEST, root);
  assert.equal(unoffered.status, 1);
  assert.ok(
    unoffered.refusals.includes(
      "package.json: ships the theme file 'khayyam-third.json', which no contributed theme offers and no offered " +
        "theme includes as its base, so its values reach no reader",
    ),
    `the theme file nothing offers was not among what was refused:\n${unoffered.refusals.join("\n")}\n${unoffered.out}`,
  );
});

test("a theme the picker would show under a name that is not Memar's is refused", () => {
  // The label is what a reader's picker shows, and the file's own `name` is what agrees
  // with it, so the two are renamed together here: what is being refused is the pair
  // agreeing on a name that does not say whose theme this is. A theme is Memar's, and a
  // reader who cannot tell that from the picker has been told nothing by it.
  const copy = manifestWith((manifest) => {
    manifest.contributes.themes[0].label = "Khayyam Dark";
  });
  const root = themesRoot();
  themeIn(root, "khayyam-dark.json", (theme) => {
    theme.name = "Khayyam Dark";
  });
  const verdict = run(CONTRACT, copy, root);
  assert.equal(verdict.status, 1);
  assert.ok(
    verdict.refusals.includes(
      "package.json: contributes the theme 'Khayyam Dark', which names no Memar theme; the label a reader's picker " +
        "shows is what says whose theme this is",
    ),
    `the theme named for something else was not among what was refused:\n${verdict.refusals.join("\n")}\n${verdict.out}`,
  );
});

test("a manifest that offers no theme at all is refused, and the refusal says where a value has left", () => {
  // A language-scoped configuration default is not a substitute: a host does not resolve
  // a semantic token's colour out of one, so a manifest without a theme leaves every role
  // resolved by nothing.
  const copy = manifestWith((manifest) => delete manifest.contributes.themes);
  const verdict = run(CONTRACT, copy);
  assert.equal(verdict.status, 1);
  assert.ok(
    verdict.refusals.some((line) => line.startsWith("package.json: contributes no theme, so no value the contract states")),
    `the manifest with no theme was not among what was refused:\n${verdict.refusals.join("\n")}\n${verdict.out}`,
  );
});

test("a colour rule that carries no value of its own is refused, and so is one holding another sheet's value", () => {
  // A rule the editor can resolve is not the same as a rule that resolves a STYLE: a rule
  // keyed by the role's own name with no foreground of its own matches the token and
  // gives it nothing, and the token is then discarded before it can override the grammar.
  // That is the shape the check has to refuse, because it looks exactly like a rule that
  // works - the legend entry is keyed, the selector matches, and nothing is drawn.
  const empty = manifestWith((manifest) => {
    const rules = manifest.contributes.configurationDefaults["[khayyam]"][
      "editor.semanticTokenColorCustomizations"
    ].rules;
    rules.keyword = {};
  });
  const blank = run(CONTRACT, empty);
  assert.equal(blank.status, 1);
  assert.ok(
    blank.refusals.includes(
      "package.json: the colour rule for 'keyword' carries no foreground, so a host resolves no style for that " +
        "token type and discards the token before it can override the grammar",
    ),
    `the value-less rule was not among what was refused:\n${blank.refusals.join("\n")}\n${blank.out}`,
  );
  const dark = JSON.parse(readFileSync(join(THEMES, "khayyam-dark.json"), "utf8")).khayyamDisplay["khayyam.keyword.color"];
  const foreign = manifestWith((manifest) => {
    const rules = manifest.contributes.configurationDefaults["[khayyam]"][
      "editor.semanticTokenColorCustomizations"
    ].rules;
    rules.keyword = { foreground: "#8CC05E" };
  });
  const wrong = run(CONTRACT, foreign);
  assert.equal(wrong.status, 1);
  assert.ok(
    wrong.refusals.includes(
      `package.json: the colour rule for 'keyword' is #8CC05E but khayyam-dark.json declares ${dark}`,
    ),
    `the other sheet's value was not among what was refused:\n${wrong.refusals.join("\n")}\n${wrong.out}`,
  );
});

test("the manifest declares one super type per role that has a kind, and none for a root or a collision", () => {
  // The declaration is the whole of what makes a reader's own rule for the standard
  // class reach our roles, so the two sides are counted against each other: every role
  // whose kind is a super type is declared with exactly that super type, and a role
  // that is a root - or whose own name IS the host's type for that kind - is declared
  // nowhere, because registering it would replace the host's own entry for that name.
  const contract = JSON.parse(readFileSync(CONTRACT, "utf8"));
  const manifest = JSON.parse(readFileSync(MANIFEST, "utf8"));
  const declared = manifest.contributes.semanticTokenTypes ?? [];
  const byId = new Map<string, any>(declared.map((entry: any) => [entry.id, entry]));
  const superTyped = contract.roles.filter((role: any) => role.kind.standardType && !role.kind.isItsOwnName);
  const roots = contract.roles.filter((role: any) => role.kind.root);
  const ownName = contract.roles.filter((role: any) => role.kind.isItsOwnName);
  for (const role of superTyped) {
    const entry = byId.get(role.name);
    assert.ok(entry, `the manifest declares no super type for '${role.name}'`);
    assert.equal(entry.superType, role.kind.standardType, `'${role.name}' is declared under the wrong super type`);
    assert.ok(
      typeof entry.description === "string" && entry.description.trim() !== "",
      `'${role.name}' is declared with no description, which the host's own schema requires to be present and non-empty`,
    );
  }
  for (const role of [...roots, ...ownName])
    assert.equal(byId.has(role.name), false, `the manifest registers '${role.name}', which the host already registers`);
  const verdict = run();
  assert.equal(verdict.status, 0, `the check refused something:\n${verdict.refusals.join("\n")}`);
  assert.match(verdict.out, /declare a super type/);
});

test("a manifest that omits a role's super type is refused, and so is one that declares a root", () => {
  const missing = manifestWith((manifest) => {
    manifest.contributes.semanticTokenTypes = (manifest.contributes.semanticTokenTypes ?? []).filter(
      (entry: any) => entry.id !== "capsule",
    );
  });
  const forgotten = run(CONTRACT, missing);
  assert.equal(forgotten.status, 1, "a role whose kind is never declared cannot pass");
  assert.ok(
    forgotten.refusals.some((line) => line.startsWith("package.json: declares no semanticTokenTypes entry for 'capsule',")),
    `the undeclared super type was not among what was refused:\n${forgotten.refusals.join("\n")}\n${forgotten.out}`,
  );
  const declared = manifestWith((manifest) => {
    manifest.contributes.semanticTokenTypes.push({
      id: "scope",
      description: "A Scope, this language's own fourth category of Type.",
    });
  });
  const rooted = run(CONTRACT, declared);
  assert.equal(rooted.status, 1, "a root the manifest registers cannot pass");
  assert.ok(
    rooted.refusals.some((line) => line.startsWith("package.json: declares the semanticTokenTypes entry 'scope',")),
    `the registered root was not among what was refused:\n${rooted.refusals.join("\n")}\n${rooted.out}`,
  );
});
