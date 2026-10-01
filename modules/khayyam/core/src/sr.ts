export type Subtype = "in" | "cp" | "mt" | "ab" | "sc";

/** One thing the frontend could not read, at the place it stands. A fault is
 *  reported, never repaired: it says the toolchain did not understand this, so a
 *  reader is never shown an answer that was guessed past it. */
export interface Fault {
  reason: RefusalReason;
  /** One-based, as a refusal message counts. */
  line: number;
  /** One-based; a string's column is its first character inside the quotes. */
  column: number;
  /** How many characters the fault covers. */
  length: number;
  /** What stood there. */
  text: string;
  /** What the fault cost, which is where reading went on: the rest of its line,
   *  the declaration it stood in, or the rest of the file. */
  extent: "line" | "declaration" | "file";
  /** The fault this one is a consequence of, when it is one. A fault that follows
   *  another says so and names it, because a reader told only what the second fault
   *  is cannot act on it: the second is what the first left behind, so repairing the
   *  first is what takes the second away. It is not a replacement for the fault's own
   *  reason and extent — those stay, so the file's broken structure is still reported
   *  where it stands. */
  because?: Fault;
}

export interface TypeInclude {
  form: "tp-in";
  name: string;
  /** The line the declaration was read on. A declaration occupies one line and the
   *  line's break terminates it (docs/khayyam/khayyam.md, Declaration separator), so
   *  this identifies it, and it is what a reader that recovers per declaration needs
   *  to pair the declaration with the line it stands on. */
  line: number;
  path: string;
}

export interface VarInclude {
  form: "vr-in";
  name: string;
  line: number;
  path: string;
}

export interface Field {
  name: string;
  type: string;
}

export interface CapsuleDecl {
  form: "tp-cp";
  name: string;
  line: number;
  fields: Field[];
  composition: string[];
}

export interface AbstractionDecl {
  form: "tp-ab";
  name: string;
  line: number;
  composition: string[];
}

export interface Param {
  name: string;
  type: string;
}

export interface MethodDecl {
  form: "tp-mt";
  name: string;
  line: number;
  owner: Param[];
  influencing: Param[];
  influenced: Param[];
  body: string | null;
}

export interface ScopeDecl {
  form: "tp-sc";
  name: string;
  line: number;
  body: string | null;
}

export interface VarDecl {
  form: "vr";
  name: string;
  line: number;
  type: string;
}

export type Declaration =
  | TypeInclude
  | VarInclude
  | CapsuleDecl
  | AbstractionDecl
  | MethodDecl
  | ScopeDecl
  | VarDecl;

export interface Unit {
  path: string;
  declarations: Declaration[];
}

/** Every way this toolchain can refuse a unit, in one list: the labels a
 *  scanner, a parser, and the analyser all draw from, so no module has to
 *  restate one and none of them can invent one the others do not know. */
export type RefusalReason =
  | "declaration-form"
  | "missing-subtype"
  | "keyword-as-identifier"
  | "semicolon"
  | "scope-placement"
  | "unterminated-string"
  | "unterminated-block-comment"
  | "unexpected-character"
  | "unbalanced-block"
  | "unresolved-import"
  | "name-not-declared"
  | "kind-mismatch"
  | "unbound-type-name";

export function declaredName(declaration: Declaration): string {
  return declaration.name;
}

export function declarationKind(declaration: Declaration): "tp" | "vr" {
  return declaration.form === "vr" ? "vr" : "tp";
}

export function referencedTypes(declaration: Declaration): string[] {
  switch (declaration.form) {
    case "tp-cp":
      return [
        ...declaration.fields.map((field) => field.type),
        ...declaration.composition,
      ];
    case "tp-ab":
      return declaration.composition;
    case "tp-mt":
      return [
        ...declaration.owner.map((param) => param.type),
        ...declaration.influencing.map((param) => param.type),
        ...declaration.influenced.map((param) => param.type),
      ];
    default:
      return [];
  }
}
