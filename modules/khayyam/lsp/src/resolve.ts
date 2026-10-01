// Turning what a declaring file says into the document an address reaches.
//
// [Dependency management](../../../docs/protocols/modules/dependency-management.md) owns
// what a manifest says. [`manifest.ts`](./manifest.ts) finds the file that declares a root;
// this file is the registry of how each kind of such a file answers, and it is where the
// answer says which reader produced it.
//
// **Two forms, and the minimal one is a marker rather than a manifest.** The owner ruled
// (2026-09-30) that a project declares where it ends with a file: `memar.manifest.{format}`
// when it has something to say, and `manifest.yaml` when the only thing it needs to say is
// "this directory is the root, and do not go above it". A file whose whole content is its
// presence is a degenerate manifest and it is the cheaper of the two by exactly as much as it
// says less — and **its text is not read**, because nothing in it is needed for the base and
// guessing at YAML this server has no parser for would be inventing a declaration nobody
// wrote. Claims go in the rich form, where there is a reader for them.
//
// The registry is ordered and every answer names the reader that produced it, so no form is
// a default that the others fall back on quietly: a project that wrote a claim and gets the
// minimal form's answer has been told which form answered, which is the fact that tells them
// their claim was in the file nobody reads. That is the same reason a format this server
// cannot read is named rather than skipped.
//
// What none of these readers may do is answer for a *name*. They say which document an
// address reaches and nothing more; whether that document declares the name is
// [`inclusions.ts`](./inclusions.ts)'s question, and a reader that answered it here would be
// letting a mechanism decide what a program means.

import { readFileSync } from "node:fs";
import { dirname, isAbsolute, join } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

import type { Resolved } from "./definition.ts";
import type { Form, Walked } from "./manifest.ts";

/** What one kind of declaring file answers, and what it calls itself when it does. */
interface Reader {
  /** The name a reader of the answer sees, so the answer names its own mechanism. */
  via: string;
  /** The document the address reaches, or the reason there is none. `manifest` is what the
   *  walk found; `address` is what the writing file wrote; `here` is the writing file itself,
   *  which is what a relative address is read against. */
  read: (manifest: Walked, address: string, here: string) => Resolved;
}

/** The minimal form: a file whose presence states the root, and an address read as a path
 *  under it. This is the form that resolves today, because it is the only one whose whole
 *  content this server can honour without a design it does not have. */
const rootManifest: Reader = {
  via: "a stated root",
  read: (manifest, address, here) => {
    const root = dirname(manifest.at!);
    const at = isAbsolute(address) ? address : join(root, address);
    let text: string;
    try {
      text = readFileSync(at, "utf8");
    } catch {
      return {
        via: rootManifest.via,
        base: baseOf(manifest),
        because:
          `${root} declares itself the root, and "${address}" names nothing under it. This is ` +
          "unresolved-import's own question: the root was found and the address resolved to nothing",
      };
    }
    return { via: rootManifest.via, base: baseOf(manifest), found: { uri: pathToFileURL(at).href, text } };
  },
};

/** The rich form: read, and reported as read, with the honest statement that what a manifest
 *  *says* is not designed yet. It does not fall through to the minimal form's answer, because
 *  a project that wrote a claim and got a path answer would never learn its claim was in a
 *  file no one reads. */
const declaredManifest: Reader = {
  via: "a module manifest",
  read: (manifest) => ({
    via: declaredManifest.via,
    base: baseOf(manifest),
    because:
      `a module manifest is at ${manifest.at} and was read, and this server does not yet know how to ` +
      "ask it anything. What a manifest says — which part of the address space is its own, how one " +
      "reaches it, which other modules it uses — belongs to Dependency and Version Management " +
      "(docs/protocols/modules/dependency-management.md) and is not designed yet",
  }),
};

/** Which reader answers which form. The form is what a declaring file's own name says, so
 *  this is the one place where a name is allowed to decide anything — and it decides only
 *  which of two declared forms answers, never what any of them says. */
const READERS: Readonly<Record<Form, Reader>> = {
  declared: declaredManifest,
  minimal: rootManifest,
};

/** What an address reaches. `walked` is what the walk found; the address and the writing
 *  file's own path are what the walk found it for.
 *  @param walked the nearest declaring file above the writing file, or the reason there is none
 *  @param address what the writing file wrote
 *  @param from the writing file's own path */
export function answerFrom(walked: Walked, address: string, from: string): Resolved {
  if (walked.at === undefined || walked.form === undefined) {
    return { because: walked.because ?? "nothing says where this file's project ends" };
  }
  const reader = READERS[walked.form];
  if (reader === undefined) {
    // Unreachable while the form is one of the two `Form` names, and kept because a form this
    // table has not heard of is a declaration this server cannot honour, and must say so
    // rather than fall through to another form's answer.
    return {
      base: baseOf(walked),
      because:
        `a declaring file is at ${walked.at} in a form this server has no reader for, and nothing is ` +
        "guessed about what it says",
    };
  }
  return reader.read(walked, address, from);
}

/** The base an answer is resolved from: the directory the declaring file sits in, which is
 *  what it declares a root to be. `dirname` rather than counting separators, because a
 *  hand-counted path is how this folder produced a base with a trailing separator on it — a
 *  base that is not a directory's own name cannot be compared with one that is.
 *  @param at the declaring file's own path */
export function baseOf(manifest: Walked): Resolved["base"] {
  return {
    directory: manifest.at === undefined ? "" : dirname(manifest.at),
    markedBy: manifest.form ?? "",
  };
}

/** The writing file's own path, from its URI, or the URI itself when it is not a path — which
 *  is the case for an editor's untitled document, and the walk then starts from nothing.
 *  @param uri the writing document's own URI */
export function pathOf(uri: string): string {
  try {
    return fileURLToPath(uri);
  } catch {
    return uri;
  }
}