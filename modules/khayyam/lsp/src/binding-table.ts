// What a name in a document binds to, and what that binding IS: the role a declaration's
// own name carries when it is declared, where this document declares the name, and the
// URI a name that arrived by an inclusion came through.
//
// The table is the whole of what a role follows. A role says what a name IS, never where
// it appears, so the role is asked of the declaration and never of the position — which
// is why this table is built once per document and handed to every line's walk rather
// than rebuilt as each line is read.
import { placeOf, type Item, type Place } from "./document-items.ts";
import type { Declaration, TypeInclude, VarInclude } from "../../core/src/sr.ts";

/** The role a declaration's own name carries when it is declared, and where the
 *  declaration came from — one entry per declaration form, because a form is one
 *  thing said two ways and the two ways have to be changed together. */
export const DECLARED: Record<Declaration["form"], { role: string; origin: string }> = {
  "tp-in": { role: "included-type", origin: "included from another file" },
  "vr-in": { role: "included-variable", origin: "included from another file" },
  "tp-cp": { role: "capsule", origin: "a Capsule declared in this file" },
  "tp-ab": { role: "abstraction", origin: "an Abstraction declared in this file" },
  "tp-mt": { role: "method", origin: "a Method declared in this file" },
  "tp-sc": { role: "scope", origin: "a Scope declared in this file" },
  vr: { role: "variable", origin: "a Variable declared in this file" },
};

/** Whether a declaration arrived by an inclusion, and so names a declaration that is
 *  not in this file. */
export function included(declaration: Declaration): declaration is TypeInclude | VarInclude {
  return declaration.form === "tp-in" || declaration.form === "vr-in";
}

export interface Bindings {
  /** Which declaration a name in this document binds to, or nothing when nothing here
   *  declares it. */
  bindingOf(name: string): Declaration | undefined;
  /** Where the name this document binds is declared, in this document. A name that
   *  arrived by an inclusion has none: it is declared in the file its URI addresses. */
  placeOf(name: string): Place | undefined;
  /** Where a declaration's own name stands, which is where this document first shows
   *  the name — on the inclusion line itself, for a name that arrived by one. */
  nameStandsAt(declaration: Declaration): Place | undefined;
  /** The declaration the parse read on a line, whose lines are one-based as the
   *  representation counts them. */
  declarationOnLine(line: number): Declaration | undefined;
}

/** The table a document's declarations make, paired with the items the scan found on
 *  their lines. */
export function bindingsIn(declarations: Declaration[], byLine: Map<number, Item[]>): Bindings {
  // The file's own declarations are the symbol table, each declaration paired with
  // the line it stands on — a declaration carries its own line because the
  // language terminates one with that line's break, so a file read with recovery
  // (where one declaration can be missing) still pairs every declaration with the
  // right line. A later declaration of the same name does not displace an
  // inclusion: a name collision is an architecture error, not a disambiguation
  // problem.
  const bindings = new Map<string, Declaration>();
  const bindingPlaces = new Map<string, Place>();
  /** Where each declaration's own name stands. A declaration occupies one line and the
   *  line's break terminates it, so its name is the second thing on that line; the scan
   *  found it there, and the representation carries the line and not the column. */
  const declarationPlaces = new Map<Declaration, Place>();
  for (const declaration of declarations) {
    const name = (byLine.get(declaration.line - 1) ?? [])[1];
    if (name === undefined || name.text !== declaration.name) continue;
    declarationPlaces.set(declaration, placeOf(declaration.line - 1, name));
  }
  for (const declaration of declarations) {
    if (bindings.has(declaration.name)) continue;
    bindings.set(declaration.name, declaration);
    // An inclusion is not a declaration of the name: the name is declared in the file
    // the URI addresses, so there is no place for it in this one. Which file is
    // `includedThrough` for.
    if (included(declaration)) continue;
    const declared = declarationPlaces.get(declaration);
    if (declared !== undefined) bindingPlaces.set(declaration.name, declared);
  }
  const declarationOnLine = new Map<number, Declaration>();
  for (const declaration of declarations) declarationOnLine.set(declaration.line, declaration);

  return {
    bindingOf: (name) => bindings.get(name),
    placeOf: (name) => bindingPlaces.get(name),
    nameStandsAt: (declaration) => declarationPlaces.get(declaration),
    declarationOnLine: (line) => declarationOnLine.get(line),
  };
}
