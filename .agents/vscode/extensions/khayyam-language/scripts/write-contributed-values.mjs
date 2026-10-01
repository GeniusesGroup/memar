// Regenerates the two maps the extension contributes to the editor from the display
// contract and one theme sheet, so neither is edited a role at a time.
//
//   node scripts/write-contributed-values.mjs [path/to/package.json]
//
// It writes the two blocks that carry a value: the `[khayyam]` default's
// `editor.tokenColorCustomizations.textMateRules` and the same default's
// `editor.semanticTokenColorCustomizations.rules`. The values are the dark sheet's,
// because a language-scoped default has no theme dimension - one value per role,
// stated once (modules/khayyam/display/display.handoff.md, Decisions). The other sheet
// is valued by scripts/verify-roles.mjs and rendered by nothing, which that script's
// own report says.
//
// It also REMOVES `contributes.semanticTokenScopes` if the manifest carries one, and
// that removal is the half of the work that matters. A bridge entry is not a fallback
// beside the colour rules: a host applies the styling defaults, where a bridge
// registers its probe of TextMate scopes, after the settings' rules, and a rule
// overwrites a score it equals or beats, while the bridge's own `language` field scores
// its selector 10 above a rule keyed the role's own name. So for every role the bridge
// carries the active theme's value for the probed scope is what reaches the reader, and
// the contract's value is not. The contract states a value for every role, so the
// realization applies it and offers a host no bridge to overwrite it with.
//
// A role the contract declares `server-only` gets no textMateRule, because it has no
// TextMate scope - and it needs none: the colour rules key every role by its own name,
// which is the token type a host matches a rule against, and that includes the one role
// no grammar can answer.
//
// It also writes the theme files' own semantic section, which is where a role's value now
// reaches a reader who selects a Khayyam theme: `semanticTokenColors`, keyed by the token
// type (the role's own name read whole, the same spelling the legend advertises), valued
// from THAT theme's own sheet, together with the `semanticHighlighting` opt-in without
// which a host gives a theme no semantic highlighting at all and the map is read by
// nothing. Each theme is found through the manifest's own contribution rather than a name
// written here, so a theme added to the manifest is a theme this run writes without this
// file being told about it.
//
// It writes the theme files' own TextMate section as well, for the same reason and from the
// same sheet: `tokenColors` is the other of the two maps a host reads a role's value out of,
// and a value in it that a hand edit put there is a value no run regenerates. Every value
// that carries a role's colour in a theme file is written here; `khayyamDisplay` is the
// only place in the extension a value is stated.
//
// A manifest path may be given as the first argument and an extension root as the second,
// so what the generator would write can be read before it is what the extension ships
// (display/test/verify-roles.test.ts). Every path the run touches is under that root.
import { readFileSync, writeFileSync } from "node:fs";
import { basename, dirname, join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";

/** The JSON documents this generator reads. Each is a document a file format and a host
 *  read at run time and that no declaration anywhere types, so each is declared here with
 *  the fields this generator reads of it - and declared once, at the reader, so the
 *  generator that writes a manifest cannot disagree with the generator that reads one.
 *
 *  A role in the display contract, as far as this generator reads it: the name every value
 *  is keyed by, the scopes that decide whether a TextMate rule exists for it at all, and
 *  the kind that decides whether a super type is declared for it.
 *  @typedef {{ name: string, scopes?: string[], identity?: string,
 *              kind?: { standardType?: string, isItsOwnName?: boolean, root?: boolean, statement?: string } }} ContractRole
 *
 *  @typedef {{ roles: ContractRole[] }} DisplayContract
 *
 *  A theme's own sheet: every role-attribute value it states, keyed exactly
 *  `khayyam.<role>.<attribute>` - the spelling the contract fixes, which is why
 *  `variableFor` builds the key rather than any code here spelling it.
 *  @typedef {Record<string, string>} ThemeSheet
 *
 *  What a colour rule carries. `foreground` is the value; `fontStyle` is written only when
 *  the sheet states one, because the host format's own convention is to leave an empty one
 *  out and what the themes' own rules do.
 *  @typedef {{ foreground?: string, fontStyle?: string }} StyleSettings
 *
 *  A theme the manifest offers, read the way the host reads `contributes.themes`.
 *  @typedef {{ label?: string, uiTheme?: string, path: string }} ThemeContribution
 *
 *  A theme file, as far as this generator writes it.
 *  @typedef {{ khayyamDisplay?: ThemeSheet, semanticHighlighting?: boolean,
 *              semanticTokenColors?: Record<string, StyleSettings>, tokenColors?: unknown[] }} ThemeFile
 *
 *  The `[khayyam]` block's own settings, as far as this generator writes them. The two
 *  settings it fills are named here rather than left as an open map, so a setting id
 *  misspelled into a write is caught at the write: the host reads a setting by its own id,
 *  and a block handed a value under an id it does not read is a silent no-op.
 *  @typedef {{
 *   "editor.tokenColorCustomizations"?: { textMateRules?: unknown[] },
 *   "editor.semanticTokenColorCustomizations"?: { rules?: Record<string, StyleSettings> }
 * }} LanguageDefaults
 *
 *  The manifest, as far as this generator writes it.
 *  @typedef {{ contributes: {
 *    themes?: ThemeContribution[],
 *    semanticTokenTypes?: Array<{ id: string, superType: string, description?: string }>,
 *    semanticTokenScopes?: unknown,
 *    configurationDefaults: Record<string, LanguageDefaults>
 *  } }} ExtensionManifest
 */

const here = dirname(fileURLToPath(import.meta.url));
const extensionRoot = join(here, "..");
const repositoryRoot = join(extensionRoot, "..", "..", "..", "..");
const LANGUAGE = "khayyam";
/** The sheet the language-scoped default carries, and the reason it is this one: that
 *  setting has no theme dimension, so it holds one sheet and the manifest's own
 *  `contributes.themes` cannot choose which. A reader who selects a theme gets that
 *  theme's values; a reader who selects none gets these. */
const SHEET = "khayyam-dark.json";

/** Reads a JSON document. It answers `unknown` on purpose: the four documents read by this
 *  run have four different shapes and none of them is declared, so each read says which one
 *  it is holding at the place it is read - a reader is never handed an untyped value to
 *  pass on, and a document that stops carrying a field this generator relies on is caught
 *  at the read rather than at the write that assumed it.
 *  @param {string} p
 *  @returns {unknown} */
const read = (p) => JSON.parse(readFileSync(p, "utf8"));
const contract = /** @type {DisplayContract} */ (read(join(repositoryRoot, "modules", "khayyam", "display", "display.json")));
const given = process.argv[2];
const manifestPath = given === undefined ? join(extensionRoot, "package.json") : resolve(given);
const root = process.argv[3] === undefined ? extensionRoot : resolve(process.argv[3]);
const sheet = /** @type {ThemeSheet} */ (
  /** @type {ThemeFile} */ (read(join(root, "themes", SHEET))).khayyamDisplay
);
const manifest = /** @type {ExtensionManifest} */ (read(manifestPath));

/** The one place a value is stated, read out of a sheet by the name the contract fixes.
 *  @param {ContractRole} role @param {string} attribute @param {ThemeSheet} from */
const value = (role, attribute, from) => from[`khayyam.${role.name}.${attribute}`];
/** The two settings a role carries, with the empty fontStyle left out - the host
 *  format's own convention, and what the themes' own rules do.
 *  @param {ContractRole} role @param {ThemeSheet} from
 *  @returns {StyleSettings} */
const settingsOf = (role, from) => {
  /** @type {StyleSettings} */
  const settings = { foreground: value(role, "color", from) };
  const style = value(role, "fontStyle", from);
  if (style !== "") settings.fontStyle = style;
  return settings;
};

const textMateRules = contract.roles
  .filter((role) => (role.scopes ?? []).length > 0)
  .map((role) => ({
    comment: `Role: ${role.name} (from ${SHEET})`,
    scope: role.scopes,
    settings: settingsOf(role, sheet),
  }));

/* ---- the kinds, declared to the host --------------------------------------- */

/** A host matches a rule's key against a token's whole type HIERARCHY, and a hierarchy is
 *  built only from super types someone declared. So a role whose kind is a standard type
 *  is declared here, and that declaration is the whole of what makes a reader's own rule
 *  for the standard class reach our roles: without it, the hierarchy is the role's own
 *  name and no rule keyed the standard type can ever reach it.
 *
 *  A role that is a ROOT declares nothing, on purpose - a root has no standard type, and
 *  declaring one would be a false claim - and a role whose own name IS the host's standard
 *  type declares nothing either, because the host already registers that name and
 *  registering it again REPLACES the host's own entry (and declaring `keyword` a kind of
 *  `keyword` makes the host's own getTypeHierarchy walk a cycle that never ends). */
/** The roles a super type is declared for, each with the standard type it is declared
 *  under. The filter the projection used to carry is inside the walk instead, because a
 *  filter says which roles qualify and says nothing about the fields being read from one:
 *  `kind` is optional on a role, and a name read off it is `string | undefined` whether or
 *  not some earlier line proved otherwise. Here it is destructured once, so the
 *  declaration this writes is the type it is declared to hold - a `superType` that must be
 *  there, which is what the host's own schema says of it.
 *  @returns {{ id: string, superType: string, description?: string }[]} */
const declaredOf = () =>
  contract.roles.flatMap((role) => {
    const kind = role.kind;
    if (kind === undefined || kind.isItsOwnName) return [];
    const { standardType, statement } = kind;
    if (standardType === undefined || standardType === "") return [];
    return [{ id: role.name, superType: standardType, description: statement }];
  });

const declared = declaredOf();
manifest.contributes.semanticTokenTypes = declared;
const roots = contract.roles.filter((role) => role.kind?.root);
const ownName = contract.roles.filter((role) => role.kind?.isItsOwnName);

const semanticRules = Object.fromEntries(contract.roles.map((role) => [role.name, settingsOf(role, sheet)]));
/** The bridge is not written and is not left behind. Every role's value reaches the
 *  editor through the colour rules, keyed by the role's own name, so a host has
 *  nothing to probe a TextMate scope with and no theme to fall back on. */
delete manifest.contributes.semanticTokenScopes;
const unscoped = contract.roles.filter((role) => (role.scopes ?? []).length === 0);

const defaults = manifest.contributes.configurationDefaults[`[${LANGUAGE}]`];
// The two settings are created if the block does not carry them. They are what this run
// fills, and the block is a document this run writes, so a setting that is not there is a
// setting to write rather than a setting to write through.
const tokenColors = (defaults["editor.tokenColorCustomizations"] ??= {});
const semanticColors = (defaults["editor.semanticTokenColorCustomizations"] ??= {});
tokenColors.textMateRules = textMateRules;
semanticColors.rules = semanticRules;

/* ---- the theme files: where a role's value reaches a reader who selects a theme -- */

/** The rules a theme's own TextMate section is written as, each naming the roles it
 *  carries. The order is the sheet's structure read off the contract's own groups rather
 *  than the contract's role order, so a reader opening the file sees one family at a time:
 *  the language's own words, the four categories of Type, the kind `type` ladder, the kind
 *  `variable` ladder, the other two kinds of name, the reference the resolver could not
 *  answer, the text that is not code, and the two refusals. Two roles in one rule share one
 *  value because they share one kind, and only where their scopes are one another's child.
 *
 *  It is a list of names, so it can fall behind the contract, and the run refuses when it
 *  does: a role that has a scope and no rule here would reach a reader through the semantic
 *  map alone, and a rule here naming no role would be a colour outside the contract. */
const SHEET_RULES = [
  ["keyword", "subtype"],
  ["capsule"], ["abstraction"], ["method"], ["scope"],
  ["type-reference"], ["method-argument-type"], ["method-owner-type"], ["included-type"],
  ["included-variable"], ["variable"], ["method-local"],
  ["capsule-field"], ["method-argument"],
  ["identifier-reference"],
  ["comment"], ["file-uri"], ["string"],
  ["invalid-number"], ["invalid-operator"],
];

/** What a rule says about itself, derived from the contract so the prose beside a value
 *  cannot describe a value that is no longer there. The clause about the kind is the
 *  contract's own answer of the three, and the tail is the palette's own rule restated.
 *  @param {ContractRole[]} named
 *  @returns {string} */
const ruleComment = (named) => {
  if (named.length > 1) {
    const kind = named[0].kind ?? {};
    return (
      `Roles: ${named.map((role) => role.name).join(", ")}. \`${named[0].name}\` and \`${named[1].name}\` are one kind, ` +
      `${kind.standardType}, and share this value because they share a kind; the palette separates the kinds ` +
      "of this family by hue, never this one by lightness."
    );
  }
  const role = named[0];
  const kind = role.kind ?? {};
  const what =
    kind.root === true
      ? "Its kind is this language's own root, declared with no standard counterpart"
      : kind.isItsOwnName === true
        ? `Its kind is the host's own standard type '${kind.standardType}', which this role's own name already is`
        : `Its kind is a kind of the host's standard type '${kind.standardType}'`;
  return (
    `Role: ${role.name}. ${role.identity} ${what}, and the value is that kind's hue at the lightness this role's ` +
    "position in its own kind calls for."
  );
};

const named = new Map(contract.roles.map((role) => [role.name, role]));
const scoped = contract.roles.filter((role) => (role.scopes ?? []).length > 0);
const written = [];
for (const contribution of manifest.contributes.themes ?? []) {
  const path = join(root, contribution.path);
  const theme = /** @type {ThemeFile} */ (read(path));
  // Its OWN sheet, not the default's: two sheets that held one value would be one sheet
  // offered twice, and a reader who selected the other theme would be reading this one.
  const own = theme.khayyamDisplay ?? {};
  const listed = SHEET_RULES.flat().flat();
  const missing = scoped.map((role) => role.name).filter((name) => !listed.includes(name));
  const unknown = listed.filter((name) => !named.has(name));
  if (missing.length > 0 || unknown.length > 0)
    throw new Error(
      `theme '${basename(path)}': SHEET_RULES in this file does not cover the contract's roles that have a scope ` +
        `(${missing.length === 0 ? "none missing" : `no rule for ${missing.join(", ")}`}` +
        `${unknown.length === 0 ? "" : `, and it names ${unknown.join(", ")}, which the contract does not define`}). ` +
        "A role with no rule reaches a reader through the semantic map alone, and a rule for a role the contract does " +
        "not define is a colour outside the contract. A role named here that has no scope - `method-local`, which the " +
        "contract declares server-only - is written as no rule, which is exactly what a role with no scope can carry.",
    );
  theme.tokenColors = SHEET_RULES.flatMap((rule) => {
    // A name SHEET_RULES holds and the contract does not define is refused above, so every
    // name here is one the contract defines; a role the contract does define is kept only
    // when it has a scope, because a rule with no scope styles nothing.
    const roles = rule
      .map((name) => named.get(name))
      .filter((role) => role !== undefined)
      .filter((role) => (role.scopes ?? []).length > 0);
    if (roles.length === 0) return [];
    // The host's own shape: one scope is written as a string and several as an array, and
    // this is the same rule either way.
    const scopes = roles.flatMap((role) => role.scopes ?? []);
    return [{
      comment: ruleComment(roles),
      scope: scopes.length === 1 ? scopes[0] : scopes,
      settings: settingsOf(roles[0], own),
    }];
  });
  theme.semanticHighlighting = true;
  theme.semanticTokenColors = Object.fromEntries(
    contract.roles.map((role) => [role.name, settingsOf(role, own)]),
  );
  writeFileSync(path, `${JSON.stringify(theme, null, 2)}\n`);
  written.push(basename(path));
}

writeFileSync(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`);
console.log(
  `wrote ${given === undefined ? relative(repositoryRoot, manifestPath).replace(/\\/g, "/") : manifestPath} from ` +
    `${SHEET}: ${Object.keys(semanticRules).length} semantic colour rules, one per role, keyed by the role's own name; ` +
    `${textMateRules.length} textMateRules, which are the roles that have a scope` +
    (unscoped.length === 0
      ? "."
      : `; ${unscoped.length} of them the contract declares server-only (${unscoped.map((role) => role.name).join(", ")}), ` +
        "which name no scope and are carried by the colour rules alone, like every other role.") +
    ` ${declared.length} super types declared, one per role whose kind is a standard type, which is what makes a ` +
    "reader's own rule for that standard type reach our roles. " +
    `${roots.length} roots declared nowhere (${roots.map((role) => role.name).join(", ")}), and ` +
    `${ownName.length} roles whose own name is the host's own standard type declared nowhere either (${ownName
      .map((role) => role.name)
      .join(", ")}), because registering one of those would replace the host's own entry for that name. ` +
    "The manifest carries no semanticTokenScopes: the colour rules are the only mechanism it offers a role, so a " +
    "host's theme never gets to decide one.",
);
console.log(
  "declared super types: " +
    declared.map((entry) => `${entry.id} : ${entry.superType}`).join(", "),
);
console.log(
  written.length === 0
    ? "wrote no theme: the manifest contributes none, so no value reaches a reader through a mechanism a host resolves"
    : `wrote ${written.join(", ")}: each opted into semantic highlighting, each carrying ${contract.roles.length} ` +
      "semantic colours keyed by the role's own name, valued from its own sheet",
);
