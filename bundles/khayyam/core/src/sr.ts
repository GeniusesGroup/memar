/* For license and copyright information please see the LEGAL file in the code repository */

export type Subtype = "in" | "cp" | "mt" | "ab" | "sc";

export interface Fault {
  reason: RefusalReason;
  line: number;
  column: number;
  length: number;
  text: string;
  extent: "line" | "declaration" | "file";
  because?: Fault;
}

export interface TypeInclude {
  form: "tp-in";
  name: string;
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
  | "unbound-type-name"
  | "capsule-in-abstraction-signature"
  | "unresolved-type-declaration";

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
