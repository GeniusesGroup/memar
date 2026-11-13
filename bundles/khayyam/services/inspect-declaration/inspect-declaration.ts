/* For license and copyright information please see the LEGAL file in the code repository */

import { createHash } from "node:crypto";
import { readUnit } from "../../core/src/parse.ts";
import type { Declaration, MethodDecl, Param } from "../../core/src/sr.ts";
import { definitionAt, type Definition, type Position, type Reach, type Resolved } from "../../lsp/src/definition.ts";
import { analyse } from "../../lsp/src/semantic.ts";

export interface SourceSnapshot { uri: string; text: string; version?: number }
export interface SourceIdentity { uri: string; hash: string; version?: number }
export interface InspectionReach extends Reach { version?(uri: string): number | undefined }
export interface InclusionHop { from: string; address: string; to?: string; via?: string; base?: Resolved["base"]; because?: string }
export interface ResolutionIssue { word: string; reason: string; uri: string }
export interface MethodSignature { owner: Param[]; influencing: Param[]; influenced: Param[] }
export interface DeclarationEvidence {
  name: string;
  category?: "cp" | "ab" | "mt" | "sc" | "vr";
  role: string;
  location: { uri: string; range: { start: Position; end: Position } };
  snapshot: SourceIdentity;
  provenance: InclusionHop[];
  signature?: MethodSignature;
  methods?: { extent: "direct-in-reached-units"; complete: false; entries: DeclarationEvidence[] };
}
export interface InspectionAnswer {
  state: "resolved" | "unresolved" | "incomplete" | "not-a-name";
  snapshot: SourceIdentity;
  reach: {
    extent: "inclusion-closure";
    complete: boolean;
    documents: SourceIdentity[];
    inclusions: InclusionHop[];
    issues: ResolutionIssue[];
  };
  declaration?: DeclarationEvidence;
}

export function identifySource(snapshot: SourceSnapshot): SourceIdentity {
  return {
    uri: snapshot.uri,
    hash: `sha256:${createHash("sha256").update(snapshot.text, "utf8").digest("hex")}`,
    ...(snapshot.version === undefined ? {} : { version: snapshot.version }),
  };
}

export function inspectDeclaration(source: SourceSnapshot, position: Position, reach: InspectionReach): InspectionAnswer {
  const snapshots = new Map<string, SourceSnapshot>([[source.uri, { ...source }]]);
  const resolutions = new Map<string, Resolved>();
  const inclusions: InclusionHop[] = [];
  const issues: ResolutionIssue[] = [];
  let tracing: InclusionHop[] | undefined;
  const held = (uri: string): string | undefined => snapshots.get(uri)?.text ?? reach.held(uri);
  const reading: Reach = {
    held,
    resolve(address, from) {
      const key = JSON.stringify([from, address]);
      let resolved = resolutions.get(key);
      if (resolved === undefined) {
        const original = reach.resolve(address, from);
        resolved = { ...original };
        if (original.found !== undefined) {
          const target = original.found;
          let fixed = snapshots.get(target.uri);
          if (fixed === undefined) {
            const overlay = reach.held(target.uri);
            fixed = { uri: target.uri, text: overlay ?? target.text,
              ...(overlay === undefined || reach.version?.(target.uri) === undefined ? {} : { version: reach.version!(target.uri) }) };
            snapshots.set(target.uri, fixed);
          }
          resolved.found = { uri: fixed.uri, text: fixed.text };
        }
        resolutions.set(key, resolved);
      }
      const hop: InclusionHop = {
        from, address,
        ...(resolved.found === undefined ? {} : { to: resolved.found.uri }),
        ...(resolved.via === undefined ? {} : { via: resolved.via }),
        ...(resolved.base === undefined ? {} : { base: resolved.base }),
        ...(resolved.because === undefined ? {} : { because: resolved.because }),
      };
      tracing?.push(hop);
      return resolved;
    },
  };
  const occurrence = analyse(source.text).roles.find(token => token.line === position.line &&
    token.startChar <= position.character && position.character < token.startChar + token.length);
  const named = occurrence !== undefined && !["keyword", "subtype", "file-uri", "string", "comment"].includes(occurrence.role);
  const provenance: InclusionHop[] = [];
  tracing = provenance;
  const definition = named ? definitionAt(source.uri, source.text, position, reading) : null;
  tracing = undefined;
  if (definition === null && named && provenance.length > 0 && provenance.every(hop => hop.to !== undefined)) {
    const visited = new Set([source.uri]);
    for (const hop of provenance) {
      if (visited.has(hop.to!)) {
        issues.push({ word: "inclusion-cycle", reason: "the name's inclusion path returns to a document already visited", uri: hop.from });
        break;
      }
      visited.add(hop.to!);
    }
  }
  const walked = new Set<string>();
  const units = new Map<string, Declaration[]>();
  function walk(uri: string): void {
    if (walked.has(uri)) return;
    walked.add(uri);
    const snapshot = snapshots.get(uri)!;
    const read = readUnit(uri, snapshot.text);
    units.set(uri, read.unit.declarations);
    for (const fault of read.faults) {
      issues.push({ word: fault.reason, reason: `source could not be read at ${fault.line}:${fault.column}`, uri });
    }
    for (const declaration of read.unit.declarations) {
      if (declaration.form !== "tp-in" && declaration.form !== "vr-in") continue;
      const resolved = reading.resolve(declaration.path, uri);
      const hop: InclusionHop = { from: uri, address: declaration.path,
        ...(resolved.found === undefined ? {} : { to: resolved.found.uri }),
        ...(resolved.via === undefined ? {} : { via: resolved.via }),
        ...(resolved.base === undefined ? {} : { base: resolved.base }),
        ...(resolved.because === undefined ? {} : { because: resolved.because }) };
      inclusions.push(hop);
      if (resolved.found === undefined) {
        issues.push({ word: "unresolved-import", reason: resolved.because ?? "the address resolved to no document", uri });
      } else walk(resolved.found.uri);
    }
  }
  walk(source.uri);
  function evidence(found: Definition, origin: InclusionHop[]): DeclarationEvidence {
    const snapshot = snapshots.get(found.uri)!;
    const declaration = units.get(found.uri)?.find(entry => entry.line === found.line + 1 && entry.name === found.name);
    const token = analyse(snapshot.text).roles.find(entry => entry.line === found.line && entry.startChar === found.startChar);
    const category = declaration === undefined || declaration.form === "tp-in" || declaration.form === "vr-in" ? undefined
      : declaration.form === "vr" ? "vr" : declaration.form.slice(3) as DeclarationEvidence["category"];
    return {
      name: found.name, ...(category === undefined ? {} : { category }), role: token?.role ?? "identifier-reference",
      location: { uri: found.uri, range: { start: { line: found.line, character: found.startChar }, end: { line: found.line, character: found.startChar + found.length } } },
      snapshot: identifySource(snapshot), provenance: origin,
      ...(declaration?.form !== "tp-mt" ? {} : { signature: signature(declaration) }),
    };
  }
  let declaration: DeclarationEvidence | undefined;
  if (definition !== null) {
    declaration = evidence(definition, provenance);
    if (declaration.category === "cp" || declaration.category === "ab") {
      const entries: DeclarationEvidence[] = [];
      for (const [uri, declarations] of units) {
        const text = snapshots.get(uri)!.text;
        const tokens = analyse(text).roles;
        for (const method of declarations) {
          if (method.form !== "tp-mt") continue;
          const owner = method.owner[0];
          if (owner === undefined || owner.type !== declaration.name) continue;
          const ownerToken = tokens.find(token => token.line === method.line - 1 && token.text === owner.type);
          if (ownerToken === undefined) continue;
          const target = definitionAt(uri, text, { line: ownerToken.line, character: ownerToken.startChar }, reading);
          if (target === null || target.uri !== definition.uri || target.line !== definition.line || target.startChar !== definition.startChar) continue;
          const nameToken = tokens.find(token => token.line === method.line - 1 && token.text === method.name && token.declaredAt?.startChar === token.startChar);
          if (nameToken === undefined) continue;
          entries.push(evidence({ uri, name: method.name, line: nameToken.line, startChar: nameToken.startChar, length: nameToken.length }, []));
        }
      }
      declaration.methods = { extent: "direct-in-reached-units", complete: false, entries };
    }
  }
  return {
    state: !named ? "not-a-name" : declaration !== undefined ? "resolved" :
      issues.length > 0 ? "incomplete" : "unresolved",
    snapshot: identifySource(source),
    reach: { extent: "inclusion-closure", complete: issues.length === 0, documents: [...snapshots.values()].map(identifySource), inclusions, issues },
    ...(declaration === undefined ? {} : { declaration }),
  };
}

function signature(method: MethodDecl): MethodSignature {
  return { owner: method.owner.map(entry => ({ ...entry })), influencing: method.influencing.map(entry => ({ ...entry })), influenced: method.influenced.map(entry => ({ ...entry })) };
}
