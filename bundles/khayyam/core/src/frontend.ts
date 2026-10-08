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

/** Every name the unit sees, and the kind of declaration each one came from. A tool that
 *  asks whether a name binds — a rename, say, which must know that a file brings its names
 *  from `in` declarations and from its own declarations and in which order those two layers
 *  are laid over each other — is asking this question and not the analyser's, which asks
 *  whether the whole unit may be compiled at all. The two are kept apart so that a second
 *  answer to "is this name visible here" cannot grow beside this one. A refusal is reported
 *  beside the set rather than in place of it, because the set is what a caller has when it
 *  is asking about names and not about a verdict. */
export function visibleNames(
  unit: Unit,
  fileSystem: FileSystem,
): { visible: Map<string, "tp" | "vr">; refusal?: Refused } {
  const visible = new Map<string, "tp" | "vr">();

  for (const declaration of unit.declarations) {
    if (declaration.form === "tp-in" || declaration.form === "vr-in") {
      const source = fileSystem.read(declaration.path);
      if (source === undefined) return { visible, refusal: { outcome: "refuse", reason: "unresolved-import" } };
      const parsed = parseUnit(declaration.path, source);
      // A file that is there and does not parse is not a URI that failed to
      // resolve; the fault is the one the target itself reports, at its own line.
      if (!parsed.ok) {
        return { visible, refusal: { outcome: "refuse", reason: parsed.fault.reason, line: parsed.fault.line } };
      }
      const target = findDeclaration(parsed.unit, declaration.name);
      if (target === undefined) {
        return { visible, refusal: { outcome: "refuse", reason: "name-not-declared" } };
      }
      const wanted = declaration.form === "tp-in" ? "tp" : "vr";
      if (declarationKind(target) !== wanted) {
        return { visible, refusal: { outcome: "refuse", reason: "kind-mismatch" } };
      }
      visible.set(declaration.name, wanted);
    }
  }

  for (const declaration of unit.declarations) {
    if (declaration.form !== "tp-in" && declaration.form !== "vr-in") {
      visible.set(declaredName(declaration), declarationKind(declaration));
    }
  }

  return { visible };
}

function analyzeImports(
  unit: Unit,
  fileSystem: FileSystem,
): Refused | undefined {
  const { visible, refusal } = visibleNames(unit, fileSystem);
  if (refusal) return refusal;

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
