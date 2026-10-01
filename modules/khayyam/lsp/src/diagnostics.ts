// What each refusal means to whoever is reading the line it stands on, and what the fault
// cost. The labels are this toolchain's own (the diagnostics contract is deferred), so the
// sentences are too.
//
// A fault is a refusal: the frontend will not hand this file to a target, so a reader is
// entitled to it as an error rather than a hint — and a reader told only that a construct
// was refused is no better off than one who is told nothing, which is why every sentence
// names what the language does have in place of the thing that was refused. The editor
// shows it on the line, which is the whole point: a file the frontend could not read in
// full used to reach the reader as a file with no diagnostic and a handful of confidently
// wrong roles, and the cost of that silence was three rounds of a working feature looking
// broken.
import type { Fault, RefusalReason } from "../../core/src/sr.ts";
import type { Finding } from "./inclusions.ts";

const SAYS: Record<RefusalReason, string> = {
  "unexpected-character":
    "a character the grammar has no form for; the dot of invocation is the only operator it has",
  "unterminated-string": "a quoted form that the line's break reached before its closing quote",
  "unterminated-block-comment": "a block comment with no closing marker",
  "declaration-form": "a form no declaration takes here",
  "missing-subtype": "a type with no subtype, and every `tp` states one",
  "keyword-as-identifier": "a reserved word used as a name",
  semicolon: "a semicolon, which separates nothing here: a declaration ends with its line",
  "scope-placement": "a `sc` outside a method body, which is this toolchain's own rule",
  "unbalanced-block": "a block with no closing brace",
  "unresolved-import": "a path with no file behind it",
  "name-not-declared": "a name the file behind the path does not declare",
  "kind-mismatch": "a name behind the path declared as the other kind",
  "unbound-type-name": "a type reference no declared or included name answers",
};

/** What the fault cost, which is where reading went on. */
const COST: Record<Fault["extent"], string> = {
  line: "The rest of that line was not read",
  declaration: "That declaration was not read; the lines around it still were",
  file: "Nothing after it could be read",
};

/** What a fault that is a consequence of another says about the other, in the two
 *  shapes it takes.
 *
 *  A fault that follows an earlier one is the earlier one's leftover, so standing on
 *  its own it tells a reader nothing they can act on: `a form no declaration takes
 *  here` at a closing brace is true of every stray brace, and says nothing of the one
 *  that is only there because a character ten lines up cost the file the brace it was
 *  holding. So the sentence names the fault it follows from and its line, and repeats
 *  what that fault cost — which is the brace going with it, in words a reader can act
 *  on. The fault is not dropped and its reason is not rewritten: the file's structure
 *  is broken, and hiding that would cost more than the wording costs. */
function consequenceOf(fault: Fault): string {
  const cause = fault.because;
  if (cause === undefined) {
    return fault.text === "}"
      ? " It is a closing brace and no block is open, so it closes nothing."
      : "";
  }
  const cost = COST[cause.extent];
  const spoken = cost.charAt(0).toLowerCase() + cost.slice(1);
  return (
    ` It follows from the ${cause.reason} at line ${cause.line}: ${spoken},` +
    " and a brace went with it, so this closing brace has nothing left to close."
  );
}

/** One diagnostic per fault of reading: where it stands, what it is, what follows from
 *  what, and what it cost. */
export function diagnosticOf(fault: Fault): object {
  return {
    range: {
      start: { line: fault.line - 1, character: fault.column - 1 },
      end: { line: fault.line - 1, character: fault.column - 1 + fault.length },
    },
    severity: 1,
    code: fault.reason,
    source: "khayyam",
    message: `${fault.reason} at line ${fault.line}, column ${fault.column} — ${
      fault.text.trim() === "" ? "the line ends there" : `${JSON.stringify(fault.text)}: `
    }${SAYS[fault.reason]}.${consequenceOf(fault)} ${COST[fault.extent]}.`,
  };
}

/** One diagnostic per claim of the document that this toolchain could not account for,
 *  which is not the same kind of thing as a fault of reading: nothing was unread, the file
 *  said something and the files behind it do not confirm it. It is published under the same
 *  label the gate would refuse a unit under, because it is the same fact about the same
 *  thing, and the sentence is the one the claim carries with it rather than the one every
 *  fault of a label shares — two unresolved URIs differ by their base and by their path,
 *  and a reader told only that a path addresses nothing cannot act on either.
 *  @see [inclusions.ts](./inclusions.ts) for what a claim is and what is deliberately not
 *  asked of one. */
export function inclusionDiagnostic(finding: Finding): object {
  return {
    range: {
      start: { line: finding.line - 1, character: finding.character },
      end: { line: finding.line - 1, character: finding.character + finding.length },
    },
    severity: 1,
    code: finding.reason,
    source: "khayyam",
    message:
      `${finding.reason} at line ${finding.line} — ${finding.message}. ` +
      "Nothing else in this file is affected: every role and every definition is still " +
      "answered from what the file declared, because a role says what the file says and " +
      "not what the files behind its URIs confirm.",
  };
}

/** A refusal of the client itself, on the document it was about, in the editor's own
 *  diagnostic collection. A payload this server cannot read is the same kind of fault as
 *  a character it cannot read, and it stands on the document that carries it: a line in a
 *  log nobody opens is how a dead server read as a success. The document keeps the text
 *  of the last change that could be read, and the next change of the declared shape takes
 *  this refusal off the file with it. */
export function refusalDiagnostic(why: string): object {
  return {
    range: { start: { line: 0, character: 0 }, end: { line: 0, character: 0 } },
    severity: 1,
    code: "text-document-sync",
    source: "khayyam",
    message:
      `the client sent a change this server cannot read: ${why}` +
      " The text this server holds is the one from the last change it could read, so every" +
      " fault and every role on it is about that text and not about the file on screen.",
  };
}
