// The host's own classification, read out of the installed product.
//
// A provider's own type is styled by a rule keyed that type, whatever else a theme
// styles; what a SUPER TYPE buys is that a rule keyed the standard type reaches it too,
// because a host matches a rule's key against the token's whole type hierarchy and the
// hierarchy is built only from super types someone declared. So the list of standard
// types is not a matter of taste and it is not a matter of memory: it is whatever the
// host registers, and it is read out of the host's own bundle here, because a list
// written into a check would agree with any contract and the defect the check exists to
// catch was exactly a name every derivation in the tree agreed with.
//
// READ OUT OF THE PRODUCT, VS Code 43.6.0, resources/app/out/vs/workbench/
// workbench.desktop.main.js. `function T4n()` is the host registering its own
// classification at load: twenty-four `registerTokenType` calls and eight
// `registerTokenModifier` calls, and the two identifiers survive in the minified text,
// so a reader finds every claim below by searching for them.
//
// It is not the list the protocol's own specification names. This host registers `member`
// and not `modifier`, and no `defaultLibrary`, so a decision about which names exist is
// made against this list, because this list is the one the host enforces.
//
// The arithmetic is here too, and for the same reason: how a host reads a rule's key,
// how deep in a token's hierarchy that key sits, and what the match scores are all
// facts about the host and are read out of the same bundle, so a check states them in
// the host's own numbers rather than asserting them.
import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";

/** A rule's key, read the way the editor reads it: the token type, whole, and the language
 *  a selector names, if it names one. The same shape `parseSelector` answers at the bottom
 *  of this file and the same shape `client.js` reads a rule key into.
 *  @typedef {{ type: string, language?: string }} Selector

/** One entry of an extension's `contributes.semanticTokenTypes`: the token types the host is
 *  told this extension registers, each with the standard type it was declared to extend.
 *  The manifest is a document a host reads at run time and types nowhere, so the two fields
 *  this module reads are stated here rather than left to inference - and the `id` is
 *  optional, because a manifest may omit it and that omission is a refusal `verify-roles`
 *  makes rather than a fact about every entry.
 *  @typedef {{ id?: string, superType?: string }} DeclaredType

/** What the host's own bundle said, once read: where it was found and where it was looked
 *  for, every token type it registers mapped to the super type it registered THAT one
 *  under (no super type reads as `undefined`, which is how the host spells it), every
 *  modifier it registers, and what could not be read - a fault rather than an empty answer.
 *  @typedef {{
 *   path: string | undefined,
 *   tried: string[],
 *   types: Map<string, string | undefined>,
 *   modifiers: string[],
 *   faults: string[]
 * }} HostClassification

/** The editor's own token-id and selector patterns. */
export const TOKEN_ID = /^\w+[-_\w+]*$/;
export const SELECTOR = /^(\w+[-_\w+]*|\*)(\.\w+[-_\w+]*)*(:\w+[-_\w+]*)?$/;
/** What a host reads as the boundary inside a name: the same two characters its own
 *  selector rule splits on. */
export const SEPARATOR = /[.$]/;

/** Used ONLY when the host's bundle could not be read, which is already a refusal by
 *  the check that runs this. It is kept so a run that cannot reach the product still
 *  says something, and it is marked as what it is: a memory, and the thing the check
 *  refuses to rely on. An open map keyed by a token-type name, for the reason `client.js`
 *  states for its own table: a key is a name the host registers and the host registers
 *  names no list here has read, so a name this table does not hold answers `undefined`.
 *  @type {Record<string, string[]>} */
const STANDARD_FALLBACK = {
  class: ["class", "type"],
  comment: ["comment"],
  decorator: ["decorator"],
  enum: ["enum", "type"],
  enumMember: ["enumMember"],
  event: ["event"],
  function: ["function", "method"],
  interface: ["interface", "type"],
  keyword: ["keyword"],
  macro: ["macro"],
  method: ["method", "function"],
  modifier: ["modifier"],
  namespace: ["namespace"],
  number: ["number"],
  operator: ["operator"],
  parameter: ["parameter", "variable"],
  property: ["property"],
  regexp: ["regexp", "string"],
  string: ["string"],
  struct: ["struct", "type"],
  typeParameter: ["typeParameter", "type"],
  variable: ["variable"],
};

/** One candidate's place, as the PARTS it is spelled in, and the path it is when every
 *  part is there. A product's install root is an environment variable, and each of these
 *  names one the running platform may not have at all: `LOCALAPPDATA` and `ProgramFiles`
 *  are absent on a POSIX machine, and `join` over a part that is absent throws rather than
 *  answering the path it was asked for - so the verifier did not run there, on the one
 *  platform where the editor is not installed and the fault it reports is the right one.
 *  A candidate with a part missing is dropped whole, because there is no path under a root
 *  that does not exist, and the survivors are joined from a `string[]` - the shape the
 *  `path` module's own signature is - so this is the one place a missing part can be caught
 *  and the type says it cannot happen again.
 *  @param {(string | undefined)[]} parts
 *  @returns {string | undefined} */
const pathOf = (parts) => {
  /** @type {string[]} */
  const present = [];
  for (const part of parts) {
    if (typeof part !== "string" || part === "") return undefined;
    present.push(part);
  }
  return join(...present);
};

/** Every place the host's own bundle may be, for the environment given. It takes the
 *  environment rather than reading it so that a platform this run is not can be asked
 *  about directly - which is the whole of the fault this shape exists to answer.
 *  @param {Record<string, string | undefined>} env
 *  @returns {string[]} */
export const hostRootsOf = (env) =>
  [
    pathOf([env.KHAYYAM_HOST_BUNDLE]),
    pathOf([env.LOCALAPPDATA, "Programs", "Microsoft VS Code", "resources", "app", "out", "vs", "workbench", "workbench.desktop.main.js"]),
    pathOf([env.LOCALAPPDATA, "Programs", "Microsoft VS Code Insiders", "resources", "app", "out", "vs", "workbench", "workbench.desktop.main.js"]),
    pathOf([env.LOCALAPPDATA, "Programs", "Microsoft VS Code"]),
    pathOf([env.ProgramFiles, "Microsoft VS Code", "resources", "app", "out", "vs", "workbench", "workbench.desktop.main.js"]),
    pathOf([env.ProgramFiles, "Microsoft VS Code"]),
    pathOf([env["ProgramFiles(x86)"], "Microsoft VS Code", "resources", "app", "out", "vs", "workbench", "workbench.desktop.main.js"]),
  ].filter((candidate) => candidate !== undefined);

/** @type {string[]} */
const hostRoots = hostRootsOf(process.env);

/** A product installed under a versioned folder keeps its bundle one level down, which
 *  is why the last candidates are searched rather than read.
 *  @returns {{ path: string | undefined, tried: string[] }} */
function findHostBundle() {
  /** @type {string[]} */
  const tried = [];
  for (const candidate of hostRoots) {
    if (existsSync(candidate) && statSync(candidate).isFile()) return { path: candidate, tried };
    tried.push(candidate);
    if (!existsSync(candidate) || !statSync(candidate).isDirectory()) continue;
    for (const entry of readdirSync(candidate, { withFileTypes: true })) {
      if (!entry.isDirectory()) continue;
      const nested = join(candidate, entry.name, "resources", "app", "out", "vs", "workbench", "workbench.desktop.main.js");
      if (existsSync(nested)) return { path: nested, tried };
      tried.push(nested);
    }
  }
  return { path: undefined, tried };
}

/** The host's own types, each with the super type IT registered, and the modifiers it
 *  registered. An empty map means the bundle was not read, which is a refusal the check
 *  reports and never a silent pass - so the two faults are worded here, where the
 *  reading they are about lives, and the path convention is the caller's because a path
 *  is shown relative to the repository in a report.
 *  @param {(path: string) => string} show
 *  @returns {HostClassification} */
export function readHostClassification(show) {
  const host = findHostBundle();
  /** @type {Map<string, string | undefined>} */
  const types = new Map();
  /** @type {string[]} */
  let modifiers = [];
  /** @type {string[]} */
  const faults = [];
  if (host.path === undefined) {
    faults.push(
      `host: the installed product's bundle was not found, so the roles' kinds cannot be checked against the list the ` +
        `host actually registers and a list written into this check instead would be exactly the defect this check exists ` +
        "to catch. Looked in:\n    " +
        host.tried.map(show).join("\n    ") +
        "\n  Name one file with KHAYYAM_HOST_BUNDLE, or install the product this extension runs in.",
    );
  } else {
    const source = readFileSync(host.path, "utf8");
    // `T4n()` registers through a local helper, so the calls are `o("id",<description>,<scopes>,<superType>)`.
    for (const call of source.matchAll(/o\("([^"]+)",\w+\(\d+,null\),(\[\[.*?\]\]|\[\]|void 0)(?:,("(?:[^"]*)"|void 0))?/g))
      types.set(call[1], call[3] === undefined || call[3] === "void 0" ? undefined : call[3]);
    modifiers = [...source.matchAll(/registerTokenModifier\("([^"]+)"/g)].map((m) => m[1]);
    if (types.size === 0)
      faults.push(
        `host: ${show(host.path)} parsed as carrying no registered token types, so the roles' kinds would be checked ` +
          "against nothing. The reading is out of `function T4n()`, which is where the host registers its own classification.",
      );
  }
  return { path: host.path, tried: host.tried, types, modifiers, faults };
}

/** The names the host registers as its own standard types, or the memory above where it
 *  registers none - which the check has already refused, and refuses again before any of
 *  this is relied on.
 *  @param {HostClassification} host
 *  @returns {Set<string>} */
export const registeredNamesOf = (host) =>
  host.types.size > 0 ? new Set(host.types.keys()) : new Set(Object.keys(STANDARD_FALLBACK));

/** Every name a token of this type inherits: its own name, then the names the manifest
 *  declares it to extend, then the host's own supertypes.
 *  @param {HostClassification} host
 *  @param {DeclaredType[]} declaredTypes
 *  @returns {{ hierarchyOf: (type: string) => string[],
 *             scoreOf: (type: string, language: string, selector: Selector) => number }} */
export function matchingOf(host, declaredTypes) {
  /** THE HOST'S OWN HIERARCHY, read from the bundle above rather than written down. In
   *  `T4n()` exactly one registered type carries a super type - `member`, under `method` -
   *  so every other standard type's hierarchy is itself, and this check used to carry a
   *  table claiming `class` extends `type` and `parameter` extends `variable`, which the
   *  host's own code does not say. What a contribution adds is read separately, here.
   *  @type {(type: string) => string[]} */
  const hostHierarchyOf = (type) => {
    const names = [type];
    for (let at = host.types.get(type); at !== undefined; at = host.types.get(at)) {
      if (names.includes(at)) break; // a declared cycle, which the host's own getTypeHierarchy has no guard for
      names.push(at);
    }
    return names;
  };
  /** @type {(name: string) => DeclaredType | undefined} */
  const declaredByIdOf = (name) => (declaredTypes ?? []).find((entry) => entry.id === name);
  /** @type {(type: string) => string[]} */
  const hierarchyOf = (type) => {
    const names = new Set(host.types.size > 0 ? hostHierarchyOf(type) : STANDARD_FALLBACK[type] ?? [type]);
    /** @type {(name: string) => string[]} */
    const superTypesOf = (name) => {
      const superType = declaredByIdOf(name)?.superType;
      return superType === undefined || superType === "" ? [] : [superType];
    };
    // The `seen` guard is what a declared cycle would otherwise turn into a hang.
    const seen = new Set();
    for (let at = type; at !== undefined && !seen.has(at); at = superTypesOf(at)[0]) {
      seen.add(at);
      names.add(at);
      for (const parent of superTypesOf(at)) names.add(parent);
    }
    return [...names];
  };

  /** The host's score for a rule that matches a token, in words and in code. Read out of
   *  `parseTokenSelector`'s `match` in the same bundle: the language part is worth 10, the
   *  type part is `100 - depth`, and each modifier is worth 100. A deeper match therefore
   *  scores LOWER, which is what makes a rule keyed a role's own name beat a rule keyed
   *  the standard type the role extends.
   *  @type {(type: string, language: string, selector: Selector) => number} */
  const scoreOf = (type, language, selector) => {
    if (selector.language !== undefined && selector.language !== language) return -1;
    let score = 0;
    if (selector.language !== undefined) score += 10;
    if (selector.type !== "*") {
      const depth = hierarchyOf(type).indexOf(selector.type);
      if (depth === -1) return -1;
      score += 100 - depth;
    }
    return score;
  };

  return { hierarchyOf, scoreOf };
}

/** A rule's key, read as the editor reads it.
 *  @param {string} key
 *  @returns {Selector} */
export const parseSelector = (key) => {
  let end = key.length;
  let language;
  for (let at = end - 1; at >= 0; at -= 1) {
    const code = key.charCodeAt(at);
    if (code === 46 || code === 36) {
      const suffix = key.slice(at + 1, end);
      end = at;
      if (code === 46) language = suffix;
    }
  }
  return { type: key.slice(0, end), language };
};

/** Whether the editor would give a token of this type, standing in this language, the
 *  style this selector carries. The token's language is the language of the document
 *  the token stands in, never something read out of a name.
 *  @param {(type: string, language: string, selector: Selector) => number} scoreOf
 *  @returns {(selector: Selector, type: string, language: string) => boolean} */
export const stylesToken = (scoreOf) => (selector, type, language) =>
  scoreOf(type, language, selector) >= 0;
