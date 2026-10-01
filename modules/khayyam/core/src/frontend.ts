import { parseUnit } from "./parse.ts";
import {
  declaredName,
  declarationKind,
  referencedTypes,
  type Declaration,
  type RefusalReason,
  type Unit,
} from "./sr.ts";

export interface FileSystem {
  read(path: string): string | undefined;
}

export interface Accepted {
  outcome: "accept";
  unit: Unit;
}

export interface Refused {
  outcome: "refuse";
  reason: RefusalReason;
  line?: number;
}

export type Analysis = Accepted | Refused;

function findDeclaration(unit: Unit, name: string): Declaration | undefined {
  return unit.declarations.find(
    (declaration) => declaredName(declaration) === name,
  );
}

function analyzeImports(
  unit: Unit,
  fileSystem: FileSystem,
): Refused | undefined {
  const visible = new Map<string, "tp" | "vr">();

  for (const declaration of unit.declarations) {
    if (declaration.form === "tp-in" || declaration.form === "vr-in") {
      const source = fileSystem.read(declaration.path);
      if (source === undefined) return { outcome: "refuse", reason: "unresolved-import" };
      const parsed = parseUnit(declaration.path, source);
      // A file that is there and does not parse is not a URI that failed to
      // resolve; the fault is the one the target itself reports, at its own line.
      if (!parsed.ok) {
        return { outcome: "refuse", reason: parsed.fault.reason, line: parsed.fault.line };
      }
      const target = findDeclaration(parsed.unit, declaration.name);
      if (target === undefined) {
        return { outcome: "refuse", reason: "name-not-declared" };
      }
      const wanted = declaration.form === "tp-in" ? "tp" : "vr";
      if (declarationKind(target) !== wanted) {
        return { outcome: "refuse", reason: "kind-mismatch" };
      }
      visible.set(declaration.name, wanted);
    }
  }

  for (const declaration of unit.declarations) {
    if (declaration.form !== "tp-in" && declaration.form !== "vr-in") {
      visible.set(declaredName(declaration), declarationKind(declaration));
    }
  }

  for (const declaration of unit.declarations) {
    for (const reference of referencedTypes(declaration)) {
      if (reference.includes(".")) continue;
      if (!visible.has(reference)) {
        return { outcome: "refuse", reason: "unbound-type-name" };
      }
    }
  }

  return undefined;
}

export function analyze(
  path: string,
  source: string,
  fileSystem: FileSystem,
): Analysis {
  const parsed = parseUnit(path, source);
  if (!parsed.ok) {
    return { outcome: "refuse", reason: parsed.fault.reason, line: parsed.fault.line };
  }
  const refused = analyzeImports(parsed.unit, fileSystem);
  if (refused) return refused;
  return { outcome: "accept", unit: parsed.unit };
}
