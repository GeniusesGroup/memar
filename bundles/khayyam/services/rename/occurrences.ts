// What an identifier service asks a language for, and what a language hands back. This is
// the seam the declaration-rename service ([`rename.ts`](./rename.ts)) is written against:
// the service owns the corpus, the plan, the report, the write, the gate and the command,
// and it owns nothing about how a name is bound — every question of that kind is asked of a
// `Binding` through the declarations below, and the binding is the one the caller beside it
// hands to the run, so nothing here looks one up or holds a second of them.
//
// The vocabulary here is deliberately the identifier's own and not any language's. A place
// in a source is a path, a line, a column, a length and a **role**: what the place is, in
// whatever words the binding that found it uses. The role of a declaration's own name, of
// the clause that brings it, of a signature, a field, a composition or a variable's type is
// Khayyam's; `Occurrence.role` is a `string` so that the service can report a role it has
// never heard of without knowing what it means. Same for `form` and `kind` on a `Place`,
// and for the `class` of an entry the binding could not bind.
//
// What a binding owes is stated once, in `Binding`, and a language that supplies a
// different set of names for the same questions has lost nothing: the service reports them
// verbatim and reasons over none of them. What a language needs beyond this is not owed
// here either: another reader over another language's source, a prose class of its own, and
// the name a run that includes either reports itself under are facts of that language's
// target and are handed to the run beside the binding it belongs to.

/** One unit of source a run reads, and the one name it is about. `paths` is the corpus the
 *  service enumerated; `declaration` is the caller's answer to a body of source that
 *  declares the name more than once, and a binding checks it rather than trusting it. */
export interface Request {
  root: string;
  paths: string[];
  name: string;
  to: string;
  declaration?: string;
}

/** A declaration at a place, in a binding's own words: `form` is what shape it has and
 *  `kind` is what it declares. */
export interface Place {
  path: string;
  line: number;
  form: string;
  kind: string;
}

/** A place in a source where the name stands, or where the binding read it and left it.
 *  `role` is the binding's word for what the place is and `why` its reason for leaving it,
 *  because "not rewritten" is only useful next to "why not". */
export interface Occurrence {
  path: string;
  line: number;
  column: number;
  length: number;
  role: string;
  why?: string;
}

/** What a binding found about one name across the request's paths, and every path among
 *  them that could not be read — a path that cannot be read is a fact about the run, not
 *  about the name. */
export interface Found {
  name: string;
  /** Declarations that own the name: everything but one that routes a name it does not
   *  own. The one this run is about is chosen from these. */
  same_name: Place[];
  /** The declarations that bring the name into another file. Each of those is the same
   *  declaration reached by another route, so none of them makes the name ambiguous —
   *  and each is reported, because a route is a consumer too. */
  carried: Place[];
  /** Places already declaring the name the caller asked for, which is why the caller
   *  asked. */
  taken: Place[];
  target: Place | null;
  /** Why the name does not say which declaration this run is about. Non-empty refuses the
   *  run before any plan. */
  ambiguity: string[];
  /** The places a rewrite is planned at. */
  sites: Occurrence[];
  /** The places the binding read the name at and did not plan. */
  left_alone: Occurrence[];
  /** Every occurrence of the raw text of the name the binding's reader does not bind,
   *  classified by that reader: what it covers, what it is part of, and what it stands in.
   *  The service reports the `class` as it stands and never re-labels it — which text is
   *  prose to one reader and another language's source to the next is that reader's own
   *  fact, and a class the service rewrote would be a class it could not account for. */
  unread: (Occurrence & { class: string; text: string })[];
  /** Declarations whose own name carries this name, which is a different declaration and
   *  its own run. */
  longer_names: { name: string; path: string; line: number }[];
  /** Files whose own name is the declaration's name under any spelling. Reported, never
   *  renamed: which spelling a repository gives a file is its own owner's question. */
  file_renames: string[];
  /** What the binding's reader refused in a file it did read. */
  faults: { path: string; reason: string; line: number }[];
  missing: string[];
}

/** Reading another file of the corpus while a plan is being checked, which is what lets a
 *  check see the plan and not only the disk. */
export type Reader = (path: string) => string | undefined;

/** A binding's verdict on one file's text: whether it still means what it meant. */
export type Outcome = { outcome: "accept" } | { outcome: "refuse"; reason: string; line?: number };

/** What a language answers, and what an identifier service may ask it. A binding is the
 *  whole of one language's knowledge in this service: a name's occurrences and the check
 *  that says whether a rewrite still means anything. There is one of these per process and
 *  the caller supplies it, so a run never has to say which language it is about — a
 *  mechanism that held two bindings would hold two definitions of what a token is, and the
 *  second one is a language the first never agreed to. */
export interface Binding {
  /** The name this binding answers for, and the name a run in it reports itself
   *  under. */
  readonly language: string;

  /** Every place the language binds `name` to a declaration, and everything it found and
   * left. This is the whole of the finder's answer; what a caller does with it is the
   * caller's own. */
  find(request: Request): Found;

  /** Whether `source` still means something, which is the build gate. `read` answers for
   *  the rest of the corpus, so a plan is checked before it is written. */
  analyze(path: string, source: string, read: Reader): Outcome;
}
