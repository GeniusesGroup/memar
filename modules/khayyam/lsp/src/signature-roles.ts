// What the three parenthesised groups of a method signature say about the names
// standing in them, and where each parameter's slot is.
//
// A signature is the one line of the language where a name is declared rather than
// used, and its groups say three different things: the owner slot names the receiver and
// the type it belongs to, and the two groups after it alternate a parameter's name with
// its type. Walking it on its own is what keeps those three apart from the bare uses a
// body statement is made of — and it returns the slots, because a use of a parameter in
// a body reaches the slot and not the signature line as a whole.
import { placeOf, type Item, type Place } from "./document-items.ts";
import type { Emitter } from "./role-emitter.ts";
import type { MethodDecl } from "../../core/src/sr.ts";

export function signatureRoles(
  declaration: MethodDecl,
  items: Item[],
  line: number,
  emitter: Emitter,
): Map<string, Place | undefined> {
  // A parameter is known by the parse, and this walk finds where its name stands, so a
  // name the parse read and the walk missed is still a parameter — and carries no place,
  // because none was found to carry.
  const parameters = new Map<string, Place | undefined>();
  for (const param of [...declaration.influencing, ...declaration.influenced]) {
    parameters.set(param.name, undefined);
  }
  let depth = 0;
  let group = 0;
  for (let at = 3; at < items.length; at += 1) {
    const item = items[at]!;
    if (item.kind === "punct" && item.text === "(") {
      depth += 1;
      if (depth === 1) group += 1;
      continue;
    }
    if (item.kind === "punct" && item.text === ")") {
      depth -= 1;
      continue;
    }
    if (item.kind !== "ident") continue;
    const next = items[at + 1];
    const isOwnerType = group === 1 && (next === undefined || next.text === ")");
    const isType = next !== undefined && next.kind === "ident";
    if (isOwnerType) {
      // A type named in a signature is still that type. The position role is what a
      // renderer says when the file does not state the type's origin, so it is the
      // answer only for a name this file does not bind; an included type stays an
      // included type here, and a type declared here keeps the role its own declaration
      // gave it, so the same identity carries one role at every position in the file.
      emitter.resolve(item, "method-owner-type");
    } else if (group === 1) {
      // The owner slot's own name is the receiver. The contract has no role for it, so
      // the grammar keeps it and the server says nothing.
      continue;
    } else if (isType) {
      // The parameter's name is the slot it is declared in, so a use of it in the body
      // reaches here.
      const declared = placeOf(line, item);
      parameters.set(item.text, declared);
      emitter.at(item, "method-argument", `a parameter of ${declaration.name}`, declared);
    } else if (group >= 2) {
      emitter.resolve(item, "method-argument-type");
    }
  }
  return parameters;
}
