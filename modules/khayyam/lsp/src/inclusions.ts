// What a document claims about the files it includes, checked against the files that are
// there.
//
// This is not a second reading of a document and not the gate's job done again. It is one
// question the reader does not ask and the gate asks only of a whole unit: a document says
// `tp Bool in "..."`, and whether anything is behind that URI is a fact about the file the
// document is, which nothing in a server that only reads would ever say. A claim this
// toolchain cannot account for is a fault where the claim stands, and it is not the same
// kind of thing as a fault of reading: nothing was unread, the file said something that
// could not be confirmed. The two are published together and neither stands for the other.
//
// What is deliberately not here: a role that changes when a URI resolves. A role says what
// the file says a name is, and a file says the same thing on every machine it is opened on;
// a role that followed the filesystem would make one file read differently in two
// directories with nothing on the screen saying why. The fault says the claim is
// unaccounted for, and the role says what was claimed.

import { readUnit } from "../../core/src/parse.ts";
import { declarationKind, type Declaration, type RefusalReason } from "../../core/src/sr.ts";
import { itemsOnLine, placeOf } from "./document-items.ts";
import { included } from "./binding-table.ts";
import type { Reach, Resolved } from "./definition.ts";

/** One claim of a document that this toolchain could not account for, and where the claim
 *  stands. It is not a `Fault` and does not pretend to be one: a fault says reading
 *  stopped, and reading did not stop here. */
export interface Finding {
  /** The toolchain's own label for the way the claim came out, one per thing that can go
   *  wrong with an inclusion. No label is invented here — these are the three the gate has
   *  refused a unit on, and each has a rule of its own. */
  reason: RefusalReason;
  /** The name the claim is about, which is what the fault stands on rather than the whole
   *  line: the name is the claim, and the path beside it is the claim about where it
   *  comes from. */
  name: string;
  /** One-based, as a refusal message counts. */
  line: number;
  /** Zero-based, as the editor counts. */
  character: number;
  length: number;
  /** What a reader has to be told to act on it, which is the one sentence in this
   *  file's answers that is not the same for every fault of the same label: two
   *  unresolved URIs differ by their base and by their path. */
  message: string;
}

/** What a claim could not be accounted for, told in a sentence a reader can act on. The
 *  reason resolution gives is in it verbatim, because an address nothing declares how to
 *  resolve and a file that is not there are two different faults with two different
 *  repairs, and a reader told only that an address addresses nothing is told neither.
 *  @param label how the claim came out
 *  @param resolution what resolving the address answered
 *  @param name the name the claim is about
 *  @param wanted the kind this document said the name is, as the language spells it */
function said(
  label: RefusalReason,
  resolution: Resolved,
  name: string,
  path: string,
  wanted: "tp" | "vr",
): string {
  if (resolution.found === undefined) {
    // The address is in the sentence whether or not it resolved: a reader told that a
    // claim cannot be accounted for and not which claim, has a line to look at and
    // nothing to read on it.
    return (
      `"${name}" arrives through "${path}", and ${resolution.because ?? "nothing says what that address resolves to"}`
    );
  }
  const where = resolution.found.uri;
  switch (label) {
    case "name-not-declared":
      return `"${name}" arrives through "${path}" as ${where}, and the file there declares no name by that one`;
    case "kind-mismatch":
      return (
        `"${name}" arrives through "${path}" as a ${wanted === "tp" ? "type" : "variable"} and ` +
        `${where} declares that name as the other kind`
      );
    default:
      return `"${name}" arrives through "${path}", and ${resolution.because ?? "nothing says what it resolves to"}`;
  }
}

/** What is wrong with this claim, or undefined when the file behind its address accounts
 *  for it: the address resolves to nothing, the file there declares no such name, or it
 *  declares that name as the other kind. The order is the gate's - an address that
 *  resolves to nothing is not asked the other two questions, because a file that is not
 *  there declares nothing by any name. */
function why(
  declaration: Declaration & { path: string },
  from: string,
  reach: Reach,
): { reason: RefusalReason; resolved: Resolved } | undefined {
  const resolved = reach.resolve(declaration.path, from);
  if (resolved.found === undefined) return { reason: "unresolved-import", resolved };
  const behind = readUnit(declaration.path, resolved.found.text).unit.declarations.find(
    (entry) => entry.name === declaration.name,
  );
  if (behind === undefined) return { reason: "name-not-declared", resolved };
  const wanted = declaration.form === "tp-in" ? "tp" : "vr";
  return declarationKind(behind) === wanted ? undefined : { reason: "kind-mismatch", resolved };
}

/** Every claim of this document about another file that the files behind those addresses
 *  do not account for, in the order the claims stand on the lines they stand on.
 *
 *  A document the reader could not read in full is still checked for the declarations it
 *  did read: the recovery is per declaration, so one unreadable line costs the file that
 *  line and every claim on the others is still a claim.
 *  @param uri the document's own URI, which is where a root is found from
 *  @param source the document's own text
 *  @param reach how the addresses its claims write are resolved */
export function inclusionFindings(uri: string, source: string, reach: Reach): Finding[] {
  const unit = readUnit("document.kh", source).unit;
  const byLine = itemsOnLine(source);
  const findings: Finding[] = [];
  for (const declaration of unit.declarations) {
    if (!included(declaration)) continue;
    const found = why(declaration, uri, reach);
    if (found === undefined) continue;
    const item = (byLine.get(declaration.line - 1) ?? [])[1];
    const place = item === undefined ? undefined : placeOf(declaration.line - 1, item);
    findings.push({
      reason: found.reason,
      name: declaration.name,
      line: declaration.line,
      character: place?.startChar ?? 0,
      length: declaration.name.length,
      message: said(
        found.reason,
        found.resolved,
        declaration.name,
        declaration.path,
        declaration.form === "tp-in" ? "tp" : "vr",
      ),
    });
  }
  return findings;
}
