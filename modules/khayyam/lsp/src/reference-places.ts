import { braceDepth, type Item } from "./document-items.ts";
import type { Declaration } from "../../core/src/sr.ts";

// Where a name a declaration references stands: the three shapes the parse gave a reference,
// each walked to find the place it stands in.
//
// This is a placement question and not a binding one. Which names a declaration references is
// `referencedTypes`' to answer ([core/src/sr.ts](../../core/src/sr.ts)), and it is answered in
// [unbound-names.ts](./unbound-names.ts), which hands this walk the names it is to place. The
// two are kept apart so that the walk below cannot become a second answer to the first: it
// decides where a name stands and never whether it binds, and a name it is not handed is a name
// it says nothing about.
//
// Each walk follows the shape the parse gave the declaration rather than a shape of its own,
// and each stops where the parse stopped. A signature is one line and its body was carried as
// text rather than read as declarations, so a name in a body is not a reference and is not
// walked; a field or composition block is read to the brace that closes it, and a block never
// closed costs the file that declaration and takes no walk with it.
//
// A form the parse reads no reference for is not walked, and the switch says so at the case
// rather than falling through: a form added to `referencedTypes` without being walked here
// would be a name asked about and never placed, and that is the one way the two answers about a
// name could part company without anything saying so.

/** The last line the scan read anything on, which bounds every walk that follows a block: a
 *  document whose block never closes would otherwise walk off its own text. */
export function lastLine(byLine: Map<number, Item[]>): number {
  let last = 0;
  for (const line of byLine.keys()) if (line > last) last = line;
  return last;
}

/** Where the names `unbound` are named by this declaration, in the order they stand.
 * @param declaration the declaration, whose line is where its walk starts
 * @param byLine what the scan read on each line, zero-based as the editor counts
 * @param unbound the names to place, which is the gate's answer and not this file's
 * @param last the last line the scan read anything on */
export function placesOf(
  declaration: Declaration,
  byLine: Map<number, Item[]>,
  unbound: Set<string>,
  last: number,
): [number, Item][] {
  const first = declaration.line - 1;
  switch (declaration.form) {
    case "tp-mt":
      return signaturePlaces(first, byLine.get(first) ?? [], unbound);
    case "tp-ab":
      // A composition block names a type on each of its lines and declares no name inside
      // itself, so every name on them is a reference.
      return blockPlaces(first, byLine, unbound, last, (idents) => idents);
    case "tp-cp":
      // A capsule block holds two shapes, and which one a line is decides what its first name
      // is: two names are a field and its type, one is a composition entry. That is the same
      // reading the roles are walked by ([semantic.ts](./semantic.ts)), so a name is not a field
      // here and a type there by two different rules.
      return blockPlaces(first, byLine, unbound, last, (idents) =>
        idents.length >= 2 ? idents.slice(1) : idents,
      );
    default:
      return [];
  }
}

/** The names a signature names, and where each stands: a parenthesised group alternates a
 *  parameter's name with its type, so a type is every other name in a group, and the owner
 *  slot's own name is the receiver — a name the signature declares rather than one it uses.
 *  The walk stops at the body, which the parse carried as text. */
function signaturePlaces(line: number, items: Item[], unbound: Set<string>): [number, Item][] {
  const found: [number, Item][] = [];
  let depth = 0;
  let groups = 0;
  let seen = 0;
  for (const item of items) {
    if (item.kind === "punct") {
      if (item.text === "{") {
        if (depth === 0) break;
        continue;
      }
      if (item.text === "(") {
        depth += 1;
        if (depth === 1) {
          groups += 1;
          seen = 0;
        }
        continue;
      }
      if (item.text === ")") depth -= 1;
      continue;
    }
    // `tp`, the method's own name and its subtype stand before the first group, and a name is
    // a reference only inside one.
    if (item.kind !== "ident" || groups === 0) continue;
    const isType = seen % 2 === 1;
    seen += 1;
    if (isType && unbound.has(item.text)) found.push([line, item]);
  }
  return found;
}

/** The names a field or composition block names, from the declaration's own line — where a
 *  block written on one line has its entries — down to the line that closes it. `isReference`
 *  says which of a line's names the block names rather than declares. */
function blockPlaces(
  first: number,
  byLine: Map<number, Item[]>,
  unbound: Set<string>,
  last: number,
  isReference: (idents: Item[]) => Item[],
): [number, Item][] {
  const found: [number, Item][] = [];
  let depth = 0;
  for (let line = first; line <= last && depth >= 0; line += 1) {
    const items = byLine.get(line) ?? [];
    depth += braceDepth(items);
    const idents = items.filter((item) => item.kind === "ident");
    // The declaration's own line carries `tp`, its name and its subtype before whatever the
    // block opens on it; the lines inside the block carry entries and nothing else.
    for (const item of isReference(line === first ? idents.slice(3) : idents)) {
      if (unbound.has(item.text)) found.push([line, item]);
    }
    if (depth === 0) break;
  }
  return found;
}
