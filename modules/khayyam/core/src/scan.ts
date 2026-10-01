import type { Fault, RefusalReason } from "./sr.ts";

/** The two keywords that open a declaration, one per top-level concept. */
const DECLARATION_KEYWORDS = ["tp", "vr"] as const;
/** The five subtype keywords, one per Type subtype. */
export const SUBTYPE_KEYWORDS = ["in", "cp", "mt", "ab", "sc"] as const;

export const KEYWORDS = [...DECLARATION_KEYWORDS, ...SUBTYPE_KEYWORDS] as const;

export type Keyword = (typeof KEYWORDS)[number];

export type TokenKind = "ident" | "string" | "punct" | "newline" | "eof";

export interface Token {
  kind: TokenKind;
  text: string;
  /** One-based, as a refusal message counts. */
  line: number;
  /** One-based, as the editor counts; a string's column is its first character
   *  inside the quotes, so the opening quote is the column before it. */
  column: number;
}

export interface ScanFailure {
  ok: false;
  fault: Fault;
  /** What was scanned before the fault. A reader that only wants positions —
   *  a display, say — can use these; a reader that wants meaning cannot. */
  tokens: Token[];
}

export interface ScanSuccess {
  ok: true;
  tokens: Token[];
  /** What the scanner could not read, each at the place it stands. A fault whose
   *  extent ends with its own line is reported and the scan resumes at the next
   *  line, so one unreadable line does not cost the file the rest of its tokens. */
  faults: Fault[];
}

export type ScanResult = ScanSuccess | ScanFailure;

const IDENT_START = /[\p{L}_]/u;
const IDENT_PART = /[\p{L}\p{Nd}_]/u;
const PUNCTUATION = "{}().,;";

export function isKeyword(text: string): text is Keyword {
  return (KEYWORDS as readonly string[]).includes(text);
}

export function scan(source: string): ScanResult {
  const tokens: Token[] = [];
  const faults: Fault[] = [];
  let index = 0;
  let line = 1;
  let lineStart = 0;

  // The scanner owns every position in a token; a consumer that has to find a
  // token's place in the source again is doing this job twice.
  const column = (at: number): number => at - lineStart + 1;
  const fault = (reason: RefusalReason, at: number, text: string, extent: Fault["extent"]): Fault => ({
    reason,
    line,
    column: column(at),
    length: text.length,
    text,
    extent,
  });
  /** A fault that ends with its own line: it is reported, and the scan resumes at
   *  the next line. The language terminates every construct a line carries with
   *  that line's break - a declaration, and a statement inside a method body the
   *  same way (docs/khayyam/khayyam.md, Declaration separator) - so the rest of
   *  that line is part of what was not understood, and the next line is the first
   *  place reading can go on. */
  const faultOnLine = (reason: RefusalReason, at: number, text: string): void => {
    faults.push(fault(reason, at, text, "line"));
    while (index < source.length && source[index] !== "\n") index += 1;
  };
  /** A fault whose extent is not known from here: the rest of the file is inside
   *  it, so there is no next place to resume and the scan cannot answer at all.
   *  The stream still ends in `eof`, because a reader of what was read before the
   *  fault needs to know where that reading stops, and an unterminated stream says
   *  nothing about where. */
  const refuse = (reason: RefusalReason, at: number, text: string): ScanFailure => {
    emit("eof", "", index);
    return { ok: false, fault: fault(reason, at, text, "file"), tokens };
  };
  const emit = (kind: TokenKind, text: string, at: number): void => {
    tokens.push({ kind, text, line, column: column(at) });
  };

  while (index < source.length) {
    const character = source[index]!;

    if (character === "\n") {
      emit("newline", "\n", index);
      line += 1;
      lineStart = index + 1;
      index += 1;
      continue;
    }

    if (character === "\r" || character === " " || character === "\t") {
      index += 1;
      continue;
    }

    if (character === "/" && source[index + 1] === "/") {
      while (index < source.length && source[index] !== "\n") index += 1;
      continue;
    }

    if (character === "/" && source[index + 1] === "*") {
      const end = source.indexOf("*/", index + 2);
      if (end < 0) return refuse("unterminated-block-comment", index, "/*");
      for (let at = index; at < end + 2; at += 1) {
        if (source[at] === "\n") {
          line += 1;
          lineStart = at + 1;
        }
      }
      index = end + 2;
      continue;
    }

    if (character === '"') {
      let end = index + 1;
      while (
        end < source.length &&
        source[end] !== '"' &&
        source[end] !== "\n"
      ) {
        end += 1;
      }
      if (end >= source.length || source[end] !== '"') {
        // A quoted form runs to the end of its line, so an unterminated one is
        // bounded by that line like any other: report it and read from the next.
        faultOnLine("unterminated-string", index + 1, source.slice(index + 1, end));
        continue;
      }
      emit("string", source.slice(index + 1, end), index + 1);
      index = end + 1;
      continue;
    }

    if (IDENT_START.test(character)) {
      let end = index + 1;
      while (end < source.length && IDENT_PART.test(source[end]!)) end += 1;
      emit("ident", source.slice(index, end), index);
      index = end;
      continue;
    }

    if (PUNCTUATION.includes(character)) {
      emit("punct", character, index);
      index += 1;
      continue;
    }

    // A character that is not a letter, a quote, or one of the punctuation the
    // grammar has: not an identifier's part, not a quoted form, not a delimiter.
    // It stands alone on its line, so the line's rest is what it takes with it.
    faultOnLine("unexpected-character", index, character);
  }

  emit("eof", "", index);
  return { ok: true, tokens, faults };
}
