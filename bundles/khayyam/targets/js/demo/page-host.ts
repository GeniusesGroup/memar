/* For license and copyright information please see the LEGAL file in the code repository */

/** The host glue of the page that compiles in a browser (target.md → Compiling in
 *  a browser): it compiles the units it is handed and loads what they emitted.
 *  It is JavaScript written for the page, not Khayyam, because nothing compiles
 *  Khayyam in a browser except this target's compiler, and a host's side of a run
 *  is the host's. It imports nothing: the compiler it uses and the URL a text is
 *  loaded from are handed to it, so the same glue runs in a page (Blob URLs, the
 *  compiler the build step wrote) and under a test (`data:` URLs, the sources). */

import type { CompiledProgram, CompileRequest, CompileResult } from "../src/program.ts";
import type { MapRead, MapRefused } from "../src/link.ts";
import type { Loader, Module } from "../src/run.ts";

/** The compiler the glue is handed: the three functions it calls. */
export interface Compiler {
  compileProgram: (request: CompileRequest) => CompileResult;
  emitUnit: (program: CompiledProgram, uri: string) => string;
  readLinkMap: (text: string) => MapRead | MapRefused;
}

/** One unit the page was handed: its URI and its source. */
export interface UnitSource {
  uri: string;
  source: string;
}

export interface CompileUnitsRequest {
  compiler: Compiler;
  /** The units, the first being the program's root. */
  units: UnitSource[];
  /** The link map's own text. */
  linkMap: string;
  /** Where the artifacts would stand, which fixes the specifiers between them. */
  buildRoot: string;
}

export type CompiledUnits =
  | { ok: true; program: CompiledProgram; texts: Record<string, string> }
  | { ok: false; problem: string };

/** Compiles the units handed over, reading no unit it was not handed, and emits
 *  each compiled unit's text. */
export function compileUnits(request: CompileUnitsRequest): CompiledUnits {
  const root = request.units[0];
  if (root === undefined) return { ok: false, problem: "no unit was handed over" };
  const map = request.compiler.readLinkMap(request.linkMap);
  if (!map.ok) return { ok: false, problem: `the link map is not a map: ${map.problems.join("; ")}` };
  const sources = new Map(request.units.map((unit) => [unit.uri, unit.source]));
  const compiled = request.compiler.compileProgram({
    root: root.uri,
    files: { read: (path) => sources.get(path) },
    links: map.map,
    buildRoot: request.buildRoot,
  });
  if (!compiled.ok) return compiled;
  const texts: Record<string, string> = {};
  for (const unit of compiled.program.units) {
    if (unit.origin === "compiled") texts[unit.uri] = request.compiler.emitUnit(compiled.program, unit.uri);
  }
  return { ok: true, program: compiled.program, texts };
}

export interface LoaderRequest {
  program: CompiledProgram;
  texts: Record<string, string>;
  /** The URL a module's text is loaded from: a Blob URL in a page. */
  urlOf: (text: string) => string;
}

/** A loader for `run`: each unit is loaded after the units it imports, with each
 *  specifier the program records for it replaced by the URL of the unit it names,
 *  since a relative specifier cannot be resolved against a Blob URL. */
export function loaderOf(request: LoaderRequest): Loader {
  const urls = new Map<string, string>();
  const reaching = new Set<string>();
  const urlFor = (uri: string): string => {
    const known = urls.get(uri);
    if (known !== undefined) return known;
    if (reaching.has(uri)) {
      throw new Error(`${uri} imports itself through another unit, which this page cannot load from Blob URLs`);
    }
    const unit = request.program.units.find((candidate) => candidate.uri === uri);
    if (unit === undefined) throw new Error(`${uri} is not one of the program's units`);
    let text = request.texts[uri];
    if (text === undefined) throw new Error(`${uri} has no text this page compiled`);
    reaching.add(uri);
    for (const entry of unit.imports) {
      const written = `from "${entry.specifier}";`;
      if (!text.includes(written)) {
        throw new Error(`the artifact of ${uri} does not import ${entry.from} as the program records it`);
      }
      text = text.replace(written, `from "${urlFor(entry.from)}";`);
    }
    reaching.delete(uri);
    const url = request.urlOf(text);
    urls.set(uri, url);
    return url;
  };
  const modules = new Map<string, Promise<Module>>();
  return (uri) => {
    let module = modules.get(uri);
    if (module === undefined) {
      module = import(urlFor(uri)) as Promise<Module>;
      modules.set(uri, module);
    }
    return module;
  };
}
