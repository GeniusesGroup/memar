// Answers where a name is declared, which is the other half of what the roles answer:
// a role says what a name IS, and a definition says where that name came from. One
// binding answers both, so the two are asked for separately and neither is derived
// from the other's answer — a definition is a place in a document, and a place is not
// a class.
//
// The answer is the reader's ([semantic.ts](./semantic.ts)), not a second reading of
// the source: every occurrence there already carries where its name was declared, and
// what is added here is the one hop that leaves the document — the file an `in`
// inclusion's URI addresses, read through the same recovering reader rather than
// through the gate, because a definition asked about one name must not be withheld
// because some other line of the file behind it could not be read.
import { readUnit } from "../../core/src/parse.ts";
import { analyse } from "./semantic.ts";
import type { Place } from "./document-items.ts";

/** A place in a document the editor counts: zero-based, as LSP counts. */
export interface Position {
  line: number;
  character: number;
}

/** Where a name is declared. Three parts, and no fourth: the document the declaration
 *  stands in — the one that was read, or the file an inclusion's URI addresses —, the
 *  line, and the extent of the declared name rather than of the whole declaration, so
 *  a reader who asks about `err` is put on `err` with the rest of the signature still
 *  there around it. */
export interface Definition {
  uri: string;
  line: number;
  startChar: number;
  length: number;
  /** The name as it was declared, which is the name that was asked about: one binding
   *  is one name at every position it stands in. */
  name: string;
}

/** How far a definition may reach beyond the document the question was asked about. A
 *  name that arrived by `in` is declared in another file, and the URI it arrived
 *  through is written from the repository root (rules/import-address), so reaching it
 *  needs that base: a caller with none answers no definition rather than sending a
 *  reader to a place it guessed. */
/** What resolving an address answered: the document it names, or the reason there is no
 *  such document, and the root it was resolved from either way. The two are one answer
 *  because a reader told only "nothing there" cannot act on it: a file missing from a
 *  repository, a repository whose root this toolchain could not find, and a repository
 *  whose manifest declares nothing about how an address resolves are three faults and one
 *  "not found". */
export interface Resolved {
  /** The base the address was resolved from, when one was found. */
  base?: { directory: string; markedBy: string };
  /** The document the address names, or undefined when it does not. */
  found?: { uri: string; text: string };
  /** Which mechanism answered, so a reader is never left guessing whether an answer came
   *  from a project's stated root or from a module manifest it had not understood. Absent
   *  only when nothing answered. */
  via?: string;
  /** Why there is no document, in a sentence a reader can act on. Absent when there is
   *  one. */
  because?: string;
}

/** How far a definition may reach beyond the document the question was asked about. An
 *  address a document writes is resolved by what the root's manifest declares, from the
 *  document's own place, so a caller with no root answers no definition rather than
 *  sending a reader to a place it guessed. */
export interface Reach {
  /** The document an address names, or the reason there is none, which is what a reader
   *  of a claim needs and what an answer of nothing is not. */
  resolve(path: string, from: string): Resolved;
  /** The text this server holds of a document: a place on the wire is read against the
   *  text the editor holds, so a document the editor has open comes before the file
   *  system. */
  held(uri: string): string | undefined;
}

/** Where a name is declared, read across as many addresses as it takes to reach a
 *  declaration that is one. An address is not a declaration - the name it names is
 *  declared elsewhere - so a file that only includes a name has nothing to be sent to and
 *  the question goes on. A cycle has no declaration anywhere in it, so there is no place
 *  to be sent to; what has to be guaranteed is that the question stops. */
function acrossInclusions(
  path: string,
  from: string,
  name: string,
  reach: Reach,
  seen: Set<string>,
): Definition | null {
  const found = reach.resolve(path, from).found;
  if (found === undefined) return null;
  if (seen.has(found.uri)) return null;
  seen.add(found.uri);
  const declaration = readUnit(path, found.text).unit.declarations.find((entry) => entry.name === name);
  if (declaration === undefined) return null;
  if (declaration.form === "tp-in" || declaration.form === "vr-in") {
    return acrossInclusions(declaration.path, found.uri, name, reach, seen);
  }
  // The declaration is in this file, so its place is found by reading this file - the
  // same reading, with the same recovery, that named it. The occurrence carrying the
  // place is the declaration's own name: a use of the same text on the same line would
  // carry the place of wherever it was declared, which is not this line.
  const declared = analyse(found.text).roles.find(
    (token) =>
      token.line === declaration.line - 1 &&
      token.text === name &&
      token.declaredAt?.line === token.line &&
      token.declaredAt?.startChar === token.startChar,
  );
  if (declared?.declaredAt === undefined) return null;
  return {
    uri: found.uri,
    line: declared.declaredAt.line,
    startChar: declared.declaredAt.startChar,
    length: declared.declaredAt.length,
    name,
  };
}

/** Where the name standing at `position` is declared, or nothing when this document
 *  declares no such name. Nothing is the answer for a reserved word, a quoted literal,
 *  punctuation, a name no binding here answers - a type the file does not declare, a
 *  method called on something - and a name that arrived through an address nothing
 *  resolves. A reader is better served by nothing than by a place that is wrong, which is
 *  the same refusal the diagnostics make and for the same reason. */
export function definitionAt(
  uri: string,
  source: string,
  position: Position,
  reach: Reach,
): Definition | null {
  const occurrence = analyse(source).roles.find(
    (token) =>
      token.line === position.line &&
      token.startChar <= position.character &&
      position.character < token.startChar + token.length,
  );
  if (occurrence === undefined) return null;
  if (occurrence.includedThrough !== undefined) {
    return acrossInclusions(occurrence.includedThrough, uri, occurrence.text, reach, new Set([uri]));
  }
  if (occurrence.declaredAt === undefined) return null;
  return { uri, ...place(occurrence.declaredAt), name: occurrence.text };
}
function place(at: Place): Pick<Definition, "line" | "startChar" | "length"> {
  return { line: at.line, startChar: at.startChar, length: at.length };
}
