import type { Command } from "../../../core/src/body.ts";
import { directory, relativeSpecifier } from "./layout.ts";
import type { CompiledMethod, CompiledProgram, CompiledUnit } from "./program.ts";

/** A name the artifact cannot resolve. The backend does not answer one by
 *  guessing what the name was meant to be, so a body it cannot translate is a
 *  refusal the compiler reports, not an artifact that is nearly right. */
export class UnresolvedName extends Error {
  readonly name: string;
  readonly why: string;

  constructor(name: string, why: string) {
    super(`${name}: ${why}`);
    this.name = name;
    this.why = why;
  }
}

/** A name a body binds. A cell is what every variable is: the language passes
 *  every variable of a call strictly by reference
 *  (docs/khayyam/khayyam.md → Method), so what a call writes into is a slot, and
 *  a slot is one object a caller hands over and a callee writes through. */
type Local =
  | { kind: "owner"; name: string; type: string }
  | { kind: "cell"; name: string; type: string }
  | { kind: "scope"; name: string };

interface Block {
  cells: Map<string, Local>;
  commands: Command[];
  scopes: { name: string; block: Block }[];
}

function emptyBlock(): Block {
  return { cells: new Map(), commands: [], scopes: [] };
}

function isParameter(method: CompiledMethod, name: string): boolean {
  if (name === method.ownerParameter) return true;
  for (const parameter of [...method.influencing, ...method.influenced]) {
    if (parameter.name === name) return true;
  }
  return false;
}

/** What a body binds. Parameters come from the signature; a `vr` and a scope
 *  come from the commands themselves; a nested scope's names are its own. The
 *  cells and the scopes of a block are lifted out of its command order, because a
 *  scope may be named by a call standing above the line that declares it, and a
 *  cell's existence carries no effect of its own. */
function bind(method: CompiledMethod): Block {
  const root = emptyBlock();
  root.cells.set(method.ownerParameter, {
    kind: "owner",
    name: method.ownerParameter,
    type: method.owner,
  });
  for (const parameter of method.influencing) {
    root.cells.set(parameter.name, { kind: "cell", name: parameter.name, type: parameter.type });
  }
  for (const parameter of method.influenced) {
    root.cells.set(parameter.name, { kind: "cell", name: parameter.name, type: parameter.type });
  }
  const walk = (block: Block, commands: Command[]): void => {
    for (const command of commands) {
      if (command.form === "declare") {
        block.cells.set(command.name, { kind: "cell", name: command.name, type: command.type });
        continue;
      }
      if (command.form === "scope") {
        const inner = emptyBlock();
        block.scopes.push({ name: command.name, block: inner });
        // A scope is a name of the body like any other: a call names it as its
        // own argument, and a scope is what an argument position admits
        // (docs/khayyam/khayyam.md → Method → Type-level arguments for sc and mt).
        block.cells.set(command.name, { kind: "scope", name: command.name });
        walk(inner, command.body);
        continue;
      }
      block.commands.push(command);
    }
  };
  walk(root, method.commands ?? []);
  return root;
}

function unitDeclaring(program: CompiledProgram, uri: string): CompiledUnit {
  const holder = program.units.find((candidate) => candidate.uri === uri);
  if (holder === undefined) throw new UnresolvedName(uri, "nothing in the program holds it");
  return holder;
}

function typeDeclaredIn(unit: CompiledUnit, name: string): string {
  const declared = unit.types[name];
  if (declared === undefined) {
    throw new UnresolvedName(name, "no type of this unit or of one it includes is named so");
  }
  return declared.uri;
}

function methodCalled(
  program: CompiledProgram,
  unit: CompiledUnit,
  owner: string,
  name: string,
): { unit: CompiledUnit; method: CompiledMethod } {
  const holder = unitDeclaring(program, typeDeclaredIn(unit, owner));
  const method = holder.methods[`${owner}$${name}`];
  if (method === undefined) {
    throw new UnresolvedName(`${owner}$${name}`, `no method of that name on the type ${owner}`);
  }
  if (method.kind === "contract") {
    // A contract asks of an implementing capsule what the abstraction requires,
    // and this backend resolves a call by the receiver's declared type — it has
    // no dispatch over capsules it did not see. The refusal stands where the call
    // is, rather than a method being emitted that would call nothing.
    throw new UnresolvedName(
      `${owner}$${name}`,
      "is a contract of an abstraction, and this target resolves a call by the receiver's declared type",
    );
  }
  return { unit: holder, method };
}

/** The value a type stands for, where a value is required: the receiver of a call
 *  made on the parent type, or a type-level argument
 *  (docs/khayyam/khayyam.md → Scope, and → Method → Type-level arguments). */
function markerOf(
  program: CompiledProgram,
  unit: CompiledUnit,
  name: string,
): { uri: string; exported: string } {
  const uri = typeDeclaredIn(unit, name);
  const exported = unitDeclaring(program, uri).exports[name];
  if (exported === undefined) {
    throw new UnresolvedName(name, "no module of the program provides it as a value");
  }
  return { uri, exported };
}

type LocalNamer = (uri: string, exported: string) => string;

/** The local name a declaration of another unit is known by inside this artifact.
 *  A `$` begins every name the artifact writes for itself, and no identifier in
 *  the language can hold one, so a local can never collide with a name an author
 *  wrote. */
function namer(unit: CompiledUnit): LocalNamer {
  const taken = new Set(Object.values(unit.exports));
  const chosen = new Map<string, string>();
  return (uri, exported) => {
    const key = `${uri} ${exported}`;
    const known = chosen.get(key);
    if (known !== undefined) return known;
    let local = `$${exported}`;
    let count = 1;
    while (taken.has(local)) {
      count += 1;
      local = `$${exported}$${count}`;
    }
    taken.add(local);
    chosen.set(key, local);
    return local;
  };
}

function findLocal(chain: Block[], name: string): Local | undefined {
  for (const level of chain) {
    const found = level.cells.get(name);
    if (found !== undefined) return found;
  }
  return undefined;
}

type Invocation = Extract<Command, { form: "invoke" }>;

interface Reached {
  uri: string;
  exported: string;
}

/** A field of the capsule a method belongs to, named the way a body reaches it:
 *  the owner parameter, a dot, and the field's name. What a field is, is what a
 *  `vr` is — a slot the program writes through and a call hands over — so this is
 *  the only form of it a body may write: the privacy rule is about a *passed*
 *  capsule's fields (docs/khayyam/encapsulation.md → Capsule Structure and
 *  Privacy), and a method reaching its own capsule's state is what that rule
 *  leaves to the capsule's own methods. */
function fieldOf(
  program: CompiledProgram,
  unit: CompiledUnit,
  method: CompiledMethod,
  name: string,
): { name: string; type: string } | undefined {
  const prefix = `${method.ownerParameter}.`;
  if (!name.startsWith(prefix)) return undefined;
  const field = name.slice(prefix.length);
  if (field === "" || field.includes(".")) return undefined;
  return unitDeclaring(program, typeDeclaredIn(unit, method.owner)).fields[method.owner]?.find(
    (one) => one.name === field,
  );
}

/** One command read against the program's declarations: which unit holds the
 *  method it calls, and which of its own names are values. */
interface Reading {
  receiver: string;
  /** The field the receiver is, where the receiver is a field rather than a
   *  variable the body binds. */
  receiverField: string | undefined;
  method: Reached;
  influencing: { name: string; marker: Reached | undefined; field: string | undefined }[];
  influenced: string[];
}

function read(
  program: CompiledProgram,
  unit: CompiledUnit,
  method: CompiledMethod,
  chain: Block[],
  command: Invocation,
): Reading {
  const bound = findLocal(chain, command.receiver);
  if (bound !== undefined && bound.kind === "scope") {
    throw new UnresolvedName(
      command.receiver,
      "a scope is a branch body, not a receiver: a call is made on a value or on the parent type",
    );
  }
  const onField = bound === undefined ? fieldOf(program, unit, method, command.receiver) : undefined;
  const marker =
    bound === undefined && onField === undefined ? markerOf(program, unit, command.receiver) : undefined;
  const owner = bound !== undefined ? bound.type : onField === undefined ? command.receiver : onField.type;
  const called = methodCalled(program, unit, owner, command.method);
  const influencing = command.influencing.map((argument) => {
    const held = findLocal(chain, argument);
    const field = held === undefined ? fieldOf(program, unit, method, argument) : undefined;
    return {
      name: argument,
      marker: held === undefined && field === undefined ? markerOf(program, unit, argument) : undefined,
      field: field?.name,
    };
  });
  for (const argument of command.influenced) {
    if (findLocal(chain, argument) !== undefined) continue;
    if (fieldOf(program, unit, method, argument) !== undefined) {
      // A field is a variable and a variable is a slot, so the write would be the
      // shape the language already has. What is open is whether a call may be
      // given one to write, and that is a rule of this level rather than a claim
      // about the language, so it stands open here instead of a backend answering
      // it by translating.
      throw new UnresolvedName(
        argument,
        "a call cannot influence a field: what a call writes is a name the body binds, and whether a field is one of those is what the rules of this level hold open",
      );
    }
    throw new UnresolvedName(argument, "a call cannot influence a name this body does not bind");
  }
  return {
    receiver: command.receiver,
    receiverField: onField?.name,
    method: { uri: called.unit.uri, exported: called.method.exportedAs },
    influencing,
    influenced: [...command.influenced],
  };
}

function eachInvocation(
  program: CompiledProgram,
  unit: CompiledUnit,
  method: CompiledMethod,
  block: Block,
  chain: Block[],
  visit: (reading: Reading, chain: Block[]) => void,
): void {
  for (const command of block.commands) {
    if (command.form === "invoke") visit(read(program, unit, method, chain, command), chain);
  }
  for (const scope of block.scopes) {
    eachInvocation(program, unit, method, scope.block, [...chain, scope.block], visit);
  }
}

/** The modules an artifact imports, and the local name each import is known by
 *  inside it. The backend asks for this before it emits anything, so every name
 *  the artifact would reach for is one the artifact can reach. */
export function resolveImports(
  program: CompiledProgram,
  unit: CompiledUnit,
): CompiledUnit["imports"] {
  const local = namer(unit);
  const found = new Map<string, { from: string; exported: string; local: string }>();
  const need = (reached: Reached): void => {
    if (reached.uri === unit.uri) return;
    const key = `${reached.uri} ${reached.exported}`;
    if (found.has(key)) return;
    found.set(key, {
      from: reached.uri,
      exported: reached.exported,
      local: local(reached.uri, reached.exported),
    });
  };
  for (const method of Object.values(unit.methods)) {
    if (method.commands === null) continue;
    const block = bind(method);
    eachInvocation(program, unit, method, block, [block], (reading, chain) => {
      need(reading.method);
      for (const argument of reading.influencing) {
        if (argument.marker !== undefined) need(argument.marker);
      }
      if (findLocal(chain, reading.receiver) === undefined && reading.receiverField === undefined) {
        need(markerOf(program, unit, reading.receiver));
      }
    });
  }
  const byModule = new Map<string, { exported: string; local: string }[]>();
  for (const reached of found.values()) {
    const bindings = byModule.get(reached.from) ?? [];
    bindings.push({ exported: reached.exported, local: reached.local });
    byModule.set(reached.from, bindings);
  }
  return [...byModule.entries()].map(([from, bindings]) => ({
    from,
    specifier: relativeSpecifier(directory(unit.path), unitDeclaring(program, from).path),
    bindings: bindings.sort((left, right) =>
      left.exported < right.exported ? -1 : left.exported > right.exported ? 1 : 0,
    ),
  }));
}

function indent(depth: number): string {
  return "    ".repeat(depth);
}

function parametersOf(method: CompiledMethod): string {
  return [
    method.ownerParameter,
    ...method.influencing.map((parameter) => parameter.name),
    ...method.influenced.map((parameter) => parameter.name),
  ].join(", ");
}

function valueOf(local: Local): string {
  if (local.kind === "cell") return `${local.name}$.value`;
  if (local.kind === "scope") return `$${local.name}$`;
  return local.name;
}

/** What a call hands over where its argument is a variable: the slot itself and
 *  not what is in it. The language passes every variable of a call strictly by
 *  reference (docs/khayyam/khayyam.md → Method) and states that the three groups
 *  are one list of variable references, so a call that received a value would be
 *  handing over something the callee cannot write through — and a field, whose
 *  slot is the capsule's own, is exactly the case that shows it. */
function referenceOf(local: Local): string {
  if (local.kind === "cell") return `${local.name}$`;
  if (local.kind === "scope") return `$${local.name}$`;
  return local.name;
}

function markerExpression(
  program: CompiledProgram,
  unit: CompiledUnit,
  name: string,
  local: LocalNamer,
): string {
  const marker = markerOf(program, unit, name);
  return marker.uri === unit.uri ? marker.exported : local(marker.uri, marker.exported);
}

function emitMethod(
  program: CompiledProgram,
  unit: CompiledUnit,
  method: CompiledMethod,
  local: LocalNamer,
): string[] {
  if (method.kind === "contract") return [];
  if (method.kind === "supplied") {
    const parameters = parametersOf(method);
    // A call hands over variables, and a variable is a slot, so a supplied
    // implementation is handed the slots too: the language states that a call
    // passes every variable of a call strictly by reference, and the owner of a
    // body-less method is the callee of last resort. The receiver is not one of
    // them — a call is made on a value.
    const variables = [...method.influencing, ...method.influenced];
    const handed = [
      method.ownerParameter,
      ...variables.map((parameter) => `${parameter.name}$`),
    ].join(", ");
    const cells = variables.map(
      (parameter) => `${indent(1)}const ${parameter.name}$ = ${parameter.name};`,
    );
    return [
      `export function ${method.exportedAs}(${parameters}) {`,
      ...cells,
      `${indent(1)}return $supplied["${method.exportedAs}"](${handed});`,
      "}",
    ];
  }
  const block = bind(method);
  const lines: string[] = [];
  for (const parameter of [...method.influencing, ...method.influenced]) {
    lines.push(`${indent(1)}const ${parameter.name}$ = ${parameter.name};`);
  }
  lines.push(...emitBlock(program, unit, method, block, [block], 1, local));
  return [`export function ${method.exportedAs}(${parametersOf(method)}) {`, ...lines, "}"];
}

function emitBlock(
  program: CompiledProgram,
  unit: CompiledUnit,
  method: CompiledMethod,
  block: Block,
  chain: Block[],
  depth: number,
  local: LocalNamer,
): string[] {
  const lines: string[] = [];
  for (const bound of block.cells.values()) {
    if (bound.kind !== "cell") continue;
    if (isParameter(method, bound.name)) continue;
    lines.push(`${indent(depth)}const ${bound.name}$ = { value: undefined };`);
  }
  for (const scope of block.scopes) {
    lines.push(`${indent(depth)}function $${scope.name}$() {`);
    lines.push(
      ...emitBlock(program, unit, method, scope.block, [...chain, scope.block], depth + 1, local),
    );
    lines.push(`${indent(depth)}}`);
  }
  for (const command of block.commands) {
    if (command.form === "return") {
      lines.push(`${indent(depth)}return;`);
      continue;
    }
    if (command.form !== "invoke") continue;
    const reading = read(program, unit, method, chain, command);
    const bound = findLocal(chain, command.receiver);
    const owner = method.ownerParameter;
    const receiver =
      reading.receiverField !== undefined
        ? `${owner}.${reading.receiverField}.value`
        : bound === undefined
          ? markerExpression(program, unit, command.receiver, local)
          : valueOf(bound);
    const name =
      reading.method.uri === unit.uri
        ? reading.method.exported
        : local(reading.method.uri, reading.method.exported);
    const influencing = reading.influencing
      .map((argument) => {
        if (argument.field !== undefined) return `${owner}.${argument.field}`;
        const found = findLocal(chain, argument.name);
        return found === undefined
          ? markerExpression(program, unit, argument.name, local)
          : referenceOf(found);
      })
      .join(", ");
    const influenced = reading.influenced
      .map((argument) => `${findLocal(chain, argument)!.name}$`)
      .join(", ");
    // The three groups are one call: the language separates them so a reader can
    // see which variables influence and which are influenced
    // (docs/khayyam/khayyam.md → Method), and states that in the underlying layer
    // they are the same thing — one list of variable references.
    const arguments_ = [receiver, influencing, influenced]
      .filter((part) => part !== "")
      .join(", ");
    lines.push(`${indent(depth)}${name}(${arguments_});`);
  }
  return lines;
}

const PROVENANCE = [
  "// An ES module generated from a Khayyam unit. It is a build product and",
  "// never a source of truth: the semantic representation is.",
];

const SUPPLY = [
  "const $supplied = Object.create(null);",
  "",
  "// A body-less method's implementation is supplied when the program is linked and",
  "// run: the body-less method is the language's own signal that the implementation",
  "// comes from the link phase (docs/khayyam/khayyam.md → Method).",
  "export function supply(implementations) {",
  "    Object.assign($supplied, implementations);",
  "}",
];

/** The artifact of one unit: an ES module, and nothing else. Everything it says
 *  about the program it came from is read out of the representation it was given,
 *  so the artifact decides nothing the representation did not already say. */
export function emitUnit(program: CompiledProgram, uri: string): string {
  const unit = unitDeclaring(program, uri);
  if (unit.origin !== "compiled") {
    throw new UnresolvedName(uri, "a linked unit is not compiled, so it has no artifact");
  }
  const local = namer(unit);
  const imports = resolveImports(program, unit);
  const lines: string[] = [`// ${uri}`, ...PROVENANCE, ""];
  for (const dependency of imports) {
    const bindings = dependency.bindings
      .map((binding) => `${binding.exported} as ${binding.local}`)
      .join(", ");
    lines.push(`import { ${bindings} } from "${dependency.specifier}";`);
  }
  if (imports.length > 0) lines.push("");
  if (unit.supplied.length > 0) lines.push(...SUPPLY, "");
  for (const [name, fields] of Object.entries(unit.fields)) {
    // A field is a variable, and a variable is a cell, so the slot is the
    // language's and what is in it is the host's: a host still creates every
    // value (docs/khayyam/khayyam.md → Separation of Syntax and Governance), and
    // it hands the values over rather than the slots.
    lines.push(
      fields.length === 0
        ? `export class ${name} { }`
        : [
            `export class ${name} {`,
            "    constructor(values) {",
            ...fields.map(
              (field) =>
                `        this.${field.name} = { value: values === undefined ? undefined : values.${field.name} };`,
            ),
            "    }",
            "}",
          ].join("\n"),
      "",
    );
  }
  for (const name of Object.keys(unit.composition)) {
    lines.push(`export const ${name} = { type: "${name}" };`, "");
  }
  for (const method of Object.values(unit.methods)) {
    // A contract is a statement about an implementing capsule, so there is
    // nothing of it in an artifact.
    const emitted = emitMethod(program, unit, method, local);
    if (emitted.length > 0) lines.push(...emitted, "");
  }
  return lines.join("\n");
}
