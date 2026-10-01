// What this server says it can do at `initialize`, and what a payload that contradicts
// that statement is.
//
// The two are one subject because a capability is not a claim about this server alone:
// it is a statement about what the client will send, so a server that accepts anything
// else is applying rules the client never agreed to. Full is chosen over Incremental for
// what a document is here rather than what is cheaper to write — this server holds one
// text per document and re-reads all of it on every change — and the [import address
// rule](../rules/import-address/import-address.md) and the display contract are what
// fix the rest of what is advertised here.
import { LEGEND } from "./contract.ts";

export interface Position {
  line: number;
  character: number;
}

/** One content change as a client sends it. `range` is only ever read to refuse a payload
 *  that contradicts the capability declared below: a Full change carries no range, so a
 *  range here is a fault of the client's, not a position this server applies. */
export interface Change {
  text: string;
  range?: { start: Position; end: Position };
}

/** The document synchronization this server declares, by LSP's own names. `change: 1`
 *  is Full and `change: 2` is Incremental.
 *
 *  It is Full, and the reason is what a document is here rather than what is cheaper to
 *  write: this server holds one text per document and re-reads all of it on every change
 *  (`analyse` scans and parses the whole thing), so there is no state an incremental
 *  update would keep up to date — it would buy a correctness burden and no saving. And
 *  these documents are the language's own unit of reading: a declaration occupies one
 *  line and the line's break terminates it (docs/khayyam/khayyam.md, Declaration
 *  separator), so the whole text is what the recovery is defined over.
 *
 *  Full also states one thing the client must honour, and which cannot be honoured by a
 *  server being lenient: the change carries the whole text and no range. A server that
 *  accepts a range anyway is applying rules the client never agreed to — that every
 *  change in one notification shares the pre-change coordinates and that they arrive
 *  bottom-up — so where a client sends them the other way the two disagree and the
 *  server holds a text no editor has. Every fault and every role it then answers is
 *  about that text, and the editor shows it as though it were about the file on screen:
 *  a fault the reader has already corrected stays on the line, and the roles never move.
 *  So the two shapes are told apart by name, and the mismatch is a refusal. */
const DECLARED_CHANGE = 1;
const FULL_CHANGE = "Full";

/** What a client reads at `initialize`: the capabilities this server answers under, and
 *  what it is. */
export function declaredCapabilities(): {
  capabilities: {
    textDocumentSync: { openClose: boolean; change: number };
    // A place a name is declared at, which is a different answer from the role it
    // carries: the two are asked for separately and neither is derived from the
    // other ([definition.ts](./definition.ts)).
    definitionProvider: boolean;
    semanticTokensProvider: { legend: { tokenTypes: string[]; tokenModifiers: string[] }; full: boolean };
  };
  serverInfo: { name: string; version: string };
} {
  return {
    capabilities: {
      textDocumentSync: { openClose: true, change: DECLARED_CHANGE },
      definitionProvider: true,
      semanticTokensProvider: {
        // The legend is the contract's roles in the contract's own order, and each entry
        // is the token type the editor matches a styling rule against, whole
        // ([contract.ts](./contract.ts)).
        legend: { tokenTypes: LEGEND, tokenModifiers: [] },
        full: true,
      },
    },
    serverInfo: { name: "khayyam-language-server", version: "0.1.0" },
  };
}

/** What a `didChange` payload is, measured against the capability declared above: one
 * content change carrying the whole document, with no range. Anything else contradicts
 * what this server said it would accept, and the reason says which field of which
 * message, so the client can be told what to send rather than left guessing. */
export function contradictsDeclaredChange(changes: Change[]): string | null {
  if (changes.length !== 1) {
    return (
      `textDocumentSync.change is ${DECLARED_CHANGE} (${FULL_CHANGE}), which is one content change` +
      ` carrying the whole document, and this textDocument/didChange carries ${changes.length}.`
    );
  }
  const [change] = changes;
  if (change?.range !== undefined) {
    return (
      `textDocumentSync.change is ${DECLARED_CHANGE} (${FULL_CHANGE}), which is a content change with` +
      ` no range, and contentChanges[0] carries the range ${JSON.stringify(change.range)}.` +
      " This server applies no ranges, so it would not be reading the editor's text."
    );
  }
  return null;
}
