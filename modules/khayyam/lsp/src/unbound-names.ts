import { readUnit } from "../../core/src/parse.ts";
import { declaredName, referencedTypes, type Declaration } from "../../core/src/sr.ts";
import { itemsOnLine } from "./document-items.ts";
import { lastLine, placesOf } from "./reference-places.ts";

// Whether a document names a type that nothing in it answers: one of the four ways the gate
// refuses a unit, and the only one nothing on the editor path ever asked. A file is published
// with what the reader could not read and what its claims could not be accounted for
// ([documents.ts](./documents.ts)), and a name in a signature that nothing declares was in
// neither: the sources held a file whose abstraction had been renamed by hand while three
// signatures still said the old name, and the gate refuses it while the editor said nothing.
//
// The question is the gate's question, asked in the gate's own words. `referencedTypes`
// (core/src/sr.ts) is what says which names a declaration names, and the visible set is every
// name the unit declares plus every name it brings in by an `in` — which is what
// `analyzeImports` (core/src/frontend.ts) builds before it walks them. A walk of this folder's
// own over signatures would be a second definition of "a type reference", and two definitions
// are two languages: a file the gate accepts and this server marks is a disagreement no reader
// can act on, and the gate is the one nobody runs. Where each of those names *stands* is the
// scan's question and not this file's ([reference-places.ts](./reference-places.ts)).
//
// Three things are deliberately not asked. A qualified reference — one containing `.`, of the
// form `pkg.Type` — is skipped, because the gate skips it and
// [rules/unbound-type-name](../rules/unbound-type-name/unbound-type-name.md) states that as
// part of the rule; what such a reference means is undecided, so checking one would be
// checking an answer this toolchain does not have. A role is not asked after either: the roles
// are a display concern, and a position that carries no role would then be a position no fault
// could be published on. And a `vr` writes a type of its own that nothing here asks about,
// because `referencedTypes` says a variable names nothing — a check that reached past it would
// mark a file the gate accepts.
//
// The visible set is built from the declarations alone and consults no file behind an `in`. A
// name the document says arrived by an address is bound by the document's own word, on this
// machine and on every other, which is the decision the roles and the definitions were made
// under ([lsp.handoff.md](../lsp.handoff.md)); the gate builds the same set from the
// declarations alone, so the two agree about the name and differ only about whether the
// address behind it is accounted for — which is published beside this, under another label,
// and neither answer stands for the other.
//
// A document the reader could not read in full is still asked about the declarations it did
// read, for the reason the claims beside it are ([inclusions.ts](./inclusions.ts)): the
// recovery is per declaration, so one unreadable declaration costs the file that declaration
// and nothing else. What such a declaration was going to declare is a fault of reading, and
// that fault is published on its own line — though what the reader makes of the tokens left
// beside a fault is its own reading, and a finding here is a statement about that reading.

/** One place a document names a type nothing in it answers. It is not a `Fault` and does not
 *  pretend to be one: nothing went unread and reading did not stop — this document says a type
 *  and the names it holds do not supply one. */
export interface UnboundName {
  /** The name, which is what the finding stands on rather than the whole line: the line is a
   *  signature or a field, and the name is the part of it nothing answers. */
  name: string;
  /** One-based, as a refusal message counts. */
  line: number;
  /** Zero-based, as the editor counts. */
  character: number;
  length: number;
}

/** Every place a document names a type that nothing it declares or includes answers, in the
 *  order the declarations stand on the lines they stand on.
 *
 *  One finding per place rather than one per name. The gate names the first unbound reference
 *  it meets and refuses the whole unit, which is the right answer to a question about a unit
 *  and the wrong one to a question about a document: a name written on two lines is two lines
 *  a reader has to be sent to.
 * @param source the document's own text */
export function unboundNameFindings(source: string): UnboundName[] {
  const unit = readUnit("document.kh", source).unit;
  const byLine = itemsOnLine(source);
  const visible = new Set(unit.declarations.map(declaredName));
  const last = lastLine(byLine);
  const findings: UnboundName[] = [];
  for (const declaration of unit.declarations) {
    const unbound = unboundIn(declaration, visible);
    if (unbound.size === 0) continue;
    for (const [line, item] of placesOf(declaration, byLine, unbound, last)) {
      findings.push({
        name: item.text,
        line: line + 1,
        character: item.startChar,
        length: item.text.length,
      });
    }
  }
  return findings;
}

/** Which of the names a declaration names nothing in the document answers. Empty for every
 *  form but three, because `referencedTypes` is empty for every form but three. */
function unboundIn(declaration: Declaration, visible: Set<string>): Set<string> {
  const unbound = new Set<string>();
  for (const reference of referencedTypes(declaration)) {
    if (reference.includes(".")) continue;
    if (!visible.has(reference)) unbound.add(reference);
  }
  return unbound;
}
