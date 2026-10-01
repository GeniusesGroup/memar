// The stream the editor reads: LSP's delta encoding of the roles the reading answered
// with.
//
// The token type is the role's index in the contract's role order, and the legend
// advertised at initialize is the role's own name at that same index — the token type the
// editor matches its styling rules against, whole. The value for the role is stated by the
// client's own `editor.semanticTokenColorCustomizations` rules, keyed by that same name;
// the language is stated in the `[khayyam]` block those rules sit in and in this
// provider's document selector, never in the name.
import { tokenTypeIndex } from "./contract.ts";
import type { SemanticToken } from "./role-emitter.ts";

export function encodeTokens(roles: SemanticToken[]): number[] {
  const data: number[] = [];
  let previousLine = 0;
  let previousStart = 0;
  for (const token of roles) {
    const type = tokenTypeIndex(token.role);
    // A role the contract does not define has no entry in the legend, so the editor
    // would drop the token while merging it into the grammar's. It is not sent, and the
    // token after it is measured from the token before that, since this one was never
    // placed.
    if (type < 0) continue;
    const deltaLine = token.line - previousLine;
    const deltaStart = deltaLine === 0 ? token.startChar - previousStart : token.startChar;
    data.push(deltaLine, deltaStart, token.length, type, 0);
    previousLine = token.line;
    previousStart = token.startChar;
  }
  return data;
}
