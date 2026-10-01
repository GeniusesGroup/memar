import { isKeyword, type Token } from "./scan.ts";
import type {
  CapsuleDecl,
  Declaration,
  Fault,
  Field,
  MethodDecl,
  Param,
  RefusalReason,
  TypeInclude,
  Unit,
  VarDecl,
  VarInclude,
} from "./sr.ts";

export { parseUnit } from "./gate.ts";
export { readUnit } from "./reader.ts";

// The parse itself: reading a unit's declarations out of its tokens, and the fault a form
// that cannot be read carries. Whether reading goes on past such a fault is what tells a
// gate from a reader, so the two are asked for apart and live apart — the gate in gate.ts,
// the reader in reader.ts.
//
// The two re-exports above are a debt, not a home. core/src/frontend.ts and the language
// server reach both entry points through this module, and neither file is in this change's
// scope. Until those callers are repointed, the module the parse lives in is also the
// module a gate and a reader are named at, which is the one thing this split sets out to
// stop. The cycle that re-export makes is safe while the entry points are hoisted function
// declarations: nothing here reads a binding of gate.ts or reader.ts while this module is
// still being evaluated.

export class Refusal extends Error {
  readonly reason: RefusalReason;
  readonly line: number;
  readonly column: number;
  readonly length: number;
  readonly text: string;
  readonly because: Fault | undefined;

  constructor(reason: RefusalReason, token: Token, because?: Fault) {
    super(`${reason} (line ${token.line}, column ${token.column})`);
    this.reason = reason;
    this.line = token.line;
    this.column = token.column;
    this.length = token.text.length;
    this.text = token.text;
    this.because = because;
  }

  get fault(): Fault {
    return {
      reason: this.reason,
      line: this.line,
      column: this.column,
      length: this.length,
      text: this.text,
      extent: "declaration",
      ...(this.because === undefined ? {} : { because: this.because }),
    };
  }
}

export class Parser {
  private index = 0;
  private readonly tokens: Token[];
  /** Whether to read past a fault. A reader recovers; a gate refuses. */
  private readonly recovering: boolean;
  /** How many blocks are open at the token this parser has consumed, which is
   *  where reading resumes after a fault. */
  private depth = 0;
  /** The faults met before this parser was given the stream — the scanner's own. A
   *  fault that follows another is told which, and a scanner's lexical fault is as
   *  much a cause as a fault of the parser's own: it is the one that can take a brace
   *  off a line and never give it back. */
  private readonly before: Fault[];
  readonly faults: Fault[] = [];

  constructor(tokens: Token[], recovering: boolean, before: Fault[] = []) {
    this.tokens = tokens;
    this.recovering = recovering;
    this.before = before;
  }

  /** The token at a place, answering past the end of the stream with the end of it.
   *  A refusal that consumed the terminator - a block that never closes, read to the
   *  `eof` that ends a file whose comment never closes - must not send the read that
   *  follows it off the end of the stream. */
  private at(index: number): Token {
    const token = this.tokens[index];
    if (token !== undefined) return token;
    const last = this.tokens[this.tokens.length - 1]!;
    return { kind: "eof", text: "", line: last.line, column: last.column };
  }

  private peek(): Token {
    return this.at(this.index);
  }

  private take(): Token {
    const token = this.at(this.index);
    this.index += 1;
    if (token.kind === "punct" && token.text === "{") this.depth += 1;
    // A closing brace with nothing open closes nothing, so it does not take the
    // count below zero. That matters only in recovery, where the count is the
    // question "has reading come back out of the blocks it was inside" — a stray
    // closer that drove it negative would answer no, and the recovery would read
    // to the end of the file instead of to the end of the declaration.
    else if (token.kind === "punct" && token.text === "}" && this.depth > 0) this.depth -= 1;
    return token;
  }

  /** The fault a refusal follows from, when it follows from one.
   *
   *  A closing brace refused where a declaration was expected is not a form the author
   *  wrote there: the file's blocks no longer pair up, so this one is the leftover of a
   *  block an earlier fault unbalanced. The language terminates what a line carries with
   *  that line's break (docs/khayyam/khayyam.md, Declaration separator), so a fault that
   *  stopped reading — a character the scanner had no form for, a declaration the parser
   *  could not read — is exactly a fault that can have taken a brace with it. The last
   *  such fault standing before this brace is the one that did: it is the most recent
   *  place reading went wrong, and it is the one whose repair takes this fault with it.
   *  A `file`-extent fault ends the file, so nothing stands after it and it is never a
   *  cause here.
   *
   *  With no such fault, the brace closes nothing on its own account and is reported as
   *  the stray form it is. Either way the fault is reported: dropping it would say the
   *  file's structure is whole, which is the one thing it is not. */
  private consequence(token: Token): Fault | undefined {
    if (this.depth > 0) return undefined;
    if (token.kind !== "punct" || token.text !== "}") return undefined;
    return [...this.before, ...this.faults]
      .filter(
        (fault) =>
          fault.extent !== "file" &&
          (fault.line < token.line || (fault.line === token.line && fault.column < token.column)),
      )
      .at(-1);
  }

  private refuse(reason: RefusalReason, token: Token, because?: Fault): never {
    // Every `declaration-form` refusal is asked whether it follows from something, and
    // the answer is one place: a form the parser cannot read at a closing brace.
    const cause = reason === "declaration-form" ? (because ?? this.consequence(token)) : because;
    throw new Refusal(reason, token, cause);
  }

  private skipNewlines(): void {
    while (this.peek().kind === "newline") this.index += 1;
  }

  private expectPunct(text: string): void {
    const token = this.peek();
    if (token.kind !== "punct" || token.text !== text) {
      this.refuse("declaration-form", token);
    }
    this.index += 1;
  }

  private expectName(): string {
    const token = this.peek();
    if (token.kind === "ident" && isKeyword(token.text)) {
      this.refuse("keyword-as-identifier", token);
    }
    if (token.kind !== "ident") this.refuse("declaration-form", token);
    this.index += 1;
    return token.text;
  }

  private expectTypeReference(): string {
    let text = this.expectName();
    while (this.peek().kind === "punct" && this.peek().text === ".") {
      this.index += 1;
      text += `.${this.expectName()}`;
    }
    return text;
  }

  private expectString(): string {
    const token = this.peek();
    if (token.kind !== "string") this.refuse("declaration-form", token);
    this.index += 1;
    return token.text;
  }

  private expectSubtype(): string {
    const token = this.peek();
    if (token.kind === "newline" || token.kind === "eof") {
      this.refuse("missing-subtype", token);
    }
    if (token.kind !== "ident" || !isKeyword(token.text)) {
      this.refuse("declaration-form", token);
    }
    this.index += 1;
    return token.text;
  }

  private parseParamList(): Param[] {
    this.expectPunct("(");
    const params: Param[] = [];
    if (this.peek().kind === "punct" && this.peek().text === ")") {
      this.index += 1;
      return params;
    }
    for (;;) {
      const name = this.expectName();
      const type = this.expectTypeReference();
      params.push({ name, type });
      const token = this.peek();
      if (token.kind === "punct" && token.text === ",") {
        this.index += 1;
        continue;
      }
      break;
    }
    this.expectPunct(")");
    return params;
  }

  private parseBlock(): string | null {
    const token = this.peek();
    if (token.kind !== "punct" || token.text !== "{") return null;
    const parts: string[] = [];
    let depth = 0;
    for (;;) {
      const current = this.take();
      if (current.kind === "eof") this.refuse("unbalanced-block", current);
      if (current.kind === "punct" && current.text === "{") depth += 1;
      if (current.kind === "punct" && current.text === "}") {
        depth -= 1;
        if (depth === 0) break;
      }
      parts.push(current.kind === "newline" ? "\n" : current.text);
    }
    return parts.join(" ");
  }

  private parseFieldBlock(): { fields: Field[]; composition: string[] } {
    this.expectPunct("{");
    const fields: Field[] = [];
    const composition: string[] = [];
    for (;;) {
      const token = this.peek();
      if (token.kind === "eof") this.refuse("unbalanced-block", token);
      if (token.kind === "punct" && token.text === "}") {
        this.index += 1;
        return { fields, composition };
      }
      if (token.kind === "newline") {
        this.index += 1;
        continue;
      }
      const name = this.expectName();
      const following = this.peek();
      if (following.kind === "ident") {
        fields.push({ name, type: this.expectTypeReference() });
        continue;
      }
      if (
        following.kind === "newline" ||
        (following.kind === "punct" && following.text === "}")
      ) {
        composition.push(name);
        continue;
      }
      this.refuse("declaration-form", following);
    }
  }

  private parseCompositionBlock(): string[] {
    this.expectPunct("{");
    const composition: string[] = [];
    for (;;) {
      const token = this.peek();
      if (token.kind === "eof") this.refuse("unbalanced-block", token);
      if (token.kind === "punct" && token.text === "}") {
        this.index += 1;
        return composition;
      }
      if (token.kind === "newline") {
        this.index += 1;
        continue;
      }
      composition.push(this.expectName());
      const following = this.peek();
      if (
        following.kind !== "newline" &&
        !(following.kind === "punct" && following.text === "}")
      ) {
        this.refuse("declaration-form", following);
      }
    }
  }

  private parseType(): Declaration {
    const start = this.peek();
    const name = this.expectName();
    const subtype = this.expectSubtype();
    const line = start.line;
    switch (subtype) {
      case "in": {
        const declaration: TypeInclude = {
          form: "tp-in",
          name,
          line,
          path: this.expectString(),
        };
        return declaration;
      }
      case "cp": {
        const { fields, composition } = this.parseFieldBlock();
        const declaration: CapsuleDecl = {
          form: "tp-cp",
          name,
          line,
          fields,
          composition,
        };
        return declaration;
      }
      case "ab": {
        const composition =
          this.peek().kind === "punct" && this.peek().text === "{"
            ? this.parseCompositionBlock()
            : [];
        return { form: "tp-ab", name, line, composition };
      }
      case "mt": {
        const owner = this.parseParamList();
        const influencing = this.parseParamList();
        const influenced = this.parseParamList();
        const declaration: MethodDecl = {
          form: "tp-mt",
          name,
          line,
          owner,
          influencing,
          influenced,
          body: this.parseBlock(),
        };
        return declaration;
      }
      case "sc": {
        this.refuse("scope-placement", this.peek());
      }
      default:
        return this.refuse("declaration-form", this.peek());
    }
  }

  private parseVariable(): Declaration {
    const start = this.peek();
    const name = this.expectName();
    const line = start.line;
    const following = this.peek();
    if (following.kind === "ident" && following.text === "in") {
      this.index += 1;
      const declaration: VarInclude = {
        form: "vr-in",
        name,
        line,
        path: this.expectString(),
      };
      return declaration;
    }
    const declaration: VarDecl = {
      form: "vr",
      name,
      line,
      type: this.expectTypeReference(),
    };
    return declaration;
  }

  private parseDeclaration(): Declaration {
    const token = this.peek();
    if (token.kind !== "ident") this.refuse("declaration-form", token);
    if (token.text === "tp") {
      this.index += 1;
      return this.parseType();
    }
    if (token.text === "vr") {
      this.index += 1;
      return this.parseVariable();
    }
    return this.refuse("declaration-form", token);
  }

  /** Where reading goes on after a declaration could not be read: the line break
   *  that ends it. The language states that a declaration occupies one line and
   *  the line's break terminates it (docs/khayyam/khayyam.md, Declaration
   *  separator), and that a statement inside a method body is terminated the same
   *  way, so a declaration is the unit of recovery - not the file, and not the
   *  single unreadable word. A declaration that opened a block ends at the break
   *  after that block closes, which the depth the parser already carries names. */
  private recoverToDeclarationBoundary(): void {
    const depth = this.depth;
    while (this.peek().kind !== "eof") {
      if (this.peek().kind === "newline" && this.depth === depth) {
        this.index += 1;
        // A blank line is no declaration and is no fault: the gap between two
        // declarations is read the same way whether or not the one before it was.
        this.skipNewlines();
        return;
      }
      this.take();
    }
  }

  parseUnit(path: string): Unit {
    const declarations: Declaration[] = [];
    this.skipNewlines();
    while (this.peek().kind !== "eof") {
      try {
        declarations.push(this.parseDeclaration());
        const token = this.peek();
        if (token.kind === "eof") break;
        if (token.kind === "newline") {
          this.index += 1;
          this.skipNewlines();
          continue;
        }
        if (token.kind === "punct" && token.text === ";") {
          this.refuse("semicolon", token);
        }
        this.refuse("declaration-form", token);
      } catch (error) {
        if (!this.recovering || !(error instanceof Refusal)) throw error;
        this.faults.push(error.fault);
        this.recoverToDeclarationBoundary();
      }
    }
    return { path, declarations };
  }
}
