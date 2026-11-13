/* For license and copyright information please see the LEGAL file in the code repository */
import { readUnit } from "../../core/src/parse.ts";
import { analyze } from "../../core/src/frontend.ts";
import { readCommands } from "../../core/src/body.ts";
import { scan } from "../../core/src/scan.ts";
import { inclusionFindings } from "../../lsp/src/inclusions.ts";
import { unboundNameFindings } from "../../lsp/src/unbound-names.ts";
import { diagnosticOf, inclusionDiagnostic, unboundNameDiagnostic } from "../../lsp/src/diagnostics.ts";
import type { Position, Resolved } from "../../lsp/src/definition.ts";
import { identifySource, type SourceSnapshot, type SourceIdentity, type InspectionReach, type InclusionHop } from "../inspect-declaration/inspect-declaration.ts";

export interface SourceEdit { range: { start: Position; end: Position }; text: string }
export interface SourceChange { base: SourceIdentity; edits: SourceEdit[] }
export interface SourceProposal { uri: string; version?: number; wholeText?: string; change?: SourceChange }
export interface ValidationQuestion { proposal: SourceProposal; overlays?: SourceSnapshot[] }
export interface ValidationDiagnostic { word: string; message: string; source: SourceIdentity; range: { start: Position; end: Position }; phase: "reader" | "gate" }
export interface ValidationAnswer {
  snapshot: SourceIdentity;
  diagnostics: ValidationDiagnostic[];
  documents: SourceIdentity[];
  inclusions: InclusionHop[];
  checks: { subject: string; state: "complete" | "incomplete" | "unsupported"; reason: string }[];
  gateAccepted: boolean;
  typeSafetyEstablished: false;
  executionEstablished: false;
}

function refuse(reason: string): never {
  throw new Error(`Validation_Request_Refused: ${reason}`);
}

function record(value: unknown): value is Record<string, any> {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function validVersion(value: unknown): boolean {
  return value === undefined || (Number.isSafeInteger(value) && (value as number) >= 0);
}

function offset(text: string, place: Position): number {
  if (!record(place) || !Number.isSafeInteger(place.line) || place.line < 0 || !Number.isSafeInteger(place.character) || place.character < 0) refuse("invalid UTF-16 edit range");
  const lines = text.split("\n");
  const line = lines[place.line];
  if (line === undefined || place.character > (line.endsWith("\r") ? line.length - 1 : line.length)) refuse("invalid UTF-16 edit range");
  const at = lines.slice(0, place.line).reduce((sum, value) => sum + value.length + 1, 0) + place.character;
  const before = text.charCodeAt(at - 1);
  const after = text.charCodeAt(at);
  if (before >= 0xd800 && before <= 0xdbff && after >= 0xdc00 && after <= 0xdfff) refuse("edit range splits a UTF-16 surrogate pair");
  return at;
}

function bodySource(source: string, line: number): string {
  const scanned = scan(source);
  const tokens = scanned.tokens;
  const start = tokens.findIndex(token => token.line >= line && token.kind === "punct" && token.text === "{");
  if (start < 0) return "";
  const opening = tokens[start]!;
  let depth = 0;
  const lines = source.split("\n");
  const at = (token: { line: number; column: number }) => lines.slice(0, token.line - 1).reduce((sum, text) => sum + text.length + 1, 0) + token.column - 1;
  for (const token of tokens.slice(start)) {
    if (token.kind !== "punct") continue;
    if (token.text === "{") depth += 1;
    if (token.text === "}") {
      depth -= 1;
      if (depth === 0) return "\n".repeat(opening.line - line) + " ".repeat(opening.column - 1) + source.slice(at(opening), at(token));
    }
  }
  return "";
}

export function validateSource(request: ValidationQuestion, reach: InspectionReach): ValidationAnswer {
  if (!record(request) || !record(request.proposal)) refuse("a source proposal is required");
  const proposal = request.proposal;
  if (typeof proposal.uri !== "string" || !validVersion(proposal.version)) refuse("source URI and nonnegative integer version required");
  if ((typeof proposal.wholeText === "string") === (proposal.change !== undefined)) refuse("exactly one wholeText or change is required");
  if (proposal.wholeText !== undefined && typeof proposal.wholeText !== "string") refuse("wholeText must be text");
  const overlays = new Map<string, SourceSnapshot>();
  if (request.overlays !== undefined && !Array.isArray(request.overlays)) refuse("overlays must be an array");
  for (const source of request.overlays ?? []) {
    if (!record(source) || typeof source.uri !== "string" || typeof source.text !== "string" || !validVersion(source.version)) refuse("invalid overlay snapshot");
    if (overlays.has(source.uri)) refuse(`duplicate overlay URI ${source.uri}`);
    overlays.set(source.uri, { ...source });
  }
  let text = proposal.wholeText;
  if (proposal.change !== undefined) {
    const change = proposal.change;
    if (!record(change) || !record(change.base) || !Array.isArray(change.edits) || typeof change.base.hash !== "string" || !validVersion(change.base.version)) refuse("a change requires a base identity and edits");
    const held = overlays.get(proposal.uri);
    const baseText = held?.text ?? reach.held(proposal.uri);
    const baseVersion = held === undefined ? reach.version?.(proposal.uri) : held.version;
    if (baseText === undefined || change.base.uri !== proposal.uri || change.base.version !== baseVersion || identifySource({ uri: proposal.uri, text: baseText }).hash !== change.base.hash) refuse("stale base: URI, hash and version must match the held source");
    text = baseText;
    for (const edit of change.edits) {
      if (!record(edit) || !record(edit.range) || typeof edit.text !== "string") refuse("invalid edit range or replacement text");
      const start = offset(text, edit.range.start);
      const end = offset(text, edit.range.end);
      if (end < start) refuse("edit range ends before its start");
      text = text.slice(0, start) + edit.text + text.slice(end);
    }
  }
  const root: SourceSnapshot = { uri: proposal.uri, text: text!, ...(proposal.version === undefined ? {} : { version: proposal.version }) };
  const sources = new Map<string, SourceSnapshot>([[root.uri, root]]);
  const resolutions = new Map<string, Resolved>();
  const inclusions: InclusionHop[] = [];
  const diagnostics: ValidationDiagnostic[] = [];
  const held = (uri: string) => sources.get(uri)?.text ?? overlays.get(uri)?.text ?? reach.held(uri);
  const reading: InspectionReach = {
    held,
    resolve(address, from) {
      const key = JSON.stringify([from, address]);
      const previous = resolutions.get(key);
      if (previous !== undefined) return previous;
      const original = reach.resolve(address, from);
      const resolved = { ...original };
      if (original.found !== undefined) {
        const target = original.found;
        let pinned = sources.get(target.uri);
        if (pinned === undefined) {
          const overlay = overlays.get(target.uri);
          const heldText = reach.held(target.uri);
          pinned = overlay ?? { uri: target.uri, text: heldText ?? target.text,
            ...(heldText === undefined || reach.version?.(target.uri) === undefined ? {} : { version: reach.version!(target.uri) }) };
          sources.set(target.uri, { ...pinned });
        }
        resolved.found = { uri: pinned.uri, text: pinned.text };
      }
      resolutions.set(key, resolved);
      inclusions.push({ from, address, ...(resolved.found === undefined ? {} : { to: resolved.found.uri }),
        ...(resolved.via === undefined ? {} : { via: resolved.via }), ...(resolved.base === undefined ? {} : { base: resolved.base }),
        ...(resolved.because === undefined ? {} : { because: resolved.because }) });
      return resolved;
    },
  };
  let gateAccepted = true;
  const walked = new Set<string>();
  function walk(source: SourceSnapshot): void {
    if (walked.has(source.uri)) return;
    walked.add(source.uri);
    const identity = identifySource(source);
    const read = readUnit(source.uri, source.text);
    const append = (diagnostic: object, phase: "reader" | "gate") => {
      const value = diagnostic as { code: string; message: string; range: ValidationDiagnostic["range"] };
      diagnostics.push({ word: value.code, message: value.message, source: identity, range: value.range, phase });
    };
    for (const fault of read.faults) append(diagnosticOf(fault), "reader");
    if (read.faults.length > 0) gateAccepted = false;
    for (const declaration of read.unit.declarations) {
      if (declaration.form === "tp-mt" && declaration.body !== null) {
        const commands = readCommands(bodySource(source.text, declaration.line), declaration.line);
        if (!commands.ok) {
          append(diagnosticOf(commands.fault), "reader");
          gateAccepted = false;
        }
      }
      if (declaration.form !== "tp-in" && declaration.form !== "vr-in") continue;
      const resolved = reading.resolve(declaration.path, source.uri);
      if (resolved.found !== undefined) walk(sources.get(resolved.found.uri)!);
    }
    for (const finding of inclusionFindings(source.uri, source.text, reading)) append(inclusionDiagnostic(finding), "gate");
    for (const finding of unboundNameFindings(source.text)) append(unboundNameDiagnostic(finding), "gate");
    if (analyze(source.uri, source.text, { read: address => reading.resolve(address, source.uri).found?.text }).outcome !== "accept") gateAccepted = false;
  }
  walk(root);
  return {
    snapshot: identifySource(root), diagnostics, documents: [...sources.values()].map(identifySource), inclusions,
    gateAccepted, typeSafetyEstablished: false, executionEstablished: false,
    checks: [
      { subject: "reader-and-gate", state: "complete", reason: "existing reader and gate applied to every reached unit, with each URI pinned once" },
      { subject: "inclusion-resolution", state: inclusions.some(hop => hop.to === undefined) ? "incomplete" : "complete", reason: "uses the supplied reach and reports its resolution provenance; no unresolved address is guessed" },
      { subject: "method-and-argument-types", state: "unsupported", reason: "method existence, arity and argument/result type compatibility are not checked" },
      { subject: "qualified-and-variable-type-references", state: "unsupported", reason: "the gate skips qualified type names and variable declaration type references" },
      { subject: "type-safety-and-execution", state: "unsupported", reason: "diagnostic absence does not certify type safety or execution; no code is executed" },
    ],
  };
}
