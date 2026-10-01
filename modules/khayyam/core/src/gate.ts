import { scan } from "./scan.ts";
import { Parser, Refusal } from "./parse.ts";
import type { Fault, Unit } from "./sr.ts";

export interface ParseFailure {
  ok: false;
  fault: Fault;
}

export interface ParseSuccess {
  ok: true;
  unit: Unit;
}

export type ParseResult = ParseFailure | ParseSuccess;

/** Reads a unit, or says why it could not be read. A gate asks this: a file with
 *  any fault in it is refused, and the fault it names is the one met first, so the
 *  labels this toolchain refuses with are unchanged by anything below. */
export function parseUnit(path: string, source: string): ParseResult {
  const scanned = scan(source);
  if (!scanned.ok) {
    return { ok: false, fault: scanned.fault };
  }
  if (scanned.faults.length > 0) {
    // A lexical fault is the frontend's own finding, and it is reported as such
    // rather than handed to a parser to read a file whose characters the scanner
    // did not accept.
    return { ok: false, fault: scanned.faults[0]! };
  }
  try {
    return { ok: true, unit: new Parser(scanned.tokens, false).parseUnit(path) };
  } catch (error) {
    if (error instanceof Refusal) {
      return { ok: false, fault: error.fault };
    }
    throw error;
  }
}
