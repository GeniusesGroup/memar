// What a line that declares nothing says about the names standing on it: a statement
// inside a method body, or a line outside any declaration.
//
// The two are one walk, because a bare use is a bare use either way. What a body adds is
// the knowledge that body has — a parameter of the method above it, a variable this body
// declared, and the dot invocation, where the name before the opening parenthesis is a
// Method called here — and that knowledge is the scope this is given. The language
// states that a declaration occupies one line and the line's break terminates it
// (docs/khayyam/khayyam.md, Declaration separator), so a line that is not a declaration
// declares nothing: two words standing side by side are not the shape of a `vr`
// declaration, and reading them as one told a reader that a word this file never declared
// was a variable of its own.
import { isKeyword, SUBTYPE_KEYWORDS } from "../../core/src/scan.ts";
import type { Declared } from "./blocks.ts";
import type { Item, Place } from "./document-items.ts";
import type { Emitter } from "./role-emitter.ts";

const SUBTYPES = new Set<string>(SUBTYPE_KEYWORDS);

/** What a method body knows about the line standing in it. A line outside any
 *  declaration is given nothing, which is what makes it a bare use. */
export interface StatementScope {
  /** The parameters of the method the line stands in, each mapped to where its name
   *  stands, so a parameter keeps the parameter role wherever in the body it is used. */
  parameters: Map<string, Place | undefined>;
  /** What a block that is open as the file stands has declared, or undefined when this
   *  file declares no such name. The role travels with it, because a body holds a
   *  `method-local` and a `scope` and the two are different identities wearing the same
   *  kind of name. */
  declares(text: string): Declared | undefined;
  /** Whether this file declares a Method by this name. The dot operator is the
   *  language's only invocation form, so the name before the opening parenthesis is a
   *  Method; the declaration says which one, and a Method this file does not declare
   *  belongs to something else and is named by nothing here. */
  declaresMethod(text: string): boolean;
}

export function statementRoles(
  items: Item[],
  scope: StatementScope | undefined,
  emitter: Emitter,
): void {
  for (let at = 0; at < items.length; at += 1) {
    const item = items[at]!;
    if (item.kind === "punct") continue;
    if (item.kind === "string") {
      emitter.overQuotes(item, "string", "a quoted literal, which no inclusion states here");
      continue;
    }
    if (isKeyword(item.text)) {
      emitter.at(item, SUBTYPES.has(item.text) ? "subtype" : "keyword", "reserved word");
      continue;
    }
    // A parameter of the method above is that parameter wherever in its body it is
    // used: a scope's statements are written inside the method that holds it.
    if (scope !== undefined) {
      if (scope.parameters.has(item.text)) {
        emitter.at(item, "method-argument", "a parameter of the method above", scope.parameters.get(item.text));
        continue;
      }
      const declaredInBody = scope.declares(item.text);
      if (declaredInBody !== undefined) {
        emitter.at(item, declaredInBody.role, declaredInBody.origin, declaredInBody.place);
        continue;
      }
      const next = items[at + 1];
      if (next && next.kind === "punct" && next.text === "(") {
        // The dot operator is the language's only invocation form, so the name before the
        // opening parenthesis is a Method — the same role it carries at its declaration.
        // A role follows the binding, never the position: when this file declares a
        // Method by that name, the call is resolved against that declaration, and a
        // Method it does not declare is a method on something else and is named by
        // nothing here, so the call carries the role and no place.
        if (scope.declaresMethod(item.text)) {
          emitter.resolve(item, "method");
        } else {
          emitter.at(item, "method", "a Method called here");
        }
        continue;
      }
    }
    emitter.resolve(item, "identifier-reference");
  }
}
