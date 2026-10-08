import type { Declaration } from "./sr.ts";
import { scan, type Token } from "./scan.ts";

// Where a referenced type name stands in a source. This is the one answer to that question
// in the toolchain: the language server ([lsp/src/unbound-names.ts`](../../lsp/src/unbound-names.ts))
// and the rename service ([services/rename/khayyam-binding.ts](../../services/rename/khayyam-binding.ts))
// both consume it, and each of them wrote the walk itself before this file existed. Two walks
// over the same tokens are two answers to one question, and they had already parted company —
// on a file whose only mismatch row said a declaration's tokens could not be walked and named
// no reason. One place stands where a name stands.
//
// Which names a declaration references is not answered here. That is `referencedTypes`'s
// question (sr.ts) and it stays there; this module is handed a declaration and asked where
// each of its references stands, and it decides placement and never binding. A name it is not
// asked about is a name it says nothing about.
//
// The walk is over `scan`'s token stream and over nothing else, which is what makes the
// answer the language's own rather than a reading of characters: a `//` comment, a `/* */`
// block, and a quoted URI are not tokens, and an identifier is one whole token rather than a
// run of characters (`docs/khayyam/khayyam.md`, Identifiers). Every place below carries the
// line and column the scanner already found the name at — one-based, as the scanner counts
// and as `scan` says it does — so a consumer moves a place to its own base and never counts a
// line of the source again.
//
// Each form is walked as the shape the parse read for it, and each walk stops where the parse
// stopped: a method's body was carried as text rather than read as declarations, and a block
// that never closes took its declaration with it. A form the reader has no reference to — a
// scope, whose block is opaque text — answers `[]` and says why at its case rather than
// falling through to a walk of a shape the reader never produced.
//
// The order is the order the names stand in the source. That is one order where
// `referencedTypes` gives another, and it is worth naming: the reader gathers a capsule's
// field types ahead of its composition entries whatever lines they stand on, because the two
// are different lists in the representation, while a place is a place and the source is where
// it stands. A capsule that writes a composition entry above one of its fields is the one
// shape where the two orders differ; every file in this repository writes its fields first.

export interface ReferencePlace {
  /** One-based, as the scanner counts it and as a refusal message does. */
  line: number;
  /** One-based, as the editor counts. */
  column: number;
  /** How many characters the name covers, a qualified reference included whole. */
  length: number;
  /** What the scanner read there, which for a qualified reference is the whole `a.b`. */
  text: string;
}

/** Every place in `source` where a type name `declaration` references stands, in the order
 *  they stand.
 *
 *  The declaration carries its own line and not a column (sr.ts), so the walk starts at the
 *  first token the scanner read on that line. A line that holds no token is a line of
 *  comments or a blank one, and a declaration was never read on it.
 *
 *  A declaration the walk cannot account for answers with the places it did account for
 *  rather than with a guess, and it opens no channel to say so. Whether the places here are
 *  the references the reader counted is a question about two answers agreeing, not a question
 *  about where a name stands — and a report this file could emit about its own walk would be
 *  that question asked once more, which is the thing this file exists to end. */
export function referencePlaces(
  source: string,
  declaration: Declaration,
): ReferencePlace[] {
  const tokens = scan(source).tokens;
  const start = firstTokenOfLine(tokens, declaration.line);
  if (start === undefined) return [];
  const places: ReferencePlace[] = [];
  // A declaration is its keyword, its name, its subtype and whatever follows. A line whose
  // leading tokens are not that is not this declaration's line: the reader recovered past a
  // fault and this line's first tokens belong to something the fault left behind.
  const keyword = tokens[start];
  const name = tokens[start + 1];
  const subtype = tokens[start + 2];
  // Which keyword this declaration was written with is asked of the form itself and not
  // through `declarationKind`: that function answers `tp` for a `vr-in`, which is what the
  // analyser compares an included declaration's kind against, and it is no use to a walk that
  // needs to know which of the two words stands at the head of this line.
  const written =
    declaration.form === "vr" || declaration.form === "vr-in" ? "vr" : "tp";
  if (keyword?.kind !== "ident" || keyword.text !== written) return [];
  if (name?.kind !== "ident") return [];

  switch (declaration.form) {
    case "tp-in":
    case "vr-in":
      // An inclusion routes a name to a file, and the name it routes is the one place a name
      // this declaration references stands at (`docs/khayyam/khayyam.md`, Import Mechanism
      // (`in`)). The URI beside it is a quoted string and names no type.
      if (subtype?.text !== "in" || tokens[start + 3]?.kind !== "string") return [];
      places.push(placeOf(name));
      return places;
    case "vr":
      // `vr {name} {type}` writes its type where `tp` writes its subtype
      // (`docs/khayyam/khayyam.md`, Variable), so the type is read from its own slot and not
      // from the slot after the subtype. A type is never the `in` keyword — `expectName`
      // refuses a keyword as a name — so this slot holding one is an inclusion, and the
      // inclusion's name is already placed above.
      if (subtype?.kind !== "ident" || subtype.text === "in") return [];
      const type = readType(tokens, start + 2);
      if (type === undefined) return [];
      places.push(type.place);
      return places;
    case "tp-cp":
      // A capsule's block holds both shapes its references take, and which shape an entry is
      // decides which of its names is the reference (`docs/khayyam/khayyam.md`, Capsule).
      if (subtype?.text !== "cp") return [];
      if (blockPlaces(tokens, start + 3, places) === undefined) return [];
      return places;
    case "tp-ab":
      // The composition block is optional (`docs/khayyam/khayyam.md`, Abstraction), so a
      // body-less abstraction reaches its line's end rather than a brace.
      if (subtype?.text !== "ab") return [];
      if (tokens[start + 3]?.text === "{") {
        if (blockPlaces(tokens, start + 3, places) === undefined) return [];
      }
      return places;
    case "tp-mt":
      // The three groups are walked and then the walk stops: what follows is the body, which
      // the reader carried as text rather than read as declarations
      // (`docs/khayyam/khayyam.md`, Method), so a name inside one is neither a reference the
      // reader counted nor one this module places. What the groups already gave are kept: a
      // body is no fault and no reason to withhold the signature before it, and a group the
      // walk could not read through keeps the groups it did.
      if (subtype?.text !== "mt") return [];
      signaturePlaces(tokens, start + 3, places);
      return places;
    case "tp-sc":
      // A scope's block holds commands, not types, and the reader never read any of it as
      // declarations (`docs/khayyam/khayyam.md`, Scope; the parser's own `parseBlock` joins a
      // body's tokens into one string). Nothing in it is a reference this module accounts for,
      // so the form answers nothing rather than walking a shape the reader never produced. The
      // case stands here for the same reason the reader refuses the form at the top level: a
      // scope belongs inside a method body (`scope-placement`).
      return [];
  }
}

/** The index of the first token the scanner read on `line`, and undefined where the line
 *  holds none — a line of comments, a blank line, or a line a recovered read never reached. */
function firstTokenOfLine(tokens: Token[], line: number): number | undefined {
  const at = tokens.findIndex((token) => token.line >= line);
  return at < 0 ? undefined : at;
}

function placeOf(token: Token): ReferencePlace {
  return {
    line: token.line,
    column: token.column,
    length: token.text.length,
    text: token.text,
  };
}

// There is no "does the declaration end here" check, and asking would be the wrong question.
// This walk holds the whole file's tokens, so the token standing after a declaration's line
// break is the next declaration's keyword and not anything that declaration left behind. Each
// form is pinned by the shape of its own head instead — a keyword, a name, a subtype, and the
// slots that subtype admits — which is the shape the parse read.

interface ReadType {
  place: ReferencePlace;
  /** The index past the reference's last token. */
  end: number;
}

/** One type reference at `index`: an identifier, or identifiers joined by dots, which is the
 *  shape `expectTypeReference` in `core/src/parse.ts` reads. A qualified reference is one
 *  reference and so one place — a caller that rewrites it rewrites `pkg.Type` whole, and one
 *  place saying which half of it is the name would let the other half be read as text. Its
 *  length is its own text's because a line break is a token of its own and a type reference
 *  never reaches one: the whole reference therefore stands on the line its first token is on.
 *  `end` is the index past its last token. */
function readType(tokens: Token[], index: number): ReadType | undefined {
  const first = tokens[index];
  if (first === undefined || first.kind !== "ident") return undefined;
  let text = first.text;
  let end = index + 1;
  while (tokens[end]?.text === "." && tokens[end + 1]?.kind === "ident") {
    text += `.${tokens[end + 1]!.text}`;
    end += 2;
  }
  return { place: { line: first.line, column: first.column, length: text.length, text }, end };
}

/** The place of every parameter type in the three groups of a method signature, walked in the
 *  order the groups stand, and the index past the third. A group is `( name type, … )`, so a
 *  name in one is a parameter naming a value and the type beside it is the reference. Nothing
 *  here reports a name, which is what keeps a parameter spelled like a type — `(self Reader)`
 *  — out of the places a type stands in; a name and a type are the same word and two
 *  different things at the same column, and only the slot says which. */
function signaturePlaces(tokens: Token[], at: number, places: ReferencePlace[]): number | undefined {
  for (let group = 0; group < 3; group += 1) {
    if (tokens[at]?.text !== "(") return undefined;
    at += 1;
    const close = closingParenthesis(tokens, at);
    if (close === undefined) return undefined;
    while (at < close) {
      if (tokens[at]!.kind !== "ident") return undefined;
      const type = readType(tokens, at + 1);
      if (type === undefined || type.end > close) return undefined;
      places.push(type.place);
      at = type.end;
      if (at === close) break;
      if (tokens[at]?.text !== ",") return undefined;
      at += 1;
    }
    at = close + 1;
  }
  return at;
}

/** The index of the `)` that closes the group opened before `at`, and undefined where the
 *  stream holds none: a group that never closes costs the parse the whole declaration, and a
 *  walk that guessed where it ended would place names in a declaration the reader never
 *  produced. */
function closingParenthesis(tokens: Token[], at: number): number | undefined {
  let depth = 1;
  for (let index = at; index < tokens.length; index += 1) {
    const token = tokens[index]!;
    if (token.kind === "eof") return undefined;
    if (token.text === "(") depth += 1;
    else if (token.text === ")") {
      depth -= 1;
      if (depth === 0) return index;
    }
  }
  return undefined;
}

/** The references a capsule's or an abstraction's block holds, from the `{` at `at` to the
 *  `}` that closes it, and the index past that `}`. Entries are newline-separated
 *  (`docs/khayyam/khayyam.md`, Capsule; Abstraction), so an entry is the tokens between two
 *  line breaks — which is what makes a field, a composition entry, and a nested block
 *  readable off the same walk, since each of them opens and closes where the reader's block
 *  read says it does. Undefined when the stream ends inside the block: a block never closed is
 *  a fault that costs the file its declaration (`unbalanced-block`), and a walk that ran to
 *  the end of the file would place names that declaration never had. */
function blockPlaces(
  tokens: Token[],
  at: number,
  places: ReferencePlace[],
): number | undefined {
  if (tokens[at]?.text !== "{") return undefined;
  let depth = 1;
  let entryFrom = at + 1;
  for (let index = at + 1; index < tokens.length; index += 1) {
    const token = tokens[index]!;
    if (token.kind === "punct" && (token.text === "{" || token.text === "}")) {
      if (!blockEntryPlace(tokens, entryFrom, index, places)) return undefined;
      entryFrom = index + 1;
      if (token.text === "{") depth += 1;
      else if (--depth === 0) return entryFrom;
    } else if (token.kind === "newline") {
      // A blank line inside a block is no entry, and it is not a fault
      // (`parseFieldBlock` skips newlines before reading a name).
      if (!blockEntryPlace(tokens, entryFrom, index, places)) return undefined;
      entryFrom = index + 1;
    }
  }
  return undefined;
}

/** Whether the tokens between `from` and `to` are one entry of a block, and the reference
 *  inside it if they are. One name is a composition entry and two are a field and its type
 *  (`docs/khayyam/khayyam.md`, Capsule; Abstraction): which one an entry is is what decides
 *  which of its names is a reference, and it is the same question the reader's
 *  `parseFieldBlock` asks, so a name is not a field here and a composition entry there. */
function blockEntryPlace(
  tokens: Token[],
  from: number,
  to: number,
  places: ReferencePlace[],
): boolean {
  if (from === to) return true;
  if (tokens[from]!.kind !== "ident") return false;
  if (to === from + 1) {
    places.push(placeOf(tokens[from]!));
    return true;
  }
  const type = readType(tokens, from + 1);
  if (type === undefined || type.end !== to) return false;
  places.push(type.place);
  return true;
}
