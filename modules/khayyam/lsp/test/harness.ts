import { spawn, type ChildProcessWithoutNullStreams } from "node:child_process";
import { fileURLToPath } from "node:url";

import type { Diagnostic, Frame } from "./wire.ts";

// How to reach this server: spawn it on its own stdio, frame what a message looks like,
// and answer the notifications it publishes. The shapes those messages carry are the
// wire's own and live in [wire.ts](./wire.ts).
//
// This is the one statement of how to speak to this server, because the synchronization
// and the definitions are both claims about the wire and a claim about the wire is only
// checkable on the wire. Two copies would be two statements of it, and they would drift:
// a second one is written to whatever the test that owns it happened to need.

const SERVER = fileURLToPath(new URL("../src/server.ts", import.meta.url));

/** The scratch document the suite reads a pasted file under. It names a path that is
 *  not there, and that is the point: nothing in these tests may depend on a file that
 *  does exist behind the text they hand the server. */
export const PROBE = "file:///c:/scratch/probe.kh";

export class Server {
  private readonly child: ChildProcessWithoutNullStreams;
  private buffer = Buffer.alloc(0);
  private readonly pending = new Map<number, (frame: Frame) => void>();
  private nextId = 1;
  readonly published: Frame[] = [];

  constructor() {
    this.child = spawn(process.execPath, [SERVER], { stdio: ["pipe", "pipe", "pipe"] });
    this.child.stdout.on("data", (chunk: Buffer) => this.receive(chunk));
  }

  private receive(chunk: Buffer): void {
    this.buffer = Buffer.concat([this.buffer, chunk]);
    for (;;) {
      const text = this.buffer.toString("utf8");
      const separator = text.indexOf("\r\n\r\n");
      if (separator < 0) return;
      const declared = /Content-Length:\s*(\d+)/i.exec(text.slice(0, separator));
      if (declared === null) {
        this.buffer = this.buffer.subarray(separator + 4);
        continue;
      }
      const length = Number(declared[1]);
      const start = separator + 4;
      if (Buffer.byteLength(text.slice(start), "utf8") < length) return;
      const frame = JSON.parse(
        Buffer.from(text.slice(start), "utf8").subarray(0, length).toString("utf8"),
      ) as Frame;
      this.buffer = this.buffer.subarray(start + length);
      const answer = this.pending.get(frame.id ?? -1);
      if (answer !== undefined) {
        this.pending.delete(frame.id!);
        answer(frame);
      } else if (frame.method !== undefined) {
        this.published.push(frame);
      }
    }
  }

  request<T>(method: string, params: unknown): Promise<T> {
    const id = this.nextId++;
    return new Promise((resolve, reject) => {
      this.pending.set(id, (frame) => {
        if (frame.error !== undefined) reject(new Error(frame.error.message));
        else resolve(frame.result as T);
      });
      this.send({ jsonrpc: "2.0", id, method, params });
    });
  }

  notify(method: string, params: unknown): void {
    this.send({ jsonrpc: "2.0", method, params });
  }

  private send(frame: unknown): void {
    const body = JSON.stringify(frame);
    this.child.stdin.write(`Content-Length: ${Buffer.byteLength(body, "utf8")}\r\n\r\n${body}`);
  }

  /** How long a wait for a publication or a request may take before it is called a
   *  failure. Long enough that a whole suite spawning a server per test does not turn a
   *  publication into a timeout — which is a different fault, reported as a different
   *  thing, and the one that made a working server look broken under load. */
  private static readonly PATIENCE = 400;
  private static readonly PAUSE = 25;

  private forUri(uri: string): Frame[] {
    return this.published.filter((frame) => frame.params?.uri === uri);
  }

  /** The diagnostics the server published for a document the first time it published for
   *  it — which is the document as it was opened, since a server answers an open before
   *  it is asked anything. */
  async firstPublishedFor(uri: string): Promise<Diagnostic[]> {
    for (let attempt = 0; attempt < Server.PATIENCE; attempt += 1) {
      const first = this.forUri(uri)[0];
      if (first !== undefined) return first.params!.diagnostics;
      await new Promise((resolve) => setTimeout(resolve, Server.PAUSE));
    }
    throw new Error(`the server published nothing for ${uri}`);
  }

  /** The next diagnostics the server publishes for a document, which is how it tells a
   *  client a fault is gone: an empty publication is the clearing, so a test that read
   *  the answer to an earlier change would be reading a stale document.
   *
   *  "Next" is counted from the publications that have already arrived, which is only the
   *  change just sent if that change's own publication has not overtaken the one before
   *  it — and a server answering two changes in order can have both in flight. So the
   *  count is taken once the earlier one has landed, which is what every caller of this
   *  gets by having been handed a server that has already seen its open answered. */
  async publishedFor(uri: string): Promise<Diagnostic[]> {
    await this.firstPublishedFor(uri);
    const seen = this.forUri(uri).length;
    for (let attempt = 0; attempt < Server.PATIENCE; attempt += 1) {
      const found = this.forUri(uri);
      if (found.length > seen) return found[found.length - 1]!.params!.diagnostics;
      await new Promise((resolve) => setTimeout(resolve, Server.PAUSE));
    }
    throw new Error(`the server published nothing new for ${uri}`);
  }

  async tokensFor(uri: string): Promise<number[]> {
    const result = await this.request<{ data: number[] }>("textDocument/semanticTokens/full", {
      textDocument: { uri },
    });
    return result.data;
  }

  stop(): void {
    this.child.kill();
  }
}

/** What a client states before it opens anything: the capabilities it understands, and
 *  the workspace its files live in. A client that states no workspace states no base,
 *  and a server told none answers no definition for a name that arrived by an inclusion
 *  while still answering every name the document it holds declares. */
export interface Stated {
  /** The workspace the files are in, as a URI. Omitted when the client states none. */
  workspace?: string;
  /** The document to open. Defaults to the suite's scratch document. */
  uri?: string;
}

/** A server that has been told what the client states, given a document, and waited for
 *  that document's first publication — which is the state a question about the text has
 *  to start from, and the state in which "the next publication" means the one the next
 *  change is about to earn rather than the open still in flight. */
export async function holding(source: string, stated: Stated = {}): Promise<Server> {
  const server = new Server();
  await server.request("initialize", {
    processId: process.pid,
    rootUri: stated.workspace ?? null,
    capabilities: {},
  });
  server.notify("initialized", {});
  const uri = stated.uri ?? PROBE;
  server.notify("textDocument/didOpen", {
    textDocument: { uri, version: 1, text: source },
  });
  await server.firstPublishedFor(uri);
  return server;
}
