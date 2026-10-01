// What the server holds about a document: the open documents and their text, and what it
// does about a document on the wire each time that text changes.
//
// Every answer this server gives about a document is computed from the text held here,
// which is why the table is one thing rather than a parameter threaded through the
// handlers: an answer computed from a text the client did not send is a fault that reads
// as a success. So a change that contradicts the declared capability is refused and the
// text stands, and every answer afterwards is about the text the server actually holds.
import { contradictsDeclaredChange, type Change } from "./capabilities.ts";
import { diagnosticOf, inclusionDiagnostic, refusalDiagnostic } from "./diagnostics.ts";
import type { Reach } from "./definition.ts";
import { inclusionFindings } from "./inclusions.ts";
import { analyse } from "./semantic.ts";
import { notify } from "./transport.ts";

const documents = new Map<string, string>();

/** Whether this server holds a document at a URI. A document it was never told about is a
 *  document that did not reach it, which is a different fault from one it holds and
 *  cannot analyse — so the answers say which rather than answering as though it were
 *  whole. */
export function holds(uri: string): boolean {
  return documents.has(uri);
}

/** The text of a document this server holds, and the text every answer about it is
 *  computed from. */
export function text(uri: string): string | undefined {
  return documents.get(uri);
}

/** What the frontend could not read of the document this server holds, and what the files
 *  behind its inclusions do not account for. One publication carries both, and neither
 *  stands for the other: the first is a fault of reading and the second is a claim this
 *  toolchain could not confirm, so a document with one and not the other must not read as
 *  though it had the other.
 *
 *  The two together are the whole of what a reader is told about a file. A reader shown a
 *  confident set of roles over a file whose inclusions name nothing was, until the second
 *  existed, shown a file the toolchain had no trouble with — and a go-to-definition on one
 *  of its names found nothing, which reads as a file with no declarations in it.
 *  @param uri the document
 *  @param reach how the addresses this document writes are resolved */
export function diagnosticsFor(uri: string, reach: Reach): object[] | undefined {
  const held = documents.get(uri);
  if (held === undefined) return undefined;
  return [
    ...analyse(held).faults.map(diagnosticOf),
    ...inclusionFindings(uri, held, reach).map(inclusionDiagnostic),
  ];
}

export function open(uri: string, source: string, reach: Reach): string[] {
  documents.set(uri, source);
  return publish(uri, reach);
}

/** A change of a document: the declared shape applies it and re-reads the whole text, and
 *  anything else is refused where the reader is and leaves the document as it was. */
export function change(uri: string, changes: Change[], reach: Reach): string[] {
  const contradiction = contradictsDeclaredChange(changes);
  if (contradiction !== null) {
    // Refused, not applied: reading the payload anyway is what made this defect
    // invisible, because the answer afterwards was a fault and a set of roles about a
    // document no editor had.
    return [notify("textDocument/publishDiagnostics", {
      uri,
      version: null,
      diagnostics: [refusalDiagnostic(contradiction)],
    })];
  }
  documents.set(uri, changes[0]!.text);
  return publish(uri, reach);
}

/** The document is gone, so its markers go with it: an empty publication is the only way
 *  a client is told to drop them. */
export function close(uri: string): string {
  documents.delete(uri);
  return notify("textDocument/publishDiagnostics", { uri, diagnostics: [] });
}

/** Publishes what the frontend could not read of a document, and clears the markers of a
 *  document that is now whole: an empty publication is how a client is told a fault is
 *  gone, so it is sent whenever there is nothing to mark. */
function publish(uri: string, reach: Reach): string[] {
  const diagnostics = diagnosticsFor(uri, reach);
  if (diagnostics === undefined) return [];
  return [notify("textDocument/publishDiagnostics", { uri, version: null, diagnostics })];
}
