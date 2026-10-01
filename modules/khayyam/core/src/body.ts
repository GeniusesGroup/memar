import { isKeyword, scan, type Token } from "./scan.ts";
import type { Fault, RefusalReason } from "./sr.ts";

export type { Fault, RefusalReason };

/** One command of a method body, as the semantic representation carries it. The
 *  language states that each command ends with a new line
 *  (docs/khayyam/khayyam.md → Scope) and that the grammar ships no control-flow
 *  keyword, no operator, and no literal of its own, so the set of forms below is
 *  the whole of what a body may contain: a variable declaration, a scope, a
 *  method invocation, and the `return` marker. Anything else is a fault, so a
 *  body is never read past a form this toolchain does not have a meaning for. */
export type Command =
  | { form: "declare"; name: string; type: string }
  | { form: "scope"; name: string; body: Command[] }
  | {
      form: "invoke";
      receiver: string;
      method: string;
      influencing: string[];
      influenced: string[];
    }
  | { form: "return" };

export interface CommandsRead {
  ok: true;
  commands: Command[];
}

export interface CommandsRefused {
  ok: false;
  fault: Fault;
}

export type CommandsResult = CommandsRead | CommandsRefused;

class Refusal {
  readonly fault: Fault;

  constructor(reason: RefusalReason, token: Token, atLine: number) {
    // The text a body is carried as is read from the line its declaration stands
    // on — the block opens on that line, so the text's first line is that line —
    // and a fault a reader reports is at the line a person reads, not at the line
    // of a string this toolchain happened to keep.
    this.fault = {
      reason,
      line: atLine + token.line - 1,
      column: token.column,
      length: token.text.length,
      text: token.text,
      extent: "line",
    };
  }
}

class CommandReader {
  private index = 0;
  private readonly tokens: Token[];
  private readonly atLine: number;

  constructor(tokens: Token[], atLine: number) {
    this.tokens = tokens;
    this.atLine = atLine;
  }

  private at(offset = 0): Token {
    const token = this.tokens[this.index + offset];
    if (token !== undefined) return token;
    const last = this.tokens[this.tokens.length - 1]!;
    return { kind: "eof", text: "", line: last.line, column: last.column };
  }

  private take(): Token {
    const token = this.at();
    this.index += 1;
    return token;
  }

  private refuse(reason: RefusalReason, token: Token = this.at()): never {
    throw new Refusal(reason, token, this.atLine);
  }

  private isPunct(text: string, offset = 0): boolean {
    const token = this.at(offset);
    return token.kind === "punct" && token.text === text;
  }

  private expectPunct(text: string): void {
    if (!this.isPunct(text)) this.refuse("declaration-form");
    this.index += 1;
  }

  private expectName(): string {
    const token = this.at();
    if (token.kind === "ident" && isKeyword(token.text)) {
      this.refuse("keyword-as-identifier", token);
    }
    if (token.kind !== "ident") this.refuse("declaration-form", token);
    this.index += 1;
    return token.text;
  }

  /** A type reference as the declarations write one: a name, then any further
   *  names the dot operator joins (docs/khayyam/khayyam.md → Type). */
  private readTypeReference(): string {
    let text = this.expectName();
    while (this.isPunct(".")) {
      this.index += 1;
      text += `.${this.expectName()}`;
    }
    return text;
  }

  /** A command ends with a newline (docs/khayyam/khayyam.md → Scope), so what
   *  stands where the line should end is a form this command does not take. */
  private atEndOfCommand(): boolean {
    const token = this.at();
    return token.kind === "newline" || token.kind === "eof" || this.isPunct("}");
  }

  private readArgumentList(): string[] {
    this.expectPunct("(");
    const arguments_: string[] = [];
    if (this.isPunct(")")) {
      this.index += 1;
      return arguments_;
    }
    for (;;) {
      arguments_.push(this.readTypeReference());
      if (this.isPunct(",")) {
        this.index += 1;
        continue;
      }
      break;
    }
    this.expectPunct(")");
    return arguments_;
  }

  /** A call is a receiver, a dot, the method's name, and both call groups — the
   *  one invocation form the language has (docs/khayyam/khayyam.md → Method
   *  Invocation Rules). The name the first opening parenthesis follows is the
   *  method and whatever the dots join before it is the receiver, which is why a
   *  qualified receiver is read the same way as a bare one. */
  private readInvoke(): Command {
    const path = [this.expectName()];
    while (this.isPunct(".")) {
      this.index += 1;
      if (this.at().kind !== "ident") this.refuse("declaration-form");
      path.push(this.expectName());
    }
    if (!this.isPunct("(")) this.refuse("declaration-form");
    if (path.length < 2) this.refuse("declaration-form");
    const influencing = this.readArgumentList();
    if (!this.isPunct("(")) this.refuse("declaration-form");
    const influenced = this.readArgumentList();
    if (!this.atEndOfCommand()) this.refuse("declaration-form");
    const method = path[path.length - 1]!;
    return {
      form: "invoke",
      receiver: path.slice(0, path.length - 1).join("."),
      method,
      influencing,
      influenced,
    };
  }

  private readDeclare(): Command {
    this.take();
    const name = this.expectName();
    const type = this.readTypeReference();
    if (!this.atEndOfCommand()) this.refuse("declaration-form");
    return { form: "declare", name, type };
  }

  /** `sc` is the one subtype a body admits: a scope is what a branch body is,
   *  and the language states the others as declarations of the file
   *  (docs/khayyam/khayyam.md → Scope). */
  private readScope(): Command {
    this.take();
    const name = this.expectName();
    const subtype = this.at();
    if (subtype.kind === "newline" || subtype.kind === "eof") {
      this.refuse("missing-subtype", subtype);
    }
    if (subtype.kind !== "ident" || !isKeyword(subtype.text)) {
      this.refuse("declaration-form", subtype);
    }
    this.index += 1;
    if (subtype.text !== "sc") this.refuse("declaration-form", subtype);
    if (!this.isPunct("{")) this.refuse("declaration-form");
    this.index += 1;
    const body = this.readBlock();
    return { form: "scope", name, body };
  }

  private readCommand(): Command {
    const token = this.at();
    if (token.kind !== "ident") this.refuse("declaration-form", token);
    if (token.text === "tp") return this.readScope();
    if (token.text === "vr") return this.readDeclare();
    // `return` is not one of the language's keywords: it is an IR marker that
    // ends with a line break, so it carries nothing on its line
    // (docs/khayyam/khayyam.md → Scope).
    if (token.text === "return" && this.at(1).kind === "newline") {
      this.index += 1;
      return { form: "return" };
    }
    return this.readInvoke();
  }

  private readBlock(): Command[] {
    const commands: Command[] = [];
    for (;;) {
      const token = this.at();
      if (token.kind === "eof") this.refuse("unbalanced-block", token);
      if (token.kind === "newline") {
        this.index += 1;
        continue;
      }
      if (this.isPunct("}")) {
        this.index += 1;
        return commands;
      }
      commands.push(this.readCommand());
    }
  }

  read(): Command[] {
    // A body is carried as the text of its block, and the block opens on the
    // declaration's own line — the closing brace is the one token the frontend
    // leaves out, because the depth it tracks is what ends the body.
    if (this.isPunct("{")) this.index += 1;
    const commands: Command[] = [];
    for (;;) {
      const token = this.at();
      if (token.kind === "eof") return commands;
      if (token.kind === "newline") {
        this.index += 1;
        continue;
      }
      if (this.isPunct("}")) this.refuse("declaration-form", token);
      commands.push(this.readCommand());
      if (!this.atEndOfCommand()) this.refuse("declaration-form");
    }
  }
}

/** Reads the commands of a method body or of a scope's block, or says why one of
 *  them could not be read. The refusal is a gate's: the first fault met is the
 *  one named, because a compiler that lowered a body it only partly understood
 *  would decide what the program means. */
function atLineOf(fault: Fault, atLine: number): Fault {
  return { ...fault, line: atLine + fault.line - 1 };
}

export function readCommands(text: string, atLine = 1): CommandsResult {
  const scanned = scan(text);
  if (!scanned.ok) return { ok: false, fault: atLineOf(scanned.fault, atLine) };
  if (scanned.faults.length > 0) {
    return { ok: false, fault: atLineOf(scanned.faults[0]!, atLine) };
  }
  try {
    return { ok: true, commands: new CommandReader(scanned.tokens, atLine).read() };
  } catch (error) {
    if (error instanceof Refusal) return { ok: false, fault: error.fault };
    throw error;
  }
}
