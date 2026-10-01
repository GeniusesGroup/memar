// The files the extension ships, and the readers over them.
//
// Every assertion the suite makes about a shipped file is made against the file
// itself and not against a copy of it, because a value the check exists to keep
// honest can only be judged where a reader will find it. Provoking a refusal is the
// opposite and needs a copy; that is `provoke.ts`'s concern and not this one's.
import { readFileSync } from "node:fs";
import { basename, join } from "node:path";
import { fileURLToPath } from "node:url";

export const ROOT = fileURLToPath(new URL("../../../../", import.meta.url));
export const EXTENSION = join(ROOT, ".agents", "vscode", "extensions", "khayyam-language");
export const THEMES = join(EXTENSION, "themes");
export const MANIFEST = join(EXTENSION, "package.json");
export const CONTRACT = join(ROOT, "modules", "khayyam", "display", "display.json");

/** The role of that name, wherever the contract was read from. It takes the contract
 *  rather than reading it, because a suite that provokes a refusal provokes it over a
 *  copy and a reader of a copy is asking the same question about a different file. */
export const roleNamed = (contract: any, name: string): any =>
  contract.roles.find((role: { name: string }) => role.name === name);

/** The base a shipped theme names, in the order a host reads it: the theme's own
 *  `include` first, then that file's own, down to the sheet that states no base of
 *  its own. The verifier walks the same chain, so the note the report carries can be
 *  read against the files rather than against a path written here. */
export function baseChain(file: string): string[] {
  const sheetOf = (name: string): any => JSON.parse(readFileSync(join(THEMES, name), "utf8"));
  const chain: string[] = [];
  for (let at = sheetOf(file).include; typeof at === "string"; at = sheetOf(basename(at)).include) {
    chain.push(basename(at));
    if (chain.length > 8) break;
  }
  return chain;
}

/** The background a reader gets from that chain: a host reads the deepest base first,
 *  so the statement nearest the theme is the one applied last and the one that stands -
 *  the first statement met walking outward. This is the background the display
 *  contract's floor is measured against, and after the base was added the theme states
 *  none of its own. */
export function baseBackground(file: string): string {
  const chain = baseChain(file).map((name) => JSON.parse(readFileSync(join(THEMES, name), "utf8")));
  return chain.find((sheet) => typeof sheet.colors?.["editor.background"] === "string")?.colors["editor.background"] ?? "(none stated)";
}
