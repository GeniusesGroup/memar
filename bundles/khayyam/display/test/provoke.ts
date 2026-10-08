// A copy of a file the extension ships, with one change in it.
//
// A refusal is provoked over a copy so the file the editor reads is never touched: a
// check that is asked about a candidate has to be able to refuse it, and the only way
// to ask is to hand it something that is not what ships. Each helper here names which
// file it copies, because a copy without a name says nothing about what was supposed
// to be wrong with it - and each one is read back afterwards where the file it copied
// is the one a reader looks at.
import { copyFileSync, mkdirSync, mkdtempSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { CONTRACT, MANIFEST, THEMES } from "./shipped.ts";

/** A copy of the contract with one change to it, so a refusal can be provoked
 *  without touching the contract the check is here to keep honest. */
export function contractWith(change: (contract: any) => void): string {
  const contract = JSON.parse(readFileSync(CONTRACT, "utf8"));
  change(contract);
  const path = join(mkdtempSync(join(tmpdir(), "khayyam-contract-")), "display.json");
  writeFileSync(path, JSON.stringify(contract, null, 2));
  return path;
}

/** A copy of the manifest with one change to it, for the same reason a copy of the
 *  contract is used: a refusal is provoked without touching the manifest the editor
 *  reads, and the verifier is pointed at the copy by its own second argument. */
export function manifestWith(change: (manifest: any) => void): string {
  const manifest = JSON.parse(readFileSync(MANIFEST, "utf8"));
  change(manifest);
  const path = join(mkdtempSync(join(tmpdir(), "khayyam-manifest-")), "package.json");
  writeFileSync(path, JSON.stringify(manifest, null, 2));
  return path;
}

/** A temporary extension root holding a copy of every theme the extension ships, so the
 *  generator and the check can be asked about the copy and the files the editor reads
 *  are never touched. */
export function themesRoot(): string {
  const root = mkdtempSync(join(tmpdir(), "khayyam-themes-"));
  const dir = join(root, "themes");
  mkdirSync(dir, { recursive: true });
  for (const name of readdirSync(THEMES)) copyFileSync(join(THEMES, name), join(dir, name));
  return root;
}

/** One theme of a copy, with one change to it, for the same reason a copy of the manifest
 *  is used. */
export function themeIn(root: string, file: string, change: (theme: any) => void): void {
  const path = join(root, "themes", file);
  const theme = JSON.parse(readFileSync(path, "utf8"));
  change(theme);
  writeFileSync(path, `${JSON.stringify(theme, null, 2)}\n`);
}
