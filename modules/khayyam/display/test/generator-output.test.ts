// The generator's own output being what the extension ships.
//
// A value the generator writes is a value no hand edit can reach, so the shipped
// manifest and the shipped themes are compared against what a run into a temporary
// extension root produces, byte for byte. The values are pinned from the generator that
// writes them rather than from the file that carries them, because the values are
// generated: a hand edit to a generated value is a value no run regenerates.
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { copyFileSync, mkdirSync, mkdtempSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { basename, join } from "node:path";
import { fileURLToPath } from "node:url";
import test from "node:test";
import { LEGEND } from "../../lsp/src/contract.ts";
import { themesRoot } from "./provoke.ts";
import { CONTRACT, EXTENSION, MANIFEST, THEMES } from "./shipped.ts";

const GENERATOR = join(EXTENSION, "scripts", "write-contributed-values.mjs");

/** What the generator writes, taken from a temporary extension root rather than from the
 *  one the editor reads: the values are generated, so a refusal is provoked by
 *  regenerating somewhere else and the shipped manifest and themes are left alone. The
 *  root holds a copy of every theme the extension ships, which is what the theme writer
 *  rewrites. */
function generate(): {
  root: string;
  contributes: Record<string, any>;
  rules: Record<string, unknown>;
  manifest: string;
  themes: Record<string, string>;
} {
  const root = themesRoot();
  const copy = join(root, "package.json");
  writeFileSync(copy, readFileSync(MANIFEST, "utf8"));
  const result = spawnSync(process.execPath, [GENERATOR, copy, root], { encoding: "utf8" });
  assert.equal(result.status, 0, `the generator refused:\n${result.stderr ?? ""}`);
  const manifest = readFileSync(copy, "utf8");
  const themes: Record<string, string> = {};
  for (const file of readdirSync(join(root, "themes")))
    themes[file] = readFileSync(join(root, "themes", file), "utf8");
  return { root, contributes: JSON.parse(manifest).contributes, rules: rulesOf(manifest), manifest, themes };
}

const rulesOf = (manifest: string): Record<string, unknown> =>
  JSON.parse(manifest).contributes.configurationDefaults["[khayyam]"][
    "editor.semanticTokenColorCustomizations"
  ].rules;

/** One theme of a copy, as the generator or a change left it. */
const themeOf = (root: string, file: string): any => JSON.parse(readFileSync(join(root, "themes", file), "utf8"));

test("the colour rules carry every role and the manifest offers no bridge for a theme to overwrite them with", () => {
  // The bridge and a colour rule for one role do not compete: a host applies the
  // styling defaults, where a bridge registers its probe, last, and a rule overwrites
  // a score it equals or beats. So a role the contract values is styled by the colour
  // rule alone, and the manifest contributes no semanticTokenScopes at all - which is
  // what leaves the contract's value the one that reaches the reader.
  const contract = JSON.parse(readFileSync(CONTRACT, "utf8"));
  const { contributes, rules, manifest } = generate();
  assert.deepEqual(
    Object.keys(rules),
    contract.roles.map((role: any) => role.name),
    "the colour rules carry one value per role, keyed by the role's own name",
  );
  assert.equal(
    "semanticTokenScopes" in contributes,
    false,
    "the manifest still contributes a bridge, so a host's theme decides the roles it carries",
  );
  // The manifest the editor reads is the generator's own output, byte for byte.
  assert.equal(manifest, readFileSync(MANIFEST, "utf8"), "the shipped manifest is not what the generator writes");
});

test("each theme the manifest offers is the generator's own output, valued from its own sheet", () => {
  // A theme is the only mechanism that carries the contract's value to a reader who
  // selects one, so its map is generated per theme from that theme's own sheet: a value
  // hand-edited into a theme is a value no run regenerates, and the shipped theme is the
  // generator's output byte for byte, which is what says so.
  const { root, themes } = generate();
  const shipped = readdirSync(THEMES);
  assert.deepEqual(Object.keys(themes).sort(), [...shipped].sort(), "the generator wrote other theme files");
  for (const file of shipped)
    assert.equal(themes[file], readFileSync(join(THEMES, file), "utf8"), `${file} is not what the generator writes`);

  const manifest = JSON.parse(readFileSync(MANIFEST, "utf8"));
  for (const contribution of manifest.contributes.themes) {
    const file = basename(contribution.path);
    const theme = themeOf(root, file);
    // Without the opt-in a host gives the theme no semantic highlighting at all, and the
    // map below is then read by nothing.
    assert.equal(theme.semanticHighlighting, true, `${file} does not opt into semantic highlighting`);
    // Every role the legend advertises, under the legend's own spelling - a token type is
    // matched whole, so a spelling the host cannot read is a token it discards.
    assert.deepEqual(Object.keys(theme.semanticTokenColors), LEGEND, `${file} does not carry the legend's spelling`);
    const sheet = JSON.parse(readFileSync(join(THEMES, file), "utf8")).khayyamDisplay;
    for (const role of LEGEND) {
      const style = theme.semanticTokenColors[role];
      assert.equal(style.foreground, sheet[`khayyam.${role}.color`], `${file} gives '${role}' a value that is not its own`);
      assert.equal(style.fontStyle ?? "", sheet[`khayyam.${role}.fontStyle`], `${file} gives '${role}' the wrong fontStyle`);
    }
  }
});
