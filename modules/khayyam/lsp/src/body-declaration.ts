// What a declaration standing inside a block declares, and where its name stands.
//
// A body holds two identities and only one of them is a variable: a `vr` written in a
// body is a `method-local` and a `tp {name} sc` written in one is a `scope`
// (display.json -> `method-local`), and the display contract splits those two positions
// into two identities because a declaration's scope of validity is part of what a name
// IS. Both forms therefore go through here, so the two are stated once and a use is
// answered by whichever of them the declaration beside it was.
//
// Either way the name is bound in the block that holds the declaration statement, so a
// use above or below the declaration, beside it or inside the block it opens, is that
// name and not one the file does not know. The block is the whole of the binding, and
// which block that is differs between the two forms: a `vr` written inside a scope is
// that scope's, and a `tp {name} sc` written in a method body is the method body's —
// which is what lets a driver name the scope it is about, the `CF.ELSE(elseProcess)` a
// line above the `tp elseProcess sc` that declares it.
import { placeOf, type Item } from "./document-items.ts";
import type { Block, Declared, OpenBlocks } from "./blocks.ts";
import type { Emitter } from "./role-emitter.ts";

/** The line a body declaration stands on, as the walk states it. */
export interface BodyLine {
  items: Item[];
  /** The keyword that opens the declaration, `vr` or `tp`. */
  first: Item;
  /** The block the line stands in, which is where the name is bound. */
  enclosing: Block | undefined;
  /** The file's brace depth before the line and after it, which together say whether the
   *  line leaves a block open behind it — the block a Scope declares. */
  depth: { before: number; after: number };
  blocks: OpenBlocks;
  emitter: Emitter;
  line: number;
}

/** Reads a line that declares something inside a block, and answers the names standing on
 *  it. A line that declares nothing here is answered by whoever holds the line, which is
 *  the walk. */
export function declaredInBody(line: BodyLine): void {
  const { items, first, enclosing, depth, blocks, emitter } = line;
  const name = items[1];
  if (name?.kind !== "ident") return;
  if (first.text === "vr") {
    // A `vr` in a body is not the file-level `variable`, and it is the one role no
    // TextMate scope can carry: a `vr` in a body and a `vr` at file level are the same
    // line of text and the line that opens the body is not on it. See the role's
    // `serverOnlyBecause`.
    const declared = here("method-local", `the variable ${name.text} declared in this body`, line.line, name);
    enclosing?.locals.set(name.text, declared);
    emitter.at(first, "keyword", "reserved word");
    emitter.at(name, declared.role, declared.origin, declared.place);
    if (items[2]?.kind === "ident") emitter.resolve(items[2], "type-reference");
    return;
  }
  const subtype = items[2];
  if (subtype?.kind !== "ident" || subtype.text !== "sc") return;
  const declared = here("scope", `the Scope ${name.text} declared here`, line.line, name);
  enclosing?.locals.set(name.text, declared);
  emitter.at(first, "keyword", "reserved word");
  emitter.at(name, declared.role, declared.origin, declared.place);
  emitter.at(subtype, "subtype", "the sc subtype");
  if (depth.after > depth.before) blocks.opened("sc", depth.after);
}

/** What a body declaration declares: the identity its name carries, the sentence saying
 *  so, and where the name stands. */
function here(role: string, origin: string, line: number, name: Item): Declared {
  return { role, origin, place: placeOf(line, name) };
}
