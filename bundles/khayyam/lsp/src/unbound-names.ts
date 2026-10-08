import { readUnit } from "../../core/src/parse.ts";
import { referencePlaces } from "../../core/src/references.ts";
import { declaredName, referencedTypes, type Declaration } from "../../core/src/sr.ts";

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
// can act on, and the gate is the one nobody runs. Where each of those names *stands* is asked
// of the compiler's own walk ([core/src/references.ts](../../core/src/references.ts)), which is
// one answer shared with the rename service, and this file is its reader rather than a second
// walk: a place placed twice is a place the two copies may part company on.
//
// Three things are deliberately not asked. A qualified reference — one containing `.`, of the
// form `pkg.Type` — is skipped, because the gate skips it and
// [rules/unbound-type-name](../rules/unbound-type-name/unbound-type-name.md) states that as
// part of the rule; what such a reference means is undecided, so checking one would be
// checking an answer this toolchain does not have. A role is not asked after either: the roles
// are a display concern, and a position that carries no role would then be a position no fault
// could be published on. And a `vr` writes a type of its own that nothing here asks about,
// because `referencedTypes` says a variable names nothing — a check that reached past it would
// mark a file the gate accepts. The walk that places names answers a wider question than this
// caller has: a rename has to place the name an `in` routes and the type a `vr` writes, which
// is why it covers them, and a wider answer is not a licence to publish a wider finding. The
// forms it covers and this one does not are therefore refused below by name.
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
  const visible = new Set(unit.declarations.map(declaredName));
  const findings: UnboundName[] = [];
  for (const declaration of unit.declarations) {
    if (!namesTypes(declaration.form)) continue;
    const unbound = unboundIn(declaration, visible);
    // Nothing the gate names and nothing answers, so there is no name to place and the walk is
    // not asked — it walks the whole document for one declaration, and a file whose every name
    // binds is not a file worth walking.
    if (unbound.size === 0) continue;
    // The walk covers the forms refused above as well as these, so each place is asked whether
    // it is one of the names this declaration leaves unbound. An exact match, and the place's
    // own text: a qualified reference arrives whole and the gate holds no qualified name, so a
    // dotted place cannot match and is not reported.
    for (const place of referencePlaces(source, declaration)) {
      if (!unbound.has(place.text)) continue;
      findings.push({
        name: place.text,
        line: place.line,
        character: place.column - 1,
        length: place.length,
      });
    }
  }
  return findings;
}

/** Whether this file is asked about the types a declaration names: the three forms the gate
 *  answers for, and no other. The placement walk covers more, and the form is asked of it here
 *  rather than left to the emptiness of the set below — a wider answer is not a licence to
 *  publish a wider finding. */
function namesTypes(form: Declaration["form"]): boolean {
  return form === "tp-mt" || form === "tp-ab" || form === "tp-cp";
}

/** Which of the names a declaration names nothing in the document answers. Empty for every
 *  form but three, because `referencedTypes` is empty for every form but three. A qualified
 *  reference is never in it: the gate skips such a reference, and this set is the gate's. */
function unboundIn(declaration: Declaration, visible: Set<string>): Set<string> {
  const unbound = new Set<string>();
  for (const reference of referencedTypes(declaration)) {
    if (reference.includes(".")) continue;
    if (!visible.has(reference)) unbound.add(reference);
  }
  return unbound;
}
