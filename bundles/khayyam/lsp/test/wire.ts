// The shapes a claim about the wire is made of, in the wire's own terms: a position, a
// range, a diagnostic, and the place a name is declared at.
//
// They are here rather than in the harness that speaks them because they are two things —
// what the wire carries, and how to reach this server — and a test that never opens a
// connection still needs the first. What speaks the wire is [harness.ts](./harness.ts).

export interface Position {
  line: number;
  character: number;
}

export interface Range {
  start: Position;
  end: Position;
}

export interface Diagnostic {
  range: Range;
  severity: number;
  code: string;
  source: string;
  message: string;
}

/** A place a name is declared at, as it goes on the wire. */
export interface Location {
  uri: string;
  range: Range;
}

export interface Frame {
  id?: number;
  method?: string;
  params?: { uri: string; diagnostics: Diagnostic[] };
  result?: unknown;
  error?: { message: string };
}
