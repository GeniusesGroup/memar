/* For license and copyright information please see the LEGAL file in the code repository */
import { change, close, holds, open, text, version } from "./documents.ts";
import { inspectDeclaration } from "../../services/inspect-declaration/inspect-declaration.ts";
import { validateSource, type ValidationQuestion } from "../../services/validate-source/validate-source.ts";
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
      return [respond(id!, declaredCapabilities())];
    case "initialized":
      return [];
    case "shutdown":
      return [respond(id!, null)];
    case "exit":
      process.exit(0);
    case "textDocument/didOpen": {
      const document = params!.textDocument as { uri: string; text: string; version?: number };
      return open(document.uri, document.text, reach(), document.version);
    }
    case "textDocument/didChange": {
      const document = params!.textDocument as { uri: string; version?: number };
      return change(document.uri, (params!.contentChanges as Change[]) ?? [], reach(), document.version);
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
    case "khayyam/inspectDeclaration": {
      const document = params?.textDocument as { uri?: string; version?: number } | undefined;
      const position = params?.position as { line?: number; character?: number } | undefined;
      if (typeof document?.uri !== "string" || !Number.isInteger(position?.line) || !Number.isInteger(position?.character) || position!.line! < 0 || position!.character! < 0) {
        return [refuse(id, -32602, "inspection needs a document URI and nonnegative integer position")!];
      }
      const refusal = refusesDocumentHeld(id, document.uri);
      if (refusal !== null) return [refusal];
      const heldVersion = version(document.uri);
      if (document.version !== undefined && document.version !== heldVersion) {
        return [refuse(id, -32602, `inspection requested version ${document.version}; held version is ${heldVersion}`)!];
      }
      return [respond(id!, inspectDeclaration({ uri: document.uri, text: text(document.uri)!, version: heldVersion },
        position as { line: number; character: number }, { ...reach(), version }))];
    }
    case "khayyam/validateSource": {
      try {
        const request = params as unknown as ValidationQuestion;
        const overlays = new Map((Array.isArray(request?.overlays) ? request.overlays : []).map(source => [source.uri, source.text]));
        return [respond(id!, validateSource(request, { ...resolutionReach(uri => overlays.get(uri) ?? text(uri)), version }))];
      } catch (error) {
        return [refuse(id, -32602, error instanceof Error ? error.message : String(error))!];
      }
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

function reach(): Reach {
  return resolutionReach(text);
}

function refusesDocumentHeld(id: number | undefined, uri: string): string | null {
  if (holds(uri)) return null;
  return refuse(
    id,
    -32602,
    `this server holds no document at ${uri}: textDocument/didOpen never arrived, or textDocument/didClose took it away`,
  );
}
