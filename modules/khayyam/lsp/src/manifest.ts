// Walking up from a file to the declaring file that says where the project ends.
//
// [Dependency management](../../../docs/protocols/modules/dependency-management.md) owns what
// a manifest says. This file owns where one is looked for, which is a fact about this
// filesystem realization and not about the protocol: the owner's ruling (2026-09-30) is that
// a project declares its own end with a file, and a reader walks upward from a file's own
// directory until it meets one.
//
// **The declaring file is the boundary, which is what the earlier two attempts at a boundary
// were not.** The first stopped at the directory holding `.agents`, which made a walk's end
// depend on a spelling. The second stopped at this repository's `MEMAR_ROOT`, which names
// where *Memar's source* sits on a machine — so in a project that merely uses Memar, which is
// what a framework is for, it names nothing about that project at all, and a criterion that
// answers for the framework rather than for the project is the storage engine's mistake in a
// project's clothes. A file in the project is about the project, needs no configuration, is
// visible in a directory listing, and travels with the project when it moves.
//
// Two forms, because the amount a project needs to say varies. `memar.manifest.{format}` is
// the one a project writes when it has something to say; `manifest.yaml` is the minimal one,
// where the file's whole content is its presence: *this directory is the root, and do not go
// above it*. Nothing is guessed about the minimal form's text — it is not read at all, which
// is not the same as being read and found empty.
//
// **The walk's second answer is that there is no filesystem.** A protocol in which a module
// is reachable has no directory to walk, and this file is that realization's half of the idea
// — the half to be replaced when the other half exists. Nothing above it may depend on *how* a
// declaring file was found, only on what it said.

import { readFileSync, readdirSync } from "node:fs";
import { basename, dirname, isAbsolute, join, parse, relative } from "node:path";

/** One manifest format a reader knows how to read. Adding a format is one entry in
 *  `FORMATS`; nothing above this file changes and nothing in the protocol names a format. */
interface Format {
  /** What a manifest's own name ends in, without the dot. */
  extension: string;
  /** What a sentence to a reader calls this format. */
  name: string;
  /** The whole file's text, read as this format. Throwing is the format's own refusal and is
   *  reported as a fault of the file rather than as a manifest that could not be found. */
  parse: (text: string) => unknown;
}

/** The formats this toolchain reads. JSON is here because a standard library parses it with
 *  nothing added; a format whose parser needs a library waits for that library, and a
 *  manifest in it is reported as unreadable rather than misread. */
const FORMATS: readonly Format[] = [{ extension: "json", name: "JSON", parse: JSON.parse }];

/** The stem of the form a project writes when it has something to say. */
const RICH = "memar.manifest.";

/** The minimal form's own name. Bare, because it is what every project has and a prefix would
 *  be a cost with nothing to say — which is also why the rich form carries one. */
const MINIMAL = "manifest.yaml";

/** Which kind of declaring file a found one is. */
export type Form = "declared" | "minimal";

/** One declaring file found in a directory. */
export interface FoundFile {
  /** Its own path. */
  at: string;
  /** Which of the two forms it is. */
  form: Form;
  /** What its name ends in, for the rich form. */
  format?: string;
}

/** Which condition ended a walk that found nothing, told apart because the remedy differs:
 *  a walk stopped by a configured boundary means the declaring file may be above it, while a
 *  walk that reached the filesystem's own root means there is nowhere further to look. */
export type Stopped = "boundary" | "filesystem";

/** What a walk found, or why it found nothing. */
export interface Walked {
  /** The declaring file, when a directory on the walk held one. */
  at?: string;
  /** Which of the two forms it is. */
  form?: Form;
  /** What its name ends in, for the rich form. */
  format?: string;
  /** Its content, read, when the rich form's format is one this toolchain reads. */
  read?: unknown;
  /** Set when a manifest is here but its content could not be produced: the format is not
   *  registered, or the file did not parse. */
  unreadable?: { format: string; reason: string };
  /** Set when a directory holds more than one declaring file, which is a fault and not a
   *  choice — a reader that picks one has invented a precedence nothing stated. */
  ambiguous?: string[];
  /** Which condition ended the walk. Set whenever no declaring file was found. */
  stopped?: Stopped;
  /** Why there is none, naming where the walk stopped. Always set when `at` is not. */
  because?: string;
}

/** Where the walk stops when this project has said so in advance, which is the one thing a
 *  declaring file cannot express: that a project's files live inside another project's tree
 *  and the walk should not leave this subtree. `MEMAR_ROOT` is read because it is the only
 *  such statement that exists, and it is a statement about **this** repository — a project
 *  that uses Memar states its own, or names a subtree of its own.
 */
export function statedBoundary(): string | undefined {
  const told = process.env.MEMAR_ROOT;
  return told === undefined || told.length === 0 ? undefined : told;
}

/** The declaring files in one directory, both forms, sorted because which of two a reader
 *  would have preferred is not a thing a reader may decide.
 *  @param at the directory to look in */
export function foundIn(at: string): FoundFile[] {
  let names: string[];
  try {
    names = readdirSync(at);
  } catch {
    return [];
  }
  const found: FoundFile[] = [];
  for (const name of names.sort()) {
    if (name === MINIMAL) found.push({ at: join(at, name), form: "minimal" });
    else if (name.startsWith(RICH) && name.length > RICH.length) {
      found.push({ at: join(at, name), form: "declared", format: name.slice(RICH.length) });
    }
  }
  return found;
}

/** What a rich manifest's path holds: its content when its format is registered, and why not
 *  when it is not. Never a fabricated empty value, because a manifest read as nothing is a
 *  manifest that declares nothing. The minimal form never comes here — its text is not read,
 *  because nothing in it is needed and guessing at YAML this server has no parser for would
 *  be inventing a declaration nobody wrote.
 *  @param at the rich manifest's own path */
export function contentOf(at: string): { read?: unknown; unreadable?: { format: string; reason: string } } {
  const extension = basename(at).slice(RICH.length);
  const format = FORMATS.find((candidate) => candidate.extension === extension);
  if (format === undefined) {
    return {
      unreadable: {
        format: extension,
        reason:
          `this toolchain reads ${FORMATS.map((each) => each.name).join(" and ")} manifests, and ${extension} ` +
          "is not one it reads. A format is one entry in the server's list, so opening an issue to add " +
          `it is the whole of the work; until then nothing at all is guessed about what this file says`,
      },
    };
  }
  try {
    return { read: format.parse(readFileSync(at, "utf8")) };
  } catch (error) {
    return {
      unreadable: {
        format: extension,
        reason: `${format.name} in this file did not parse: ${error instanceof Error ? error.message : String(error)}`,
      },
    };
  }
}

/** The walk: upward from a directory, one at a time, ending at the first declaring file, at
 *  a boundary stated in advance, or at the filesystem's own root. The walk does not continue
 *  past a declaring file — one that added to a higher one rather than replacing it would leave
 *  "which project does this file belong to" undecidable.
 *  @param from the directory to walk up from, which is a file's own directory
 *  @param boundary where to stop before passing, or undefined for the filesystem's root */
export function declaringAbove(from: string, boundary = statedBoundary()): Walked {
  // A stated boundary that does not stand above this file does not bound this walk. The walk
  // still happens, all the way to the filesystem's root, and the answer says so — because
  // stopping at a place this walk cannot reach would report a missing declaration for a file
  // that may have one three directories up.
  const bounded = boundary !== undefined && isUnder(boundary, from);
  const top = bounded ? boundary! : parse(from).root;
  let here = from;
  for (;;) {
    const found = foundIn(here);
    if (found.length > 1) {
      return {
        ambiguous: found.map((each) => each.at),
        because:
          `${here} holds ${found.length} declaring files, and a reader may not choose between them: ` +
          `${found.map((each) => basename(each.at)).join(", ")}. One directory holds one, or one of them ` +
          "says which of them is the one",
      };
    }
    if (found.length === 1) {
      const file = found[0]!;
      const { read, unreadable } = file.form === "minimal" ? {} : contentOf(file.at);
      return { at: file.at, form: file.form, format: file.format, read, unreadable };
    }
    if (here === top) {
      return {
        stopped: bounded ? "boundary" : "filesystem",
        because:
          `no ${RICH}<format> and no ${MINIMAL} was found in ${here} or in any directory above it, up to ` +
          (bounded ? `the boundary stated in advance, ${boundary}` : "the filesystem's own root") +
          ". No project has declared where this file's project ends",
      };
    }
    const up = dirname(here);
    if (up === here) {
      return {
        stopped: "filesystem",
        because:
          `no declaring file was found in ${here} or in any directory above it, up to the filesystem's ` +
          "own root, which is where the walk stops",
      };
    }
    here = up;
  }
}

/** Whether `directory` is `root` or stands under it. Written with the platform's own path
 *  arithmetic rather than a string prefix, because `C:\a` is not under `C:\ab` and a walk that
 *  believed otherwise would stop one directory short of where it was told to stop. */
function isUnder(root: string, directory: string): boolean {
  const below = relative(root, directory);
  return below === "" || (!below.startsWith("..") && !isAbsolute(below));
}