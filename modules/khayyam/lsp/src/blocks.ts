// The blocks a document holds open as it is walked, and how far its braces carry it —
// the two together are what says which block a line stands in and whether it leaves one
// open behind it.
//
// A block is a fact about the document rather than about a line, which is why the whole
// of what distinguishes a method-local from a file-level variable is held here and can
// carry no TextMate scope: the line that opens the body is not on the line that declares
// the variable (display.json -> method-local, `serverOnlyBecause`).
//
// A walk records what each block it opens has had declared in it, in the order it opened
// them, so that a second walk over the same lines can begin with the whole of what the
// bodies declare already bound. That is the two-pass reading stated as a thing this
// module holds rather than as a trick a walk performs: the language fixes a
// declaration's line and says nothing about the order of a body's statements, so a use
// cannot be resolved against the names it happens to be preceded by — a name would be two
// things, the body's own on the line after its declaration and a bare use on the line
// before it.
import { braceDepth, type Item, type Place } from "./document-items.ts";

export interface Block {
  kind: "cp" | "ab" | "mt" | "sc";
  fields: Set<string>;
  composition: Set<string>;
  /** The parameters of a method, each mapped to where its name stands in the signature,
   *  and mapped to nothing when the walk did not find it there. A method's parameters
   *  are read from the parse, so a name is known to be one even where the walk over the
   *  line missed it — a file read with recovery can hold such a line — and a definition
   *  asked at that name is then no answer rather than one that points somewhere else. */
  parameters: Map<string, Place | undefined>;
  /** What the block has had declared in it, each mapped to the identity the name carries
   *  and where it stands. A `vr` in a body is a `method-local` and a `tp {name} sc` in
   *  one is a `scope`; the display contract splits those two into two identities, so a
   *  block holds what each name IS rather than only where it stands. */
  locals: Map<string, Declared>;
  /** How many braces were open inside this block when it was entered, which is what
   *  says whether the file has come back out of it. A line's block is the last one
   *  entered whose depth the file has not yet returned from, so a brace on any line
   *  counts — a body statement may open a block no declaration opened, and a count
   *  that read only the declaration lines lost its place on the first one. */
  depth: number;
}

/** What a body declared: the role its name carries, the sentence saying what it is, and
 *  where the name stands. The role travels with the place because a body holds two
 *  identities and only one of them is a variable. */
export interface Declared {
  role: string;
  origin: string;
  place: Place;
}

/** What a declaration gives the block it opens, beyond its kind and depth. */
export interface Carries {
  fields?: Set<string>;
  composition?: Set<string>;
  parameters?: Map<string, Place | undefined>;
}

/** How far a line's braces carry the file: where it stood before the line, and where it
 *  stands after it. */
export interface Depth {
  before: number;
  after: number;
}

export interface OpenBlocks {
  /** Applies what one line's items do to the depth, and leaves the file standing in
   *  the block that line stands in. The count does not fall below zero, because a
   *  brace closes nothing. */
  entered(items: Item[]): Depth;
  /** A block the file has entered and not come back out of. */
  opened(kind: Block["kind"], depth: number, carries?: Carries): void;
  /** The block a line stands in: the last one entered that the file has not come back
   *  out of. */
  enclosing(): Block | undefined;
  /** The method a statement belongs to, which is the nearest one open. */
  method(): Block | undefined;
  /** Where the name is declared inside a block that is open as the file stands, or
   *  undefined when this file declares no such name. The nearest block that declares
   *  it is the one it is, which is what makes the body's own declaration win over a
   *  file-level name of the same text. */
  declares(text: string): Declared | undefined;
  /** What each block this walk has opened has had declared in it, in the order it opened
   *  them, for a second walk over the same lines to begin with. */
  collected(): Map<string, Declared>[];
}

export function openBlocks(alreadyDeclared?: Map<string, Declared>[]): OpenBlocks {
  const stack: Block[] = [];
  /** How many braces are open as the file stands, counted over every line. */
  let depth = 0;
  /** One entry per block opened, holding what that block has had declared in it. The
   *  order is what pairs a block with its own entry in another walk's record, and the two
   *  walks open the same blocks in the same order because they walk the same lines. */
  const log: Map<string, Declared>[] = [];

  return {
    entered: (items) => {
      const before = depth;
      depth = Math.max(0, before + braceDepth(items));
      // The file's brace depth before and after a line say which block the line stands
      // in and whether it leaves one open behind it: a block is left when the depth the
      // file had come back to is shallower than the block was entered at.
      while (stack.length > 0 && stack[stack.length - 1]!.depth > before) stack.pop();
      return { before, after: depth };
    },
    opened: (kind, at, carries) => {
      // A second walk begins with what the first one found here already bound, so a use
      // is resolved against the whole of what its body declares rather than against what
      // it has been preceded by. Copied, so the record the first walk returns is its own.
      const locals = new Map(alreadyDeclared?.[log.length] ?? []);
      log.push(locals);
      stack.push({
        kind,
        fields: carries?.fields ?? new Set(),
        composition: carries?.composition ?? new Set(),
        parameters: carries?.parameters ?? new Map(),
        locals,
        depth: at,
      });
    },
    enclosing: () => stack[stack.length - 1],
    method: () => {
      for (let at = stack.length - 1; at >= 0; at -= 1) {
        if (stack[at]!.kind === "mt") return stack[at]!;
      }
      return undefined;
    },
    declares: (text) => {
      for (let at = stack.length - 1; at >= 0; at -= 1) {
        const declared = stack[at]!.locals.get(text);
        if (declared !== undefined) return declared;
      }
      return undefined;
    },
    collected: () => log.map((entry) => new Map(entry)),
  };
}
