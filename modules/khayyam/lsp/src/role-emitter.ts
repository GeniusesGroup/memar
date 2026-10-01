// What one occurrence's role becomes: the token a line's walk answers with, and the
// answer for a name, which is the one thing every line shape asks the same way.
//
// A token carries more than a role because a role alone cannot be read: it carries the
// sentence saying what the name IS, where it was declared, and the URI an included name
// arrived through. The first is what makes the answer checkable by a reader of the
// stream, and the last two are what a definition asked at this occurrence is answered
// from ([definition.ts](./definition.ts)) — so both absences are stated here, and they
// are different: nothing here declares the name, or it is declared in another file.
import { type Item, type Place } from "./document-items.ts";
import { DECLARED, included, type Bindings } from "./binding-table.ts";

export interface SemanticToken {
  line: number; // zero-based, as LSP counts
  startChar: number;
  length: number;
  role: string;
  text: string;
  /** What the occurrence was resolved to, so the output can be read and checked. */
  resolvedTo: string;
  /** Where the name this occurrence resolves to is declared, in the document that was
   *  read. Absent when nothing here declares it — a reserved word, a type the file does
   *  not declare, a method called on something — and absent for a name that arrived by
   *  an inclusion, whose declaration stands in another file: those two absences are
   *  different, which is why they are not one absent value. A definition asked at this
   *  occurrence is this place ([definition.ts](./definition.ts)). */
  declaredAt?: Place;
  /** The URI a name that arrived by `in` came through. Its declaration is not in the
   *  document that was read, so this is where the question of its definition goes on
   *  to; absent for every other occurrence. */
  includedThrough?: string;
}

/** How the roles of one line are said, and how a name the line stands on is answered.
 *  Every line shape asks these the same way, which is what lets a signature, a body
 *  statement and a bare use be walked by different files. */
export interface Emitter {
  /** The role for an item standing on this line, said directly — for a name named by
   *  what stands there rather than by a binding: a reserved word, a subtype, a field's
   *  name, a call site. */
  at(item: Item, role: string, resolvedTo: string, declaredAt?: Place, includedThrough?: string): void;
  /** The same, for a quoted form, whose extent covers the quotes because the quotes are
   *  part of what a token must cover. Which role it carries is the declaration's to say:
   *  the path of an `in` inclusion is the path an inclusion routes to, and any other
   *  quoted form is not one — the contract gives that second form the `string` role and
   *  names it a reserved one, so a literal is not displayed as a path. */
  overQuotes(item: Item, role: string, resolvedTo: string): void;
  /** What a name is answered: the role its binding carries, or the fallback the caller
   *  asks for when nothing in the document binds it. */
  resolve(item: Item, fallback: string): void;
}

export function emitterInto(tokens: SemanticToken[], line: number, bindings: Bindings): Emitter {
  return {
    at: (item, role, resolvedTo, declaredAt, includedThrough) => {
      tokens.push({
        line,
        startChar: item.startChar,
        length: item.text.length,
        role,
        text: item.text,
        resolvedTo,
        declaredAt,
        includedThrough,
      });
    },
    overQuotes: (item, role, resolvedTo) => {
      tokens.push({
        line,
        startChar: item.startChar - 1,
        length: item.text.length + 2,
        role,
        text: `"${item.text}"`,
        resolvedTo,
      });
    },
    resolve: (item, fallback) => {
      const binding = bindings.bindingOf(item.text);
      if (!binding) {
        // Nothing here declares the name, so it is answered by the fallback role and by
        // no place at all: there is nowhere a reader could be sent.
        tokens.push({
          line,
          startChar: item.startChar,
          length: item.text.length,
          role: fallback,
          text: item.text,
          resolvedTo: "not bound in this file",
          declaredAt: undefined,
          includedThrough: undefined,
        });
        return;
      }
      const declared = DECLARED[binding.form];
      tokens.push({
        line,
        startChar: item.startChar,
        length: item.text.length,
        role: declared.role,
        text: item.text,
        resolvedTo: `${item.text} is ${declared.origin}`,
        declaredAt: bindings.placeOf(item.text),
        // A name that arrived by an inclusion is bound here and declared elsewhere,
        // which is a different absence and is why the URI it came through travels with
        // it.
        includedThrough: included(binding) ? binding.path : undefined,
      });
    },
  };
}
