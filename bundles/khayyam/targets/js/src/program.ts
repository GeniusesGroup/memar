import { analyze, type FileSystem } from "../../../core/src/frontend.ts";
import type { Declaration, MethodDecl, Param, Unit } from "../../../core/src/sr.ts";
import { readCommands, type Command } from "../../../core/src/body.ts";
import { resolveImports, UnresolvedName } from "./emit.ts";
import { artifactPath } from "./layout.ts";
import type { LinkEntry, LinkMap } from "./link.ts";

/** One method of a compiled unit, as the representation carries it: the three
 *  groups of the signature and the commands of the body — or nothing at all, for
 *  a method that has no body. What a body-less method is depends on its owner:
 *  on a capsule it is the link form, whose implementation arrives when the
 *  program is run, and on an abstraction it is the contract form, which asks of
 *  an implementing capsule rather than of the link phase. */
export type MethodKind = "implemented" | "supplied" | "contract";

export interface CompiledMethod {
  kind: MethodKind;
  /** The name the artifact exports it under. A `$` joins the two names, and no
   *  identifier in the language can hold one, so a generated name can never
   *  collide with a name the author wrote. */
  exportedAs: string;
  owner: string;
  ownerParameter: string;
  influencing: Param[];
  influenced: Param[];
  commands: Command[] | null;
}

export interface CompiledUnit {
  uri: string;
  /** Where the unit's code stands: an artifact under the build root, or the
   *  module the map linked in its place. */
  path: string;
  /** A linked unit is not compiled at all — the map's declarations and exports
   *  stand in for the unit's own, which is the whole of what link-first means. */
  origin: "compiled" | "linked";
  /** The names this unit can name as types, and the unit that declares each. */
  types: Record<string, { uri: string; kind: "capsule" | "abstraction" }>;
  /** The fields each capsule declares, with the type each was declared as. */
  fields: Record<string, { name: string; type: string }[]>;
  /** The abstractions each composition names. */
  composition: Record<string, string[]>;
  /** Every method of the unit, by the name it is called under. */
  methods: Record<string, CompiledMethod>;
  /** The unit's variable declarations. */
  variables: { name: string; type: string }[];
  /** The export each type of the unit is known by outside it. */
  exports: Record<string, string>;
  /** The modules this unit's artifact imports, with the local name each import
   *  is known by inside it. */
  imports: {
    from: string;
    specifier: string;
    bindings: { exported: string; local: string }[];
  }[];
  /** The exported methods whose implementation the link phase supplies. */
  supplied: string[];
}

export interface CompiledProgram {
  /** The unit the program was asked for. */
  root: string;
  /** Where artifacts are written, as a path from the repository root. */
  buildRoot: string;
  /** The units in the order they were reached. */
  units: CompiledUnit[];
}

export interface CompileRequest {
  /** The URI of the unit the program starts from. */
  root: string;
  files: FileSystem;
  links: LinkMap;
  /** Where artifacts are written, as a path from the repository root. */
  buildRoot: string;
  /** A unit the caller already holds the declarations of, offered before the
   *  unit's own source is read. This is the cache's seam: a unit standing from
   *  an earlier build is not read, and a caller that answers nothing reads every
   *  unit as usual. */
  reuse?: (uri: string) => CompiledUnit | undefined;
}

export interface Compiled {
  ok: true;
  program: CompiledProgram;
}

export interface CompileRefused {
  ok: false;
  problem: string;
}

export type CompileResult = Compiled | CompileRefused;

class Refusal {
  readonly problem: string;

  constructor(problem: string) {
    this.problem = problem;
  }
}

function methodKey(owner: string, name: string): string {
  return `${owner}$${name}`;
}

class Builder {
  private readonly request: CompileRequest;
  private readonly files: FileSystem;
  private readonly links: LinkMap;
  private readonly buildRoot: string;
  private readonly units: CompiledUnit[] = [];
  private readonly byUri = new Map<string, CompiledUnit>();

  constructor(request: CompileRequest) {
    this.request = request;
    this.files = request.files;
    this.links = request.links;
    this.buildRoot = request.buildRoot;
  }

  private empty(uri: string, origin: CompiledUnit["origin"], path: string): CompiledUnit {
    return {
      uri,
      path,
      origin,
      types: {},
      fields: {},
      composition: {},
      methods: {},
      variables: [],
      exports: {},
      imports: [],
      supplied: [],
    };
  }

  private read(uri: string, importer: string): Unit {
    const source = this.files.read(uri);
    if (source === undefined) {
      throw new Refusal(importer === uri ? `${uri} is not there` : `${importer}: ${uri} is not there`);
    }
    const result = analyze(uri, source, this.files);
    if (result.outcome === "refuse") {
      const where = result.line === undefined ? "" : ` at line ${result.line}`;
      throw new Refusal(`${uri} is refused: ${result.reason}${where}`);
    }
    return result.unit;
  }

  /** The map is asked before a unit's own source is read, so a link never depends
   *  on the `.kh` file it stands in for. An entry whose module cannot be read is
   *  not a link: the unit falls back to its own source, which is the rule the
   *  link-first decision keeps. */
  private linkable(uri: string): LinkEntry | undefined {
    const entry = this.links[uri];
    if (entry === undefined) return undefined;
    if (this.files.read(entry.module) === undefined) return undefined;
    return entry;
  }

  private addLinked(uri: string, entry: LinkEntry): CompiledUnit {
    const unit = this.register(uri, this.empty(uri, "linked", entry.module));
    for (const [name, declaration] of Object.entries(entry.declares)) {
      if (declaration.kind === "method") {
        unit.methods[methodKey(declaration.owner, name)] = {
          kind: "supplied",
          exportedAs: name,
          owner: declaration.owner,
          ownerParameter: declaration.ownerParameter,
          influencing: declaration.influencing.map((parameter) => ({ ...parameter })),
          influenced: declaration.influenced.map((parameter) => ({ ...parameter })),
          commands: null,
        };
        continue;
      }
      unit.types[name] = { uri, kind: declaration.kind };
      if (declaration.kind === "capsule") unit.fields[name] = [];
      else unit.composition[name] = [];
    }
    for (const [name, exported] of Object.entries(entry.provides)) {
      unit.exports[name] = exported;
    }
    return unit;
  }

  private addCompiled(uri: string, importer: string): CompiledUnit {
    const parsed = this.read(uri, importer);
    const unit = this.register(uri, this.empty(uri, "compiled", artifactPath(this.buildRoot, uri)));
    const methods: MethodDecl[] = [];
    for (const declaration of parsed.declarations) {
      this.addDeclaration(unit, declaration, methods);
    }
    for (const declaration of methods) this.addMethod(unit, declaration);
    return unit;
  }

  private addDeclaration(unit: CompiledUnit, declaration: Declaration, methods: MethodDecl[]): void {
    switch (declaration.form) {
      case "tp-cp":
        unit.types[declaration.name] = { uri: unit.uri, kind: "capsule" };
        unit.fields[declaration.name] = declaration.fields;
        unit.exports[declaration.name] = declaration.name;
        return;
      case "tp-ab":
        unit.types[declaration.name] = { uri: unit.uri, kind: "abstraction" };
        unit.composition[declaration.name] = [...declaration.composition];
        unit.exports[declaration.name] = declaration.name;
        return;
      case "tp-in": {
        const included = this.include(unit, declaration.path);
        const kind = included.types[declaration.name]?.kind;
        if (kind === undefined) {
          throw new Refusal(`${unit.uri}: ${declaration.path} declares no ${declaration.name}`);
        }
        unit.types[declaration.name] = { uri: declaration.path, kind };
        const exported = included.exports[declaration.name];
        if (exported !== undefined) unit.exports[declaration.name] = exported;
        return;
      }
      case "vr-in":
        this.include(unit, declaration.path);
        return;
      case "vr":
        unit.variables.push({ name: declaration.name, type: declaration.type });
        return;
      case "tp-mt":
        methods.push(declaration);
        return;
      case "tp-sc":
        // A scope outside a body is refused by the frontend; one inside a body is
        // a command of that body, not a declaration of the unit.
        return;
    }
  }

  private include(unit: CompiledUnit, path: string): CompiledUnit {
    const known = this.byUri.get(path);
    if (known !== undefined) return known;
    const standing = this.reuse(path);
    if (standing !== undefined) {
      this.register(path, standing);
      return standing;
    }
    const entry = this.linkable(path);
    return entry === undefined ? this.addCompiled(path, unit.uri) : this.addLinked(path, entry);
  }

  /** The unit a caller already holds, taken as it stands: the driver's job is to
   *  reach the declarations of every unit a program names, and a unit whose
   *  declarations are already known needs nothing read. */
  private reuse(uri: string): CompiledUnit | undefined {
    const standing = this.request.reuse?.(uri);
    if (standing === undefined) return undefined;
    return { ...standing, uri: standing.uri === uri ? standing.uri : uri };
  }

  private register(uri: string, unit: CompiledUnit): CompiledUnit {
    unit.uri = uri;
    this.units.push(unit);
    this.byUri.set(uri, unit);
    return unit;
  }

  private addMethod(unit: CompiledUnit, declaration: MethodDecl): void {
    const [owner] = declaration.owner;
    if (owner === undefined) {
      throw new Refusal(
        `${unit.uri}: ${declaration.name} names no owner, and every call is made on one`,
      );
    }
    let body: Command[] | null = null;
    if (declaration.body !== null) {
      const commands = readCommands(declaration.body, declaration.line);
      if (!commands.ok) {
        throw new Refusal(
          `${unit.uri}: line ${declaration.line}: the body of ${declaration.name} is refused: ${commands.fault.reason}`,
        );
      }
      body = commands.commands;
    }
    const key = methodKey(owner.type, declaration.name);
    // A body-less method is the language's contract form on an abstraction and
    // its link form on a concrete capsule (docs/khayyam/khayyam.md → Method). A
    // contract is a statement about an implementing capsule rather than a
    // request for an implementation, so it is neither written into an artifact
    // nor waited on at run time; calling one is the question the backend has no
    // answer to, and says so where the call stands.
    const kind: MethodKind =
      body !== null
        ? "implemented"
        : unit.types[owner.type]?.kind === "abstraction"
          ? "contract"
          : "supplied";
    unit.methods[key] = {
      kind,
      exportedAs: key,
      owner: owner.type,
      ownerParameter: owner.name,
      influencing: declaration.influencing.map((parameter) => ({ ...parameter })),
      influenced: declaration.influenced.map((parameter) => ({ ...parameter })),
      commands: body,
    };
    if (kind === "implemented") {
      unit.exports[key] = key;
      return;
    }
    if (kind === "contract") return;
    unit.exports[key] = key;
    unit.supplied.push(key);
  }

  build(root: string): CompiledProgram {
    const entry = this.linkable(root);
    if (entry === undefined) this.addCompiled(root, root);
    else this.addLinked(root, entry);
    const program: CompiledProgram = { root, buildRoot: this.buildRoot, units: this.units };
    for (const unit of this.units) {
      if (unit.origin !== "compiled") continue;
      unit.imports = resolveImports(program, unit);
    }
    return program;
  }
}

/** Reads a `.kh` unit and everything it reaches, and holds what the backend
 *  translates. A unit is compiled only when no conformant equivalent is linked
 *  for it, which is the link-first rule. */
export function compileProgram(request: CompileRequest): CompileResult {
  try {
    return { ok: true, program: new Builder(request).build(request.root) };
  } catch (error) {
    if (error instanceof Refusal) return { ok: false, problem: error.problem };
    if (error instanceof UnresolvedName) {
      return { ok: false, problem: `${request.root}: ${error.message}` };
    }
    throw error;
  }
}

export { emitUnit } from "./emit.ts";
