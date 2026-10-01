// One theme the manifest contributes, read and judged.
//
// A theme reaches a reader only by being OFFERED: the manifest names it, and a host
// resolves a semantic token's colour out of the theme's own `semanticTokenColors` whether
// or not any setting says so. So everything this module judges is a claim the theme
// makes about the contract - the three fields that identify it to a reader, the value
// its own sheet states, the map a host reads those values out of, the base it rests on,
// and the colours it may not state - and a theme is judged in three passes because two
// of them need what the rest of the check has read first: the map against the legend the
// server advertises, and the values against the palette the contract states.
import { existsSync, readFileSync, readdirSync } from "node:fs";
import { basename, dirname, extname, join, resolve, sep } from "node:path";

/** The JSON documents this module judges, and the view of the contract it judges them
 *  against. A manifest, a theme file and a specification are documents a file format and a
 *  host read at run time and that no declaration anywhere types, so each is declared here
 *  with the fields this module reads - a field whose KIND is the thing under test is
 *  declared `unknown`, because `typeof contribution.label !== "string"` is a refusal and
 *  not a type error.
 *
 *  One role of the contract, as far as this module reads it.
 *  @typedef {{ name: string, scopes?: string[],
 *              kind?: { standardType?: string, isItsOwnName?: boolean, root?: boolean, statement?: string } }} ContractRole
 *
 *  What a colour rule carries: a foreground, and a fontStyle the host format writes only
 *  when a value states one.
 *  @typedef {{ foreground?: string, fontStyle?: string }} StyleSettings
 *
 *  A theme file, as far as this module judges it.
 *  @typedef {{ name?: string, type?: string, include?: unknown, colors?: Record<string, unknown>,
 *              khayyamDisplay?: Record<string, string>, semanticHighlighting?: unknown,
 *              semanticTokenColors?: Record<string, StyleSettings>,
 *              tokenColors?: Array<{ scope?: string | string[], settings?: StyleSettings }> }} ThemeFile
 *
 *  One theme the manifest offers, and one theme as it was read, beside the file it came
 *  from. The label is the reader's picker spelling and the file is what a path resolves to.
 *  @typedef {{ label: string, file: string, path: string, theme: ThemeFile }} ThemeEntry
 *
 *  The contract, read once and handed to this module: the roles, the attributes among
 *  them, the names and scopes among those, the container scopes, and the two spellings
 *  every side of a claim is matched on.
 *  @typedef {{
 *   roles: ContractRole[],
 *   attributeNames: string[],
 *   roleNames: Set<string>,
 *   specScopes: Set<string>,
 *   containerScopes: Set<string>,
 *   variableFor: (role: string, attribute: string) => string,
 *   kindOf: (role: ContractRole) => NonNullable<ContractRole["kind"]>
 * }} ContractView
 *
 *  A recorded colour-vision pair: which sheet it was measured on and the two role names it
 *  is between, spelled `role/role`.
 *  @typedef {{ theme?: string, pair?: string }} RecordedPair
 *
 *  The contract document, as far as the palette rules are read from it.
 *  @typedef {{ palette?: { recordedDichromacyPairs?: { pairs?: RecordedPair[] } } }} Specification
 *
 *  The manifest, as far as this module reads it: the themes it offers, and the
 *  declarations beside them that the same manifest carries.
 *  @typedef {{ contributes?: {
 *    themes?: Array<{ label?: unknown, uiTheme?: unknown, path?: unknown }>,
 *    configurationDefaults?: Record<string, unknown>,
 *    semanticTokenTypes?: Array<{ id?: string, superType?: string, description?: string }>,
 *    semanticTokenScopes?: unknown
 *  } }} ExtensionManifest
 */

/** Reads a JSON document. It answers `unknown` on purpose, and each read says which
 *  document it is holding - so no value reaches a refusal as an untyped one. */
const read = (/** @type {string} */ p) => JSON.parse(readFileSync(p, "utf8"));

/** The name a theme a reader selects must carry. Both sheets are Memar's, and the display
 *  contract they realize is Memar's statement about how a Khayyam source is read; the
 *  theme realizes it and does not own it, so the label a reader's picker shows says whose
 *  theme this is and not what it is for. */
const MEMAR = "Memar";

/** The first pass: every offered contribution against the file it names, and then every
 *  offered theme against the base it rests on. The base walk follows the host's own
 *  reading of `include`, so the ground a theme stands on is walked the way a reader walks
 *  it rather than the way a path is spelled.
 *  @param {{ pkg: ExtensionManifest, themesRoot: string, contract: ContractView,
 *           variableFor: (role: string, attribute: string) => string }} carried
 *  @returns {{ themes: ThemeEntry[], errors: string[], notes: string[] }} */
export function readContributions({ pkg, themesRoot, contract, variableFor }) {
  const { roles, attributeNames, roleNames, specScopes, containerScopes } = contract;
  /** @type {string[]} */
  const errors = [];
  /** @type {string[]} */
  const notes = [];
  const themesDir = join(themesRoot, "themes");

  /** A theme reaches a reader only by being OFFERED: the manifest names it, and a host
   *  resolves a semantic token's colour out of the theme's own `semanticTokenColors` whether
   *  or not any setting says so. That is the whole difference from the language-scoped
   *  default the check holds beside it, which a host reads no semantic colour out of at
   *  all. So the two are counted against each other in both directions - a contribution
   *  naming no file, and a file nothing offers - and a theme is identified by the three
   *  fields the manifest itself carries: the label a reader's picker shows, the uiTheme
   *  the picker marks it by, and the file the path names. No file in this repository names
   *  a theme, so none of them can be right about one on its own. */
  const contributions = pkg.contributes?.themes ?? [];
  if (contributions.length === 0) {
    errors.push(
      "package.json: contributes no theme, so no value the contract states reaches a reader through a mechanism a host " +
        "resolves: a semantic token's colour is read out of a theme's own semanticTokenColors, and a language-scoped " +
        "configuration default is not that mechanism",
    );
  }
/** @type {ThemeEntry[]} */
  const themes = [];
    /** @type {Set<string>} */
    const offered = new Set();
    for (const contribution of contributions) {
      const label = typeof contribution.label === "string" ? contribution.label : "(unnamed)";

    if (typeof contribution.label !== "string" || contribution.label.trim() === "")
      errors.push(
        `package.json: contributes the theme at '${contribution.path}' with no label, so a reader's picker has nothing to select`,
      );
    if (typeof contribution.uiTheme !== "string" || contribution.uiTheme.trim() === "")
      errors.push(`package.json: contributes the theme '${label}' with no uiTheme, so the picker cannot mark it dark or light`);
    if (typeof contribution.path !== "string" || contribution.path.trim() === "") {
      errors.push(`package.json: contributes the theme '${label}' with no path`);
      continue;
    }
    const path = join(themesRoot, contribution.path);
    if (!existsSync(path)) {
      errors.push(
        `package.json: contributes the theme '${label}', whose path '${contribution.path}' names no file the extension ships`,
      );
      continue;
    }
    const file = basename(path);
    offered.add(file);
    const theme = /** @type {ThemeFile} */ (read(path));
    themes.push({ label, file, path, theme });

    // The three fields are each a claim about one file, and two of them disagreeing is a
    // theme a reader sees under one name and is given another.
    if (theme.name !== contribution.label)
      errors.push(
        `package.json: contributes the theme '${label}', but the file it points at is named '${theme.name}'`,
      );
    // The label is what a reader's picker shows, and it is therefore what says whose theme
    // this is. Both sheets are Memar's, and the display contract they realize is Memar's
    // contract for reading Khayyam, so a name that does not say so tells a reader nothing
    // about whose choice of colours they are looking at.
    if (!label.startsWith(MEMAR))
      errors.push(
        `package.json: contributes the theme '${label}', which names no ${MEMAR} theme; the label a reader's picker ` +
          "shows is what says whose theme this is",
      );
    const kind = contribution.uiTheme === "vs-dark" ? "dark" : contribution.uiTheme === "vs" ? "light" : undefined;
    if (kind !== undefined && theme.type !== kind)
      errors.push(
        `package.json: contributes the theme '${label}' as a '${contribution.uiTheme}' theme, but the file it points at is a '${theme.type}' one`,
      );

    const declared = theme.khayyamDisplay ?? null;
    if (!declared) {
      errors.push(`theme '${file}': has no 'khayyamDisplay' map, so it states no value for any role-attribute pair`);
      continue;
    }

    // every value the theme supplies must name a known role and a known attribute
    for (const variable of Object.keys(declared)) {
      const parts = variable.split(".");
      if (parts[0] !== "khayyam" || parts.length !== 3) {
        errors.push(`theme '${file}': value '${variable}' is not keyed khayyam.<role>.<attribute>`);
        continue;
      }
      const [, role, attribute] = parts;
      if (!roleNames.has(role)) errors.push(`theme '${file}': supplies a value for unknown role '${role}'`);
      if (!attributeNames.includes(attribute))
        errors.push(`theme '${file}': supplies a value for unknown attribute '${attribute}' (role '${role}')`);
    }

    // every required role-attribute pair must have a value
    for (const role of roles) {
      for (const attribute of attributeNames) {
        const variable = variableFor(role.name, attribute);
        if (!(variable in declared)) errors.push(`theme '${file}': no value for '${variable}'`);
        else if (typeof declared[variable] !== "string")
          errors.push(`theme '${file}': value for '${variable}' is not a string`);
      }
    }

    // the host-format rules must agree with the declared values
    const ruleFor = new Map();
    for (const rule of theme.tokenColors ?? []) {
      for (const scope of [rule.scope].flat()) ruleFor.set(scope, rule.settings ?? {});
    }
    for (const role of roles) {
      const color = declared[variableFor(role.name, "color")];
      const fontStyle = declared[variableFor(role.name, "fontStyle")];
      if (color === undefined) continue;
      for (const scope of role.scopes ?? []) {
        const settings = ruleFor.get(scope);
        if (!settings) {
          errors.push(`theme '${file}': role '${role.name}' has no tokenColors rule for ${scope}`);
          continue;
        }
        if (settings.foreground !== color)
          errors.push(
            `theme '${file}': ${scope} is ${settings.foreground} but ${variableFor(role.name, "color")} declares ${color}`
          );
        const styled = settings.fontStyle ?? "";
        if (styled !== (fontStyle ?? ""))
          errors.push(
            `theme '${file}': ${scope} carries fontStyle '${styled}' but ${variableFor(role.name, "fontStyle")} declares '${fontStyle ?? ""}'`
          );
      }
    }
    for (const scope of ruleFor.keys()) {
      if (!specScopes.has(scope)) errors.push(`theme '${file}': styles scope '${scope}', which no role names`);
    }
    for (const scope of containerScopes) {
      if (ruleFor.has(scope)) errors.push(`theme '${file}': styles container scope '${scope}', which must carry no value`);
    }

    // A theme's own colour contribution is the contract's twenty-one roles and nothing
    // else, and the base it includes states the workbench's colours. A workbench colour
    // stated here is a second copy of one the base already carries, and a second copy is a
    // copy that will drift from the base the next time the base changes - which is the whole
    // of what a base is for. The `tokenColors` rules above are held to the same line already:
    // a rule for a scope no role names is a colour outside the contract's roles, in the
    // shape the host reads for a language.
    for (const id of Object.keys(theme.colors ?? {})) {
      errors.push(
        `theme '${file}': states the workbench colour '${id}', which is no role the contract names: this theme's ` +
          "colours are the twenty-one roles and its base states the workbench's, and a second statement of one of them " +
          "is a copy that will drift from it",
      );
    }
  }

  /* ---- the base each offered theme rests on -------------------------------- */

  /** A contributed colour theme REPLACES the active one outright, so what a reader gets by
   *  selecting one is the whole window and not only the code's colours. These carry values
   *  for the twenty-one roles and for no other language, so a reader who selected one as
   *  they stood lost every other language's colours (measured against the real highlighter:
   *  0 of 26 Python tokens kept a colour, against 26 of 26 under Dark+). What a theme rests
   *  on is therefore not a detail of it: it is what every other file in the window is drawn
   *  with, and the run says which base that is rather than leaving it to be discovered.
   *
   *  HOW A HOST READS `include`, read out of the editor's own bundle (VS Code 43.6.0,
   *  `resources/app/out/vs/workbench/workbench.desktop.main.js`), in the colour theme's own
   *  `load` and the function it calls, where the identifiers survive:
   *
   *  1. `extname(location) === ".json"` decides the branch: a `.json` include is read as a
   *     colour theme and anything else as a TextMate theme (the same function's other half).
   *  2. `joinPath(dirname(location), theme.include)` is where the include is resolved - a
   *     path relative to the file that states it, and nothing else. There is no lookup by a
   *     theme's label or its `settingsId` anywhere on that path, so naming a theme the host
   *     already ships resolves to a file of that name in this extension's own folder, and
   *     that file does not exist.
   *  3. The read is `readExtensionResource`, and the base is read BEFORE the theme that
   *     includes it - the including file's own `colors` are then applied over what the base
   *     gave, which is why a theme that restates one of them owns a copy of it.
   *  4. It recurses, so the base's own `include` is part of the chain, and the deepest base
   *     is read first - so the last statement of a colour in the chain is the one a reader
   *     gets.
   *
   *  What that rules out is a base named by identity, and what it requires is a file the
   *  extension ships: the check therefore refuses a base that is not there, one that
   *  resolves outside the folder a contributed path is resolved against (a path on this
   *  machine is not something a reader of the extension receives), one that is not a JSON
   *  object, and a chain that includes itself. A `.tmTheme` include is a legitimate way to
   *  bring token colours in and this check does not read those files, so it reports the
   *  base as unconfirmed rather than passing a chain it has not walked. */
  const themesRootAbs = resolve(themesRoot);
  /** @param {string} p @returns {boolean} */
  const insideExtension = (p) => {
    const at = resolve(p);
    return at === themesRootAbs || at.startsWith(themesRootAbs + sep);
  };
  /** The base files the chain reached, by name, so the count below can tell a file a theme
   *  rests on from a file nothing reaches. */
  /** @type {Set<string>} */
  const based = new Set();

  for (const { file, path: themePath, theme } of themes) {
    if (typeof theme.include !== "string" || theme.include.trim() === "") {
      errors.push(
        `theme '${file}': includes no base theme, so selecting it gives the reader this extension's twenty-one roles ` +
          "and no other language's colours, and every other file in the window is left uncoloured",
      );
      continue;
    }
    /** @type {string[]} */
    const chain = [];
    /** @type {Set<string>} */
    const seen = new Set([resolve(themePath)]);
    let holder = file;
    let from = themePath;
    let include = theme.include;
    let background;
    /** Whether the chain was walked to its end: a note naming a base is only true of a base
     *  the walk reached, and a walk that stopped at a fault has already said so. */
    let walked = true;
    /** @type {(message: string) => void} */
  const fault = (message) => {
      errors.push(message);
      walked = false;
    };
    for (;;) {
      const base = resolve(join(dirname(from), include));
      // 2. A base the reader is not given is not a base. The boundary is the root this run
      //    resolves contributed paths against, so a run asked about a copy of the themes is
      //    asked the question a run over the shipped ones is asked.
      if (!insideExtension(base)) {
        fault(
          `theme '${holder}': includes '${include}', which resolves outside the folder a contributed path is ` +
            "resolved against, so the base would be a file on this machine and not one the extension ships",
        );
        break;
      }
      // 1. A `.tmTheme` is a base this check does not read, and refusing one would refuse a
      //    legitimate theme; so it is reported, not passed.
      if (extname(base) !== ".json") {
        walked = false;
        notes.push(
          `theme '${holder}': includes '${include}', which a host reads as a TextMate theme rather than a colour ` +
            "theme, and which this check does not read, so the base it reaches is unconfirmed",
        );
        break;
      }
      if (!existsSync(base)) {
        fault(
          `theme '${holder}': includes '${include}', which names no file the extension ships, so a host reading it ` +
            "has no base and every other language's tokens are left uncoloured",
        );
        break;
      }
      let sheet;
      try {
        sheet = /** @type {ThemeFile} */ (read(base));
      } catch (faultReading) {
        fault(
          `theme '${holder}': includes '${include}', which is not readable as JSON (${
            faultReading instanceof Error ? faultReading.message : String(faultReading)
          }), so a host reading it has no base`,
        );
        break;
      }
      if (sheet === null || typeof sheet !== "object" || Array.isArray(sheet)) {
        fault(
          `theme '${holder}': includes '${include}', which is not a JSON object, and a host reads anything else as a ` +
            "theme file it cannot use",
        );
        break;
      }
      if (seen.has(resolve(base))) {
        fault(
          `theme '${holder}': includes '${include}', which the chain already includes, so a host reading it never ` +
            "reaches a base",
        );
        break;
      }
      seen.add(resolve(base));
      based.add(basename(base));
      chain.push(basename(base));
      // 4. The base is read deepest-first, so the statement NEAREST the theme is the last
      //    one applied and the one a reader gets - which is the first statement met walking
      //    outward from the theme.
      if (background === undefined && typeof sheet.colors?.["editor.background"] === "string")
        background = sheet.colors["editor.background"];
      if (typeof sheet.include === "string" && sheet.include.trim() !== "") {
        holder = basename(base);
        from = base;
        include = sheet.include;
        continue;
      }
      break;
    }
    if (walked)
      notes.push(
        `theme '${file}': rests on ${chain.join(" -> ")}, which the extension ships and a host reads before this ` +
          "theme's own values: the base gives the workbench its colours and every other language its token colours " +
          `(its editor.background is ${background ?? "stated by no base in the chain"}), and this theme overrides ` +
          "none of them",
      );
  }

  // The other direction of the same count: a theme file neither offered nor included is a
  // sheet whose values reach no reader at all, and it is the shape a file left behind after
  // a contribution was dropped takes.
  for (const file of readdirSync(themesDir).filter((f) => f.endsWith(".json"))) {
    if (!offered.has(file) && !based.has(file))
      errors.push(
        `package.json: ships the theme file '${file}', which no contributed theme offers and no offered theme ` +
          "includes as its base, so its values reach no reader",
      );
  }

  return { themes, errors, notes };
}

/** The second pass: the map a host reads a role's value out of, against the legend the
 *  server actually advertises.
 *  @param {{ themes: ThemeEntry[], legend: string[] | null,
 *           variableFor: (role: string, attribute: string) => string }} carried
 *  @returns {string[]} */
export function judgeSemanticMaps({ themes, legend, variableFor }) {
  /** @type {string[]} */
  const errors = [];
  if (legend === null) return errors; // the failure is already recorded; there is nothing to compare
  for (const { file, theme } of themes) {
    // A theme is the mechanism a host reads a semantic token's colour out of, and it reads
    // it from the theme's own `semanticTokenColors`, keyed by the token TYPE. So the legend
    // is the key set every offered theme must carry, spelled exactly as the server
    // advertises it, and a theme's own sheet is where each value must come from: two sheets
    // holding one value would be one sheet offered twice, and a reader who selected the
    // other theme would be reading this one.
    //
    // The opt-in is the first of the two, because it is the one a theme can omit and a host
    // gives no error for: a theme declaring no `semanticHighlighting` is given no semantic
    // highlighting at all, and every value in the map below is then read by nothing.
    if (theme.semanticHighlighting !== true) {
      errors.push(
        `theme '${file}': declares no semanticHighlighting, so a host gives it no semantic highlighting at all and ` +
          "every value in its semanticTokenColors is read by nothing",
      );
    }
    const colours = theme.semanticTokenColors;
    if (colours === null || typeof colours !== "object" || Array.isArray(colours)) {
      errors.push(
        `theme '${file}': has no semanticTokenColors map, so a host reads none of the contract's values out of it and ` +
          "resolves no style for any token type",
      );
      continue;
    }
    const sheet = theme.khayyamDisplay ?? {};
    for (const name of legend) {
      if (!(name in colours)) {
        errors.push(
          `theme '${file}': semanticTokenColors carries no '${name}', which the server's advertised legend spells ` +
            "exactly that way, so a host resolves no style for that token type and discards the token",
        );
        continue;
      }
      const style = colours[name] ?? {};
      const color = sheet[variableFor(name, "color")];
      const fontStyle = sheet[variableFor(name, "fontStyle")] ?? "";
      if (style.foreground !== color)
        errors.push(`theme '${file}': semanticTokenColors.${name} is ${style.foreground} but khayyamDisplay declares ${color}`);
      if ((style.fontStyle ?? "") !== fontStyle)
        errors.push(
          `theme '${file}': semanticTokenColors.${name} carries fontStyle '${style.fontStyle ?? ""}' but khayyamDisplay ` +
            `declares '${fontStyle}'`,
        );
    }
    for (const key of Object.keys(colours)) {
      if (!legend.includes(key))
        errors.push(
          `theme '${file}': semanticTokenColors carries '${key}', which is no name in the server's advertised legend`,
        );
    }
  }
  return errors;
}

/** The third pass: the values a theme states, measured against the contract's own palette
 *  rules. A theme is not a set of values; it is a derivation from rules, and a rule that
 *  cannot fail is not a rule. So the values are measured here, in the same five steps the
 *  derivation used: OKLCH built and converted to sRGB with anything outside the gamut
 *  refused rather than clipped; contrast by the WCAG 2.x relative-luminance definition
 *  against the background THAT theme states, read from its own base chain; a
 *  colour-vision deficiency estimated with the Machado, Oliveira and Fernandes (2009)
 *  matrices at severity 1.0 in linear RGB and measured in CIE L*a*b* (D65) as dE76. The
 *  dE76 figures are an estimate of what a reader perceives and not a measurement of it.
 *  @param {{ themes: ThemeEntry[], spec: Specification, contract: ContractView }} carried
 *  @returns {{ errors: string[], lowestPerTheme: Map<string, number>, refusals: string[],
 *             WARM: { from: number, to: number, minChroma: number },
 *             recordedPairs: RecordedPair[], recordedThemes: string[] }} */
export function measureValues({ themes, spec, contract }) {
  const { roles, kindOf, variableFor } = contract;
  /** @type {string[]} */
  const errors = [];
  /** @param {number} x @returns {number} */
  const clamp01 = (x) => (x < 0 ? 0 : x > 1 ? 1 : x);
  /** @param {number} c @returns {number} */
  const gammaOf = (c) => (c <= 0.0031308 ? 12.92 * c : 1.055 * Math.pow(c, 1 / 2.4) - 0.055);
  /** @param {number} c @returns {number} */
  const degammaOf = (c) => (c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4));
  /** The three gamma-encoded channels of a hex triple, as the TUPLE they are: the map below
   *  is what turns a hex triple into a triple, and a tuple is the type that says so rather
   *  than an array of some length.
   *  @param {string} hex @returns {[number, number, number] | null} */
  const hexToRgb = (hex) => {
    const h = String(hex).replace("#", "");
    if (!/^[0-9a-fA-F]{6}$/.test(h)) return null;
    return /** @type {[number, number, number]} */ ([0, 2, 4].map((i) => parseInt(h.slice(i, i + 2), 16) / 255));
  };
  /** The three channels, degenerate-mapped: `map` over a tuple answers an array, and a
   *  triple is still a triple, so the tuple is restated at the two places that destructure
   *  one rather than left to an array of no stated length.
   *  @param {[number, number, number]} rgb
   *  @returns {[number, number, number]} */
  const linearChannelsOf = (rgb) => /** @type {[number, number, number]} */ (rgb.map(degammaOf));

  /** @param {number} r @param {number} g @param {number} b @returns {number[]} */
  const linearToOklab = (r, g, b) => {
    const l = Math.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b);
    const m = Math.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b);
    const s = Math.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b);
    return [0.2104542553 * l + 0.793617785 * m - 0.0040720468 * s, 1.9779984951 * l - 2.428592205 * m + 0.4505937099 * s, 0.0259040371 * l + 0.7827717662 * m - 0.808675766 * s];
  };
  /** @param {[number, number, number]} rgb
   *  @returns {{ L: number, C: number, H: number }} */
  const oklchOf = (rgb) => {
    const [L, a, b] = linearToOklab(...linearChannelsOf(rgb));
    let H = (Math.atan2(b, a) * 180) / Math.PI;
    if (H < 0) H += 360;
    return { L: L * 100, C: Math.hypot(a, b), H };
  };
  /** @param {[number, number, number]} rgb @returns {number} */
  const luminanceOf = (rgb) => {
    const [r, g, b] = linearChannelsOf(rgb);
    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
  };
  /** @param {[number, number, number]} a @param {[number, number, number]} b @returns {number} */
  const contrastOf = (a, b) => {
    const [hi, lo] = [luminanceOf(a), luminanceOf(b)].sort((x, y) => y - x);
    return (hi + 0.05) / (lo + 0.05);
  };
  /** @param {[number, number, number]} rgb @returns {number} */
  const lStarOf = (rgb) => {
    const y = luminanceOf(rgb);
    return y > 0.008856 ? 116 * Math.cbrt(y) - 16 : 903.3 * y;
  };
  /** The Machado, Oliveira and Fernandes (2009) matrix per deficiency, each the nine
   *  coefficients of a 3x3 transform in linear RGB. A key here is the deficiency this run
   *  simulates, and the loop over `Object.keys` names every one of them, so the table is
   *  an open map: a matrix added below is simulated without this file being told.
   *  @type {Record<string, number[]>} */
  const MACHADO = {
    protanopia: [0.152286, 1.052583, -0.204868, 0.114503, 0.786281, 0.099216, -0.003882, -0.048116, 1.051998],
    deuteranopia: [0.367322, 0.860646, -0.227968, 0.280085, 0.672501, 0.047413, -0.011820, 0.042940, 0.968881],
    tritanopia: [1.255528, -0.076749, -0.178779, -0.078411, 0.930809, 0.147602, 0.004733, 0.691367, 0.303900],
  };
  /** @param {[number, number, number]} rgb three gamma-encoded channels
   *  @param {string} kind
   *  @returns {[number, number, number]} */
  const simulate = (rgb, kind) => {
    const m = MACHADO[kind];
    const [r, g, b] = linearChannelsOf(rgb);
    // The simulated colour is written to 8 bits a channel and read back, because 8 bits a
    // channel is what a display can show and the number being estimated is what a reader
    // would see. It is answered as the channels rather than as a hex string, and the
    // division by 255 is the same one `hexToRgb` applies, so this is the value the round
    // trip through those two hex digits answered.
    return /** @type {[number, number, number]} */ (
      [m[0] * r + m[1] * g + m[2] * b, m[3] * r + m[4] * g + m[5] * b, m[6] * r + m[7] * g + m[8] * b]
        .map((v) => Math.round(clamp01(gammaOf(clamp01(v))) * 255) / 255)
    );
  };
  /** A triple, in CIE L*a*b* (D65). */
  /** @param {[number, number, number]} rgb
   *  @returns {number[]} */
  const labOfRgb = ([r, g, b]) => {
    const x = (0.4124564 * r + 0.3575761 * g + 0.1804375 * b) / 0.95047;
    const y = 0.2126729 * r + 0.7151522 * g + 0.072175 * b;
    const z = (0.0193339 * r + 0.119192 * g + 0.9503041 * b) / 1.08883;
    /** @param {number} t @returns {number} */
    const f = (t) => (t > 0.008856 ? Math.cbrt(t) : 7.787 * t + 16 / 116);
    const [fx, fy, fz] = [f(x), f(y), f(z)];
    return [116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)];
  };
  /** Two triples, dE76 apart. A simulated colour is never written back as a hex, because
   *  rounding it to 8 bits first would put a quantisation error into the one number a
   *  reader's vision is estimated by. */
  /** @param {[number, number, number]} a @param {[number, number, number]} b
   *  @returns {number} */
  const deltaE = (a, b) => {
    const [l1, a1, b1] = labOfRgb(linearChannelsOf(a)), [l2, a2, b2] = labOfRgb(linearChannelsOf(b));
    return Math.hypot(l1 - l2, a1 - a2, b1 - b2);
  };
  /** The family a role is read in, which is what the palette's rules are stated over: a
   *  role and another role of a different kind are told apart by hue, and two roles of one
   *  family are the pairs the colour-vision rule is about. */
  /** @param {ContractRole} role @returns {string} */
  const familyOf = (role) => {
    const kind = kindOf(role);
    if (kind.root === true) return role.name.startsWith("invalid-") ? "refusal" : "not-a-name";
    if (kind.standardType === "keyword") return "word";
    // A role whose kind names no standard type is in no family, and a membership test over
    // a list of names is asked about it only after `root` and `keyword` have been ruled
    // out - so the name is read as the optional thing it is rather than as a `string`.
    if (kind.standardType !== undefined) {
      if (["property", "variable", "parameter"].includes(kind.standardType)) return "name";
      if (["type", "class", "interface", "method"].includes(kind.standardType)) return "Type";
      if (kind.standardType === "scope") return "Type";
    }
    return "not-a-name";
  };
  const refusals = roles.filter((role) => role.name.startsWith("invalid-")).map((role) => role.name);
  const WARM = { from: 15, to: 120, minChroma: 0.05 };
  /** @param {{ C: number, H: number }} m @returns {boolean} */
  const isWarm = (m) => m.C >= WARM.minChroma && m.H >= WARM.from && m.H <= WARM.to;
  const NEUTRAL_CHROMA = 0.05;
  /** @param {number} a @param {number} b @returns {number} */
  const hueGap = (a, b) => {
    const d = Math.abs(a - b) % 360;
    return Math.min(d, 360 - d);
  };
  const recordedPairs = spec.palette?.recordedDichromacyPairs?.pairs ?? [];
  /** Which sheets the records are about, so the report says a record is on a sheet rather
   *  than leaving a reader to wonder whether it applies to the one in front of them. */
  const recordedThemes = [
    ...new Set(recordedPairs.map((entry) => entry.theme).filter((theme) => theme !== undefined)),
  ].sort();
  /** A recorded pair names two ROLES, and a pair of roles is a pair of VALUES: three roles
   *  of one kind may share one value, and a decision about two of them is a decision about
   *  the two colours. So the match is by the value each name carries, and a third role
   *  carrying the same value as a recorded one is covered by that record. */
  /** @param {string} themeName @param {{ hex: string }} ra @param {{ hex: string }} rb
   *  @param {Map<string, string>} byName @returns {boolean} */
  const recordedFor = (themeName, ra, rb, byName) => {
    /** @param {string} name @returns {string | undefined} */
    const valueOf = (name) => (typeof name === "string" ? byName.get(name) : undefined);
    return recordedPairs.some((entry) => {
      const names = String(entry.pair ?? "").split("/");
      return (
        entry.theme === themeName &&
        ((valueOf(names[0]) === ra.hex && valueOf(names[1]) === rb.hex) ||
          (valueOf(names[1]) === ra.hex && valueOf(names[0]) === rb.hex))
      );
    });
  };
  /** @type {Map<string, number>} */
  const lowestPerTheme = new Map();

  for (const { file, path: themePath, theme } of themes) {
    const declared = theme.khayyamDisplay ?? {};
    // The background is the base chain's, not this file's: a contributed theme states no
    // workbench colour of its own, and the contrast floor is measured against what a
    // reader's window actually is behind it.
    let background;
    for (let at = themePath, sheet = theme; ; ) {
      if (typeof sheet.colors?.["editor.background"] === "string") { background = sheet.colors["editor.background"]; break; }
      if (typeof sheet.include !== "string" || sheet.include === "") break;
      const next = join(dirname(at), sheet.include);
      if (!existsSync(next)) break;
      at = next;
      sheet = /** @type {ThemeFile} */ (read(next));
    }
    if (typeof background !== "string") {
      errors.push(
        `theme '${file}': no base in its chain states editor.background, so the contract's contrast floor cannot be ` +
          "measured against what a reader would actually see behind this sheet",
      );
      continue;
    }
    // A background that is a string is not yet a colour: `hexToRgb` refuses anything that
    // is not six hex digits, and the measurement below needs the three channels, so the
    // refusal is made here where the base chain is being read rather than left to throw
    // from a `map` over nothing.
    const behind = hexToRgb(background);
    if (behind === null) {
      errors.push(
        `theme '${file}': editor.background is '${background}', which is not a hex triple, so the contract's contrast ` +
          "floor cannot be measured against what a reader would actually see behind this sheet",
      );
      continue;
    }
    /** The channels and the numbers derived from them, per role. The channels are carried
     *  because the hex was decoded to get here and a well-formed triple is what a decode
     *  answers, so nothing below has to ask whether the hex decodes.
     *  @type {Map<string, { hex: string, rgb: [number, number, number],
     *    L: number, C: number, H: number, lStar: number }>} */
    const measured = new Map();
    for (const role of roles) {
      const hex = declared[variableFor(role.name, "color")];
      const rgb = typeof hex === "string" ? hexToRgb(hex) : null;
      if (rgb === null) continue; // a missing or malformed value is already refused above
      measured.set(role.name, { hex, rgb, ...oklchOf(rgb), lStar: lStarOf(rgb) });
    }
    for (const [name, value] of measured) {
      const ratio = contrastOf(value.rgb, behind);
      const lowest = lowestPerTheme.get(file);
      if (lowest === undefined || ratio < lowest) lowestPerTheme.set(file, ratio);
      if (ratio < 4.5)
        errors.push(
          `theme '${file}': '${name}' is ${value.hex}, ${ratio.toFixed(2)}:1 against that theme's own background ` +
            `${background}, and the floor is 4.5:1. The floor is one number for the whole palette and no role holds an ` +
            "exemption from it.",
        );
      const warm = isWarm(value);
      if (warm && !refusals.includes(name))
        errors.push(
          `theme '${file}': '${name}' is warm (OKLCH hue ${value.H.toFixed(0)}, chroma ${value.C.toFixed(3)}, inside ` +
            `the band ${WARM.from}-${WARM.to}) and is not one of the two refusals. Warm means error and nothing else.`,
        );
      if (!warm && refusals.includes(name))
        errors.push(
          `theme '${file}': '${name}' is one of the two refusals and is not warm (OKLCH hue ${value.H.toFixed(0)}, chroma ` +
            `${value.C.toFixed(3)}), so the one place a reader is told the file is wrong has no band of its own.`,
        );
    }
    // Hue is the kind's, and lightness and chroma are the role's position in it.
    for (let i = 0; i < roles.length; i += 1)
      for (let j = i + 1; j < roles.length; j += 1) {
        const [ra, rb] = [roles[i], roles[j]];
        const a = measured.get(ra.name), b = measured.get(rb.name);
        if (a === undefined || b === undefined) continue;
        const sameKind =
          familyOf(ra) === familyOf(rb) &&
          kindOf(ra).standardType !== undefined &&
          kindOf(ra).standardType === kindOf(rb).standardType;
        const shareAValue = a.hex === b.hex;
        const dh = hueGap(a.H, b.H), dl = Math.abs(a.lStar - b.lStar), dc = Math.abs(a.C - b.C);
        if (sameKind) {
          if (shareAValue) continue; // two roles of one kind may share a value, and the contract permits it
          if (dh > 6)
            errors.push(
              `theme '${file}': '${ra.name}' and '${rb.name}' are one kind (${kindOf(ra).standardType}) and their hues differ by ` +
                `${dh.toFixed(0)} degrees. A super type carries kind and nothing else, so origin and validity have nowhere ` +
                "else to go: they are carried by lightness and by chroma, and never by hue.",
            );
          if (dl < 8 || dc < 0.005)
            errors.push(
              `theme '${file}': '${ra.name}' and '${rb.name}' are one kind (${kindOf(ra).standardType}) and are told apart by ` +
                `dL* ${dl.toFixed(1)} and dC ${dc.toFixed(3)}, where the rule is at least 8 L* and at least 0.005 of chroma`,
            );
          continue;
        }
        const an = a.C < NEUTRAL_CHROMA, bn = b.C < NEUTRAL_CHROMA;
        if (an !== bn) {
          if (dc < 0.025 && dl < 8)
            errors.push(
              `theme '${file}': '${ra}' and '${rb}' are one neutral and one chromatic (dC ${dc.toFixed(3)}, dL* ` +
                `${dl.toFixed(1)}), where the rule is at least 0.025 of chroma or 8 L*`,
            );
          continue;
        }
        if (an && bn) {
          if (dl < 8)
            errors.push(
              `theme '${file}': '${ra}' and '${rb}' are two kinds of the neutral lane and are told apart by dL* ` +
                `${dl.toFixed(1)}, where the rule is at least 8 L*`,
            );
          continue;
        }
        if (dh < 20 && dl < 12)
          errors.push(
            `theme '${file}': '${ra}' and '${rb}' are told apart by neither hue nor lightness (dH ${dh.toFixed(0)}, dL* ` +
              `${dl.toFixed(1)}), where the rule is at least 20 degrees of hue or at least 12 L*`,
          );
      }
    // Colour-vision: a pair below dE76 10 is a decision, and a decision is recorded here.
    for (let i = 0; i < roles.length; i += 1)
      for (let j = i + 1; j < roles.length; j += 1) {
        const [ra, rb] = [roles[i], roles[j]];
        const a = measured.get(ra.name), b = measured.get(rb.name);
        if (a === undefined || b === undefined) continue;
        if (familyOf(ra) !== familyOf(rb)) continue;
        if (a.hex === b.hex) continue; // one value, and the contract permits two roles to share one
        if ((declared[variableFor(ra.name, "fontStyle")] ?? "") !== (declared[variableFor(rb.name, "fontStyle")] ?? "")) continue;
        const themeName = file.replace(/^khayyam-/, "").replace(/\.json$/, "");
        const byName = new Map([...measured].map(([name, value]) => [name, value.hex]));
        let worst = Infinity, worstKind = "";
        for (const kind of Object.keys(MACHADO)) {
          const d = deltaE(simulate(a.rgb, kind), simulate(b.rgb, kind));
          if (d < worst) { worst = d; worstKind = kind; }
        }
        if (worst < 10 && !recordedFor(themeName, a, b, byName))
          errors.push(
            `theme '${file}': '${ra.name}' and '${rb.name}' are ${worstKind} ${worst.toFixed(1)} apart, and the contract records ` +
              "no such pair. A pair that falls under dE76 10 is a decision and the contract's " +
              "`palette.recordedDichromacyPairs` is where the decision goes; a pair that fails silently is the defect.",
          );
      }
  }

  return { errors, lowestPerTheme, refusals, WARM, recordedPairs, recordedThemes };
}
