import type { CompiledProgram } from "./program.ts";

/** A loaded artifact or linked module: a table of the names it exports. */
export type Module = Record<string, unknown>;

/** Loads the code a unit stands at. What stands at a unit is the program's
 *  decision, not the host's — a compiled artifact, or a module a link put in a
 *  unit's place — so the host is asked for a URI and not told which it is. */
export type Loader = (uri: string) => Promise<Module>;

/** What to run. Entry and lifecycle are the host's configuration and not the
 *  language's (docs/protocols/computer/compiler.md → Entry and lifecycle are not
 *  grammar), which is why a request names a method rather than a `main`. */
export interface EntryRequest {
  /** The unit that declares the entry method. */
  uri: string;
  /** The program's units, because every one of them is reached at run time: a
   *  body-less method's implementation is supplied to the unit that declares it,
   *  whatever unit imported it. */
  units: string[];
  /** The method to call. */
  method: string;
  /** What the call is made on: the parent type named in the method's owner
   *  group, and the values of that capsule's fields. */
  owner: { type: string; fields?: Record<string, unknown> };
  /** The influencing variables, in the order the signature writes them. */
  influencing: unknown[];
  /** The influenced variables' values before the call, in the order the
   *  signature writes them; a call writes into them, so what it wrote is what
   *  the run answers. */
  influenced?: unknown[];
  /** The implementation of each body-less method, keyed by the URI of the unit
   *  that declares it and then by the name the artifact exports it under. */
  supplied?: Record<string, Record<string, (...parameters: unknown[]) => unknown>>;
}

export interface RunAnswer {
  /** What the call wrote into each influenced variable, in the order the
   *  signature writes them. */
  influenced: unknown[];
}

function supplyOf(module: Module): ((implementations: Record<string, unknown>) => void) | undefined {
  const candidate = module["supply"];
  return typeof candidate === "function"
    ? (candidate as (implementations: Record<string, unknown>) => void)
    : undefined;
}

/** Runs one entry of a program on the host: loads every unit the program stands
 *  on, hands each unit the implementations of its body-less methods, builds the
 *  owner the call is made on, and makes the call. Nothing here decides what the
 *  program means — the artifact does — so this is configuration and a call. */
export async function run(request: EntryRequest, load: Loader): Promise<RunAnswer> {
  const modules = new Map<string, Module>();
  for (const uri of request.units) {
    const module = await load(uri);
    modules.set(uri, module);
    const supply = supplyOf(module);
    if (supply !== undefined) supply(request.supplied?.[uri] ?? {});
  }
  const root = modules.get(request.uri);
  if (root === undefined) throw new Error(`${request.uri} is not one of the program's units`);
  const owner = root[request.owner.type];
  if (typeof owner !== "function") {
    throw new Error(`${request.uri} declares no capsule named ${request.owner.type}`);
  }
  const instance = new (owner as new (fields: Record<string, unknown>) => unknown)(
    request.owner.fields ?? {},
  );
  const entry = root[`${request.owner.type}$${request.method}`];
  if (typeof entry !== "function") {
    throw new Error(`${request.uri} declares no method named ${request.method}`);
  }
  // Every variable of a call is a slot (docs/khayyam/khayyam.md → Method), and
  // the entry is a call the host makes on the program's own method: the host
  // hands over values and this is where each becomes the slot the artifact's
  // methods hand to one another.
  const influencing = (request.influencing ?? []).map((value) => ({ value }));
  const influenced = (request.influenced ?? []).map((value) => ({ value }));
  (entry as (...parameters: unknown[]) => unknown)(
    instance,
    ...influencing,
    ...influenced,
  );
  return { influenced: influenced.map((slot) => slot.value) };
}

