// What a document yields: the role of every occurrence in it, and every fault met on the
// way. A file the frontend could not read in full still has the one, and a reader is told
// about the other rather than shown a confident answer.
//
// This is the layer a TextMate grammar cannot be. A grammar matches one line at a time and
// holds no symbol table, so it cannot know that a word used deep in a method body is the
// same word the file brought in through an `in` inclusion. Here the file's own
// declarations are the symbol table ([binding-table.ts](./binding-table.ts)), and a role
// follows the binding, never the position.
//
// This file walks the lines and says which of them is which; each shape is walked by the
// file that names it — what the scan read ([document-items.ts](./document-items.ts)), the
// blocks the file holds open ([blocks.ts](./blocks.ts)), a signature
// ([signature-roles.ts](./signature-roles.ts)), a statement
// ([statement-roles.ts](./statement-roles.ts)), and how an answer becomes a token
// ([role-emitter.ts](./role-emitter.ts)).
import { isKeyword } from "../../core/src/scan.ts";
import { readUnit } from "../../core/src/parse.ts";
import type { Declaration, Fault } from "../../core/src/sr.ts";
import { bindingsIn, DECLARED, included, type Bindings } from "./binding-table.ts";
import { declaredInBody } from "./body-declaration.ts";
import { openBlocks, type Declared } from "./blocks.ts";
import { itemsOnLine, placeOf, type Item } from "./document-items.ts";
import { emitterInto, type SemanticToken } from "./role-emitter.ts";
import { signatureRoles } from "./signature-roles.ts";
import { statementRoles } from "./statement-roles.ts";

export interface DocumentReading {
  roles: SemanticToken[];
  faults: Fault[];
}

/** What one walk over a document's lines left behind: the answers it gave, and what each
 *  block it opened had declared in it. */
interface Walked {
  roles: SemanticToken[];
  declared: Map<string, Declared>[];
}

export function analyse(source: string): DocumentReading {
  // A unit is read with recovery, because a reader is owed the part that was
  // understood: the parse is refused per declaration and the rest of the file
  // still holds, so one unreadable line does not take every other line's roles
  // with it. The faults come back beside the roles, and it is the server's job to
  // publish them — a role answered from a file the frontend could not read is
  // exactly the silent degradation this reading exists to end.
  const read = readUnit("document.kh", source);
  const declarations: Declaration[] = read.unit.declarations;
  const lines = source.split("\n");
  const byLine = itemsOnLine(source);
  const bindings = bindingsIn(declarations, byLine);

  // A body is read in two passes. The first binds what the bodies declare; the second
  // resolves what they use, and answers only the uses. Which reading of a body is right
  // is the language's, and both are consistent with what the language states — but a
  // forward-only pass would make a name two things, the body's own below its declaration
  // and a bare use above it, and a name is one thing wherever it stands.
  const bound = walk(lines, byLine, bindings);
  return { roles: walk(lines, byLine, bindings, bound.declared).roles, faults: read.faults };
}

function walk(
  lines: string[],
  byLine: Map<number, Item[]>,
  bindings: Bindings,
  alreadyDeclared?: Map<string, Declared>[],
): Walked {
  const blocks = openBlocks(alreadyDeclared);
  const tokens: SemanticToken[] = [];

  for (let line = 0; line < lines.length; line++) {
    const items = byLine.get(line) ?? [];
    const first = items[0];
    // The file's brace depth before and after this line says which block the line
    // stands in and whether it leaves one open behind it.
    const { before: depthHere, after: depthAfter } = blocks.entered(items);
    const enclosing = blocks.enclosing();
    const emitter = emitterInto(tokens, line, bindings);
    const resolve = (item: Item, fallback: string): void => emitter.resolve(item, fallback);

    // A declaration line: the declaration the parse read on this line. Paired by the
    // line it stands on, not by counting, so a line the parse could not read costs
    // itself and not the declaration after it.
    const insideBlock = enclosing !== undefined;
    if (first && first.kind === "ident" && (first.text === "tp" || first.text === "vr")) {
     if (insideBlock) {
        // A declaration inside a body is not a top-level declaration, and the two forms
        // the body admits are read by the file that names them.
        declaredInBody({ items, first, enclosing, depth: { before: depthHere, after: depthAfter }, blocks, emitter, line });
        continue;
      }      const declaration = bindings.declarationOnLine(line + 1);
      if (declaration) {
        emitter.at(first, "keyword", "reserved word");
        const name = items[1];
        if (name) {
          emitter.at(
            name,
            DECLARED[declaration.form].role,
            `${declaration.name} is ${DECLARED[declaration.form].origin}`,
            bindings.nameStandsAt(declaration),
            included(declaration) ? declaration.path : undefined,
          );
          const subtype = items[2];
          if (subtype && subtype.kind === "ident" && isKeyword(subtype.text)) {
            emitter.at(subtype, "subtype", `the ${subtype.text} subtype`);
          }
          if (included(declaration)) {
            const path = items.find((item) => item.kind === "string");
            if (path) {
              emitter.overQuotes(path, "file-uri", `the path ${declaration.path} routes to`);
            }
          }
          if (declaration.form === "tp-mt") {
            const parameters = signatureRoles(declaration, items, line, emitter);
            if (depthAfter > depthHere) blocks.opened("mt", depthAfter, { parameters });
          }
          if (declaration.form === "tp-cp" || declaration.form === "tp-ab") {
            const fields = new Set<string>();
            const composition = new Set<string>();
            if (declaration.form === "tp-cp") {
              for (const field of declaration.fields) fields.add(field.name);
              for (const entry of declaration.composition) composition.add(entry);
            } else {
              for (const entry of declaration.composition) composition.add(entry);
            }
            if (depthAfter > depthHere) {
              blocks.opened(declaration.form === "tp-cp" ? "cp" : "ab", depthAfter, {
                fields,
                composition,
              });
            }
          }
          if (declaration.form === "vr") {
            const type = items[2];
            if (type && type.kind === "ident") {
              resolve(type, "type-reference");
            }
          }
        }
      }
      continue;
    }

    // A closing brace on a line of its own carries no name, and the block it closed
    // has already been left above: the depth this line reached is what says which.
    const block = enclosing;

    if (block && (block.kind === "cp" || block.kind === "ab")) {
      const idents = items.filter((item) => item.kind === "ident");
      if (idents.length === 0) continue;
      if (idents.length >= 2) {
        // A field's name is declared on the line it stands on, which is what a reader
        // asking about it is sent to.
        emitter.at(idents[0]!, "capsule-field", `a field of the capsule above`, placeOf(line, idents[0]!));
        resolve(idents[1]!, "type-reference");
        for (const extra of idents.slice(2)) resolve(extra, "type-reference");
      } else {
        // A one-token line in a composition block is an abstraction name, which the
        // contract makes a type reference; a name this file included keeps its
        // inclusion role, because a role follows the binding.
        resolve(idents[0]!, "type-reference");
      }
      continue;
    }

    // The method a statement here belongs to, which is the nearest one open: a
    // scope's statements are written inside the method that holds it, and a parameter
    // of that method is that parameter wherever in its body it is used.
    const method = blocks.method();
    statementRoles(items, method === undefined ? undefined : {
      parameters: method.parameters,
      declares: (text) => blocks.declares(text),
      declaresMethod: (text) => bindings.bindingOf(text)?.form === "tp-mt",
    }, emitter);
  }

  return { roles: tokens, declared: blocks.collected() };
}

/** The roles alone, for a caller that has no use for the faults. */
export function semanticRoles(source: string): SemanticToken[] {
  return analyse(source).roles;
}
