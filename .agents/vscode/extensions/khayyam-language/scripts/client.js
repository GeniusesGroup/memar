// Khayyam language extension: starts the language server and serves the roles it
// answers with.
//
// The display contract (modules/khayyam/display/display.json) stays the single
// source of truth. The server reads it and advertises each role's NAME as its
// semantic-token legend, and a name is the token type the editor matches a styling
// rule against; the value for each role is stated by the manifest's own
// `editor.semanticTokenColorCustomizations` rules, keyed by that same name, and the
// language is stated in the `[khayyam]` block those rules sit in and in the provider's
// document selector - never in the name. The grammar keeps handling what a grammar can
// handle; the server answers for every occurrence whose binding only a semantic
// analysis can know.
//
// No build step: this file is plain CommonJS, loaded directly by the editor.

const { spawn } = require("node:child_process");
const fs = require("node:fs");
const path = require("node:path");
const vscode = require("vscode");

const { definitionRequest, readTarget } = require("./definition.js");

const SERVER_RELATIVE = ["modules", "khayyam", "lsp", "src", "server.ts"];
const CONTRACT_RELATIVE = ["modules", "khayyam", "display", "display.json"];

/**
 * What the server pushes in the one notification this client acts on: a
 * document's faults. Declared here rather than left to inference, so a handler
 * that reads a field of it is checked against the shape the server sends.
 * @typedef {{
 *   uri?: string,
 *   diagnostics?: Array<{
 *     range: { start: { line: number, character: number }, end: { line: number, character: number } },
 *     message: string,
 *     severity?: number
 *   }>
 * }} NotificationParams
 */

/** One entry of that array, named because a mapper over it is written once and reads
 *  three fields of it.
 *  @typedef {NonNullable<NotificationParams["diagnostics"]>[number]} ReportedFault
 */

/** A rule's key, read the way the editor reads it: the token type, whole, and the
 *  language a selector names, if it names one at all.
 *  @typedef {{ type: string, language?: string }} Selector
 */

/**
 * The one setting of the `[khayyam]` block this file reads: the map from a selector to the
 * style that selector carries. The host reads a rule's own keys as the selectors, so the
 * value under one is a style and the value here is deliberately not named - this function
 * reads the selector and no part of a style.
 * @typedef {{ rules?: Record<string, unknown> }} SemanticTokenColorCustomizations
 */

/**
 * The manifest of this extension, as far as this file reads it. The editor declares
 * `Extension.packageJSON` as `any` - a manifest is the document it is and the host types
 * no part of it - so this is the declaration the editor's own `any` cannot give, and it
 * is stated once, where the fields this file reads are named. The one block carries the
 * two settings it reads by their own ids, because an open map answers every key of it
 * `unknown` and the read below is a call that wants a shape.
 * @typedef {{
 *   contributes?: {
 *     semanticTokenTypes?: Array<{ id: string, superType?: string, description?: string }>,
 *     configurationDefaults?: Record<
 *       string,
 *       Record<string, unknown> & { "editor.semanticTokenColorCustomizations"?: SemanticTokenColorCustomizations }
 *     >
 *   }
 * }} ExtensionManifest
 */

/**
 * The display contract document, as far as this file reads it: a JSON file this process
 * parses at run time, which no declaration anywhere types, so the fields read here are
 * stated at this declaration - what it calls itself and its version, and each role's name
 * and how the contract says the role is realized.
 * @typedef {{
 *   specification: string,
 *   version: string,
 *   roles: Array<{ name: string, implementedBy?: string }>
 * }} DisplayContract
 */

/** What `initialize` answers with, as far as this file reads it: the legend the server
 *  advertises, the name it calls itself by, and whether it answers a definition request.
 *  The last is what decides whether a definition provider is registered at all, because a
 *  provider the server cannot answer is a provider that fails a reader's go-to-definition
 *  in a way that says nothing about why.
 *  @typedef {{
 *    capabilities?: {
 *      semanticTokensProvider?: { legend?: { tokenTypes?: string[] } },
 *      definitionProvider?: boolean
 *    },
 *    serverInfo?: { name?: string }
 *  }} InitializeAnswer
 */

/** What `textDocument/semanticTokens/full` answers with: the flat stream the editor
 *  decodes against the legend, five numbers per token.
 *  @typedef {{ data?: number[] }} SemanticTokensAnswer
 */

/** A place the server or the contract may be, and the setting that named it.
 *  @typedef {{ where: string, file: string }} Candidate
 */

/** The child process a connection owns, with the three pipes this file reads and writes.
 *  The editor's own `spawn` types every stream as nullable because `stdio` may be
 *  `'ignore'`, and `startServer` below names all three - so the pipes are not a hope but
 *  what was asked for, and this is the type that says so where the asking happens.
 *  @typedef {import("node:child_process").ChildProcess & {
 *    stdin: import("node:stream").Writable,
 *    stdout: import("node:stream").Readable,
 *    stderr: import("node:stream").Readable
 *  }} PipedChild
 */

/** The message a thrown value carries, for a report line. A `catch` binds `unknown`,
 *  because anything at all may be thrown and this file reads one field of it; this is
 *  where that unknown becomes text, and it is text for a value that is not an `Error`
 *  too, because a refusal that reported nothing is the fault this file exists to avoid.
 *  @param {unknown} thrown
 *  @returns {string} */
function messageOf(thrown) {
  return thrown instanceof Error ? thrown.message : String(thrown);
}

/** A frame on the wire. Two shapes arrive here: an answer, carrying `id` and then
 *  `result` or `error`, or a notification, carrying `method` and `params`. It is a JSON
 *  document this process parses at run time, so it is declared here; a notification's
 *  parameters are typed `NotificationParams` because the one handler this connection
 *  declares takes exactly that, and this client acts on one method.
 *  @typedef {{
 *    id?: number,
 *    method?: string,
 *    params?: NotificationParams,
 *    result?: unknown,
 *    error?: { message: string }
 *  }} JsonRpcFrame

/** What this connection puts on the wire: a request or a notification, so a `method` is
 *  always named and the parameters are whatever that method's parameters are.
 *  @typedef {{ id?: number, method: string, params?: unknown }} JsonRpcMessage

/** This extension's own manifest, under the declared type the editor's `packageJSON: any`
 *  cannot give. The one place a document with no declared type is given one; everything
 *  downstream of it is checked.
 *  @param {vscode.ExtensionContext} context
 *  @returns {ExtensionManifest} */
function manifestOf(context) {
  return /** @type {ExtensionManifest} */ (context.extension.packageJSON);
}

/** The language this extension contributes, and where the editor is told it: the
 *  `[khayyam]` block the colour rules sit in and the provider's document selector. It
 *  is deliberately not part of a role's name — a legend entry is the token type, read
 *  whole. */
const LANGUAGE_ID = "khayyam";

/** What the display contract says about a role no TextMate scope can carry: a grammar
 *  matches one line at a time and holds no symbol table, so `vr index U32` is one line of
 *  text whether the name stands in a body or at file level. It is named in the log rather
 *  than counted apart, because it is styled the same way as every other role: the colour
 *  rules key a role by its own name, and a name is the token type a host matches a rule
 *  against, whether a scope carries it or not. */
const SERVER_ONLY = "server-only";

/** What a rule's KEY means to the editor, and what it costs to get the key wrong.
 *  Transcribed from the editor bundle (VS Code 43.6.0,
 *  out/vs/workbench/workbench.desktop.main.js):
 *
 *    - a rule's key is split right to left on '.' and '$': the segment before the
 *      FIRST separator is the token TYPE, the segment after it is the LANGUAGE, and
 *      everything further right is dropped. So `entity.name.import.khayyam` is the
 *      token type `entity` in the language `name`.
 *    - a selector that names a language styles only tokens of that language; one
 *      that names none styles that token type in every language.
 *    - the type is looked up in the token's type HIERARCHY, which is the token's own
 *      name followed by every name it was declared to extend — and of the editor's
 *      own standard types, the supertypes above them. An extension that declares no
 *      `semanticTokenTypes` gives every custom type a hierarchy of exactly one name.
 *
 *  So the token's type is the legend entry whole, and the token's language is the
 *  language of the document it stands in. A legend entry that carries a language of
 *  its own has a one-name hierarchy that no rule keyed the same way can reach, and a
 *  token the editor resolves no style for is dropped while the grammar's tokens are
 *  merged in: the editor asks for the tokens, receives them, and draws nothing.
 *
 *  So the extension checks, before it reports itself ready, that every name in the
 *  legend is a style the editor can actually resolve.
 *  @param {string} key
 *  @returns {Selector} */
function parseSelector(key) {
  let end = key.length;
  let language;
  for (let at = end - 1; at >= 0; at -= 1) {
    const code = key.charCodeAt(at);
    if (code === ".".charCodeAt(0) || code === "$".charCodeAt(0)) {
      const suffix = key.substring(at + 1, end);
      end = at;
      if (code === ".".charCodeAt(0)) language = suffix;
    }
  }
  return { type: key.substring(0, end), language };
}

/** The editor's own standard token types and what each one extends, so that a
 *  reader's rule for `function` is recognised as reaching this extension's `method`
 *  and is not reported as a missing one. A name outside this table and outside the
 *  extension's own `semanticTokenTypes` stands alone.
 *
 *  It is an OPEN map rather than a closed set of keys, because a key here is a token
 *  type the host registers and the host registers names this file has never read. A
 *  lookup with a name the table does not hold therefore answers `undefined`, and
 *  `typeHierarchy` reads that as a name standing alone - which is the same answer the
 *  host gives, so declaring the keys closed would claim the host's list is this file's.
 *  @type {Record<string, string[]>} */
const STANDARD_TYPE_HIERARCHY = {
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

/** Every name a token of this type inherits, itself first, then the types this
 *  extension declares it to extend, then the editor's own supertypes.
 *  @param {string} type
 *  @param {vscode.ExtensionContext} context
 *  @returns {string[]} */
function typeHierarchy(type, context) {
  const hierarchy = new Set(STANDARD_TYPE_HIERARCHY[type] ?? [type]);
  const declared = manifestOf(context).contributes?.semanticTokenTypes ?? [];
  /** What the manifest declares a type to extend, as the LIST the two loops below walk.
   *  It is a list because a loop walks a list: the manifest states one super type per
   *  entry, so `superType ?? []` hands back that bare STRING when there is one, and
   *  walking a string walks its CHARACTERS - `subtype`'s declared `keyword` arrived as
   *  `k`, so no reader's rule for a declared super type ever reached the role, which is
   *  the whole question `typeHierarchy` exists to answer.
   *  @type {(name: string) => string[]} */
  const superTypesOf = (name) => {
    const superType = declared.find((entry) => entry.id === name)?.superType;
    return superType === undefined || superType === "" ? [] : [superType];
  };
  // The `seen` guard is what a declared cycle would otherwise turn into a hang, and
  // this runs while the editor is starting up.
  const seen = new Set();
  for (let at = type; at !== undefined && !seen.has(at); at = superTypesOf(at)[0]) {
    seen.add(at);
    hierarchy.add(at);
    for (const parent of superTypesOf(at)) hierarchy.add(parent);
  }
  return [...hierarchy];
}

/** Whether the editor would give a token of `type`, standing in `language`, the style
 *  this rule carries. The editor's own rule, and the reason a self-test cannot stand
 *  in for it: nothing here is measurable from inside this process.
 *  @param {Selector} selector
 *  @param {string} type
 *  @param {string} language
 *  @param {vscode.ExtensionContext} context
 *  @returns {boolean} */
function selectorStyles(selector, type, language, context) {
  if (selector.language !== undefined && selector.language !== language) return false;
  return typeHierarchy(type, context).includes(selector.type);
}

/** What to tell someone whose MEMAR_ROOT is not set, or names nothing usable.
 *  The variable is the only place Memar's location comes from: this extension
 *  never guesses a path from the home directory, the extension's own
 *  location, or anything else. The bootstrap is fetched from Memar's repository
 *  at the point of use, because no project carries a copy of it. */
function unsetMessage() {
  return (
    "MEMAR_ROOT is not set, so this extension does not know where Memar is on " +
    "this machine. Install it, which sets the variable for you:\n" +
    '    powershell -ExecutionPolicy Bypass -Command "& ([scriptblock]::Create((irm https://raw.githubusercontent.com/GeniusesGroup/memar/main/.agents/scripts/install.ps1)))"   (Windows)\n' +
    '    sh -c "$(curl -fsSL https://raw.githubusercontent.com/GeniusesGroup/memar/main/.agents/scripts/install.sh)" install.sh                               (POSIX)\n' +
    "Then restart the editor: a running program does not read a new " +
    "environment value, so this window keeps seeing MEMAR_ROOT as unset until it is.\n" +
    "To point at a Memar folder you already have, add --register <folder> " +
    "(POSIX) or -Register <folder> (Windows) to that command."
  );
}

/** Every place the server may be, most explicit first. Nothing is guessed silently.
 *  @returns {Candidate[]} */
function serverCandidates() {
  const configured = vscode.workspace.getConfiguration("khayyam").get("languageServer.path", "");
  /** @type {Candidate[]} */
  const candidates = [];
  if (configured) candidates.push({ where: "khayyam.languageServer.path", file: path.resolve(configured) });
  if (process.env.KHAYYAM_LSP) candidates.push({ where: "KHAYYAM_LSP", file: path.resolve(process.env.KHAYYAM_LSP) });
  if (process.env.MEMAR_ROOT) {
    candidates.push({ where: "MEMAR_ROOT", file: path.join(process.env.MEMAR_ROOT, ...SERVER_RELATIVE) });
    candidates.push({
      where: "MEMAR_ROOT (built)",
      file: path.join(process.env.MEMAR_ROOT, "modules", "khayyam", "lsp", "dist", "server.js"),
    });
  }
  return candidates;
}

/** Every place the display contract may be, in the same order and for the same reason.
 *  @returns {Candidate[]} */
function contractCandidates() {
  const configured = vscode.workspace.getConfiguration("khayyam").get("contractPath", "");
  return [
    ...(configured ? [{ where: "khayyam.contractPath", file: path.resolve(configured) }] : []),
    ...(process.env.MEMAR_ROOT
      ? [{ where: "MEMAR_ROOT", file: path.join(process.env.MEMAR_ROOT, ...CONTRACT_RELATIVE) }]
      : []),
  ];
}

/** The contract at the first place it is found, and everywhere that was looked for - the
 *  second is what a refusal reports, so a reader is told what was tried rather than only
 *  that nothing was found.
 *  @param {(line: string) => void} report
 *  @returns {{ contract: DisplayContract | undefined, tried: Candidate[] }} */
function readContract(report) {
  const candidates = contractCandidates();
  for (const candidate of candidates) {
    try {
      return {
        // A JSON file parsed at run time, which no declaration types: `DisplayContract`
        // is stated at the top of this file, so what the reader of this function sees is
        // the contract's own shape and not a value every caller inherits as `any`.
        contract: /** @type {DisplayContract} */ (JSON.parse(fs.readFileSync(candidate.file, "utf8"))),
        tried: candidates,
      };
    } catch {
      report(`display contract not at ${candidate.file} (${candidate.where})`);
    }
  }
  return { contract: undefined, tried: candidates };
}

/** The scope a Khayyam setting has to be read against. Whether the editor asks this
 *  server for anything at all is decided here and nowhere else, so this is read with a
 *  DOCUMENT and not with a bare Uri: a language override - this extension's own
 *  `[khayyam]` default in package.json - resolves against a document and against nothing
 *  else. Measured on 1.139.1, the same setting reads `true` through a TextDocument and
 *  `configuredByTheme` through a Uri or through no scope at all, and at activation there
 *  may be no active editor to take a document from, so the first open Khayyam document
 *  is asked.
 *  @returns {vscode.TextDocument | undefined} */
function khayyamScope() {
  return (
    vscode.workspace.textDocuments.find((document) => document.languageId === LANGUAGE_ID) ??
    vscode.window.activeTextEditor?.document
  );
}

/** The keys of one `editor.semanticTokenColorCustomizations`, read the way the editor
 *  reads them: its `rules` is a MAP from selector to style, and anything else there
 *  configures nothing, because the editor takes a rule's own keys as its selectors.
 *
 *  The editor types `WorkspaceConfiguration.get` as `get<T>(section): T | undefined` and
 *  nothing constrains `T` here, so a setting read without a default arrives as `any`;
 *  the shape it actually has is the one the typedef above states.
 *  @param {SemanticTokenColorCustomizations | undefined} customizations
 *  @returns {string[]} */
function ruleNamesOf(customizations) {
  const rules = customizations?.rules;
  return rules && typeof rules === "object" && !Array.isArray(rules) ? Object.keys(rules) : [];
}

/** Every legend name the editor would resolve no style for, and where the rest resolve
 *  theirs from.
 *
 *  ONE mechanism styles a role here, and this function judges that mechanism alone:
 *  `editor.semanticTokenColorCustomizations`, whose `rules` is a MAP from selector to
 *  style (an array there configures nothing, because the editor reads the rule's own
 *  keys as the selectors). The manifest contributes no `contributes.semanticTokenScopes`
 *  on purpose, so there is no second place a host could take a value from: a bridge entry
 *  is applied after these rules, not beside them, and a rule overwrites a score it equals
 *  or beats, so a bridge for a role the contract values would replace the contract's
 *  value with the active theme's on every role it carried.
 *
 *  Both sources of the colour rules are counted: this extension's own `[khayyam]`
 *  default, and whatever the reader has configured over it. The first is read from the
 *  manifest because a language-scoped default does not resolve against a scope that is
 *  not a Khayyam document, and at activation the setting may be read with no such
 *  document in the editor - a rule this extension contributed is then not absent from the
 *  editor, only from this read of it, and reading it as absent is what refused a role
 *  the editor styles.
 *  @param {string[]} legend the token types the server advertised: the editor's own
 *    `SemanticTokensLegend.tokenTypes`, which its declarations type as `string[]`
 *  @param {vscode.ExtensionContext} context
 *  @returns {{ unstyled: string[], ruled: number, own: number }} */
function styledRoles(legend, context) {
    const defaults = manifestOf(context).contributes?.configurationDefaults ?? {};
    const own = ruleNamesOf(defaults[`[${LANGUAGE_ID}`]?.["editor.semanticTokenColorCustomizations"]).map(parseSelector);
  const reader = ruleNamesOf(
    vscode.workspace.getConfiguration("editor", khayyamScope()).get("semanticTokenColorCustomizations"),
  ).map(parseSelector);
  const ruled = [...new Set([...own, ...reader])];
  /** @type {(name: string, selectors: Selector[]) => boolean} */
  const resolves = (name, selectors) => selectors.some((selector) => selectorStyles(selector, name, LANGUAGE_ID, context));
  /** @type {(selectors: Selector[]) => number} */
  const reached = (selectors) => legend.filter((name) => resolves(name, selectors)).length;
  return {
    unstyled: legend.filter((name) => !resolves(name, ruled)),
    ruled: reached(ruled),
    own: reached(own),
  };
}

/** A Language Server connection over a child process's stdio. */
class Connection {
  /** @param {PipedChild} child */
  constructor(child) {
    this.child = child;
    this.buffer = Buffer.alloc(0);
    this.nextId = 1;
    this.pending = new Map();
    /**
     * Notifications the server pushes, by method, so a client can act on them.
     * The declared shape is the contract the reader relies on: a bare empty
     * arrow types itself as taking no arguments, which lets a call that passes
     * a method and its parameters typecheck as a call to something that takes
     * nothing. The parameters are optional because the wire says so - a
     * notification may arrive with none - and a handler that reads one has to
     * say what it does with a notification that carried none, which is what
     * the handler below does before it reads anything.
     * @type {(method: string, params: NotificationParams | undefined) => void}
     */
    this.onNotification = () => {};
    this.child.stdout.on("data", (/** @type {Buffer} */ chunk) => this.receive(chunk));
      this.child.on("exit", (/** @type {number | null} */ code) => {
        this.exited = true;
        this.exitCode = code;

      for (const [, entry] of this.pending) entry.reject(new Error(`the language server exited (code ${code})`));
      this.pending.clear();
    });
  }

  /** @param {Buffer} chunk */
  receive(chunk) {
    this.buffer = Buffer.concat([this.buffer, chunk]);
    for (;;) {
      const text = this.buffer.toString("utf8");
      const separator = text.indexOf("\r\n\r\n");
      if (separator < 0) return;
      const match = /Content-Length:\s*(\d+)/i.exec(text.slice(0, separator));
      if (!match) {
        this.buffer = this.buffer.subarray(separator + 4);
        continue;
      }
      const length = Number(match[1]);
      const bodyStart = separator + 4;
      if (Buffer.byteLength(text.slice(bodyStart), "utf8") < length) return;
      const body = Buffer.from(text.slice(bodyStart), "utf8").subarray(0, length).toString("utf8");
      this.buffer = this.buffer.subarray(bodyStart + length);
      let message;
      try {
        message = /** @type {JsonRpcFrame} */ (JSON.parse(body));
      } catch {
        continue;
      }
      const entry = this.pending.get(message.id);
      if (entry) {
        this.pending.delete(message.id);
        // A server that answers with an error is saying why it cannot answer. Reading
        // that as an answer with nothing in it is how a server's own fault reached the
        // reader as a document with no roles, so the error is raised instead.
        if (message.error) entry.reject(new Error(`${entry.method} failed: ${message.error.message}`));
        else entry.resolve(message.result);
      } else if (message.method) {
        this.onNotification(message.method, message.params);
      }
    }
  }

  /** @param {JsonRpcMessage} message */
  send(message) {
    const body = JSON.stringify({ jsonrpc: "2.0", ...message });
    this.child.stdin.write(`Content-Length: ${Buffer.byteLength(body, "utf8")}\r\n\r\n${body}`);
  }

  /** Ask the server and wait for its answer.
   *
   *  The answer is a JSON document the server writes and no declaration types, so this
   *  answers `Promise<unknown>` and the caller declares the shape it reads at the call
   *  it reads it from - `InitializeAnswer` and `SemanticTokensAnswer` above. Deciding
   *  here instead would put one server's answer behind every method on the connection.
   *  @param {string} method
   *  @param {unknown} params
   *  @param {number} [timeoutMs]
   *  @returns {Promise<unknown>} */
  request(method, params, timeoutMs = 10000) {
    const id = this.nextId++;
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        this.pending.delete(id);
        reject(new Error(`${method} timed out after ${timeoutMs}ms`));
      }, timeoutMs);
      this.pending.set(id, {
        method,
        resolve: (/** @type {unknown} */ value) => {
          clearTimeout(timer);
          resolve(value);
        },
        reject: (/** @type {Error} */ error) => {
          clearTimeout(timer);
          reject(error);
        },
      });
      this.send({ id, method, params });
    });
  }

  /** @param {string} method
   *  @param {unknown} params */
  notify(method, params) {
    this.send({ method, params });
  }
}

/**
 * Start the server.
 *
 * `process.execPath` in the extension host is the editor binary, not node, so a
 * spawn without ELECTRON_RUN_AS_NODE launches a second editor window instead of
 * the server. Every shipped language extension that forks from the editor sets it
 * (the Go extension's transport sets ELECTRON_RUN_AS_NODE and ELECTRON_NO_ASAR);
 * with it, this editor's binary answers as node v24, which reads a TypeScript
*  server directly.
 *  @param {string} serverFile
 *  @param {(line: string) => void} report
 *  @returns {Connection} */
function startServer(serverFile, report) {
  const child = spawn(process.execPath, [serverFile], {
    stdio: ["pipe", "pipe", "pipe"],
    env: { ...process.env, ELECTRON_RUN_AS_NODE: "1", ELECTRON_NO_ASAR: "1" },
  });
  child.on("error", (/** @type {Error} */ error) => report(`launch FAILED: the language server could not be started: ${error.message}`));
  child.stderr.on("data", (/** @type {Buffer} */ chunk) => report(`server: ${String(chunk).trimEnd()}`));
  report(`launch: ${process.execPath} ${serverFile}`);
  return new Connection(/** @type {PipedChild} */ (child));
}

/** @param {vscode.ExtensionContext} context */
async function activate(context) {
  const output = vscode.window.createOutputChannel("Khayyam");
  context.subscriptions.push(output);
  /** @type {string[]} */
  const lines = [];
  /** @type {(line: string) => void} */
  const report = (line) => {
    lines.push(line);
    output.appendLine(line);
  };

  let status = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 100);
  status.command = "khayyam.showOutput";
  context.subscriptions.push(status);
  context.subscriptions.push(
    vscode.commands.registerCommand("khayyam.showOutput", () => {
      output.show(true);
    }),
  );

  /** @param {string} stage @param {string} reason */
  const fail = (stage, reason) => {
    // Never silent, and never without a stage. A fault in launch, handshake, document
    // or request all reach the reader as the same thing - no colours - so the one line
    // that says which of the four broke is the whole point of this function.
    status.text = `$(warning) Khayyam: ${stage} failed`;
    status.tooltip = reason;
    status.show();
    report(`${stage} FAILED: ${reason}`);
    vscode.window.showErrorMessage(`Khayyam ${stage}: ${reason}`, "Show log").then((choice) => {
      if (choice === "Show log") output.show(true);
    });
  };

  const { contract, tried } = readContract(report);
  if (!contract) {
    fail(
      "contract",
      tried.length === 0
        ? unsetMessage()
        : "the display contract was not found. Tried: " +
            tried.map((c) => `${c.file} (${c.where})`).join("; "),
    );
    return;
  }

  const candidates = serverCandidates();
  const found = candidates.find((candidate) => fs.existsSync(candidate.file));
  for (const candidate of candidates) {
    report(`${candidate.file} - ${found === candidate ? "FOUND" : "not found"} (${candidate.where})`);
  }
  if (!found) {
    fail(
      "launch",
      candidates.length === 0
        ? unsetMessage()
        : "the language server was not found. Tried: " +
            candidates.map((c) => `${c.file} (${c.where})`).join("; ") +
            ". Set khayyam.languageServer.path to point elsewhere.",
    );
    return;
  }

  /** @type {Connection | undefined} */
  let connection;
  try {
    connection = startServer(found.file, report);
    /** The connection every callback below closes over. It is a second name for one
     *  value on purpose: a `let` read inside a nested function carries none of the
     *  narrowing the assignment above earned, so each handler would read it as a
     *  connection that may not exist — and it exists, because the editor cannot call a
     *  handler registered below before this line has run. This is where that fact is
     *  stated, once, rather than asserted at each of the six reads.
     */
    const live = connection;
    const initialized = /** @type {InitializeAnswer} */ (
      await connection.request("initialize", {
      processId: process.pid,
      rootUri: vscode.workspace.workspaceFolders?.[0]?.uri.toString() ?? null,
      // The server says what it could not read of a document, and this is the
      // capability that says the editor will show it. Without the declaration the
      // editor discards those messages, and a file the frontend could not read in
      // full reaches the reader looking like any other file - which is how three
      // rounds of a working feature came to look broken.
      capabilities: { textDocument: { publishDiagnostics: {} } },
      })
    );
    connection.notify("initialized", {});
    report(`handshake: initialize answered by ${initialized.serverInfo?.name ?? "a server that named itself nothing"}`);

    // The legend carries the contract's own role names, spelled plainly: a name that
    // welded a language to itself could not be matched by a rule keyed the same way,
    // and the server's answer would be discarded while looking like a success.
    const expected = contract.roles.map((role) => role.name);
    const legend = initialized?.capabilities?.semanticTokensProvider?.legend?.tokenTypes ?? [];
    // Whether the server answers a definition request at all. Read here, once, and said
    // either way: a reader whose go-to-definition finds nothing cannot tell a file with
    // no declarations in it from an editor that asked no one, and that is the same
    // confusion the self-test below was written to end for the roles.
    const capabilities = {
      definitionProvider: initialized?.capabilities?.definitionProvider === true,
    };
    report(
      capabilities.definitionProvider
        ? "handshake: the server answers textDocument/definition, so a definition provider is registered for it"
        : "handshake: the server declares no definition provider, so this extension registers none and " +
            "a go-to-definition will find nothing — that is the server's answer to declare, not a fault to read past",
    );
    if (JSON.stringify(legend) !== JSON.stringify(expected)) {
      fail(
        "handshake",
        `the server's roles do not match ${contract.specification} v${contract.version}; ` +
          `expected ${expected.length} roles (${expected[0]}, ...) and got ${legend.length}` +
          (legend.length > 0 ? ` (${legend[0]}, ...)` : ""),
      );
      return;
    }
    const unreadable = legend.filter((name) => /[.$]/.test(name));    if (unreadable.length > 0) {
      fail(
        "handshake",
        `the server advertised ${unreadable.length} legend name(s) carrying a separator, which the ` +
          `editor reads as a token type and a language: ${unreadable.join(", ")}. A legend entry is ` +
          "the token type whole, so a name like that no rule can match and every token of it is " +
          "discarded. The role's name is the contract's own name, and the language belongs in the " +
          `[${LANGUAGE_ID}] block the colour rules sit in and the provider's document selector.`,
      );
      return;
    }

    // A legend the editor cannot colour is worse than no server at all: the editor
    // discards those tokens silently and the reader sees grammar colours, which is
    // the failure this check exists to make loud. The line names what is missing for
    // each of them, and not what does exist: a reader has the manifest already. It
    // judges the colour rules ALONE, and says so, because the manifest contributes no
    // semanticTokenScopes: there is no other mechanism this extension could be
    // styling a role through.
    const { unstyled, ruled, own } = styledRoles(legend, context);
    if (unstyled.length > 0) {
      fail(
        "styling",
        `the editor would discard ${unstyled.length} of ${legend.length} semantic tokens, so those ` +
          `roles would show the grammar's colours with no error anywhere. The check judges ` +
          "editor.semanticTokenColorCustomizations alone - this manifest contributes no " +
          "contributes.semanticTokenScopes, so there is no other mechanism that can style a role. " +
          "For each of them, this is what is missing: " +
          unstyled
            .map((name) => `${name} (no editor.semanticTokenColorCustomizations rule keyed '${name}')`)
            .join("; ") +
          ".",
      );
      return;
    }
    // Whether the editor asks this server for anything at all is decided here and
    // nowhere else, so this check is read with a DOCUMENT and not with a bare Uri: a
    // language override - this extension's own `[khayyam]` default in package.json -
    // resolves against a document and against nothing else (khayyamScope above).
    const highlighting = vscode.workspace
      .getConfiguration("editor", khayyamScope())
      .get("semanticHighlighting.enabled");
    if (highlighting === false) {
      fail(
        "request",
        'editor.semanticHighlighting.enabled is false for Khayyam, so the editor discards every ' +
          "semantic token this server answers with. The grammar's colours are all that would be shown.",
      );
      return;
    }
    if (highlighting !== true) {
      report(
        `request: editor.semanticHighlighting.enabled reads ${JSON.stringify(highlighting)} with no ` +
          `Khayyam document in scope, so the colour theme (${
            vscode.window.activeColorTheme
              ? vscode.ColorThemeKind[vscode.window.activeColorTheme.kind]
              : "unknown"
          }) ` +
          "decides whether the editor asks this server at all. The request below is what settles it.",
      );
    }

    status.text = "$(check) Khayyam: server on";
    status.tooltip = `${initialized.serverInfo?.name} from ${found.file}`;
    status.show();
    report(`ready: ${legend.length} roles from ${contract.specification} v${contract.version}`);
    // The line says WHICH mechanism reaches the editor, because a reader who sees only
    // a count of roles styled cannot tell a value the contract states from one a theme
    // supplied - and with no bridge contributed, the colour rules are the whole of it.
    const unscoped = contract.roles.filter((role) => role.implementedBy === SERVER_ONLY).map((role) => role.name);
    report(
      `styled: ${legend.length} of ${legend.length} roles resolve a style through ` +
        `editor.semanticTokenColorCustomizations (${ruled} keyed by this extension's own ` +
        `[${LANGUAGE_ID}] default` +
        (ruled > own ? `, ${ruled - own} by the reader's own settings` : "") +
        "). That is the only mechanism the manifest offers a role: it contributes no " +
        "semanticTokenScopes, so a host resolves each role from that rule and a theme's value for a " +
        "probed scope never replaces one" +
        (unscoped.length > 0
          ? ` — and it is what carries ${unscoped.join(", ")}, the role no TextMate scope reaches`
          : ""),
    );
    vscode.window.setStatusBarMessage("Khayyam language server started", 4000);

    // What the server could not read, on the line it stands. This is the editor's
    // own diagnostic collection, so a refusal is marked where it happened rather
    // than being one line in a log nobody opens - the whole defect was a refusal
    // that was invisible across the whole file.
    const faults = vscode.languages.createDiagnosticCollection("khayyam");
    context.subscriptions.push(faults);
    connection.onNotification = (method, params) => {
      if (method !== "textDocument/publishDiagnostics" || !params?.uri) return;
      const name = path.basename(params.uri);
      const reported = params.diagnostics ?? [];
      if (reported.length === 0) {
        faults.delete(vscode.Uri.parse(params.uri));
        return;
      }
      /** @type {(diagnostic: ReportedFault) => vscode.Diagnostic} */
      const toDiagnostic = (diagnostic) =>
        new vscode.Diagnostic(
          new vscode.Range(
            new vscode.Position(diagnostic.range.start.line, diagnostic.range.start.character),
            new vscode.Position(diagnostic.range.end.line, diagnostic.range.end.character),
          ),
          diagnostic.message,
          diagnostic.severity === 1 ? vscode.DiagnosticSeverity.Error : vscode.DiagnosticSeverity.Warning,
        );
      faults.set(vscode.Uri.parse(params.uri), reported.map(toDiagnostic));
      const first = reported[0];
      report(`refusal: ${name} — ${reported.length} the server could not read, first at line ${first.range.start.line + 1}: ${first.message}`);
      status.text = "$(warning) Khayyam: the server could not read part of this file";
      status.tooltip = `${name}: ${first.message} (${reported.length} in this file). Roles are still answered for everything the server did read.`;
      status.show();
    };

    const legendOf = new vscode.SemanticTokensLegend(legend, []);
    /** @type {Map<string, Uint32Array>} */
    const cache = new Map();
    let asked = 0;
    /** Tell the server about a document, and say that it happened: a document that
     *  never reached the server and a document the server cannot analyse both end as
     *  no colours, and only this line tells them apart afterwards.
     *  @param {vscode.TextDocument} document */
    const open = (document) => {
      live.notify("textDocument/didOpen", {
        textDocument: { uri: document.uri.toString(), version: document.version, text: document.getText() },
      });
      report(`document: ${path.basename(document.uri.toString())} sent`);
    };
    // The server holds a document only once it has been told about it, and
    // onDidOpen fires for documents opened from now on: the ones already open
    // when this extension activated are told here, or they are answered empty.
    for (const document of vscode.workspace.textDocuments) {
      if (document.languageId !== "khayyam") continue;
      open(document);
    }

    context.subscriptions.push(
      vscode.workspace.onDidOpenTextDocument((document) => {
        if (document.languageId !== "khayyam") return;
        open(document);
        cache.delete(document.uri.toString());
      }),
      vscode.workspace.onDidChangeTextDocument((event) => {
        if (event.document.languageId !== "khayyam") return;
        // The server declares textDocumentSync.change = 1 (Full), so a change carries
        // the whole document and no range. Sending the per-edit ranges instead is a
        // payload the server never promised to read, and it is applied with rules this
        // event does not promise to follow: every change in one event shares the
        // pre-change coordinates and they arrive top-down, so a second edit lands where
        // the first one moved the text. The server then holds a document the editor
        // has not: the fault the reader corrected stays on the line and the roles never
        // move, and nothing says why. One whole text per change, which is what Full
        // means, makes the server's document the editor's document.
        live.notify("textDocument/didChange", {
          textDocument: { uri: event.document.uri.toString(), version: event.document.version },
          contentChanges: [{ text: event.document.getText() }],
        });
        // The cache holds the roles the server answered for the text of a past version.
        // A Full change replaces the document whole, so every change invalidates all of
        // it — the invalidation is exactly the shape of what was sent, which a partial
        // payload could not be.
        cache.delete(event.document.uri.toString());
      }),
      vscode.workspace.onDidCloseTextDocument((document) => {
        if (document.languageId !== "khayyam") return;
        const uri = document.uri.toString();
        live.notify("textDocument/didClose", { textDocument: { uri } });
        cache.delete(uri);
      }),
      vscode.languages.registerDocumentSemanticTokensProvider(
        { language: "khayyam" },
        {
          async provideDocumentSemanticTokens(document) {
            const uri = document.uri.toString();
            // Every call is logged, not only the ones that miss the cache. A cache
            // hit produced no line at all, so a log that ends in the self-test's
            // two lines could not tell "the editor never asked" from "the editor
            // asked and the answer was already here" - and those are different
            // faults with different fixes.
            asked += 1;
            report(
              `editor asked (call ${asked}): ${path.basename(uri)}${cache.has(uri) ? " answered from roles already fetched" : ""}`,
            );
            if (!cache.has(uri)) {
              // A request that did not answer, or an answer with no data, is a fault
              // in this layer and is said so. Answering an empty token stream instead
              // is what made an earlier failure of this whole semantic layer look like
              // a success: the editor drew the grammar and reported nothing.
              let result;
              try {
                result = /** @type {SemanticTokensAnswer} */ (
                  await live.request("textDocument/semanticTokens/full", { textDocument: { uri } })
                );
              } catch (error) {
                report(`request FAILED: ${path.basename(uri)} could not be asked for its roles: ${messageOf(error)}`);
                status.text = "$(warning) Khayyam: request failed";
                status.tooltip = `the server did not answer for ${path.basename(uri)}: ${messageOf(error)}`;
                status.show();
                throw error;
              }
              const data = result?.data;
              if (!Array.isArray(data) || data.length === 0) {
                report(`request FAILED: the server answered ${path.basename(uri)} with no roles at all`);
                status.text = "$(warning) Khayyam: no roles";
                status.tooltip = `the server answered ${path.basename(uri)} with no roles`;
                status.show();
                throw new Error(`the Khayyam language server answered ${path.basename(uri)} with no roles`);
              }
              cache.set(uri, new Uint32Array(data));
              report(`fetch: ${path.basename(uri)} answered with ${data.length / 5} roles`);
            }
            // The second argument is the editor's `resultId` for an incremental
            // update, and it is a string: the legend is given once, at
            // registration, and this provider answers in full every time, so
            // there is no id to hand back. Handing the legend object over
            // instead put an object where the editor reads a string, and the
            // editor took the answer to be unusable - the tokens were computed,
            // logged, and then never drawn.
            //
            // The answer is read out of the map rather than off the array the
            // fetch above built, because the two are the same value by
            // construction and only one of them is what the map says. Answering
            // with nothing where the editor reads a stream is the failure this
            // whole layer exists to make loud, so it is said rather than drawn.
            const roles = cache.get(uri);
            if (roles === undefined)
              throw new Error(`the Khayyam language server answered ${path.basename(uri)} with roles that are not in the cache`);
            return new vscode.SemanticTokens(new Uint32Array(roles));
          },
        },
        // The legend is the editor's third required argument: it is the list the
        // token type indices in the data are read against, and without it the
        // editor has nothing to decode a computed stream with and discards it.
        // It is built once, from the legend the server advertised at handshake.
        legendOf,
      ),
      // A definition provider, which is what makes a go-to-definition ask the server at
      // all. This extension builds its own client rather than a library one, so a feature
      // the editor routes through a provider is one that has to be registered here: the
      // server answering `textDocument/definition` proves nothing to a reader whose editor
      // asks nothing, and a go-to-definition that finds nothing reads exactly like a file
      // with no declarations in it. What the server can answer is read at the handshake
      // above, so this is registered only when it says it answers definitions.
      ...(capabilities.definitionProvider
        ? [
            vscode.languages.registerDefinitionProvider(
              { language: "khayyam" },
              {
                /** @param {vscode.TextDocument} document
                 *  @param {vscode.Position} position */
                async provideDefinition(document, position) {
                  const uri = document.uri.toString();
                  const asked0 = (asked += 1);
                  report(`editor asked (call ${asked0}): ${path.basename(uri)} definition at line ${position.line + 1}`);
                  let answer;
                  try {
                    answer = /** @type {unknown} */ (
                      await live.request(
                        "textDocument/definition",
                        definitionRequest(uri, { line: position.line, character: position.character }),
                      )
                    );
                  } catch (error) {
                    // A request that did not answer is a fault in this layer and is said
                    // so here rather than shown as a name with no definition, which is the
                    // one answer a reader cannot act on and cannot tell from a real one.
                    report(`request FAILED: ${path.basename(uri)} could not be asked where a name is declared: ${messageOf(error)}`);
                    status.text = "$(warning) Khayyam: definition request failed";
                    status.tooltip = `the server did not answer where a name is declared: ${messageOf(error)}`;
                    status.show();
                    return [];
                  }
                  const target = readTarget(answer);
                  if (target === null) {
                    report(`no definition: ${path.basename(uri)} line ${position.line + 1} — nothing declares that name here`);
                    return [];
                  }
                  report(`definition: ${path.basename(uri)} line ${position.line + 1} is declared at ${path.basename(target.uri)} line ${/** @type {{ start: { line: number } }} */ (target.range).start.line + 1}`);
                  const range = /** @type {{ start: { line: number; character: number }; end: { line: number; character: number } }} */ (target.range);
                  return [
                    new vscode.Location(
                      vscode.Uri.parse(target.uri),
                      new vscode.Range(
                        range.start.line,
                        range.start.character,
                        range.end.line,
                        range.end.character,
                      ),
                    ),
                  ];
                },
              },
            ),
          ]
        : []),
      { dispose: () => live.child.kill() },
    );

    // A live server, a matched legend and a registered provider are three facts, and
    // none of them is the request path: that is walked only when a request comes back
    // carrying roles for a document the editor has. Nothing said so until the editor
    // happened to ask, so a provider the editor never called ended this log at
    // `ready` - which reads exactly like success, and cost three rounds to tell apart.
    // So the path is walked here, once per document this window already holds, and the
    // answer or its absence is what the reader is given.
    //
    // What is walked is the EXTENSION'S OWN request, made here, over the same
    // connection. It proves the server holds the document and answers roles for it, and
    // it proves nothing about the editor: only the `editor asked (call N)` lines above
    // are the editor calling the provider. So every line of this walk says so in the
    // line itself - a self-test is not the editor asking, and a log in which the two
    // read alike is how three rounds of a working feature came to look broken.
    report(`provider: registered for language "khayyam" with ${legend.length} token types`);
    const held = vscode.workspace.textDocuments.filter((document) => document.languageId === "khayyam");
    if (held.length === 0) {
      report(
        "self-test: no Khayyam document was open, so the server holds no document and the " +
          "self-test below has nothing to ask about — this is not the editor asking for anything",
      );
    }
    for (const document of held) {
      const name = path.basename(document.uri.toString());
      let result;
      try {
        result = /** @type {SemanticTokensAnswer} */ (
          await connection.request("textDocument/semanticTokens/full", {
            textDocument: { uri: document.uri.toString() },
          })
        );
      } catch (error) {
        fail("request", `${name} could not be asked for its roles: ${messageOf(error)}`);
        return;
      }
      const data = result?.data;
      if (!Array.isArray(data) || data.length === 0) {
        fail("request", `the server answered ${name} with no roles, so it holds no document it can analyse`);
        return;
      }
      report(
        `self-test: the extension asked its own server for ${name} and got ${data.length / 5} roles. ` +
          "This is the extension's own request, NOT the editor asking the provider for anything — " +
          "only an `editor asked (call N)` line above is the editor.",
      );
      // The definition path is walked the same way, and said the same way. A server that
      // answers roles for a document and a reader whose go-to-definition finds nothing are
      // two different worlds that look identical in a log, so the question is asked here
      // rather than left for the first reader to find out.
      if (!capabilities.definitionProvider) continue;
      // The first name this document DECLARES, walked out of the stream already in hand.
      // Both halves of that sentence are load-bearing, and the second was a day of this
      // self-test reporting nothing for the wrong reason.
      //
      // A name, first: a reserved word (`tp`), a subtype category, an inclusion's path, a
      // comment, a string, and a stray number or operator are all tokens the server
      // publishes, and asking where a reserved word is declared is answered with nothing
      // every time — a self-test whose answer is always the same is a self-test that proves
      // nothing.
      //
      // This document declares, second: the first two names in a Khayyam file are almost
      // always the ones that arrived by an `in`, because that is how a file starts, and a
      // name that arrived by an address is declared in the file it names — which no
      // manifest here declares how to reach. So a self-test that took the first name asked
      // about precisely the one kind of name that cannot have a definition, and printed
      // "nothing declares that name" for a file whose very next name it would have found.
      // Nothing is the same answer a provider that was never registered gives, which is
      // the one distinction this self-test exists to draw.
      //
      // The roles are named rather than excluded, and a role this file does not name is
      // skipped: the contract is where a new role arrives, and a role added tomorrow that
      // this list has not heard of is skipped rather than asked about. Failing towards
      // asking one name later is a self-test that is one line shorter; failing the other
      // way is one that asks about a path and calls it a name.
      const askable = new Set(
        [
          "capsule",
          "abstraction",
          "method",
          "scope",
          "type-reference",
          "variable",
          "method-local",
          "method-argument",
          "method-argument-type",
          "method-owner-type",
          "capsule-field",
          "identifier-reference",
        ]
          .map((role) => legend.indexOf(role))
          .filter((at) => at >= 0),
      );
      // The stream's shape, walked as the protocol states it. Five numbers per token:
      // how many lines down from the last one, how far along that line, how long, which
      // type, which modifiers. A line delta of zero means the token is on the same line
      // as the one before it, and the character is then a difference from that token's
      // character. A line delta of anything else means the character is stated outright,
      // counted from the start of its own line. The first token in the stream is a line
      // delta of zero from nothing, so it is the case that needs the rule rather than the
      // exception — a walk that treats every character as a difference drifts by one
      // token per line from the second one on, and the position it arrives at is a
      // position the server never heard of. Measured 2026-09-29 on [`main.kh`](../../../../main.kh):
      // a name on its eighth line was read as sitting at character 42 of a line that is
      // eighteen characters long.
      let at = 0;
      let line = 0;
      let character = 0;
      let named;
      while (at < data.length) {
        line += data[at];
        character = data[at] === 0 ? character + data[at + 1] : data[at + 1];
        if (askable.has(data[at + 3]) && data[at + 2] > 0) {
          named = { line, character };
          break;
        }
        at += 5;
      }
      if (named === undefined) continue;
      // Asked at the token's START, and not at the character after it. A name ends
      // where the next one begins, and where a name ends is where the next name stands,
      // so a request one character past the end asks about a name the editor is not on
      // and is answered with nothing every time. That reads exactly like a server that
      // knows no definitions, which is the one thing this self-test exists to
      // distinguish: a name is asked for from inside the name, never from beside it.
      let target;
      try {
        target = /** @type {unknown} */ (
          await live.request(
            "textDocument/definition",
            definitionRequest(document.uri.toString(), {
              line: named.line,
              character: named.character,
            }),
          )
        );
      } catch (error) {
        fail("request", `${name} could not be asked where a name is declared: ${messageOf(error)}`);
        return;
      }
      let where;
      try {
        where = readTarget(target);
      } catch (error) {
        fail("request", `${name} was answered something a reader cannot be sent to: ${messageOf(error)}`);
        return;
      }
      report(
        where === null
          ? `self-test: the extension asked its own server where the first name of ${name} is declared and ` +
              "the answer was nothing — that name is declared nowhere, which is an answer and not a fault. " +
              "This is the extension's own request, NOT the editor asking for anything."
          : `self-test: the extension asked its own server where the first name of ${name} is declared and was ` +
              `sent to ${path.basename(where.uri)} line ` +
              `${/** @type {{ start: { line: number } }} */ (where.range).start.line + 1}. This is the ` +
              "extension's own request, NOT the editor asking for anything.",
      );    }

    connection.child.on("exit", (/** @type {number | null} */ code) => {
      status.text = "$(warning) Khayyam: server stopped";
      status.tooltip = `the language server exited with code ${code}`;
      status.show();
      report(`the language server exited with code ${code}`);
    });
  } catch (error) {
    connection?.child.kill();
    fail(
      "handshake",
      `the language server did not answer: ${messageOf(error)}. Log: ${lines.length} lines in the Khayyam output channel.`,
    );
  }
}

function deactivate() {
  // The child process is registered as a subscription and dies with the host.
}

module.exports = { activate, deactivate };
