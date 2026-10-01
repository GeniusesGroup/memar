// What a theme file itself must carry.
//
// A theme is a file a host resolves a semantic token's colour out of, so what it states
// is a claim about the contract: the opt-in without which a host gives it no semantic
// highlighting at all, the map under the legend's own spelling valued from that theme's
// own sheet, the base it rests on, and no colour outside the roles. Each of those is
// read here over a copy of the themes, so the sheets a reader selects are never the
// ones a refusal is provoked against.
import assert from "node:assert/strict";
import { readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import test from "node:test";
import { themeIn, themesRoot } from "./provoke.ts";
import { CONTRACT, MANIFEST, THEMES } from "./shipped.ts";
import { run } from "./the-check.ts";

test("a theme that does not opt into semantic highlighting is refused", () => {
  // A theme declaring nothing is given no semantic highlighting by a host, with no
  // error: every role in its semanticTokenColors is then read by nothing, and a reader
  // who selected the theme sees the grammar's colours alone.
  const root = themesRoot();
  themeIn(root, "khayyam-light.json", (theme) => delete theme.semanticHighlighting);
  const verdict = run(CONTRACT, MANIFEST, root);
  assert.equal(verdict.status, 1);
  assert.ok(
    verdict.refusals.includes(
      "theme 'khayyam-light.json': declares no semanticHighlighting, so a host gives it no semantic highlighting " +
        "at all and every value in its semanticTokenColors is read by nothing",
    ),
    `the missing opt-in was not among what was refused:\n${verdict.refusals.join("\n")}\n${verdict.out}`,
  );
});

test("a theme whose semantic colour is the other sheet's value is refused", () => {
  // The two sheets differ, and a theme carries its OWN sheet's value: a role valued from
  // the other sheet is a reader reading one theme and seeing the other's colours. Both
  // attributes are checked, because the second is the one a colour alone does not show.
  const light = JSON.parse(readFileSync(join(THEMES, "khayyam-light.json"), "utf8")).khayyamDisplay["khayyam.keyword.color"];
  const colour = themesRoot();
  themeIn(colour, "khayyam-light.json", (theme) => {
    theme.semanticTokenColors.keyword.foreground = "#8CC05E";
  });
  const refused = run(CONTRACT, MANIFEST, colour);
  assert.equal(refused.status, 1);
  assert.ok(
    refused.refusals.includes(
      `theme 'khayyam-light.json': semanticTokenColors.keyword is #8CC05E but khayyamDisplay declares ${light}`,
    ),
    `the other sheet's colour was not among what was refused:\n${refused.refusals.join("\n")}\n${refused.out}`,
  );
  const style = themesRoot();
  themeIn(style, "khayyam-light.json", (theme) => {
    theme.semanticTokenColors["method-argument"].fontStyle = "italic";
  });
  const italic = run(CONTRACT, MANIFEST, style);
  assert.equal(italic.status, 1);
  assert.ok(
    italic.refusals.includes(
      "theme 'khayyam-light.json': semanticTokenColors.method-argument carries fontStyle 'italic' but khayyamDisplay " +
        "declares 'bold'",
    ),
    `the wrong fontStyle was not among what was refused:\n${italic.refusals.join("\n")}\n${italic.out}`,
  );
});

test("a theme that leaves a role out of its semantic colours is refused, and so is one that names a role the legend does not", () => {
  // Both directions of the one map, because either alone is a shape a later reader would
  // have to guess at: a role the legend advertises with no colour of its own resolves no
  // style and is discarded, and a key the legend does not advertise styles a token type
  // no token of ever carries.
  const missing = themesRoot();
  themeIn(missing, "khayyam-light.json", (theme) => delete theme.semanticTokenColors["method-argument"]);
  const withoutRole = run(CONTRACT, MANIFEST, missing);
  assert.equal(withoutRole.status, 1);
  assert.ok(
    withoutRole.refusals.includes(
      "theme 'khayyam-light.json': semanticTokenColors carries no 'method-argument', which the server's advertised " +
        "legend spells exactly that way, so a host resolves no style for that token type and discards the token",
    ),
    `the role left out was not among what was refused:\n${withoutRole.refusals.join("\n")}\n${withoutRole.out}`,
  );
  const extra = themesRoot();
  themeIn(extra, "khayyam-light.json", (theme) => {
    theme.semanticTokenColors["method_argument"] = theme.semanticTokenColors["method-argument"];
  });
  const withRole = run(CONTRACT, MANIFEST, extra);
  assert.equal(withRole.status, 1);
  assert.ok(
    withRole.refusals.includes(
      "theme 'khayyam-light.json': semanticTokenColors carries 'method_argument', which is no name in the server's " +
        "advertised legend",
    ),
    `the role the legend does not advertise was not among what was refused:\n${withRole.refusals.join("\n")}\n${withRole.out}`,
  );
});

test("a theme that includes no base is refused, and so is one whose base names no file or resolves outside the extension", () => {
  // A contributed theme REPLACES the active one, so a theme carrying only this extension's
  // twenty-one roles leaves every other language's tokens uncoloured - measured against
  // the real highlighter, 0 of 26 Python tokens kept a colour. A base is what the reader
  // keeps, and a base the reader is not given is not a base: hence all three refusals, one
  // for each way the `include` can fail to name a file the extension ships.
  const none = themesRoot();
  themeIn(none, "khayyam-light.json", (theme) => delete theme.include);
  const baseless = run(CONTRACT, MANIFEST, none);
  assert.equal(baseless.status, 1, "a theme with no base cannot pass");
  assert.ok(
    baseless.refusals.includes(
      "theme 'khayyam-light.json': includes no base theme, so selecting it gives the reader this extension's " +
        "twenty-one roles and no other language's colours, and every other file in the window is left uncoloured",
    ),
    `the theme with no base was not among what was refused:\n${baseless.refusals.join("\n")}\n${baseless.out}`,
  );
  const absent = themesRoot();
  themeIn(absent, "khayyam-light.json", (theme) => {
    theme.include = "./absent-base.json";
  });
  const missing = run(CONTRACT, MANIFEST, absent);
  assert.equal(missing.status, 1);
  assert.ok(
    missing.refusals.includes(
      "theme 'khayyam-light.json': includes './absent-base.json', which names no file the extension ships, so a host " +
        "reading it has no base and every other language's tokens are left uncoloured",
    ),
    `the base that names no file was not among what was refused:\n${missing.refusals.join("\n")}\n${missing.out}`,
  );
  const outside = themesRoot();
  themeIn(outside, "khayyam-light.json", (theme) => {
    theme.include = "../../../../AGENTS.md";
  });
  const escaped = run(CONTRACT, MANIFEST, outside);
  assert.equal(escaped.status, 1);
  assert.ok(
    escaped.refusals.includes(
      "theme 'khayyam-light.json': includes '../../../../AGENTS.md', which resolves outside the folder a contributed " +
        "path is resolved against, so the base would be a file on this machine and not one the extension ships",
    ),
    `the base outside the extension was not among what was refused:\n${escaped.refusals.join("\n")}\n${escaped.out}`,
  );
});

test("a base's own missing base is refused, and a base this check cannot read is reported as one", () => {
  // The host reads the base before the theme that includes it, so the base's own
  // `include` is part of the chain, and a chain that ends at nothing is a theme with no
  // base - found in the base rather than in the theme that named it. The other kind of
  // include is not a refusal: a host reads a `.tmTheme` include as a TextMate theme, which
  // is a legitimate way to bring token colours in, and this check does not read those
  // files - so it says so rather than passing a chain it has not walked.
  const broken = themesRoot();
  writeFileSync(join(broken, "themes", "light_modern.json"), JSON.stringify({ name: "Light Modern", include: "./gone.json" }));
  const missing = run(CONTRACT, MANIFEST, broken);
  assert.equal(missing.status, 1, "a chain that ends at nothing cannot pass");
  assert.ok(
    missing.refusals.includes(
      "theme 'light_modern.json': includes './gone.json', which names no file the extension ships, so a host reading " +
        "it has no base and every other language's tokens are left uncoloured",
    ),
    `the base a base names and the extension does not ship was not among what was refused:\n${missing.refusals.join("\n")}\n${missing.out}`,
  );
  const other = themesRoot();
  themeIn(other, "khayyam-light.json", (theme) => {
    theme.include = "./synthetic.tmTheme";
  });
  const unread = run(CONTRACT, MANIFEST, other);
  assert.ok(
    unread.out.includes(
      "note       : theme 'khayyam-light.json': includes './synthetic.tmTheme', which a host reads as a TextMate " +
        "theme rather than a colour theme, and which this check does not read, so the base it reaches is unconfirmed",
    ),
    `the base this check cannot read was not among the notes:\n${unread.out}\n${unread.refusals.join("\n")}`,
  );
});

test("a theme that carries a colour outside the contract's roles is refused", () => {
  // The theme's own colour contribution is the twenty-one roles, and the base states the
  // workbench's colours and every other language's. A theme that states a workbench
  // colour of its own is a second copy of one the base already carries, and a second copy
  // drifts; a `tokenColors` rule for a scope no role names is the other shape of the same
  // thing, and the check that refuses it has been there since the sheets were valued.
  const workbench = themesRoot();
  themeIn(workbench, "khayyam-light.json", (theme) => {
    theme.colors = { "editor.background": "#FFFFFF" };
  });
  const stated = run(CONTRACT, MANIFEST, workbench);
  assert.equal(stated.status, 1, "a theme restating a workbench colour cannot pass");
  assert.ok(
    stated.refusals.includes(
      "theme 'khayyam-light.json': states the workbench colour 'editor.background', which is no role the contract " +
        "names: this theme's colours are the twenty-one roles and its base states the workbench's, and a second " +
        "statement of one of them is a copy that will drift from it",
    ),
    `the restated workbench colour was not among what was refused:\n${stated.refusals.join("\n")}\n${stated.out}`,
  );
  const foreign = themesRoot();
  themeIn(foreign, "khayyam-light.json", (theme) => {
    theme.tokenColors.push({ scope: "string.quoted.double.python", settings: { foreground: "#A31515" } });
  });
  const scoped = run(CONTRACT, MANIFEST, foreign);
  assert.equal(scoped.status, 1);
  assert.ok(
    scoped.refusals.includes(
      "theme 'khayyam-light.json': styles scope 'string.quoted.double.python', which no role names",
    ),
    `the other language's scope was not among what was refused:\n${scoped.refusals.join("\n")}\n${scoped.out}`,
  );
});
