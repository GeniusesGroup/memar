// The answer to each request this server takes, one concern per method. This file routes
// and nothing else: what a document is held is [documents.ts](./documents.ts), what a
// name's role is [semantic.ts](./semantic.ts), where a name is declared
// [definition.ts](./definition.ts), and how any of it goes on the wire is
// [transport.ts](./transport.ts).
//
// The grammar keeps doing what a grammar can do; everything a grammar cannot know — which
// binding an occurrence denotes — comes from here.
import { change, close, holds, open, text } from "./documents.ts";
import { declaredCapabilities, type Change } from "./capabilities.ts";
import { definitionAt, type Reach } from "./definition.ts";
import { refuse, respond } from "./transport.ts";
import { encodeTokens } from "./token-stream.ts";
import { analyse } from "./semantic.ts";
import { resolutionReach } from "./workspace.ts";

export interface Message {
  id?: number;
  method?: string;
  params?: Record<string, unknown>;
}

export function handle(message: Message): string[] {
  const { id, method, params } = message;
  switch (method) {
    case "initialize":
      // The workspace a client states is not read. It used to be the base an address was
      // resolved from, which made this server right only for a reader who opened the root
      // and wrong for every reader who opened a folder inside it. The base is now the
      // manifest of the module that wrote the address, and a client's window is not that
      // module — so what the client says is recorded by the client and used for nothing
      // here.
      return [respond(id!, declaredCapabilities())];
    case "initialized":
      return [];
    case "shutdown":
      return [respond(id!, null)];
    case "exit":
      process.exit(0);
    case "textDocument/didOpen": {
      const document = params!.textDocument as { uri: string; text: string };
      return open(document.uri, document.text, reach());
    }
    case "textDocument/didChange": {
      const document = params!.textDocument as { uri: string };
      return change(document.uri, (params!.contentChanges as Change[]) ?? [], reach());
    }
    case "textDocument/didClose": {
      const document = params!.textDocument as { uri: string };
      return [close(document.uri)];
    }
    case "textDocument/semanticTokens/full": {
      const document = params!.textDocument as { uri: string };
      const refusal = refusesDocumentHeld(id, document.uri);
      return refusal === null ? [respond(id!, { data: encodeTokens(analyse(text(document.uri)!).roles) })] : [refusal];
    }
    case "textDocument/definition": {
      const document = params!.textDocument as { uri: string };
      const position = params!.position as { line: number; character: number };
      const refusal = refusesDocumentHeld(id, document.uri);
      if (refusal !== null) return [refusal];
      const found = definitionAt(document.uri, text(document.uri)!, position, reach());
      return [respond(id!, found === null ? null : {
        uri: found.uri,
        range: {
          start: { line: found.line, character: found.startChar },
          end: { line: found.line, character: found.startChar + found.length },
        },
      })];
    }
    default: {
      const answer = id === undefined ? null : respond(id, null);
      return answer ? [answer] : [];
    }
  }
}

/** How far this server reaches beyond a document: the files the addresses it writes resolve
 *  to, found from the document's own place, and the documents it holds, which come before
 *  the file system because a place the editor is sent to is read against the text the
 *  editor holds. */
function reach(): Reach {
  return resolutionReach(text);
}

/** A refusal of a question about a document this server holds no text for, or nothing at
 *  all when the question is one a notification may ask. A document this server was never
 *  told about is a document that did not reach it, which is a different fault from one it
 *  holds and cannot answer about: the empty answer of either role or definition is a real
 *  answer for a real document, and must not be one for a fault. */
function refusesDocumentHeld(id: number | undefined, uri: string): string | null {
  if (holds(uri)) return null;
  return refuse(
    id,
    -32602,
    `this server holds no document at ${uri}: textDocument/didOpen never arrived, or textDocument/didClose took it away`,
  );
}
