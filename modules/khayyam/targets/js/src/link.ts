import type { FileSystem } from "../../../core/src/frontend.ts";

/** A parameter as a method signature writes it: a name and the type it carries. */
export interface SignatureParam {
  name: string;
  type: string;
}

/** What the linked module declares in place of the unit's own declarations. A
 *  link that stood in for a unit without saying what the unit declared would
 *  leave the unit's contracts — an abstraction's methods especially — stated
 *  nowhere. */
export type LinkedDeclaration =
  | { kind: "capsule" }
  | { kind: "abstraction" }
  | {
      kind: "method";
      owner: string;
      ownerParameter: string;
      influencing: SignatureParam[];
      influenced: SignatureParam[];
    };

/** One link-map entry: what a URI's declarations are served by, and the record
 *  of the check that let a link stand in for compiling the unit. The record is
 *  the point of the entry — a link that silently replaced the semantic
 *  representation as the source of truth would leave nothing to check. */
export interface LinkEntry {
  /** The JavaScript module that provides the unit's declarations, written as a
   *  path from the repository root. This is where the JavaScript module lives, and
   *  it is not a claim about what an `in` address resolves from: no module manifest
   *  exists yet, so nothing resolves any address, and where an address's base comes
   *  from is stated by the import address rule rather than by this field. */
  module: string;
  /** The protocol document the implementation was checked against. */
  protocol: string;
  /** What was checked, each naming the section of the document it was read at. */
  checked: { requirement: string; at: string }[];
  /** The unit's declarations, each as the map states the module has it. */
  declares: Record<string, LinkedDeclaration>;
  /** The declarations that are values at run time, each with the module export
   *  that provides it. A type no program names as a value — a scope's own
   *  primitive, for one — is declared without being provided. */
  provides: Record<string, string>;
}

export type LinkMap = Record<string, LinkEntry>;

export interface MapRead {
  ok: true;
  map: LinkMap;
}

export interface MapRefused {
  ok: false;
  problems: string[];
}

export type MapResult = MapRead | MapRefused;

export interface LinkProblem {
  uri: string;
  about: string;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function entryProblems(uri: string, entry: unknown): string[] {
  if (!isRecord(entry)) return [`${uri}: the entry is not a table`];
  const problems: string[] = [];
  if (typeof entry["module"] !== "string" || entry["module"] === "") {
    problems.push(`${uri}: the entry names no module`);
  }
  if (typeof entry["protocol"] !== "string" || entry["protocol"] === "") {
    problems.push(`${uri}: the entry names no protocol document`);
  }
  const checked = entry["checked"];
  if (!Array.isArray(checked) || checked.length === 0) {
    problems.push(`${uri}: the entry records no conformance check`);
  } else {
    for (const check of checked) {
      if (
        !isRecord(check) ||
        typeof check["requirement"] !== "string" ||
        typeof check["at"] !== "string"
      ) {
        problems.push(`${uri}: a recorded check names no requirement or no section`);
      }
    }
  }
  const provides = entry["provides"];
  if (!isRecord(provides) || Object.keys(provides).length === 0) {
    problems.push(`${uri}: the entry provides nothing`);
  } else {
    for (const [name, exported] of Object.entries(provides)) {
      if (typeof exported !== "string" || exported === "") {
        problems.push(`${uri}: ${name} is provided by no export`);
      }
    }
  }
  const declares = entry["declares"];
  if (!isRecord(declares) || Object.keys(declares).length === 0) {
    problems.push(`${uri}: the entry declares nothing in place of the unit`);
  } else {
    for (const [name, declaration] of Object.entries(declares)) {
      const problemsFor = declarationProblems(name, declaration);
      problems.push(...problemsFor.map((problem) => `${uri}: ${problem}`));
    }
    for (const name of Object.keys(provides as Record<string, string>)) {
      if (!(name in declares)) {
        problems.push(`${uri}: ${name} is provided but not declared`);
      }
    }
  }
  return problems;
}

function declarationProblems(name: string, declaration: unknown): string[] {
  if (!isRecord(declaration)) return [`${name} is declared with no shape`];
  const kind = declaration["kind"];
  if (kind === "capsule" || kind === "abstraction") return [];
  if (kind !== "method") return [`${name} is declared as neither a capsule, an abstraction, nor a method`];
  const problems: string[] = [];
  if (typeof declaration["owner"] !== "string" || declaration["owner"] === "") {
    problems.push(`${name} is a method that names no owner`);
  }
  if (typeof declaration["ownerParameter"] !== "string") {
    problems.push(`${name} is a method whose owner is not named`);
  }
  for (const group of ["influencing", "influenced"] as const) {
    const parameters = declaration[group];
    if (!Array.isArray(parameters)) {
      problems.push(`${name} is a method with no ${group} group`);
      continue;
    }
    for (const parameter of parameters) {
      if (
        !isRecord(parameter) ||
        typeof parameter["name"] !== "string" ||
        typeof parameter["type"] !== "string"
      ) {
        problems.push(`${name} is a method with a parameter that names no name or type`);
      }
    }
  }
  return problems;
}

/** Reads the map from its source, or says every way the source is not a map. A
 *  map is configuration rather than a unit, so a fault in it is named in words
 *  and not with the frontend's labels, which are the labels a `.kh` unit is
 *  refused with. */
export function readLinkMap(source: string): MapResult {
  let parsed: unknown;
  try {
    parsed = JSON.parse(source);
  } catch {
    return { ok: false, problems: ["the map is not JSON"] };
  }
  if (!isRecord(parsed)) return { ok: false, problems: ["the map is not a table"] };
  const problems: string[] = [];
  for (const [uri, entry] of Object.entries(parsed)) {
    if (!uri.endsWith(".kh")) problems.push(`${uri}: a link is keyed by the URI of a .kh unit`);
    problems.push(...entryProblems(uri, entry));
  }
  if (problems.length > 0) return { ok: false, problems };
  return { ok: true, map: parsed as LinkMap };
}

/** The section titles a document states, as the anchors a check is recorded
 *  against. A heading is read as the text after its last run of `#`. */
function sectionsOf(document: string): Set<string> {
  const sections = new Set<string>();
  for (const line of document.split("\n")) {
    const match = /^#{1,6}\s+(.*\S)\s*$/.exec(line);
    if (match !== null) sections.add(match[1]!);
  }
  return sections;
}

/** Reports every entry that does not resolve: a module that is not there, a
 *  protocol document that is not there, and a recorded check standing at a
 *  section the document does not have. A check is only worth recording if the
 *  document can be opened at it, so an anchor no document carries is a fault of
 *  the record and not of the implementation it describes. */
export function checkLinks(map: LinkMap, files: FileSystem): LinkProblem[] {
  const problems: LinkProblem[] = [];
  for (const [uri, entry] of Object.entries(map)) {
    if (files.read(entry.module) === undefined) {
      problems.push({ uri, about: `the module ${entry.module} is not there` });
    }
    const document = files.read(entry.protocol);
    if (document === undefined) {
      problems.push({ uri, about: `the protocol document ${entry.protocol} is not there` });
      continue;
    }
    const sections = sectionsOf(document);
    for (const check of entry.checked) {
      if (!sections.has(check.at)) {
        problems.push({
          uri,
          about: `the protocol document has no section ${check.at}`,
        });
      }
    }
  }
  return problems;
}
