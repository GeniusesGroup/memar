/* For license and copyright information please see the LEGAL file in the code repository */
import { contradictsDeclaredChange, type Change } from "./capabilities.ts";
import {
  diagnosticOf,
  inclusionDiagnostic,
  refusalDiagnostic,
  unboundNameDiagnostic,
} from "./diagnostics.ts";
import type { Reach } from "./definition.ts";
import { inclusionFindings } from "./inclusions.ts";
import { analyse } from "./semantic.ts";
import { notify } from "./transport.ts";
import { unboundNameFindings } from "./unbound-names.ts";

const documents = new Map<string, string>();
const versions = new Map<string, number>();

export function version(uri: string): number | undefined {
  return versions.get(uri);
}

export function holds(uri: string): boolean {
  return documents.has(uri);
}

export function text(uri: string): string | undefined {
  return documents.get(uri);
}

export function diagnosticsFor(uri: string, reach: Reach): object[] | undefined {
  const held = documents.get(uri);
  if (held === undefined) return undefined;
  return [
    ...analyse(held).faults.map(diagnosticOf),
    ...inclusionFindings(uri, held, reach).map(inclusionDiagnostic),
    ...unboundNameFindings(held).map(unboundNameDiagnostic),
  ];
}

export function open(uri: string, source: string, reach: Reach, atVersion?: number): string[] {
  documents.set(uri, source);
  if (atVersion === undefined) versions.delete(uri);
  else versions.set(uri, atVersion);
  return publish(uri, reach);
}

export function change(uri: string, changes: Change[], reach: Reach, atVersion?: number): string[] {
  const previous = versions.get(uri);
  if (atVersion !== undefined && previous !== undefined && atVersion <= previous) {
    return [notify("textDocument/publishDiagnostics", {
      uri, version: previous, diagnostics: [refusalDiagnostic(`document version ${atVersion} does not follow held version ${previous}`)],
    })];
  }
  const contradiction = contradictsDeclaredChange(changes);
  if (contradiction !== null) {
    return [notify("textDocument/publishDiagnostics", {
      uri,
      version: null,
      diagnostics: [refusalDiagnostic(contradiction)],
    })];
  }
  documents.set(uri, changes[0]!.text);
  if (atVersion === undefined) versions.delete(uri);
  else versions.set(uri, atVersion);
  return publish(uri, reach);
}

export function close(uri: string): string {
  documents.delete(uri);
  versions.delete(uri);
  return notify("textDocument/publishDiagnostics", { uri, diagnostics: [] });
}

function publish(uri: string, reach: Reach): string[] {
  const diagnostics = diagnosticsFor(uri, reach);
  if (diagnostics === undefined) return [];
  return [notify("textDocument/publishDiagnostics", { uri, version: null, diagnostics })];
}
