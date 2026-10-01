import { scan } from "./scan.ts";
import { Parser, Refusal } from "./parse.ts";
import type { Fault, Unit } from "./sr.ts";

/** What a reader that recovers gets: the declarations that were read, and every
 *  fault that was met while reading them. */
export interface ReadResult {
  unit: Unit;
  faults: Fault[];
}

/** Reads what of a unit it can, and reports every fault met while reading it. This
 *  is for a reader, not a gate: a diagnostic is owed for each fault, and the rest
 *  of the file still has meaning to show. The recovery is per declaration, at the
 *  line break that ends one (docs/khayyam/khayyam.md, Declaration separator) - the
 *  language's own unit - so one unreadable declaration costs the file that
 *  declaration, and the inclusion form is no different: a `tp … in "…"` is one
 *  line, so a bad path costs its own line and not the inclusions beside it. The
 *  parser is given the scanner's faults as well as collecting its own, because one
 *  fault can be the cause of another and only a reader that has met both can say so. */
export function readUnit(path: string, source: string): ReadResult {
  const scanned = scan(source);
  // A fault with no next place to resume still leaves the lines before it whole —
  // the fault stands at a character, and every line above it ended where it says it
  // did — so those are read and the fault is reported beside them.
  const parser = new Parser(scanned.tokens, true, scanned.ok ? scanned.faults : [scanned.fault]);
  try {
    const unit = parser.parseUnit(path);
    return scanned.ok
      ? { unit, faults: [...scanned.faults, ...parser.faults] }
      : { unit, faults: [scanned.fault, ...parser.faults] };
  } catch (error) {
    if (!(error instanceof Refusal)) throw error;
    return {
      unit: { path, declarations: [] },
      faults: [...(scanned.ok ? scanned.faults : [scanned.fault]), error.fault],
    };
  }
}
