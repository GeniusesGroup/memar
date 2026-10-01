// The wire this server speaks: a header, a blank line, and a body of exactly the declared
// byte length — and the two ends of it, the frames it sends and the ones it reads.
//
// Reading a frame is here rather than in the loop that answers it because a frame may be
// split across reads and because a frame this server cannot read is not a reason to stop
// serving. Both are claims about bytes on a pipe, which is why they are held apart from
// the answers ([handlers.ts](./handlers.ts)): a client that sends a header with no length
// has said nothing this server can act on, and the next frame it sends is still read.
import type { Message } from "./handlers.ts";

/** The three shapes this server sends: a notification, a response, and a refusal. A
 *  refusal carries the client's own connection's error rather than a result, because a
 *  payload this server cannot read is not an answer it has. */
export function notify(method: string, params: unknown): string {
  return frame({ jsonrpc: "2.0", method, params });
}

export function respond(id: number, result: unknown): string {
  return frame({ jsonrpc: "2.0", id, result });
}

/** A refusal, in the shape the client's own connection raises rather than answers.
 *  `id` is absent on a notification, and a notification cannot be refused, so there is
 *  nothing to send. */
export function refuse(id: number | undefined, code: number, message: string): string | null {
  if (id === undefined) return null;
  return frame({ jsonrpc: "2.0", id, error: { code, message } });
}

export function frame(payload: unknown): string {
  const body = JSON.stringify(payload);
  // The length is counted in bytes, because the body is sent as bytes and a client
  // reading a character count would cut a frame short wherever the text is not ASCII.
  return `Content-Length: ${Buffer.byteLength(body, "utf8")}\r\n\r\n${body}`;
}

export type Taken =
  | { kind: "frame"; message: Message; rest: Buffer }
  /** A frame this server will not act on — a header that declares no length, a body that
   *  will not parse — which is dropped so that the frame after it is still read. */
  | { kind: "skipped"; rest: Buffer }
  /** The buffer holds no whole frame yet: the body of this one has not all arrived. */
  | { kind: "more" };

/** One frame out of the buffer, and the bytes that follow it. The buffer is drained in a
 *  loop, so a read carrying several frames yields several calls. */
export function takeFrame(buffer: Buffer): Taken {
  const text = buffer.toString("utf8");
  const separator = text.indexOf("\r\n\r\n");
  if (separator < 0) return { kind: "more" };
  const match = /Content-Length:\s*(\d+)/i.exec(text.slice(0, separator));
  if (!match) return { kind: "skipped", rest: buffer.subarray(separator + 4) };
  const length = Number(match[1]);
  const bodyStart = separator + 4;
  if (Buffer.byteLength(text.slice(bodyStart), "utf8") < length) return { kind: "more" };
  const body = Buffer.from(text.slice(bodyStart), "utf8").subarray(0, length).toString("utf8");
  const rest = buffer.subarray(bodyStart + length);
  let message: unknown;
  try {
    message = JSON.parse(body);
  } catch {
    return { kind: "skipped", rest };
  }
  return { kind: "frame", message: message as Message, rest };
}

/** Every way out of this process says where it went. A server that stops without a word
 *  is one the client cannot tell from a server that is working, and the client shows its
 *  reader nothing until someone goes looking — which is how a dead server read as a
 *  success. stderr is the channel the client forwards to its own log. */
export function stop(code: number, why: string): never {
  process.stderr.write(`${why}\n`);
  process.exit(code);
}

/** Reads frames off this process's stdin and writes the answers onto its stdout, for as
 *  long as the client keeps talking. */
export function serve(answer: (message: Message) => string[]): void {
  let buffer: Buffer = Buffer.alloc(0);
  process.stdout.on("error", (error) => stop(1, `stdout closed, so no frame can be sent: ${String(error)}`));
  process.on("uncaughtException", (error) => stop(1, `uncaught fault, the server is stopping: ${String(error)}`));
  process.on("unhandledRejection", (reason) => stop(1, `unhandled rejection, the server is stopping: ${String(reason)}`));
  process.stdin.on("data", (chunk: Buffer) => {
    buffer = Buffer.concat([buffer, chunk]);
    for (;;) {
      const taken = takeFrame(buffer);
      if (taken.kind === "more") return;
      buffer = taken.rest;
      if (taken.kind === "skipped") continue;
      try {
        for (const response of answer(taken.message)) process.stdout.write(response);
      } catch (error) {
        // A fault while answering is a fault in this server, not in the frame, and it is
        // said twice on purpose: on stderr, which the client forwards to its log, and in
        // the response itself, so the client's request comes back a refusal that names the
        // fault instead of waiting out its timeout on a request that can never be answered.
        const text = String(error);
        process.stderr.write(`${text}\n`);
        const failure = refuse(taken.message.id, -32603, text);
        if (failure) process.stdout.write(failure);
      }
    }
  });
  process.stdin.on("end", () => stop(0, "stdin closed, so the client is gone"));
}
