// What the scanner hands back before anything asks what a name is: the items of each
// line, in the columns the editor counts, and how far one line's braces carry the file.
//
// This is the origin every placement in this server is counted from — a role's extent,
// a diagnostic's range, a definition's line — so the columns here are the ones a client
// counts characters in: string indices, zero-based, which is what the scanner's
// one-based columns are moved back to once, here, rather than by each caller.
import { scan } from "../../core/src/scan.ts";

export interface Item {
  kind: "ident" | "string" | "punct";
  text: string;
  /** Zero-based, as the editor counts. */
  startChar: number;
}

/** A place in the document that was read, zero-based as the editor counts. The
 *  representation carries the line of every declaration and not its column
 *  (core/src/sr.ts), so a column is always the one the scan already found it at. */
export interface Place {
  line: number;
  startChar: number;
  length: number;
}

/** Groups what the scanner read by the line it stands on. A scan that stopped at a
 *  lexical fault still hands back what it read, so a document with one unterminated
 *  string is not left with no display at all. */
export function itemsOnLine(source: string): Map<number, Item[]> {
  const scanned = scan(source);
  const byLine = new Map<number, Item[]>();
  for (const token of scanned.tokens) {
    if (token.kind === "newline" || token.kind === "eof") continue;
    const line = token.line - 1;
    const list = byLine.get(line) ?? [];
    list.push({ kind: token.kind, text: token.text, startChar: token.column - 1 });
    byLine.set(line, list);
  }
  return byLine;
}

/** How far the braces of a line carry the file, and so whether the line leaves a block
 *  open behind it. `tp Counter cp {}` opens and closes on its own line and leaves
 *  nothing open; `tp Run mt (…) (…) (…) {` opens one that the lines after it stand in. */
export function braceDepth(items: Item[]): number {
  let depth = 0;
  for (const item of items) {
    if (item.kind !== "punct") continue;
    if (item.text === "{") depth += 1;
    else if (item.text === "}") depth -= 1;
  }
  return depth;
}

/** The place an item stands at, which is the place of the name it spells. */
export function placeOf(line: number, item: Item): Place {
  return { line, startChar: item.startChar, length: item.text.length };
}
