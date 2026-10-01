// The client's half of a definition: the request this extension sends, and the reading of
// what comes back.
//
// It is a file of its own, and it requires nothing from the editor, because the two things
// a definition is made of are a statement about the wire and a statement about an answer —
// neither of which is a thing the editor's own objects are. The editor's `vscode.Location`
// is built in `client.js` from what this reads, and this is what says which document and
// which range.
//
// A role says what a name is and a definition says where it is declared at
// (modules/khayyam/lsp/src/definition.ts). This is only the second, and the answer carries
// nothing else: no name, no role, and no answer at all for a name nothing declares. Both
// of those are the server's own answers and neither is translated here — an answer this
// cannot read is refused by name, because a request that failed and a name that has no
// declaration have to look different in a log, and only one of them is a fault.

/**
 * The parameters of `textDocument/definition`, which is a document and a position and
 * nothing else.
 * @param {string} uri
 * @param {{ line: number; character: number }} position
 */
function definitionRequest(uri, position) {
  return { textDocument: { uri }, position: { line: position.line, character: position.character } };
}

/** Whether a value is the position the editor counts in: two whole numbers, counted from
 * zero, where a character offset is not one.
 * @param {unknown} value
 * @returns {value is { line: number; character: number }}
 */
function isPosition(value) {
  return (
    typeof value === "object" &&
    value !== null &&
    Number.isInteger(/** @type {{ line?: unknown }} */ (value).line) &&
    /** @type {{ line: number }} */ (value).line >= 0 &&
    Number.isInteger(/** @type {{ character?: unknown }} */ (value).character) &&
    /** @type {{ character: number }} */ (value).character >= 0
  );
}

/**
 * The place the server named, or null when it named none. An answer that is neither is
 * refused: answering something the editor cannot use is the failure this whole layer
 * exists to make loud, and reading a malformed answer leniently is what would send a
 * reader to the start of a file instead of to the name they asked about.
 * @param {unknown} answer
 * @returns {{ uri: string; range: unknown } | null}
 */
function readTarget(answer) {
  if (answer === null || answer === undefined) return null;
  const located = /** @type {{ uri?: unknown; range?: { start?: unknown; end?: unknown } }} */ (answer);
  if (
    typeof located.uri !== "string" ||
    typeof located.range !== "object" ||
    located.range === null ||
    !isPosition(located.range.start) ||
    !isPosition(located.range.end)
  ) {
    throw new Error(
      `the definition answer is not a place: ${JSON.stringify(answer)} — a definition is a document and a range`,
    );
  }
  return { uri: located.uri, range: { start: located.range.start, end: located.range.end } };
}

module.exports = { definitionRequest, readTarget };
