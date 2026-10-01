// Runs the checks and prints the verdict.
//
// What the extension contributes is one claim, and this run holds every side of it to
// the display contract (modules/khayyam/display/display.json, documented in
// modules/khayyam/display/display.md): the contract's own shape, which mechanism answers
// each role, every scope the grammar emits, the manifest's declarations, the legend the
// server actually advertises, and the language-scoped default the editor layers over the
// active theme. Its own last line is the verdict, and a run that refuses something says
// what it refused on stderr and exits 1.
//
// Two concerns are not this file's and are stated where they are:
//   scripts/host-classification.mjs  the host's own registered classification and the
//                                    arithmetic that decides which value a reader sees,
//                                    both read out of the installed product's bundle
//   scripts/contribution.mjs         one theme the manifest contributes: what it
//                                    identifies itself by, the values its own sheet
//                                    states, the map a host reads them out of, the base
//                                    it rests on, and those values measured against the
//                                    contract's palette rules
//
// Run: node scripts/verify-roles.mjs [path/to/display.json] [path/to/package.json] [path/to/extension/root]
//
// A contract path may be given as the first argument, so a candidate contract can be
// checked before it is the contract: the same refusals, against a file that is not
// yet the one the extension ships. A manifest path may be given as the second, for
// the same reason and over the same refusals, and an extension root as the third, so
// a run can be asked about a copy of the themes rather than the ones a reader reads.

import { readFileSync } from "node:fs";
import { dirname, join, relative, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { judgeSemanticMaps, measureValues, readContributions } from "./contribution.mjs";
import { matchingOf, readHostClassification, registeredNamesOf, TOKEN_ID, parseSelector, SELECTOR, SEPARATOR, stylesToken } from "./host-classification.mjs";

/** The JSON documents this run reads, declared here with the fields it reads of them. A
 *  specification, a grammar and a manifest are documents a file format and a host read at
 *  run time and that no declaration types, so each is stated once, at the reader, and a
 *  role's kind is `unknown`-shaped where its kind is the thing under test.
 *
 *  One role of the display contract.
 *  @typedef {{ name: string, appliesTo?: string, implementedBy?: string, scopes?: string[],
 *              serverOnlyBecause?: string, attributes?: Record<string, string>,
 *              identity?: string,
 *              kind?: { standardType?: string, isItsOwnName?: boolean, root?: boolean,
 *                       statement?: string, because?: string } }} Role
 *
 *  The container scopes the contract declares: each names a region and says what it is for.
 *  @typedef {{ name: string, purpose?: string }} ContainerScope
 *
 *  The display contract, as far as this run reads it.
 *  @typedef {{
 *   roles: Role[],
 *   attributeSchema?: { attributes?: Record<string, unknown>, deliberateExclusions?: Record<string, unknown> },
 *   containerScopes?: { scopes?: ContainerScope[] },
 *   palette?: { recordedDichromacyPairs?: { pairs?: Array<{ theme?: string, pair?: string }> } }
 * }} Specification
 *
 *  The TextMate grammar, as far as this run reads it: the scope name it declares and the
 *  pattern lists its repository defines. The rest of the tree is walked without being
 *  declared, because the walk asks each node only whether it is an object, an array, or a
 *  leaf.
 *  @typedef {{ scopeName?: string, repository?: Record<string, unknown> }} GrammarFile
 *
 *  The `[khayyam]` block's own settings, as far as this run reads them. The three settings
 *  it reads are named here rather than left as an open map of unknown values: the run
 *  compares each against what a host reads out of it, and a setting that stops being
 *  declared is a silent no-op for every role the manifest was reaching a reader through.
 *  @typedef {{
 *   "editor.tokenColorCustomizations"?: {
 *     textMateRules?: Array<{ scope?: string | string[], settings?: StyleSettings }>
 *   },
 *   "editor.semanticTokenColorCustomizations"?: { rules?: unknown },
 *   "editor.semanticHighlighting.enabled"?: unknown
 * }} LanguageDefaults
 *
 *  The manifest, as far as this run reads it.
 *  @typedef {{
 *   contributes?: {
 *     themes?: Array<{ label?: unknown, uiTheme?: unknown, path?: unknown }>,
 *     configurationDefaults?: Record<string, LanguageDefaults>,
 *     semanticTokenTypes?: Array<{ id?: string, superType?: string, description?: string }>,
 *     semanticTokenScopes?: unknown
 *   }
 * }} ExtensionManifest
 *
 *  What a colour rule carries, which the host format gives as a foreground and an optional
 *  fontStyle.
 *  @typedef {{ foreground?: string, fontStyle?: string }} StyleSettings
 */

const here = dirname(fileURLToPath(import.meta.url));
const extensionRoot = join(here, "..");
const repositoryRoot = join(extensionRoot, "..", "..", "..", "..");
/** @param {string} p @returns {string} */
const rel = (p) => relative(repositoryRoot, p).replace(/\\/g, "/");
/** A path outside this repository is shown as it was given, since a relative path out
 *  of the root names more `../` than it does places.
 *  @param {string} p @returns {string} */
const shown = (p) => (p.startsWith(repositoryRoot) ? rel(p) : p);

const given = process.argv[2];
const specPath = given === undefined ? join(repositoryRoot, "modules", "khayyam", "display", "display.json") : resolve(given);
const givenManifest = process.argv[3];
const manifestPath = givenManifest === undefined ? join(extensionRoot, "package.json") : resolve(givenManifest);
/** A contributed theme's `path` is resolved against an extension root, which the third
 *  argument may replace so a run can be asked about a copy of the themes rather than the
 *  ones the editor reads. */
const themesRoot = process.argv[4] === undefined ? extensionRoot : resolve(process.argv[4]);
const grammarPath = join(extensionRoot, "syntaxes", "khayyam.tmLanguage.json");

/** Reads a JSON document. It answers `unknown` on purpose, and each of the three reads
 *  below says which document it is holding - so the run never passes an untyped value to
 *  the checks that judge it. */
const read = (/** @type {string} */ p) => JSON.parse(readFileSync(p, "utf8"));

const spec = /** @type {Specification} */ (read(specPath));
const grammar = /** @type {GrammarFile} */ (read(grammarPath));
const pkg = /** @type {ExtensionManifest} */ (read(manifestPath));
/** @type {string[]} */
const errors = [];
/** @type {string[]} */
const notes = [];

/* ---- the contract's own shape ------------------------------------------- */

const roles = spec.roles ?? [];
const attributeNames = Object.keys(spec.attributeSchema?.attributes ?? {});
/** @param {string} role @param {string} attribute @returns {string} */
const variableFor = (role, attribute) => `khayyam.${role}.${attribute}`;

if (roles.length === 0) errors.push("contract: no roles are defined");
if (attributeNames.length === 0) errors.push("contract: the attribute schema defines no attribute");

for (const excluded of Object.keys(spec.attributeSchema?.deliberateExclusions ?? {})) {
  if (attributeNames.includes(excluded))
    errors.push(`contract: '${excluded}' is both excluded and declared as an attribute`);
}

/** @type {Set<string>} */
const roleNames = new Set();
for (const role of roles) {
  if (roleNames.has(role.name)) errors.push(`contract: role '${role.name}' is defined twice`);
  roleNames.add(role.name);
  if (!role.appliesTo) errors.push(`contract: role '${role.name}' does not say what it applies to`);
  // Whether a role names a scope is not asked here: it follows from which mechanism
  // implements the role, and the section below is where that is checked.

  for (const attribute of attributeNames) {
    const declared = role.attributes?.[attribute];
    const expected = variableFor(role.name, attribute);
    if (typeof declared !== "string") {
      errors.push(`contract: role '${role.name}' names no value for the attribute '${attribute}'`);
    } else if (declared !== expected) {
      errors.push(
        `contract: role '${role.name}' attribute '${attribute}' names variable '${declared}', but the contract fixes it at '${expected}'`
      );
    }
  }
  for (const attribute of Object.keys(role.attributes ?? {})) {
    if (!attributeNames.includes(attribute))
      errors.push(
        `contract: role '${role.name}' uses attribute '${attribute}', which the attribute schema does not define (an excluded attribute is an error, not a value)`
      );
  }
}

/** @type {Set<string>} */
const containerScopes = new Set((spec.containerScopes?.scopes ?? []).map((c) => c.name));
for (const c of spec.containerScopes?.scopes ?? []) {
  if (!c.purpose) errors.push(`contract: container scope '${c.name}' does not say what it is for`);
}

/* ---- what implements each role ------------------------------------------- */

/** A role is answered either by a scope a grammar emits or by a resolver alone, and
 *  which of the two is a property of what the role IS rather than of any realization:
 *  a TextMate grammar matches one line at a time and holds no symbol table, so a role
 *  whose whole distinction is a block the grammar cannot see has no scope to carry it
 *  at all. The contract says so per role, in `implementedBy`, and this checks that
 *  every role says which - and that a server-only role says WHY, in the one place a
 *  consumer is shown it, because a consumer that cannot answer the role is entitled to
 *  know that before it starts rather than after it has guessed a scope of its own.
 *
 *  Without this the check would refuse `method-local` as a role the grammar does not
 *  implement, which is right by its own rule and wrong for that role: no grammar can
 *  implement it, and the contract has already said so. A role that states neither is
 *  still refused, and so is one that states one and contradicts it. */
const GRAMMAR_SCOPE = "grammar-scope";
const SERVER_ONLY = "server-only";
/** @type {string[]} */
const serverOnlyRoles = [];
/** @type {string[]} */
const grammarScopedRoles = [];

for (const role of roles) {
  const by = role.implementedBy;
  const scopes = role.scopes ?? [];
  if (by !== GRAMMAR_SCOPE && by !== SERVER_ONLY) {
    errors.push(
      `contract: role '${role.name}' states implementedBy ${by === undefined ? "nothing" : `'${by}'`}, which is ` +
        `neither '${GRAMMAR_SCOPE}' nor '${SERVER_ONLY}'; a role is answered either by a scope a grammar emits or ` +
        "by a resolver that can see the whole document, and a role that says which is neither cannot be checked " +
        "against anything",
    );
    continue;
  }
  if (by === SERVER_ONLY) {
    serverOnlyRoles.push(role.name);
    if (typeof role.serverOnlyBecause !== "string" || role.serverOnlyBecause.trim() === "")
      errors.push(
        `contract: role '${role.name}' is declared server-only and does not say why: 'serverOnlyBecause' is the one ` +
          "place a reader is told a consumer may not be able to answer this role, so the reason is not optional",
      );
    if (scopes.length > 0)
      errors.push(
        `contract: role '${role.name}' is declared server-only but names the scope(s) [${scopes}], which is what a ` +
          "grammar emits and is exactly what 'server-only' denies",
      );
  } else {
    grammarScopedRoles.push(role.name);
    if (scopes.length === 0)
      errors.push(
        `contract: role '${role.name}' states implementedBy '${GRAMMAR_SCOPE}' and names no scope, so nothing ` +
          "implements it",
      );
    if (role.serverOnlyBecause !== undefined)
      errors.push(
        `contract: role '${role.name}' states implementedBy '${GRAMMAR_SCOPE}' and carries a 'serverOnlyBecause' ` +
          "reason, which only a role declared server-only may have",
      );
  }
}

/* ---- the host's own registered classification, read out of the host --------- */

const host = readHostClassification(shown);
for (const fault of host.faults) errors.push(fault);

/* ---- every role's kind, against the host's own list ------------------------- */

/** @param {Role} role @returns {NonNullable<Role["kind"]>} */
const kindOf = (role) => (role.kind ?? {});
/** @type {string[]} */
const rootRoles = [];
/** @type {string[]} */
const ownNameRoles = [];
/** @type {Role[]} */
const superTypedRoles = [];
for (const role of roles) {
  const kind = kindOf(role);
  if (kind === null || typeof kind !== "object" || Object.keys(kind).length === 0) {
    errors.push(
      `contract: role '${role.name}' states no kind, so nothing says what kind of thing the name is; a role states the ` +
        "host's own standard type it is a kind of, or that it is this language's own root with no standard counterpart",
    );
    continue;
  }
  const isRoot = kind.root === true;
  const hasStandard = typeof kind.standardType === "string" && kind.standardType !== "";
  if (isRoot && hasStandard) {
    errors.push(
      `contract: role '${role.name}' states itself a root and also names the standard type '${kind.standardType}': a ` +
        "root is a kind the host has no counterpart for, and a role that is both is neither",
    );
    continue;
  }
  if (!isRoot && !hasStandard) {
    errors.push(
      `contract: role '${role.name}' states neither a root nor a standard type, so nothing says what kind of thing the ` +
        "name is",
    );
    continue;
  }
  if (typeof kind.statement !== "string" || kind.statement.trim() === "")
    errors.push(`contract: role '${role.name}' states a kind and no statement, so nothing says what the kind is for`);
  if (isRoot) {
    if (typeof kind.because !== "string" || kind.because.trim() === "")
      errors.push(
        `contract: role '${role.name}' is declared a root and does not say why: 'because' is the one place a reader is ` +
          "told what this language adds to the host's vocabulary, so the reason is not optional",
      );
    rootRoles.push(role.name);
  } else if (host.types.size > 0 && kind.standardType !== undefined && !host.types.has(kind.standardType)) {
    errors.push(
      `contract: role '${role.name}' names the kind '${kind.standardType}', which the host does not register: a kind is ` +
        `the host's own standard type, read out of the product's own bundle, and '${kind.standardType}' is not among the ` +
        `${host.types.size} it registers`,
    );
  } else if (kind.isItsOwnName === true) {
    if (kind.standardType !== role.name)
      errors.push(
        `contract: role '${role.name}' states its kind is its own name and names '${kind.standardType}' instead, which is ` +
          "a different token type and a claim about a kind the host registers under another name",
      );
    ownNameRoles.push(role.name);
  } else {
    superTypedRoles.push(role);
  }
}
const distinctKinds = new Set(
  roles.map((role) => kindOf(role).root === true ? `root:${role.name}` : kindOf(role).standardType),
);

/* ---- every scope the grammar emits -------------------------------------- */

/** @type {Set<string>} */
const grammarScopes = new Set();
/** @type {Set<string>} */
const grammarIncludes = new Set();
/** The grammar as a tree of nodes walked for the two fields it states: a node is an object,
 *  an array of nodes, or a leaf, and the walk asks nothing of a leaf.
 *  @param {unknown} node @returns {void} */
const walk = (node) => {
  if (Array.isArray(node)) {
    node.forEach(walk);
    return;
  }
  if (!node || typeof node !== "object") return;
  for (const [key, value] of Object.entries(node)) {
    if (key === "name" && typeof value === "string" && value.includes(".")) grammarScopes.add(value);
    if (key === "include" && typeof value === "string") grammarIncludes.add(value);
    walk(value);
  }
};
walk(grammar);

/** @type {Set<string>} */
const specScopes = new Set(roles.flatMap((r) => r.scopes ?? []));

for (const role of roles) {
  // A role declared server-only is one no scope can carry, so the grammar is not
  // asked for one; the contract's own reason is the check, and it is made above.
  if (serverOnlyRoles.includes(role.name)) continue;
  const missing = (role.scopes ?? []).filter((scope) => !grammarScopes.has(scope));
  if (missing.length > 0)
    errors.push(`grammar: role '${role.name}' is not implemented; the grammar emits no ${missing.join(", ")}`);
}
for (const scope of grammarScopes) {
  if (!specScopes.has(scope) && !containerScopes.has(scope))
    errors.push(`grammar: scope '${scope}' is emitted but no role or container scope in the contract names it`);
}
for (const scope of specScopes) {
  if (!grammarScopes.has(scope)) errors.push(`grammar: scope '${scope}' is named by the contract but never emitted`);
}
for (const ref of grammarIncludes) {
  if (ref.startsWith("#") && !(ref.slice(1) in (grammar.repository ?? {})))
    errors.push(`grammar: pattern list includes '${ref}', which the repository does not define`);
  if (!ref.startsWith("#") && ref !== grammar.scopeName)
    notes.push(`grammar: includes '${ref}', an external grammar this check cannot inspect`);
}

/* ---- every theme the extension ships, and every theme the manifest offers ----- */

/** What the contract fixes, read out of it once and handed to the theme check: the roles
 *  and their attributes, the names and scopes among them, the container scopes, and the
 *  two spellings every side of a claim is matched on. */
const contract = { roles, attributeNames, roleNames, specScopes, containerScopes, variableFor, kindOf };
const contributions = readContributions({ pkg, themesRoot, contract, variableFor });
for (const refusal of contributions.errors) errors.push(refusal);
for (const note of contributions.notes) notes.push(note);
const themes = contributions.themes;

/* ---- the language-scoped default the editor layers over the active theme ------- */

// The roles reach the editor additively, as a language-scoped default of
// editor.tokenColorCustomizations, which the editor layers over the active
// theme (verified in the editor bundle: setCustomTokenColors is applied to the
// current colour theme). Those defaults must carry the same values the theme
// file declares.
//
// A semantic token is the other way in, and the editor treats it very
// differently (all verified in the editor bundle, VS Code 43.6.0):
//   - a rule's key is split right to left on '.' and '$': the segment before the
//     first separator is the token TYPE, the one after it is the LANGUAGE, and
//     anything further right is discarded. A legend entry is therefore a token
//     type, not a TextMate scope, and a scope name used as a rule's key - like
//     `entity.name.import.khayyam`, read as the type `entity` in the language
//     `name` - styles nothing, while the role's own name with no separator at all
//     is exactly the type the editor matches against.
//   - editor.semanticTokenColorCustomizations.rules is a MAP from selector to
//     style. An array of {scope, settings} - the TextMate shape - configures
//     nothing there, because the editor reads the rule's own keys as selectors
//     and the keys of an array are its indices.
//   - a token type no rule styles is given no style at all, and the editor then
//     DISCARDS the token, leaving the grammar's colour with no error. So every
//     role's token type needs a rule of our own, keyed by the role's own name, and
//     that is all it needs: the contract states a value for every role, so a
//     realization applies it and must not let a host's theme decide it.
const LANGUAGE = "khayyam";
/** The manifest's `configurationDefaults`, bound once: a block that carries no settings is
 *  a manifest that offers none, and reading it through `?.` at each of the four places
 *  below would ask the question of the manifest four times over. */
const configurationDefaults = pkg.contributes?.configurationDefaults;
const textMateRules = configurationDefaults?.["[khayyam]"]?.["editor.tokenColorCustomizations"]?.textMateRules;
const semanticCustomizations =
  configurationDefaults?.["[khayyam]"]?.["editor.semanticTokenColorCustomizations"];
const semanticHighlighting =
  configurationDefaults?.["[khayyam]"]?.["editor.semanticHighlighting.enabled"];
const bridge = pkg.contributes?.semanticTokenScopes;
/** The manifest's own TextMate-shaped rules, read the way a host reads them: one scope is
 *  written as a string and several as an array, and the map below is the same either way.
 *  @param {Array<{ scope?: string | string[], settings?: StyleSettings }>} rules
 *  @returns {Map<string, StyleSettings>} */
const settingsByScope = (rules) => {
  /** @type {Map<string, StyleSettings>} */
  const byScope = new Map();
  // A rule naming no scope styles nothing: the host reads the rule's own `scope`, so a
  // rule without one is not a rule about any scope and is not entered under a stand-in.
  for (const rule of rules ?? [])
    for (const scope of [rule.scope].flat())
      if (typeof scope === "string") byScope.set(scope, rule.settings ?? {});
  return byScope;
};

/* ---- the manifest's own declarations, against the contract's kinds ----------- */

/** A super type is the whole of what makes a reader's own rule for the standard class
 *  reach our roles, so the manifest's declarations and the contract's kinds are counted
 *  against each other in both directions. A role that declares no super type where its
 *  kind names one is the shape that looks like it works: the role is styled by this
 *  extension's own rule, and no rule a reader already has reaches it through its kind. */
const declaredTypes = pkg.contributes?.semanticTokenTypes ?? [];
/** @type {Map<string, { id?: string, superType?: string, description?: string }>} */
const declaredById = new Map();
for (const entry of declaredTypes) {
  if (typeof entry?.id !== "string" || entry.id === "") {
    errors.push("package.json: contributes a semanticTokenTypes entry with no id, which the host's own schema refuses");
    continue;
  }
  if (declaredById.has(entry.id)) {
    errors.push(
      `package.json: declares the semanticTokenTypes entry '${entry.id}' twice, so which super type it carries is a ` +
        "property of which one a host read first",
    );
    continue;
  }
  if (!TOKEN_ID.test(entry.id)) {
    errors.push(
      `package.json: declares the semanticTokenTypes entry '${entry.id}', which is not a legal token type in the host ` +
        `(${TOKEN_ID.source}); registerTokenType refuses it with 'Invalid token type id.'`,
    );
  }
  if (typeof entry.description !== "string" || entry.description.trim() === "") {
    errors.push(
      `package.json: declares the semanticTokenTypes entry '${entry.id}' with no description, which the host's own ` +
        "schema requires to be present and non-empty, and which is the one place a reader is told what the type is",
    );
  }
  declaredById.set(entry.id, entry);
}

for (const role of superTypedRoles) {
  const entry = declaredById.get(role.name);
  const kind = kindOf(role);
  if (entry === undefined) {
    errors.push(
      `package.json: declares no semanticTokenTypes entry for '${role.name}', whose kind is the host's standard type ` +
        `'${kind.standardType}'. Its type hierarchy is then the role's own name and nothing else, so a reader's own rule ` +
        `for '${kind.standardType}' never reaches it - which is not a cosmetic loss: a theme that has never heard of ` +
        "Khayyam styles the role not at all.",
    );
    continue;
  }
  if (entry.superType !== kind.standardType)
    errors.push(
      `package.json: declares the semanticTokenTypes entry '${role.name}' under the super type ` +
        `'${entry.superType ?? "(none)"}', but the contract states its kind as '${kind.standardType}'`,
    );
  if (entry.superType === role.name)
    errors.push(
      `package.json: declares the semanticTokenTypes entry '${role.name}' under its own name, which makes the host's ` +
        "getTypeHierarchy walk a cycle that never ends: it starts at the name, pushes the super type, looks the super " +
        "type up, and finds the same entry again",
    );
  // An entry that declares no super type declares no name, and no name is one the host
  // does not register - so the two cases answer the same question and are asked together.
  const superType = entry.superType;
  if (host.types.size > 0 && (superType === undefined || !host.types.has(superType)))
    errors.push(
      `package.json: declares the semanticTokenTypes entry '${role.name}' under the super type '${superType}', ` +
        `which the host does not register: a super type is matched against the hierarchy, and a hierarchy can hold a ` +
        "name the host never registered, which no rule could ever reach",
    );
}

for (const [id, entry] of declaredById) {
  const role = roles.find((candidate) => candidate.name === id);
  if (role === undefined) {
    errors.push(
      `package.json: declares the semanticTokenTypes entry '${id}', which is no role the contract defines, so a host ` +
        "registers a type no token of this extension ever carries",
    );
    continue;
  }
  if (rootRoles.includes(id))
    errors.push(
      `package.json: declares the semanticTokenTypes entry '${id}', which the contract declares a ROOT: a root is a kind ` +
        "the host has no counterpart for, its hierarchy is exactly itself by design, and registering it under anything " +
        "would be a claim about the language that the contract does not make",
    );
  if (ownNameRoles.includes(id))
    errors.push(
      `package.json: declares the semanticTokenTypes entry '${id}', whose kind the contract states is its own name: the ` +
        "host already registers that name, and registering it again REPLACES the host's own entry - its description, its " +
        "number, and the property the theme-styling schema holds for it",
    );
}

/* ---- the score, stated as arithmetic rather than as a claim ----------------- */

const { hierarchyOf, scoreOf } = matchingOf(host, declaredTypes);

/** The decision this whole classification exists to reach: whose value reaches a reader
 *  for a role whose hierarchy has more than one entry. The host's own code says it, so
 *  the run says it in the host's own numbers rather than asserting it. */
{
  // The role and the kind the CONTRACT states, kept only where the MANIFEST also declares
  // that kind: this block is about a role that states a kind and is declared under it, and
  // a name read apart from the entry that carries it is the one that can be absent. Which
  // of the two names is scored is the contract's own - the check above already refuses the
  // two disagreeing - and it is the manifest's entry that decides which role is asked.
  const decided = superTypedRoles.flatMap((candidate) => {
    const superType = kindOf(candidate).standardType;
    const declaredSuper = declaredById.get(candidate.name)?.superType;
    return superType !== undefined && declaredSuper !== undefined ? [{ role: candidate, superType }] : [];
  });
  const asked = decided[0];
  if (asked !== undefined) {
    const { role, superType } = asked;
    const declared = role.name;
    const hierarchy = hierarchyOf(declared);
    const ours = scoreOf(declared, LANGUAGE, parseSelector(declared));
    const theirs = scoreOf(declared, LANGUAGE, parseSelector(superType));
    if (ours <= theirs)
      errors.push(
        `score: this extension's own rule for '${declared}' scores ${ours} against the ${theirs} of a reader's rule for ` +
          `'${superType}', so the value the contract states is NOT the one a reader would see. The super type is the ` +
          "wrong ground and the manifest must not declare one until it is right.",
      );
    else
      notes.push(
        `score: '${declared}' keyed by its own name sits at depth 0 of the hierarchy ['${hierarchy.join(", ")}'] and ` +
          `scores ${ours}; a reader's rule for '${superType}' sits at depth ${hierarchy.indexOf(superType)} and scores ` +
          `${theirs}, and a style is written when a rule's score is greater than or equal to the one held, so the value ` +
          "this extension contributes is the one a reader sees while a theme that never heard of Khayyam still reaches " +
          "our roles through their declared kind",
      );
  }
}

/* ---- the legend the server advertises, and whether the editor can match it --- */

/** THE RULE, in words, because it is stated nowhere else in this repository and every
 *  file that read a legend name agreed with the others instead of with it. Transcribed
 *  from the editor bundle (VS Code 43.6.0,
 *  resources/app/out/vs/workbench/workbench.desktop.main.js):
 *
 *  1. A token's TYPE is its legend entry, whole, and its LANGUAGE is the language of
 *     the document it stands in. Neither is read out of the name.
 *  2. A styling rule is a SELECTOR, and a selector's key is split on the FIRST
 *     separator: what precedes it is the type, what follows it is the language, and
 *     anything further right is dropped. `method-argument.khayyam` asks for the token
 *     type `method-argument` in the language `khayyam`.
 *  3. A selector that names a language reaches only that language; one that names none
 *     reaches that token type in every language.
 *  4. A selector's type must be in the token's type HIERARCHY: the token's own name,
 *     then every name it was declared to extend under `semanticTokenTypes`, then the
 *     editor's own supertypes for its standard types. An extension that declares no
 *     `semanticTokenTypes` gives every custom type a hierarchy of exactly one name -
 *     the name itself.
 *
 *  So a legend entry that carries a separator can never be styled by a rule keyed with
 *  that same entry: the rule reads the part before the separator as the type, and the
 *  token's one-name hierarchy does not contain it. The editor gives such a token no
 *  style and drops it while merging the grammar's tokens in, so the request succeeds,
 *  the tokens arrive, and nothing is drawn. */
const legendPath = join(repositoryRoot, "modules", "khayyam", "lsp", "src", "contract.ts");
const LEGEND = await import(pathToFileURL(legendPath).href)
  .then(
    /** @param {{ LEGEND?: string[] }} module @returns {string[] | null} */
    (module) => {
      // A module that exports no legend is the same fault as a module that cannot be
      // imported: the names the server advertises could not be read. It is refused here so
      // that what this run carries is a legend or nothing, and never a name that is not
      // there.
      if (!Array.isArray(module.LEGEND)) {
        errors.push(`legend: ${rel(legendPath)} exports no LEGEND, so the names the server advertises are not read`);
        return null;
      }
      return module.LEGEND;
    },
  )
  .catch(
    /** @param {Error} fault @returns {null} */
    (fault) => {
      errors.push(`legend: the server's advertised legend could not be read from ${rel(legendPath)}: ${fault.message}`);
      return null;
    },
  );

/** The legend, read out of the module the server advertises it from. It is read and
 *  not rebuilt: a check that derived the legend from the contract would agree with any
 *  derivation, and the defect this exists to catch was a name that every derivation in
 *  the tree agreed with and that the editor could not read. */
const colorRules = /** @type {Record<string, StyleSettings>} */ (semanticCustomizations?.rules ?? {});
const reachable = Object.keys(colorRules).map(parseSelector);
/** The names the host registers as its own standard types, so the report can say which of
 *  our legend entries the host already has a type for. */
const registeredNames = registeredNamesOf(host);

/** @type {string[]} */
const unreadable = [];
// A Set, so the count reported is a count of names and not a count of complaints: one
// name can be missing and unreachable at once.
/** @type {Set<string>} */
const unspelled = new Set();
/** @type {string[]} */
const unmatched = [];

if (LEGEND === null) {
  // the failure is already recorded; there is nothing to compare
} else {
  if (LEGEND.length !== roles.length) {
    errors.push(
      `legend: the server advertises ${LEGEND.length} token types against the contract's ${roles.length} roles`,
    );
  }
  for (const [index, name] of LEGEND.entries()) {
    // 1. A legend entry that carries a separator is a name no rule keyed the same way
    //    can reach, so it is refused here rather than discovered in the editor.
    if (SEPARATOR.test(name)) {
      const selector = parseSelector(name);
      unreadable.push(name);
      errors.push(
        `legend: entry ${index} is '${name}', which carries a separator. A legend entry is the token type ` +
          `the editor matches a rule against, whole: the rule's key '${name}' is read as the type ` +
          `'${selector.type}' in the language '${selector.language ?? "(none)"}', while the token's own type ` +
          `hierarchy is ['${name}'], so no rule reaches it and the editor discards the token. A role's name ` +
          `is the contract's own name; the language belongs in the [${LANGUAGE}] block the colour rules sit in ` +
          `and in the provider's document selector.`,
      );
    }
    // 2. The same spelling, in the one mechanism the editor reads for a role's value.
    if (!TOKEN_ID.test(name)) {
      errors.push(
        `package.json: the legend entry '${name}' is not a legal token type in the editor (${TOKEN_ID.source})`,
      );
    }
    if (!SELECTOR.test(name)) {
      errors.push(`package.json: '${name}' is not a legal semantic token selector in the editor (${SELECTOR.source})`);
    }
    if (!(name in colorRules)) {
      unspelled.add(name);
      errors.push(
        `package.json: the legend entry '${name}' keys no editor.semanticTokenColorCustomizations rule under ` +
          "that spelling, so the token the server answers with it reaches no colour of its own, and the manifest " +
          "contributes no semanticTokenScopes that could style it",
      );
    }
    // 3. And the editor's own rule, which is what the check above reasons about.
    if (!reachable.some((selector) => stylesToken(scoreOf)(selector, name, LANGUAGE))) {
      unmatched.push(name);
      errors.push(
        `legend: no rule the editor can resolve reaches '${name}' as the token type of a ${LANGUAGE} token, ` +
          "so the editor would give it no style and drop it while merging the grammar's tokens in",
      );
    }
  }
  for (const key of Object.keys(colorRules)) {
    if (!LEGEND.includes(key)) {
      errors.push(
        `package.json: editor.semanticTokenColorCustomizations.rules styles '${key}', which is no name in ` +
          "the server's advertised legend",
      );
    }
  }
  // A selector that names no language reaches its token type in every language, so what
  // keeps these rules inside Khayyam is where they are contributed, not how their keys
  // are spelled: they are a language-scoped default. A reader's own rule for a standard
  // type therefore still resolves for every other language.
  const scoped = Object.keys(configurationDefaults ?? {}).filter(
    (block) => configurationDefaults?.[block]?.["editor.semanticTokenColorCustomizations"] !== undefined,
  );
  if (scoped.length !== 1 || scoped[0] !== `[${LANGUAGE}]`) {
    errors.push(
      `package.json: editor.semanticTokenColorCustomizations is contributed under [${scoped.join("], [") || "nothing"}] ` +
        `rather than as the language-scoped default [${LANGUAGE}], and a rule whose key names no language ` +
        "reaches its token type in every language",
    );
  }
  const standard = LEGEND.filter((name) => registeredNames.has(name));
  if (standard.length > 0) {
    notes.push(
      `legend: ${standard.length} of ${LEGEND.length} entries are also standard token types the host registers ` +
        `(${standard.join(", ")}), each styled by the rule spelled its own name. They are scoped to Khayyam by ` +
        `where they are contributed - the [${LANGUAGE}] default - and not by the shape of the key, so a reader's ` +
        "own rule for the same standard type is untouched in every other language",
    );
  }
}

// Each theme's own map, judged against the legend now that it is read. A theme that
// carries no value reaches no reader, so this cannot be asked before the legend is.
for (const refusal of judgeSemanticMaps({ themes, legend: LEGEND, variableFor })) errors.push(refusal);

/** The sheet the language-scoped default carries, found by comparing its values with each
 *  offered theme's own - named in the verdict rather than decided here. */
let defaultSheet = "no offered theme";

if (!textMateRules) {
  errors.push(
    "package.json: contributes no [khayyam] textMateRules, so the roles reach the editor only if a user configures them by hand"
  );
} else {
  // The language-scoped default carries ONE sheet - that setting has no theme dimension,
  // so a manifest that named two would be naming one of them and hiding the other. So the
  // values it carries must match ONE of the offered themes exactly - not every theme,
  // which is what a light and a dark sheet together make impossible - and the run's last
  // line names which one, so a reader knows what a reader who selects no theme is given.
  const byScope = settingsByScope(textMateRules);
  for (const scope of byScope.keys()) {
    if (!specScopes.has(scope)) errors.push(`package.json: contributed colour rule styles '${scope}', which no role names`);
  }
  // A role declared server-only names no scope, so it has no contributed colour rule
  // to compare: its value reaches the editor through the semantic rules above, and
  // asking whether a textMateRule matches it would be asking about a rule that cannot
  // exist. So the comparison is over the roles a rule can carry.
  const ruled = roles.filter((role) => (role.scopes ?? []).length > 0);
  const matching = themes.filter(({ theme }) => {
    const declared = theme.khayyamDisplay ?? {};
    return ruled.every((role) => {
      // A role `ruled` holds has a scope, and its own first one is the scope its rule is
      // keyed by; the filter above is what says so, and it is asked again here because a
      // list that has been filtered is not a list whose elements are narrowed.
      const scope = role.scopes?.[0];
      const settings = scope === undefined ? undefined : byScope.get(scope);
      return (
        settings &&
        settings.foreground === declared[variableFor(role.name, "color")] &&
        (settings.fontStyle ?? "") === (declared[variableFor(role.name, "fontStyle")] ?? "")
      );
    });
  });
  if (matching.length === 0) {
    errors.push(
      `package.json: the contributed colour rules match none of the ${themes.length} offered theme(s): ${
        themes.map((entry) => entry.file).join(", ") || "none"
      }`,
    );
  } else {
    const sheets = matching.map((entry) => entry.file).join(", ");
    defaultSheet = sheets;
    notes.push(`package.json: the contributed colour rules are the values of ${sheets}`);
  }
  // The colour rules carry the same sheet as the token rules above, and the reason is the
  // mechanic read out of the editor: a rule that MATCHES a token is not a rule that
  // resolves a style for it, so a rule keyed by the role's own name and carrying no
  // foreground of its own gives the token nothing and the token is then discarded before
  // it can override the grammar. A rule that looks like that is the shape a check has to
  // refuse, because the legend entry is keyed and the selector matches - nothing tells a
  // reader the value is not there.
  for (const role of roles) {
    const rule = colorRules[role.name];
    if (rule === undefined) continue; // already refused: the legend entry keys no rule
    if (typeof rule.foreground !== "string" || rule.foreground === "")
      errors.push(
        `package.json: the colour rule for '${role.name}' carries no foreground, so a host resolves no style for that ` +
          "token type and discards the token before it can override the grammar",
      );
  }
  if (matching.length > 0) {
    const { file, theme } = matching[0];
    const declared = theme.khayyamDisplay ?? {};
    for (const role of roles) {
      const rule = colorRules[role.name];
      if (rule === undefined || typeof rule.foreground !== "string" || rule.foreground === "") continue;
      const color = declared[variableFor(role.name, "color")];
      const fontStyle = declared[variableFor(role.name, "fontStyle")] ?? "";
      if (rule.foreground !== color)
        errors.push(`package.json: the colour rule for '${role.name}' is ${rule.foreground} but ${file} declares ${color}`);
      if ((rule.fontStyle ?? "") !== fontStyle)
        errors.push(
          `package.json: the colour rule for '${role.name}' carries fontStyle '${rule.fontStyle ?? ""}' but ${file} ` +
            `declares '${fontStyle}'`,
        );
    }
  }
  for (const { theme } of themes) {
    for (const role of roles) {
      for (const scope of role.scopes ?? []) {
        if (!byScope.get(scope)) {
          errors.push(`package.json: role '${role.name}' has no contributed colour rule for ${scope}`);
        }
      }
    }
  }
}

if (semanticHighlighting !== true) {
  errors.push(
    "package.json: [khayyam] does not set editor.semanticHighlighting.enabled, so whether semantic tokens are shown at all is left to the active theme, and a theme that does not declare semanticHighlighting discards every role with no error"
  );
}

if (semanticCustomizations?.rules && Array.isArray(semanticCustomizations.rules)) {
  errors.push(
    "package.json: editor.semanticTokenColorCustomizations.rules is an array; the editor reads a rule's own key as its selector, so an array configures nothing and every role it names would be discarded. Use a map from selector to style, keyed by the role's own name."
  );
}

/* ---- the theme values, measured against the contract's own rules ----------- */

const measured = measureValues({ themes, spec, contract });
for (const refusal of measured.errors) errors.push(refusal);

/* ---- the bridge, which is refused rather than checked --------------------- */

/** WHY, in words, because it is a fact about a host and nothing in this repository
 *  states it. Read out of the editor bundle (VS Code 43.6.0,
 *  resources/app/out/vs/workbench/workbench.desktop.main.js), in the colour theme's own
 *  `getTokenStyle` and in the registry's `parseTokenSelector`:
 *
 *  1. A token's style is resolved from the theme's own semantic rules first, then from
 *     the settings' - which is where `editor.semanticTokenColorCustomizations` is read -
 *     and only for the fields those leave unset, from the STYLING DEFAULTS, which is
 *     where `contributes.semanticTokenScopes` registers a probe of TextMate scopes.
 *  2. A style is written when the rule's score is greater than OR EQUAL to the score
 *     already held, so of two rules for one token the later one wins a tie.
 *  3. A rule's score is 100 minus the depth of its type in the token's own type
 *     hierarchy, plus 10 when the rule's key names a language.
 *
 *  A bridge entry names a language on its own entry and the colour rules name none, so
 *  the two do not compete: the bridge scores 110 where the rule scores 100, and it is
 *  applied after it in any case. Its probe then resolves the role's TextMate scope
 *  against the ACTIVE THEME, up the scope hierarchy, and whatever the theme gives that
 *  ordinary scope is the foreground the reader gets - which is why a role reached by a
 *  bridge arrives in the theme's colour for `variable`, `keyword.control` or
 *  `entity.name.function` and not in the value the contract states for it.
 *
 *  The bridge therefore is not a fallback beside the colour rules; for every role it
 *  carries it is the rule that wins. The contract states a value for every role, so a
 *  realization applies that value and contributes no bridge: what a host falls back to
 *  without one is its own default styling for an unknown token type, which is no style
 *  at all - the editor discards the token and the grammar's colour stands - so a reader
 *  who overrides our rules loses the semantic colours rather than inheriting a theme's. */
if (bridge !== undefined) {
  const claimed = (Array.isArray(bridge) ? bridge : [bridge]).flatMap((entry) => Object.keys(entry?.scopes ?? {}));
  errors.push(
    `package.json: contributes semanticTokenScopes${claimed.length === 0 ? "" : ` for [${claimed.join(", ")}]`}, ` +
      "so a host resolves those roles from a TextMate scope probe as well as from the colour rules. It does not " +
      "compete with them: a host applies the styling defaults, where a bridge registers its probe, after the " +
      "settings' rules, and a rule overwrites a score it equals or beats, while the bridge's own `language` field " +
      "scores its selector 10 above a rule keyed the role's own name - so the active theme's value for the probed " +
      "scope replaces the contract's on every role the bridge carries. The contract states a value for every " +
      "role, so a realization applies it and contributes no bridge.",
  );
}

/* ---- report ------------------------------------------------------------- */

const pairs = roles.length * attributeNames.length;
const legendVerdict =
  LEGEND === null
    ? "not read"
    : `${LEGEND.length} token types, ${unreadable.length} carrying a separator, ${unspelled.size} keyed by no ` +
      `contributed colour rule under that spelling, ${unmatched.length} no contributed rule can reach`;

/** The two mechanisms, and the roles each of them answers. A role declared
 *  server-only is the whole of what the grammar cannot reach, so naming them is the
 *  report's first obligation: a reader who sees "20 of 21 roles implemented" and no
 *  name has been told which one is missing and why. */
const byMechanism = `${grammarScopedRoles.length} implemented by a grammar scope, ${serverOnlyRoles.length} declared server-only${
  serverOnlyRoles.length === 0 ? "" : ` (${serverOnlyRoles.join(", ")})`
}`;
const themeCounts = themes
  .map(({ file, theme }) => {
    const declared = theme.khayyamDisplay ?? {};
    const valued = roles.reduce(
      (count, role) =>
        count + attributeNames.filter((attribute) => typeof declared[variableFor(role.name, attribute)] === "string").length,
      0,
    );
    return `${file} ${valued}/${pairs} pairs`;
  })
  .join(", ");

console.log(`contract   : ${shown(specPath)} (${roles.length} roles x ${attributeNames.length} attributes = ${pairs} pairs)`);
console.log(`roles      : ${byMechanism}`);
console.log(
  `kinds      : ${roles.length} roles over ${distinctKinds.size} kinds${
    host.types.size > 0 ? `, read against ${host.path === undefined ? "no host" : shown(host.path)}'s ${host.types.size} registered token types and ${host.modifiers.length} modifiers` : ""
  }: ${superTypedRoles.length} declare a super type, ${rootRoles.length} are this language's own root${
    rootRoles.length === 0 ? "" : ` (${rootRoles.join(", ")})`
  }, ${ownNameRoles.length} stand as a standard type of their own name${
    ownNameRoles.length === 0 ? "" : ` (${ownNameRoles.join(", ")})`
  } and are registered nowhere`,
);
console.log(`grammar    : ${rel(grammarPath)} (${grammarScopes.size} scopes)`);
console.log(`themes     : ${themes.length} (${themeCounts || "none"})`);
console.log(`legend     : ${rel(legendPath)} (${legendVerdict})`);
console.log(
  `palette    : ${themes.length === 0 ? "no theme to measure" : `the lowest measured value is ${Math.min(...measured.lowestPerTheme.values()).toFixed(2)}:1 against a floor of 4.5:1`}, the warm band ${measured.WARM.from}-${measured.WARM.to} is held by the two refusals alone (${measured.refusals.join(", ")}), and ${measured.recordedPairs.length} colour-vision ${measured.recordedPairs.length === 1 ? "pair is" : "pairs are"} recorded with a reason${measured.recordedThemes.length === 0 ? "" : ` (on ${measured.recordedThemes.join(", ")})`}`,
);
for (const note of notes) console.log(`note       : ${note}`);

if (errors.length > 0) {
  console.error(`\nFAIL (${errors.length}):`);
  for (const e of errors) console.error(`  - ${e}`);
  process.exit(1);
}
console.log(
  `\nOK: ${grammarScopedRoles.length} roles implemented by a grammar scope and ${serverOnlyRoles.length} declared ` +
    `server-only${serverOnlyRoles.length === 0 ? "" : ` (${serverOnlyRoles.join(", ")})`}, each with its reason ` +
    `stated in the contract; ${roles.length} roles over ${distinctKinds.size} kinds read against the host's own ` +
    `${host.types.size} registered token types: ${superTypedRoles.length} declare a super type, ${rootRoles.length} are ` +
    `this language's own root${rootRoles.length === 0 ? "" : ` (${rootRoles.join(", ")})`}, ${ownNameRoles.length} stand as ` +
    `a standard type of their own name and are registered nowhere; ${pairs} role-attribute pairs valued in every theme; ` +
    `every one of the ${LEGEND?.length} legend entries is a name the host can match and is carried by ${themes.length} ` +
    `contributed theme${themes.length === 1 ? "" : "s"} under that spelling, each with its own sheet's value, so the ` +
    `contract's value is the one that reaches a reader; the lowest measured value is ` +
    `${Math.min(...measured.lowestPerTheme.values()).toFixed(2)}:1 against a floor of 4.5:1 and the warm band is held by the two ` +
    `refusals alone; the [${LANGUAGE}] default carries ${defaultSheet} for a reader who selects no theme, and the ` +
    "manifest contributes no semanticTokenScopes for a host's theme to overwrite it with.",
);
