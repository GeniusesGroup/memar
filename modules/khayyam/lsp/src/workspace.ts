// What an address a document writes resolves to, and the reason when it resolves to
// nothing.
//
// The base an address is resolved from is **the manifest of the module that wrote it**, and
// not a repository root and not a folder a client says it has open. The owner's ruling of
// 2026-09-29 says where the declaration comes from: a module's manifest says everything
// about itself — which part of the address space is its own, how one reaches it, and which
// other modules it uses — and a file's addresses are read through that. A document that
// writes `in "memar/error"` is a file of some module, and that module's own manifest is
// what answers for the name; a repository that holds a hundred modules holds a hundred
// manifests, and there is no one base they all resolve from.
//
// This file therefore names no root and looks for no marker. It used to walk up for a
// version-control directory, and that walk is gone: it made the storage engine a fact of
// the model, and [Knowledge](../docs/knowledge.md) is explicit that version control is not
// this project's method of managing knowledge — a directory named `.git` is where a
// provisional tool happened to put things, and a resolver that reads its answers out of
// that directory is answering from the representation and calling it the represented.
//
// Every refusal opens with the same clause, and only its tail differs. The clause is the rule
// — an address is resolved through the manifest of the module that wrote it — and stating it
// in all three answers means a reader is told the rule once and what happened to it, rather
// than being handed a different sentence each time and having to work out which part is the
// rule. What the tails are told apart for is the remedy: a module that has not declared
// itself wants a manifest written, a manifest this server cannot read wants an issue opened,
// and a manifest this server can read wants a design it does not have yet. None of the three
// wants a file behind an address rewritten, because that file may well be there while nothing
// says how to reach it.
//
// A fourth thing rides along on the tails and is not optional: **where the walk ended**. A
// manifest found without a boundary stated for this file was found by walking out of the
// project, and on a machine holding several projects that is another project's module. The
// criterion for where a walk stops is a statement the *project being worked on* makes — this
// repository states one in `MEMAR_ROOT`, and a project that merely uses Memar states its own
// somewhere else and does not have one yet. That asymmetry is stated in the answer rather than
// smoothed over, because a resolver that silently took another project's module for its own
// would be wrong in a way nothing afterwards could explain.
//
// **What cannot be read is still the whole of what this server can say about a manifest.** The
// format is readable and the fields are not designed, so a manifest this server opens is read
// and not yet understood, and it says so rather than reporting an empty manifest as one that
// declares nothing. A reader of this file should not find an absolute URL in a diagnostic: a
// document is named by where it is in the tree, and the tree moves.
import { declaringAbove } from "./manifest.ts";
import { answerFrom, baseOf, pathOf } from "./resolve.ts";
import type { Reach, Resolved } from "./definition.ts";

export type { Resolved };

/** The rule every refusal below opens with, stated once so the tails can be short. */
const RULE = "an address is resolved through the declaring file of the project it is written in";

/** What an address written in a document resolves to, and why not when it does not. The
 *  address is the question the project asked; the declaring file is what answers it.
 *  @param uri the document the address was written in, which is where the walk for a
 *    declaring file starts — a file's own directory, and not a window's */
export function resolutionOf(uri: string, address: string): Resolved {
  const here = pathOf(uri);
  const walked = declaringAbove(here);
  if (walked.at === undefined) {
    return {
      because:
        `${RULE}, and no project has declared where ${uri} ends: ${walked.because ?? ""}. ` +
        "The thing to write is a declaring file, not a file — a file behind an address may well be there",
    };
  }
  if (walked.unreadable !== undefined) {
    return {
      via: "a module manifest",
      base: baseOf(walked),
      because:
        `${RULE}, and a manifest is at ${walked.at} but this server cannot read it — ` +
        `${walked.unreadable.reason}. Nothing is guessed about what it says, so the address ` +
        "resolves to nothing",
    };
  }
  return answerFrom(walked, address, here);
}



/** How far an answer may reach beyond the document it was asked about: the file an address
 *  names, read whole from where the writing module's manifest says it is, or the reason
 *  there is none.
 *
 *  A document this server holds comes before the file system, because a `Location` is read
 *  by the editor against the text the editor holds and this server's text of an open
 *  document is the editor's own — so a definition into a document the reader has open with
 *  unsaved edits would otherwise name a line the reader is not on.
 *  @param held the text this server holds of a document, if it holds one */
export function resolutionReach(held: (uri: string) => string | undefined = () => undefined): Reach {
  return { resolve: (address, from) => resolutionOf(from, address), held };
}
